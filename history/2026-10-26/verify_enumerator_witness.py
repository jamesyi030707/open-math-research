"""Exact enumerator-relaxation certificate, not a code construction.
Run with Python 3, standard library only. No search or solver is needed.
The residual basis is the previously verified Grassl-derived candidate.
"""
import json
from collections import Counter
from math import comb

BASIS = [int(x, 16) for x in [
    '17e7146801','6293dc808','f714c2017','35dfc802d','b1f3485c',
    '63e6a0ae','65be14f','196fc233','3e690ce6','cb73897']]
# (two residual weights, common A weight, number of h-pairs).
CATEGORIES = [(14,22,14,160),(16,24,16,80),(16,16,16,31),
              (18,18,10,140),(18,18,14,16),(18,18,18,4),
              (20,20,8,8),(20,20,12,6),(20,20,16,64),(20,20,20,2)]

def krawtchouk(n, j, w):
    return sum((-1)**i * comb(w,i) * comb(n-w,j-i)
               for i in range(max(0,j-(n-w)), min(j,w)+1))

def macwilliams(n, size, distribution):
    out = []
    for j in range(n+1):
        numerator = sum(count*krawtchouk(n,j,w) for w,count in distribution.items())
        assert numerator >= 0 and numerator % size == 0, (n,j,numerator)
        out.append(numerator//size)
    assert out[0] == 1 and sum(out) == 2**n//size
    return out

def main():
    words = []
    for u in range(1024):
        w = 0
        for i,row in enumerate(BASIS):
            if u >> i & 1: w ^= row
        words.append(w)
    assert len(set(words)) == 1024
    weights = [w.bit_count() for w in words]
    heavy = [u for u,w in enumerate(weights) if w == 32]
    assert heavy == [1008]
    h = heavy[0]
    assert all((words[h]&row).bit_count()%2 == 0 for row in BASIS)
    pairs = Counter(tuple(sorted((weights[u],weights[u^h])))
                    for u in range(1024) if u < (u^h))
    proposed = Counter({(0,32):1})
    A,D,C = Counter({0:1}),Counter({0:1,32:1}),Counter({0:1,27:1,32:1,59:1})
    for r,s,a,count in CATEGORIES:
        proposed[r,s] += count
        for t in (r,s):
            assert 27-t <= a <= t and a%2 == 0 and (a+t)%4 == 0
        A[a] += count
        for t in (r,s):
            D[a+t] += count
            C[a+t] += count
            C[27-a+t] += count
    assert pairs == proposed
    assert sum(A.values()) == 512 and sum(D.values()) == 1024 and sum(C.values()) == 2048
    assert all(w%4==0 for w in D)
    assert min(w for w in D if w) >= 28 and min(w for w in C if w) == 27
    dualA,dualD,dualC = macwilliams(27,512,A),macwilliams(64,1024,D),macwilliams(64,2048,C)
    # Necessary nested-code nonnegative differences: D subset C subset D-perp,
    # D subset C-perp subset D-perp. These tests also pass formally.
    for j in range(65):
        assert dualD[j] >= dualC[j] >= D.get(j,0)
        assert dualD[j] >= C.get(j,0)
    return {'residual_h_message':h,'residual_pair_counts':{f'{r},{s}':v for (r,s),v in sorted(pairs.items())},
            'categories':CATEGORIES,'A':dict(sorted(A.items())),'D':dict(sorted(D.items())),
            'C':dict(sorted(C.items())),'dual_A':dualA,'dual_D':dualD,'dual_C':dualC,
            'checked_dual_coefficients':158,
            'scope':'Formal integer enumerators satisfy the stated kernel-one pair and ordinary MacWilliams tests. No generator matrix or lift is supplied; realizability is unproved.'}

if __name__ == '__main__':
    print(json.dumps(main(),indent=2))
