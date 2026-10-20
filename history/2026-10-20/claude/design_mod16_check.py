#!/usr/bin/env python3
"""Audit: E=[64,10,28]=RM(1,6)+<q1,q2,q3>. (1) weight-4 words of E^perp = 4-subsets with XOR of points 0 and XOR q_i = 0 (=2-flats isotropic for all B_qi): 2-(64,4,3) design, 1008 blocks, degree 63.
(2) V=#blocks meeting F (|F|=w) oddly: V = 63w - 6C(w,2) (mod 4)  [design counting: n1+2n2+3n3+4n4=63w, n2+3n3+6n4=3C(w,2)].
(3) T4: sum_{e in E} K4(wt(f+e)) = 1024*(1008-2V) for every f (character sum over the 1008 dual words).
(4) For an odd coset with weights 27..37 only, complement-closed: (b27,b29,b31)=(x,288+..): y=960-3x, z=2x-448 (T2=0); T4 then gives x=C=2828-4V; V=3 (mod 4) => C=0 (mod 16) => x=224+4t, t=0 (mod 4).
(5) Full MacWilliams dual enumerator of D=E u (f+E) for all 25 old profiles."""
import itertools, random
from math import comb
from fractions import Fraction
from collections import Counter
G = 0x2759262d5d506d
rows = [(G << i) | ((bin(G << i).count("1") & 1) << 63) for i in range(10)]
cw = [0] * 1024
for m in range(1, 1024):
    low = m & -m; cw[m] = cw[m ^ low] ^ rows[low.bit_length() - 1]
pc = lambda x: bin(x).count("1"); wts = [pc(w) for w in cw]
A = [wts.count(i) for i in range(65)]; assert {i: A[i] for i in range(65) if A[i]} == {0: 1, 28: 448, 32: 126, 36: 448, 64: 1}
K = [[sum((-1) ** s * comb(i, s) * comb(64 - i, j - s) for s in range(min(i, j) + 1)) for i in range(65)] for j in range(65)]
Ad = [sum(A[i] * K[j][i] for i in range(65)) // 1024 for j in range(65)]; assert all(sum(A[i] * K[j][i] for i in range(65)) % 1024 == 0 for j in range(65))
print("dual enumerator: A4perp =", Ad[4], "| A2perp =", Ad[2], "| sum =", sum(Ad) == 2 ** 54)
cols = [sum(((rows[i] >> y) & 1) << i for i in range(10)) for y in range(64)]
blocks = [B for B in itertools.combinations(range(64), 4) if cols[B[0]] ^ cols[B[1]] ^ cols[B[2]] ^ cols[B[3]] == 0]
# GF(64) point map and quadratics (as rm16_membership.py)
EXP = [0] * 126; e = 1
for i in range(63):
    EXP[i] = e; e <<= 1
    if e & 64: e ^= 0x43
for i in range(63, 126): EXP[i] = EXP[i - 63]
LOG = {EXP[i]: i for i in range(63)}
mul = lambda a, b: 0 if a == 0 or b == 0 else EXP[LOG[a] + LOG[b]]
pw = lambda y, k: 0 if y == 0 else EXP[(LOG[y] * k) % 63]
tr8 = lambda z: (z ^ mul(z, z) ^ pw(z, 4)) if z else 0
PT = EXP[:63] + [0]; Qp = [[tr8(mul(EXP[9 * k], pw(y, 36))) for y in range(64)] for k in range(3)]   # indexed by POINT
geo = [B for B in itertools.combinations(range(64), 4) if PT[B[0]] ^ PT[B[1]] ^ PT[B[2]] ^ PT[B[3]] == 0 and all(Qp[k][PT[B[0]]] ^ Qp[k][PT[B[1]]] ^ Qp[k][PT[B[2]]] ^ Qp[k][PT[B[3]]] == 0 for k in range(3))]
deg = Counter(y for B in blocks for y in B); pr = Counter(p for B in blocks for p in itertools.combinations(B, 2))
print(f"blocks (dual weight 4) = {len(blocks)} | equal to geometric set (xor points=0, xor q_i=0): {set(blocks) == set(geo)} | point degrees {sorted(set(deg.values()))} | pair multiplicities {sorted(set(pr.values()))} over {len(pr)} pairs (of 2016)")
random.seed(21); okV = okcount = okT4 = True
for w in list(range(1, 64, 2)) * 4 + list(range(0, 65, 4)):
    F = random.sample(range(64), w); fm = sum(1 << y for y in F); n = Counter(pc(fm & sum(1 << y for y in B)) for B in blocks)
    V = n[1] + n[3]; okV &= V % 4 == (63 * w - 6 * comb(w, 2)) % 4 and (w % 2 == 0 or V % 4 == 3)
    okcount &= sum(j * n[j] for j in range(5)) == 63 * w and sum(comb(j, 2) * n[j] for j in range(5)) == 3 * comb(w, 2)
    okT4 &= sum(K[4][pc(fm ^ c)] for c in cw) == 1024 * (1008 - 2 * V)
print("random F (all sizes): V = 63w-6C(w,2) mod 4 and V=3 mod 4 for odd w:", okV, "| design counting identities:", okcount, "| T4 = 1024(1008-2V) identity:", okT4)
bad = 0
for x in range(224, 321, 4):
    y, z = 960 - 3 * x, 2 * x - 448; assert x + y + z == 512
    T4 = x * (K[4][27] + K[4][37]) + y * (K[4][29] + K[4][35]) + z * (K[4][31] + K[4][33])
    V = Fraction(1008) - Fraction(T4, 1024 * 2) ; V = (1008 - Fraction(T4, 1024)) / 2; bad += V != Fraction(2828 - x, 4)
print("T4 on the 25-point family gives V=(2828-C)/4 for every x=C:", bad == 0, "| residues: V=3 mod 4 => C mod 16 =", sorted({(2828 - 4 * V) % 16 for V in range(4) if V == 3}))
print("hence C=224+4t = 0 mod 16 <=> t = 0 mod 4; V range for survivors:", [(2828 - (224 + 4 * t)) // 4 for t in range(0, 25, 4)])
res = []; table = []
for t in range(25):
    x, y, z = 224 + 4 * t, 288 - 12 * t, 8 * t; b = [0] * 65
    b[27] = b[37] = x; b[29] = b[35] = y; b[31] = b[33] = z
    Dp = []; ok = True
    for j in range(65):
        s = sum((A[i] + b[i]) * K[j][i] for i in range(65))
        if s % 2048: ok = False; Dp.append(Fraction(s, 2048))
        else: Dp.append(s // 2048)
    good = ok and all(0 <= Dp[j] <= Ad[j] for j in range(65)) and sum(Dp) == 2 ** 53
    res.append((t, good)); table.append((t, x, y, z, Dp))
print("MacWilliams dual of D=E u (f+E): integrality + 0<=A'perp_j<=Aperp_j (containment) + sum=2^53 passes for t =", [t for t, g in res if g], "| fails for", [t for t, g in res if not g])
with open("design_mod16_dual_table.txt", "w") as fh:
    for t, x, y, z, Dp in table: fh.write(f"t={t} (b27,b29,b31)=({x},{y},{z}) A'perp_j (j=0..64): {[str(v) for v in Dp]}\n")
print("A'perp_4 = 301 + C/4 for the seven survivors:", [(t, table[t][4][4]) for t in range(0, 25, 4)])
