"""Standalone exact independent audit of the fixed-residual q=28 obstruction.

Python standard library only. No external commands, network, or solver. This is
a necessary-condition check, not an enumeration of target generator matrices.
"""
from collections import Counter
from itertools import combinations, product
import json
import time

PIN = "3157b1c81a69ddb061cc21f9aaeaac93eadd9a11"
ROWS = (0x17e7146801,0x6293dc808,0xf714c2017,0x35dfc802d,0xb1f3485c,
        0x63e6a0ae,0x65be14f,0x196fc233,0x3e690ce6,0xcb73897)
H = 1008
COSET_SET = (2,3,5,6,8,9,10,11,12,14)
FIVE = (1,4,7,13,15)
PLANES = ((2,22,0),(3,26,0),(5,8,0),(6,13,1),(8,10,1),
          (9,19,1),(10,14,0),(11,28,0),(12,29,0),(14,23,0))

def require(ok, label):
    if not ok:
        raise ValueError(label)

def parity(x):
    return x.bit_count() % 2

def linear_word(message, rows):
    value = 0
    for i,row in enumerate(rows):
        if (message >> i) & 1:
            value ^= row
    return value

def gf2_rank(rows):
    pivots = {}
    for row in rows:
        while row:
            p = row.bit_length()-1
            if p not in pivots:
                pivots[p] = row
                break
            row ^= pivots[p]
    return len(pivots)

def require_plane(fixed, normal, constant):
    require(set(fixed) == {s for s in range(32) if parity(normal&s)==constant},
            "forced-14 set is not the stated hyperplane")

def require_moments(weights, blocks, z, variance=192):
    require(all(sum(weights[s] for s in block)==48+4*z for block in blocks),
            "four-message block sum failed")
    require(sum((w-12-z)**2 for w in weights)==variance,
            "coset second moment failed")

def rejected(call):
    try:
        call()
    except ValueError:
        return True
    return False

