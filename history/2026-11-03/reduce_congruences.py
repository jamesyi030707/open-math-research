"""Exact bounded row-module reduction; no search over variable assignments."""
import csv, json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
KEYS=['p','q','y10','y14','z8','z12','z16','constant']
M=64
raw=list(csv.DictReader((ROOT.parent/'2026-10-29'/'affine_coefficients.csv').open()))
A=[[int(r[k]) for k in KEYS] for r in raw]
assert len(A)==1064 and all(int(r['denominator'])==1024 for r in raw)
assert all(v%16==0 for row in A for v in row)
A=[[v//16%M for v in row] for row in A]
R=[row[:] for row in A]; C=[{i:1}for i in range(len(A))]; cols=list(range(8)); k=0
# Each pivot has globally minimal 2-adic valuation in its remaining block.
# Consequently its value divides every remaining entry; its annihilator
# annihilates its entire row. No nonunit division of an equation is used.
def val(v): return (v & -v) if v else M
while k<8:
 d,i,j=min((val(R[i][j]),i,j)for i in range(k,len(R))for j in range(k,8))
 if d==M:break
 R[k],R[i]=R[i],R[k];C[k],C[i]=C[i],C[k]
 cols[k],cols[j]=cols[j],cols[k]
 for row in R:row[k],row[j]=row[j],row[k]
 u=pow(R[k][k]//d,-1,M)
 R[k]=[v*u%M for v in R[k]];C[k]={i:v*u%M for i,v in C[k].items() if v*u%M}
 assert R[k][k]==d and all(v%d==0 for v in R[k])
 for i in range(k+1,len(R)):
  assert R[i][k]%d==0
  q=R[i][k]//d
  R[i]=[(a-q*b)%M for a,b in zip(R[i],R[k])]
  for t,v in C[k].items(): C[i][t]=(C[i].get(t,0)-q*v)%M
  C[i]={t:v for t,v in C[i].items() if v}
 k+=1
assert all(not any(r) for r in R[k:])
B=[]
for row in R[:k]:
 out=[0]*8
 for j,c in enumerate(cols):out[c]=row[j]
 B.append(out)
# Independent short equalities: B=UA and A=VB, all modulo64.
U=[[[i,v]for i,v in sorted(c.items())] for c in C[:k]]
V=[]
for row in A:
 residual=row[:]; coeff=[]
 for j,b in enumerate(B):
  d=b[cols[j]];assert residual[cols[j]]%d==0
  q=residual[cols[j]]//d;coeff.append(q)
  residual=[(a-q*v)%M for a,v in zip(residual,b)]
 assert not any(residual)
 V.append(coeff)
cert={'input_sha256':hashlib.sha256((ROOT.parent/'2026-10-29'/'affine_coefficients.csv').read_bytes()).hexdigest(),'original_modulus':1024,'common_divisor':16,'modulus':64,'columns':KEYS,'basis':B,'basis_from_input_sparse':U,'input_from_basis':V,'pivot_columns':cols[:k],'pivot_values':[R[j][j] for j in range(k)]}
(ROOT/'certificate.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
print(json.dumps({k:v for k,v in cert.items()if k not in ['input_from_basis']},indent=2))
