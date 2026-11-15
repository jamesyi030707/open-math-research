from itertools import combinations, product
from collections import Counter
import json,time
start=time.process_time()
E=(1,2,3,4,8,16,28)
chi=lambda s,v:1-2*((s&v).bit_count()%2)
m={v:(3-sum(chi(s,v) for s in E))//4 for v in range(1,32)}
single=[v for v in m if m[v]==1]; double=[v for v in m if m[v]==2]
base={s:sum(m[v] for v in m if (s&v).bit_count()%2) for s in range(1,32)}
require=lambda c,msg: None if c else (_ for _ in ()).throw(ValueError(msg))
# Enumerate smaller selected/unselected nonzero multiset, rather than bitsets of columns.
solutions=[]; attempts=0
for r in (4,8,20,24):
 for z in range(3):
  num=r*(28-r)+32*z*(z-3)
  if num%32 or not 0<=num//32<=3: continue
  P=num//32
  flip=r>13
  need=25-(r-z) if flip else r-z
  for js in product(range(3),repeat=3):
   if sum(j==1 for j in js)!=P:continue
   n=need-sum(js)
   if not 0<=n<=len(single):continue
   for sel in combinations(single,n):
    attempts+=1
    sparse=list(sel)+[v for v,j in zip(double,js) for _ in range(j)]
    xor=0
    for v in sparse:xor^=v
    if xor:continue
    I={s:sum(1 for v in sparse if (s&v).bit_count()%2) for s in range(1,32)}
    if flip:I={s:base[s]-I[s] for s in I}
    ws=[r+base[s]-2*I[s] for s in range(1,32)]
    if not all(w in (12,16) for w in ws):continue
    selected={v:sparse.count(v) for v in m}
    if flip:selected={v:m[v]-selected[v] for v in m}
    require(ws.count(12)==24+r//4-8*z,'qprime')
    cols=[v+32*e for v in m for e in (0,1) for _ in range(selected[v] if e else m[v]-selected[v])]+[0]*(2-z)+[32]*z
    w64=[sum((u&v).bit_count()%2 for v in cols) for u in range(64)]
    require(all(w%4==0 for w in w64),'double even')
    require(w64[32]==r and all(w64[u] in (12,16) for u in range(1,64) if u!=32),'windows')
    solutions.append({'r':r,'z':z,'selected':[(v,selected[v]) for v in selected if selected[v]],'columns':cols})
counts=Counter((x['r'],x['z']) for x in solutions)
require(len(solutions)==277,'total')
print(json.dumps({'scope':'canonical S-label q24 restriction only; no external coset or all-label exclusion','attempted_multisets':attempts,'total':len(solutions),'counts':{str(k):v for k,v in sorted(counts.items())},'solutions':solutions,'cpu_seconds':time.process_time()-start},indent=2))
