"""Independent direct character-table test, no geometry input or solver."""
import itertools,time,json
from collections import Counter
start=time.process_time()
B=[0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897]
def need(p,s):
 if not p:raise ValueError(s)
def bw(u):
 a=0
 for i,b in enumerate(B):
  if u>>i&1:a^=b
 return a.bit_count()
def W(t):return ((t&31)<<4)^(1008 if t>=32 else 0)
# Enumerate dimension-two and dimension-three subspaces by independent bases.
Ts={tuple(sorted((0,a,b,a^b))) for a in range(1,32) for b in range(a+1,32)}
Us=set()
for T in Ts:
 for x in range(1,32):
  if x not in T:Us.add(tuple(sorted(T+tuple(v^x for v in T))))
Ts=sorted(Ts);Us=sorted(Us)
need(len(Ts)==len(Us)==155,'subspace count')
pre={};groups={};secs=(2,3,5,6,8,9,10,11,12,14)
for a in secs:
 H=[t for t in range(64) if bw(a^W(t))==14]
 need(len(H)==16,'section count')
 chars=[tuple(1-2*((t&v).bit_count()%2) for t in H) for v in range(64)]
 for r in (4,24):
  bigbit=0 if r==4 else 32;smallbit=32-bigbit
  pats=[];ids=[]
  for v in range(32):
   raw=chars[v+bigbit];p=tuple(z*raw[0] for z in raw)
   if p not in pats:pats.append(p)
   ids.append(pats.index(p))
  need(len(pats)==16,'orthogonal class count')
  need(all(sum(x*y for x,y in zip(p,q))==16*(i==j) for i,p in enumerate(pats) for j,q in enumerate(pats)),'orthogonal classes')
  # Positive controls from real signed multisets, including repeats/zero.
  for case in range(5):
   labels=list(range(32))+[0,0,7]
   ys=[1 if ((j*7+case*3)%5)<2 else -1 for j in range(len(labels))]
   target=[sum(y*chars[v+bigbit][i] for v,y in zip(labels,ys)) for i in range(16)]
   expected=[sum(y*chars[v+bigbit][0] for v,y in zip(labels,ys) if ids[v]==k) for k in range(16)]
   nums=[sum(x*y for x,y in zip(p,target)) for p in pats]
   need(nums==[16*x for x in expected],'real multiset inversion')
   M=Counter(ids[v] for v in labels)
   need(all(abs(expected[k])<=M[k] and (expected[k]-M[k])%2==0 for k in range(16)),'real multiset capacities')
  groups[a,r]=ids
  for T in Ts:
   small=list(T[1:])+([0] if r==4 else [])
   poss=set()
   for sig in itertools.product((-1,1),repeat=len(small)):
    rhs=[-1-sum(z*chars[v+smallbit][i] for v,z in zip(small,sig)) for i in range(16)]
    numer=[sum(x*y for x,y in zip(p,rhs)) for p in pats]
    if all(x%16==0 for x in numer):poss.add(tuple(x//16 for x in numer))
   pre[a,r,T]=poss
out={4:Counter(),24:Counter()};pairs=0
for U in Us:
 for T in Ts:
  if set(U)&set(T)!={0}:continue
  pairs+=1
  for r in (4,24):
   big=[v for v in range(32) if v not in U and v not in T]+[0]*(2 if r==4 else 3)
   for a in secs:
    mult=Counter(groups[a,r][v] for v in big)
    if not any(all(abs(c[i])<=mult[i] and (c[i]-mult[i])%2==0 for i in range(16)) for c in pre[a,r,T]):out[r][a]+=1;break
   else:raise ValueError(('survivor',U,T,r))
need(pairs==9920,'pair count')
print(json.dumps({'status':'PASS','pairs':pairs,'branches':2,'direct_character_rejections':out,'cpu':time.process_time()-start},indent=2))
