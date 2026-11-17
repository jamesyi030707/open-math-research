"""Full B-column stabilizer fixing h and preserving S; exact finite certificate."""
import itertools,json,time
from collections import deque
START=time.process_time()
B=(0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
def dot(x,y):return (x&y).bit_count()%2
def lin(images,x):
 y=0
 for i,v in enumerate(images):
  if x>>i&1:y^=v
 return y
def require(c):
 if not c:raise ValueError('invariant')
cols=[sum(((b>>j)&1)<<i for i,b in enumerate(B)) for j in range(37)]
f={c>>4&31:c&15 for c in cols if dot(c,1008)}
Z=sorted(c&15 for c in cols if not dot(c,1008))
require(len(f)==32 and len(Z)==5 and len(set(cols))==37)
rad={}
for a in range(1,16):
 q=[dot(a,f[x]) for x in range(32)]
 # verify quadratic: each first derivative is affine
 require(all(all((q[x^v]^q[x]^q[v]^q[0])==sum((q[(1<<i)^v]^q[1<<i]^q[v]^q[0]) for i in range(5) if x>>i&1)%2 for x in range(32)) for v in range(32)))
 R=[v for v in range(32) if all(q[x^v]^q[x]^q[v]^q[0]==0 for x in range(32))]
 require(len(R)==2);rad[a]=R[1]
# all linear D preserving Z, via images of four independent members
basisZ=next(z for z in itertools.combinations(Z,4) if len({lin(z,x) for x in range(16)})==16)
invZ={lin(basisZ,x):x for x in range(16)}
valid=[]; stages={"D":0,"radical_linear":0,"affine_difference":0}
for perm in itertools.permutations(Z):
 Dz={basisZ[i]:perm[i] for i in range(4)}
 D=[lin(perm[:4],invZ[1<<i]) for i in range(4)]
 if sorted(lin(D,z) for z in Z)!=Z:continue
 stages["D"]+=1
 dualD={a:sum(dot(a,D[i])<<i for i in range(4)) for a in range(16)}
 pairs=[(rad[dualD[a]],rad[a]) for a in range(1,16)]
 base=next(p for p in itertools.combinations(pairs,5) if len({lin([q[0] for q in p],x) for x in range(32)})==32)
 inv={lin([q[0] for q in base],x):x for x in range(32)}
 L=[lin([q[1] for q in base],inv[1<<i]) for i in range(5)]
 if not all(lin(L,x)==y for x,y in pairs):continue
 stages["radical_linear"]+=1
 diff=[f[lin(L,x)]^lin(D,f[x]) for x in range(32)]
 if diff[0]!=0:continue
 K=[diff[1<<i] for i in range(5)]
 if not all(diff[x]==lin(K,x) for x in range(32)):continue
 stages["affine_difference"]+=1
 transformed=[]
 for col in cols:
  z=col&15;x=col>>4&31;e=dot(col,1008)
  zz=lin(D,z)^lin(K,x);xx=lin(L,x)
  transformed.append(zz^(xx<<4)^((e^(xx.bit_count()%2))<<9))
 require(set(transformed)==set(cols))
 S_action=[sum(dot(s,L[i])<<i for i in range(5)) for s in range(32)]
 valid.append({'D':D,'L':L,'K':K,'S_action':S_action,'permutation':[cols.index(c) for c in transformed]})
E=(1,2,3,4,8,16,28)
orbit=sorted({tuple(sorted(g['S_action'][s] for s in E)) for g in valid})
print(json.dumps({'stages':stages,'Z':Z,'radicals':rad,'group_order':len(valid),'orbit_size':len(orbit),'stabilizer_of_E':sum(tuple(sorted(g['S_action'][s] for s in E))==E for g in valid),'orientations':orbit,'elements':valid,'cpu_seconds':time.process_time()-START},indent=2))
