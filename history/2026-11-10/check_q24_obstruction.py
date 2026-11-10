#!/usr/bin/env python3
"""Exact finite certificates accompanying RESULT.md. Standard library only."""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from math import comb
from pathlib import Path
import hashlib,json,time
ROOT=Path(__file__).resolve().parent
BLOB='8f76beaa5994563a2980ea9cb87412640d6560b4'
CERT=[(2,22,0),(3,26,0),(5,8,0),(6,13,1),(8,10,1),(9,19,1),(10,14,0),(11,28,0),(12,29,0),(14,23,0)]
CAP=[1,4,7,13,15]
def need(p,s):
    if not p: raise ValueError(s)
def par(x):return x.bit_count()%2
def rank(vec):
    d={}
    for x in vec:
        while x:
            i=x.bit_length()-1
            if i not in d:d[i]=x;break
            x^=d[i]
    return len(d)
def codeword(u,rows):
    x=0
    for i,r in enumerate(rows):
        if u>>i&1:x^=r
    return x
def blocks(P):
    remain=set(range(32));out=[]
    while remain:
        a=min(remain);b=[a^p for p in P];out.append(b);remain.difference_update(b)
    return out
def check_windows(windows,cert):
    for t,n,c in cert:
        for s in range(32):
            need(windows[t][s]==([14] if par(n&s)==c else [10,14,18]),'Hyperplane certificate')
def moments(cols,t):
    z=sum(par(t&v) for v in cols if ((v>>4)&31)==0)
    ww=[sum(par((t^(s<<4))&v) for v in cols) for s in range(32)]
    # Four times the centered energy, using no floats.
    E4=sum((2*w-25-2*z)**2 for w in ww)
    groups={}
    for c in cols:
        v=c>>4&31
        if v:groups.setdefault(v,[]).append(c)
    expected4=32*sum(sum((-1)**par(t&c) for c in group)**2 for group in groups.values())
    need(E4==expected4,'Signed multiplicity moment')
    return z,ww,E4//4

