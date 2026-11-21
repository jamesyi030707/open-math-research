"""Exact reproduction of ten honest local controls and their actual sections."""
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

B = (0x17e7146801, 0x6293dc808, 0xf714c2017, 0x35dfc802d,
     0xb1f3485c, 0x63e6a0ae, 0x65be14f, 0x196fc233,
     0x3e690ce6, 0xcb73897)

def verify(test, label):
    if not test:
        raise ValueError(label)

def chi(t, v):
    return 1 - 2 * ((t & v).bit_count() % 2)

def residual_weight(word):
    row = 0
    for i, bits in enumerate(B):
        if word >> i & 1:
            row ^= bits
    return row.bit_count()

def w(t):
    return ((t & 31) << 4) ^ (1008 if t & 32 else 0)

def swap(v, i, j):
    return v ^ ((1 << i) ^ (1 << j)) if ((v >> i) ^ (v >> j)) & 1 else v

def key(cols):
    return tuple(sorted(cols))

def translate(cols, shift):
    return key(v ^ (shift if v & 32 else 0) for v in cols)

def signed_dp(vectors):
    points = {(0, 0)}
    for a, b in vectors:
        if a or b:
            points = {(x + e*a, y + e*b) for x, y in points for e in (-1, 1)}
    return points

def main():
    path = (Path(sys.argv[1]) if len(sys.argv) == 2 else
            Path(__file__).resolve().parent.parent / '2026-11-15/h.json')
    solutions = json.loads(path.read_text())['solutions']
    columns = solutions[1]['columns']
    prior = {translate(s['columns'], u) for s in solutions for u in range(32)}
    verify(len(solutions) == 277 and len(prior) == 8408, 'old explicit transport set')
    H = {a: [t for t in range(64) if residual_weight(a ^ w(t)) == 14]
         for a in range(1, 16)}
    actual_sections = {a: h for a, h in H.items() if h}
    verify(list(actual_sections) == [2,3,5,6,8,9,10,11,12,14], 'minimum sections')
    by_swap = []
    for i, j in combinations(range(5), 2):
        c = [swap(v, i, j) for v in columns]
        local = [sum((t & v).bit_count() % 2 for v in c) for t in range(64)]
        for t in range(1, 64):
            b, x = residual_weight(w(t)), local[t]
            verify(27-b <= x <= b and (b+x) % 4 == 0 and x != 0, ('local',i,j,t))
        E = [t for t in range(1, 32) if local[t] == 16]
        r, z = sum(v >> 5 for v in c), c.count(32)
        a0, maxb = c.count(0), max(Counter(v & 31 for v in c if v & 32).values())
        qt = {translate(c, t) for t in range(32)
              if a0 + c.count(32 + t) == 2}
        verify(len(E) == 7 and (r,z,a0,maxb) == (4,1,1,1) and qt == {key(c)},
               'q24; survives old multiplicity filter; unique q24 pattern in orbit')
        rejected = []
        scalar_fail = []
        for a, h in actual_sections.items():
            m = [[chi(t, v) for v in c] for t in h]
            targets = [-sum(chi(t, k) for t in h) for k in (0, 1)]
            coef = [[sum(chi(t, k)*m[l][n] for l, t in enumerate(h))
                     for n in range(27)] for k in (0, 1)]
            verify(all(v % 4 == 0 for v in targets+coef[0]+coef[1]), 'scaling')
            target = tuple(v//4 for v in targets)
            active = [[n, u//4, v//4] for n, (u,v) in enumerate(zip(*coef)) if u or v]
            points = signed_dp([(u,v) for _,u,v in active])
            px, py = {x for x,y in points}, {y for x,y in points}
            if target[0] not in px or target[1] not in py:
                scalar_fail.append(a)
            if target not in points:
                rejected.append(dict(a=a, active=active, target_div4=target,
                                     reachable_count=len(points),
                                     target_y_slice=sorted(x for x,y in points if y == target[1])))
        witness = min(rejected, key=lambda x: (len(x['active']), x['a']))
        by_swap.append(dict(swap=[i,j], columns=c, E=E, in_old_transport=key(c) in prior,
                            is_original_pattern=key(c) == key(columns),
                            old_multiplicity=[a0,maxb], scalar_failures=scalar_fail,
                            rejecting_sections=[x['a'] for x in rejected], witness=witness))
    verify(len({key(x['columns']) for x in by_swap}) == 10, 'ten distinct restrictions')
    new = [x for x in by_swap if not x['in_old_transport']]
    verify([x['swap'] for x in new] == [[0,2],[0,3],[0,4],[1,2],[1,3],[1,4]], 'new six')
    verify(all(not x['scalar_failures'] for x in by_swap), 'both coordinates pass alone')
    verify(all(x['witness']['target_div4'] == (-4,0) and
               x['witness']['target_y_slice'] == [-8,0,8] for x in new), 'six joint slices')
    isolated_specs = [(1,6,-1,14),(2,10,1,12),(2,5,1,11),
                      (4,5,1,12),(2,5,1,15),(1,6,-1,14)]
    h = actual_sections[2]
    f = [sum(chi(t,v) for t in h) for v in range(64)]
    for x, (u,v,s,j) in zip(new, isolated_specs):
        c = x['columns']
        # This recomputes the actual section; no substitution of local GL into B.
        rows = [[f[k^d] for d in c] for k in (u,v)]
        rhs = [-f[u],-f[v]]
        summed = [p+s*q for p,q in zip(*rows)]
        verify(rhs[0]+s*rhs[1] == 0 and
               summed == [16*(k==j) for k in range(27)], 'one-column isolation')
        x['isolated_column_certificate'] = dict(
            a=2, characters=[u,v], combine_sign=s, rhs=rhs, rows=rows,
            forced_column_index=j, coefficient=16)
    print(json.dumps(dict(seed=1, old_transport_count=len(prior),
                          minimum_sections=actual_sections, examined=by_swap,
                          new_relative_to_named_prior_certificates=len(new)), indent=2))

if __name__ == '__main__':
    main()
