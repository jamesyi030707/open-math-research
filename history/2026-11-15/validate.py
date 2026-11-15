import json
from pathlib import Path
p=Path(__file__).resolve().parent
read=lambda n:json.loads((p/n).read_text())
def need(x,m):
 if not x:raise ValueError(m)
a=read('h.json'); b=read('local.json')
A=set()
for x in a['solutions']:
 v=[0]*32;v[0]=x['z']
 for lab,n in x['selected']:v[lab]=n
 A.add((x['r'],tuple(v)))
B={(int(r),tuple(v)) for r,d in b['results'].items() for v in d['patterns']}
need(A==B and len(A)==277,'complete vector agreement')
for f,g in [('h.json','h_optimized.json'),('local.json','local_optimized.json')]:
 x,y=read(f),read(g);x.pop('cpu_seconds');y.pop('cpu_seconds');need(x==y,'optimization agreement')
need(read('orbits.json')==read('orbits_optimized.json'),'orbit modes')
# Deliberately break a real local code; it must leave the allowed windows.
x=a['solutions'][0];cols=x['columns'][:]
w=lambda u,cs:sum((u&c).bit_count()%2 for c in cs)
need(all(w(u,cols) in (12,16) for u in range(1,64) if u!=32),'positive control')
cols[0]^=32
need(any(w(u,cols) not in (12,16) for u in range(1,64) if u!=32),'damaged control')
print('PASS: all 277 vectors agree; normal/-O agree; positive and damaged controls checked.')
