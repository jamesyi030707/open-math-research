import json, math, collections, time
from pathlib import Path
out=Path(__file__).parent
# GF64 polynomial x^6+x+1.
def mul(a,b):
 r=0
 while b:
  if b&1:r^=a
  b>>=1;a<<=1
  if a&64:a^=67
 return r
powers=[1]
for i in range(1,63):powers.append(mul(powers[-1],2))
assert len(set(powers))==63 and mul(powers[-1],2)==1
roots=set()
for i in range(1,27):
 j=i
 while j not in roots:
  roots.add(j);j=j*2%63
# Product (X-alpha^i) for binary cyclotomic closure.
g=[1]
for i in sorted(roots):
 r=[0]*(len(g)+1)
 for j,c in enumerate(g):r[j]^=mul(c,powers[i]);r[j+1]^=c
 g=r
assert set(g)<={0,1}
gint=sum(c<<i for i,c in enumerate(g))
basis=[gint<<i for i in range(63-(len(g)-1))]
assert len(basis)==10
words=[0]
for v in basis:words += [u^v for u in words]
ext=[v|((v.bit_count()%2)<<63) for v in words]
enum=dict(sorted(collections.Counter(v.bit_count() for v in ext).items()))
assert len(ext)==1024 and min(v.bit_count() for v in ext if v)==28 and (1<<64)-1 in ext

def K(j,w):return sum((-1)**i*math.comb(w,i)*math.comb(64-w,j-i) for i in range(max(0,j-(64-w)),min(j,w)+1))
C=[sum(a*K(j,w) for w,a in enum.items()) for j in range(65)]
assert all(c%1024==0 and c>=0 for c in C)
D=[c//1024 for c in C]
# For a possible odd coset, complement symmetry gives x each at27,37;
# y each at29,35; z each at31,33 and x+y+z=512.
T=[[K(j,w)+K(j,64-w) for w in [27,29,31]] for j in range(65)]
# Union with the linear code would be a dimension11 code. Its dual
# enumerator is (C+T.[x,y,z])/2048, integer between0 and D_j.
constraints=[]
for j in range(65):
 a,b,c=T[j]
 constraints.append((j,a-c,b-c,C[j]+512*c,2048*D[j]))
feasible=[];fail=collections.Counter()
for x in range(513):
 for y in range(513-x):
  z=512-x-y
  for j,a,b,c,hi in constraints:
   t=a*x+b*y+c
   if t<0 or t>hi or t%2048:
    fail[j]+=1;break
  else:feasible.append([x,y,z])
r={'field_primitive_polynomial':'x^6+x+1','generator_degree':len(g)-1,'generator_hex':hex(gint),'root_exponents':sorted(roots),'dimension':10,'minimum_distance':28,'contains_all_ones':True,'weight_enumerator':enum,'dual_weight_enumerator':{j:d for j,d in enumerate(D) if d},'coset_distribution_variables':'x=A27=A37,y=A29=A35,z=A31=A33; x+y+z=512','feasible_integer_distributions':feasible,'first_failed_constraints':dict(fail),'constraints_j_a_b_constant_upper':constraints}
(out/'results.json').write_text(json.dumps(r,indent=2))
print(json.dumps({k:v for k,v in r.items() if k not in ['root_exponents','dual_weight_enumerator','constraints_j_a_b_constant_upper','feasible_integer_distributions']},indent=2))
print('FEASIBLE',len(feasible),feasible[:30])
print('SMALL CONSTRAINTS',constraints[:13])
