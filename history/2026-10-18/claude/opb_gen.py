#!/usr/bin/env python3
"""Dependency-free exact OPB generator for the fixed parent E = extended BCH(63,27) [64,10,28]  (g = 0x2759262d5d506d; bit y of a word = coordinate y+1).
Decision problem: is there an ODD f in F2^64 with wt(f+e) >= 27 for ALL 1024 e in E?   (Upper side wt<=37 is the same condition at e+all-ones, all-ones in E.)
EQUIVALENCE ARGUMENT (mode 'full').
 Gauge: coordinates I = 0..9 form an information set of E (projection of E to I is bijective; asserted below).  For any f put e = the word of E agreeing with f on I; then f+e vanishes on I,
   d(f+e,E)=d(f,E) and wt(f+e) = wt(f) (mod 2) because E is even.  So solutions exist iff solutions with f|_I=0 exist; no coset is lost.
 Variables x1..x54 = f_y for y in J = {10..63} (f_y = 0 on I).  For e in E:  wt(f+e) = wt(e|_I) + sum_{y in J, e_y=0} f_y + sum_{y in J, e_y=1} (1-f_y)
   = wt(e) + sum_{e_y=0} f_y - sum_{e_y=1} f_y.   Hence  wt(f+e) >= 27  <=>  sum_{e_y=0} f_y - sum_{e_y=1} f_y >= 27 - wt(e)      (exact; frozen bits are inside wt(e)).  One row per e, 1024 rows.
 Parity: bits b0..b4 = x55..x59,  t = sum 2^i b_i in [0,31].  Row:  sum_{j} x_j - 2t = 1.  Safe: sum_j x_j <= 54 so a feasible t = (sum-1)/2 <= 26 < 32; an odd sum gives exactly one t,
   an even sum gives none.  So (f,t) feasible <=> f odd (t determined by f).  Total: #variable=59, #constraint=1025.
 Mode 'rm_free' (control only): 64 free variables, only the 128 words of RM(1,6) inside E; expected SATISFIABLE (bent function with one flipped point)."""
import sys
G = 0x2759262d5d506d
def words():
    rows = [(G << i) | ((bin(G << i).count("1") & 1) << 63) for i in range(10)]
    cw = [0] * 1024
    for m in range(1, 1024):
        low = m & -m; cw[m] = cw[m ^ low] ^ rows[low.bit_length() - 1]
    return cw
def make(mode):
    cw = words()
    if mode == "full":
        I = list(range(10)); J = [y for y in range(64) if y not in I]; ws = cw
        assert len({tuple((w >> y) & 1 for y in I) for w in cw}) == 1024        # information set
    else:
        J = list(range(64)); ws = [w for w in cw if bin(w).count("1") in (0, 32, 64)]
    nv = len(J) + 5; nc = len(ws) + 1
    out = [f"* #variable= {nv} #constraint= {nc}", f"* mode={mode}; x1..x{len(J)} = f at coordinates {J[0]}..{J[-1]} (bit y of a word); x{len(J)+1}..x{nv} = bits b0..b4 of t",
           "* rows: sum_{e_y=0} f_y - sum_{e_y=1} f_y >= 27 - wt(e), one per word e; last row: sum f - 2t = 1"]
    for e in ws:
        out.append(" ".join(("-1" if (e >> y) & 1 else "+1") + f" x{c+1}" for c, y in enumerate(J)) + f" >= {27 - bin(e).count('1')} ;")
    out.append(" ".join(f"+1 x{c+1}" for c in range(len(J))) + " " + " ".join(f"-{2 << i} x{len(J)+1+i}" for i in range(5)) + " = 1 ;")
    return "\n".join(out) + "\n"
if __name__ == "__main__":
    open("ebch_hole.opb", "w").write(make("full")); open("ebch_hole_rm_control.opb", "w").write(make("rm_free"))
    print("wrote ebch_hole.opb (59 vars, 1025 constraints) and ebch_hole_rm_control.opb (69 vars, 129 constraints)")
