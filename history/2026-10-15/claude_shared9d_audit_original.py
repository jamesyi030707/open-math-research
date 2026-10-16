#!/usr/bin/env python3
"""Exact audit of the shared-subcode route for the fixed [64,11,26] baseline (11 hex rows from the user; bit0 = coordinate 1; message bit i selects row i).
All weights are even, so a subcode H has d>=27 iff it contains NO weight-26 word.  No dependencies; process-time guard 110 s.
(1) rebuild code, check weight distribution + rank 11;  (2) dimension-10 H = ker(a): min #W26 in H;
(3) ALL 698,027 dimension-9 H = ker(a,b) with canonical a<b<a^b: histogram of #W26 messages in H;
(4) all-W26 subspaces (every nonzero element has weight 26): counts per dimension, maximal dimension, explicit certificate.
Why (4) matters: if U is an all-W26 subspace of dimension k, every subcode H of codimension c<=k-1 meets U in dimension >= k-c >= 1, hence contains a weight-26 word."""
import time
from collections import Counter
T0 = time.process_time(); LIMIT = 110.0
def ok(): return time.process_time() - T0 < LIMIT
rows = [int(h, 16) for h in "0023cba93f2574f1 00645cfb416f9d13 00eb725fbdfa4ed7 01f52f1644d1e95f 03c99585b686a64f 07b0e0a25228386f 0f420aed9b75042f 1ea7de7209cf7caf 3d6c774d2cbb8daf 7afb253366526faf f5d581cff381abaf".split()]
cw = [0] * 2048
for m in range(1, 2048):
    low = m & -m; cw[m] = cw[m ^ low] ^ rows[low.bit_length() - 1]
wt = [w.bit_count() for w in cw]
dist = dict(sorted(Counter(wt).items()))
assert dist == {0: 1, 26: 234, 28: 259, 30: 420, 32: 396, 34: 186, 36: 261, 38: 216, 40: 75}, dist
assert len(set(cw)) == 2048
print("weight distribution matches; all 2048 words distinct (rank 11):", dist)
W = [m for m in range(1, 2048) if wt[m] == 26]; S = set(W)
chk = [11, 32, 43]
print("user circuit messages 11,32,43: xor =", 11 ^ 32 ^ 43, "| codeword xor =", cw[11] ^ cw[32] ^ cw[43], "| weights", [wt[m] for m in chk], "| hex", [format(cw[m], "016x") for m in chk])
par = [bin(i).count("1") & 1 for i in range(2048)]
Z = [0] * 2048
for a in range(1, 2048):
    mk = 0
    for idx, m in enumerate(W):
        if not par[a & m]: mk |= 1 << idx
    Z[a] = mk
c10 = [Z[a].bit_count() for a in range(1, 2048)]
print(f"dim-10 H=ker(a): 2047 hyperplanes; min #W26 in H = {min(c10)}; hyperplanes with 0 W26 words: {c10.count(0)}")
hist = Counter(); total = 0; best = (10**9, None); zero = []; done = True
for a in range(1, 2047):
    if not ok(): done = False; break
    za = Z[a]
    for b in range(a + 1, 2048):
        if (a ^ b) <= b: continue
        k = (za & Z[b]).bit_count(); total += 1; hist[k] += 1
        if k < best[0]: best = (k, (a, b, a ^ b))
        if k == 0 and len(zero) < 3: zero.append((a, b))
print(f"dim-9 H=ker(a,b): enumerated {total} of 698027 (complete={done}); H with zero W26 words: {hist.get(0, 0)}; min #W26 in H = {best[0]} (dual subspace {best[1]}), attained by {hist[best[0]]} subspaces")
print("lowest counts (k:#H):", sorted(hist.items())[:6], "| max count:", max(hist))
levels = {}; lv = set()
for i, w1 in enumerate(W):
    for w2 in W[i + 1:]:
        if (w1 ^ w2) in S: lv.add(frozenset((0, w1, w2, w1 ^ w2)))
levels[2] = lv; k = 2; full = True
print("all-W26 subspaces: dim1 =", len(W), "| dim2 =", len(lv))
while levels[k] and ok():
    nxt = set()
    for U in levels[k]:
        for s in W:
            if s in U: continue
            if all((s ^ u) in S for u in U if u): nxt.add(U | frozenset(s ^ u for u in U))
    k += 1; levels[k] = nxt; print(f"all-W26 subspaces: dim{k} =", len(nxt))
if levels[k] == set() or not ok():
    full = levels[k] == set()
kmax = max(d for d in levels if levels[d])
U = sorted(next(iter(levels[kmax]))); basis = []; span = {0}
for x in U:
    if x and x not in span: basis.append(x); span |= {x ^ y for y in span}
words = [x for x in sorted(span) if x]
print(f"max all-W26 subspace dimension = {kmax} (search complete={full}); basis messages {basis}; {len(words)} nonzero messages; all weight 26: {all(wt[x] == 26 for x in words)}")
print("certificate hex words:", [format(cw[x], "016x") for x in words])
print(f"=> every subcode of codimension <= {kmax-1} (dimension >= {11-kmax+1}) contains a weight-26 word; process time {time.process_time()-T0:.1f}s")
