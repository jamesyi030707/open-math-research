import itertools,json,time
from collections import Counter
start=time.process_time()
rows=[0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897]
w=[]
for u in range(1024):
 b=0
 for i,r in enumerate(rows):
  if u>>i&1:b^=r
 w.append(b.bit_count())
assert Counter(w)=={0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1}
allowed={}
for u in range(1,512):
 r,s=w[u],w[u^1008]
 allowed[u]=tuple(a for a in range(28) if 27-r<=a<=r and 27-s<=a<=s and (a+r)%4==0 and (a+s)%4==0)
planes=sorted({tuple(sorted((0,a,b,a^b))) for a in range(1,32) for b in range(a+1,32)})
assert len(planes)==155
summary=Counter(); survivors=[]; first_fail=Counter(); sample=None; masks_counts=Counter()
for A in planes:
 blocks=[];unused=set(range(32))
 while unused:
  block=tuple(sorted(min(unused)^a for a in A));blocks.append(block);unused.difference_update(block)
 masks=[]
 for t in range(1,16):
  zs=[]
  for z in range(4):
   energies={0}; witness={0:[]}
   for block in blocks:
    opts={}
    for aa in itertools.product(*(allowed[t+(s<<4)] for s in block)):
     if sum(aa)==48+4*z:
      e=sum((a-12-z)**2 for a in aa)
      if e<=192:opts[e]=aa
    new={}
    for e,hist in witness.items():
     for d,aa in opts.items():
      if e+d<=192:new[e+d]=hist+[aa]
    witness=new;energies=set(witness)
    if not energies:break
   if 192 in energies:
    zs.append(z)
    if sample is None:sample={'plane':A,'t':t,'z':z,'blocks':blocks,'weights':witness[192]}
  masks.append(tuple(zs))
 if all(masks):survivors.append(A)
 else:first_fail[next(i+1 for i,m in enumerate(masks) if not m)]+=1
 summary[tuple(masks)]+=1
 masks_counts.update(masks)
print(json.dumps({'planes':len(planes),'survivors':len(survivors),'mask_counts':[[k,v]for k,v in masks_counts.items()],'patterns':[[k,v]for k,v in summary.items()],'first_fail':dict(first_fail),'sample':sample,'cpu_seconds':time.process_time()-start}))