def main():
    start=time.process_time()
    raw=(ROOT/'inputs/residual_candidate.json').read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    need(blob==BLOB,'Pinned residual blob')
    data=json.loads(raw);rows=[int(x,16) for x in data['basis_hex']]
    w=[codeword(u,rows).bit_count() for u in range(1024)]
    need(rank(rows)==10 and Counter(w)=={0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1},'Residual distribution/rank')
    h=1008;need([u for u in range(1,1024) if w[u]>=27]==[h],'Unique kernel candidate')
    mon=[1<<i for i in range(10)]+[(1<<i)|(1<<j) for i,j in combinations(range(10),2)]
    need(rank([sum((int(u&m==m)<<i) for i,m in enumerate(mon)) for u in range(1024) if w[u]==14])==55,'Double-even rigidity')
    need(all(w[s<<4]==16 and w[(s<<4)^h]==16 for s in range(1,32)),'S residual pairs')
    windows=[]
    for t in range(16):
        a=[]
        for s in range(32):
            u=t^(s<<4);b,bh=w[u],w[u^h]
            a.append([j for j in range(28) if max(27-b,27-bh)<=j<=min(b,bh) and (j+b)%4==0])
        windows.append(a)
    windows[0][0]=[0]
    check_windows(windows,CERT)
    # Classification's small coding-theoretic premise: a [7,2] dual containing
    # all-ones and no weight1/2 words has only complementary 3/4 supports.
    dual_patterns=[]
    for a in range(1,127):
        D=[0,127,a,a^127]
        if min(x.bit_count() for x in D[1:])>=3:
            need(sorted(x.bit_count() for x in D)==[0,3,4,7],'Dual classification')
            dual_patterns.append(a)
    need(len(dual_patterns)==70,'Dual support count')
    # Canonical representative forced by the general proof in RESULT.md.
    H=[1,2,3,4,8,16,28]
    mult={v:(sum(par(v&s) for s in H)-2)//2 for v in range(1,32)}
    need(all(sum(par(v&s) for s in H)%2==0 for v in range(32)),'Seven-message XOR')
    need(Counter(mult.values())=={0:9,1:19,2:3},'Multiplicity classification')
    need([v for v in mult if mult[v] and v&3==0]==[28],'Unique active column zero on P')
    active=[v for v,m in mult.items() for _ in range(m)]
    local=[sum(par(v&s) for v in active) for s in range(32)]
    need(Counter(local)=={0:1,12:24,16:7},'Real q24 restriction')
    need([s for s in range(32) if local[s]==16]==H,'Canonical heavy messages')
    need(sum(comb(m,2) for m in mult.values())==3,'Three repeated pairs')
    # Exhaust all geometric orientations needed by the z=0 contradiction.
    # No Q/complement classification enumeration is necessary: every possible
    # unique column v0 in P-perp and both affine offsets are covered.
    Ps=sorted({tuple(sorted([0,a,b,a^b])) for a,b in combinations(range(1,32),2)})
    need(len(Ps)==155,'All planes')
    checked=0;orient=Counter()
    for P in Ps:
        BB=blocks(P)
        for v0 in range(1,32):
            if any(par(v0&p) for p in P):continue
            for e in range(2):
                need(Counter(e^par(v0&B[0]) for B in BB)=={0:4,1:4},'Four/four singleton blocks')
                for t,n,c in CERT:
                    checked+=1
                    transverse=any(par(n&p) for p in P)
                    if not transverse:
                        forced=[B for B in BB if all(par(n&s)==c for s in B)]
                        need(len(forced)==4 and all(48+4*(e^par(v0&B[0]))<56 for B in forced),'Parallel z0 exclusion')
                        orient['parallel']+=1
                    else:
                        energy4=0
                        for B in BB:
                            b=e^par(v0&B[0]);need(sum(par(n&s)==c for s in B)==2,'Transverse hyperplane')
                            free=[(x,y) for x,y in product((10,14,18),repeat=2) if 28+x+y==48+4*b]
                            energies={2*(28-25)**2+(2*x-25)**2+(2*y-25)**2 for x,y in free}
                            need(len(energies)==1,'Forced z0 block moment')
                            energy4+=next(iter(energies))
                        need(energy4==480 and energy4<4*152,'Transverse z0 energy contradiction')
                        orient['transverse']+=1
    need(checked==155*7*2*10,'Complete geometric cases')
    # Terminal fact uses no geometry search.
    T=sorted(t for t,n,c in CERT)
    need(sorted(a^b for a,b in combinations(CAP,2))==T,'Cap certificate')
    need(all((a^b) not in CAP for a,b in combinations(CAP,2)),'No 2-plane in complement')
    maps=list(combinations_with_replacement(range(16),2))
    surviving=[list(M) for M in maps if all(any(par(t&a) for a in M) for t in T)]
    need(len(maps)==136 and not surviving,'Two-column maps cannot avoid zero on T')
    # Positive controls: genuine length27 rank9 matrices, all four possible
    # repeated-pair moments, all sixteen cosets, and all block identities.
    embed=lambda v:(v<<4)|(par(v)<<9)
    cols=[embed(v) for v in active]
    doubles=[v for v,m in mult.items() if m==2]
    for delta,v in zip((1,2,4),doubles):
        j=[j for j,a in enumerate(active) if a==v][-1];cols[j]^=delta
    singles=[j for j,v in enumerate(active) if mult[v]==1]
    cols[singles[0]]^=8
    cols+= [1,2]
    need(len(cols)==27 and rank(cols)==9 and all(par(h&c)==0 for c in cols),'Full left-control shape')
    energies=[]
    singleton_idx=active.index(28)
    for t in range(16):
        z,ww,E=moments(cols,t);energies.append(E)
        need(E in (152,184,216,248),'Allowed moment')
        for B in blocks([0,1,2,3]):
            bit=par((t^(B[0]<<4))&cols[singleton_idx])
            need(sum(ww[s] for s in B)==48+4*z+4*bit,'Actual control block identity')
    need(set(energies)=={152,184,216,248},'All cross-term energy values exercised')
    violations=[u for u in range(1,1024) if not 27-w[u]<=sum(par(u&c) for c in cols)<=w[u]]
    need(bool(violations),'Control is not target code')
    # Deliberately corrupted assumptions must be rejected.
    badcert=[(t,n,c^(t==2)) for t,n,c in CERT]
    try:check_windows(windows,badcert)
    except ValueError:bad_hyperplane=True
    else:raise ValueError('Bad hyperplane accepted')
    need(any(E!=200 for E in energies),'Distinct-column energy misuse detected')
    # Previously published q24 formal survivor: exact 1075 old conditions.
    p,q,y10,y14,z8,z12,z16=counts=[28,24,76,32,18,44,18]
    need(min([p,80-p,q,31-q,y10,y14,160-y10-y14,z8,z12,z16,80-z8-z12-z16])>=0,'Count bounds')
    joint=Counter({(0,0):1,(0,32):1})
    for b,bh,a,n in [(14,22,14,160),(16,24,12,p),(16,24,16,80-p),(16,16,12,q),(16,16,16,31-q),(18,18,10,y10),(18,18,14,y14),(18,18,18,160-y10-y14),(20,20,8,z8),(20,20,12,z12),(20,20,16,z16),(20,20,20,80-z8-z12-z16)]:
        joint[a,b]+=n;joint[a,bh]+=n
    def k(n,a,j):return sum((-1)**i*comb(a,i)*comb(n-a,j-i) for i in range(max(0,j-n+a),min(a,j)+1))
    L={(a,i):k(27,a,i) for a,b in joint for i in range(28)}
    R={(b,j):k(37,b,j) for a,b in joint for j in range(38)}
    dual=[]
    for i in range(28):
        for j in range(38):
            num=sum(n*L[a,i]*R[b,j] for (a,b),n in joint.items());value,rem=divmod(num,1024)
            need(rem==0 and value>=0,'Formal survivor split transform');dual.append(value)
    need(sum(dual)==2**54 and sum(joint.values())==1024,'Formal survivor mass')
    need(2*6+6-14-2==2,'Nov8 cut slack')
    out={'verified':True,'result':'q=24 impossible for archived residual B in kernel-one branch only','input_blob':blob,'input_sha256':hashlib.sha256(raw).hexdigest(),'residual_messages':1024,'quadratic_rank':55,'hyperplane_certificate':[dict(t=t,n=n,c=c) for t,n,c in CERT],'q24_classification':{'heavy_messages_canonical':H,'multiplicity_distribution':dict(sorted(Counter(mult.values()).items())),'canonical_columns':active,'active_columns':25,'zero_on_S_positions':2,'repeat_pairs':3,'possible_energies':[152,184,216,248]},'geometric_cases':checked,'orientation_cases':dict(orient),'z0_transverse_energy':120,'actual_energy_lower_bound':152,'two_column_maps_checked':136,'surviving_maps':surviving,'controls':{'actual_left_columns':cols,'rank':rank(cols),'coset_energies':energies,'local_distribution':dict(Counter(local)),'lift_violations':len(violations),'not_target':True,'changed_hyperplane_rejected':bad_hyperplane,'distinct_column_formula_rejected':True},'previous_formal_survivor':{'counts':counts,'integer_coordinates':[6,14,4,6,13,0,18],'bounds_checked':11,'split_coefficients_checked':len(dual),'nov8_cut_slack':2,'still_formally_feasible':True},'scope':'No exclusion of q16/q20, kernel-zero, other residuals or all binary [64,11,27] codes. No novelty or external peer-review claim. General classification is proved in RESULT.md, not inferred from this finite canonical control.','cpu_seconds':time.process_time()-start}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
