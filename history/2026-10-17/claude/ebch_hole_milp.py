#!/usr/bin/env python3
"""Exact shared-variable model: does an ODD vector f in F2^64 exist with wt(f+e) in [27,37] for ALL 1024 words e of E = extended BCH(63,27) [64,10,28]?
(wt(f+e)>=27 for all e  <=>  coset f+E has minimum weight >= 27; <=37 is the same condition applied to e+all-ones, all-ones in E.)
Variables: f_y (y = coordinate), odd parity.  Constraints: for the 512 representatives e (up to complement):  27-wt(e) <= sum_y (1-2e_y) f_y <= 37-wt(e)
  [equivalently |W_{f+q}(u)| <= 10, W = sum_y (-1)^{f+e}]   -- 512 two-sided Walsh bounds.
Symmetry reduction (lossless): f -> f+e (e in E) preserves feasibility (d(f+e,E)=d(f,E)) and oddness (E even).  For an information set I of E (10 independent columns),
  every coset has exactly one representative with f|_I = 0; so fixing f_y=0 on I removes no coset.  No further (group) reduction is applied.
Solver: SciPy milp (HiGHS, bundled). Time limit 100 s of the <=120 CPU-s budget. A candidate is re-checked against all 1024 words independently of the solver.
UNSAT from HiGHS would be a SOLVER CLAIM ONLY (no independently checkable certificate); a timeout is UNRESOLVED."""
import time, sys, json, random
import numpy as np, scipy
from scipy.optimize import milp, LinearConstraint, Bounds
T0 = time.process_time()
g = 0x2759262d5d506d
rows = [(g << i) | ((bin(g << i).count("1") & 1) << 63) for i in range(10)]
cw = [0] * 1024
for m in range(1, 1024):
    low = m & -m; cw[m] = cw[m ^ low] ^ rows[low.bit_length() - 1]
assert len(set(cw)) == 1024 and all(w.bit_count() % 2 == 0 for w in cw) and ((1 << 64) - 1) in set(cw)
# information set: greedy independent columns of the generator matrix
basis = {}; I = []
for y in range(64):
    v = sum(((rows[i] >> y) & 1) << i for i in range(10)); x = v
    while x:
        p = x.bit_length() - 1
        if p in basis: x ^= basis[p]
        else: basis[p] = x; I.append(y); break
    if len(I) == 10: break
assert len({tuple((w >> y) & 1 for y in I) for w in cw}) == 1024        # projection onto I is bijective
J = [y for y in range(64) if y not in I]
reps = sorted({min(w, w ^ ((1 << 64) - 1)) for w in cw})
assert len(reps) == 512
A = np.zeros((512 + 1, len(J) + 1)); lb = np.zeros(513); ub = np.zeros(513)
for r, e in enumerate(reps):
    wt = e.bit_count()
    for c, y in enumerate(J): A[r, c] = 1 - 2 * ((e >> y) & 1)
    lb[r], ub[r] = 27 - wt, 37 - wt
A[512, :len(J)] = 1; A[512, len(J)] = -2; lb[512] = ub[512] = 1           # sum f_J = 2k+1  (odd)
# encoding self-test: row formula vs direct weights for random f vanishing on I
random.seed(3)
for _ in range(200):
    f = 0
    for y in J:
        if random.getrandbits(1): f |= 1 << y
    for r, e in enumerate(reps):
        s = sum(A[r, c] for c, y in enumerate(J) if (f >> y) & 1); w = (f ^ e).bit_count()
        assert (lb[r] <= s <= ub[r]) == (27 <= w <= 37) and s == w - e.bit_count()
print("model: %d binary f-variables (+1 integer k), 512 two-sided Walsh rows + 1 parity row; information set I = %s" % (len(J), I))
with open("ebch_hole_model.lp", "w") as fh:                                  # solver-neutral export (CPLEX LP format)
    fh.write("\\ odd f, 54 free binaries (f=0 on information set), 512 two-sided rows\nMinimize\n obj: 0 f0\nSubject To\n")
    for r in range(512):
        terms = " ".join(("+" if A[r, c] > 0 else "-") + " f%d" % c for c in range(len(J)))
        fh.write(f" lo{r}: {terms} >= {int(lb[r])}\n hi{r}: {terms} <= {int(ub[r])}\n")
    fh.write(" par: " + " ".join("+ f%d" % c for c in range(len(J))) + " - 2 k = 1\nBounds\n 0 <= k <= 27\nBinary\n " + " ".join("f%d" % c for c in range(len(J))) + "\nGeneral\n k\nEnd\n")
print("scipy", scipy.__version__, "numpy", np.__version__)
hv = None
try:
    from scipy.optimize import _highspy; hv = [n for n in dir(_highspy) if "version" in n.lower()]
except Exception as ex: hv = repr(ex)
print("HiGHS (bundled with SciPy); version attributes found:", hv)
res = milp(c=np.zeros(len(J) + 1), constraints=LinearConstraint(A, lb, ub), integrality=np.ones(len(J) + 1), bounds=Bounds(np.zeros(len(J) + 1), np.r_[np.ones(len(J)), 27]),
           options={"time_limit": 100.0, "disp": False})
print("solver status code:", res.status, "| message:", res.message, "| success:", res.success)
print("mip_node_count:", getattr(res, "mip_node_count", None), "| mip_dual_bound:", getattr(res, "mip_dual_bound", None), "| mip_gap:", getattr(res, "mip_gap", None))
if res.x is not None:
    f = sum(1 << y for c, y in enumerate(J) if round(res.x[c])); ws = sorted(bin(f ^ e).count("1") for e in cw)
    print("CANDIDATE returned; independent check over all 1024 words: min wt(f+e) =", ws[0], "max =", ws[-1], "| wt(f) =", f.bit_count(), "| valid hole:", ws[0] >= 27 and f.bit_count() % 2 == 1)
    print("f =", format(f, "016x"))
else:
    print("no candidate returned;", "SOLVER CLAIM ONLY: infeasible (no checkable certificate)" if res.status == 2 else "UNRESOLVED (limit/other status)")
print(f"CPU process time {time.process_time()-T0:.1f}s")
