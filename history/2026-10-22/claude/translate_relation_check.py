#!/usr/bin/env python3
"""Exact relation between Walsh spectra of two translates f+q, f+q' (q,q' in Q): with q''=q+q' (bent quadratic, W_{q''}(w)=8(-1)^{dual(w)}),
 W_{f+q'}(u) = (1/64) sum_v W_{f+q}(v) W_{q''}(u+v) = (1/8) sum_v W_{f+q}(v) (-1)^{dual_{q''}(u+v)}   (convolution theorem; (-1)^{f+q'} = (-1)^{f+q}(-1)^{q''}).
M=(1/8)(-1)^{dual(u+v)} is an orthogonal involution (bent: autocorrelation of dual vanishes off 0).  Small controls only; 64-point explicit tables, additive structure = XOR of 6-bit points."""
import random
from fractions import Fraction
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
def wht(s):
    a = s[:]; h = 1
    while h < 64:
        for i in range(0, 64, 2 * h):
            for j in range(i, i + h): x, y = a[j], a[j + h]; a[j], a[j + h] = x + y, x - y
        h *= 2
    return a
W = lambda f: wht([1 - 2 * v for v in f])
qlam = {l: [(Q[0][y] if l & 1 else 0) ^ (Q[1][y] if l & 2 else 0) ^ (Q[2][y] if l & 4 else 0) for y in range(64)] for l in range(8)}
dual = {}
for l in range(1, 8):
    Wq = W(qlam[l]); assert all(abs(w) == 8 for w in Wq); dual[l] = [0 if w > 0 else 1 for w in Wq]
def M(spec, l, d=None, exact=False):
    d = dual[l] if d is None else d
    out = []
    for u in range(64):
        s = sum(spec[v] * (1 - 2 * d[u ^ v]) for v in range(64))
        if exact: out.append(Fraction(s, 8))
        else: assert s % 8 == 0; out.append(s // 8)
    return out
random.seed(23); ok1 = ok2 = ok3 = True
for _ in range(40):
    f = [random.getrandbits(1) for _ in range(64)]; Wf = W(f)
    for l in range(1, 8):
        ok1 &= M(Wf, l) == W([a ^ b for a, b in zip(f, qlam[l])])
    for q in range(8):
        Wq_ = W([a ^ b for a, b in zip(f, qlam[q])])
        for q2 in range(8):
            if q2 != q: ok3 &= M(Wq_, q ^ q2) == W([a ^ b for a, b in zip(f, qlam[q2])])
    v = [random.randint(-20, 20) for _ in range(64)]; ok2 &= M(M(v, 3, exact=True), 3, exact=True) == v
print("positive control (random truth tables): relation W_{f+q''}=M W_f:", ok1, "| all 56 ordered translate pairs W_{f+q'}=M_{q+q'}W_{f+q}:", ok3, "| M^2=I:", ok2)
bad = 0; tot = 0
for _ in range(10):
    f = [random.getrandbits(1) for _ in range(64)]; Wf = W(f)
    for l, wrong in ((1, 2), (2, 4), (3, 5)):
        try: got = M(Wf, l, dual[wrong])
        except AssertionError: bad += 1; tot += 1; continue
        tot += 1; bad += got != W([a ^ b for a, b in zip(f, qlam[l])])
print(f"negative control (wrong dual function): mismatches {bad}/{tot}")
def rnd_quad():
    B = random.getrandbits(15); P = [(i, j) for i in range(6) for j in range(i + 1, 6)]
    aff = random.getrandbits(7)
    return [(sum(((y >> i) & 1) & ((y >> j) & 1) for n, (i, j) in enumerate(P) if (B >> n) & 1) + bin(y & (aff >> 1)).count("1") + (aff & 1)) % 2 for y in range(64)]
hist = {}; agree = True
for _ in range(1500):
    f = rnd_quad()
    for _ in range(random.randint(1, 3)): f[random.randrange(64)] ^= 1
    Wf = W(f); direct = [max(abs(w) for w in W([a ^ b for a, b in zip(f, qlam[q])])) <= 10 for q in range(8)]
    viaM = [max(abs(w) for w in (Wf if q == 0 else M(Wf, q))) <= 10 for q in range(8)]
    agree &= direct == viaM; k = sum(direct); hist[k] = hist.get(k, 0) + 1
print("near-quadratic f: predicate '|W_{f+q}|<=10' identical via direct truth table vs via M applied to W_f:", agree, "| #satisfied translates histogram:", dict(sorted(hist.items())))
