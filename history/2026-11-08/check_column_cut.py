#!/usr/bin/env python3
"""Exact bounded certificate checks for the fixed residual/kernel-one cut.

Python standard library only. Does not search matrices or rely on solver status.
"""
from collections import Counter
from math import comb
from pathlib import Path
import csv
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
NAMES = ['p', 'q', 'y10', 'y14', 'z8', 'z12', 'z16']

def require(ok, message):
    if not ok:
        raise ValueError(message)

def parity(x):
    return x.bit_count() & 1

def rank(values):
    basis = {}
    for v in values:
        while v:
            k = v.bit_length() - 1
            if k not in basis:
                basis[k] = v
                break
            v ^= basis[k]
    return len(basis)

def word(u, rows):
    result = 0
    for j, row in enumerate(rows):
        if (u >> j) & 1:
            result ^= row
    return result

def forward(u):
    a,b,c,d,e,f,g = u
    return [4+64*a-16*b+4*d-4*e-6*f-6*g, 4*d,
            6+8*c-4*d+2*e+2*g, -4+16*b-16*c-4*e-4*g,
            2*f+g, 2*e+g, g]

def joint(x):
    p,q,y10,y14,z8,z12,z16 = x
    entries = [(14,22,14,160),(16,24,12,p),(16,24,16,80-p),
               (16,16,12,q),(16,16,16,31-q),
               (18,18,10,y10),(18,18,14,y14),
               (18,18,18,160-y10-y14),
               (20,20,8,z8),(20,20,12,z12),(20,20,16,z16),
               (20,20,20,80-z8-z12-z16)]
    result = Counter({(0,0):1, (0,32):1})
    for r,s,w,n in entries:
        require(n >= 0, 'Negative source category')
        result[w,r] += n
        result[w,s] += n
    return result

def kraw(n, j, w):
    return sum((-1)**i * comb(w,i) * comb(n-w,j-i)
               for i in range(max(0,j-(n-w)), min(w,j)+1))

def check_point(u, domains, table, original):
    x = forward(u)
    p,q,y10,y14,z8,z12,z16 = x
    domain = [p,80-p,q,31-q,y10,y14,160-y10-y14,
              z8,z12,z16,80-z8-z12-z16]
    require(all(v >= 0 for v in domain), 'Count domain')
    actual_domain = [int(r['constant']) + sum(int(r[k])*v for k,v in zip('abcdefg',u))
                     for r in domains]
    require(actual_domain == domain, 'Transported domain mismatch')
    J = joint(x)
    require(sum(J.values()) == 1024, 'Joint mass')
    require(all((w+r) % 4 == 0 for w,r in J), 'Doubly even source support')
    left = {(i,w):kraw(27,i,w) for i in range(28) for w in {w for w,r in J}}
    right = {(j,r):kraw(37,j,r) for j in range(38) for r in {r for w,r in J}}
    values = []
    for i in range(28):
        for j in range(38):
            n = sum(n*left[i,w]*right[j,r] for (w,r),n in J.items())
            v, rem = divmod(n,1024)
            require(rem == 0 and v >= 0, 'Direct split transform invalid')
            index = i*38+j
            row = table[index]
            require(v == int(row['constant']) + sum(int(row[k])*v0 for k,v0 in zip('abcdefg',u)),
                    'Integer coefficient mismatch')
            row = original[index]
            original_n = int(row['constant']) + sum(int(row[k])*v0 for k,v0 in zip(NAMES,x))
            require(int(row['denominator']) == 1024 and original_n == n,
                    'Original affine coefficient mismatch')
            values.append(v)
    require(sum(values) == 2**54, 'Split dual mass')
    a,b,c,d,e,f,g = u
    require(values[38] == a-6 and values[39] == b-3*a+4,
            'Low-degree dual coefficients')
    return {'integer_parameters':u, 'seven_counts':x,
            'domain_constraints_checked':11, 'split_positions_checked':1064,
            'nonnegative_integral_split_coefficients':True,
            'split_coefficient_sum':sum(values),
            'q_at_least_16':q >= 16,
            'T_1_0':values[38], 'T_1_1':values[39],
            'columns_zero_on_S_if_realizable':d-4,
            'zero_column_inclusion_slack':d+2-a,
            'new_cut_slack':2*a+d-b-2}

