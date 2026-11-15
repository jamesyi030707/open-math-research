import itertools,json,time,collections
start=time.process_time()
H={1,2,3,4,8,16,28}
labels=[0,0]
for v in range(1,32):
 k=sum((s&v).bit_count()%2 for s in H)
 if k%2 or k<2:raise ValueError(k)
 labels.extend([v]*((k-2)//2))
words=[sum(((s&v).bit_count()%2)<<j for j,v in enumerate(labels)) for s in range(1,32)]
if len(labels)!=27:raise ValueError('len')
full=(1<<27)-1
results={}
for r in [4,8,20,24]:
 patterns=set(); counts=collections.Counter(); samples={}
 size=min(r,27-r)
 for c in itertools.combinations(range(27),size):
  v=0;mask=0
  for j in c:v^=labels[j];mask|=1<<j
  if v:continue
  if r>13:mask^=full
  weights=[(w^mask).bit_count() for w in words]
  if any(w not in (12,16) for w in weights):continue
  selected=tuple(sum((mask>>j)&1 for j,u in enumerate(labels) if u==v) for v in range(32))
  if selected in patterns:continue
  patterns.add(selected)
  key=(selected[0],weights.count(12));counts[key]+=1;samples.setdefault(str(key),selected)
 results[r]={'count':len(patterns),'counts':{str(k):v for k,v in sorted(counts.items())},'samples':samples,'patterns':sorted(patterns)}
print(json.dumps({'labels':labels,'results':results,'cpu_seconds':time.process_time()-start}))
