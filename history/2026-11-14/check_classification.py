"""Exact bounded q=28 classification and section compatibility verifier.
Python standard library only. No target-matrix search or numerical solver.
"""
import json,itertools,time
from collections import Counter
start=time.process_time()
def require(c,msg):
 if not c:raise ValueError(msg)
def dot(a,b):return (a&b).bit_count()%2
def basis(xs):
 p={}
 for v in xs:
  while v:
   k=v.bit_length()-1
   if k in p:v^=p[k]
   else:p[k]=v;break
 return list(p.values())
ROWS=[0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897]
def residual_weight(u):
 w=0
 for i,b in enumerate(ROWS):
  if u>>i&1:w^=b
 return w.bit_count()
def wmsg(t):return ((t&31)<<4)^(1008 if t&32 else 0)
def span(bs):
 s={0}
 for b in bs:s|={x^b for x in list(s)}
 return frozenset(s)
def subs(d):
 out={frozenset({0})}
 for _ in range(d):out={span(tuple(s)+(v,)) for s in out for v in range(1,32) if v not in s}
 return sorted(out,key=lambda s:tuple(sorted(s)))
Us=subs(3);Ts=subs(2)
secs=[]
for a in (2,3,5,6):
 H=[t for t in range(64) if residual_weight(a^wmsg(t))==14]
 require(len(H)==16,'section size')
 proj={t&31:t>>5 for t in H};o=min(proj)
 require(len(proj)==16,'graph projection')
 bs=basis(sorted(x^o for x in proj))
 require(len(bs)==4,'hyperplane dimension')
 xs=[0]
 for b in bs:xs += [x^b for x in xs]
 require({o^x for x in xs}==set(proj),'hyperplane equality')
 g=[proj[o^x] for x in xs]
 G=[sum((-1)**(g[x]^dot(x,z)) for x in range(16)) for z in range(16)]
 require(all(abs(v)==4 for v in G),'bent spectrum')
 for v in range(32):
  lam=sum(dot(v,b)<<i for i,b in enumerate(bs))
  for e in (0,1):
   actual=[sum((-1)**(dot(v,o^xs[x])^(e*g[x])^dot(x,z)) for x in range(16)) for z in range(16)]
   expected=[(-1)**dot(v,o)*(G[z^lam] if e else 16*int(z==lam)) for z in range(16)]
   require(actual==expected,'single column transform')
 secs.append({'coset':a,'projection_origin':o,'projection_basis':bs,'graph_Walsh':G,'H':H})
require(len(Us)==155 and len(Ts)==155,'subspace counts')
pre={}
positive=None
for sec in secs:
 bs=sec['projection_basis']; G=sec['graph_Walsh']; K=[[G[z^l]//4 for l in range(16)] for z in range(16)]
 lam=[sum(((v&b).bit_count()%2)<<i for i,b in enumerate(bs)) for v in range(32)]
 for T in Ts:
  line=sorted(T-{0})
  for r in (4,24):
   small=line+[0] if r==4 else line
   arr=[]
   for signs in itertools.product((-1,1),repeat=len(small)):
    c=[0]*16
    for v,y in zip(small,signs):c[lam[v]]+=y
    if r==4:num=[-4*int(z==0)-sum(K[z][l]*c[l] for l in range(16)) for z in range(16)]
    else:
     c[0]+=1
     num=[-sum(K[z][l]*c[z] for z in range(16)) for l in range(16)]
    if all(n%4==0 for n in num):arr.append((tuple(n//4 for n in num), signs))
   pre[(sec['coset'],T,r)]=(lam,arr)
res={4:Counter(),24:Counter()}; survivors={4:[],24:[]}; paircount=0
for U in Us:
 for T in Ts:
  if U&T!={0}:continue
  paircount+=1
  big=sorted(set(range(32))-U-T)
  for r in (4,24):
   rejected=None
   for sec in secs:
    lam,arr=pre[(sec['coset'],T,r)]; M=Counter(lam[v] for v in big+[0]*(2 if r==4 else 3))
    feasible=[(c,signs) for c,signs in arr if all(abs(c[z])<=M[z] and (c[z]-M[z])%2==0 for z in range(16))]
    if not feasible:rejected=sec['coset'];break
    if positive is None:
     c,signs=feasible[0]
     small=sorted(T-{0})+([0] if r==4 else [])
     large=big+[0]*(2 if r==4 else 3)
     e_small=int(r==4);e_large=1-e_small
     signed=[(v,e_small,y) for v,y in zip(small,signs)]
     for z in range(16):
      group=[v for v in large if lam[v]==z]
      nplus=(len(group)+c[z])//2
      signed += [(v,e_large,1 if i<nplus else -1) for i,v in enumerate(group)]
     # Undo the origin sign before comparing directly in original W coordinates.
     cols=[v+32*e for v,e,y in signed]
     ys=[y*(-1)**dot(v,sec['projection_origin']) for v,e,y in signed]
     direct=[sum(y*(-1)**dot(t,v) for y,v in zip(ys,cols)) for t in sec['H']]
     require(direct==[-1]*16,'real section positive witness')
     bad=ys[:];bad[0]*=-1
     require(any(sum(y*(-1)**dot(t,v) for y,v in zip(bad,cols))!=-1 for t in sec['H']),'damaged positive witness')
     positive={'U':sorted(U),'T':sorted(T),'r':r,'coset':sec['coset'],'columns':cols,'outside_bits':[int(y==-1) for y in ys],'direct_character_sums':direct}
   if rejected is None:survivors[r].append([sorted(U),sorted(T)])
   else:res[r][rejected]+=1
require(paircount==9920,'pair count')
require(all(not x for x in survivors.values()),'all cases rejected')
require(positive is not None,'positive control exists')
out={'positive_control':positive,'U_count':len(Us),'T_count':len(Ts),'pairs':paircount,'rejections':res,'survivor_counts':{r:len(x) for r,x in survivors.items()},'survivors':survivors,'cpu_seconds':time.process_time()-start,'passed':True}
print(json.dumps(out,indent=2))
