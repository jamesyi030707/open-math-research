"""Certified W translations and finite transport of excluded restrictions."""
import json,time
from pathlib import Path
from collections import Counter
START=time.process_time()
B=(0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
def dot(x,y):return (x&y).bit_count()%2
def lin(images,x):
 out=0
 for i,v in enumerate(images):
  if x>>i&1:out^=v
 return out
def require(b):
 if not b:raise ValueError('invariant')
cols=[sum(((b>>j)&1)<<i for i,b in enumerate(B)) for j in range(37)]
f={c>>4&31:c&15 for c in cols if dot(c,1008)}
perms=[]
for t in range(32):
 K=[f[(1<<i)^t]^f[1<<i]^f[t] for i in range(5)]
 require(all(f[x^t]^f[x]^f[t]==lin(K,x) for x in range(32)))
 new=[]
 for c in cols:
  z,x,e=c&15,c>>4&31,dot(c,1008)
  zz=z^lin(K,x)^(f[t] if e else 0); xx=x^(t if e else 0)
  new.append(zz^(xx<<4)^((e^dot(xx,31))<<9))
 require(set(new)==set(cols));perms.append([cols.index(c) for c in new])
solutions=json.loads((Path(__file__).parent.parent/'2026-11-15/h.json').read_text())['solutions']
images={}
for i,s in enumerate(solutions):
 for t in range(32):
  pat=tuple(sorted((v^(t if v&32 else 0)) for v in s['columns']))
  if pat not in images:images[pat]=(i,t)
counts=Counter();byE=Counter()
for pat in images:
 ws=[sum(dot(s,v) for v in pat) for s in range(1,32)]
 require(set(ws)<={12,16})
 q=ws.count(12);counts[q]+=1
 if q==24:byE[tuple(s for s,w in enumerate(ws,1) if w==16)]+=1
print(json.dumps({'translation_count':32,'column_permutations':perms,'unique_excluded_restrictions':len(images),'q_counts':dict(counts),'q24_E_counts':[{'E':e,'excluded':n} for e,n in sorted(byE.items())],'transported':[{'columns':p,'source':i,'translation':t} for p,(i,t) in sorted(images.items())],'cpu_seconds':time.process_time()-START},indent=2))
