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
    if good and all(dual[w] >= a[i] for i, w in enumerate(W)) and dual[1] == z and sum(dual) == 2 ** 53: surv.append((a, z, dual))
print("aggregates passing ALL exact dual integrality/nonnegativity/containment (j=0..64):", len(surv))
def s2form(): return (59776, {"n12": -112, "m12": -112, "p10": 100, "p14": 196, "p18": 324, "r8": 64, "r12": 144, "r16": 256, "r20": 400})
names = ["n12", "m12", "p10", "p14", "p18", "r8", "r12", "r16", "r20", "E"]
def counts_to_agg(c):
    n12, m12, p10, p14, p18, r8, r12, r16, r20 = c
    return (160 + n12 + 2 * m12 + 2 * p10 + 2 * r8, 143 - n12 - 2 * m12 + 2 * p14 + 2 * r12, 160 + n12 + 2 * p18 + 2 * r16, 80 - n12 + 2 * r20)
found = None; tried = 0
for a, z, dual in surv:
    if time.process_time() - T0 > 40: break
    tried += 1; A2 = dual[2]
    Ssum = 512 * (27 - z) // 2                                  # sum over pairs of s
    rows = []; rhs = []
    rows.append([1, 2, 2, 0, 0, 2, 0, 0, 0, 0]); rhs.append(a[0] - 160)
    rows.append([-1, -2, 0, 2, 0, 0, 2, 0, 0, 0]); rhs.append(a[1] - 143)
    rows.append([1, 0, 0, 0, 2, 0, 0, 2, 0, 0]); rhs.append(a[2] - 160)
    rows.append([-1, 0, 0, 0, 0, 0, 0, 0, 2, 0]); rhs.append(a[3] - 80)
    rows.append([0, 0, 1, 1, 1, 0, 0, 0, 0, 0]); rhs.append(160)
    rows.append([0, 0, 0, 0, 0, 1, 1, 1, 1, 0]); rhs.append(80)
    c0, co = s2form(); rows.append([co[n] for n in names[:9]] + [-256]); rhs.append(27 * 2 * Ssum - 89856 - c0 + 0)   # sum s^2 - 256E = 27*sum s - 89856  (sum s over u = 2*Ssum)
    # sum s over u = 2*Ssum ; formula uses per-pair sums: sum_pairs s^2 - 27 sum_pairs s*... rewritten below
    res = None
    # per-pair form: sum_u (s-13.5)^2 = 2*sum_pairs(s-13.5)^2 = 256(27+2E)  =>  sum_pairs s^2 -27*Ssum + 93312 = 256E + 3456
    rows[-1] = [co[n] for n in names[:9]] + [-256]; rhs[-1] = 27 * Ssum - 93312 + 3456 - c0
    lb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]; ub = [80, 31, 160, 160, 160, 80, 80, 80, 80, min(351, A2)]
    r = so.milp(c=np.zeros(10), constraints=so.LinearConstraint(np.array(rows, float), rhs, rhs), integrality=np.ones(10), bounds=so.Bounds(lb, ub), options={"time_limit": 2.0})
    if r.x is None: continue
    x = [int(round(v)) for v in r.x]; c = x[:9]; E = x[9]
    if counts_to_agg(c) != tuple(a) or sum(c[2:5]) != 160 or sum(c[5:9]) != 80 or min(x) < 0: continue
    n12, m12, p10, p14, p18, r8, r12, r16, r20 = c
    pairs = [(14, 160, -1), (12, n12, 3), (16, 80 - n12, 3), (12, m12, -5), (16, 31 - m12, -5), (10, p10, -1), (14, p14, -1), (18, p18, -1), (8, r8, 3), (12, r12, 3), (16, r16, 3), (20, r20, 3), (0, 1, -5)]
    Ssum2 = sum(s * n for s, n, d in pairs); S2 = sum(n * (Fraction(s) - Fraction(27, 2)) ** 2 for s, n, d in pairs)
    Xn = sum(n * (Fraction(s) - Fraction(27, 2)) * d for s, n, d in pairs) / 256
    EA = S2 / 256 - Fraction(27, 2); z_ok = Ssum2 == 256 * (27 - z)
    if z_ok and EA == E and Xn.denominator == 1 and Xn >= 0 and E + Xn == A2: found = (a, z, dual, c, E, int(Xn)); break
print(f"aggregates tried by ILP finder: {tried}")
if found:
    a, z, dual, c, E, X = found
    print("FOUND relaxation point (not a code): weights A_28,A_32,A_36,A_40 =", a, "| z_A =", z, "| A'_1 =", dual[1], "| A'_2 =", dual[2], "= E_A + X =", E, "+", X)
    print("  counts n12,m12,p10,p14,p18,r8,r12,r16,r20 =", c, "| dual A'_j j=1..12:", dual[1:13])
else:
    print("no fully consistent realization found within the finder budget (this is NOT an exclusion unless no aggregate survived)")
print(f"process time {time.process_time()-T0:.1f}s")
