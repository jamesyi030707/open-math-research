"""Optional numerical candidate finder, not a proof. Requires NumPy/SciPy.
The published witness is checked separately with exact standard-library arithmetic.
No generator matrix is constructed. A different solver/version may return another candidate.
"""
from math import comb
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
cats=[(16,24,12),(16,24,16),(16,16,12),(16,16,16),(18,18,10),(18,18,14),(18,18,18),(20,20,8),(20,20,12),(20,20,16),(20,20,20)]
def K(n,j,w):return sum((-1)**i*comb(w,i)*comb(n-w,j-i) for i in range(max(0,j-n+w),min(j,w)+1))
# L dual: j=1..27; D dual: j=1..6; C dual: j=1..6 and58..64.
# Full transforms are subsequently checked by the exact checker.
N=11+27+6+13;A=[];rhs=[]
for a,b,t in [(0,2,80),(2,4,31),(4,7,160),(7,11,80)]:
 row=[0]*N
 for i in range(a,b):row[i]=1
 A.append(row);rhs.append(t)
for code,n,size,js,start in [('A',27,512,27,11),('D',64,1024,6,38),('C',64,2048,13,44)]:
 for j in range(1,js+1):
  jj=j if code!='C' or j<=6 else 51+j
  row=[0]*N
  for i,(r,s,a) in enumerate(cats):
   weights={'A':[a],'D':[a+r,a+s],'C':[a+r,a+s,27-a+r,27-a+s]}[code]
   row[i]=sum(K(n,jj,w) for w in weights)
  fixed={'A':{0:1,14:160},'D':{0:1,32:1,28:160,36:160},'C':{0:1,27:161,32:1,59:1,28:160,36:160,35:160}}[code]
  row[start+j-1]=-size;A.append(row);rhs.append(-sum(v*K(n,jj,w) for w,v in fixed.items()))
res=milp(np.zeros(N),integrality=np.ones(N),bounds=Bounds(np.zeros(N),np.r_[[80]*2,[31]*2,[160]*3,[80]*4,[np.inf]*(N-11)]),constraints=LinearConstraint(np.array(A,float),rhs,rhs),options={'time_limit':20})
print(res.message)
if res.x is not None:
 vals=np.rint(res.x).astype(int).tolist();print(vals);print('exact',all(sum(a*b for a,b in zip(row,vals))==r for row,r in zip(A,rhs)))
