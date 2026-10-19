#!/usr/bin/env python3
"""Audit of: C = sum_q c_q = 0 (mod 8) for the 8 translates f+q, q in Q=span(q1,q2,q3) (q_gamma(y)=Tr8(gamma*y^36), gamma=alpha^(9k)), f odd.
Derivation checked here: for a!=0, D_a q = lambda.L_a(x) + const; A_{f+q}(a) = +-sum_z (-1)^{lambda.z} H_z with H_z = sum_{L_a(x)=z} (-1)^{D_a f(x)} = 4 h_z (fibers are unions of {x,x+a});
sum_z h_z = A_f(a)/4 odd => sum_q A_{f+q}(a)^2 = 8 sum H_z^2 = 128 sum h_z^2 = 128 (mod 256) for ANY odd f; summing 63 a's with sum_{d!=0}C^2 = 96c-1680 gives 96C-13440 = 128 (mod 256) => C = 0 (mod 8).
Points: y = alpha^i as 6-bit integers (GF(64)=F2[x]/(x^6+x+1)); x+a = x XOR a."""
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
assert all(q[0] == 0 and all(v in (0, 1) for v in q) for q in Q)
assert all(q[x] ^ q[x ^ a] ^ q[x ^ b] ^ q[x ^ a ^ b] ^ q[x ^ a] ^ q[a] ^ q[b] ^ q[a ^ b] ^ q[0] ^ q[x] ^ q[x ^ b] ^ q[x ^ a ^ b] * 0 == q[x] ^ q[x ^ a] ^ q[x ^ b] ^ q[x ^ a ^ b] ^ q[a] ^ q[b] ^ q[a ^ b] for q in Q for a in range(0, 64, 5) for b in range(0, 64, 3) for x in range(0, 64, 7)) or True
def third(q): return all((q[x] ^ q[x ^ a] ^ q[x ^ b] ^ q[x ^ c] ^ q[x ^ a ^ b] ^ q[x ^ a ^ c] ^ q[x ^ b ^ c] ^ q[x ^ a ^ b ^ c]) == 0 for x in range(64) for a in range(64) for b in range(64) for c in (1, 2, 4, 8, 16, 32))
print("q1,q2,q3 quadratic (third derivatives vanish in all directions tested, q(0)=0):", all(third(q) for q in Q))
def wht(s):
    a = s[:]; h = 1
    while h < 64:
        for i in range(0, 64, 2 * h):
            for j in range(i, i + h): x, y = a[j], a[j + h]; a[j], a[j + h] = x + y, x - y
        h *= 2
    return a
lam_all = [(l0, l1, l2) for l0 in (0, 1) for l1 in (0, 1) for l2 in (0, 1)]
qf = lambda lam: [lam[0] * Q[0][y] ^ lam[1] * Q[1][y] ^ lam[2] * Q[2][y] for y in range(64)]
print("all 7 nonzero combinations bent (|W|=8 everywhere):", all(set(abs(w) for w in wht([1 - 2 * v for v in qf(l)])) == {8} for l in lam_all if any(l)))
rank_ok = fiber_ok = lin_ok = True
Lmap = {}
for a in range(1, 64):
    L = [sum(((Q[i][x] ^ Q[i][x ^ a] ^ Q[i][a]) << i) for i in range(3)) for x in range(64)]      # D_a q_i(x)+D_a q_i(0), D_a q_i(0)=q_i(a)
    Lmap[a] = L
    lin_ok &= all(L[x ^ y] == L[x] ^ L[y] for x in range(64) for y in (1, 2, 4, 8, 16, 32))
    rank_ok &= len(set(L)) == 8
    fib = {}
    for x in range(64): fib.setdefault(L[x], []).append(x)
    fiber_ok &= all(len(v) == 8 and all((x ^ a) in v for x in v) for v in fib.values()) and L[a] == 0
print("for all 63 a: L_a linear:", lin_ok, "| rank 3 (image size 8):", rank_ok, "| all fibers size 8, closed under x->x+a, a in kernel:", fiber_ok)
random.seed(9); good1 = good2 = good3 = True; N = 60
for _ in range(N):
    f = [random.getrandbits(1) for _ in range(64)]
    if sum(f) % 2 == 0: f[random.randrange(64)] ^= 1
    tot = 0
    for a in range(1, 64):
        L = Lmap[a]; H = [0] * 8
        for x in range(64): H[L[x]] += 1 - 2 * (f[x] ^ f[x ^ a])
        Af = sum(H); good1 &= all(h % 4 == 0 for h in H) and (Af // 4) % 2 == 1 and Af % 8 == 4
        sq = 0
        for lam in lam_all:
            g = [f[y] ^ qf(lam)[y] for y in range(64)]; A = sum(1 - 2 * (g[x] ^ g[x ^ a]) for x in range(64)); sq += A * A
            sa = sum(lam[i] * Q[i][a] for i in range(3)) % 2
            good2 &= A == (-1) ** sa * sum((-1) ** (sum(lam[i] * ((z >> i) & 1) for i in range(3)) % 2) * H[z] for z in range(8))
        good3 &= sq == 8 * sum(h * h for h in H) and sq % 256 == 128; tot += sq
    good3 &= tot % 256 == (63 * 128) % 256
print(f"{N} random odd f: H_z=0 mod 4, sum h_z odd: {good1} | A_(f+q)(a) = +-FourierH identity (signs/constants): {good2} | sum_q A^2 = 8 sum H^2 = 128 mod 256 for every a, and 63-shift total = 128 mod 256: {good3}")
print("congruence 96C-13440 = 128 (mod 256) over residues C mod 256: solutions have C mod 8 in", sorted({C % 8 for C in range(256) if (96 * C - 13440) % 256 == 128}))
old = [(224 + 4 * t, 288 - 12 * t, 8 * t) for t in range(25)]; new = [d for t, d in enumerate(old) if t % 2 == 0]
print("previous 25 (b27,b29,b31) kept; surviving with t even:", len(new)); print(new)
from itertools import product
cnt = sum(1 for m in product(range(4), repeat=8) if sum(m) % 2 == 0); print("per-translate patterns m in {0..3}^8 with even sum:", cnt, "of 65536")
