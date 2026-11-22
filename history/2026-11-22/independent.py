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
from itertools import permutations
from pathlib import Path
from hashlib import sha256
from sys import argv

def req(ok):
 if not ok:raise ValueError("verification failed")

def section(a):
 H=[t for t in range(64) if bw(a^W(t))==14]
 req(len(H)==16)
 F=[sum(ch(t,v) for t in H) for v in range(64)]
 polar=[k for k in range(1,32) if abs(F[k])==16]
 req(len(polar)==1)
 k=polar[0]
 rep=lambda u:min(u,u^k)
 gauge=H[0]
 G=[ch(gauge,u)*F[u] for u in range(64)]
 req(all(G[u]==G[u^k] for u in range(64)))
 Q=sorted({rep(u) for u in range(32)})
 req(len(Q)==16 and [G[u] for u in Q]==[16]+[0]*15)
 req(all(abs(G[32|v])==4 for v in Q))
 f={u:G[32|u]//4 for u in Q}
 req(all(sum(f[u]*f[rep(u^d)] for u in Q)==16*(d==0) for d in Q))
 witness={}; counts=Counter()
 for u,v in combinations(range(64),2):
  for s in (-1,1):
   d=tuple(F[c^u]+s*F[c^v] for c in range(64))
   if d[0] or not any(d):continue
   support=frozenset(c for c,x in enumerate(d) if x)
   req((u^v)&32==0)
   sign=s*ch(gauge,u^v)
   lowhalf=u&32
   direct={lowhalf|x for x in (u&31,(u&31)^k,v&31,(v&31)^k)}
   other={c for c in range(64) if (c&32)!=lowhalf and f[rep((c^u)&31)]==sign*f[rep((c^v)&31)]}
   req(support==direct|other and len(support)==(34 if rep(u)==rep(v) else 20))
   counts[(u>>5,s)]+=1
   witness.setdefault(support,[]).append((u,v,s))
 req(len(witness)==345 and sum(counts.values())==1335)
 supports=sorted(map(sorted,witness))
 return witness, {
  "H":H,"F":F,"low_half_period_or_antiperiod":k,"F_at_period_or_antiperiod":F[k],
  "pair_count":sum(counts.values()),
  "pair_counts_by_half_and_literal_sign":{str(t):n for t,n in sorted(counts.items())},
  "support_count":len(witness),"support_sizes":dict(sorted(Counter(map(len,witness)).items())),
  "sorted_support_digest":sha256(json.dumps(supports,separators=(',',':')).encode()).hexdigest(),
 }

def permute(c,P):
 return (c&32)|sum(((c>>i)&1)<<j for i,j in enumerate(P))

path=Path(argv[1]) if len(argv)==2 else Path(__file__).resolve().parent.parent/'2026-11-15/h.json'
data=json.loads(path.read_text())['solutions']
canonical={tuple(sorted(x['columns'])) for x in data}
req(len(canonical)==277 and data[1]['columns']==C)
old17={tuple(sorted(tr(c,t))) for c in canonical for t in range(32)}
req(len(old17)==8408)
old21_swaps=((0,2),(0,3),(0,4),(1,2),(1,3),(1,4))
old21={tuple(sorted(tr(dict(swaps())[pair],t))) for pair in old21_swaps for t in range(32)}
req(len(old21)==48 and not old17&old21)
atlas={tuple(sorted(permute(c,P) for c in C)) for P in permutations(range(5))}
sections={a:section(a) for a in (2,6)}
records=[]; orbit_keys=set(); hit_strata=Counter(); atlas_cover=Counter()
for pattern in sorted(atlas):
 orbit={tuple(sorted(tr(pattern,t))) for t in range(32)}
 q24=[c for c in orbit if len(E(c))==7]
 req(tuple(q24)==(pattern,) and len(orbit)==8 and all(local(c) for c in orbit))
 orbit_keys.add(pattern)
 req(pattern.count(0)+max(Counter(c&31 for c in pattern if c&32).values())==2)
 covered17=bool(orbit&old17);covered21=bool(orbit&old21)
 req(covered17==(pattern in old17) and covered21==(pattern in old21))
 atlas_cover[covered17,covered21]+=1
 certs={}
 for a,(witness,summ) in sections.items():
  occ=Counter(pattern)
  valid=[S for S in witness if sum(occ[c] for c in S)==1]
  certs[a]={"support_count":len(valid),"example":witness[valid[0]][0] if valid else None}
 hit_strata[tuple(bool(certs[a]['support_count']) for a in (2,6))]+=1
 records.append({"columns":pattern,"covered_nov17":covered17,"covered_nov21":covered21,"sections":certs})
req(len(atlas)==len(orbit_keys)==60)
req(hit_strata=={(True,True):48,(True,False):6,(False,True):6})
req(atlas_cover=={(False,False):48,(True,False):6,(False,True):6})
print(json.dumps({
 "sections":{a:summ for a,(_,summ) in sections.items()},
 "atlas_markings":len(atlas),"atlas_true_q24_orbits":len(orbit_keys),
 "hit_strata_a2_a6":{str(k):v for k,v in sorted(hit_strata.items())},
 "prior_coverage_strata_nov17_nov21":{str(k):v for k,v in sorted(atlas_cover.items())},
 "new_rejections_relative_to_named_batches":atlas_cover[False,False],
 "records":records
},separators=(',',':')))
