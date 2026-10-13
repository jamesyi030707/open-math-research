#!/usr/bin/env python3
"""
Generate a certificate for  P(<=J) := { (n,j) : n>2, 1<=j<=J, 3^q<2^j, T^j(n)>=n }   (paradoxical sequences, Rozier-Terracol Def. 1.1)
for ALL n, by a finite argument (re-derived here; the AM-GM step is the one in Rozier-Terracol Thm 4.2 / Cor 4.3):

  (1) T^j(n) = n * (3^q/2^j) * prod_k (1 + 1/(3 m_k)),  m_k = the q odd terms among n,...,T^{j-1}(n)   [each odd step: (3m+1)/2 = (3m/2)(1+1/(3m))].
  (2) paradoxical => prod_k (1+1/(3m_k)) >= 2^j/3^q;  AM-GM: prod <= (1+1/(3h))^q, h = harmonic mean of the m_k
      => (3+1/h)^q >= 2^j  => h <= h*(j,q) := max integer h with (3h+1)^q >= 2^j h^q (exact integer search; the function is decreasing in h).
  (3) q <= qmax(j) := max q with 3^q < 2^j, and h*(j,q) increases with q, so the smallest odd term m_o <= h <= H(j) := h*(j,qmax(j)).
      (If m_o = 1 the orbit ends in {1,2} and T^j(n) <= 2 < n: impossible for n>2.)
  (4) m_o = T^i(n) (i<=j-1), so n <= T^j(n) = T^{j-i}(m_o) <= MT(m_o) = max of the orbit of m_o.
      Hence n <= X(J) := max{ MT(m) : m odd, 3<=m<=Hmax(J) },  Hmax(J) = max_{j<=J} H(j).   [orbits of those m are followed to 1]
  (5) Therefore P(<=J) is finite and is obtained by scanning n in [3,X(J)], j<=J  (C program paradox_scan.c).
Usage: gcc -O2 -o /tmp/paradox_scan paradox_scan.c ; PARADOX_SCAN=/tmp/paradox_scan python3 paradox_gen.py J
       -> paradox_cert_J<J>.json, qmax_J<J>.txt
This script only GENERATES; verification is check_paradox_cert.py (independent code path).
"""
import json, os, subprocess, sys, hashlib

def T(n): return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def qmax_of(j):
    q = 0
    while 3 ** (q + 1) < 2 ** j: q += 1
    return q

def hstar(j, q):
    if q < 1: return 0
    cond = lambda h: (3 * h + 1) ** q >= (2 ** j) * h ** q
    if not cond(1): return 0
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

def main():
    J = int(sys.argv[1])
    qm = [None] + [qmax_of(j) for j in range(1, J + 1)]
    H = [None] + [hstar(j, qm[j]) for j in range(1, J + 1)]
    Hmax = max(H[1:])
    X = max(MT(m) for m in range(3, Hmax + 1, 2))
    open(f"qmax_J{J}.txt", "w").write("\n".join(str(qm[j]) for j in range(1, J + 1)) + "\n")
    out = subprocess.run([os.environ.get("PARADOX_SCAN", "./paradox_scan"), str(J), str(X), f"qmax_J{J}.txt"], capture_output=True, text=True, check=True).stdout
    hits = [tuple(map(int, l.split())) for l in out.splitlines()]
    cert = {"J": J, "qmax": qm[1:], "H": H[1:], "Hmax": Hmax, "X": X, "hits": hits}
    fn = f"paradox_cert_J{J}.json"
    json.dump(cert, open(fn, "w"))
    print(f"J={J}: Hmax={Hmax}, X={X}, hits={len(hits)}; wrote {fn}  sha256={hashlib.sha256(open(fn,'rb').read()).hexdigest()}")
    print("GENERATED (not verified). Run: python3 check_paradox_cert.py", fn)

if __name__ == "__main__":
    main()
