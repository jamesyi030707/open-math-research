#!/usr/bin/env python3
"""Branch Ah=0 (A rows even, D=<(A|B)> doubly even, h = weight-32 word of B, kernel of u->uA is {0,h}).
Pair types {u,u+h} share s=wt(uA) (even, s=t mod 4, 27-t<=s<=t):  P1(14,22):s=14 x160 | P2(16,24):s in{12,16} x80 | P3(16,16):s in{12,16} x31 | P4(18,18):s in{10,14,18} x160 | P5(20,20):s in{8,12,16,20} x80 | P0(0,32):s=0 x1.
Exact checks: E_B=0 and z_B=0 from B's enumerator; for D: A_w from counts; dual weights A'_j=(1/1024)sum A_w K_j(w) must be integers >=0, A'_w>=A_w (D subset D^perp), A'_1=z_A, A'_2=E_A+X with E_A (equal A-column pairs) and X (equal A-B column pairs) integers>=0 (E_B=0).
Deterministic; aggregates enumerated exhaustively (first moment: a32+2a36+3a40 = 1031-128z); realizations by a small ILP FINDER, every result re-verified in exact integers."""
import time, numpy as np
from fractions import Fraction
from math import comb
import scipy.optimize as so
T0 = time.process_time()
Bw = {0: 1, 14: 160, 16: 142, 18: 320, 20: 160, 22: 160, 24: 80, 32: 1}
assert sum(Bw.values()) == 1024
m1 = sum(w * c for w, c in Bw.items()); m2 = sum(Fraction(2 * w - 37, 2) ** 2 * c for w, c in Bw.items())
print("B: sum t =", m1, "= 512*37:", m1 == 512 * 37, "| sum (t-18.5)^2 =", m2, "-> E_B =", (m2 / 256 - 37) / 2, "(equal-column pairs), z_B =", 37 - Fraction(m1, 512) )
K = lambda j, w: sum((-1) ** s * comb(w, s) * comb(64 - w, j - s) for s in range(min(w, j) + 1))
W = [28, 32, 36, 40]; Kt = {j: [K(j, 0)] + [K(j, w) for w in W] for j in range(65)}
cands = []
for z in range(0, 9):
    R = 1031 - 128 * z
    for a40 in range(0, 344):
        a36 = np.arange(160, 516, dtype=np.int64); a32 = R - 2 * a36 - 3 * a40; a28 = 1023 - a32 - a36 - a40
        ok = (a32 >= 1) & (a28 >= 160)
        for a36v, a32v, a28v in zip(a36[ok], a32[ok], a28[ok]): cands.append((int(a28v), int(a32v), int(a36v), a40, z))
cn = np.array(cands, dtype=np.int64); print("aggregate candidates after first moment & ranges:", len(cands))
keep = np.ones(len(cn), dtype=bool)
for j in range(2, 15):
    k = Kt[j]; T = k[0] + cn[:, 0] * k[1] + cn[:, 1] * k[2] + cn[:, 2] * k[3] + cn[:, 3] * k[4]
    keep &= (T % 1024 == 0) & (T >= 0)
    if j in (2, 3, 4, 14): print(f"  after dual j<={j}: {int(keep.sum())} survive")
surv = []
for row in cn[keep]:
    a = [int(row[0]), int(row[1]), int(row[2]), int(row[3])]; z = int(row[4]); good = True; dual = []
    for j in range(65):
        k = Kt[j]; T = k[0] + sum(a[i] * k[i + 1] for i in range(4))
        if T % 1024 or T < 0: good = False; break
        dual.append(T // 1024)
    if good and all(dual[w] >= a[i] for i, w in enumerate(W)) and dual[1] == z and sum(dual) == 2 ** 54: surv.append((a, z, dual))
print("aggregates passing ALL exact dual integrality/nonnegativity/containment (j=0..64):", len(surv))
