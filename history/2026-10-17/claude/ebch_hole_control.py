#!/usr/bin/env python3
"""Positive control for the model/solver pipeline: keep only the RM(1,6) subcode of E (128 words = words of E with weight in {0,32,64}); 64 free binary f_y, odd parity,
27 <= wt(f+e) <= 37 for the 64 representatives.  A feasible point is expected (bent function with one flipped point has distance 27 from RM(1,6)).  Time limit 30 s."""
import time, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
T0 = time.process_time(); g = 0x2759262d5d506d
rows = [(g << i) | ((bin(g << i).count("1") & 1) << 63) for i in range(10)]
cw = [0] * 1024
for m in range(1, 1024):
    low = m & -m; cw[m] = cw[m ^ low] ^ rows[low.bit_length() - 1]
rm = [w for w in cw if w.bit_count() in (0, 32, 64)]; assert len(rm) == 128
reps = sorted({min(w, w ^ ((1 << 64) - 1)) for w in rm}); assert len(reps) == 64
A = np.zeros((65, 65)); lb = np.zeros(65); ub = np.zeros(65)
for r, e in enumerate(reps):
    for y in range(64): A[r, y] = 1 - 2 * ((e >> y) & 1)
    lb[r], ub[r] = 27 - e.bit_count(), 37 - e.bit_count()
A[64, :64] = 1; A[64, 64] = -2; lb[64] = ub[64] = 1
res = milp(c=np.zeros(65), constraints=LinearConstraint(A, lb, ub), integrality=np.ones(65), bounds=Bounds(np.zeros(65), np.r_[np.ones(64), 32]), options={"time_limit": 30.0})
print("control status:", res.status, res.message)
if res.x is not None:
    f = sum(1 << y for y in range(64) if round(res.x[y]))
    d_rm = min((f ^ e).bit_count() for e in rm); d_E = min((f ^ e).bit_count() for e in cw)
    print("control candidate: wt(f) =", f.bit_count(), "| min wt(f+e) over the 128 RM(1,6) words =", d_rm, "| over all 1024 words of E =", d_E)
print(f"CPU process time {time.process_time()-T0:.1f}s")
