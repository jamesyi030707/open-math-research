#!/usr/bin/env python3
"""Audit of the r=13 exclusion (rank-4 h), the r=15 single-spectrum witness, and a coupling constraint across the 8 translates.
(1) rank-4 quadratic h (with affine part): W_h = +-16 on an AFFINE subspace S=a0+R^perp (|S|=16), 0 elsewhere (checked).  P(x)=(1/64) sum_{a in S} W_phi(a)(-1)^{a.x} is a signed average over 4-point R-cosets => 64P in {-64,-32,0,32,64}.
(2) r=13: aligned sum 152, |W|<=10, W=2 mod 4 => deficit patterns (8) or (4,4); every pattern gives some x with 64P not in {-64,-32,0,32,64} (exhaustive over the 16+120 patterns for 300 random rank-4 h).
(3) witness u = x0x1+x2x3+x4x5 + delta_48 (LSB-first), h = x0x1+x2x3.
(4) coupling: for a quadratic g, (f+q)+(g+q) = f+g, so ALL eight pairs have the same r.  A translate of rank <=2 forces r >= 23; rank 0: r>=27."""
import random
from collections import Counter
from itertools import combinations
def wht(a):
    a = a[:]; h = 1
    while h < 64:
        for i in range(0, 64, 2 * h):
            for j in range(i, i + h): x, y = a[j], a[j + h]; a[j], a[j + h] = x + y, x - y
        h *= 2
    return a
PAIRS = [(i, j) for i in range(6) for j in range(i + 1, 6)]
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
def quad(B, aff):
    return [(sum(((y >> i) & 1) & ((y >> j) & 1) for n, (i, j) in enumerate(PAIRS) if (B >> n) & 1) + bin(y & (aff >> 1)).count("1") + (aff & 1)) % 2 for y in range(64)]
dot = lambda a, x: bin(a & x).count("1") & 1
random.seed(17); ok_aff = ok_P = True; bad_patterns = tot_patterns = 0; nh = 0
while nh < 300:
    B = random.getrandbits(15)
    if rank(B) != 4: continue
    nh += 1; h = quad(B, random.getrandbits(7)); W = wht([1 - 2 * v for v in h]); S = [u for u in range(64) if W[u]]
    eps = {a: (1 if W[a] > 0 else -1) for a in S}
    ok_aff &= len(S) == 16 and all(abs(W[a]) == 16 for a in S) and all((a ^ b ^ c) in S for a in S[:6] for b in S[:6] for c in S[:6])
    phi = [random.getrandbits(1) for _ in range(64)]; Wp = wht([1 - 2 * v for v in phi])
    ok_P &= all(sum(Wp[a] * (-1) ** dot(a, x) for a in S) in (-64, -32, 0, 32, 64) for x in range(64))
    pats = [{a: 8} for a in S] + [{a: 4, b: 4} for a, b in combinations(S, 2)]
    for d in pats:
        tot_patterns += 1
        Wq = {a: eps[a] * (10 - d.get(a, 0)) for a in S}; assert sum(eps[a] * Wq[a] for a in S) == 152
        if any(sum(Wq[a] * (-1) ** dot(a, x) for a in S) not in (-64, -32, 0, 32, 64) for x in range(64)): bad_patterns += 1
print(f"300 random rank-4 h (random affine parts): S affine of size 16 with |W|=16: {ok_aff} | 64P in {{-64,-32,0,32,64}} for random phi: {ok_P}")
print(f"r=13 deficit patterns tested: {tot_patterns}; patterns whose projection leaves the allowed set: {bad_patterns} (all must fail)")
bit = lambda y, i: (y >> i) & 1
h = [(bit(y, 0) & bit(y, 1)) ^ (bit(y, 2) & bit(y, 3)) for y in range(64)]
u = [h[y] ^ (bit(y, 4) & bit(y, 5)) ^ (1 if y == 48 else 0) for y in range(64)]
Wh = wht([1 - 2 * v for v in h]); Wu = wht([1 - 2 * v for v in u]); S = [a for a in range(64) if Wh[a]]
al = sorted((Wu[a] * (1 if Wh[a] > 0 else -1)) for a in S)
print(f"witness: wt(u)={sum(u)}, d(u,h)={sum(a ^ b for a, b in zip(u, h))}, max|W_u|={max(map(abs, Wu))}, aligned values on S: ten 10s={al.count(10)}, six 6s={al.count(6)}, aligned sum={sum(al)} (=256-8*15={256-120}), |S|={len(S)}")
print("   P values (64P) taken by the witness:", sorted({sum(Wu[a] * (-1) ** dot(a, x) for a in S) for x in range(64)}), "| single translate only; not a statement about all 512 coefficients of a fixed E")
# coupling constraint: how many polar classes B_g survive as possible CLOSEST quadratics (no translate of rank <=2)
import itertools
EXP = [0] * 126; e = 1
for i in range(63):
    EXP[i] = e; e <<= 1
    if e & 64: e ^= 0x43
for i in range(63, 126): EXP[i] = EXP[i - 63]
LOG = {EXP[i]: i for i in range(63)}
mul = lambda a, b: 0 if a == 0 or b == 0 else EXP[LOG[a] + LOG[b]]
pw = lambda y, k: 0 if y == 0 else EXP[(LOG[y] * k) % 63]
tr8 = lambda z: (z ^ mul(z, z) ^ pw(z, 4)) if z else 0
Qf = [[tr8(mul(EXP[9 * k], pw(y, 36))) for y in range(64)] for k in range(3)]
BQ = [sum((Qf[k][1 << i] ^ Qf[k][1 << j] ^ Qf[k][(1 << i) | (1 << j)]) << n for n, (i, j) in enumerate(PAIRS)) for k in range(3)]
span = [(BQ[0] if l & 1 else 0) ^ (BQ[1] if l & 2 else 0) ^ (BQ[2] if l & 4 else 0) for l in range(8)]
prof = Counter(); minr = Counter()
for Bg in range(1 << 15):
    rs = [rank(Bg ^ s) for s in span]; minr[min(rs)] += 1; prof[(min(rs), rs.count(4), rs.count(6))] += 1
print("min polar rank over the 8 translates, over all 32768 B_g:", dict(sorted(minr.items())), "| forms with a translate of rank<=2:", minr[0] + minr[2])
print("profile (min rank, #rank-4 translates, #rank-6 translates) counts for min-rank-4 forms:", sorted(((k, v) for k, v in prof.items() if k[0] == 4), key=lambda t: t[0][1]))
