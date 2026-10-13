"""Independent unpruned reverse-tree pilot. No imported generator; J=20.
Enumerate exact-depth predecessors of all odd anchors 3..31, depth 0..19.
Filter original starts only to 3..890 and directly test 20 steps.
Not a new theorem, not a global Collatz result.
"""
import json,time,hashlib
from pathlib import Path
p=Path(__file__).parent;t=time.perf_counter()
J,H,X=20,31,890
level=set(range(3,H+1,2));candidates=set();counts=[]
for d in range(J):
 counts.append(len(level));candidates.update(x for x in level if 3<=x<=X)
 if d<J-1:
  nxt={2*x for x in level}
  nxt.update((2*x-1)//3 for x in level if x%3==2)
  level=nxt
hits=[]
for n in sorted(candidates):
 x=n;q=0
 for j in range(1,J+1):
  if x%2:q+=1;x=(3*x+1)//2
  else:x//=2
  if 3**q<2**j and x>=n:hits.append([n,j,q])
base=json.load(open(p/'baseline_paradox_cert_J92.json'))
expected=[h for h in base['hits'] if h[1]<=J]
assert hits==expected,(hits,expected)
r={'J':J,'H':H,'X':X,'levels':counts,'total_layer_nodes':sum(counts),'candidates':len(candidates),'candidate_steps':len(candidates)*J,'hits':hits,'baseline_matches':True,'runtime_s':time.perf_counter()-t,'pruning':'none; start filter only'}
(p/'independent_pilot_result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
