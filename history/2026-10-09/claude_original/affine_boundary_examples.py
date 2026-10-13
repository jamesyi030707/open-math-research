#!/usr/bin/env python3
"""
Part B.  For a parity word of length j with s odd steps and class r mod 2^j:
   T^j(n) = (3^s n + b)/2^j  for every n = r (mod 2^j), with integer b >= 0.
   T^j(n) < n   <=>   b < (2^j - 3^s) * n          (multiply by 2^j; exact, strict)
 Consequences (general j, paper proof):  D := 2^j - 3^s  is never 0 for j>=1;  D<0 => T^j(n) > n for all n>=1;
 D>0 => descent iff n > b/D.  "slope 3^s/2^j < 1" (i.e. D>0) alone does NOT give descent for a given n.
Boundary: n=1, word (1,0) [class 1 mod 4], s=1, b=1, D=1: slope 3/4 < 1 but T^2(1)=1 (not < 1; T^2(1)=1 is the cycle 1->2->1).
This script derives (s,b) by DIRECT SIMULATION (b = 2^j T^j(n) - 3^s n) and checks the iff for all 1<=n<=4095, 1<=j<=12.
"""
def T(n): return n // 2 if n % 2 == 0 else (3 * n + 1) // 2

def sb(n, j):
    x = n; s = 0
    for _ in range(j):
        s += x & 1; x = T(x)
    return s, (1 << j) * x - 3 ** s * n, x          # s, b, T^j(n)

def main():
    print("== boundary examples ==")
    for n, j in ((1, 2), (2, 2)):
        s, b, x = sb(n, j); D = (1 << j) - 3 ** s
        print(f"  n={n}, j={j}: s={s}, b={b}, D=2^j-3^s={D} (slope {3**s}/{2**j} < 1: {D>0}); "
              f"b < D*n ? {b} < {D*n} -> {b < D*n};  T^j(n) = {x} ({'<' if x < n else '>='} n)")
    print("  n=5 (same class as n=1 mod 4): j=2:", sb(5, 2), "-> T^2(5) =", sb(5, 2)[2], "< 5")
    print("== exact iff over 1<=n<=4095, 1<=j<=12:  T^j(n)<n  <=>  D>0 and b < D*n ==")
    mism = 0; slope_lt1_nodrop = 0; ex_with_earlier = 0; ex_without_earlier = 0; first_ex = []
    total = 0
    for n in range(1, 4096):
        earlier = False
        for j in range(1, 13):
            s, b, x = sb(n, j); D = (1 << j) - 3 ** s
            assert D != 0 and b >= 0
            lhs = x < n; rhs = (D > 0 and b < D * n)
            total += 1
            if lhs != rhs: mism += 1
            if D > 0 and not lhs:
                slope_lt1_nodrop += 1
                if earlier: ex_with_earlier += 1
                else:
                    ex_without_earlier += 1
                    if n >= 2: first_ex.append((n, j))
                if len(first_ex) < 0: pass
            earlier = earlier or lhs
    print(f"  pairs tested: {total}; iff mismatches: {mism}")
    print(f"  pairs with slope<1 (D>0) but NO strict descent at that j: {slope_lt1_nodrop}")
    print(f"     of which a strict descent happened at an EARLIER j': {ex_with_earlier}")
    print(f"     of which no earlier descent: {ex_without_earlier}   (n>=2 among these: {first_ex[:5]};  the only ones should be n=1)")
    s, b, x = sb(2, 2)
    print(f"  example with earlier descent: n=2: T(2)=1<2 at j=1, but at j=2: D=1>0, b={b}, b<D*n? {b} < {2} -> False; T^2(2)={x}")
    assert mism == 0

if __name__ == "__main__":
    main()
