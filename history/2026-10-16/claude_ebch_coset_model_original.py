#!/usr/bin/env python3
"""Extended BCH(63,27) parent E = [64,10,28] and the exact NECESSARY model for an odd coset r+E with min weight >= 27 (so E+<r> would be a [64,11,>=27] code).
Standard library only.  Conventions: GF(64)=F2[x]/(x^6+x+1), alpha=x.  Zeros of the cyclic code: all cosets (mod 63, x->2x) meeting {1..26}  (narrow-sense, designed distance 27).
g(x)=product of their minimal polynomials; h=(x^63+1)/g.  Bit k of an integer = coefficient of x^k = coordinate k+1.  Generator matrix rows x^i g(x), i=0..9 (63 bits) plus
coordinate 64 (bit 63) = parity of the row.  Message bit i selects row i.
Coset identity (derived): for r+E with weight counts b_i:  sum_i b_i K_j(i) = 1024 * sum_{h in E^perp, wt h=j} (-1)^{<h,r>}   =: 1024 t_j,  |t_j|<=A^perp_j,  t_j = A^perp_j (mod 2), K_j exact Krawtchouk (n=64).
If all-ones in E: coset closed under complement (b_i=b_{64-i}), E^perp even, A^perp_odd=0; r odd => odd weights only, so (27..37 odd): b27=b37,b29=b35,b31=b33, b27+b29+b31=512."""
import math, random, time
from fractions import Fraction
from collections import Counter
from itertools import combinations
T0 = time.process_time()
EXP = [0] * 126; e = 1
for i in range(63):
    EXP[i] = e; e <<= 1
    if e & 64: e ^= 0x43
assert e == 1 and len(set(EXP[:63])) == 63
for i in range(63, 126): EXP[i] = EXP[i - 63]
LOG = {EXP[i]: i for i in range(63)}
mul = lambda a, b: 0 if a == 0 or b == 0 else EXP[LOG[a] + LOG[b]]
def minpoly(C):
    p = [1]
    for c in C:
        r = EXP[c % 63]; q = [0] * (len(p) + 1)
        for i, co in enumerate(p): q[i + 1] ^= co; q[i] ^= mul(co, r)
        p = q
    assert all(x in (0, 1) for x in p); return sum(b << i for i, b in enumerate(p))
def pmul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        a <<= 1; b >>= 1
    return r
def pdiv(a, b):
    q = 0
    while a.bit_length() >= b.bit_length():
        s = a.bit_length() - b.bit_length(); q |= 1 << s; a ^= b << s
    assert a == 0; return q
cos = []; seen = set()
for s in range(63):
    if s in seen: continue
    C = []; x = s
    while x not in C: C.append(x); x = 2 * x % 63
    seen |= set(C); cos.append(sorted(C))
zero = [C for C in cos if any(1 <= c <= 26 for c in C)]; nonz = [C for C in cos if C not in zero]
g = 1
for C in zero: g = pmul(g, minpoly(C))
h = pdiv((1 << 63) | 1, g)
print("zero cosets sizes", [len(C) for C in zero], "| nonzero cosets", nonz, "| deg g =", g.bit_length() - 1, "deg h =", h.bit_length() - 1)
print(f"g(x) = 0x{g:x}   h(x)=(x^63+1)/g = 0x{h:x}   (bit k = coeff of x^k)")
rows = []
for i in range(10):
    r63 = g << i; rows.append(r63 | ((bin(r63).count("1") & 1) << 63))
cw = [0] * 1024
for m in range(1, 1024):
    low = m & -m; cw[m] = cw[m ^ low] ^ rows[low.bit_length() - 1]
assert len(set(cw)) == 1024
basis = {}
for r in rows:
    x = r
    while x:
        p = x.bit_length() - 1
        if p in basis: x ^= basis[p]
        else: basis[p] = x; break
