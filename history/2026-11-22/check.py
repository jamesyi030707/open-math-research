"""Exact certificate catalog for fixed sections of B, and a 5! local control family."""
from collections import Counter, defaultdict
from itertools import combinations, permutations
from hashlib import sha256
from pathlib import Path
import json
import sys

B = (0x17e7146801, 0x6293dc808, 0xf714c2017, 0x35dfc802d,
     0xb1f3485c, 0x63e6a0ae, 0x65be14f, 0x196fc233,
     0x3e690ce6, 0xcb73897)
def req(ok, what):
    if not ok:
        raise ValueError(what)

def chi(t, v):
    return 1 - 2*((t & v).bit_count() & 1)

def w(t):
    return ((t & 31) << 4) ^ (1008 if t & 32 else 0)

def bw(msg):
    x = 0
    for i, row in enumerate(B):
        if msg >> i & 1:
            x ^= row
    return x.bit_count()

def real_trans(c, t):
    return tuple(sorted(v ^ (t if v & 32 else 0) for v in c))

def weight(t, c):
    return sum((t & v).bit_count() & 1 for v in c)

def catalog(a):
    H = [t for t in range(64) if bw(a ^ w(t)) == 14]
    req(len(H) == 16, 'external section size')
    raw = [sum(chi(t,v) for t in H) for v in range(64)]
    origin = H[0]
    F = [x*chi(origin,v) for v,x in enumerate(raw)]
    k, = [i for i in range(1,32) if F[i] != 0]
    req(F[0] == F[k] == 16, 'low spectrum')
    req(all(F[v] == F[v^k] for v in range(64)), 'quotient')
    req(all(abs(F[v]) == 4 for v in range(32,64)), 'high spectrum')
    reps = [x for x in range(32) if x < (x ^ k)]
    req(len(reps) == 16, 'quotient size')
    req(all(sum(F[32|x]*F[32|(x^d)] for x in reps) == 0 for d in reps[1:]),
        'balanced derivatives')

    def support(vec):
        return sum(1<<c for c in range(64) if vec[c])

    brute = {}
    raw_pair_count = 0
    for u,v in combinations(range(64),2):
        for s in (-1,1):
            vec = [raw[u^c]+s*raw[v^c] for c in range(64)]
            if vec[0] == 0 and any(vec):
                raw_pair_count += 1
                brute.setdefault(support(vec),(u,v,s))

    structural = set()
    for u,v in combinations(reps[1:],2):
        for s in (-1,1):
            mask = support([F[u^c]+s*F[v^c] for c in range(64)])
            structural.add(mask)
    for u,v in combinations((32|x for x in reps),2):
        s = -(F[u]*F[v])//16
        structural.add(support([F[u^c]+s*F[v^c] for c in range(64)]))
    for u in reps[1:]:
        structural.add(support([F[u^c]+F[(u^k)^c] for c in range(64)]))
    req(structural == set(brute) and len(brute) == 345 and raw_pair_count == 1335,
        'complete catalog')

    low = (1<<32)-1
    hist = Counter(((m&low).bit_count(),(m>>32).bit_count()) for m in brute)
    req(hist == {(4,16):210,(16,4):120,(2,32):15}, 'catalog families')
    supports = sorted([c for c in range(64) if mask>>c & 1] for mask in brute)
    digest = sha256(json.dumps(supports,separators=(',',':')).encode()).hexdigest()
    return raw, brute, dict(a=a, H=H, origin=origin, k=k, raw_walsh=raw,
                            raw_pairs=raw_pair_count, sorted_support_digest=digest,
                            mask_counts={str(p):n for p,n in sorted(hist.items())})

def main():
    root = Path(__file__).resolve().parent.parent
    h = Path(sys.argv[1]) if len(sys.argv)>1 else root/'2026-11-15/h.json'
    y = Path(sys.argv[2]) if len(sys.argv)>2 else root/'2026-11-21/result.json'
    src = json.loads(h.read_text())['solutions']
    old_six = [x for x in json.loads(y.read_text())['examined'] if not x['in_old_transport']]
    req(len(src) == 277 and len(old_six) == 6, 'source record counts')
    old = {real_trans(x['columns'],t) for x in src for t in range(32)}
    yesterday = {real_trans(x['columns'],t) for x in old_six for t in range(32)}
    req((len(old),len(yesterday)) == (8408,48) and old.isdisjoint(yesterday), 'prior sets')
    catalogs = [catalog(a) for a in (2,6)]

    controls = {}
    seed = src[1]['columns']
    for perm in permutations(range(5)):
        c = [(v & 32) | sum((v>>i & 1)<<b for i,b in enumerate(perm)) for v in seed]
        controls.setdefault(tuple(sorted(c)),(perm,c))
    req(len(controls) == 60, 'distinct patterns from 120 permutations')
    cases = []
    canonical_orbits = set()
    for key, (perm,c) in sorted(controls.items()):
        for t in range(1,64):
            a,b = weight(t,c),bw(w(t))
            req(a > 0 and 27-b <= a <= b and (a+b)%4 == 0, ('local',perm,t))
        E = [t for t in range(1,32) if weight(t,c)==16]
        req(len(E)==7 and weight(32,c)==4 and c.count(32)==1, 'q24 r4 z1')
        z = c.count(0)+max(Counter(v & 31 for v in c if v & 32).values())
        req(z==2, 'passes multiplicity bound')
        orbit = {real_trans(c,t) for t in range(32)}
        q24 = {p for p in orbit if sum(weight(t,p)==12 for t in range(1,32))==24}
        req(q24 == {key} and len(orbit)==8, 'unique q24 slice in each orbit')
        canonical_orbits.add(min(orbit))

        matches=[]
        for F, masks, desc in catalogs:
            for mask, (u,v,s) in masks.items():
                positions = [j for j,x in enumerate(c) if mask >> x & 1]
                if len(positions)==1:
                    j, = positions
                    vals = [F[u^x]+s*F[v^x] for x in c]
                    req(vals[j]!=0 and not any(vals[:j]+vals[j+1:]) and
                        F[u]+s*F[v]==0, 'full exact certificate replay')
                    matches.append(dict(a=desc['a'],u=u,v=v,s=s,column=j,
                                        label=c[j],coefficient=vals[j]))
                    break
        req(matches,'at least one of the two actual sections has a certificate')
        cases.append(dict(perm=perm,E=E,columns=c,hits=matches,
                          prior=('Nov17' if key in old else
                                 'Nov21' if key in yesterday else None)))
    counts = Counter(x['prior'] for x in cases)
    hits = Counter(y['a'] for x in cases for y in x['hits'])
    req(len(canonical_orbits)==60 and dict(counts)=={None:48,'Nov17':6,'Nov21':6},'scope')
    req(hits=={2:54,6:54},'two section boundaries')
    print(json.dumps(dict(permutations=120, controls=len(cases), distinct_q24_orbits=60,
                          hits_by_section=dict(hits), covered_by_either=60,
                          old_nov17=6, old_nov21=6, outside_named_prior_sets=48,
                          sections=[d for _,_,d in catalogs], cases=cases),separators=(',',':')))

if __name__ == '__main__':
    main()
