"""Twelve fixed q24 controls: singletons, congruence, and exact projection gaps."""
import json
from collections import Counter
from itertools import combinations
from math import gcd
from pathlib import Path
from sys import argv

B = (0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,
     0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
INDICES = (1,19,115,139,163,259)
def req(ok, text):
    if not ok:
        raise ValueError(text)

def bw(m):
    x=0
    for i,row in enumerate(B):
        if m>>i&1:
            x^=row
    return x.bit_count()

def W(t):
    return ((t&31)<<4)^(1008 if t&32 else 0)

def parity(v):
    return v.bit_count()&1

def weight(t,c):
    return sum(parity(t&v) for v in c)

def orbit(c):
    return {tuple(sorted(v^(t if v&32 else 0) for v in c)) for t in range(32)}

def exact_full(c,H):
    y=[sum(parity(t&v)<<j for j,v in enumerate(c)) for t in H]
    left_rows=[v&8191 for v in y]
    right_rows=[v>>13 for v in y]
    def encode(x,rows):
        return sum((x^v).bit_count()<<(5*i) for i,v in enumerate(rows))
    left=Counter(encode(x,left_rows) for x in range(1<<13))
    target=sum(14<<(5*i) for i in range(len(H)))
    return sum(left[target-encode(x,right_rows)] for x in range(1<<14))

def pair_pass(rows,u,v,rhs):
    # Scale by four. The packed y-component cannot offset a nonzero x-difference.
    p=512
    steps=[abs(u0*p+v0) for u0,v0 in zip(rows[u],rows[v])]
    target=p*rhs[u]+rhs[v]+sum(steps)
    bits=1
    for step in steps:
        bits|=bits<<(2*step)
    return target>=0 and (bits>>target)&1==1

def main():
    base=Path(__file__).resolve().parent.parent
    src=Path(argv[1]) if len(argv)>1 else base/'2026-11-15/h.json'
    prev=Path(argv[2]) if len(argv)>2 else base/'2026-11-22/result.json'
    data=json.loads(src.read_text())['solutions']
    cases22=json.loads(prev.read_text())['cases']
    old=set().union(*(orbit(x['columns']) for x in data))
    old22=set().union(*(orbit(x['columns']) for x in cases22))
    req((len(data),len(old),len(old22))==(277,8408,480),'prior set sizes')
    H={a:[t for t in range(64) if bw(a^W(t))==14] for a in range(1,16)}
    H={a:h for a,h in H.items() if h}
    req(len(H)==10 and all(len(h)==16 for h in H.values()),'actual minimum sections')
    F={a:[sum(1-2*parity(t&u) for t in h) for u in range(64)] for a,h in H.items()}
    out=[]
    for i in INDICES:
        shape=[data[i]['r'],data[i]['z']]
        req(all([x['r'],x['z']]!=shape for x in data[:i]),'first representative')
        for sw in (False,True):
            c=[v^5 if sw and parity(v&5) else v for v in data[i]['columns']]
            for t in range(1,64):
                a0,b0=weight(t,c),bw(W(t))
                req(a0>0 and 27-b0<=a0<=b0 and (a0+b0)%4==0,'genuine local weights')
            req(sum(weight(t,c)==12 for t in range(1,32))==24,'q24')
            req([weight(32,c),c.count(32)]==shape,'shape')
            req(c.count(0)+max(Counter(v&31 for v in c if v&32).values())==2,
                'passes prior multiplicity')
            key=tuple(sorted(c))
            hits={}
            for a,f in F.items():
                rows=[[f[u^x] for x in c] for u in range(64)]
                n_single=0
                n_congruence=0
                n_zero=0
                for u,v in combinations(range(64),2):
                    for s in (-1,1):
                        vals=[x+s*y for x,y in zip(rows[u],rows[v])]
                        t=-f[u]-s*f[v]
                        g=gcd(*vals)
                        n_zero+=g==0 and t!=0
                        n_single+=t==0 and sum(x!=0 for x in vals)==1
                        n_congruence+=g!=0 and (t-sum(vals))%(2*g)!=0
                hits[a]=[n_single,n_congruence,n_zero]
            rec=dict(index=i,swap_0_2=sw,shape=shape,columns=c,
                     prior_8408=key in old,prior_nov22_orbits=key in old22,hits=hits)
            if i not in (1,259):
                rec['exact_full_counts']={}
                rec['pair_pass_counts']={}
                for a in (2,3):
                    f=F[a]
                    req(all(x%4==0 for x in f),'scale')
                    rows=[[f[u^x]//4 for x in c] for u in range(64)]
                    rhs=[-x//4 for x in f]
                    rec['pair_pass_counts'][a]=sum(pair_pass(rows,u,v,rhs) for u,v in combinations(range(64),2))
                    rec['exact_full_counts'][a]=exact_full(c,H[a])
                req(rec['pair_pass_counts']=={2:2016,3:2016} and rec['exact_full_counts'][2]>0
                    and rec['exact_full_counts'][3]==0,'projection gap')
                req(not any(v for triple in hits.values() for v in triple),'no arithmetic hit')
            else:
                req(sum(t[0] for t in hits.values())==(88 if sw else 84) and
                    sum(t[1] for t in hits.values())==576,'arithmetic hits')
            if i==259 and sw:
                f=F[2]
                vals=[f[33^x]-f[38^x] for x in c]
                req(f[33]==f[38] and vals==[16*(j==14) for j in range(27)],'new singleton')
                gcd_vals=[f[32^x]-f[47^x] for x in c]
                req([(j,x) for j,x in enumerate(gcd_vals) if x]==
                    [(8,-16),(11,16),(18,-16),(25,16),(26,16)] and f[32]==f[47],
                    'explicit larger congruence')
                req(not orbit(c)&(old|old22),'outside named coverage')
                rec['witness']=dict(a=2,u=33,v=38,s=-1,column=14,coefficient=16,target=0)
            if sw and i!=1:
                images=orbit(c)
                req(len(images)==32 and not images&(old|old22),'five new orbits')
                rec['own_q24_orbit_size']=sum(sum(weight(t,k)==12 for t in range(1,32))==24 for k in images)
            out.append(rec)
    req([x['own_q24_orbit_size'] for x in out if 'own_q24_orbit_size' in x]
        ==[8,1,20,1,3], 'q24 sizes')
    req(len({tuple(sorted(x['columns'])) for x in out})==12,'distinct controls')
    print(json.dumps(dict(actual_minimum_sections=H, pair_combinations_per_a=4032,
                          hit_columns=['singleton','gcd_congruence','zero_vector_nonzero_target'],
                          controls=out),separators=(',',':')))

if __name__=='__main__':
    main()
