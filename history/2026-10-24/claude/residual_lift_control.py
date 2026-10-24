#!/usr/bin/env python3
"""Residual-lift criterion, tiny controls (NOT a target-code claim).  Code C = < c0=(1^w|0^(n-w)), rows (A_i|B_i) >, d(C)>=d=w.
Criterion: for every u != 0, with s=wt(uA), t=wt(uB):  w-t <= s <= t   (pair (uA,uB) and (uA+1,uB)).  Checked against direct minimum distance on random small instances (w=d=3, n=7, k=4)."""
import random
pc = lambda x: bin(x).count("1")
def direct_min(w, nb, A, B):                       # A rows: w-bit ints, B rows: nb-bit ints; words as (a<<nb)|b with a as w-bit
    k1 = len(A); best = 10**9; full = (1 << w) - 1
    for lam in (0, 1):
        for u in range(1 << k1):
            if lam == 0 and u == 0: continue
            a = 0; b = 0
            for i in range(k1):
                if (u >> i) & 1: a ^= A[i]; b ^= B[i]
            if lam: a ^= full
            best = min(best, pc(a) + pc(b))
    return best
def criterion(w, A, B):
    k1 = len(A)
    for u in range(1, 1 << k1):
        a = b = 0
        for i in range(k1):
            if (u >> i) & 1: a ^= A[i]; b ^= B[i]
        s, t = pc(a), pc(b)
        if not (w - t <= s <= t): return False
    return True
random.seed(31); w, nb = 3, 4; agree = pos = neg = 0; N = 120000
for _ in range(N):
    A = [random.getrandbits(w) for _ in range(3)]; B = [random.getrandbits(nb) for _ in range(3)]
    c = criterion(w, A, B); dd = direct_min(w, nb, A, B) >= w and w >= 3
    agree += c == dd; pos += c; neg += not c
print(f"random (A,B) pairs: {N}; criterion <=> d(C)>=3 agree: {agree}/{N}; criterion true: {pos}, false: {neg}")
# Hamming [7,4,3] derived positive control: rows G=[I4|P], c0 = row0 (weight 3), complement rows 1..3; coordinates permuted so supp(c0) first
P = [[1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]]
rows = [[1 if j == i else 0 for j in range(4)] + P[i] for i in range(4)]; c0 = rows[0]; supp = [j for j in range(7) if c0[j]]; order = supp + [j for j in range(7) if j not in supp]
assert len(supp) == 3
tomask = lambda bits: sum(b << i for i, b in enumerate(bits))
A = [tomask([rows[i][j] for j in order[:3]]) for i in (1, 2, 3)]; B = [tomask([rows[i][j] for j in order[3:]]) for i in (1, 2, 3)]
def words_B():
    out = []
    for u in range(1, 8):
        b = 0
        for i in range(3):
            if (u >> i) & 1: b ^= B[i]
        out.append((u, b))
    return out
def s_of(u):
    a = 0
    for i in range(3):
        if (u >> i) & 1: a ^= A[i]
    return pc(a)
rho = [pc(a) & 1 for a in A]
t2 = [(u, pc(b)) for u, b in words_B()]; W2 = [u for u, t in t2 if t == 2]
print("Hamming control: criterion:", criterion(3, A, B), "| direct min distance:", direct_min(3, 4, A, B), "| residual B dimension 3, min weight", min(t for _, t in t2))
print("   weight-2 residual words:", len(W2), "| wt(uA) in {1,2} for all of them:", all(s_of(u) in (1, 2) for u in W2), "| parity wt(uA)=u.rho (mod 2) for all u:", all(s_of(u) % 2 == sum(((u >> i) & 1) * rho[i] for i in range(3)) % 2 for u in range(1, 8)))
cnt3 = 0
for lam in (0, 1):
    for u in range(1, 8):
        a = b = 0
        for i in range(3):
            if (u >> i) & 1: a ^= A[i]; b ^= B[i]
        if lam: a ^= 7
        cnt3 += pc(a) + pc(b) == 3
print("   A_3(C) =", cnt3 + 1, " >= 1 + A_2(B) =", 1 + len(W2), "(each weight-t_min residual word gives one weight-w and one weight-(w+1) word)")
A_bad = A[:]; A_bad[0] ^= 1                         # negative control: flip one entry of A
Wbad = [u for u in W2 if s_of(u) in (1, 2)]
def s_bad(u):
    a = 0
    for i in range(3):
        if (u >> i) & 1: a ^= A_bad[i]
    return pc(a)
print("negative control (one flipped bit of A): criterion:", criterion(3, A_bad, B), "| direct min distance:", direct_min(3, 4, A_bad, B), "| some weight-2 word has wt(uA) outside {1,2}:", any(s_bad(u) not in (1, 2) for u in W2))
