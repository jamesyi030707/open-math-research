import json,time,itertools
from pathlib import Path
start=time.process_time()
B=(0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
def BW(u):
 v=0
 for i,b in enumerate(B):
  if u>>i&1:v^=b
 return v.bit_count()
def W(t):return ((t&31)<<4)^(1008 if t&32 else 0)
p=Path(__file__).parent
ss=json.load(open(p.parent/'2026-11-15'/'h.json'))['solutions'];dd=json.load(open(p/'independent_result.json'))['domains']
weights={a:[BW(a^W(t)) for t in range(64)] for a in range(16)}
out={}
for idx,ds in dd.items():
 if any(not d for d in ds.values()):continue
 cols=ss[int(idx)]['columns'];words=[sum((((t&v).bit_count()%2)<<j) for j,v in enumerate(cols)) for t in range(64)]
 def valid(a,x):
  return all(27-b<=(x^v).bit_count()<=b and ((x^v).bit_count()+b)%4==0 for b,v in zip(weights[a],words))
 # Span 2 and 3 contains 1; add 5 and check all newly induced cosets.
 pairs=[(x,y) for x in ds['2'] for y in ds['3'] if valid(1,x^y)]
 triples=[(x,y,z) for x,y in pairs for z in ds['5'] if valid(7,x^z) and valid(6,y^z) and valid(4,x^y^z)]
 out[idx]={'pairs_2_3':len(pairs),'triples_2_3_5':len(triples)}
print(json.dumps({'scope':'canonical 18 survivors, exact linear compatibility of first three quotient basis rows','counts':out,'cpu_seconds':time.process_time()-start},indent=2))
