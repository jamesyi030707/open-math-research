#!/usr/bin/env python3
"""Handoff checker: E = extended BCH(63,27) [64,10,28] (g=0x2759262d5d506d) contains RM(1,6) under an explicit coordinate map, plus three complementary generators.
Coordinate map: coordinate i (1..63, bit i-1 of a word) <-> point y = alpha^(i-1) in GF(64)=F2[x]/(x^6+x+1), alpha=x; coordinate 64 (bit 63) <-> y = 0.
Reason (Mattson-Solomon): c_k = sum_{s in nonzeros} C_s alpha^(-sk); nonzeros {0},{31,..} give a + Tr64(beta*y); nonzeros {27,45,54} give Tr8(gamma*y^36) (quadratic).
Standard library only."""
EXP = [0] * 126; e = 1
for i in range(63):
    EXP[i] = e; e <<= 1
    if e & 64: e ^= 0x43
for i in range(63, 126): EXP[i] = EXP[i - 63]
LOG = {EXP[i]: i for i in range(63)}
mul = lambda a, b: 0 if a == 0 or b == 0 else EXP[LOG[a] + LOG[b]]
def pw(y, k): return 0 if y == 0 else EXP[(LOG[y] * k) % 63]
def tr64(y):                                   # absolute trace GF(64)->F2
    t = 0
    for i in range(6): t ^= pw(y, 2 ** i) if y else 0
    assert t in (0, 1); return t
def tr8(z):                                    # trace GF(8)->F2 for z in GF(8) (z = z^8)
    t = z ^ mul(z, z) ^ pw(z, 4) if z else 0
    assert t in (0, 1); return t
pts = [EXP[i] for i in range(63)] + [0]
word = lambda f: sum(f(y) << i for i, y in enumerate(pts))
g = 0x2759262d5d506d
rows = [(g << i) | ((bin(g << i).count("1") & 1) << 63) for i in range(10)]
cw = [0] * 1024
for m in range(1, 1024):
    low = m & -m; cw[m] = cw[m ^ low] ^ rows[low.bit_length() - 1]
E = set(cw); assert len(E) == 1024
aff = {word(lambda y, a=a, b=b: a ^ tr64(mul(b, y))) for a in (0, 1) for b in range(64)}
print("RM(1,6) words from the map: distinct =", len(aff), "| all in E:", aff <= E, "| equals {w in E: wt in {0,32,64}}:", aff == {w for w in E if bin(w).count('1') in (0, 32, 64)})
basis_rm = [word(lambda y: 1)] + [word(lambda y, j=j: tr64(mul(EXP[j], y))) for j in range(6)]
print("RM(1,6) basis (all-ones, Tr(alpha^j y), j=0..5):", [format(w, "016x") for w in basis_rm])
theta = EXP[9]
q = [word(lambda y, gm=EXP[9 * k]: tr8(mul(gm, pw(y, 36)))) for k in range(3)]
def span(vs):
    S = {0}
    for v in vs: S |= {s ^ v for s in S}
    return S
print("q1,q2,q3 (gamma = 1, theta, theta^2; theta=alpha^9):", [format(w, "016x") for w in q], "| in E:", all(w in E for w in q))
print("dim span(RM(1,6), q1,q2,q3) =", len(span(basis_rm + q)).bit_length() - 1, "(=10 means they complement RM(1,6) in E) | equals E:", span(basis_rm + q) == E)
Q = span(q); Wts = sorted({bin(a ^ w).count("1") for w in Q if w for a in aff})
print("weights of (nonzero q in span) + affine:", Wts, "-> all 7 nonzero quadratics bent (distance 28 from RM(1,6))")
