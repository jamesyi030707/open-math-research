#!/usr/bin/env python3
"""Independent verifier/tests for the OPB files: parses the TEXT files only, rebuilds E separately, checks rows <-> E words, per-row equivalence on random and boundary f, parity encoding, planted control."""
import random
G = 0x2759262d5d506d
rows_ = [(G << i) | ((bin(G << i).count("1") & 1) << 63) for i in range(10)]
E = [0] * 1024
for m in range(1, 1024):
    low = m & -m; E[m] = E[m ^ low] ^ rows_[low.bit_length() - 1]
pc = lambda x: bin(x).count("1")
assert len(set(E)) == 1024 and all(pc(w) % 2 == 0 for w in E) and min(pc(w) for w in E if w) == 28 and (1 << 64) - 1 in set(E)
def parse(path):
    nv = nc = None; cons = []
    for line in open(path):
        line = line.strip()
        if line.startswith("*"):
            if "#variable=" in line: p = line.split(); nv = int(p[2]); nc = int(p[4])
            continue
        if not line: continue
        assert line.endswith(";"); t = line[:-1].split()
        k = next(i for i, s in enumerate(t) if s in (">=", "="))
        cs = [int(t[i]) for i in range(0, k, 2)]; vs = [int(t[i + 1][1:]) for i in range(0, k, 2)]
        cons.append((cs, vs, t[k], int(t[k + 1])))
    return nv, nc, cons
def masks(cs, vs):
    P = N = 0
    for c, v in zip(cs, vs):
        assert abs(c) == 1; 
        if c > 0: P |= 1 << (v - 1)
        else: N |= 1 << (v - 1)
    return P, N
random.seed(11)
# ---------------- full model
nv, nc, cons = parse("ebch_hole.opb"); assert (nv, nc, len(cons)) == (59, 1025, 1025)
J = list(range(10, 64)); rows = cons[:1024]; par = cons[1024]
Jpart = {sum(((w >> y) & 1) << c for c, y in enumerate(J)): w for w in E}; assert len(Jpart) == 1024      # J-projection injective (d=28>10)
rowinfo = []
for cs, vs, op, rhs in rows:
    assert op == ">=" and vs == list(range(1, 55)); P, N = masks(cs, vs); e = Jpart[N]; assert rhs == 27 - pc(e) and P == (~N) & ((1 << 54) - 1)
    rowinfo.append((P, N, rhs, e))
assert len({r[3] for r in rowinfo}) == 1024
print("full: header 59 vars/1025 constraints OK; 1024 rows <-> 1024 distinct words of E; rhs = 27-wt(e) for every row; all coefficients +-1")
scatter = lambda F: sum(((F >> c) & 1) << y for c, y in enumerate(J))
def row_ok(r, F): P, N, rhs, e = r; return pc(F & P) - pc(F & N) >= rhs
mism = 0; tested = 0
for _ in range(3000):
    F = random.getrandbits(54); f = scatter(F)
    for r in rowinfo:
        tested += 1; mism += row_ok(r, F) != (pc(f ^ r[3]) >= 27)
print(f"random f (zero on I): {tested} row evaluations, mismatches vs direct wt(f+e)>=27: {mism}")
mism = 0; n = 0
for _ in range(400):
    P, N, rhs, e0 = random.choice(rowinfo)
    for w in (26, 27):
        k = w - pc(e0 & ((1 << 10) - 1)); S = random.sample(J, k); g = (e0 & ((1 << 10) - 1)) | sum(1 << y for y in S); f = e0 ^ g
        assert f & ((1 << 10) - 1) == 0 and pc(f ^ e0) == w; F = sum(((f >> y) & 1) << c for c, y in enumerate(J)); n += 1
        mism += row_ok((P, N, rhs, e0), F) != (w >= 27)
print(f"boundary f at distance exactly 26/27 from a chosen e0: {n} tests, mismatches: {mism}")
cs, vs, op, rhs = par; assert op == "=" and rhs == 1 and cs == [1] * 54 + [-2, -4, -8, -16, -32]
bad = 0
for s in range(55):
    sol = [t for t in range(32) if s - 2 * t == 1]; bad += (len(sol) != (s % 2)) or any(t > 26 for t in sol)
print("parity row: for every sum 0..54 exactly one t (<=26<32) iff sum odd, none if even; violations:", bad)
# ---------------- control (RM-only, free variables) with a planted solution: bent q1 plus one flipped point
nv2, nc2, cons2 = parse("ebch_hole_rm_control.opb"); assert (nv2, nc2, len(cons2)) == (69, 129, 129)
q1 = 0x172e5cb972e5cb97; assert q1 in set(E) and pc(q1) in (28, 36)
f = q1 ^ 1; rmw = [w for w in E if pc(w) in (0, 32, 64)]; ok = True
for (cs, vs, op, rhs), e in zip(cons2[:128], rmw):
    P, N = masks(cs, vs); val = pc(f & P) - pc(f & N); ok &= (val >= rhs) == (pc(f ^ e) >= 27) and val >= rhs
s = pc(f); t = (s - 1) // 2
print("control (RM-only, free vars): planted f = q1 xor delta_0, odd:", s % 2 == 1, "| all 128 RM rows satisfied and equal to direct test:", ok, "| min wt(f+e) over E =", min(pc(f ^ e) for e in E), "(<27, so full model rejects it)")
