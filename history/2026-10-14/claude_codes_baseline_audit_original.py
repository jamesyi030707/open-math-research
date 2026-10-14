#!/usr/bin/env python3
"""Exact audit (no search): single-column replacement on [64,11,26] codes obtained from the extended cyclic [65,13,25] code (GF(2), x^65-1 over GF(2)).
Rebuilds the cyclic code from cyclotomic cosets mod 65 (check polynomial (x+1)*minpoly), extends by parity, shortens at a coordinate pair, and tests the
necessary AND sufficient condition for replacing coordinate i by a new column (all extended weights are even, so the shortened code has no weight 27):
  every weight-26 word has w_i = 0  and  some linear functional f has f(w)=1 on all weight-26 words (affine-hyperplane / GF(2) consistency)."""
import time
t0 = time.time(); pc = lambda x: bin(x).count("1")
def primitive():
    for p in range(0x1001, 0x2000, 2):
        e = 1; order = None
        for i in range(1, 4096):
            e <<= 1
            if e & 0x1000: e ^= p
            if e == 1: order = i; break
        if order == 4095: return p
P = primitive(); EXP = [1] * 4095; LOG = {}
e = 1
for i in range(4095):
    EXP[i] = e; LOG[e] = i; e <<= 1
    if e & 0x1000: e ^= P
mul = lambda a, b: 0 if a == 0 or b == 0 else EXP[(LOG[a] + LOG[b]) % 4095]
def minpoly(coset):
    pol = [1]
    for c in coset:
        r = EXP[(63 * c) % 4095]; new = [0] * (len(pol) + 1)
        for i, co in enumerate(pol):
            new[i + 1] ^= co; new[i] ^= mul(co, r)
        pol = new
    assert all(x in (0, 1) for x in pol); return sum(b << i for i, b in enumerate(pol))
def pmul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        a <<= 1; b >>= 1
    return r
def pdiv(a, b):
    q = 0
    while a.bit_length() >= b.bit_length():
        s = a.bit_length() - b.bit_length(); q |= 1 << s; a ^= b << s
    assert a == 0; return q
seen = set(); cos = []
for s in range(65):
    if s in seen: continue
    C = sorted({(s << i) % 65 for i in range(12)}); seen |= set(C); cos.append((s, C))
print("cyclotomic coset sizes mod 65:", sorted(len(C) for _, C in cos))
best = None
for s, C in cos:
    if len(C) != 12: continue
    h = pmul(0b11, minpoly(C)); g = pdiv((1 << 65) | 1, h); rows = [g << i for i in range(13)]
    cw = [0] * 8192
    for m in range(1, 8192):
        low = m & -m; cw[m] = cw[m ^ low] ^ rows[low.bit_length() - 1]
    d = min(pc(x) for x in cw[1:]); print(f"coset rep {s}: [65,13] cyclic d={d}")
    if d == 25 and best is None: best = cw
ext = [x | ((pc(x) & 1) << 65) for x in best]
def consistent(vecs):
    basis = {}
    for m in vecs:
        r = m | (1 << 13)
        while r & 0x1FFF:
            p = (r & 0x1FFF).bit_length() - 1
            if p in basis: r ^= basis[p]
            else: basis[p] = r; break
        else:
            if r: return None
    u = 0
    for p in sorted(basis):
        row = basis[p]; u |= (((row >> 13) & 1) ^ (pc(row & 0x1FFF & ~(1 << p) & u) & 1)) << p
    return u
print("pair(i,j)  d  A26  |union supp|  free coords  hyperplane-consistent  triple w1+w2=w3 in W26")
pairs = [(65, 0)] + [(0, dl) for dl in range(1, 33)]; feasible = 0
for (i, j) in pairs:
    sel = [m for m in range(1, 8192) if not (ext[m] >> i) & 1 and not (ext[m] >> j) & 1]; assert len(sel) == 2047
    d = min(pc(ext[m]) for m in sel); W = [m for m in sel if pc(ext[m]) == 26]
    OR = 0
    for m in W: OR |= ext[m]
    rem = [x for x in range(66) if x not in (i, j)]; free = [x for x in rem if not (OR >> x) & 1]
    u = consistent(W); Ws = set(W); triple = any((a ^ b) in Ws for a in W for b in W if a < b)
    print(f"({i:2d},{j:2d})  {d}  {len(W):4d}  {len(rem) - len(free):3d}/64      {len(free):3d}          {'yes' if u is not None else 'NO '}                  {triple}")
    if free and u is not None: feasible += 1; print("   >>> candidate replacement exists; verify directly before believing it")
# r-column generalisation (exact): a deletion set D can only work if no weight-26 support contains D (gain <= r - |supp(w) & D| must be >= 1)
import itertools
def free_sets(Wm, rem, r):
    return sum(1 for D in itertools.combinations(rem, r) if not any(all((w >> x) & 1 for x in D) for w in Wm))
tot2 = 0
for (i, j) in pairs:
    Wm = [ext[m] for m in range(1, 8192) if not (ext[m] >> i) & 1 and not (ext[m] >> j) & 1 and pc(ext[m]) == 26]
    rem = [x for x in range(66) if x not in (i, j)]; tot2 += free_sets(Wm, rem, 2)
print("r=2: deletion pairs contained in NO weight-26 support, summed over the 33 baselines:", tot2)
for (i, j) in pairs[:2]:
    Wm = [ext[m] for m in range(1, 8192) if not (ext[m] >> i) & 1 and not (ext[m] >> j) & 1 and pc(ext[m]) == 26]
    rem = [x for x in range(66) if x not in (i, j)]
    print(f"r=3, baseline ({i},{j}): deletion triples contained in NO weight-26 support:", free_sets(Wm, rem, 3), "of", len(list(itertools.combinations(rem, 3))))
print("pairs passing both necessary tests:", feasible, "of", len(pairs), f"({time.time()-t0:.1f}s)")
