#!/usr/bin/env python3
"""Exact standard-library checks for the fixed-residual q=28 obstruction.

No solver, target-matrix search, external service, or unbounded enumeration.
The accompanying RESULT.md supplies the proof for arbitrary actual lifts.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from math import comb
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
INPUT_BLOB = '8f76beaa5994563a2980ea9cb87412640d6560b4'
COMMIT = '3157b1c81a69ddb061cc21f9aaeaac93eadd9a11'
CERTIFICATE = [(2,22,0),(3,26,0),(5,8,0),(6,13,1),(8,10,1),
               (9,19,1),(10,14,0),(11,28,0),(12,29,0),(14,23,0)]
C = [1,4,7,13,15]

def require(ok, message):
    if not ok:
        raise ValueError(message)

def parity(v):
    return v.bit_count() & 1

def rank(vectors):
    pivots = {}
    for v in vectors:
        while v:
            i = v.bit_length()-1
            if i not in pivots:
                pivots[i] = v
                break
            v ^= pivots[i]
    return len(pivots)

def word(u, rows):
    value = 0
    for i,row in enumerate(rows):
        if (u>>i)&1:
            value ^= row
    return value

def validate_left_shape(columns, h):
    require(len(columns)==27 and rank(columns)==9 and all(parity(h&v)==0 for v in columns),
            'Actual left-control dimensions/kernel')

def blocks(K):
    unseen = set(range(32))
    result = []
    while unseen:
        a = min(unseen)
        block = sorted(a^k for k in K)
        result.append(block)
        unseen.difference_update(block)
    return result

def require_hyperplanes(windows, certificate):
    for t,n,c in certificate:
        for s in range(32):
            expected = [14] if parity(s&n)==c else [10,14,18]
            require(windows[t][s]==expected, 'Residual hyperplane certificate mismatch')

def compatible_z(windows, K, t):
    result=[]
    for z in range(4):
        possibles={0}
        for block in blocks(K):
            energies={sum((w-12-z)**2 for w in ws)
                      for ws in product(*(windows[t][s] for s in block))
                      if sum(ws)==48+4*z}
            possibles={a+b for a in possibles for b in energies if a+b<=192}
        if 192 in possibles:
            result.append(z)
    return result

def main():
    start=time.process_time()
    raw=(HERE/'inputs/residual_candidate.json').read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    require(blob==INPUT_BLOB, 'Input Git blob mismatch')
    residual=json.loads(raw)
    R=[int(s,16) for s in residual['basis_hex']]
    weights=[word(u,R).bit_count() for u in range(1024)]
    require(rank(R)==10 and Counter(weights)=={0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1},
            'Residual rank or distribution mismatch')
    h=1008
    require([u for u in range(1024) if weights[u]>=27]==[h], 'Heavy residual message')
    S=list(range(0,512,16))
    require(rank(S)==5 and rank(S+[h])==6, 'Subspace dimensions')
    require(all(weights[s]==16 and weights[s^h]==16 for s in S[1:]), 'S residual type')
    # Check the inherited double-even rigidity input, not only the output windows.
    monomials=[1<<i for i in range(10)]+[(1<<i)|(1<<j) for i in range(10) for j in range(i+1,10)]
    evaluations=[sum(int(u&m==m)<<j for j,m in enumerate(monomials))
                 for u in range(1024) if weights[u]==14]
    require(rank(evaluations)==55, 'Inherited quadratic rigidity rank')
    # u=t+(s<<4), t in F2^4, s in F2^5 is a transversal modulo <h>.
    representatives={t^(s<<4) for t in range(16) for s in range(32)}
    require(len(representatives)==512 and not any((u^h) in representatives for u in representatives),
            'Quotient coordinate transversal')
    windows=[]
    for t in range(16):
        coset=[]
        for s in range(32):
            u=t^(s<<4)
            r,rh=weights[u],weights[u^h]
            coset.append([w for w in range(28) if max(27-r,27-rh)<=w<=min(r,rh)
                          and (w+r)%4==0])
        windows.append(coset)
    # The zero message is not subject to nonzero lift lower bound; only t>0
    # is used in the new certificate. It is assigned its actual left weight.
    windows[0][0]=[0]
    require_hyperplanes(windows,CERTIFICATE)
    T=[t for t,n,c in CERTIFICATE]
    pair_xors=sorted(a^b for a,b in combinations(C,2))
    require(pair_xors==T and len(set(pair_xors))==10, 'Five-label pair sum certificate')
    # All possible 2D K, without selecting one orientation or assuming symmetry.
    Ks=sorted({tuple(sorted([0,a,b,a^b])) for a in range(1,32) for b in range(a+1,32)})
    require(len(Ks)==155, 'Number of 2D subspaces')
    seen=Counter()
    for K in Ks:
        require(rank(K)==2, 'Invalid K')
        for t,n,c in CERTIFICATE:
            require(compatible_z(windows,K,t)==[2], 'Coset obstruction mismatch')
            seen['parallel' if all(parity(k&n)==0 for k in K) else 'transverse']+=1
    # Independent tiny arithmetic of the transverse block cases, not a solver.
    transverse={}
    for z in range(4):
        energies=sorted({(14-12-z)**2*2+(x-12-z)**2+(y-12-z)**2
                         for x,y in product([10,14,18],repeat=2) if 28+x+y==48+4*z})
        transverse[str(z)]=energies
    require(transverse=={'0':[16],'1':[12],'2':[0,32],'3':[12]}, 'Block energy arithmetic')
    # Finite redundant terminal check: all unordered 3-column maps F2^4 -> F2^3.
    maps=list(combinations_with_replacement(range(16),3))
    compatible=[v for v in maps if all(sum(parity(t&x) for x in v)==2 for t in T)]
    require(len(maps)==816 and compatible==[], 'Terminal map contradiction')
    parity_classes=[[v for v in range(8) if parity(v)==p] for p in range(2)]
    require(all(len(V)==4 and all((a^b).bit_count()==2 for a,b in combinations(V,2))
                for V in parity_classes), 'Four-vector equidistant positive control')
    # Actual q28 left-matrix control: preserves hA=0, has rank9 and 3 zero-on-S
    # columns. It verifies all moments/blocks but is explicitly not a target lift.
    active=list(range(8,32)) # F2^5 minus U, U=span(1,2,4)
    columns=[(v<<4)|(parity(v)<<9) for v in active]
    for i,low in enumerate([1,2,4,8]):
        columns[i]^=low
    columns += [1,2,3]
    validate_left_shape(columns,h)
    local_weights=[sum(parity((s<<4)&v) for v in columns) for s in range(32)]
    require(Counter(local_weights)=={0:1,12:28,16:3}, 'Actual q28 restriction control')
    zero_columns=[v for v in columns if all(parity(s&v)==0 for s in S)]
    require(zero_columns==[1,2,3], 'Actual three zero-on-S columns')
    K=[0,8,16,24]
    for t in range(16):
        z=sum(parity(t&v) for v in zero_columns)
        ww=[sum(parity((t^(s<<4))&v) for v in columns) for s in range(32)]
        require(sum(ww)==384+32*z and sum((w-12-z)**2 for w in ww)==192,
                'Actual control coset moments')
        require(all(sum(ww[s] for s in block)==48+4*z for block in blocks(K)),
                'Actual control four-message blocks')
    violations=[u for u in range(1,1024)
                if not 27-weights[u]<=sum(parity(u&v) for v in columns)<=weights[u]]
    require(violations, 'Control must not be called a target lift')
    # Explicit corruption regressions; exception-based checks also run under -O.
    bad=[(t,n,c^(t==2)) for t,n,c in CERTIFICATE]
    try:
        require_hyperplanes(windows,bad)
    except ValueError:
        damaged_hyperplane_rejected=True
    else:
        raise ValueError('Damaged certificate was not rejected')
    damaged_columns=columns[:-1] # length26 and only2 zero positions
    try:
        validate_left_shape(damaged_columns,h)
    except ValueError:
        truncated_matrix_rejected=True
    else:
        raise ValueError('Truncated matrix was not rejected')
    # Regression of the published Nov8 formal q28 survivor, not a new search.
    p,q,y10,y14,z8,z12,z16=counts=[32,28,72,32,18,44,18]
    bounds=[p,80-p,q,31-q,y10,y14,160-y10-y14,z8,z12,z16,80-z8-z12-z16]
    require(min(bounds)>=0, 'Nov8 formal survivor count bounds')
    joint=Counter({(0,0):1,(0,32):1})
    entries=[(14,22,14,160),(16,24,12,p),(16,24,16,80-p),
      (16,16,12,q),(16,16,16,31-q),(18,18,10,y10),(18,18,14,y14),
      (18,18,18,160-y10-y14),(20,20,8,z8),(20,20,12,z12),
      (20,20,16,z16),(20,20,20,80-z8-z12-z16)]
    for r,rh,w,n in entries:
        joint[w,r]+=n; joint[w,rh]+=n
    def polynomial_coefficient(n,w,j):
        return sum((-1)**i*comb(w,i)*comb(n-w,j-i)
                   for i in range(max(0,j-(n-w)),min(w,j)+1))
    L={(i,w):polynomial_coefficient(27,w,i) for i in range(28) for w,r in joint}
    Rpoly={(j,r):polynomial_coefficient(37,r,j) for j in range(38) for w,r in joint}
    dual=[]
    for i in range(28):
        for j in range(38):
            numerator=sum(n*L[i,w]*Rpoly[j,r] for (w,r),n in joint.items())
            v,rem=divmod(numerator,1024)
            require(v>=0 and rem==0, 'Nov8 formal survivor split coefficient')
            dual.append(v)
    require(sum(joint.values())==1024 and sum(dual)==2**54, 'Formal survivor masses')
    require(2*6+7-14-2==3, 'Nov8 formal survivor column cut')
    result={
      'verified':True,'input_commit':COMMIT,'input_blob_sha1':blob,
      'input_sha256':hashlib.sha256(raw).hexdigest(),
      'result':'q=28 is impossible for the archived fixed-residual, kernel-one lift branch.',
      'residual_messages_checked':1024,'quadratic_rigidity_rank':55,
      'quotient_representatives_checked':512,'hyperplane_certificates':[
        {'t':t,'normal_in_F2_5':n,'offset':c,'forced_left_weight':14,
         'on_hyperplane_messages':16,'off_hyperplane_allowed_weights':[10,14,18]}
        for t,n,c in CERTIFICATE],
      'two_dimensional_K_checked':155,'K_coset_checks':1550,'orientation_cases':dict(seen),
      'transverse_block_square_sums':transverse,
      'required_coset_square_sum':192,'forced_z_on_ten_cosets':2,
      'five_quotient_labels':C,'ten_pairwise_xors':pair_xors,
      'unordered_three_column_maps_checked':816,'surviving_maps':0,
      'controls':{'equidistant_binary_triples':parity_classes,
        'actual_left_matrix':{'column_labels':columns,'rank':rank(columns),'length':len(columns),
          'zero_on_S_column_labels':zero_columns,'local_weight_distribution':dict(sorted(Counter(local_weights).items())),
          'cosets_with_moment_and_block_checks':16,'residual_lift_violations':len(violations),
          'scope':'Genuine rank-nine left matrix with q28 restriction; not a target lift.'},
        'damaged_hyperplane_rejected':damaged_hyperplane_rejected,
        'truncated_matrix_rejected':truncated_matrix_rejected},
      'previous_formal_q28_survivor':{'integer_coordinates':[6,14,4,7,13,0,18],
        'seven_counts':counts,'domain_rows_checked':11,'split_rows_checked':len(dual),
        'minimum_split_coefficient':min(dual),'dual_mass':sum(dual),'nov8_cut_slack':3,
        'scope':'Still formally feasible under Nov8 checks; now no actual lift in this branch.'},
      'scope':'Excludes only q=28 of this fixed residual/kernel-one branch. No exclusion of q16,20,24, kernel-zero, other residuals, or global [64,11,27] existence. No novelty or external peer-review claim.',
      'cpu_seconds':time.process_time()-start}
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
