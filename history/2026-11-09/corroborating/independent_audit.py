#!/usr/bin/env python3
"""Independent coordinate-level audit of the fixed-residual q=28 obstruction.

Standard library only. The row data are the archived residual input (Git blob
8f76beaa5994563a2980ea9cb87412640d6560b4). No generator/checker is imported.
All calculations are exact. Runtime is bounded externally by timeout 60s.
"""
import itertools
import json
from collections import Counter

R = [0x17e7146801, 0x6293dc808, 0xf714c2017, 0x35dfc802d,
     0xb1f3485c, 0x63e6a0ae, 0x65be14f, 0x196fc233, 0x3e690ce6, 0xcb73897]

def dot(a, b, dimension):
    return sum(((a // (2**i)) % 2) * ((b // (2**i)) % 2)
               for i in range(dimension)) % 2

# Expand actual binary coordinates; do not use XOR word recurrence.
matrix = [[(row // (2**j)) % 2 for j in range(37)] for row in R]
messages = list(itertools.product((0, 1), repeat=10))
words = {}
for bits in messages:
    u = sum(bit * 2**i for i, bit in enumerate(bits))
    words[u] = tuple(sum(bits[i] * matrix[i][j] for i in range(10)) % 2
                     for j in range(37))
assert len(set(words.values())) == 1024
weights = {u: sum(w) for u, w in words.items()}
assert Counter(weights.values()) == {
    0: 1, 14: 160, 16: 142, 18: 320, 20: 160, 22: 160, 24: 80, 32: 1}
assert [u for u, w in weights.items() if w == 32] == [1008]
assert all(weights[s << 4] == weights[(s << 4) ^ 1008] == 16
           for s in range(1, 32))
planes = sorted({tuple(sorted((0, a, b, a ^ b)))
                 for a in range(1, 32) for b in range(a+1, 32)})
assert len(planes) == 155
F = (2, 3, 5, 6, 8, 9, 10, 11, 12, 14)
E = (1, 4, 7, 13, 15)
expected = {2:(22,0),3:(26,0),5:(8,0),6:(13,1),8:(10,1),
            9:(19,1),10:(14,0),11:(28,0),12:(29,0),14:(23,0)}
derived = {}
plane_types = {}
for t in range(1,16):
    allowed = []
    for s in range(32):
        u = t + 16*s
        r, r1 = weights[u], weights[u ^ 1008]
        allowed.append(tuple(a for a in range(28)
            if 27-r <= a <= r and 27-r1 <= a <= r1
            and (a+r) % 4 == (a+r1) % 4 == 0))
    if t not in F:
        assert Counter(allowed) == {(12,16):16, (8,12,16,20):16}
        continue
    assert Counter(allowed) == {(14,):16,(10,14,18):16}
    fixed = tuple(x == (14,) for x in allowed)
    fits = [(v,c) for v in range(1,32) for c in (0,1)
            if all(fixed[s] == (dot(v,s,5) == c) for s in range(32))]
    assert len(fits) == 1
    derived[t] = fits[0]
    assert fits[0] == expected[t]
    v, c = fits[0]
    counts = Counter()
    for K in planes:
        blocks = {tuple(sorted(s ^ k for k in K)) for s in range(32)}
        assert len(blocks) == 8
        numbers = sorted(sum(fixed[s] for s in block) for block in blocks)
        if all(dot(v,k,5) == 0 for k in K):
            assert numbers == [0]*4 + [4]*4
            counts["contained"] += 1
        else:
            assert numbers == [2]*8
            counts["transverse"] += 1
    assert counts == {"contained":35,"transverse":120}
    plane_types[t] = dict(counts)

# Independent direct moment counts for the 16 variable positions.
moment_solutions = {}
for z in range(4):
    sols = []
    for n10 in range(17):
        for n18 in range(17-n10):
            n14 = 16-n10-n18
            total = 16*14 + 10*n10 + 14*n14 + 18*n18
            energy = (16+n14)*(14-12-z)**2 + n10*(10-12-z)**2 + n18*(18-12-z)**2
            if total == 384+32*z and energy == 192:
                sols.append((n10,n14,n18))
    moment_solutions[z] = sols
assert moment_solutions == {0:[],1:[(11,2,3)],2:[(6,4,6)],3:[(3,2,11)]}
block_energies = {}
for z in (1,3):
    pairs = [(a,b) for a in (10,14,18) for b in (10,14,18)
             if 28+a+b == 48+4*z]
    energies = {2*(14-12-z)**2 + (a-12-z)**2 + (b-12-z)**2 for a,b in pairs}
    assert energies == {12}
    block_energies[z] = sorted(energies)
assert 8*12 != 192

# Verify q=28 classified active columns and character identities for EVERY plane.
for K in planes:
    active = [v for v in range(32) if any(dot(v,k,5) for k in K)]
    assert len(active) == 24
    chars = [[(-1)**dot(s,v,5) for s in range(32)] for v in active]
    assert all(sum(c) == 0 for c in chars)
    for i in range(24):
        for j in range(i,24):
            assert sum(a*b for a,b in zip(chars[i],chars[j])) == (32 if i == j else 0)
    blocks = {tuple(sorted(s ^ k for k in K)) for s in range(32)}
    assert all(sum(c[s] for s in block) == 0 for c in chars for block in blocks)
    local = [sum(dot(s,v,5) for v in active) for s in range(32)]
    assert Counter(local) == {0:1,12:28,16:3}

# All ordered maps, distinct from the unordered-triple generator.
hist = Counter()
for columns in itertools.product(range(16), repeat=3):
    satisfied = sum(sum(dot(t,c,4) for c in columns) == 2 for t in F)
    hist[satisfied] += 1
assert sum(hist.values()) == 4096 and hist[10] == 0
assert {a ^ b for a,b in itertools.combinations(E,2)} == set(F)
assert {sum(1 << i for i in range(4) if dot(t,1 << i,4)) for t in F} == set(F)

print(json.dumps({
    "verified": True,
    "residual_messages_checked":1024,
    "hyperplanes":derived,
    "plane_count":155,
    "hyperplane_plane_types":plane_types,
    "full_moment_solutions_n10_n14_n18":moment_solutions,
    "transverse_block_energies":block_energies,
    "ordered_linear_maps_checked":4096,
    "satisfied_forced_positions_histogram":dict(sorted(hist.items())),
    "scope":"Only archived residual/kernel-one q=28; q16,20,24 and global target remain unresolved."
}, indent=2, sort_keys=True))
