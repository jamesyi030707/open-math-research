"""One exact split-dual necessary inequality on seven kernel-one counts.
No enumeration of the integer domain and no feasibility claim.
"""
from fractions import Fraction
from collections import Counter
import json
NAMES=['p','q','y10','y14','z8','z12','z16']

def joint(v):
    p,q,y10,y14,z8,z12,z16=v
    groups=[(14,22,14,160),(16,24,12,p),(16,24,16,80-p),
            (16,16,12,q),(16,16,16,31-q),
            (18,18,10,y10),(18,18,14,y14),(18,18,18,160-y10-y14),
            (20,20,8,z8),(20,20,12,z12),(20,20,16,z16),(20,20,20,80-z8-z12-z16)]
    J=Counter({(0,0):1,(0,32):1})
    for r,s,a,count in groups:
        J[a,r]+=count;J[a,s]+=count
    return J

def numerator(v):
    return sum(c*(27-2*a)*((37-2*r)**2-37)//2 for (a,r),c in joint(v).items())

def main():
    zero=[0]*7
    constant=numerator(zero)
    coeff=[]
    for k in range(7):
        e=zero[:];e[k]=1;coeff.append(numerator(e)-constant)
    # This is an identity of affine expressions, not sampled evidence for the whole domain.
    # Each category count enters linearly in joint(). The eight evaluations extract its coefficients.
    witness=[0,0,140,16,8,6,64]
    value=constant+sum(a*b for a,b in zip(coeff,witness))
    assert value==numerator(witness)==-16384
    assert sum(joint(witness).values())==1024
    assert all(c>=0 for c in joint(witness).values())
    from math import gcd
    from functools import reduce
    g=reduce(gcd,[abs(constant)]+list(map(abs,coeff)))
    return {'variables':NAMES,'domain':['0 <= p <= 80','0 <= q <= 31','y10 >= 0, y14 >= 0, y10+y14 <= 160','z8 >= 0, z12 >= 0, z16 >= 0, z8+z12+z16 <= 80','all variables are integers'],
            'numerator_constant':constant,'numerator_coefficients':coeff,'dual_normalization':1024,
            'reduced_numerator_constant':constant//g,'reduced_numerator_coefficients':[a//g for a in coeff],'reduction_gcd':g,
            'prior_witness':dict(zip(NAMES,witness)),'prior_witness_numerator':value,'prior_witness_dual_coefficient':value//1024,
            'scope':'Necessary inequality only for this fixed residual and kernel-one category model. It is a rewrite of the split test, not an additional independent condition; integer domain not solved.'}
if __name__=='__main__':print(json.dumps(main(),indent=2))
