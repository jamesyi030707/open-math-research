#!/usr/bin/env python3
"""(1) Corollary check on paradox_cert_J300.json: for every hit (n,j): tau(n) < j and min(orbit n..T^j(n)) < n
   (=> no counterexample to Terras's CST t(n)=tau(n) among n>=3 with tau(n)<=300; n=2 has t=tau=1).
   (2) Budget probe: bound sizes Hmax(J), X(J) and scan cost ~ X*J for larger J (bounds only, no scan)."""
import json
def T(n): return n // 2 if n % 2 == 0 else (3 * n + 1) // 2
c = json.load(open("paradox_cert_J300.json"))
bad_tau = bad_min = 0
for n, j, q in c["hits"]:
    x, s, tau = n, 0, None
    orb = [n]
    for i in range(1, j + 1):
        s += x & 1; x = T(x); orb.append(x)
        if tau is None and 3 ** s < 2 ** i: tau = i
    if not (tau is not None and tau < j): bad_tau += 1
    if not min(orb) < n: bad_min += 1
print(f"hits: {len(c['hits'])}; with tau(n) >= j: {bad_tau}; with min(orbit) >= n: {bad_min}")
print("=> every paradoxical sequence with j<=300 is strictly after the stopping time of its first term (RT statements C2/C3 hold on this set)")
def qmax(j):
    q = 0
    while 3 ** (q + 1) < 2 ** j: q += 1
    return q
def hstar(j, q):
    cond = lambda h: (3 * h + 1) ** q >= (2 ** j) * h ** q
    if q < 1 or not cond(1): return 0
    hi = 1
    while cond(2 * hi): hi *= 2
    lo, hi = hi, 2 * hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cond(mid): lo = mid
        else: hi = mid
    return lo
def MT(m):
    x = m; mx = m
    while x != 1:
        x = T(x); mx = max(mx, x)
    return mx
print("J     Hmax    X(J)            scan cost X*J (steps)")
for J in (300, 400, 500, 700, 1000):
    H = max(hstar(j, qmax(j)) for j in range(2, J + 1))
    X = max(MT(m) for m in range(3, H + 1, 2))
    print(f"{J:5d} {H:7d} {X:14d}  {X*J:.2e}")
