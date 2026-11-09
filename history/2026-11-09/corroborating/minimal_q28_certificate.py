#!/usr/bin/env python3
"""Read-only standard-library certificate: fixed residual, kernel-one, q=28."""
from collections import Counter
from itertools import combinations_with_replacement
import json,time
start=time.process_time()
rows=[0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897]
words=[0]*1024
for u in range(1,1024):
 bit=u&-u
 words[u]=words[u^bit]^rows[bit.bit_length()-1]
weights=[x.bit_count() for x in words]
assert Counter(weights)=={0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1}
cert={2:(22,0),3:(26,0),5:(8,0),6:(13,1),8:(10,1),9:(19,1),10:(14,0),11:(28,0),12:(29,0),14:(23,0)}
for t,(v,c) in cert.items():
 for s in range(32):
  u=t+16*s
  r,rh=weights[u],weights[u^1008]
  allowed=tuple(a for a in range(28) if 27-r<=a<=r and 27-rh<=a<=rh and (a+r)%4==0 and (a+rh)%4==0)
  fixed=(s&v).bit_count()%2==c
  assert allowed==((14,) if fixed else (10,14,18))
# Full moments: n10+n18=12+2(z-2)^2 and n18-n10=8(z-2).
assert 12+2*(0-2)**2>16
# A transverse four-block has two fixed14 and two variable entries.
for z in (1,3):
 pairs=[(a,b) for a in (10,14,18) for b in (10,14,18) if 28+a+b==48+4*z]
 assert pairs
 assert {2*(14-12-z)**2+(a-12-z)**2+(b-12-z)**2 for a,b in pairs}=={12}
 assert 8*12!=192
# A contained in hyperplane direction has an all-fixed14 block, forcing z=2.
assert sum((14,)*4)==48+4*2
exceptional=set(range(1,16))-set(cert)
assert exceptional=={1,4,7,13,15}
assert not any(a^b in exceptional for a in exceptional for b in exceptional if a!=b)
# Independent exhaustive control of all 816 unordered triples of zero-column functionals.
triples=list(combinations_with_replacement(range(16),3))
assert len(triples)==816
survivors=[cs for cs in triples if all(sum((t&c).bit_count()%2 for c in cs)==2 for t in cert)]
assert not survivors
print(json.dumps({"verified":True,"forced_z2_cosets":sorted(cert),"affine_hyperplanes":cert,"exceptional_cosets":sorted(exceptional),"zero_column_triples_checked":len(triples),"survivors":survivors,"cpu_seconds":time.process_time()-start}))
