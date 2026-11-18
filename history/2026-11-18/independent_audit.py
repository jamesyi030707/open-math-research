"""Independent count and local zero-column obstruction audit; no GL transport of B."""
import itertools,json,time,gzip
from collections import Counter
from pathlib import Path
root=Path(__file__).resolve().parent;start=time.process_time()
def require(x):
 if not x:raise ValueError('independent audit failed')
def span(vectors):
 s={0}
 for x in vectors:s|={u^x for u in s}
 return frozenset(s)
def wt(cols,s):return sum((s&v).bit_count()%2 for v in cols)
solutions=json.loads((root.parent/'2026-11-15/h.json').read_text())['solutions']
violators=[]; qchecks=0
for i,sol in enumerate(solutions):
 c=sol['columns'];a0=c.count(0);b=Counter(v&31 for v in c if v&32)
 violates=a0+max(b.values(),default=0)>2
 if violates:violators.append({'index':i,'r':sol['r'],'z':sol['z'],'a0':a0,'max_b':max(b.values())})
 for t in range(32):
  out=[v^(t if v&32 else 0) for v in c]
  weights=[wt(out,s) for s in range(1,32)]
  require(set(weights)<={12,16})
  require(weights.count(12)==16+4*(a0+b[t]))
  qchecks+=1
require(len(violators)==1 and violators[0]['r']==4 and violators[0]['z']==0)
# Enumerate the actual E label sets independently via complementary circuit spans.
lines={span(pair) for pair in itertools.combinations(range(1,32),2)}
spaces={span(triple) for triple in itertools.combinations(range(1,32),3) if len(span(triple))==8}
require(len(lines)==155 and len(spaces)==155)
circuits={U:[C for C in itertools.combinations(sorted(U-{0}),4) if C[0]^C[1]^C[2]^C[3]==0] for U in spaces}
require(all(len(v)==7 for v in circuits.values()))
Es=set();complement_counts=[]
for L in lines:
 comp=[U for U in spaces if len(U&L)==1];complement_counts.append(len(comp))
 for U in comp:
  for C in circuits[U]:Es.add(tuple(sorted((L-{0})|set(C))))
require(set(complement_counts)=={64} and len(Es)==69440)
# Directly check the unique r4,z0 pattern for every E, without assuming a B symmetry.
patterns=set()
for E in Es:
 m={v:(3-sum(1-2*((s&v).bit_count()%2) for s in E))//4 for v in range(1,32)}
 require(Counter(m.values())==Counter({0:9,1:19,2:3}))
 doubles=[v for v,n in m.items() if n==2];single=doubles[0]^doubles[1]^doubles[2]
 require(m[single]==1)
 selected=set(doubles+[single]);require(len(selected)==4)
 c=[0,0]
 for v,n in m.items():c.extend([v]*(n-(v in selected)));c.extend([v+32] if v in selected else [])
 require(len(c)==27 and sum(v>>5 for v in c)==4 and c.count(32)==0)
 require(all(wt(c,s)==(16 if s in E else 12) for s in range(1,32)))
 require(all(wt(c,s+32) in (12,16) for s in range(1,32)))
 require(c.count(0)==2 and max(Counter(v&31 for v in c if v&32).values())==1)
 patterns.add(tuple(sorted(c)))
require(len(patterns)==69440)
old=json.load(gzip.open(root.parent/'2026-11-17/transport.json.gz','rt'))['transported']
overlap=sum(tuple(item['columns']) in patterns for item in old)
print(json.dumps({'canonical_patterns':len(solutions),'translation_moment_checks':qchecks,'violators':violators,'line_count':len(lines),'three_space_count':len(spaces),'complements_per_line':64,'circuits_per_complement':7,'E_count':len(Es),'checked_distinct_r4_z0_patterns':len(patterns),'overlap_with_Nov17_explicit_set':overlap,'new_vs_Nov17_explicit_set':len(patterns)-overlap,'cpu_seconds':time.process_time()-start},indent=2))
