import json,itertools,time
from pathlib import Path
start=time.process_time()
p=Path(__file__).parent
src=json.load(open(p/'result.json')); sols=json.load(open(p.parent/'2026-11-15'/'h.json'))['solutions']
B=(0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
def cw(u):
 r=0
 for i,b in enumerate(B):
  if (u>>i)&1:r^=b
 return r
def W(t):return ((t&31)<<4)^(1008 if t&32 else 0)
BW={a:[cw(a^W(t)).bit_count() for t in range(64)] for a in range(16)}
out={}
for istr,dd in src['full_coset_domains'].items():
 i=int(istr);D={int(a):set(v) for a,v in dd.items()}
 if any(not v for v in D.values()):out[i]={'status':'empty_domain'};continue
 cols=sols[i]['columns'];left=[sum((((t&v).bit_count()&1)<<j) for j,v in enumerate(cols)) for t in range(64)]
 nodes=[0]*4;witness=[]
 def valid(a,m):
  if a in D:return m in D[a]
  return all(27-b<=(m^l).bit_count()<=b and ((m^l).bit_count()+b)%4==0 for b,l in zip(BW[a],left))
 def dfs(level,span):
  if level==4:witness.append(span);return
  a=(2,3,5,8)[level]
  for m in sorted(D[a]):
   nodes[level]+=1
   new={k^a:v^m for k,v in span.items()}
   if all(valid(k,v) for k,v in new.items()):dfs(level+1,span|new)
 dfs(0,{0:0})
 out[i]={'status':'no_common_extension' if not witness else 'extension','candidate_nodes':nodes,'witnesses':witness}
print(json.dumps({'scope':'canonical 277 q24 markings only; fixed residual and kernel0 doubly-even branch','results':out,'cpu_seconds':time.process_time()-start},indent=2))
