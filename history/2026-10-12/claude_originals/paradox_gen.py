#!/usr/bin/env python3
"""
Generate a certificate for  P(<=J) := { (n,j) : n>2, 1<=j<=J, 3^q<2^j, T^j(n)>=n }   (paradoxical sequences, Rozier-Terracol Def. 1.1)
for ALL n.  (q = number of odd terms among n,...,T^{j-1}(n).)   [header corrected: steps (2)-(4)]

  (1) T^j(n) = n * (3^q/2^j) * prod_k (1 + 1/(3 m_k)),  m_k = the q odd terms among n,...,T^{j-1}(n)
      [each odd step: (3m+1)/2 = (3m/2)(1+1/(3m))].
  (2) Paradoxical (T^j(n) >= n, C=3^q/2^j<1) => prod_k (1+1/(3 m_k)) >= 2^j/3^q.  AM-GM: prod <= (1+1/(3h))^q, h = HARMONIC MEAN of
      the m_k (a real number)  =>  (3+1/h)^q >= 2^j  =>  1/h >= 2^{j/q}-3 > 0  =>  h <= R(j,q) := 1/(2^{j/q}-3)   (the REAL root).
  (3) Let m_o be the smallest odd value among the m_k (an INTEGER).  m_o <= h <= R(j,q) <= R(j,qmax(j))  (R increases with q, q<=qmax(j):=max{q: 3^q<2^j}),
      hence  m_o <= floor(R(j,qmax(j))) =: H(j).   For an integer h:  (3h+1)^q >= 2^j h^q  <=>  h <= R(j,q), so  floor(R(j,q)) is the largest
      integer h satisfying that inequality (this is what floor_R computes; it is NOT a bound on h itself, only on the integer m_o).
      (If m_o = 1 the orbit ends in {1,2}, T^j(n) <= 2 < n: impossible for n>2; so 3 <= m_o <= H(j) <= Hmax(J) := max_{j<=J} H(j).)
  (4) m_o = T^i(n) with 0<=i<=j-1, so  n <= T^j(n) = T^{j-i}(m_o) with 1 <= j-i <= J.  Therefore
        n <= X(J) := max{ T^t(m) : m odd, 3<=m<=Hmax(J), 0<=t<=J }.
      Only the FIRST J iterates of each m are used; no assumption that any orbit converges.
  (5) P(<=J) is finite and is obtained by scanning n in [3,X(J)], j<=J  (C program paradox_scan.c, unsigned __int128, no overflow possible
      for the values that occur; the independent numpy checker has an explicit guard).
Usage: gcc -O2 -o /tmp/paradox_scan paradox_scan.c ; PARADOX_SCAN=/tmp/paradox_scan python3 paradox_gen.py J
       -> paradox_cert_J<J>.json, qmax_J<J>.txt        (GENERATES only; verification = check_paradox_cert.py)
"""
import json, os, subprocess, sys, hashlib

def T(n): return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def qmax_of(j):
    q = 0
    while 3 ** (q + 1) < 2 ** j: q += 1
    return q

def floor_R(j, q):
    """floor of the real root R(j,q)=1/(2^{j/q}-3): largest integer h>=1 with (3h+1)^q >= 2^j h^q; 0 if none."""
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

def first_iterates_max(m, J):
    """max of T^t(m), t=0..J  (first J iterates only)"""
    x = m; mx = m
    for _ in range(J):
        x = T(x)
        if x > mx: mx = x
    return mx

def main():
    J = int(sys.argv[1])
    qm = [None] + [qmax_of(j) for j in range(1, J + 1)]
    H = [None] + [floor_R(j, qm[j]) for j in range(1, J + 1)]
    Hmax = max(H[1:])
    X = max(first_iterates_max(m, J) for m in range(3, Hmax + 1, 2))
    open(f"qmax_J{J}.txt", "w").write("\n".join(str(qm[j]) for j in range(1, J + 1)) + "\n")
    out = subprocess.run([os.environ.get("PARADOX_SCAN", "./paradox_scan"), str(J), str(X), f"qmax_J{J}.txt"],
                         capture_output=True, text=True, check=True).stdout
    hits = [tuple(map(int, l.split())) for l in out.splitlines()]
    cert = {"J": J, "x_definition": "max T^t(m), m odd, 3<=m<=Hmax, 0<=t<=J (first J iterates)", "qmax": qm[1:], "H": H[1:],
            "Hmax": Hmax, "X": X, "hits": hits}
    fn = f"paradox_cert_J{J}.json"
    json.dump(cert, open(fn, "w"))
    print(f"J={J}: Hmax={Hmax}, X={X}, hits={len(hits)}; wrote {fn}  sha256={hashlib.sha256(open(fn,'rb').read()).hexdigest()}")
    print("GENERATED (not verified). Run: python3 check_paradox_cert.py", fn)

if __name__ == "__main__":
    main()
