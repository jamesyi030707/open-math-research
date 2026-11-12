from pathlib import Path
from collections import Counter
import json,hashlib,time,itertools
T=time.process_time()
def require(x,s):
 if not x: raise ValueError(s)
def par(x):return x.bit_count()%2
def rank(xs):
 b={}
 for x in xs:
  while x:
   p=x.bit_length()
   if p in b:x^=b[p]
   else:b[p]=x;break
 return len(b)
raw=(Path(__file__).parent/'inputs/residual_candidate.json').read_bytes()
require(hashlib.sha256(raw).hexdigest()=='276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80','input pin')
B=[int(s,16) for s in json.loads(raw)['basis_hex']]
def bw(u):
 x=0
 for i,b in enumerate(B):
  if u>>i&1:x^=b
 return x.bit_count()
w=[bw(u) for u in range(1024)];h=1008
require(rank(B)==10 and w[h]==32,'residual rank and h')
require(all(w[s<<4]==w[(s<<4)^h]==16 for s in range(1,32)),'W residual weights')
# Rigidity prerequisite, independently rebuild degree <= 2 evaluation rows.
pairs=list(itertools.combinations(range(10),2))
evals=[u | sum((((u>>i)&1)*((u>>j)&1))<<(10+k) for k,(i,j) in enumerate(pairs)) for u in range(1024) if w[u]==14]
require(len(evals)==160 and rank(evals)==55,'double-even rigidity')
windows={str(b):[a for a in range(28) if 27-b<=a<=b and (a+b)%4==0] for b in sorted(set(w[1:]))}
require(windows['32']==list(range(0,25,4)),'h window, remove zero in kernel-zero branch')
summary=[]
for q in [16,20,24,28]:
 L=31-q//4;M=992-14*q-L*L;R=(M-L)//2
 keep=[]
 for r in range(4,25,4):
  for z in range(28-L):
   qp=q+r//4-8*z;P=r*(28-r)//32+z*(L+z-28)
   # Both h-selected and h-unselected active columns have XOR zero:
   # self-orthogonality, plus S evenness. One nonzero column is impossible.
   if 0<=qp<=31 and 0<=P<=R and r-z!=1 and L-(r-z)!=1:keep.append({'r':r,'z':z,'qprime':qp,'P':P})
 summary.append({'q':q,'L':L,'M':M,'pair_budget':R,'survivors':keep})
require(sorted(set(k['r'] for k in summary[3]['survivors']))==[4,24],'q28 cut')
require(sorted(set(k['r'] for k in summary[2]['survivors']))==[4,8,20,24],'q24 cut')
# Real six-dimensional controls: complement of a 3-flat in F2^5.
active=list(range(8,32));line=[8,16,24]; controls=[]
for r in [4,24]:
 offsets=[int(v in line) if r==4 else int(v not in line) for v in active]
 zeros=[1,0,0] if r==4 else [1,1,1]
 cols=[v|(e<<5) for v,e in zip(active,offsets)]+[e<<5 for e in zeros]
 ww=[sum(par(u&c) for c in cols) for u in range(64)]
 require(rank(cols)==6,'real control rank six')
 require(ww[32]==r and set(ww[1:32]+ww[33:])<={12,16},'real W windows')
 q=ww[1:32].count(12);qp=ww[33:].count(12);L=24;z=sum(zeros)
 split=Counter((c&31,c>>5) for c in cols);P=sum(split[v,0]*split[v,1] for v in range(1,32))
 require(q==28 and qp==q+r//4-8*z,'first moment')
 require(P==r*(28-r)//32+z*(L+z-28)==0,'second moment')
 controls.append({'r':r,'columns':cols,'rank':6,'q':q,'qprime':qp,'z':z,'P':P,'weights':dict(Counter(ww))})
# Exhaustive genuine small-column controls for the unrestricted affine moment identity.
# General identity: sum w(s+h)^2 - sum w(s)^2 = 32Lz+32z^2-32P in dimension five.
checks=0
for d in range(1,4):
 for cols in itertools.combinations_with_replacement(range(1<<(d+1)),4):
  base=[sum(par(s&c) for c in cols) for s in range(1<<d)]
  aff=[sum(par((s|(1<<d))&c) for c in cols) for s in range(1<<d)]
  mask=(1<<d)-1;sp=Counter((c&mask,c>>d) for c in cols)
  L=sum(c&mask!=0 for c in cols);z=sp[0,1];P=sum(sp[v,0]*sp[v,1] for v in range(1,1<<d))
  require(sum(a*a for a in aff)-sum(a*a for a in base)==(1<<d)*(L*z+z*z-P),'general moment identity')
  checks+=1
# Negative control: formal r12,q28,z0 meets first moment and per-message W supports,
# but distinct columns imply P0 while the new identity demands P6.
require(28+12//4==31 and 12*(28-12)//32==6,'negative first-moment witness')
result={'scope':'fixed residual, kernel-zero necessary conditions; no full lift or exclusion','windows':windows,'cases':summary,'real_controls':controls,'small_real_controls':checks,'negative_control':{'q':28,'r':12,'z':0,'qprime':31,'required_P':6,'available_P':0},'cpu_seconds':time.process_time()-T}
print(json.dumps(result,indent=2))
