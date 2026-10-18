#!/usr/bin/env python3
"""57-variable OPB variant: parity row  sum f - 2u = 27,  u = b0+2*b1+4*b2 (x55..x57), replacing the 5-bit row sum f - 2t = 1.  ebch_hole.opb (59 vars) is read, NOT modified.
PROOF.  The 1024 rows include e=0 (sum f >= 27) and e=all-ones (-sum f >= 27-64, i.e. sum f <= 37), both present in the file (checked below).
 (=>) If (f,b) satisfies everything: sum f = 27+2u is odd, in [27,37].  (<=) If f is odd and satisfies the rows: sum f in {27,29,...,37}, so u=(sum f-27)/2 in {0..5} subset of [0,7]
 has exactly one bit pattern.  u=6,7 would need sum f = 39,41 > 37, excluded by the all-ones row.  Hence (f,u) feasible <=> f odd and all 1024 rows hold; same f-solution set as the 59-variable file."""
import hashlib
# Editorial portability correction: record the input digest here instead of relying on an unprovided session scratch file.
original_sha = hashlib.sha256(open("ebch_hole.opb", "rb").read()).hexdigest()
lines = open("ebch_hole.opb").read().splitlines(); assert lines[0] == "* #variable= 59 #constraint= 1025"
rows = [l for l in lines if l and not l.startswith("*")]; assert len(rows) == 1025; body, par_old = rows[:1024], rows[1024]
assert par_old == " ".join(f"+1 x{c}" for c in range(1, 55)) + " -2 x55 -4 x56 -8 x57 -16 x58 -32 x59 = 1 ;"
par_new = " ".join(f"+1 x{c}" for c in range(1, 55)) + " -2 x55 -4 x56 -8 x57 = 27 ;"
open("ebch_hole_u3.opb", "w").write("\n".join(["* #variable= 57 #constraint= 1025", "* mode=full_u3; x1..x54 = f at coordinates 10..63; x55..x57 = bits b0..b2 of u; same 1024 distance rows as ebch_hole.opb",
    "* last row: sum f - 2u = 27"] + body + [par_new]) + "\n")
new = [l for l in open("ebch_hole_u3.opb").read().splitlines() if l and not l.startswith("*")]
print("new file: 57 vars, constraints:", len(new), "| first 1024 rows identical to original:", new[:1024] == body)
allp = " ".join(f"+1 x{c}" for c in range(1, 55)); alln = " ".join(f"-1 x{c}" for c in range(1, 55))
print("e=0 row present:", allp + " >= 27 ;" in body, "| e=all-ones row present:", alln + " >= -37 ;" in body)
lo, hi = 27, 37
new_s = sorted((s, u) for s in range(55) for u in range(8) if lo <= s <= hi and s - 2 * u == 27)
old_s = sorted((s, t) for s in range(55) for t in range(32) if lo <= s <= hi and s - 2 * t == 1)
print("exhaustive: 55 sums x 8 u-values -> feasible (sum,u):", new_s)
print("old encoding feasible (sum,t) count:", len(old_s), "| same sum-sets:", [s for s, _ in new_s] == [s for s, _ in old_s], "| each sum has exactly one aux value in both")
print("u=6,7 would force sums", [27 + 2 * u for u in (6, 7)], "-> violate all-ones row sum<=37:", all(27 + 2 * u > 37 for u in (6, 7)))
# planted witness for the RM-only control (explicit assignment => relaxed control SAT; says nothing about the full E model)
G = 0x2759262d5d506d; R = [(G << i) | ((bin(G << i).count("1") & 1) << 63) for i in range(10)]; E = [0] * 1024
for m in range(1, 1024):
    low = m & -m; E[m] = E[m ^ low] ^ R[low.bit_length() - 1]
pc = lambda x: bin(x).count("1"); RM = [w for w in E if pc(w) in (0, 32, 64)]
f = 0x172e5cb972e5cb97 ^ 1; dE = [pc(f ^ e) for e in E]; dR = [pc(f ^ e) for e in RM]
print(f"witness f = {f:016x} (q1 xor delta_coordinate1), wt(f) = {pc(f)}, t = {(pc(f)-1)//2}")
print("direct distances: RM(1,6) min/max =", min(dR), max(dR), "| all E min/max =", min(dE), max(dE), "| attained at e =", f"{E[dE.index(min(dE))]:016x}")
print("original 59-var file unchanged:", hashlib.sha256(open('ebch_hole.opb','rb').read()).hexdigest() == original_sha)
