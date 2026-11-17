"""Exact bounded transvection subgroup; does not classify all automorphisms."""
import json,itertools,time
from collections import Counter,deque
START=time.process_time()
B=(0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
def dot(x,y):return (x&y).bit_count()%2
def word(u):
 r=0
 for i,b in enumerate(B):
  if u>>i&1:r^=b
 return r
cols=[sum(((b>>j)&1)<<i for i,b in enumerate(B)) for j in range(37)]
M=Counter(cols); weights=[word(u).bit_count() for u in range(1024)]
G=[]; trials=0
for s in range(1,32):
 v=s<<4
 for l in range(1,1024):
  if dot(l,v) or dot(l,1008):continue
  trials+=1
  transformed=[c^(l if dot(v,c) else 0) for c in cols]
  if Counter(transformed)!=M:continue
  if any(weights[u]!=weights[u^(v if dot(l,u) else 0)] for u in range(1024)):raise ValueError('dual test mismatch')
  perm=[cols.index(c) for c in transformed]
  if len(set(perm))!=37:raise ValueError('nonprojective B requires multiset matching')
  images=[s0^(s if dot(l,s0<<4) else 0) for s0 in range(32)]
  G.append({'v':v,'l':l,'S_action':images,'coordinate_permutation':perm})
actions=sorted(set(tuple(g['S_action']) for g in G)); E=(1,2,3,4,8,16,28)
orbit={E};todo=deque([E])
while todo:
 e=todo.popleft()
 for g in actions:
  f=tuple(sorted(g[x] for x in e))
  if f not in orbit:orbit.add(f);todo.append(f)
print(json.dumps({'candidate_pairs':trials,'valid_transvections':len(G),'distinct_S_actions':len(actions),'orbit_size':len(orbit),'orientations':sorted(orbit),'generators':G,'cpu_seconds':time.process_time()-START},indent=2))
