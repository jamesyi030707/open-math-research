"""Exact canonical external coset domains; standalone integer implementation."""
import itertools,json,time
from collections import defaultdict,Counter
from pathlib import Path
START=time.process_time()
B=(0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
def codeword(u):
 x=0
 for i,b in enumerate(B):
  if (u>>i)&1:x^=b
 return x
def W(t):return ((t&31)<<4)^(1008 if t&32 else 0)
def chi(t,v):return 1-2*((t&v).bit_count()&1)
def require(c):
 if not c:raise ValueError('invariant')
A=(2,3,5,6,8,9,10,11,12,14)
BW={a:[codeword(a^W(t)).bit_count() for t in range(64)] for a in A}
HS={a:[t for t in range(64) if BW[a][t]==14] for a in A}
# Choose fixed orthogonal basis from each h-half, retaining original signs.
CACHE={}
for a in A:
 require(len(HS[a])==16)
 for half in (0,32):
  basis=[];maps={}
  for v in range(half,half+32):
   c=tuple(chi(t,v) for t in HS[a]); matched=False
   for k,b in enumerate(basis):
    if c==b or c==tuple(-x for x in b):maps[v]=(k,1 if c==b else -1);matched=True;break
   if not matched:maps[v]=(len(basis),1);basis.append(c)
  require(len(basis)==16)
  require(all(sum(x*y for x,y in zip(b,c))==16*(i==j) for i,b in enumerate(basis) for j,c in enumerate(basis)))
  CACHE[a,half]=(basis,maps)
def domain(cols,a,full=False):
 half=0 if sum(v>>5 for v in cols)<14 else 32
 basis,maps=CACHE[a,half]
 small=[j for j,v in enumerate(cols) if (v&32)!=half]
 groups=defaultdict(list)
 for j,v in enumerate(cols):
  if (v&32)==half:
   k,sgn=maps[v];groups[k].append((j,sgn))
 out=[]
 for bits in itertools.product((0,1),repeat=len(small)):
  residual=[-1-sum((1-2*b)*chi(t,cols[j]) for j,b in zip(small,bits)) for t in HS[a]]
  coeff=[sum(x*y for x,y in zip(row,residual)) for row in basis]
  if any(x%16 for x in coeff):continue
  coeff=[x//16 for x in coeff]
  if any(abs(c)>len(groups[k]) or (c-len(groups[k]))%2 for k,c in enumerate(coeff)):continue
  if not full:return True
  options=[]
  for k,c in enumerate(coeff):
   g=groups[k];opts=[]
   for negative in itertools.combinations(range(len(g)),(len(g)-c)//2):
    neg=set(negative);mask=0
    for n,(j,s) in enumerate(g):
     y=s*(-1 if n in neg else 1)
     if y<0:mask|=1<<j
    opts.append(mask)
   options.append(opts)
  init=sum(b<<j for j,b in zip(small,bits))
  for masks in itertools.product(*options):
   mask=init
   for z in masks:mask|=z
   # Exact lift window for residual b: 27-b <= left <= b, with doubly-even congruence.
   lw=[(mask ^ sum((((t&v).bit_count()&1)<<j) for j,v in enumerate(cols))).bit_count() for t in range(64)]
   if all(27-b<=l<=b and (l+b)%4==0 for b,l in zip(BW[a],lw)):out.append(mask)
 return sorted(set(out)) if full else False
solutions=json.load(open(Path(__file__).parent.parent/'2026-11-15'/'h.json'))['solutions']
first=Counter();sur=[]
for i,s in enumerate(solutions):
 for a in A:
  if not domain(s['columns'],a):first[a]+=1;break
 else:sur.append(i)
full={}
for i in sur:
 full[i]={a:domain(solutions[i]['columns'],a,True) for a in A}
print(json.dumps({'scope':'canonical S only; not all q24 orientations','first_rejections':dict(first),'survivors':sur,'full_coset_domains':full,'cpu_seconds':time.process_time()-START},indent=2))
