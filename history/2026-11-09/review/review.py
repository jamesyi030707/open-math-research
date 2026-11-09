#!/usr/bin/env python3
"""Independent necessary-condition audit; no candidate-matrix search."""
from pathlib import Path
from itertools import combinations, combinations_with_replacement, product
from collections import Counter
import hashlib,json,time
start=time.process_time()
P=Path(__file__).resolve().parent.parent/'inputs/residual_candidate.json'
raw=P.read_bytes()
blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
def req(x,msg):
    if not x: raise ValueError(msg)
def bit(x,y):return (x&y).bit_count()%2
def rank(vecs):
    a=list(vecs);r=0
    for j in reversed(range(max(a,default=0).bit_length())):
        p=next((i for i in range(r,len(a)) if a[i]>>j&1),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r]
        for i in range(len(a)):
            if i!=r and a[i]>>j&1:a[i]^=a[r]
        r+=1
    return r
req(blob=='8f76beaa5994563a2980ea9cb87412640d6560b4','Pinned blob')
R=[int(x,16) for x in json.loads(raw)['basis_hex']]
words=[]
for m in range(1024):
    acc=0
    for i in range(10):
        if m>>i&1:acc^=R[i]
    words.append(acc)
w=[x.bit_count() for x in words]
req(rank(R)==10,'B rank')
req(Counter(w)=={0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1},'Weight spectrum')
req([m for m in range(1,1024) if w[m]>=27]==[1008],'Heavy message')
mons=[(i,) for i in range(10)]+list(combinations(range(10),2))
evalrows=[]
for m in range(1024):
    if w[m]!=14:continue
    ev=0
    for j,I in enumerate(mons):
        if all(m>>i&1 for i in I):ev|=1<<j
    evalrows.append(ev)
req(rank(evalrows)==55,'Quadratic rigidity')
h=1008; S=[s*16 for s in range(32)]
req(rank(S)==5 and rank(S+[h])==6,'S plus h')
req({min(m,m^h) for m in range(1024) if w[m]==w[m^h]==16}==set(S[1:]),'Pair category')
req({t^(s<<4)^(a*h) for t in range(16) for s in range(32) for a in range(2)}==set(range(1024)),'Quotient basis')
# Enumerate ALL 3-element heavy sets and derive their restrictions by Fourier
# inversion, independently checking the q=28 classification without assuming K.
valid_H=[]
for H in combinations(range(1,32),3):
    nums=[12-4*sum(1-2*bit(v,s) for s in H) for v in range(1,32)]
    if all(x>=0 and x%16==0 for x in nums):
        req(H[0]^H[1]^H[2]==0,'Heavy set closure')
        valid_H.append(H)
req(len(valid_H)==155,'155 subspaces')
Ks=[(0,)+H for H in valid_H]
# Exact necessary windows, not applying the nonzero-word inequality at zero.
windows={}
for t in range(1,16):
    windows[t]=[]
    for s in range(32):
        u=t^(s<<4)
        windows[t].append(tuple(a for a in range(28)
                               if all(27-w[v]<=a<=w[v] and (a+w[v])%4==0 for v in (u,u^h))))
expected_T={2,3,5,6,8,9,10,11,12,14}
T={t for t in range(1,16) if set(windows[t])=={(14,),(10,14,18)}}
req(T==expected_T,'Ten quotient messages')
# Independently identify each broad location set as affine hyperplane.
hyperplanes={}
for t in sorted(T):
    broad={s for s in range(32) if windows[t][s]==(10,14,18)}
    matches=[(v,b) for v in range(1,32) for b in range(2) if broad=={s for s in range(32) if bit(v,s)==b}]
    req(len(matches)==1,'Broad affine hyperplane')
    hyperplanes[t]=matches[0]
blocks_hist=Counter(); moments_hist=Counter(); checks=0
for K in Ks:
    annihilator={v for v in range(32) if all(bit(v,k)==0 for k in K)}
    req(len(annihilator)==8,'Annihilator size')
    active=set(range(32))-annihilator
    req(len(active)==24 and 0 not in active,'Active restrictions')
    for s in range(32):
        localw=sum(bit(v,s) for v in active)
        req(localw==(0 if s==0 else 16 if s in K else 12),'Local q28 control')
    blocks=sorted({tuple(sorted(s^k for k in K)) for s in range(32)})
    req(len(blocks)==8,'Eight K cosets')
    for t in sorted(T):
        typ=tuple(sorted(sum(len(windows[t][s])==3 for s in block) for block in blocks))
        req(typ in [(0,0,0,0,4,4,4,4),(2,2,2,2,2,2,2,2)],'Hyperplane blocks')
        blocks_hist[typ]+=1
        allowed=[]
        for z in range(4):
            moments={0}
            for block in blocks:
                mset=set()
                for ws in product(*(windows[t][s] for s in block)):
                    if sum(ws)==48+4*z:
                        mset.add(sum((a-12-z)**2 for a in ws))
                moments={m+n for m in moments for n in mset}
            moments_hist[(typ,z,tuple(sorted(moments)))]+=1
            if 192 in moments:allowed.append(z)
            if typ==(2,2,2,2,2,2,2,2) and z!=2:
                req(moments=={128 if z==0 else 96},'Corrected rejected moments')
        req(allowed==[2],'Forced z=2')
        checks+=1
# Analytic contradiction: parity vanishes on 10>8 inputs, hence rank <=2;
# kernel is >=2D but complement of T has no two-dimensional subspace.
Z=set(range(16))-T
req(Z=={0,1,4,7,13,15},'Zero set')
req(all(a^b in T for a,b in combinations(Z-{0},2)),'No 2D kernel')
req(all(sum(bit(v,t)==0 for t in range(16))==8 for v in range(1,16)),'Parity hyperplanes')
patterns=list(combinations_with_replacement(range(16),3))
req(len(patterns)==816,'Three-column multisets')
req(not any(all(sum(bit(v,t) for v in pat)==2 for t in T) for pat in patterns),'Brute linear map control')
# Verify moment identity directly for one arbitrary quotient lift per K.
for K in Ks:
    active=[v for v in range(32) if any(bit(v,k) for k in K)]
    cols=[(v,(3*v+1)%16) for v in active]+[(0,1),(0,3),(0,14)]
    for t in range(16):
        z=sum(bit(a,t) for v,a in cols if v==0)
        weights=[sum(bit(v,s)^bit(a,t) for v,a in cols) for s in range(32)]
        req(sum((a-12-z)**2 for a in weights)==192,'Direct character moment control')
result={
 'status':'PASS', 'residual_blob_sha':blob, 'B_rank':10,
 'quadratic_evaluation_rank':55, 'unique_heavy_message':1008,
 'q28_three_heavy_sets_tested':4495,'valid_two_dimensional_K':len(Ks),
 'quotient_T':sorted(T),'complement_Z':sorted(Z),
 'broad_affine_hyperplanes':hyperplanes,
 'K_message_cases':checks,
 'block_types':{str(k):v for k,v in blocks_hist.items()},
 'mixed_block_rejected_moments':{'z0':128,'z1':96,'z3':96},
 'required_centered_second_moment':192,
 'three_column_multisets':len(patterns),'survivors':0,
 'scope':'No q=28 target lift for this fixed B with left projection kernel one and normalized doubly-even even subcode. Not whole branch/global nonexistence.',
 'cpu_seconds':time.process_time()-start
}
print(json.dumps(result,indent=2))
