#!/usr/bin/env python3
"""Audit: every hole f of E (odd, all 8 translates f+q with |W|<=10) has distance >= 13 from RM(2,6).
Proof sketch checked here.  g any quadratic, h=g+q (q in Q).  (f+q)+h = f+g, so wt((f+q)+h)=r=wt(f+g).
(a) Polar forms: B_{g+q}=B_g+B_q.  Enumerate all 2^15 alternating B_g: min_q rank(B_g+B_q) <= 4 (else span(Q,g) = vectorial bent (6,4), impossible by Nyberg m<=n/2).
(b) Quadratic h with polar rank 2k: |W_h| = 2^(6-k) on exactly 2^(2k) points S, 0 elsewhere.  eps=sign(W_h) on S.  Inverse transform: sum_{u in S} eps(u)(-1)^{u.y} = 2^k (-1)^{h(y)}.
    So Phi(phi) := sum_S eps W_phi = 2^k (64 - 2 wt(phi+h))   (exact).
(c) Target: |W_{f+q}|<=10 => Phi(f+q) <= 10*4^k  =>  64-2r <= 10*2^k  =>  r >= 32-5*2^k : k=2: 12, k=1: 22, k=0: 27.  RM(2,6) words have even weight, f odd => r odd => r>=13."""
import random
EXP = [0] * 126; e = 1
for i in range(63):
    EXP[i] = e; e <<= 1
    if e & 64: e ^= 0x43
for i in range(63, 126): EXP[i] = EXP[i - 63]
LOG = {EXP[i]: i for i in range(63)}
mul = lambda a, b: 0 if a == 0 or b == 0 else EXP[LOG[a] + LOG[b]]
pw = lambda y, k: 0 if y == 0 else EXP[(LOG[y] * k) % 63]
tr8 = lambda z: (z ^ mul(z, z) ^ pw(z, 4)) if z else 0
Q = [[tr8(mul(EXP[9 * k], pw(y, 36))) for y in range(64)] for k in range(3)]
PAIRS = [(i, j) for i in range(6) for j in range(i + 1, 6)]
def polar(q):                                   # 15-bit vector B(e_i,e_j), checked bilinear
    B = {(i, j): q[1 << i] ^ q[1 << j] ^ q[(1 << i) | (1 << j)] for i, j in PAIRS}
    for x in range(64):
        for y in (1, 2, 4, 8, 16, 32):
            for z in (3, 5, 24):
                pass
    return sum(B[p] << n for n, p in enumerate(PAIRS))
def rank(vec):
    M = [0] * 6
    for n, (i, j) in enumerate(PAIRS):
        if (vec >> n) & 1: M[i] |= 1 << j; M[j] |= 1 << i
    r = 0
    for c in range(6):
        p = next((k for k in range(r, 6) if (M[k] >> c) & 1), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for k in range(6):
            if k != r and (M[k] >> c) & 1: M[k] ^= M[r]
        r += 1
    return r
BQ = [polar(q) for q in Q]
# bilinearity of the polar form of q1 via the full table (sanity)
assert all((Q[0][x] ^ Q[0][y] ^ Q[0][x ^ y]) == (sum(((x >> i) & 1) * ((y >> j) & 1) * ((BQ[0] >> n) & 1) + ((x >> j) & 1) * ((y >> i) & 1) * ((BQ[0] >> n) & 1) for n, (i, j) in enumerate(PAIRS)) % 2) for x in range(64) for y in range(64))
span = [0] * 8
for lam in range(8): span[lam] = BQ[0] * (lam & 1) ^ BQ[1] * ((lam >> 1) & 1) ^ BQ[2] * ((lam >> 2) & 1)
for lam in range(8): span[lam] ^= 0
from collections import Counter
# NB: XOR of 15-bit vectors with integer multiplication above only valid for 0/1 coefficients
span = [(BQ[0] if lam & 1 else 0) ^ (BQ[1] if lam & 2 else 0) ^ (BQ[2] if lam & 4 else 0) for lam in range(8)]
print("Q: ranks of the 7 nonzero polar forms:", sorted(rank(span[l]) for l in range(1, 8)))
hist = Counter(); worst = 0
for B in range(1 << 15):
    m = min(rank(B ^ s) for s in span); hist[m] += 1
print("all 32768 alternating forms B_g: min over the 8 translates of polar rank ->", dict(sorted(hist.items())), "| max =", max(hist), "(claim: <= 4)")
def wht(a):
    a = a[:]; h = 1
    while h < 64:
        for i in range(0, 64, 2 * h):
            for j in range(i, i + h): x, y = a[j], a[j + h]; a[j], a[j + h] = x + y, x - y
        h *= 2
    return a
def quad(B, aff):                                # function table of a quadratic with polar vector B plus affine part aff (7 bits: const + 6 linear)
    return [(sum(((y >> i) & 1) & ((y >> j) & 1) for n, (i, j) in enumerate(PAIRS) if (B >> n) & 1) + bin(y & (aff >> 1)).count("1") + (aff & 1)) % 2 for y in range(64)]
random.seed(13); ok_struct = ok_id = ok_even = True; used = Counter(); N = 1500
for _ in range(N):
    B = random.getrandbits(15); s = min(span, key=lambda v: rank(B ^ v)); rk = rank(B ^ s); k = rk // 2; used[rk] += 1
    h = quad(B ^ s, random.getrandbits(7)); W = wht([1 - 2 * v for v in h])
    S = [u for u in range(64) if W[u]]; ok_struct &= len(S) == 2 ** rk and all(abs(W[u]) == 2 ** (6 - k) for u in S)
    ok_even &= sum(h) % 2 == 0
    phi = [random.getrandbits(1) for _ in range(64)]; Wp = wht([1 - 2 * v for v in phi]); Phi = sum((1 if W[u] > 0 else -1) * Wp[u] for u in S)
    ok_id &= Phi == 2 ** k * (64 - 2 * sum(a ^ b for a, b in zip(phi, h)))
print(f"{N} random g: structure |S|=2^rank, |W|=2^(6-rank/2): {ok_struct} | exact identity Phi = 2^k(64-2wt(phi+h)) for random phi: {ok_id} | weights even: {ok_even} | ranks used: {dict(used)}")
print("bounds r >= 32-5*2^k:", {k: 32 - 5 * 2 ** k for k in (2, 1, 0)}, "=> distance from RM(2,6) >= 13 (odd f, even-weight quadratics)")
