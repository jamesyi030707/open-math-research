"""Exact short joint-character certificate; standard library only."""
import json,sys,itertools
from pathlib import Path
from fractions import Fraction
from collections import Counter
B=(0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
def require(c):
 if not c:raise ValueError('certificate failed')
def bw(u):
 x=0
 for i,b in enumerate(B):
  if u>>i&1:x^=b
 return x.bit_count()
def W(t):return ((t&31)<<4)^(1008 if t&32 else 0)
def chi(a,b):return 1-2*((a&b).bit_count()%2)
H=[t for t in range(64) if bw(2^W(t))==14]
require(len(H)==16)
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'2026-11-15/h.json'
S=[s['columns'] for s in json.loads(path.read_text())['solutions']]
def reachable(vectors):
 vals={tuple(0 for _ in vectors[0])}
 for v in vectors:
  vals={tuple(a+sg*b for a,b in zip(q,v)) for q in vals for sg in (-1,1)}
 return vals
def rank_consistency(M):
 A=[[Fraction(x) for x in row]+[Fraction(-1)] for row in M];r=0
 for k in range(27):
  pivot=next((i for i in range(r,16) if A[i][k]),None)
  if pivot is None:continue
  A[r],A[pivot]=A[pivot],A[r];d=A[r][k];A[r]=[x/d for x in A[r]]
  for i in range(16):
   if i!=r and A[i][k]:
    d=A[i][k];A[i]=[x-d*y for x,y in zip(A[i],A[r])]
  r+=1
  if r==16:break
 return r,not any(not any(row[:27]) and row[27] for row in A)
ranks=Counter();scalar_fail=[];pair_fail=[];control=None
for idx,c in enumerate(S):
 M=[[chi(t,v) for v in c] for t in H]
 rank,consistent=rank_consistency(M);require(consistent);ranks[rank]+=1
 coeff=[[sum(chi(t,v)*M[i][j] for i,t in enumerate(H)) for j in range(27)] for v in range(64)]
 targets=[-sum(chi(t,v) for t in H) for v in range(64)]
 require(all(x%4==0 for row in coeff for x in row) and all(x%4==0 for x in targets))
 coeff=[[x//4 for x in row] for row in coeff];targets=[x//4 for x in targets]
 for v in range(64):
  if (targets[v],) not in reachable([(x,) for x in coeff[v]]):scalar_fail.append([idx,v])
 points=reachable(list(zip(coeff[0],coeff[1])))
 if tuple(targets[:2]) not in points:pair_fail.append(idx)
 if idx==1:
  require(all(sum((t&v).bit_count()%2 for v in c) in (12,16) for t in range(1,32)))
  require(all(sum(((t+32)&v).bit_count()%2 for v in c) in (12,16) for t in range(1,32)))
  require(sum(v>>5 for v in c)==4)
  control={'index':idx,'columns':c,'H':H,'multipliers':[[chi(t,v) for t in H] for v in (0,1)],'coefficients_divided_by_4':coeff[:2],'target_divided_by_4':targets[:2],'rank':rank,'reachable_points':sorted(points),'reachable_count':len(points),'y_zero_x_values':sorted(x for x,y in points if y==0)}
require(len(S)==277 and dict(ranks)=={16:269,15:8} and not scalar_fail)
require(pair_fail==[0,1,2,3,5,6,7,8,9,11,12,13,14,15,16,17,18])
require(control['reachable_count']==47 and control['y_zero_x_values']==[-8,0,8])
print(json.dumps({'scope':'a=2 section; existing canonical local restrictions only','ranks':dict(ranks),'real_inconsistent':0,'scalar_tests':277*64,'scalar_failures':scalar_fail,'fixed_pair_rejections':pair_fail,'control':control,'newly_excluded_patterns_claimed':0},indent=2))
