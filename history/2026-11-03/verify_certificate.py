"""Standard-library checker: no elimination, solvers, or assignment search.
Verify two matrix identities modulo64, retaining the affine constant column.
"""
import csv,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent
C=json.loads((P/'certificate.json').read_text()); data=(P.parent/'2026-10-29'/'affine_coefficients.csv').read_bytes()
assert hashlib.sha256(data).hexdigest()==C['input_sha256']
rows=list(csv.DictReader(data.decode().splitlines()))
keys=['p','q','y10','y14','z8','z12','z16','constant']
assert C['columns']==keys and C['modulus']==64 and C['common_divisor']==16 and C['original_modulus']==1024
assert len(rows)==1064 and {(int(r['i']),int(r['j']))for r in rows}=={(i,j)for i in range(28)for j in range(38)}
assert all(int(r['denominator'])==1024 for r in rows)
A=[[int(r[k])for k in keys]for r in rows]
assert all(x%16==0 for r in A for x in r)
A=[[x//16%64 for x in r]for r in A]
B=C['basis']; U=C['basis_from_input_sparse']; V=C['input_from_basis']
assert len(B)==len(U)==6 and len(V)==1064
assert all(len(r)==8 for r in B) and all(len(r)==6 for r in V)
for b,u in zip(B,U):
 assert all(0<=i<1064 and isinstance(c,int)for i,c in u)
 assert all((sum(c*A[i][j]for i,c in u)-b[j])%64==0 for j in range(8))
for a,v in zip(A,V):
 assert all((sum(v[i]*B[i][j]for i in range(6))-a[j])%64==0 for j in range(8))
# Exact target expressions, including their affine constants, lifted to mod64.
# a*x+c = 0 modulo m, in the declared column order.
E=[([1,1,2,1,3,2,1,-12],64),([0,2,2,1,0,0,0,-8],16),
   ([0,1,1,0,0,-1,-1,-6],8),([0,1,0,0,2,0,2,0],4),
   ([0,0,0,0,0,1,1,0],2),([0,0,0,0,1,0,1,0],2)]
assert all(all((a*(64//m)-b)%64==0 for a,b in zip(e,r))for (e,m),r in zip(E,B))
w=[0,0,140,16,8,6,64,1]
assert all(sum(a*b for a,b in zip(r,w))%64==0 for r in A)
original=[[int(r[k])for k in keys]for r in rows]
vals=[sum(a*b for a,b in zip(r,w))//1024 for r in original]
negative=[(int(r['i']),int(r['j']),v)for r,v in zip(rows,vals)if v<0]
assert len(negative)==8 and (1,2,-16)in negative
print(json.dumps({'verified':True,'input_rows':len(A),'reduced_congruences':len(B),'forward_affine_identities':48,'reverse_affine_identities':8512,'witness_integral':True,'witness_negative_cells':negative},indent=2))
