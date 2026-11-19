"""Count actual translation orbits meeting the q24 slice; no new exclusion."""
import json,sys
from pathlib import Path
from collections import Counter
from fractions import Fraction
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'2026-11-15/h.json'
S=json.loads(p.read_text())['solutions']
def require(b):
 if not b:raise ValueError('verification failed')
def weight(cols,s):return sum((s&c).bit_count()%2 for c in cols)
def translate(cols,t):return tuple(sorted(c^(t if c&32 else 0) for c in cols))
table=Counter();total=Fraction();checks=0
for s in S:
 c=s['columns'];a0=c.count(0);b=Counter(x&31 for x in c if x&32)
 if a0+max(b.values())>2:continue
 H=[t for t in range(32) if all(b[v]==b[v^t] for v in range(32))]
 T=[t for t in range(32) if a0+b[t]==2]
 orbit={translate(c,t) for t in range(32)}
 slice24={d for d in orbit if sum(weight(d,u)==12 for u in range(1,32))==24}
 require(len(orbit)==32//len(H) and len(slice24)==len(T)//len(H))
 key=min(slice24)
 for d in orbit:
  same={translate(d,t) for t in range(32)}
  require(same==orbit)
  require(min(same & slice24)==key)
  checks+=1
 N=len(slice24);table[(s['r'],s['z'],len(T),len(H),N)]+=1
 total+=Fraction(1,N)
require(total*69440==10915968)
print(json.dumps({'scope':'local q24 slice after multiplicity filter, before older exclusions','table':[{'r':r,'z':z,'q24_parameters':t,'stabilizer':h,'q24_orbit_intersection':n,'canonical_E_count':count} for (r,z,t,h,n),count in sorted(table.items())],'per_E_weighted_sum':str(total),'E_count':69440,'q24_patterns':276*69440,'orbits_meeting_q24':int(total*69440),'canonical_key_checks':checks,'new_exclusions':0},indent=2))
