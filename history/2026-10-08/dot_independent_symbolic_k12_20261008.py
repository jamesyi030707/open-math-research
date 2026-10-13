"""Independent exact affine-symbolic check; imports no Claude checker."""
import json
import sys
from fractions import Fraction
from collections import Counter
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().with_name('claude_cert_k12_20261008.json')
c=json.loads(p.read_text()); assert c['k']==12
M=4096
firsts={}; derived={}; residual=[]
for r in range(M):
    # For every q>=0, x=a*q+d exactly; a is even before each tested branch.
    a,d,s=M,r,0
    first=None
    for j in range(1,13):
        assert a%2==0
        if d%2:
            a,d=3*a//2,(3*d+1)//2
            s+=1
        else: a,d=a//2,d//2
        assert a*2**j==M*3**s
        b=2**j*d-3**s*r; D=2**j-3**s
        assert b>=0 and D!=0
        if first is None and D>0:
            nmin=r if r>=2 else r+M
            assert b<D*nmin
            first=j
            e=j; z=r%(2**e); n0=z if z>=2 else z+2**e
            assert b<D*n0
            item={'len':e,'res':z,'s':s,'b':b,'D':D,'nmin':n0}
            key=(e,z)
            if key in derived: assert derived[key]==item
            derived[key]=item
        if first is None: assert D<0
    firsts[r]=first
    if first is None: residual.append(r)
assert len(c['prefixes'])==len(derived)==57
assert {(p['len'],p['res']) for p in c['prefixes']}==set(derived)
for p in c['prefixes']: assert p==derived[(p['len'],p['res'])]
assert sorted(c['open'])==residual and len(residual)==226
cover=Counter(r for p in c['prefixes'] for r in range(p['res'],M,2**p['len']))
assert len(cover)==3870 and set(cover.values())=={1}
assert set(cover).isdisjoint(residual) and set(cover)|set(residual)==set(range(M))
w=sum((Fraction(1,2**p['len']) for p in c['prefixes']),Fraction())
assert w==Fraction(1935,2048)
print('EXACT SYMBOLIC CHECK PASSED: all q>=0, with n=0,1 excluded from descent theorem.')
print('57 prefixes; 3870 covered classes; 226 residual classes; weight',w)
print('First strict descent length counts:',dict(sorted(Counter(p['len'] for p in c['prefixes']).items())))
print('For every integer n>1: sigma(n)<=12 iff n mod 4096 is covered; certified length equals sigma(n).')
print('This proves the finite-horizon classification and density, not the Collatz conjecture.')
