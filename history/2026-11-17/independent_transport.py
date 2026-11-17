"""Independent W-translation audit using row operations, not column updates."""
import json,time,hashlib
from collections import Counter
from pathlib import Path
start=time.process_time();root=Path(__file__).resolve().parent
B=[0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897]
def p(x):return bin(x).count('1')%2
def require(x):
 if not x:raise ValueError('transport audit invariant')
points=[sum(((r>>j)&1)<<i for i,r in enumerate(B)) for j in range(37)]
f={x>>4&31:x&15 for x in points if p(x&1008)}
def combine(vectors,u):
 out=0
 for i,r in enumerate(vectors):
  if u>>i&1:out^=r
 return out
permutations=[]
for t in range(32):
 derivative=[f[(1<<i)^t]^f[1<<i]^f[t] for i in range(5)]
 require(all(f[x^t]^f[x]^f[t]==combine(derivative,x) for x in range(32)))
 def F(c):
  e=p(c&1008);x=c>>4&31;z=c&15
  xx=x^(t if e else 0);zz=z^combine(derivative,x)^(f[t] if e else 0)
  return zz^(xx<<4)^((e^p(xx))<<9)
 mapped=list(map(F,points));require(set(mapped)==set(points))
 images=[F(1<<i) for i in range(10)]
 # Independently evaluate the actual transpose on ALL messages.
 for u in range(1024):
  gu=sum(p(u&c)<<i for i,c in enumerate(images))
  require(combine(B,u).bit_count()==combine(B,gu).bit_count())
  if u&15==0:
   s=u>>4&31;eps=u>>9&1
   # coordinates of W: u=(s<<4) xor epsilon*h
   eps=u>>9&1;s=(u^(1008 if eps else 0))>>4
   require(gu==u^(1008 if p(s&t) else 0))
 permutations.append([points.index(x) for x in mapped])
require(len(set(map(tuple,permutations)))==32)
solutions=json.loads((root.parent/'2026-11-15/h.json').read_text())['solutions']; unique={}
for n,sol in enumerate(solutions):
 columns=sol['columns']
 rows=[sum(((c>>i)&1)<<j for j,c in enumerate(columns)) for i in range(6)]
 for t in range(32):
  newrows=[rows[i]^(rows[5] if t>>i&1 else 0) for i in range(5)]+[rows[5]]
  cols=tuple(sorted(sum(((row>>j)&1)<<i for i,row in enumerate(newrows)) for j in range(27)))
  sw=[combine(newrows[:5],s).bit_count() for s in range(1,32)]
  require(set(sw)<={12,16})
  q=sw.count(12);E=tuple(s for s,w in enumerate(sw,1) if w==16)
  unique.setdefault(cols,{'q':q,'E':E,'origin':[n,t]})
counts=Counter(v['q'] for v in unique.values())
e24=Counter(v['E'] for v in unique.values() if v['q']==24)
lines='\n'.join(','.join(map(str,c)) for c in sorted(unique))+'\n'
result={'verified_B_automorphisms':32,'verified_weight_pairs':32*1024,'source_restrictions':len(solutions),'transport_attempts':len(solutions)*32,'distinct_restrictions':len(unique),'q_distribution':dict(sorted(counts.items())),'q24_E_count':len(e24),'q24_counts_by_E':[{'E':e,'restrictions':v} for e,v in sorted(e24.items())],'distinct_patterns_sha256':hashlib.sha256(lines.encode()).hexdigest(),'cpu_seconds':time.process_time()-start}
print(json.dumps(result,indent=2))
