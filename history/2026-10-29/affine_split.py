"""Exact affine split MacWilliams model, fixed residual/kernel-one branch.
Standard library, no solver and no enumeration of the integer count domain.
Print summary by default; --table prints all 1064 numerator rows as CSV.
"""
from collections import defaultdict
from fractions import Fraction
from math import comb,gcd
from functools import reduce
import json,sys,csv
VARS=['p','q','y10','y14','z8','z12','z16']
# Each pair contributes both residual weights, even when they coincide.
GROUPS=[(14,22,14,[160,0,0,0,0,0,0,0]),
 (16,24,12,[0,1,0,0,0,0,0,0]),(16,24,16,[80,-1,0,0,0,0,0,0]),
 (16,16,12,[0,0,1,0,0,0,0,0]),(16,16,16,[31,0,-1,0,0,0,0,0]),
 (18,18,10,[0,0,0,1,0,0,0,0]),(18,18,14,[0,0,0,0,1,0,0,0]),
 (18,18,18,[160,0,0,-1,-1,0,0,0]),
 (20,20,8,[0,0,0,0,0,1,0,0]),(20,20,12,[0,0,0,0,0,0,1,0]),
 (20,20,16,[0,0,0,0,0,0,0,1]),(20,20,20,[80,0,0,0,0,-1,-1,-1])]
def K(n,j,w):
 return sum((-1)**t*comb(w,t)*comb(n-w,j-t) for t in range(max(0,j-(n-w)),min(j,w)+1))
def joint_basis():
 J=defaultdict(lambda:[0]*8)
 J[0,0][0]=J[0,32][0]=1
 for r,s,a,v in GROUPS:
  for b in [r,s]:
   J[a,b]=[x+y for x,y in zip(J[a,b],v)]
 return dict(J)
def make_table():
 J=joint_basis();left={a:[K(27,i,a) for i in range(28)] for a,b in J};right={b:[K(37,j,b) for j in range(38)] for a,b in J}
 return {(i,j):[sum(v[k]*left[a][i]*right[b][j] for (a,b),v in J.items()) for k in range(8)] for i in range(28) for j in range(38)}
def main(table=False):
 J=joint_basis();T=make_table()
 assert [sum(v[k] for v in J.values()) for k in range(8)]==[1024]+[0]*7
 assert T[0,0]==[1024]+[0]*7
 assert [sum(v[k] for v in T.values()) for k in range(8)]==[1024*2**54]+[0]*7
 # Vandermonde/Krawtchouk convolution: identity in all seven variables.
 for w in range(65):
  diagonal=[sum(v[k] for (i,j),v in T.items() if i+j==w) for k in range(8)]
  ordinary=[sum(v[k]*K(64,w,a+b) for (a,b),v in J.items()) for k in range(8)]
  assert diagonal==ordinary
 # Invert the unnormalized table symbolically, retaining all eight affine columns.
 L=[[K(27,a,i) for i in range(28)] for a in range(28)]
 R=[[K(37,b,j) for j in range(38)] for b in range(38)]
 mid={(a,j):[sum(L[a][i]*T[i,j][k] for i in range(28)) for k in range(8)] for a in range(28) for j in range(38)}
 for a in range(28):
  for b in range(38):
   back=[sum(R[b][j]*mid[a,j][k] for j in range(38)) for k in range(8)]
   assert back==[2**64*x for x in J.get((a,b),[0]*8)]
 # Both source blocks have even weight: dual complement symmetries are affine identities.
 assert all(v==T[27-i,j]==T[i,37-j] for (i,j),v in T.items())
 assert all(T[0,j][k]==0 for j in range(38) for k in range(1,8))
 assert T[1,2]==[91264,288,-96,-576,-288,-672,-448,-224]
 witness=[1,0,0,140,16,8,6,64]
 old={ij:Fraction(sum(a*b for a,b in zip(v,witness)),1024) for ij,v in T.items()}
 assert all(v.denominator==1 for v in old.values())
 negatives=[[i,j,int(v)] for (i,j),v in old.items() if v<0]
 assert len(negatives)==8 and old[1,2]==-16
 if table:
  w=csv.writer(sys.stdout,lineterminator='\n');w.writerow(['i','j','constant']+VARS+['denominator'])
  for (i,j),v in T.items():w.writerow([i,j]+v+[1024])
  return
 result={'variables':VARS,'domain':['all counts integral','0 <= p <= 80','0 <= q <= 31','y10,y14 >= 0; y10+y14 <= 160','z8,z12,z16 >= 0; z8+z12+z16 <= 80'],
 'partition':[27,37],'source_dimension':10,'normalization':1024,'split_rows':len(T),'affine_entries':len(T)*8,
 'source_joint_support':len(J),'dual_size':2**54,'zero_coefficient':[1,0,0,0,0,0,0,0],
 'normalization_coefficient_sums':[2**54]+[0]*7,'ordinary_diagonal_identities':65,
 'complement_orbits':14*19,'row_1_2_numerators':T[1,2],
 'prior_witness_negative_cells':negatives,'checks':['all 8512 integer affine entries','inverse transform in all eight affine columns','source total1024','dual zero coefficient1','dual total2^54','65 diagonal affine identities','both block complement symmetries','fixed right marginal','prior fixed negative witness'],
 'scope':'Exact necessary-condition representation only for this fixed residual and kernel-one category model; no integer-domain solve, matrix search, feasibility decision or new target-code exclusion.'}
 print(json.dumps(result,indent=2))
if __name__=='__main__':main('--table' in sys.argv)
