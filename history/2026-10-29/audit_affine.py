import csv,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
P=Path(__file__).resolve().parent
# Polynomial coefficients by repeated multiplication, no binomial/Krawtchouk formula.
def poly(n,w):
 c=[1]
 for t in range(n):
  sign=-1 if t<w else 1
  q=[0]*(len(c)+1)
  for j,x in enumerate(c):q[j]+=x;q[j+1]+=sign*x
  c=q
 return c
# Explicit pair populations independently transcribed from the Oct 28 definitions.
def joint(v):
 p,q,y10,y14,z8,z12,z16=v
 J=Counter({(0,0):1,(0,32):1})
 groups=[((14,22),[(14,160)]),((16,24),[(12,p),(16,80-p)]),((16,16),[(12,q),(16,31-q)]),((18,18),[(10,y10),(14,y14),(18,160-y10-y14)]),((20,20),[(8,z8),(12,z12),(16,z16),(20,80-z8-z12-z16)])]
 for (r,s),choices in groups:
  for a,count in choices:J[a,r]+=count;J[a,s]+=count
 return dict(J)
zero=[0]*7
J0=joint(zero)
Jbasis=[J0]
for k in range(7):
 v=zero.copy();v[k]=1;J=joint(v)
 Jbasis.append({ij:J.get(ij,0)-J0.get(ij,0) for ij in J.keys()|J0.keys()})
T={(i,j):[0]*8 for i in range(28) for j in range(38)}
for k,J in enumerate(Jbasis):
 assert sum(J.values())==(1024 if k==0 else 0)
 for (a,r),count in J.items():
  if not count:continue
  l=poly(27,a);rpoly=poly(37,r)
  for i,x in enumerate(l):
   for j,y in enumerate(rpoly):T[i,j][k]+=count*x*y
with open(P/'affine_coefficients.csv') as f:rows=list(csv.DictReader(f))
assert len(rows)==1064
keys=['constant','p','q','y10','y14','z8','z12','z16']
for row in rows:
 ij=int(row['i']),int(row['j']);assert int(row['denominator'])==1024
 assert T[ij]==[int(row[x]) for x in keys],ij
for k,J in enumerate(Jbasis):
 ordinary=[0]*65
 for (a,r),count in J.items():
  for w,x in enumerate(poly(64,a+r)):ordinary[w]+=count*x
 for w in range(65):assert sum(T[i,j][k] for i,j in T if i+j==w)==ordinary[w]
assert T[0,0]==[1024]+[0]*7
assert [sum(v[k] for v in T.values()) for k in range(8)]==[1024*2**54]+[0]*7
orbits={}
for ij,v in T.items():
 i,j=ij;orb={(i,j),(27-i,j),(i,37-j),(27-i,37-j)}
 assert len(orb)==4
 assert all(T[x]==v for x in orb)
 orbits[min(orb)]=orb
assert len(orbits)==266
assert all(T[0,j][k]==0 for j in range(38) for k in range(1,8))
witness=[1,0,0,140,16,8,6,64]
values={ij:Fraction(sum(a*b for a,b in zip(v,witness)),1024) for ij,v in T.items()}
assert all(x.denominator==1 for x in values.values())
neg=[[i,j,int(v)] for (i,j),v in values.items() if v<0]
assert len(neg)==8 and values[1,2]==-16
assert T[1,2]==[91264,288,-96,-576,-288,-672,-448,-224]
res={'status':'PASS','independent_method':'Repeated multiplication of (1+x) and (1-x), evaluated affine basis from independently restated category populations; no import of publisher implementation.','checked_integer_entries':8512,'split_positions':1064,'diagonal_identities':65,'dual_total':2**54,'four_element_complement_orbits':266,'prior_witness_negatives':neg,'scope':'Exact affine representation and identities only. No variable-domain solve, no rank assertion and no target-code exclusion.'}
# Independent separable second transform; compare every original joint basis coefficient.
L=[poly(27,i) for i in range(28)]; R=[poly(37,j) for j in range(38)]
for k,J in enumerate(Jbasis):
 mid={(a,j):sum(T[i,j][k]*L[i][a] for i in range(28)) for a in range(28) for j in range(38)}
 for a in range(28):
  for b in range(38):assert sum(mid[a,j]*R[j][b] for j in range(38))==(2**64)*J.get((a,b),0)
res['symbolic_inverse_entries']=8512
print(json.dumps(res))
