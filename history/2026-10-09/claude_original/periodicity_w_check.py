#!/usr/bin/env python3
"""
Part A.  w(m) = (3^m-1)/2^{v}, v = v2(3^m-1) (so w is odd).  W_L(m) = first L branches (parities of w, T(w), ...).

RETRACTED (false):  "W_L(m) depends only on m mod 2^(L-1)"   (counterexample: L=3, m=2 vs 6).
CORRECTED (proved on paper, see header comments below; this script only checks FINITE instances):

 Lemma O.  For k>=1: 3^(2^k) = 1 (mod 2^(k+2)).  Induction: k=1: 9=1 (mod 8). If 3^(2^k)=1+2^(k+2)a then
           squaring gives 1+2^(k+3)a+2^(2k+4)a^2 = 1 (mod 2^(k+3)).  Hence m = m' (mod 2^k), k>=1  =>  3^m = 3^m' (mod 2^(k+2)).
 Lemma V.  v2(3^m-1) = 1 (m odd); = 2+v2(m) (m even).
 Lemma A.  Theorem A (branches of x depend only on x mod 2^L) => W_L(m) is determined by w mod 2^L.

 Prop. (sufficient moduli; NOT claimed minimal)
   m odd , L>=2 :  W_L depends only on m mod 2^(L-1).      [v=1; w mod 2^L <- 3^m mod 2^(L+1); Lemma O with k=L-1>=1]
   m odd , L=1  :  W_1 = (1) always (w is odd).
   m even, e=v2(m)>=1, any L>=1:  W_L depends only on (e, m mod 2^(e+L)).   [v=e+2 fixed by e; w mod 2^L <- 3^m mod 2^(e+L+2); Lemma O with k=e+L>=2]
   Unnormalised x=3^m-1, L>=3: first L branches of x depend on m mod 2^(L-2); word(x) = 0^v followed by word(w) (when L>v).
 The even-m statement is the point: the earlier claim ignored that v depends on e.
"""
import random

def T(n): return n // 2 if n % 2 == 0 else (3 * n + 1) // 2
def v2(x):
    return (x & -x).bit_length() - 1
def word(x, L):
    w = []
    for _ in range(L): w.append(x & 1); x = T(x)
    return tuple(w)
def w_of(m):
    x = 3 ** m - 1; v = v2(x); return x >> v, v, x

def modexp(m, L):
    """exponent a with sufficient modulus 2^a for W_L(m) (within the stratum of m); None if W_L is constant"""
    if m % 2: return None if L <= 2 else L - 1
    return v2(m) + L

def main():
    print("== 1. counterexamples to the retracted claim ==")
    for L in (2, 3):
        for m in (2, 6):
            w, v, x = w_of(m)
            print(f"  L={L} m={m}: 3^m-1={x} = 2^{v} * {w},  w mod 8 = {w % 8},  W_L = {''.join(map(str, word(w, L)))}   (m mod 2^(L-1) = {m % 2**(L-1)})")
    print("  m=2 and m=6 are congruent mod 4 but W_3 = 101 vs 110 (and W_2 = 10 vs 11).")
    print("  e=v2(m)=1 for both; corrected modulus 2^(e+L) = 16 separates them (2 != 6 mod 16).")

    print("== 2. table: v2(3^m-1) formula (Lemma V), m=1..40 ==")
    assert all(v2(3 ** m - 1) == (1 if m % 2 else 2 + v2(m)) for m in range(1, 41))
    print("  verified m=1..40")

    print("== 3. corrected statement: grouped check m=1..3000, L=1..10 ==")
    M = 3000
    ws = {m: w_of(m)[0] for m in range(1, M + 1)}
    for L in range(1, 11):
        groups = {}
        for m in range(1, M + 1):
            a = modexp(m, L)
            key = ('odd', 0 if a is None else m % 2 ** a) if m % 2 else ('even', v2(m), m % 2 ** a)
            groups.setdefault(key, set()).add(word(ws[m], L))
        multi = sum(1 for k, s in groups.items() if len(s) > 1)
        nontriv = sum(1 for m in range(1, M + 1))  # all m belong to some group
        print(f"  L={L:2d}: groups={len(groups):5d}, groups with 2+ different words under CORRECTED key: {multi}")
        assert multi == 0
    print("  (large e+L makes most groups singletons; step 4 tests shifted pairs explicitly)")

    print("== 4. targeted shifted pairs: m' = m + t*2^a  (a = corrected exponent), and the RETRACTED shift 2^(L-1) ==")
    ok_pairs = 0; orig_bad = 0; orig_pairs = 0; orig_bad_examples = []
    for L in range(1, 9):
        for m in range(1, 401):
            a = modexp(m, L)
            if a is None: shifts = [2, 4, 6]            # W_L constant for odd m, L<=2; keep parity
            else:
                if a > 12: continue
                shifts = [2 ** a * t for t in (1, 2, 3)]
            for sh in shifts:
                mp = m + sh
                assert (mp % 2 == m % 2) and (m % 2 or v2(mp) == v2(m))   # same stratum
                assert word(w_of(m)[0], L) == word(w_of(mp)[0], L), (L, m, mp)
                ok_pairs += 1
            if L >= 2:                                    # retracted claim: shift by 2^(L-1) only
                mp = m + 2 ** (L - 1)
                if mp <= 20000 and (mp % 2 == m % 2):
                    orig_pairs += 1
                    if word(w_of(m)[0], L) != word(w_of(mp)[0], L):
                        orig_bad += 1
                        if len(orig_bad_examples) < 5: orig_bad_examples.append((L, m, mp))
    print(f"  corrected-modulus shifted pairs checked: {ok_pairs}, all equal")
    print(f"  retracted-claim pairs (same parity, shift 2^(L-1)): {orig_pairs}, with DIFFERENT words: {orig_bad}; first examples (L,m,m'): {orig_bad_examples}")

    print("== 5. unnormalised remark: x=3^m-1 ==")
    bad = 0
    for m in range(1, 201):
        w, v, x = w_of(m)
        for L in range(1, 13):
            if L > v:
                if word(x, L) != (0,) * v + word(w, L - v): bad += 1
            else:
                if word(x, L) != (0,) * L: bad += 1
    print(f"  word(x)=0^v + word(w): violations {bad}")
    bad = 0
    for L in range(3, 11):
        by = {}
        for m in range(1, 1500):
            by.setdefault(m % 2 ** (L - 2), set()).add(word(3 ** m - 1, L))
        bad += sum(1 for s in by.values() if len(s) > 1)
    print(f"  first L branches of x depend on m mod 2^(L-2) (L=3..10, m<1500): violating groups {bad}")
    print("DONE (finite checks of statements proved on paper; not a proof by themselves)")

if __name__ == "__main__":
    main()
