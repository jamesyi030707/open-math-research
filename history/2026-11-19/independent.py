"""Independent direct-image audit of the q24 slice."""
import json,sys
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'2026-11-15/h.json'
data=json.loads(path.read_text())['solutions']
def require(c):
 if not c:raise ValueError('independent orbit audit failed')
def act(c,t):return tuple(sorted(v^t if v&32 else v for v in c))
def in_X(c):
 a0=c.count(0);b=Counter(v&31 for v in c if v&32)
 return a0+b[0]==2 and a0+max(b.values(),default=0)<=2
stats=defaultdict(Counter);weighted=Fraction();keys=set();checks=0;accepted=0
for sol in data:
 c=tuple(sorted(sol['columns']))
 if not in_X(c):continue
 accepted+=1;a0=c.count(0);b=tuple(c.count(v+32) for v in range(32))
 T=sum(a0+x==2 for x in b)
 H=sum(all(b[x]==b[x^t] for x in range(32)) for t in range(32))
 orbit={act(c,t) for t in range(32)}
 intersection={d for d in orbit if in_X(d)};N=len(intersection)
 require(len(orbit)==32//H and T==N*H)
 for d in orbit:
  weights=[sum((s&v).bit_count()%2 for v in d) for s in range(1,32)]
  require(set(weights)<={12,16})
  require((weights.count(12)==24)==in_X(d))
 for d in intersection:
  require(sum(v>>5 for v in d)==sol['r'] and d.count(32)==sol['z'])
 key=min(intersection);keys.add(key)
 for d in orbit:
  shifted={act(d,t) for t in range(32)}
  require(shifted==orbit and min(e for e in shifted if in_X(e))==key)
  checks+=1
 require(min(d for d in {act(key,t) for t in range(32)} if in_X(d))==key)
 stats[sol['r'],sol['z']][T,H,N]+=1;weighted+=Fraction(1,N)
require(accepted==276 and weighted==Fraction(786,5))
require(69440*weighted==10915968 and len(keys)==276 and checks==8400)
print(json.dumps({'strata':{str(k):{str(a):b for a,b in v.items()} for k,v in sorted(stats.items())},'canonical_weighted_sum':str(weighted),'all_X_size':69440*accepted,'orbits_meeting_X':int(69440*weighted),'canonical_distinct_keys':len(keys),'checked_transported_outputs':checks},indent=2))