print("GF(2) rank of the 10x64 generator matrix:", len(basis), "| generator rows (hex):", [format(r, "016x") for r in rows])
wt = Counter(w.bit_count() for w in cw); A = [wt.get(i, 0) for i in range(65)]
print("extended weight enumerator A_i:", {i: A[i] for i in range(65) if A[i]}, "| min distance", min(i for i in range(1, 65) if A[i]))
w63 = Counter((w & ((1 << 63) - 1)).bit_count() for w in cw); print("unextended [63,10] weight enumerator:", dict(sorted(w63.items())))
ONES = (1 << 64) - 1; print("all-ones vector in E:", ONES in set(cw), "| all weights even:", all(i % 2 == 0 for i in range(65) if A[i]))
K = [[sum((-1) ** s * math.comb(i, s) * math.comb(64 - i, j - s) for s in range(min(i, j) + 1)) for i in range(65)] for j in range(65)]
Ad = []
for j in range(65):
    t = sum(A[i] * K[j][i] for i in range(65)); assert t % 1024 == 0 and t >= 0; Ad.append(t // 1024)
print("dual enumerator A^perp_j (j even, nonzero):", {j: Ad[j] for j in range(0, 65, 2) if Ad[j]}, "| odd j all zero:", all(Ad[j] == 0 for j in range(1, 65, 2)), "| sum =", sum(Ad), "= 2^54:", sum(Ad) == 2 ** 54)
# --- sanity of the derived necessary conditions on REAL odd cosets (random, not near-feasible)
random.seed(7); ok = 0; mins = []
for _ in range(30):
    r = random.getrandbits(64)
    if r.bit_count() % 2 == 0: r ^= 1
    b = Counter((r ^ w).bit_count() for w in cw); mins.append(min(b))
    good = all((lambda T: T % 1024 == 0 and abs(T) <= 1024 * Ad[j] and (T // 1024 - Ad[j]) % 2 == 0)(sum(b[i] * K[j][i] for i in b)) for j in range(65))
    ok += good
print(f"sanity: {ok}/30 random odd cosets satisfy all integer Krawtchouk/congruence constraints; their min weights lie in [{min(mins)},{max(mins)}]")
# --- necessary model: unknowns x=b27, y=b29, z=b31=512-x-y ; constraints for even j (odd j trivial, j=64 automatic)
cons = []
for j in range(2, 64, 2):
    Ua = K[j][27] + K[j][37]; Ub = K[j][29] + K[j][35]; Uc = K[j][31] + K[j][33]
    a, b = Ua - Uc, Ub - Uc; U = 1024 * Ad[j]
    cons.append((a, b, U - 512 * Uc, f"T_{j} <= 1024*A^perp_{j}")); cons.append((-a, -b, U + 512 * Uc, f"-T_{j} <= 1024*A^perp_{j}"))
cons += [(-1, 0, 0, "x>=0"), (0, -1, 0, "y>=0"), (1, 1, 512, "z>=0 (x+y<=512)")]
print("real relaxation: variables (x,y), z=512-x-y; constraints:", len(cons))
verts = set()
for (a1, b1, c1, _), (a2, b2, c2, _) in combinations(cons, 2):
    det = a1 * b2 - a2 * b1
    if det == 0: continue
    x = Fraction(c1 * b2 - c2 * b1, det); y = Fraction(a1 * c2 - a2 * c1, det)
    if all(a * x + b * y <= c for a, b, c, _ in cons): verts.add((x, y))
if verts:
    print("REAL RELAXATION FEASIBLE; polygon vertices (x,y,z):", sorted((str(x), str(y), str(512 - x - y)) for x, y in verts)[:8])
    pts = [(x, y) for x in range(513) for y in range(513 - x) if all(abs(T) <= 1024 * Ad[j] and T % 1024 == 0 and (T // 1024 - Ad[j]) % 2 == 0
           for j in range(2, 64, 2) for T in [512 * (K[j][31] + K[j][33]) + x * (K[j][27] + K[j][37] - K[j][31] - K[j][33]) + y * (K[j][29] + K[j][35] - K[j][31] - K[j][33])])]
    print("integer/congruence model: feasible integer points (b27,b29,b31):", len(pts), pts[:5])
else:
    best = None
    for i1, i2, i3 in combinations(range(len(cons)), 3):
        A_ = [cons[i][0] for i in (i1, i2, i3)]; B_ = [cons[i][1] for i in (i1, i2, i3)]; C_ = [cons[i][2] for i in (i1, i2, i3)]
        lam = [A_[1] * B_[2] - A_[2] * B_[1], A_[2] * B_[0] - A_[0] * B_[2], A_[0] * B_[1] - A_[1] * B_[0]]
        if all(l == 0 for l in lam): continue
        if any(l < 0 for l in lam) and any(l > 0 for l in lam): continue
        if any(l < 0 for l in lam): lam = [-l for l in lam]
        gg = math.gcd(*lam); lam = [l // gg for l in lam]
        if sum(l * c for l, c in zip(lam, C_)) < 0:
            key = (sum(1 for l in lam if l), sum(lam))
            if best is None or key < best[0]: best = (key, (i1, i2, i3), lam)
    (_, idx, lam) = best
    print("REAL RELAXATION INFEASIBLE (hence the integer/congruence model, a subset, is infeasible). Rational Farkas witness (lambda>=0):")
    for l, i in zip(lam, idx):
        if l: print(f"   lambda={l}  *  [{cons[i][3]}]   (a,b,c)=({cons[i][0]},{cons[i][1]},{cons[i][2]})")
    sa = sum(l * cons[i][0] for l, i in zip(lam, idx)); sb = sum(l * cons[i][1] for l, i in zip(lam, idx)); sc = sum(l * cons[i][2] for l, i in zip(lam, idx))
    print("   exact check: sum lambda*a =", sa, "; sum lambda*b =", sb, "; sum lambda*c =", sc, "< 0 :", sa == 0 and sb == 0 and sc < 0)
print(f"process time {time.process_time()-T0:.1f}s")
