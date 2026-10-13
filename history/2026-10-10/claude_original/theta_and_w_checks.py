#!/usr/bin/env python3
"""
Part I  (G6 correction).  For a class r mod 2^k let  D_j=2^j-3^{s_j},  b_j = 2^j T^j(n)-3^{s_j} n  (j<=k),
   theta_r := min{ b_j/D_j : 1<=j<=k, D_j>0 }  (inf if the set is empty).
 Exact class criterion (paper proof: T^j(n)<n <=> D_j>0 and b_j<D_j n; exists j  <=>  n>theta_r):
        for n = r (mod 2^k):   sigma(n) <= k   <=>   n > theta_r.
 First-threshold condition (stronger, sufficient for the classification): least n>1 of a covered class exceeds b_{j*}/D_{j*}.
 Classification 'sigma(n)<=k <=> n in a covered class, for all n>1' holds  <=>  every covered class has  nmin(r) > theta_r.
 (Necessity of the FIRST-threshold condition is NOT claimed: n could fail at j* and still descend later within k steps.)
Part II (w_m).  w_m=(3^m-1)/2^v, v=v2(3^m-1).  Same layer e=v2(m):  v2(w_m'-w_m) = 1+v2(m'-m) (e=0), v2(m'-m)-e (e>=1).
 Proof: w'-w=(3^m'-3^m)/2^v; 3^m'-3^m=3^m(3^d-1), d=m'-m even, v2(3^d-1)=2+v2(d); v=1 (e=0) or e+2 (e>=1).
 Hence w_m' = w_m (mod 2^L) iff m'=m mod 2^{L-1} (e=0)  or  mod 2^{e+L} (e>=1); with the bijection words <-> residues
 (branches of w mod 2^L), these moduli are EXACT within a layer (not just sufficient), except for degenerate small L (printed below).
"""
import json
from fractions import Fraction
INF = None
def T(n): return n // 2 if n % 2 == 0 else (3 * n + 1) // 2
def v2(x): return (x & -x).bit_length() - 1
def sigma_le(n, k):
    x = n
    for j in range(1, k + 1):
        x = T(x)
        if x < n: return j
    return None

def class_info(r, k):
    n0 = r + (1 << k); x = n0; s = 0; thetas = []; first = None
    for j in range(1, k + 1):
        s += x & 1; x = T(x)
        D = (1 << j) - 3 ** s; b = (1 << j) * x - 3 ** s * n0
        assert D != 0 and b >= 0
        if D > 0:
            f = Fraction(b, D); thetas.append(f)
            if first is None: first = f
    return (min(thetas) if thetas else INF), first

def part1():
    print("== Part I: theta_r vs first threshold, k=1..14 ==")
    print(" k  covered  classif.valid  first-thr valid  #classes theta<first  max theta   max first-thr   exact-criterion mismatches (n<=60000)")
    for k in range(1, 15):
        M = 1 << k; info = [class_info(r, k) for r in range(M)]
        covered = sum(1 for th, f in info if th is not INF)
        ok_theta = ok_first = True; strict = 0; mt = Fraction(0); mf = Fraction(0)
        for r, (th, f) in enumerate(info):
            if th is INF: continue
            nmin = r if r >= 2 else r + M
            ok_theta &= nmin > th; ok_first &= nmin > f
            strict += th < f; mt = max(mt, th); mf = max(mf, f)
        mism = 0
        for n in range(2, 60001):
            th = info[n % M][0]
            pred = th is not INF and n > th
            if pred != (sigma_le(n, k) is not None): mism += 1
        print(f"{k:2d}  {covered:6d}  {str(ok_theta):13s}  {str(ok_first):15s}  {strict:10d}      {str(mt):>10s}  {str(mf):>12s}   {mism}")

def part2():
    print("== Part II: w_m formulas ==")
    w = {}
    for m in range(1, 301):
        x = 3 ** m - 1; v = v2(x); w[m] = (x >> v, v)
    bad = pairs = 0
    for m in range(1, 301):
        for mp in range(m + 1, 301):
            if v2(m) != v2(mp): continue
            e = v2(m); pairs += 1
            exp = 1 + v2(mp - m) if e == 0 else v2(mp - m) - e
            if v2(w[mp][0] - w[m][0]) != exp: bad += 1
    print(f"  v2(w_m'-w_m) formula, all same-layer pairs m<m'<=300: {pairs} pairs, violations {bad}")
    odd_ok = all(w[m][0] % 4 == 1 and (m == 1 or T(T(w[m][0])) < w[m][0]) for m in range(1, 301, 2))
    print(f"  odd m<=299: w=1 mod 4 and (m>=3) T^2(w)<w: {odd_ok};  m=1: w=1, T^2(1)={T(T(1))} (not < 1)")
    def word(x, L):
        o = []
        for _ in range(L): o.append(x & 1); x = T(x)
        return tuple(o)
    # exact minimal translation periods within a layer (brute force over m<=4096), vs formula
    W = {}
    for m in range(1, 4097):
        x = 3 ** m - 1; W[m] = word(x >> v2(x), 11)
    print("  minimal a with (m=m' mod 2^a, same layer => same W_L) vs formula [odd: L-1 ; even: e+L]  ('deg' = degenerate small L)")
    print("   e  L : min a   formula   note")
    for e in (0, 1, 2, 3):
        for L in range(1, 9):
            if e + L > 10: continue
            ms = [m for m in range(1, 4097) if v2(m) == e]
            a = 0
            while True:
                grp = {}
                for m in ms: grp.setdefault(m % (1 << a), set()).add(W[m][:L])
                if all(len(s) == 1 for s in grp.values()): break
                a += 1
            f = (L - 1) if e == 0 else (e + L)
            note = "" if a == f else "deg (W constant on the layer)" if a == 0 else "DIFFERS"
            print(f"   {e}  {L} : {a:5d}   {f:7d}   {note}")
    # bijection / counts, L=12, e=1 and covered fraction
    cert = json.load(open("cert_k12.json"))
    covered = set()
    for p in cert["prefixes"]:
        for t in range(1 << (12 - p["len"])): covered.add(p["res"] + (t << p["len"]))
    cov_odd = sum(1 for r in covered if r % 2 == 1)
    print(f"  certificate: covered odd residues mod 4096 = {cov_odd} of 2048 -> {Fraction(cov_odd, 2048)} (expected 1822/2048 = 911/1024)")
    for e in (1, 2):
        res = {}; bad = 0
        for q in range(1, 4096, 2):
            m = (1 << e) * q; x = 3 ** m - 1; ww = x >> v2(x)
            res[q] = ww % 4096
            if m != 2 and ww > 1:
                direct = sigma_le(ww, 12) is not None
                if direct != (ww % 4096 in covered): bad += 1
        distinct = len(set(res.values())); cov = sum(1 for q, r in res.items() if r in covered)
        print(f"  layer e={e}: q odd mod 4096 -> w mod 4096: {distinct} distinct residues (bijection onto odd residues: {distinct == 2048}); "
              f"covered {cov} (= {Fraction(cov, 2048)}); direct sigma<=12 vs covered mismatches (m!=2): {bad}")
    print("  note: this is about descent of w_m BELOW w_m (w_m ~ 1.5^m*(2^m-1)); it says nothing about sigma(2^m-1).")

if __name__ == "__main__":
    part1(); part2()
