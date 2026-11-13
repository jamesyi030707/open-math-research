"""Exact geometry check for the fixed residual's ten minimum-word sections.
No solver, target-code search, or full branch exclusion. Python stdlib only.
"""
import json, time
from collections import Counter
START=time.process_time()
ROWS=[0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897]
def require(c,m):
 if not c:raise ValueError(m)
def span(xs):
 out=[0]
 for x in xs:out += [y^x for y in out]
 return out
def basis(xs):
 piv={}
 for v in xs:
  while v:
   k=v.bit_length()-1
   if k in piv:v^=piv[k]
   else:piv[k]=v;break
 return list(piv.values())
def dot(a,b):return (a&b).bit_count()%2
def graph_info(points):
 origin=points[0]
 diffs={p^origin for p in points}
 return {'size':len(points),'affine_span_dimension':len(basis(diffs)),
         'is_affine_flat':len(span(basis(diffs)))==len(points)}
words=span(ROWS)
weights=[x.bit_count() for x in words]
W=[((s&31)<<4)^(1008 if s&32 else 0) for s in range(64)]
require(len(set(W))==64,'W dimension')
sections=[]
for t in range(16):
 H=[s for s in range(64) if weights[t^W[s]]==14]
 if not H:continue
 info=graph_info(H)
 require(info=={'size':16,'affine_span_dimension':5,'is_affine_flat':False},'nonflat section')
 proj={s&31:s>>5 for s in H}
 require(len(proj)==16,'graph not injective')
 o=min(proj);bs=basis(sorted(x^o for x in proj));xs=span(bs)
 require(len(bs)==4 and set(o^x for x in xs)==set(proj),'projection affine hyperplane')
 g=[proj[o^x] for x in xs];anf=g[:]
 for j in range(4):
  for x in range(16):
   if x>>j&1:anf[x]^=anf[x^(1<<j)]
 terms=[x for x,a in enumerate(anf) if a]
 require(max(x.bit_count() for x in terms)==2,'quadratic degree')
 spectrum=[sum((-1)**(g[x]^dot(x,z)) for x in range(16)) for z in range(16)]
 require(all(abs(a)==4 for a in spectrum),'bent')
 K=[[spectrum[z^v]//4 for v in range(16)] for z in range(16)]
 require(all(sum(K[z][v]*K[y][v] for v in range(16))==(16 if z==y else 0) for z in range(16) for y in range(16)),'Hadamard identity')
 # The exact Fourier formula is tested for every one-column character (v,e).
 # Summing these identities gives any signed column multiset, including repeats/zeros.
 for v in range(32):
  lam=sum(dot(v,b)<<i for i,b in enumerate(bs))
  for e in (0,1):
   vals=[(-1)**(dot(v,o^x)^(e*g[i])) for i,x in enumerate(xs)]
   direct=[sum(vals[x]*(-1)**dot(x,z) for x in range(16)) for z in range(16)]
   expected=[(-1)**dot(v,o)*(16*int(z==lam) if e==0 else spectrum[z^lam]) for z in range(16)]
   require(direct==expected,'character transform')
 sections.append({'coset':t,'W_coordinate_messages':H,**info,'projection_origin':o,'projection_basis':bs,'graph_ANF_bitmasks':terms,'graph_Walsh':spectrum})
require(len(sections)==10,'ten sections')
# A true affine four-flat with same cardinality is correctly accepted.
flat=[3^x for x in span([1,2,4,8])]
require(graph_info(flat)=={'size':16,'affine_span_dimension':4,'is_affine_flat':True},'affine positive control')
# A real affine binary-column model, with repeated and zero columns, is
# constant of weight 14 on this flat: 14 constant-one zero-label columns.
control_columns=[0]*27
control_offsets=[1]*14+[0]*13
control_weights=[sum(dot(x,v)^b for v,b in zip(control_columns,control_offsets)) for x in flat]
require(control_weights==[14]*16,'real affine column positive control')
result={'scope':'Fixed residual geometry and exact section Fourier transform only; no exclusion.',
        'residual_weight_distribution':dict(sorted(Counter(weights).items())),
        'sections':sections,'single_column_transform_tests':10*64,
        'true_affine_control':graph_info(flat),'real_column_control_weights':dict(Counter(control_weights)),
        'cpu_seconds':time.process_time()-START,'passed':True}
print(json.dumps(result,indent=2))
