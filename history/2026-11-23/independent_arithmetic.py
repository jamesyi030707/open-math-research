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
require(len(sol)==277)
canon={norm(x['columns']) for x in sol}
prev17={tr(C,t) for C in canon for t in range(32)}
require(len(prev17)==8408)
prev22={tr(norm(perm(c,P) for c in sol[1]['columns']),t) for P in permutations(range(5)) for t in range(32)}
require(len(prev22)==480)
sections={a:[t for t in range(64) if bw(a^W(t))==14] for a in A}
combos={}
for a,H in sections.items():
 F=[sum(1-2*p(v&t) for t in H) for v in range(64)]
 combos[a]=[(u,v,s,tuple(F[c^u]+s*F[c^v] for c in range(64))) for u,v in combinations(range(64),2) for s in (-1,1)]
indices=[i for i in range(1,277) if (sol[i]['r'],sol[i]['z'])!=(sol[i-1]['r'],sol[i-1]['z'])]
require(indices==[1,19,115,139,163,259])
records=[]
for i in indices:
 for swapped in (False,True):
  C=tuple(swap(c) if swapped else c for c in sol[i]['columns'])
  require(sum(c>>5 for c in C)==sol[i]['r'] and C.count(32)==sol[i]['z'])
  require(sum(sum(p(t&c) for c in C)==12 for t in range(1,32))==24)
  require(all(27-b<=a<=b and (a+b)%4==0 for t in range(1,64) for a,b in [(sum(p(t&c) for c in C),bw(W(t)))]))
  z=C.count(0)+max(Counter(c&31 for c in C if c&32).values())
  per={}; examples={}; masks=set()
  for a, rows in combos.items():
   card=Counter()
   singleton_masks=set()
   for u,v,s,D in rows:
    ds=[D[c] for c in C]; T=-D[0]; S=sum(ds); g=reduce(gcd,ds)
    hits=T==0 and sum(bool(x) for x in ds)==1
    badg=g>0 and (T-S)%(2*g)!=0
    bad0=g==0 and T!=0
    if hits:
     require(badg);card['singleton']+=1
     support=frozenset(c for c,e in enumerate(D) if e)
     singleton_masks.add(support);masks.add((a,support))
    elif badg:card['gcd_only_combination']+=1
    if badg:card['gcd_failure']+=1
    if bad0:card['zero_row_nonzero_target']+=1
    for cond,k in ((hits,'singleton'),(badg and not hits,'gcd_only_combination'),(bad0,'zero_row_nonzero_target')):
     if cond and k not in examples:
      examples[k]={'a':a,'u':u,'v':v,'sign':s,'T':T,'sum':S,'g':g,'local_coeff':ds}
   card['singleton_supports']=len(singleton_masks)
   per[a]=dict(card)
  tot=sum((Counter(c) for c in per.values()),Counter())
  require(tot['singleton_supports']==len(masks))
  records.append({'index':i,'swapped':swapped,'r':sol[i]['r'],'z':sol[i]['z'],'cols':C,
    'zero_column_bound':z,'in_old_8408':norm(C) in prev17,'in_nov22_480':norm(C) in prev22,
    'totals':dict(tot),'by_section':per,'first':examples})
require(len({norm(x['cols']) for x in records})==len(records))
print(json.dumps({'h_sections':sections,'coverage_first_indices':indices,'control_count':len(records),
 'per_control_row_combinations':len(A)*2016*2,'records':records},indent=2))
