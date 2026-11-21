from itertools import combinations
from collections import Counter
B=[0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897]
C=[37,6,7,9,10,11,13,14,15,17,18,19,21,22,23,25,58,27,28,29,29,30,30,31,63,0,32]
p=lambda n:n.bit_count()%2
def bw(u):
 x=0
 for i,b in enumerate(B):
  if u>>i&1:x^=b
 return x.bit_count()
def W(t):return ((t&31)<<4)^(1008 if t&32 else 0)
def ch(t,c):return 1-2*p(t&c)
def local(C):return all(27-b<=a<=b and (a+b)%4==0 for t in range(1,64) for b,a in [(bw(W(t)),sum(p(t&c) for c in C))])
def E(C):return tuple(t for t in range(1,32) if sum(p(t&c) for c in C)==16)
def tr(C,t):return [c^t if c&32 else c for c in C]
def swaps():
 for i,j in combinations(range(5),2):
  yield (i,j),[c^((p(c&((1<<i)|(1<<j))))*((1<<i)|(1<<j))) for c in C]
import json
def require(ok):
 if not ok:raise ValueError("audit mismatch")
controls=[
 ((0,2),1,6,-1,14),
 ((0,3),2,10,1,12),
 ((0,4),2,5,1,11),
 ((1,2),4,5,1,12),
 ((1,3),2,5,1,15),
 ((1,4),1,6,-1,14),
]
a=2
H=[t for t in range(64) if bw(a^W(t))==14]
require(len(H)==16)
cases=[]
orbit_keys=set()
for swap,v,z,sgn,j in controls:
 D=dict(swaps())[swap]
 require(local(D) and len(E(D))==7 and E(D)!=E(C))
 rows=[[sum(ch(t,f^c) for t in H) for c in D] for f in range(64)]
 rhs=[-sum(ch(t,f) for t in H) for f in range(64)]
 scalar=[]
 for row,w in zip(rows,rhs):
  sums={0}
  for coefficient in row:sums={u+s*coefficient for u in sums for s in (-1,1)}
  scalar.append(w in sums)
 combine=[x+sgn*y for x,y in zip(rows[v],rows[z])]
 require(all(scalar))
 require(rhs[v]+sgn*rhs[z]==0 and combine[j]==16)
 require(sum(x!=0 for x in combine)==1)
 orbit={tuple(sorted(tr(D,t))) for t in range(32)}
 require(all(E(P)!=E(C) for P in orbit))
 orbit_keys.add(min(orbit))
 zero=D.count(0)+max(Counter(c&31 for c in D if c&32).values())
 require(zero==2)
 cases.append({
  "swap_low_bits_zero_based":swap,"columns":D,"local_windows_passed":63,
  "weight16_label_set":E(D),"zero_column_bound":zero,
  "matches_canonical_E_under_any_translation":False,
  "distinct_translated_patterns_by_q":dict(sorted(Counter(31-len(E(P)) for P in orbit).items())),
  "single_character_projections_feasible":sum(scalar),
  "failed_single_character_projections":[i for i,f in enumerate(scalar) if not f],
  "joint_characters":[v,z],"combine_sign":sgn,
  "active_column_of_combination_zero_based":j,"combined_coefficient":combine[j],
  "combined_target":rhs[v]+sgn*rhs[z]
 })
require(len(orbit_keys)==len(controls))
print(json.dumps({"outside_coset":a,"minimum_weight_section":H,"distinct_translation_orbits":len(orbit_keys),"controls":cases},indent=2))
