import itertools,json,collections
from pathlib import Path
root=Path(__file__).resolve().parent
x=json.loads((root/'local.json').read_text())
quad=(4,8,16,28)
perms=[]
for a,b in itertools.permutations((1,2,3),2):
 for c,d,e,f in itertools.permutations(quad):
  if c^d^e!=f:raise ValueError('q')
  images=(a,b,c,d,e)
  p=tuple(sum(((v&g).bit_count()%2)<<i for i,g in enumerate(images)) for v in range(32))
  if len(set(p))!=32:raise ValueError('rank')
  perms.append(p)
if len(set(perms))!=144:raise ValueError('group')
report={}
for r,data in x['results'].items():
 pats=set(map(tuple,data['patterns']));orbits=[]
 while pats:
  p=min(pats);orb=set()
  for perm in perms:
   out=[0]*32
   for v,m in enumerate(p):out[perm[v]]=m
   orb.add(tuple(out))
  if not orb<=pats:raise ValueError('overlap or missing')
  pats-=orb
  orbits.append({'size':len(orb),'z':p[0],'representative':p})
 report[r]=orbits
print(json.dumps({'group_order':144,'orbits':report}))