def check_matrix_control(cols, B, h, S):
    require(all(parity(v&h) == 0 for v in cols), 'h not in A kernel')
    zeroS = sum(all(parity(s&v) == 0 for s in S) for v in cols)
    zero = cols.count(0)
    coincidences = sum(v == w for v in cols for w in B)
    slack = zeroS-zero-coincidences
    complement = [v for v in cols if all(parity(s&v) == 0 for s in S)
                  and v != 0 and v not in B]
    require(slack == len(complement) and slack >= 0, 'Column-count control')
    return {'length':len(cols), 'rank':rank(cols), 'column_labels':cols,
            'zero_on_S':zeroS, 'globally_zero':zero,
            'A_B_column_coincidences':coincidences, 'cut_slack':slack,
            'scope':'Actual left matrix control; not a target-code construction.'}

def main():
    start = time.process_time()
    sources = json.loads((HERE/'input_sources.json').read_text())
    for rec in sources['files']:
        data = (HERE/rec['local']).read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob == rec['git_blob_sha'], 'Pinned input blob mismatch')
    rdata = json.loads((HERE/'inputs/residual_candidate.json').read_text())
    rows = [int(x,16) for x in rdata['basis_hex']]
    require(rank(rows) == 10, 'Residual rank')
    weights = [word(u,rows).bit_count() for u in range(1024)]
    require(Counter(weights) == {0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1},
            'Residual distribution')
    # Recheck the fixed-input rank condition behind the inherited doubly-even
    # normalization: an even left code has q_A=wt(A)/2 mod2 quadratic, and all
    # weight-14 residual messages force q_A=q_B=1.
    monomials = [1 << i for i in range(10)] + [
        (1 << i) | (1 << j) for i in range(10) for j in range(i+1,10)]
    evaluations = [sum(int(u & mask == mask) << j for j,mask in enumerate(monomials))
                   for u in range(1024) if weights[u] == 14]
    require(len(evaluations) == 160 and rank(evaluations) == 55,
            'Doubly-even rigidity rank condition')
    require([u for u,w in enumerate(weights) if w >= 27] == [1008], 'Unique heavy message')
    h = 1008
    S = list(range(0,512,16))
    require(rank(S) == 5 and rank(S+[h]) == 6, 'Subspace ranks')
    require(all((s^t) in S for s in S for t in S), 'S closure')
    pairs = {min(u,u^h) for u in range(1024) if weights[u] == weights[u^h] == 16}
    require(pairs == set(S[1:]), 'S category identification')
    B = [sum(((r>>j)&1)<<i for i,r in enumerate(rows)) for j in range(37)]
    require(0 not in B and len(set(B)) == 37, 'B nonzero distinct columns')
    compatible = [v for v in B if parity(v&h) == 0]
    require(sorted(compatible) == [1,4,7,13,15], 'Compatible B columns')
    require(all(parity(v&s) == 0 for v in compatible for s in S),
            'Compatible B columns not zero on S')
    # The cut is an exact count identity for ANY matrix with hA=0.
    # Exhaust all 512 individually permitted 10-bit columns as a finite control.
    allowed = [v for v in range(1024) if parity(v&h) == 0]
    for v in allowed:
        zS = all(parity(v&s) == 0 for s in S)
        require(int(zS)-int(v==0)-B.count(v) in [0,1], 'Per-column lemma')
    exhaustive = check_matrix_control(allowed,B,h,S)
    # Lift the published genuine q=16 local code to an actual rank-nine A.
    local = list(range(1,16)) + [19,19,23,23,27,27,28,28,29,29,30,30]
    cols = [(v<<4)|(parity(v)<<9) for v in local]
    for position,low in [(16,1),(18,2),(20,4),(22,8)]:
        cols[position] |= low
    saturated = check_matrix_control(cols,B,h,S)
    require(saturated['rank'] == 9 and saturated['cut_slack'] == 0, 'Saturated control')
    local_weights = [sum(parity(s&v) for v in cols) for s in S]
    require(Counter(local_weights) == {0:1,12:16,16:15}, 'Local code weights')
    violations = [u for u in range(1,1024)
                  if not (27-weights[u] <= sum(parity(u&v) for v in cols) <= weights[u])]
    require(violations, 'Do not mislabel left control as lift')
    saturated['residual_lift_violations'] = len(violations)
    saturated['local_weight_distribution'] = dict(sorted(Counter(local_weights).items()))
    domains = list(csv.DictReader((HERE/'inputs/domain_inequalities.csv').open()))
    table = list(csv.DictReader((HERE/'inputs/integer_coefficients.csv').open()))
    original = list(csv.DictReader((HERE/'inputs/affine_coefficients.csv').open()))
    expected_positions = [(i,j) for i in range(28) for j in range(38)]
    require(len(domains) == 11, 'Domain length')
    for records in [table,original]:
        require([(int(r['i']),int(r['j'])) for r in records] == expected_positions,
                'Complete split table')
    rejected = check_point([6,19,10,4,-31,-33,66],domains,table,original)
    require(rejected['seven_counts'] == [26,16,140,0,0,4,66], 'Witness counts')
    require(rejected['zero_column_inclusion_slack'] == 0 and rejected['new_cut_slack'] == -5,
            'Nonredundancy witness')
    survivors = [check_point([6,14,4,d,13,0,18],domains,table,original) for d in range(4,8)]
    require(all(r['new_cut_slack'] >= 0 for r in survivors), 'Surviving formal points')
    # Corruption controls: invalid original count and one coefficient alteration.
    damaged = [6,19,10,8,-31,-33,66]
    try:
        check_point(damaged,domains,table,original)
    except ValueError:
        corrupted_count_rejected = True
    else:
        raise ValueError('Invalid q was not rejected')
    altered = [dict(row) for row in table]
    altered[39]['constant'] = str(int(altered[39]['constant'])+1)
    try:
        check_point([6,19,10,4,-31,-33,66],domains,altered,original)
    except ValueError:
        corrupted_coefficient_rejected = True
    else:
        raise ValueError('Altered coefficient was not rejected')
    out = {'verified':True, 'input_commit':sources['commit'],
           'minimum_word_quadratic_evaluation_rank':55,
           'residual_columns':B, 'compatible_B_columns':sorted(compatible),
           'compatible_column_positions_zero_based':[j for j,v in enumerate(B) if v in compatible],
           'permitted_columns_checked':len(allowed),
           'new_necessary_cut':'2*a+d-b-2 >= 0',
           'equivalent_count_cut':'p+5*q-2*y10-y14+3*z8+2*z12+z16-60 >= 0',
           'rejected_formal_point':rejected, 'surviving_formal_points':survivors,
           'controls':{'all_allowed_columns':exhaustive,
                       'rank_nine_saturated_left_matrix':saturated,
                       'corrupted_count_rejected':corrupted_count_rejected,
                       'corrupted_coefficient_rejected':corrupted_coefficient_rejected},
           'scope':'Only the archived fixed residual and kernel-one branch. The new cut rejects every labelling of the displayed formal point. It does not exclude the entire branch or any remaining q value, construct a target code, or resolve global [64,11,27] existence.',
           'cpu_seconds':time.process_time()-start}
    print(json.dumps(out,indent=2))

if __name__ == '__main__':
    main()
