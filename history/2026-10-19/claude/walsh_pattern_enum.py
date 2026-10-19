#!/usr/bin/env python3
"""Count-pattern lemma for an odd f with d(f,E)>=27 (E = RM(1,6) + 3 bent quadratics q1..q3), translates g_q = f+q (8 of them), W_q(u)=sum_y (-1)^{g_q(y)+u.y}.
STANDARD identities (textbook): Parseval sum_u W^2 = 4096; Wiener-Khinchin W(u)^2 = sum_d C(d)(-1)^{u.d}, C(d)=sum_y (-1)^{g(y)+g(y+d)}, C(0)=64, hence sum_u W^4 = 64 sum_d C(d)^2 and sum_d C(d)=W(0)^2.
ELEMENTARY consequences derived here: (i) odd weight => #pairs {y,y+d} with g(y)!=g(y+d) is odd => C(d) = 64-4m, m odd => C(d) = 4 mod 8 (so |C|>=4) for every d!=0.
 (ii) |W|<=10 and W=2 mod 4 (odd weight) => W in {+-2,+-6,+-10}; counts (a,b,c): a+b+c=64, 4a+36b+100c=4096 => b=120-3c, a=2c-56, c in [28,40].
 (iii) sum_u W^4 = 6144c+154624 => sum_{d!=0} C^2 = 96c-1680 = 1008 + 64*sum_k n_k k(k+1)  (n_k = #d with |C|=4+8k) => sum_k n_k k(k+1) = 1.5(c-28) must be an EVEN integer => c in {28,32,36,40}.
 (iv) coset link: each (q,u) with |W|=10,6,2 contributes one word of weight 27,29,31 (and its complement 37,35,33) to f+E, so (b27,b29,b31) = (sum c_q, sum b_q, sum a_q).
Nothing here excludes the code; it only restricts per-translate count patterns."""
import random
from math import comb
# ---- GF(64) point map (as in rm16_membership.py): coordinate i<->alpha^i (6-bit integer), coordinate 63 <-> 0
EXP = [0] * 63; e = 1
for i in range(63):
    EXP[i] = e; e <<= 1
    if e & 64: e ^= 0x43
PT = EXP + [0]
def table(word): F = [0] * 64; [F.__setitem__(PT[i], (word >> i) & 1) for i in range(64)]; return F
def wht(a):
    a = a[:]; h = 1
    while h < 64:
        for i in range(0, 64, 2 * h):
            for j in range(i, i + h): x, y = a[j], a[j + h]; a[j], a[j + h] = x + y, x - y
        h *= 2
    return a
def spec(F):
    s = [1 - 2 * v for v in F]; return wht(s), [sum(s[y] * s[y ^ d] for y in range(64)) for d in range(64)]
random.seed(5); ok = True
for _ in range(300):
    F = [random.getrandbits(1) for _ in range(64)]
    if sum(F) % 2 == 0: F[random.randrange(64)] ^= 1
    W, C = spec(F)
    ok &= sum(w * w for w in W) == 4096 and sum(w ** 4 for w in W) == 64 * sum(c * c for c in C) and all(c % 8 == 4 for c in C[1:]) and sum(C) == W[0] ** 2
print("(computed sanity) 300 random odd functions: Parseval, sum W^4 = 64 sum C^2, sum C = W(0)^2, and C(d)=4 mod 8 (d!=0) all hold:", ok)
pats = [(a, 64 - a - c, c) for c in range(0, 65) for a in range(0, 65 - c) if 4 * a + 36 * (64 - a - c) + 100 * c == 4096]
print("Parseval-only patterns (a=#|W|=2, b=#|W|=6, c=#|W|=10):", [(a, b, c) for a, b, c in pats])
def signed_sums(mags):
    S = {0}
    for m in mags: S = {s + m for s in S} | {s - m for s in S}
    return S
print("autocorrelation refinement (63 values C(d)=4 mod 8, sum C^2 = 96c-1680, sum C = W(0)^2-64):")
kept = []
for a, b, c in pats:
    T = 3 * (c - 28)
    if T % 2 or (T // 2) % 2: print(f"  c={c}: sum n_k k(k+1) = {T/2} not an even integer -> REJECTED"); continue
    T //= 2; feas = {}
    for n1 in range(0, 64):
        for n2 in range(0, 64):
            for n3 in range(0, 64):
                if 2 * n1 + 6 * n2 + 12 * n3 != T or n1 + n2 + n3 > 63: continue
                mags = [4] * (63 - n1 - n2 - n3) + [12] * n1 + [20] * n2 + [28] * n3
                S = signed_sums(mags)
                for w0 in ([2] if a else []) + ([6] if b else []) + ([10] if c else []):
                    if w0 * w0 - 64 in S and w0 not in feas: feas[w0] = (n1, n2, n3)
    print(f"  c={c} (a,b)=({a},{b}): sum n_k k(k+1)={T}; feasible |W(0)| with example (n_|C|=12,20,28):", feas); kept.append((a, b, c))
print("surviving per-translate patterns (a,b,c):", kept)
# planted check: translate q=0 of the odd RM-control witness f = q1 xor delta_coordinate1
f = 0x172e5cb972e5cb97 ^ 1; W, C = spec(table(f))
cnt = {k: sum(1 for w in W if abs(w) == k) for k in (2, 6, 8, 10)}
print("planted f (not a full-E hole): translate q=0 spectrum magnitude counts", cnt, "| |C(d)|=4 for all d!=0:", all(abs(c) == 4 for c in C[1:]), "| sum_{d!=0} C^2 =", sum(c * c for c in C[1:]), "(formula 96*28-1680 = 1008)")
# coset link and the 25 aggregate distributions
import itertools
poly = [1]
for _ in range(8):
    new = [0] * (len(poly) + 3)
    for i, v in enumerate(poly):
        for k in range(4): new[i + k] += v
    poly = new
bad = 0; n = 0
for m in itertools.product(range(4), repeat=8):
    t = sum(m); n += 1
    bad += (sum(28 + 4 * x for x in m), sum(36 - 12 * x for x in m), sum(8 * x for x in m)) != (224 + 4 * t, 288 - 12 * t, 8 * t)
print(f"coset link: {n} patterns m in {{0..3}}^8 (c_q=28+4m, b_q=36-12m, a_q=8m); (b27,b29,b31)=(224+4t,288-12t,8t), t=sum m; violations {bad}; patterns per t=0..24:", poly[:25])
print("aggregate model allowed e.g. c=(29,31,28,...) with the same sum; the mod-4 rule removes such per-translate splits (a genuine refinement).")
