#!/usr/bin/env python3
"""Independent exact audit of the fixed-residual parity-period obstruction.

No imports from the proposed proof checker. Standard library only; explicit
exceptions preserve acceptance checks under Python -O.
"""
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_SHA = '276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80'
EXPECTED_CERT = [(2,22,0),(3,26,0),(5,8,0),(6,13,1),(8,10,1),
                 (9,19,1),(10,14,0),(11,28,0),(12,29,0),(14,23,0)]

def require(value, label):
    if not value:
        raise RuntimeError(label)

def bit(x):
    return x.bit_count() & 1

def binary_rank(vectors):
    work = list(vectors)
    pivots = 0
    while work:
        p = max(work)
        if p == 0:
            break
        work.remove(p)
        lead = 1 << (p.bit_length()-1)
        work = [x ^ p if x & lead else x for x in work]
        pivots += 1
    return pivots

def span(vectors):
    out = {0}
    for v in vectors:
        out |= {x ^ v for x in out}
    return out

def reject(call, label):
    try:
        call()
    except RuntimeError:
        return True
    raise RuntimeError('Corrupted control accepted: ' + label)

def verify_certificate(windows, certificate):
    for t,n,c in certificate:
        for s in range(32):
            expected = (14,) if bit(n & s) == c else (10,14,18)
            require(windows[t][s] == expected, 'Residual hyperplane certificate')

def check_actual_matrix(columns, n, c):
    # A column is the six-bit label (five S bits, one quotient bit).
    # t=1 gives the signed sum used by the lemma. All weights come from this
    # actual binary generator matrix, not an invented weight histogram.
    require(len(columns) == 27, 'Control length')
    counts = Counter(v & 31 for v in columns)
    L = 27 - counts[0]
    z = sum(v >> 5 for v in columns if v & 31 == 0)
    signed = [sum(1 - 2*(v >> 5) for v in columns if v & 31 == x)
              for x in range(32)]
    direct = [sum(bit(v & (s | 32)) for v in columns) for s in range(32)]
    require(all(direct[s] == 14 for s in range(32) if bit(n&s) == c),
            'Actual control is not constant fourteen')
    for s,w in enumerate(direct):
        require(sum(signed[v] * (1-2*bit(v&s)) for v in range(32)) == 27-2*w,
                'Full character expansion')
        require(2*w == L+2*z-sum(signed[v]*(1-2*bit(v&s)) for v in range(1,32)),
                'Active-column character expansion')
    sign = 1-2*c
    require(signed[0] == 27-L-2*z, 'Zero coefficient')
    require(signed[n] == (L+2*z-28)*sign, 'Special coefficient sign/normalization')
    for v in range(1,32):
        require((signed[v]-counts[v]) % 2 == 0, 'Signed multiplicity parity')
        if v != n:
            require(signed[v]+sign*signed[v^n] == 0, 'Nonconstant pair coefficient')
    f = [L%2] + [counts[v]%2 for v in range(1,32)]
    require(all(f[v] == f[v^n] for v in range(32)), 'Artificial-zero parity period')
    wrong_f = [counts[v]%2 for v in range(32)]
    require(wrong_f[0] != wrong_f[n], 'Wrong zero coefficient must fail')
    return {'rank': binary_rank(columns), 'active': L, 'zero_positions': counts[0],
            'zero_weight': z, 'max_restriction_multiplicity': max(counts.values()),
            'coefficient_at_n': signed[n]}

