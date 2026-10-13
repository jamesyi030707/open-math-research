#!/usr/bin/env python3
"""
Independent checker for paradox_cert_J<J>.json.   (Does NOT import paradox_gen.py; no C code; scan is numpy.)
Checks:
  K1  qmax[j] == max{q : 3^q < 2^j}                                   (exact integers, recomputed)
  K2  H[j] is the exact integer bound: cond(H) true and cond(H+1) false, cond(h) := (3h+1)^q >= 2^j h^q at q=qmax[j]
       (cond is monotone decreasing in h, so this pins H = floor(h*); if cond(1) is false then H must be 0)
  K3  Hmax = max H, and X == max{ T^t(m) : m odd, 3<=m<=Hmax, 0<=t<=J }   (own code; FIRST J iterates only, no convergence assumed)
  K4  completeness: numpy scan of n in [3,X], j<=J with the rule  q <= qmax[j]  and  T^j(n) >= n  gives EXACTLY the certificate list
  K5  every listed (n,j,q): exact big-integer simulation: q odd terms, 3^q<2^j, T^j(n)>=n
  K6  sanity beyond the proof: scan of n in (X, X+200000] finds nothing (NOT part of the argument)
  --static-only: run K1-K3 only (used to re-check an already independently verified large certificate; scans are then NOT re-run)
  --selftest: mutated certificates (drop hit, fake hit, wrong H, wrong X, wrong qmax) must be rejected.
Soundness of the bound X is the paper argument in paradox_gen.py's header; K1-K3 check its numbers, K4-K5 the scan.
"""
import copy, hashlib, json, sys
import numpy as np

def T(n): return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def exact_qmax(j):
    q = 0
    while 3 ** (q + 1) < 2 ** j: q += 1
    return q

def first_iterates_max(m, J):
    x, mx = m, m
    for _ in range(J):
        x = T(x)
        if x > mx: mx = x
    return mx

def scan(lo, hi, J, qmax, chunk=1 << 20):
    hits = set()
    for start in range(lo, hi + 1, chunk):
        n = np.arange(start, min(hi, start + chunk - 1) + 1, dtype=np.uint64)
        x = n.copy(); q = np.zeros(n.shape, dtype=np.int32)
        for j in range(1, J + 1):
            odd = (x & np.uint64(1)).astype(bool)
            if int(x.max()) >= 2 ** 61: raise OverflowError("uint64 guard: value >= 2^61 (3x+1 could wrap)")
            x = np.where(odd, (np.uint64(3) * x + np.uint64(1)) >> np.uint64(1), x >> np.uint64(1))
            q += odd
            idx = np.nonzero((q <= qmax[j - 1]) & (x >= n))[0]
            for i in idx: hits.add((int(n[i]), j, int(q[i])))
    return hits

def static_checks(c):
    F = []
    J = c["J"]
    qm = [exact_qmax(j) for j in range(1, J + 1)]
    if c["qmax"] != qm: F.append("K1 qmax table differs")
    H_ok = True
    for j in range(1, J + 1):
        q = qm[j - 1]; H = c["H"][j - 1]
        cond = lambda h: (3 * h + 1) ** q >= (2 ** j) * h ** q
        if q < 1 or not cond(1):
            if H != 0: H_ok = False; F.append(f"K2 H[{j}] should be 0")
        else:
            if not (H >= 1 and cond(H) and not cond(H + 1)): H_ok = False; F.append(f"K2 H[{j}]={H} is not the exact bound")
    if max(c["H"]) != c["Hmax"]: F.append("K3 Hmax differs")
    X = max(first_iterates_max(m, J) for m in range(3, max(c["H"]) + 1, 2))
    if X != c["X"]: F.append(f"K3 X differs: recomputed {X}, certificate {c['X']}")
    return F, qm, H_ok, X

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    selftest = "--selftest" in sys.argv; static_only = "--static-only" in sys.argv
    path = args[0]
    raw = open(path, "rb").read()
    print(f"certificate {path} sha256={hashlib.sha256(raw).hexdigest()} ({len(raw)} bytes)")
    c = json.loads(raw); J = c["J"]
    F, qm, H_ok, X = static_checks(c)
    print(f"[{'PASS' if not F else 'FAIL'}] K1-K3: qmax table, exact H(j) bounds, Hmax={c['Hmax']}, X={c['X']} (recomputed X={X})")
    if static_only:
        print("[SKIPPED] K4-K6 (scan not re-run; relies on previously recorded independent verification)")
        print("=" * 60); print("STATIC CHECKS " + ("PASSED" if not F else "FAILED: " + str(F[:3]))); sys.exit(1 if F else 0)
    S = scan(3, c["X"], J, qm)
    cert_hits = {tuple(h) for h in c["hits"]}
    if S != cert_hits or len(cert_hits) != len(c["hits"]):
        F.append(f"K4 scan mismatch: only-scan={sorted(S-cert_hits)[:5]} only-cert={sorted(cert_hits-S)[:5]}")
    else:
        print(f"[PASS] K4 independent numpy scan of n in [3,{c['X']}], j<={J} reproduces the certificate list exactly ({len(S)} hits)")
    bad = 0
    for n, j, q in cert_hits:
        x, qq = n, 0
        for _ in range(j):
            if x & 1: qq += 1
            x = T(x)
        if not (qq == q and 3 ** qq < 2 ** j and x >= n and n > 2): bad += 1
    if bad: F.append(f"K5 {bad} listed hits fail direct verification")
    else: print(f"[PASS] K5 each listed hit verified by exact big-integer simulation")
    extra = scan(c["X"] + 1, c["X"] + 200000, J, qm)
    if extra: F.append(f"K6 sanity scan found hits above X: {sorted(extra)[:5]}")
    else: print(f"[PASS] K6 (sanity, not part of proof) no hits for n in ({c['X']}, {c['X']+200000}]")
    if selftest:
        print("---- selftest: mutated certificates must be REJECTED ----")
        def verdict(m):
            f, *_ = static_checks(m)
            h = {tuple(t) for t in m["hits"]}
            if h != S or len(h) != len(m["hits"]): f.append("scan mismatch")
            return f
        muts = []
        m = copy.deepcopy(c); m["hits"] = m["hits"][1:]; muts.append(("drop one hit", m))
        m = copy.deepcopy(c); m["hits"] = m["hits"] + [[3, 5, 2]]; muts.append(("add fake hit", m))
        jj = c["H"].index(max(c["H"])); m = copy.deepcopy(c); m["H"][jj] -= 1; muts.append(("H too small by 1", m))
        m = copy.deepcopy(c); m["H"][jj] += 1; muts.append(("H too large by 1", m))
        m = copy.deepcopy(c); m["X"] -= 1; muts.append(("X too small by 1", m))
        m = copy.deepcopy(c); m["qmax"][J // 2] += 1; muts.append(("qmax wrong", m))
        for name, m in muts:
            f = verdict(m)
            print(f"  mutation '{name}': {'REJECTED' if f else 'ACCEPTED (BAD!)'}")
            if not f: F.append(f"selftest: {name} accepted")
    print("=" * 60)
    if F: print("FAIL:", F[:4]); sys.exit(1)
    print(f"ALL CHECKS PASSED for J={J}: P(<=J) has exactly {len(S)} elements (n>2, all n); finite certificate, not a Collatz proof")

if __name__ == "__main__":
    main()
