#!/usr/bin/env python3
"""Independent column/count audit. Does not import or run the proposed checker.
Uses coordinate-vector dot products and polynomial coefficient multiplication.
"""
import json,csv,hashlib,itertools
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parent
src=json.loads((P/'input_sources.json').read_text())
for f in src['files']:
 raw=(P/f['local']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==f['git_blob_sha']
assert src['commit']=='74a2d33c0f9536100a7bed277db521b2707bdfd0'
r=json.loads((P/'inputs/residual_candidate.json').read_text())
rows=[[int(c) for c in format(int(s,16),'037b')[::-1]] for s in r['basis_hex']]
B=list(zip(*rows))
def dot(v,w):return sum(a*b for a,b in zip(v,w))%2
def label(v):return sum(b*2**k for k,b in enumerate(v))
V=list(itertools.product((0,1),repeat=10))
words={v:tuple(dot(v,c) for c in B) for v in V}
assert len(set(words.values()))==1024
weights={v:sum(w) for v,w in words.items()}
assert Counter(weights.values())=={0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1}
h,= [v for v,w in weights.items() if w>=27]
assert label(h)==1008
add=lambda v,w:tuple((a+b)%2 for a,b in zip(v,w))
pairs={frozenset((v,add(v,h))) for v,w in weights.items() if w==16 and weights[add(v,h)]==16}
S={v for v in V if all(v[k]==0 for k in [0,1,2,3,9])}
assert len(S)==32 and len(pairs)==31
assert all(len(p & S)==1 for p in pairs)
assert len(set(B))==37 and (0,)*10 not in B
compat=[c for c in B if dot(h,c)==0]
assert sorted(map(label,compat))==[1,4,7,13,15]
assert all(dot(s,c)==0 for s in S for c in compat)
allowed=[v for v in V if dot(v,h)==0]
slack={label(c):int(all(dot(s,c)==0 for s in S))-int(not any(c))-B.count(c) for c in allowed}
assert set(slack.values())=={0,1}
# Polynomial coefficients of (1-z)^w(1+z)^(n-w), independent of binomial-sum implementation.
def poly(n,w):
 out=[1]
 for sign in [-1]*w+[1]*(n-w):
  nxt=[0]*(len(out)+1)
  for k,a in enumerate(out):nxt[k]+=a;nxt[k+1]+=sign*a
  out=nxt
 return out
# Recover affine joint enumerator from category constants and signed parameter increments.
# Each row: left weight, paired right weights, constant and seven coefficients.
groups=[(14,(14,22),[160,0,0,0,0,0,0,0]),(12,(16,24),[0,1,0,0,0,0,0,0]),(16,(16,24),[80,-1,0,0,0,0,0,0]),(12,(16,16),[0,0,1,0,0,0,0,0]),(16,(16,16),[31,0,-1,0,0,0,0,0]),(10,(18,18),[0,0,0,1,0,0,0,0]),(14,(18,18),[0,0,0,0,1,0,0,0]),(18,(18,18),[160,0,0,-1,-1,0,0,0]),(8,(20,20),[0,0,0,0,0,1,0,0]),(12,(20,20),[0,0,0,0,0,0,1,0]),(16,(20,20),[0,0,0,0,0,0,0,1]),(20,(20,20),[80,0,0,0,0,-1,-1,-1]),(0,(0,32),[1,0,0,0,0,0,0,0])]
# Coordinates x = F (1,a,b,c,d,e,f,g).
F=[[4,64,-16,0,4,-4,-6,-6],[0,0,0,0,4,0,0,0],[6,0,0,8,-4,2,0,2],[-4,0,16,-16,0,-4,0,-4],[0,0,0,0,0,0,2,1],[0,0,0,0,0,2,0,1],[0,0,0,0,0,0,0,1]]
def transport(coeff):return [coeff[0]*int(k==0)+sum(coeff[t+1]*F[t][k] for t in range(7)) for k in range(8)]
aff=list(csv.DictReader((P/'inputs/affine_coefficients.csv').open()))
integer=list(csv.DictReader((P/'inputs/integer_coefficients.csv').open()))
assert len(aff)==len(integer)==1064
K={(n,w):poly(n,w) for n in [27,37] for w in range(n+1)}
derived=[]
for i in range(28):
 for j in range(38):
  a=[sum(co[t]*K[27,l][i]*sum(K[37,rw][j] for rw in rr) for l,rr,co in groups) for t in range(8)]
  z=i*38+j
  assert (int(aff[z]['i']),int(aff[z]['j']))==(i,j)
  assert [int(aff[z][k]) for k in ['constant','p','q','y10','y14','z8','z12','z16']]==a
  assert int(aff[z]['denominator'])==1024
  b=transport(a)
  assert all(x%1024==0 for x in b)
  b=[x//1024 for x in b]
  assert (int(integer[z]['i']),int(integer[z]['j']))==(i,j)
  assert [int(integer[z][k]) for k in ['constant',*'abcdefg']]==b
  derived.append(b)
assert derived[38]==[-6,1,0,0,0,0,0,0]
assert derived[39]==[4,-3,1,0,0,0,0,0]
assert transport([-60,1,5,-2,-1,3,2,1])==[-64,64,-32,0,32,0,0,0]
domain=list(csv.DictReader((P/'inputs/domain_inequalities.csv').open()))
def evaluate(u):
 v=[1]+u
 x=[sum(a*b for a,b in zip(row,v)) for row in F]
 p,q,y10,y14,z8,z12,z16=x
 constraints=[p,80-p,q,31-q,y10,y14,160-y10-y14,z8,z12,z16,80-z8-z12-z16]
 assert constraints==[sum(int(row[k])*a for k,a in zip(['constant',*'abcdefg'],v)) for row in domain]
 assert min(constraints)>=0
 dual=[sum(a*b for a,b in zip(row,v)) for row in derived]
 assert min(dual)>=0 and sum(dual)==2**54
 a,b,c,d,e,f,g=u
 return dict(u=u,x=x,split_tests=1064,domain_tests=11,old_pass=True,q_ge16=q>=16,new_slack=2*a+d-b-2,T10=dual[38],T11=dual[39],zero_on_S=d-4)
witness=evaluate([6,19,10,4,-31,-33,66]);assert witness['new_slack']==-5 and witness['x']==[26,16,140,0,0,4,66]
survivors=[evaluate([6,14,4,d,13,0,18]) for d in range(4,8)]
assert all(v['new_slack']>=0 for v in survivors)
# Mutation controls must break independent raw input and constraint checks.
try:evaluate([6,19,10,8,-31,-33,66])
except AssertionError:bad_count=True
else:raise AssertionError('Mutation not caught')
original=integer[39]['constant'];integer[39]['constant']=str(int(original)+1)
bad_coefficient=derived[39]!=[int(integer[39][k]) for k in ['constant',*'abcdefg']]
assert bad_coefficient
out=dict(verified=True,commit=src['commit'],method='Independent coordinate tuples, full 1024-message enumeration, polynomial multiplication, full affine-table identities',residual_columns=list(map(label,B)),heavy=label(h),S_labels=sorted(map(label,S)),pair_classes=len(pairs),compatible_B=sorted(map(label,compat)),per_column_controls=Counter(slack.values()),all_affine_and_integer_rows_verified=1064,count_expression_equals='32 * (2*a+d-b-2)',rejected=witness,survivors=survivors,mutation_controls={'invalid_count':bad_count,'altered_coefficient':bad_coefficient},proof=['For nonzero s in S, assumed target left weights give sum_s wt(sA)=12q+16(31-q)=496-4q. Each column nonzero on S contributes 16, so columns zero on S = 27-(496-4q)/16=q/4-4=d-4.','Dual coefficient T10 counts globally zero A columns, and T11 counts A/B column coincidences with multiplicities. Distinct, nonzero B columns make these disjoint subsets of A positions.','hA=0 ensures every matched B column is one of labels 1,4,7,13,15, which all annihilate S. Zero A columns also annihilate S. Thus T10+T11 <= d-4, giving 2a+d-b-2>=0.'],limitations=['Conditional on fixed residual basis and specified kernel-one target category model, especially hA=0 and S left weights 12/16.','The count form is 32 times the integer cut, not numerically equal to it.','Formal surviving points are not target code constructions, and no branch or global existence conclusion follows.','Local file hashes match the supplied commit manifest; this offline audit does not independently authenticate the remote GitHub commit.'])
# Audit the proposed explicit matrix as data, independently of its reported rank/counts.
control=json.loads((P/'column_cut_result.json').read_text())['controls']['rank_nine_saturated_left_matrix']
A=[tuple((v//2**k)%2 for k in range(10)) for v in control['column_labels']]
assert len(A)==27 and all(dot(h,c)==0 for c in A)
left={v:tuple(dot(v,c) for c in A) for v in V}
assert len(set(left.values()))==512 # rank nine, without Gaussian elimination
local=Counter(sum(left[s]) for s in S)
assert local=={0:1,12:16,16:15}
zs=sum(all(dot(s,c)==0 for s in S) for c in A)
z0=sum(not any(c) for c in A)
matches=sum(c==b for c in A for b in B)
assert (zs,z0,matches)==(0,0,0)
violations=sum(not (27-weights[v]<=sum(left[v])<=weights[v]) for v in V if any(v))
assert violations==130
out['rank_nine_matrix_control']={'length':27,'rank':9,'local_weights':dict(local),'zero_on_S':zs,'zero_columns':z0,'matching_columns':matches,'cut_slack':zs-z0-matches,'target_lift_bound_violations':violations,'is_target_construction':False}
(P/'audit_column_obstruction_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
