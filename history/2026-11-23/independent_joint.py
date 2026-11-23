from math import gcd
from itertools import combinations,permutations
from collections import Counter
from functools import reduce
from pathlib import Path
import sys,json
B=(0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
A=(2,3,5,6,8,9,10,11,12,14)
def bw(u):
 x=0
 for i,b in enumerate(B):
  if (u>>i)&1:x^=b
 return x.bit_count()
def W(t):return ((t&31)<<4)^(1008 if t&32 else 0)
def p(x):return x.bit_count()&1
def norm(x):return tuple(sorted(x))
def tr(x,t):return norm(c^t if c&32 else c for c in x)
def swap(c):return c^(5*p(c&5))
def perm(c,P):return (c&32)|sum(((c>>i)&1)<<j for i,j in enumerate(P))
def require(ok):
 if not ok:raise ValueError('audit invariant')
source=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'2026-11-15/h.json'
sol=json.loads(source.read_text())['solutions']
def pair_pass(rows,targets):
 for u,v in combinations(range(64),2):
  # Encode signed sums into one integer with spacing larger than
  # the possible variation in the first coordinate.
  radix=2+2*sum(abs(x) for x in rows[u])+2*abs(targets[u])
  coefficient=[x+radix*y for x,y in zip(rows[u],rows[v])]
  want=targets[u]+radix*targets[v]
  reachable=1
  shifted=(sum(map(abs,coefficient))+want)
  if shifted%2 or shifted<0:return False
  for c in coefficient:
   reachable|=reachable<<abs(c)
  if not ((reachable>>(shifted//2))&1):return False
 return True


def full_weights(C,H):
 # Compute an exhaustive 13/14 meet-in-the-middle join in actual
 # A-side weight coordinates, without Fourier inversion or packing.
 base=tuple(sum(p(t&c) for c in C) for t in H)
 delta=[tuple(1-2*p(t&c) for t in H) for c in C]
 def halves(ds):
  sums=[(0,)*len(H)]
  for col in ds:
   sums += [tuple(x+y for x,y in zip(x0,col)) for x0 in sums]
  return sums
 left={}
 for k,v in enumerate(halves(delta[:13])):
  n,_=left.get(v,(0,0))
  left[v]=(n+1,k)
 right=halves(delta[13:])
 total=0; witness=None
 for k,vec in enumerate(right):
  need=tuple(14-x-y for x,y in zip(base,vec))
  if need in left:
   n,j=left[need]
   total+=n
   if witness is None:
    witness=j|(k<<13)
    require(all(sum(p(t&c)^((witness>>i)&1) for i,c in enumerate(C))==14 for t in H))
 require((witness is None)==(total==0))
 return total,witness

out={}
for a in (2,3):
 H=[t for t in range(64) if bw(a^W(t))==14]
 require(len(H)==16)
 F=[sum(1-2*p(v&t) for t in H) for v in range(64)]
 require(all(x%4==0 for x in F))
 F=[x//4 for x in F]
 records=[]
 for i in (19,115,139,163):
  for swapped in (False,True):
   C=tuple(swap(c) if swapped else c for c in sol[i]['columns'])
   rows=[[F[v^c] for c in C] for v in range(64)]
   require(pair_pass(rows,[-x for x in F]))
   count,mask=full_weights(C,H)
   require((count>0)==(a==2))
   records.append({'index':i,'swapped':swapped,'pairs_feasible':2016,
                   'full_H_weight14_count':count,'example_mask':mask})
 out[a]={'H':H,'records':records}
print(json.dumps(out,indent=2))
