#!/usr/bin/env python3
"""Task 1 & 2 for T(n)=n/2 (even), (3n+1)/2 (odd). Pure integer arithmetic."""
import sys
from collections import Counter
K = 12

def T(n): return n//2 if n % 2 == 0 else (3*n+1)//2

# ---- Implementation A: recurrence on (s,b), parity read from (3^s r + b)/2^j ----
def table_A(k=K):
    tab = {}
    for r in range(2**k):
        s, b, found = 0, 0, None
        for j in range(0, k):
            num = 3**s * r + b
            assert num % 2**j == 0
            odd = (num >> j) & 1            # parity of T^j(r); depends only on r mod 2^(j+1)
            if odd: s, b = s+1, 3*b + 2**j
            # even: s,b unchanged
            jj = j+1
            D = 2**jj - 3**s
            if D > 0:
                found = (jj, s, b, D, b//D + 1)   # least n with n > b/D
                break
        tab[r] = found
    return tab

# ---- Implementation B: direct orbit simulation of representative, b solved from T^j(r) ----
def table_B(k=K):
    tab = {}
    for r in range(2**k):
        x, s, found = r, 0, None
        for jj in range(1, k+1):
            if x % 2: s += 1
            x = T(x)
            if 2**jj > 3**s:
                b = 2**jj * x - 3**s * r
                D = 2**jj - 3**s
                found = (jj, s, b, D, b//D + 1)
                break
        tab[r] = found
    return tab

def main():
    A, B = table_A(), table_B()
    assert A == B, "implementations disagree"
    print("A==B on all", 2**K, "residues")
    # classes by (j, r mod 2^j)
    cls = {}
    for r, f in A.items():
        if f: cls.setdefault((f[0], r % 2**f[0]), f)
    cnt = Counter(f[0] if f else None for f in A.values())
    print("residues r mod 4096 with coefficient-stop j<=12:", sum(v for k_, v in cnt.items() if k_), "of 4096")
    print("no stop within 12:", cnt[None])
    print("distribution of earliest j:", dict(sorted((k_, v) for k_, v in cnt.items() if k_)))
    print("distinct (j, class mod 2^j):", len(cls), " (these are the maximal-prefix classes)")
    print("max threshold:", max(f[4] for f in cls.values()), " at", max(cls.items(), key=lambda kv: kv[1][4]))
    # sanity: classes with j<=12 should partition fraction of Z; measure
    from fractions import Fraction
    print("density covered by coefficient-stop classes:", sum(Fraction(1, 2**j) for (j, c) in cls))
    unst = [r for r, f in A.items() if f is None]
    print("unstopped residues:", len(unst), "e.g. 4095 in it:", 4095 in unst)

    # ---- tests on 2<=n<=100000 ----
    N = 100000; bad = 0; early = 0; checked = 0; nodesc = 0
    for n in range(2, N+1):
        f = A[n % 2**K]
        # (a) exact closed form + parity branches for first 12 steps
        x, s, odds = n, 0, []
        for j in range(K):
            odds.append(x % 2); x = T(x)
        # verify T^j formula along the way using recurrence for j<=12
        s, b, x = 0, 0, n
        for j in range(K):
            assert x * 2**j == 3**s * n + b, (n, j)
            if x % 2: s, b = s+1, 3*b + 2**j
            x = T(x)
        assert x * 2**K == 3**s * n + b
        if f:
            j, s_, b_, D, thr = f
            y = n
            for _ in range(j): y = T(y)
            assert y * 2**j == 3**s_ * n + b_
            if n >= thr:
                checked += 1
                if not y < n: bad += 1
            else:
                if y >= n: nodesc += 1       # below threshold, formula doesn't give descent
                else: early += 1             # below threshold yet still descended at j (allowed)
    print(f"n in [2,{N}]: formula/branch asserts passed; n>=thr cases {checked}, violations {bad};"
          f" n<thr: no descent at j {nodesc}, descended anyway {early}")
    # ---- boundary: for every class, n just above and at/below b/D (exact rational test) ----
    bb = 0; nb = 0
    for (j, c), (jj, s_, b_, D, thr) in cls.items():
        # smallest n>=1 with n == c mod 2^j and n >= thr ; largest n <= b/D (i.e. n < thr) in class
        n0 = c + ((thr - c + 2**j - 1)//2**j)*2**j if thr > c else c
        while n0 < thr: n0 += 2**j
        while n0 - 2**j >= thr: n0 -= 2**j
        n1 = n0 - 2**j
        if n0 >= 1:
            y = n0
            for _ in range(j): y = T(y)
            assert y < n0, ("above-threshold failure", j, c, n0); nb += 1
        if n1 >= 1:
            y = n1
            for _ in range(j): y = T(y)
            assert y >= n1, ("below-threshold unexpected descent", j, c, n1); nb += 1
        # equality case n = b/D exactly
        if b_ % D == 0 and (b_//D) % 2**j == c and b_//D >= 1:
            y = b_//D
            for _ in range(j): y = T(y)
            assert y == b_//D
            bb += 1
    print("boundary checks passed:", nb, "; exact-equality fixed-point cases (T^j(n)=n):", bb)
    # ---- Task 2: n=2^m-1 ----
    print("Task2: closed form T^j(2^m-1)=3^j 2^(m-j)-1 (0<=j<=m); first descent time:")
    out = []
    for m in range(2, 61):
        n = 2**m - 1; x = n
        for j in range(1, m+1):
            x = T(x); assert x == 3**j * 2**(m-j) - 1 and x > n
        t = 0; x = n
        while x >= n:
            x = T(x); t += 1
        out.append((m, t))
    print(out)
    print("min over m of t-m:", min(t-m for m, t in out), " max:", max(t-m for m, t in out))
    # also sigma_infinity for all n<=2^22: max stopping time
    best = (0, 0)
    for n in range(2, 2**22):
        x, t = n, 0
        while x >= n: x = T(x); t += 1
        if t > best[0]: best = (t, n)
    print("max first-descent time for 2<=n<2^22:", best)
main()
