"""Exact RM containment and finite coupled model data. No feasibility solve."""
import json
from pathlib import Path
p=Path(__file__).parent
r=json.loads((p/'results.json').read_text());g=int(r['generator_hex'],16)
G=[(g<<i)|(((g<<i).bit_count()%2)<<63) for i in range(10)]
E={0}
for row in G:E|={v^row for v in list(E)}
coords=[];a=1
for j in range(63):
 coords.append(a);a<<=1
 if a&64:a^=67
coords.append(0)
assert len(set(coords))==64
R=[(1<<64)-1]+[sum(((x>>b)&1)<<j for j,x in enumerate(coords)) for b in range(6)]
H={0}
for row in R:H|={v^row for v in list(H)}
assert len(H)==128 and H<=E
span=set(H);Q=[]
for row in G:
 if row not in span:
  Q.append(row);span|={v^row for v in list(span)}
assert len(Q)==3 and span==E
reps=[0]
for q in Q:reps += [v^q for v in reps]
# Exact linear forms in shared binary variables f_j:
# W_{q,a}=sum_j (-1)^(q_j+a.dot(coords[j])) * (1-2*f_j).
# 512 inequalities |W|<=10 plus sum f_j odd are equivalent
# to minwt(f+E)>=27, because E=disjoint union of8 affine blocks.
rows=[]
for q in reps:
 for a in range(64):
  signs=[1-2*(((q>>j)&1)^((a&x).bit_count()%2)) for j,x in enumerate(coords)]
  rows.append(signs)
assert len(rows)==512 and all(len(s)==64 for s in rows)
# Limited implementation consistency checks, NOT solving the binary model.
for f in [1,7,0x13579bdf2468ace1]:
 direct=min((f^c).bit_count() for c in E)
 walsh=(64-max(abs(sum(s[j]*(1-2*((f>>j)&1)) for j in range(64))) for s in rows))//2
 assert direct==walsh
result={'coordinate_labels':coords,'rm_generators_hex':[hex(v) for v in R],'complement_generators_hex':[hex(v) for v in Q],'coset_representatives_hex':[hex(v) for v in reps],'rm_dimension':7,'parent_dimension':10,'shared_binary_variables':64,'signed_linear_forms':512,'solve_performed':False}
(p/'rm_model.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
# Separately check the explicit complement proposed in the second discussion.
Q2=[0x172e5cb972e5cb97,0x65cb972e5cb972e5,0x3972e5cb972e5cb9]
S=set(H)
for q in Q2:
 assert q in E
 S|={v^q for v in list(S)}
assert S==E
T={0}
for q in Q2:T|={v^q for v in list(T)}
for q in T-{0}:
 assert {(q^h).bit_count() for h in H}=={28,36}
 # Mobius transform in polynomial-basis coordinates checks algebraic degree.
 anf=[0]*64
 for j,x in enumerate(coords):anf[x]=(q>>j)&1
 for b in range(6):
  for x in range(64):
   if x&(1<<b):anf[x]^=anf[x^(1<<b)]
 assert max(x.bit_count() for x,v in enumerate(anf) if v)==2
result['claude_explicit_complement_verified']=True
result['claude_complement_generators_hex']=[hex(q) for q in Q2]
result['seven_nonzero_combinations_bent_and_degree_two']=True
(p/'rm_model.json').write_text(json.dumps(result,indent=2))
print('Explicit second-discussion complement independently verified: membership, full span, seven bent quadratics.')
