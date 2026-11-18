"""Uniform translated-zero-column obstruction, exact finite checks."""
import json,gzip
from collections import Counter
from pathlib import Path
P=Path(__file__).resolve().parent.parent

def require(x,message):
 if not x: raise ValueError(message)
def dot(a,b):return (a&b).bit_count()%2
solutions=json.loads((P/'2026-11-15/h.json').read_text())['solutions']
bad=[]; hist=Counter(); checked=0
for i,s in enumerate(solutions):
 cols=s['columns'];a=Counter(c for c in cols if c<32);b=Counter(c&31 for c in cols if c&32)
 require(len(cols)==27,'length')
 for t in range(32):
  tr=[c^(t if c&32 else 0) for c in cols]
  weights=[sum(dot(u,c) for c in tr) for u in range(1,32)]
  require(set(weights)<={12,16},'windows')
  require(all(sum(dot(u+32,c) for c in tr) in (12,16) for u in range(1,32)),'shifted windows')
  require(sum(dot(32,c) for c in tr)==s['r'],'special h weight')
  require(weights.count(12)==16+4*(a[0]+b[t]),'moment')
  checked+=1
 score=a[0]+max(b.values());hist[score]+=1
 if score>2:
  ts=[t for t in range(32) if a[0]+b[t]==3]
  bad.append({'source_index':i,'r':s['r'],'z':s['z'],'columns':cols,'translations_to_q28':ts})
require(len(bad)==1 and (bad[0]['r'],bad[0]['z'])==(4,0),'unique marking')
# Number of pairs: 2-space U, complementary 3-space V, 4-circuit in V.
# [5 choose 2]_2=155; 2^(2*3)=64 complements; |GL(3,2)|/24=7 circuits.
E_count=155*64*7
old=json.loads(gzip.decompress((P/'2026-11-17/transport.json.gz').read_bytes()))['transported']
overlap=0
for s in old:
 cols=s['columns'];weights=[sum(dot(u,c) for c in cols) for u in range(1,32)]
 a=Counter(c for c in cols if c<32);b=Counter(c&31 for c in cols if c&32)
 if weights.count(12)==24 and a[0]+max(b.values())>2:overlap+=1
require(overlap==7,'overlap')
print(json.dumps({'scope':'fixed B, normalized doubly-even kernel-zero lifts only','local_markings':len(solutions),'translations_checked':checked,'score_counts':dict(hist),'excluded_canonical':bad,'q24_E_count':E_count,'uniform_q24_exclusions':E_count,'survivors_per_E_of_this_filter_only':276,'q24_remaining_after_this_filter_only':E_count*276,'overlap_with_nov17_explicit_q24_set':overlap,'not_in_nov17_explicit_set':E_count-overlap},indent=2))
