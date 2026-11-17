"""Independent truth-table/linear-closure audit of the S,h stabilizer.

No import from the main implementation. Derives each induced map from
radical-line correspondences using XOR closure, then directly tests all
1024 message weights, with a recovered coordinate permutation.
"""
import itertools,json,time
from collections import Counter
start=time.process_time()
rows=[0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897]
def parity(x):return bin(x).count('1')%2
def demand(x):
 if not x:raise RuntimeError('audit invariant')
def extend(pairs,n):
 table={0:0}
 for x,y in pairs:
  if x in table:
   if table[x]!=y:return None
  else:
   extra={a^x:b^y for a,b in table.items()}
   if any(a in table and table[a]!=b for a,b in extra.items()):return None
   table.update(extra)
 if len(table)!=2**n or len(set(table.values()))!=2**n:return None
 return table
points=[sum(((row>>j)&1)*2**i for i,row in enumerate(rows)) for j in range(37)]
pointcoords=[(p&15,(p>>4)&31,parity(p&1008)) for p in points]
demand(len(set(points))==37)
zero=[z for z,x,e in pointcoords if e==0]; demand(all(x==0 for z,x,e in pointcoords if e==0))
graph={x:z for z,x,e in pointcoords if e==1}; demand(len(graph)==32 and graph[0]==0)
# Compute every polarization directly from truth table.
polar={a:[[parity(a&(graph[x]^graph[y]^graph[x^y]^graph[0])) for y in range(32)] for x in range(32)] for a in range(1,16)}
rad={}
for a,m in polar.items():
 rs=[x for x in range(32) if not any(m[x])];demand(len(rs)==2);rad[a]=rs[1]
# quadraticity is checked independently by additivity of each polar row
for m in polar.values():
 demand(all(m[x][y^z]==(m[x][y]^m[x][z]) for x in range(32) for y in range(32) for z in range(32)))
counts=Counter(); accepted=[]
for images in itertools.permutations(zero):
 D=extend(list(zip(zero,images)),4)
 if D is None:continue
 counts['D_permutations']+=1
 Dt={a:sum(parity(a&D[2**i])*2**i for i in range(4)) for a in range(16)}
 L=extend([(rad[Dt[a]],rad[a]) for a in range(1,16)],5)
 if L is None:continue
 counts['radical_consistent']+=1
 if not all(polar[a][L[x]][L[y]]==polar[Dt[a]][x][y] for a in range(1,16) for x in range(32) for y in range(32)):continue
 counts['polar_consistent']+=1
 K={x:graph[L[x]]^D[graph[x]] for x in range(32)}
 demand(all(K[x^y]==K[x]^K[y] for x in range(32) for y in range(32)))
 # General form z'=D z + K x + c e. c=0 is forced by f(0)=0.
 def F(p):
  z=p&15;x=p>>4&31;e=parity(p&1008)
  y=L[x]
  return D[z]^K[x]^(y<<4)^((e^parity(y))<<9)
 transformed=list(map(F,points));demand(set(transformed)==set(points))
 images10=[F(2**i) for i in range(10)]
 perm=[points.index(p) for p in transformed]
 for u in range(1024):
  transformed_u=sum(parity(u&p)*2**i for i,p in enumerate(images10))
  w0=0;w1=0
  for i,row in enumerate(rows):
   if u>>i&1:w0^=row
   if transformed_u>>i&1:w1^=row
  demand(w0.bit_count()==w1.bit_count())
 counts['all_1024_weights_checked']+=1
 accepted.append({'column_map_basis':images10,'coordinate_permutation':perm,'S_action':[sum(parity(s&L[2**i])*2**i for i in range(5)) for s in range(32)]})
print(json.dumps({'counts':dict(counts),'group_order':len(accepted),'elements':accepted,'cpu_seconds':time.process_time()-start},indent=2))
