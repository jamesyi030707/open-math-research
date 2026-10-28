import json,itertools
from fractions import Fraction
from pathlib import Path
root=Path(__file__).resolve().parent
def poly(n,w):
 p=[1]
 for s in [-1]*w+[1]*(n-w):
  q=[0]*(len(p)+1)
  for i,x in enumerate(p):q[i]+=x;q[i+1]+=s*x
  p=q
 return p
out=[]
for case in json.loads((root/'control_result.json').read_text())['controls']:
 n=case['length'];m=case['left_block_low_bits']; rows=[int(x,2) for x in case['rows_msb_first']]
 C=[]
 for bits in itertools.product([0,1],repeat=len(rows)):
  x=0
  for b,r in zip(bits,rows):
   if b:x^=r
  C.append(x)
 assert len(set(C))==2**case['dimension']
 assert min(x.bit_count() for x in C if x)==case['min_distance']
 dual=[x for x in range(2**n) if all((x&r).bit_count()%2==0 for r in rows)]
 J=lambda words:[[sum((x%(2**m)).bit_count()==i and (x//(2**m)).bit_count()==j for x in words) for j in range(n-m+1)] for i in range(m+1)]
 direct=J(dual); src=J(C)
 tr=[[Fraction(sum(src[a][b]*poly(m,a)[i]*poly(n-m,b)[j] for a in range(m+1) for b in range(n-m+1)),len(C)) for j in range(n-m+1)] for i in range(m+1)]
 assert tr==direct
 assert sum(map(sum,tr))==len(dual)
 assert [[i,j,v] for i,row in enumerate(direct) for j,v in enumerate(row) if v]==case['dual_joint']
 assert [sum(direct[i][j] for i in range(m+1) for j in range(n-m+1) if i+j==w) for w in range(n+1)]==case['ordinary_dual']
 assert Fraction(sum(map(sum,src)),2*len(C))==Fraction(1,2)
 back=[[Fraction(sum(direct[a][b]*poly(m,a)[i]*poly(n-m,b)[j] for a in range(m+1) for b in range(n-m+1)),len(dual)) for j in range(n-m+1)] for i in range(m+1)]
 assert back==src
 out.append({'n':n,'k':len(rows),'d':case['min_distance'],'dual_size':len(dual),'cells':(m+1)*(n-m+1),'pass':True})
# Derive each pair's contribution from literal polynomial coefficients.
f=lambda a,r:(27-2*a)*poly(37,r)[2]
pair=lambda a,r,s:f(a,r)+f(a,s)
const=f(0,0)+f(0,32)+160*pair(14,14,22)+80*pair(16,16,24)+31*pair(16,16,16)+160*pair(18,18,18)+80*pair(20,20,20)
coef=[pair(12,16,24)-pair(16,16,24),pair(12,16,16)-pair(16,16,16),pair(10,18,18)-pair(18,18,18),pair(14,18,18)-pair(18,18,18),pair(8,20,20)-pair(20,20,20),pair(12,20,20)-pair(20,20,20),pair(16,20,20)-pair(20,20,20)]
c=json.loads((root/'category_cut.json').read_text());assert const==c['numerator_constant'] and coef==c['numerator_coefficients']
assert const+sum(a*b for a,b in zip(coef,[0,0,140,16,8,6,64]))==-16384
result={'controls':out,'constant':const,'coefficients':coef,'scope':'Finite positive controls and affine identity only; no target feasibility decision.'}
print(json.dumps(result,indent=2))
