#!/usr/bin/env python3
"""Exact necessary enumerator tests; no construction or feasibility claim.
All arithmetic is integer, with explicit divisibility checked before division.
"""
from math import comb
from pathlib import Path
import json
N=64
E={0:1,28:448,32:126,36:448,64:1}
def krawtchouk(k,w):
    return sum((-1)**j*comb(w,j)*comb(N-w,k-j)
               for j in range(max(0,k-(N-w)),min(k,w)+1))
def transform(A,size):
    nums=[sum(a*krawtchouk(k,w) for w,a in A.items()) for k in range(N+1)]
    assert all(x%size==0 for x in nums)
    return [x//size for x in nums]
def main():
    B=transform(E,1024)
    assert all(x>=0 for x in B) and sum(B)==2**54
    rows=[]
    for t in range(25):
        A=E|{27:224+4*t,37:224+4*t,29:288-12*t,35:288-12*t,31:8*t,33:8*t}
        assert sum(A.values())==2048
        D=transform(A,2048)
        complement=[b-d for b,d in zip(B,D)]
        assert min(D)>=0 and min(complement)>=0
        assert sum(D)==sum(complement)==2**53
        assert D[0]==1 and complement[0]==0
        assert all(D[k]==complement[k]==0 for k in range(1,65,2))
        # Involution is a separate exact consistency check.
        inv=transform({k:v for k,v in enumerate(D)},2**53)
        assert inv==[A.get(k,0) for k in range(65)]
        rows.append({'t':t,'survives_oct19_condition':t%4==0,
                     'dual_weight_enumerator':D,
                     'complement_in_parent_dual':complement})
    out={'date':'2026-10-20','status':'PASS',
         'parent_dual_weight_enumerator':B,
         'profiles_checked':25,'coefficients_per_profile':65,
         'macwilliams_integrality_nonnegativity_survivors':list(range(25)),
         'oct19_seven_survivors':list(range(0,25,4)),
         'additional_exclusions':0,'profiles':rows,
         'scope':'Formal necessary weight-enumerator tests only. No code, coset or proof of full feasibility/nonexistence is supplied.'}
    Path(__file__).with_name('macwilliams_report.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: all 25 formal profiles pass; no additional exclusion among seven.')
if __name__=='__main__':main()
