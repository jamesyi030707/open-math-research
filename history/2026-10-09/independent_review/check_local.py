from fractions import Fraction

def v2(n): return (n&-n).bit_length()-1

def w(m,L):
 a=1 if m%2 else v2(m)+2
 return ((pow(3,m,1<<(a+L))-1)%(1<<(a+L)))>>a

def parity(x,L):
 out=0
 for j in range(L):
  out|=(x%2)<<j
  x=(3*x+1)//2 if x%2 else x//2
 return out

checks=0
for e in range(6):
 for L in range(1,11):
  p=1<<(max(1,L-1) if e==0 else e+L)
  xs=[m for m in range(1,p+1) if v2(m)==e]
  ys=[w(m,L) for m in xs]
  expected=(1 if L==1 else 1<<(L-2)) if e==0 else 1<<(L-1)
  assert len(set(ys))==expected
  if e: assert set(ys)==set(range(1,1<<L,2))
  elif L>=2: assert set(ys)==set(range(1,1<<L,4))
  for m,y in zip(xs,ys):
   assert w(m+p,L)==y
   assert parity((3**m-1)//(1<<(1 if e==0 else e+2)),L)==parity(y,L)
   checks+=1
print('PASS lifting/image/period/parity:',checks,'representatives; e=0..5,L=1..10')

# Independent reconstruction; no imports or reads from Claude's files.
covered=[]; prefixes=set(); max_threshold=Fraction(0)
for r in range(4096):
 x=r; A=1; B=0; bits=[]; first=None
 for j in range(1,13):
  bit=x&1;bits.append(bit)
  if bit: x=(3*x+1)//2; A*=3; B=3*B+(1<<(j-1))
  else: x//=2
  D=(1<<j)-A
  if D>0 and first is None:
   first=j; threshold=Fraction(B,D)
   q=r% (1<<j); nmin=q
   while nmin<=1: nmin+=1<<j
   assert nmin>threshold
   prefixes.add(tuple(bits));max_threshold=max(max_threshold,threshold)
 if first is not None: covered.append(r)
assert len(prefixes)==57 and len(covered)==3870
assert sum(r%2==0 for r in covered)==2048
assert sum(r%2==1 for r in covered)==1822
assert set(range(1,4096,4))<=set(covered)
assert max_threshold==Fraction(319,13)
print('PASS independently reconstructed k12:',len(prefixes),'prefixes;',len(covered),'covered;',4096-len(covered),'open')
print('PASS strict least-n>1 threshold in every stopping prefix; maximum',max_threshold)
print('PASS all 2048 even residues covered; 1822 odd covered; all 1 mod4 covered')
print('Conditional-layer density:',Fraction(1822,2048))
