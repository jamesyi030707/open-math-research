#!/usr/bin/env python3
"""Exhaustive, exact quadratic-rank obstruction for the specified BCH parent.
Standard library only. No search over target Boolean functions.
"""
from itertools import combinations
from collections import Counter
from pathlib import Path
import json,time

def fwht(a):
 a=list(a); step=1
 while step<len(a):
  for start in range(0,len(a),2*step):
   for j in range(start,start+step):
    u,v=a[j],a[j+step]; a[j],a[j+step]=u+v,u-v
  step*=2
 return a

def span_add(basis,span,candidates):
 for w in sorted(candidates):
  if w not in span:
   basis.append(w); span.update([w^v for v in span])
 return basis,span

def main():
 start=time.process_time(); gen=0x2759262d5d506d
 E=[]
 for m in range(1024):
  w=0
  for j in range(10):
   if m>>j&1:w^=gen<<j
  w|=(w.bit_count()%2)<<63; E.append(w)
 E=set(E); assert len(E)==1024
 rm={w for w in E if w.bit_count() in (0,32,64)}
 one=(1<<64)-1
 rb,rs=span_add([one],{0,one},rm)
 assert len(rb)==7 and rs==rm
 labels=[sum(((rb[j+1]>>i)&1)<<j for j in range(6)) for i in range(64)]
 assert sorted(labels)==list(range(64)); pos=[labels.index(x) for x in range(64)]
 qb,es=span_add([],set(rm),E); assert len(qb)==3 and es==E
 pairs=list(combinations(range(6),2)); qmask=[]
 for w in qb:
  a=[w>>pos[x]&1 for x in range(64)]
  for j in range(6):
   for x in range(64):
    if x>>j&1:a[x]^=a[x^(1<<j)]
  assert all(not c or x.bit_count()<=2 for x,c in enumerate(a))
  qmask.append(sum(a[(1<<i)|(1<<j)]<<k for k,(i,j) in enumerate(pairs)))
 Q=[0]
 for q in qmask:Q += [x^q for x in Q]
 def rank(mask):
  rows=[0]*6
  for k,(i,j) in enumerate(pairs):
   if mask>>k&1:rows[i]^=1<<j; rows[j]^=1<<i
  r=0
  for j in range(6):
   p=next((i for i in range(r,6) if rows[i]>>j&1),None)
   if p is None:continue
   rows[r],rows[p]=rows[p],rows[r]
   for i in range(6):
    if i!=r and rows[i]>>j&1:rows[i]^=rows[r]
   r+=1
  return r
 ranks=[rank(m) for m in range(1<<15)]
 assert all(ranks[q]==6 for q in Q[1:])
 hist=Counter(); minhist=Counter(); allbent=[]
 for m in range(1<<15):
  rr=tuple(sorted(ranks[m^q] for q in Q)); hist[rr]+=1; minhist[min(rr)]+=1
  if min(rr)==6:allbent.append(m)
 assert not allbent
 # Independently check spectral rank formula and exact inverse normalization
 # for EVERY homogeneous quadratic, not merely a representative per rank.
 monomials=[sum(((x>>i&1)&(x>>j&1))<<x for x in range(64)) for i,j in pairs]
 truth=[0]*(1<<15)
 for m in range(1,1<<15):
  low=m&-m; truth[m]=truth[m^low]^monomials[low.bit_length()-1]
 for m,w in enumerate(truth):
  signs=[1-2*(w>>x&1) for x in range(64)]; W=fwht(signs)
  r=ranks[m]; amp=1<<(6-r//2)
  assert sum(v!=0 for v in W)==1<<r
  assert all(v==0 or abs(v)==amp for v in W)
  eps=[v//amp for v in W]
  assert fwht(eps)==[(64//amp)*s for s in signs]
  assert sum(e*v for e,v in zip(eps,W))==amp*(1<<r)
 bounds=[]
 for r in (0,2,4):
  amp=1<<(6-r//2); size=1<<r; initial=amp*size; cap=10*size
  change=2*(64//amp); raw=(initial-cap+change-1)//change
  odd=raw if raw%2 else raw+1
  bounds.append(dict(rank=r,walsh_amplitude=amp,support_size=size,initial_functional=initial,target_max=cap,max_change_per_flip=change,minimum_flips=raw,minimum_odd_flips=odd))
 out={'date':'2026-10-20','status':'PASS','generator_hex':hex(gen),'quadratic_quotient_basis_hex':[hex(w) for w in qb], 'quadratic_coefficient_masks':qmask,'homogeneous_forms_checked':1<<15,'rank_histogram':dict(sorted(Counter(ranks).items())),'minimum_rank_in_eight_translates_histogram':dict(sorted(minhist.items())),'eight_translates_all_bent_count':len(allbent),'rank_patterns':[{ 'ranks':list(k),'count':v} for k,v in sorted(hist.items())],'full_spectrum_and_inverse_normalization_checks':1<<15,'flip_bounds':bounds,'conclusion':'For the fixed parent E, any odd f with all eight Walsh spectra bounded by 10 has distance at least 13 from RM(2,6). This is necessary, not existence or global nonexistence.','cpu_seconds':round(time.process_time()-start,4)}
 Path(__file__).with_name('quadratic_neighborhood_report.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