def main():
    started = time.process_time()
    words = [linear_word(u, ROWS) for u in range(1024)]
    W = [w.bit_count() for w in words]
    require(len(set(words))==1024, "residual rank")
    require(dict(Counter(W))=={0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1},
            "residual weight distribution")
    require([u for u in range(1024) if W[u]>=27]==[H], "unique heavy message")
    monomials = [(i,) for i in range(10)] + list(combinations(range(10),2))
    evaluations = [sum(int(all((u>>i)&1 for i in m))<<j for j,m in enumerate(monomials))
                   for u in range(1024) if W[u]==14]
    require(gf2_rank(evaluations)==55, "quadratic evaluation rank")

    # Five-bit labels s denote original messages 16*s; quotient labels t are low bits.
    S = [16*s for s in range(32)]
    require(all(W[s]==W[s^H]==16 for s in S[1:]), "S paired residual weights")
    require(set(S)|{s^H for s in S} ==
            {u for u in range(1024) if u in (0,H) or W[u]==W[u^H]==16},
            "S has precisely the required paired-message preimage")
    windows = []
    for t in range(16):
        windows.append([])
        for s in range(32):
            u=t^(s<<4)
            windows[t].append(tuple(a for a in range(28)
                if 27-W[u]<=a<=W[u] and 27-W[u^H]<=a<=W[u^H]
                and (a+W[u])%4==0 and (a+W[u^H])%4==0))
    for t,n,c in PLANES:
        fixed = {s for s in range(32) if windows[t][s]==(14,)}
        require_plane(fixed,n,c)
        require(len(fixed)==16, "hyperplane size")
        require(all(windows[t][s]==(10,14,18) for s in range(32) if s not in fixed),
                "other half of the coset window")

    kernels=sorted({tuple(sorted((0,a,b,a^b))) for a in range(1,32)
                    for b in range(a+1,32)})
    require(len(kernels)==155, "two-dimensional subspace coverage")
    profile_counts=Counter()
    for K in kernels:
        blocks=[]; unseen=set(range(32))
        while unseen:
            a=min(unseen)
            block=tuple(sorted(a^k for k in K)); blocks.append(block)
            unseen.difference_update(block)
        profile=[]
        for t in range(1,16):
            allowed_z=[]
            for z in range(4):
                possible={0}
                for block in blocks:
                    squares={sum((a-12-z)**2 for a in assignment)
                        for assignment in product(*(windows[t][s] for s in block))
                        if sum(assignment)==48+4*z}
                    possible={a+b for a in possible for b in squares if a+b<=192}
                if 192 in possible:
                    allowed_z.append(z)
            require(allowed_z==([2] if t in COSET_SET else [0,1,2,3]),
                    "unexpected necessary-condition profile")
            profile.append(tuple(allowed_z))
        profile_counts[tuple(profile)]+=1
    pair_sums=sorted(a^b for a,b in combinations(FIVE,2))
    require(pair_sums==list(COSET_SET), "five labels do not give ten distinct forced cosets")
    compatible=0
    for columns in product(range(16),repeat=3):
        if all(sum(parity(t&v) for v in columns)==2 for t in COSET_SET):
            compatible+=1
    require(compatible==0, "linear three-coordinate map unexpectedly feasible")

    # Actual q=28 restricted code: columns F2^5 minus span(e0,e1,e2), plus three zero.
    active=tuple(range(8,32))
    restricted=[sum(parity(s&v) for v in active) for s in range(32)]
    require(dict(Counter(restricted))=={0:1,12:28,16:3}, "genuine q28 restriction control")
    K=(0,8,16,24)
    blocks=[tuple(a^k for k in K) for a in range(8)]
    controls=0
    # Eight specified sign assignments, each with each possible zero-column weight.
    # These are controls, not an enumeration of the 2^24 sign assignments.
    signs=(0,1,(1<<24)-1,0xAAAAAA,0x555555,0x123456,0xABCDEF,0x010101)
    last_weights=None
    for pattern in signs:
        for z in range(4):
            weights=[z+sum(((pattern>>j)&1)^parity(s&v) for j,v in enumerate(active))
                     for s in range(32)]
            require_moments(weights,blocks,z)
            controls+=1
            last_weights=weights
    four=(0,3,5,6)
    require(all((a^b).bit_count()==2 for a,b in combinations(four,2)),
            "four-vector terminal positive control")
    # Explicit corruptions ensure the relevant verification gates reject bad inputs.
    fixed={s for s in range(32) if windows[2][s]==(14,)}
    corrupt_fixed=fixed^{0}
    require(rejected(lambda:require_plane(corrupt_fixed,22,0)), "corrupt plane accepted")
    require(rejected(lambda:require_moments(last_weights,blocks,3,191)),
            "corrupt second moment accepted")
    require(rejected(lambda:require(sorted(a^b for a,b in combinations((1,4,7,13,13),2))
                                   ==list(COSET_SET), "corrupt terminal labels")),
            "corrupt terminal labels accepted")
    result={
        "status":"passed", "commit":PIN,
        "residual_blob":"8f76beaa5994563a2980ea9cb87412640d6560b4",
        "residual_rank":10,"messages":1024,"quadratic_evaluation_rank":55,
        "hyperplanes":[{"t":t,"normal":n,"constant":c} for t,n,c in PLANES],
        "two_dimensional_subspaces":155,"nonzero_quotient_cosets":15,
        "zero_coordinate_weight_choices":4,"linear_maps_checked":4096,
        "compatible_linear_maps":0,"positive_coset_controls":controls,
        "corruption_tests":3,"cpu_seconds":time.process_time()-started,
        "scope":"Only q=28 for this fixed residual and normalized even-subcode kernel-one branch. No exclusion of q=16,20,24, kernel-zero, other residuals, or all [64,11,27] codes."
    }
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