def check_old_formal_point(q):
    # Independent three-term Krawtchouk recurrence, not polynomial multiplication
    # or the archived affine coefficient arrays.
    def krawtchouk(n,a):
        values = [1,n-2*a]
        for j in range(1,n):
            numerator = (n-2*a)*values[j]-(n-j+1)*values[j-1]
            value,remainder = divmod(numerator,j+1)
            require(remainder==0, 'Exact Krawtchouk recurrence')
            values.append(value)
        return values
    p,y10,y14,z8,z12,z16 = q+4,100-q,32,18,44,18
    bounds = [p,80-p,q,31-q,y10,y14,160-y10-y14,z8,z12,z16,80-z8-z12-z16]
    require(min(bounds)>=0, 'Old count domain')
    distribution = Counter({(0,0):1,(0,32):1})
    categories = [(14,22,14,160),(16,24,12,p),(16,24,16,80-p),
                  (16,16,12,q),(16,16,16,31-q),
                  (18,18,10,y10),(18,18,14,y14),(18,18,18,160-y10-y14),
                  (20,20,8,z8),(20,20,12,z12),(20,20,16,z16),
                  (20,20,20,80-z8-z12-z16)]
    for b,b2,a,count in categories:
        distribution[a,b]+=count
        distribution[a,b2]+=count
    require(sum(distribution.values())==1024, 'Old formal mass')
    left = {a:krawtchouk(27,a) for a,b in distribution}
    right = {b:krawtchouk(37,b) for a,b in distribution}
    transform = {}
    for i in range(28):
        for j in range(38):
            numerator=sum(count*left[a][i]*right[b][j] for (a,b),count in distribution.items())
            value,remainder=divmod(numerator,1024)
            require(remainder==0 and value>=0, 'Old integral nonnegative split transform')
            transform[i,j]=value
    require(sum(transform.values())==2**54, 'Old formal dual mass')
    slack=q//4-4-transform[1,0]-transform[1,1]
    require(slack==q//4-4 and slack>=0, 'Old incidence cut')
    return {'counts':[p,q,y10,y14,z8,z12,z16], 'bounds_checked':len(bounds),
            'split_coefficients_checked':len(transform),'incidence_slack':slack,
            'still_formally_feasible':True}

def main():
    start = time.process_time()
    raw = (HERE/'inputs/residual_candidate.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_SHA, 'Input SHA256')
    data = json.loads(raw)
    basis = [int(x,16) for x in data['basis_hex']]
    require(len(basis)==10 and all(0 <= x < (1<<37) for x in basis), 'Residual shape')
    # Recurrence expansion, independent of the prior per-message dot-product code.
    words = [0]
    for row in basis:
        words += [x ^ row for x in words]
    require(len(set(words))==1024, 'Residual dimension')
    weights = [x.bit_count() for x in words]
    require(Counter(weights)=={0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1},
            'Residual weight distribution')
    heavy = [u for u in range(1,1024) if weights[u] >= 27]
    require(heavy == [1008], 'Unique nonzero left-kernel candidate')
    h = heavy[0]
    S = [s << 4 for s in range(32)]
    require(h not in S and len(span([1,2,4,8,16,32,64,128,256,h]))==1024,
            'Quotient coordinate decomposition')
    require(all(weights[u]==weights[u^h]==16 for u in S if u), 'S residual pairs')

    # For an even code, wt/2 mod2 is a quadratic polynomial with zero constant.
    # The residual weight14 messages force total weight28, so rank55 certifies
    # every coefficient zero and hence the inherited double-even normalization.
    monomials = [(i,) for i in range(10)] + list(itertools.combinations(range(10),2))
    evaluation_rows = []
    for u,w in enumerate(weights):
        if w == 14:
            mask = 0
            for j,indices in enumerate(monomials):
                if all(u & (1<<i) for i in indices):
                    mask |= 1<<j
            evaluation_rows.append(mask)
    require(len(evaluation_rows)==160 and binary_rank(evaluation_rows)==55,
            'Rank55 quadratic rigidity')

    windows = []
    for t in range(16):
        row = []
        for s in range(32):
            u = t | (s << 4)
            if u == 0:
                allowed = (0,)
            else:
                allowed = tuple(a for a in range(28)
                                if 27 <= a+weights[u] and 27 <= a+weights[u^h]
                                and a <= weights[u] and a <= weights[u^h]
                                and (a+weights[u])%4 == 0)
            row.append(allowed)
        windows.append(row)
    require(windows[0][0] == (0,), 'Zero-message exception')
    require(all(windows[0][s] == (12,16) for s in range(1,32)), 'S weights')
    # Recover the certificate, rather than merely validating supplied normals.
    recovered = []
    for t in range(1,16):
        for n in range(1,32):
            for c in (0,1):
                if all(windows[t][s] == ((14,) if bit(n&s)==c else (10,14,18))
                       for s in range(32)):
                    recovered.append((t,n,c))
    require(recovered==EXPECTED_CERT, 'Complete recovered hyperplane list')
    verify_certificate(windows, recovered)
    normals = [n for _,n,_ in recovered]
    require(binary_rank(normals)==5 and span(normals)==set(range(32)), 'Normals span F2^5')
    independent_normals = []
    for n in normals:
        if binary_rank(independent_normals+[n]) > len(independent_normals):
            independent_normals.append(n)
    bad = list(recovered)
    t,n,c = bad[0]
    bad[0] = (t,n,c^1)
    rejected_offset = reject(lambda:verify_certificate(windows,bad), 'hyperplane offset')

    cases = []
    for q in range(32):
        total_weight = 12*q + 16*(31-q)
        if total_weight%16:
            continue
        L = total_weight//16
        if L > 27:
            continue
        centered4 = L*L + q*(24-L)**2 + (31-q)*(32-L)**2
        require(centered4%32==0, 'Integral squared multiplicity sum')
        squares = centered4//32
        require(squares==992-14*q-L*L, 'Independent moment derivations agree')
        if L%2:
            require(L<31, 'All31 multiplicities odd gives contradiction')
            reason = 'All 31 nonzero multiplicities odd would require at least 31 active columns.'
        else:
            require(squares<2*L, 'Even-multiplicity moment contradiction')
            reason = 'Every multiplicity even implies sum(m^2)>=2*sum(m), violating the exact moment.'
        cases.append({'q':q,'L':L,'sum_m_squared':squares,'contradiction':reason})
    require([(x['q'],x['L'],x['sum_m_squared']) for x in cases]
            ==[(16,27,39),(20,26,36),(24,25,31),(28,24,24)], 'Complete q cases')

    # 186 real generator matrices: every nonzero normal, either offset, three
    # deterministic repeated-column profiles. Pair character terms cancel on
    # the requested hyperplane; a singleton supplies sign sum -1, i.e. weight14.
    controls = []
    max_mult = 0
    zero_values = set()
    n_coeff_signs = set()
    for n in range(1,32):
        representatives = [v for v in range(32) if v < (v^n)]
        for c in (0,1):
            for profile in range(3):
                if profile == 0:
                    chosen = representatives[:13]
                elif profile == 1:
                    chosen = representatives[1:12]+[representatives[1],representatives[2]]
                else:
                    chosen = [representatives[0]]*3+representatives[1:11]
                require(len(chosen)==13, 'Control pair count')
                columns = [n | ((1-c)<<5)]
                for j,v in enumerate(chosen):
                    e = (j+profile)&1
                    columns.extend([v | (e<<5), (v^n) | ((e^(1-c))<<5)])
                result = check_actual_matrix(columns,n,c)
                result.update(n=n,c=c,profile=profile)
                controls.append(result)
                max_mult=max(max_mult,result['max_restriction_multiplicity'])
                zero_values.add(result['zero_weight'])
                n_coeff_signs.add((result['coefficient_at_n']>0)-(result['coefficient_at_n']<0))
    require(len(controls)==186 and max_mult>=3 and 0 in zero_values and 1 in zero_values,
            'Control coverage')
    require(-1 in n_coeff_signs and 1 in n_coeff_signs, 'Special coefficient signs exercised')
    # Independent extension of a genuine q20 restriction. Its restricted column
    # list was supplied as a candidate and is verified directly here. Quotient
    # bits are assigned to singles, unlike the originator's double-column
    # extension, and the zero-on-S column is nonzero on the quotient.
    q20_active = [1,3,5,7,9,11,13,14,14,15,17,19,21,22,22,23,25,26,26,
                  27,28,28,29,30,30,31]
    q20_counts = Counter(q20_active)
    q20_columns = [(v<<4) | (bit(v)<<9) for v in q20_active]
    for j,delta in zip((0,1,2,3),(1,2,4,8)):
        q20_columns[j] ^= delta
    q20_columns.append(4)
    require(binary_rank(q20_columns)==9 and all(bit(v&h)==0 for v in q20_columns),
            'Independent q20 left-control rank and h-kernel')
    q20_weights = [sum(bit(u&v) for v in q20_columns) for u in range(1024)]
    require([u for u,w in enumerate(q20_weights) if w==0]==[0,h], 'Exact q20 left kernel')
    require(Counter(q20_weights[s<<4] for s in range(32))=={0:1,12:20,16:11},
            'Actual q20 restriction weights')
    require(sum(m*m for m in q20_counts.values())==36, 'Actual q20 squared multiplicities')
    q20_energy_checks = 0
    for t in range(16):
        z = sum(bit(t&v) for v in q20_columns if v&496==0)
        a = [sum(1-2*bit(t&v) for v in q20_columns if (v>>4)&31==j)
             for j in range(1,32)]
        require(sum((q20_weights[t|(s<<4)]-13-z)**2 for s in range(32))
                ==8*sum(x*x for x in a), 'Actual q20 coset energy')
        q20_energy_checks += 1
    q20_lift_failures = [u for u in range(1,1024)
                         if not 27-weights[u] <= q20_weights[u] <= weights[u]]
    q20_double_even_failures = [u for u in range(1024)
                               if (q20_weights[u]+weights[u])%4]
    q20_forced_point_failures = [(t,s) for t,n,c in recovered for s in range(32)
                                if bit(n&s)==c and q20_weights[t|(s<<4)]!=14]
    require(q20_lift_failures and q20_double_even_failures and q20_forced_point_failures,
            'Local q20 control must not be mistaken for a target lift')
    out = {
        'verified': True,
        'scope':'Excludes only the archived residual B in the normalized even-subcode left-projection kernel dimension one branch.',
        'input_sha256':EXPECTED_SHA,
        'residual_messages':len(words),
        'quadratic_evaluation_rank':binary_rank(evaluation_rows),
        'zero_message_window':windows[0][0],
        'hyperplane_certificate':recovered,
        'normal_rank':binary_rank(normals),
        'independent_normals':independent_normals,
        'normal_span_size':len(span(normals)),
        'branch_cases':cases,
        'actual_matrix_controls':len(controls),
        'control_ranks':dict(sorted(Counter(x['rank'] for x in controls).items())),
        'control_zero_position_counts':sorted(set(x['zero_positions'] for x in controls)),
        'control_zero_weights':sorted(zero_values),
        'control_max_multiplicity':max_mult,
        'control_special_coefficient_signs':sorted(n_coeff_signs),
        'control_scope':'Actual six-message-bit length27 binary matrices checking the general hyperplane lemma. Not claimed q16/q20 restrictions or target residual lifts.',
        'q20_local_control':{
            'columns':q20_columns,
            'rank':binary_rank(q20_columns),
            'kernel':[0,h],
            'restriction_distribution':dict(Counter(q20_weights[s<<4] for s in range(32))),
            'squared_multiplicity_sum':36,
            'coset_energy_checks':q20_energy_checks,
            'full_lift_failures':len(q20_lift_failures),
            'double_even_failures':len(q20_double_even_failures),
            'forced14_point_failures':len(q20_forced_point_failures),
            'not_target':True,
        },
        'old_formal_points':[check_old_formal_point(16),check_old_formal_point(20)],
        'corrupt_offset_rejected':rejected_offset,
        'wrong_artificial_zero_rejected_in_controls':186,
        'no_search_or_solver':True,
        'cpu_seconds':time.process_time()-start,
    }
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
