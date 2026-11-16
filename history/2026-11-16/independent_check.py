"""Independent meet-in-the-middle verification, canonical 18 surviving labels, ten external cosets.
No signed-capacity transform used. Enumerates all halves of 27-coordinate vectors.
"""
import json,time,collections
from pathlib import Path
start=time.process_time()
B=(0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
def BW(u):
 v=0
 for i,b in enumerate(B):
  if u>>i&1:v^=b
 return v.bit_count()
def W(t):return ((t&31)<<4)^(1008 if t&32 else 0)
bs=[BW(2^W(t)) for t in range(64)]
h=[t for t,b in enumerate(bs) if b==14]
def enum(vecs):
 n=len(vecs);s=[sum(v[j] for v in vecs) for j in range(16)];last=0
 yield 0,tuple(s)
 for q in range(1,1<<n):
  gray=q^(q>>1);delta=gray^last; k=delta.bit_length()-1
  factor=-2 if gray>>k&1 else 2
  for j in range(16):s[j]+=factor*vecs[k][j]
  yield gray,tuple(s)
  last=gray
ss=json.load(open(Path(__file__).parent.parent/'2026-11-15'/'h.json'))['solutions']
# The 18 are exactly those passing all ten equality sections in previous exploration.
ids=[29,49,56,86,92,118,121,135,138,142,145,159,162,173,193,200,230,236]
out={}
for idx in ids:
 cols=ss[idx]['columns']; words=[sum((((t&v).bit_count()%2)<<j) for j,v in enumerate(cols)) for t in range(64)]
 out[idx]={}
 for rep in (2,3,5,6,8,9,10,11,12,14):
  bs=[BW(rep^W(t)) for t in range(64)];h=[t for t,b in enumerate(bs) if b==14]
  vs=[tuple(1-2*((t&v).bit_count()%2) for t in h) for v in cols]
  left=collections.defaultdict(list)
  for m,s in enum(vs[:13]):left[s].append(m)
  masks=[]
  for m,s in enum(vs[13:]):
   for x in left.get(tuple(-1-z for z in s),[]):
    mask=x|(m<<13)
    if all(27-b<=(mask^v).bit_count()<=b and ((mask^v).bit_count()+b)%4==0 for b,v in zip(bs,words)):masks.append(mask)
  out[idx][rep]=sorted(masks)
print(json.dumps({'domains':out,'cpu_seconds':time.process_time()-start}))
