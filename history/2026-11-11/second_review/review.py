#!/usr/bin/env python3
"""Independent replay of the fixed-B parity-period obstruction; stdlib only."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import hashlib, json, time

ROOT = Path(__file__).resolve().parent

def check(condition, why):
    if not condition:
        raise RuntimeError(why)

def dot(a, b):
    return (a & b).bit_count() % 2

def row_reduce(rows):
    rows = list(rows)
    pivots = []
    for col in reversed(range(max(rows, default=0).bit_length())):
        choices = [j for j in range(len(pivots), len(rows)) if rows[j] >> col & 1]
        if not choices:
            continue
        j = choices[0]
        k = len(pivots)
        rows[k], rows[j] = rows[j], rows[k]
        for i in range(len(rows)):
            if i != k and rows[i] >> col & 1:
                rows[i] ^= rows[k]
        pivots.append(col)
    return len(pivots), rows[:len(pivots)]

def span(basis):
    points = [0]
    for b in basis:
        points += [s ^ b for s in points]
    return points

def main():
    start = time.process_time()
    raw = (ROOT / 'inputs/residual_candidate.json').read_bytes()
    check(hashlib.sha256(raw).hexdigest() == '276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80', 'Input bytes')
    B = [int(x, 16) for x in json.loads(raw)['basis_hex']]
    check(row_reduce(B)[0] == 10, 'B rank')
    words = span(B)
    weights = [x.bit_count() for x in words]
    check(len(set(words)) == 1024, 'B injectivity')
    check(Counter(weights) == {0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1}, 'B enumerator')
    heavy = [u for u in range(1024) if weights[u] >= 27]
    check(heavy == [1008], 'Unique kernel candidate')
    h = heavy[0]
    monomials = [(i,) for i in range(10)] + list(combinations(range(10), 2))
    def quadratic_eval(u):
        bits = [(u >> i) & 1 for i in range(10)]
        values = [bits[m[0]] if len(m) == 1 else bits[m[0]] * bits[m[1]] for m in monomials]
        return sum(x << i for i, x in enumerate(values))
    min_messages = [u for u in range(1024) if weights[u] == 14]
    qrank, _ = row_reduce([quadratic_eval(u) for u in min_messages])
    check(qrank == 55, 'Double-even forcing rank')
    # Independently reconstruct wt(uB)/2 as a quadratic over all messages.
    qcoef = [(B[i].bit_count() // 2) % 2 for i in range(10)]
    qcoef += [dot(B[i], B[j]) for i, j in combinations(range(10), 2)]
    coeffmask = sum(b << i for i, b in enumerate(qcoef))
    check(all(dot(coeffmask, quadratic_eval(u)) == weights[u] // 2 % 2 for u in range(1024)), 'Quadratic identity on B')
    Sbasis = [16,32,64,128,256]
    check(row_reduce(Sbasis + [h,1,2,4,8])[0] == 10, 'Direct quotient')
    S = span(Sbasis)
    check(S == [s << 4 for s in range(32)], 'Chosen S labels')
    check(set(u for u in range(1024) if weights[u] == weights[u ^ h] == 16) == set(S[1:]) | {s ^ h for s in S[1:]}, 'Exactly the 31 sixteen/sixteen pairs')
    windows = {}
    for t in range(16):
        windows[t] = []
        for s in S:
            u = t ^ s
            permitted = []
            for a in range(28):
                ok = all((27 - weights[v] <= a <= weights[v] and (a + weights[v]) % 4 == 0) for v in (u,u ^ h) if v)
                if ok and (u or a == 0):
                    permitted.append(a)
            windows[t].append(tuple(permitted))
    check(windows[0] == [(0,)] + [(12,16)] * 31, 'S allowed weights')
    found = []
    for t in range(1,16):
        for n in range(1,32):
            for c in (0,1):
                if all(windows[t][s] == ((14,) if dot(n,s) == c else (10,14,18)) for s in range(32)):
                    found.append((t,n,c))
    expected = [(2,22,0),(3,26,0),(5,8,0),(6,13,1),(8,10,1),(9,19,1),(10,14,0),(11,28,0),(12,29,0),(14,23,0)]
    check(found == expected, 'Exhaustively derived hyperplanes')
    nrank, reduced = row_reduce([n for t,n,c in found])
    check(nrank == 5 and set(span(reduced)) == set(range(32)), 'Normal span')
    # Solve the parity equations including the artificial origin f(0)=L mod2.
    equations = [1 << v ^ 1 << (v ^ n) for t,n,c in found for v in range(32)]
    check(row_reduce(equations)[0] == 31, 'Only constant parity functions survive')
    qcases = []
    for q in range(32):
        first = 12*q + 16*(31-q)
        L = Fraction(first,16)
        if L.denominator != 1 or L > 27:
            continue
        L = int(L)
        second = 12**2*q + 16**2*(31-q)
        m2 = Fraction(second,8) - L*L
        pairs = (m2-L)/2
        check(m2.denominator == pairs.denominator == 1, 'Integral multiplicity moments')
        if L % 2:
            check(L < 31, 'Odd multiplicity contradiction')
        else:
            check(m2 < 2*L, 'Even multiplicity contradiction')
        qcases.append(dict(q=q,L=L,sum_m2=int(m2),pairs=int(pairs)))
    check(qcases == [dict(q=16,L=27,sum_m2=39,pairs=6),dict(q=20,L=26,sum_m2=36,pairs=5),dict(q=24,L=25,sum_m2=31,pairs=3),dict(q=28,L=24,sum_m2=24,pairs=0)], 'Complete q cases')
    # Different enumeration from the producer: multisets of affine functions,
    # each encoded by its three-bit linear part plus its constant bit.
    controls = constant_tests = affine_tests = 0
    for length in range(5):
        for columns in combinations_with_replacement(range(16), length):
            m = Counter(v & 7 for v in columns)
            L = length - m[0]
            f = [L%2] + [m[v]%2 for v in range(1,8)]
            a = [sum((-1)**(x>>3) for x in columns if x&7 == v) for v in range(1,8)]
            a = [0] + a
            z = sum(x>>3 for x in columns if x&7 == 0)
            w = [sum(dot(s,x&7) ^ (x>>3) for x in columns) for s in range(8)]
            for n in range(1,8):
                for c in (0,1):
                    H = [s for s in range(8) if dot(n,s) == c]
                    K = w[H[0]]
                    actual = all(w[s] == K for s in H)
                    fourier = a[n] == (-1)**c * (L+2*z-2*K) and all(a[v] + (-1)**c*a[v^n] == 0 for v in range(1,8) if v != n)
                    check(actual == fourier, 'Exact Fourier equivalence on true affine code')
                    if actual:
                        constant_tests += 1
                        check(all(f[v] == f[v^n] for v in range(8)), 'Parity translation on true affine code')
                    affine_tests += 1
            controls += 1
    # A real local code can fail the spanning hypothesis, and must survive.
    m = Counter([1,2,3]); f = [1] + [m[v]%2 for v in range(1,8)]
    periods = [n for n in range(8) if all(f[v] == f[v^n] for v in range(8))]
    check(periods == [0,1,2,3] and len(set(f)) == 2, 'Rank-deficient guard')
    # Origin cannot be identified with the number of zero columns: in F2^1,
    # the one-column identity code is constant on either singleton hyperplane.
    singleton_w = [dot(s,1) for s in range(2)]
    check(singleton_w == [0,1], 'Single-column real code')
    for c in (0,1):
        H = [s for s in range(2) if dot(s,1) == c]
        check(len({singleton_w[s] for s in H}) == 1, 'Real singleton hyperplane')
    good_origin, physical_origin = [1,1], [0,1]
    check(all(good_origin[v] == good_origin[v^1] for v in range(2)) and not all(physical_origin[v] == physical_origin[v^1] for v in range(2)), 'Artificial origin is essential')
    # Independently rebuild the producer's published-in-artifact local q20 control.
    active = [1,3,5,7,9,11,13,14,14,15,17,19,21,22,22,23,25,26,26,27,28,28,29,30,30,31]
    restricted = [sum(dot(s,v) for v in active) for s in range(32)]
    check(Counter(restricted) == {0:1,12:20,16:11}, 'True q20 restricted control')
    full_columns = [v*16 + 512*(v.bit_count()%2) for v in active]
    for lowbit,v in zip([1,2,4,8],[14,22,26,28]):
        j = len(active)-1-active[::-1].index(v)
        full_columns[j] ^= lowbit
    full_columns.append(0)
    check(row_reduce(full_columns)[0] == 9 and all(dot(h,x)==0 for x in full_columns), 'q20 left control rank and kernel')
    left_w = [sum(dot(u,x) for x in full_columns) for u in range(1024)]
    violations = [u for u in range(1,1024) if not 27-weights[u] <= left_w[u] <= weights[u]]
    check(len(violations) == 123, 'q20 control is not a target lift')
    control_mult = Counter(active)
    control_f = [0]+[control_mult[v]%2 for v in range(1,32)]
    control_periods = [n for n in range(32) if all(control_f[v]==control_f[v^n] for v in range(32))]
    check(control_periods == list(range(0,32,2)), 'q20 control period rank four')
    print(json.dumps(dict(verified=True,source_commit='3229383ae26e6c445adf62f70545553fcc5d2055',input_sha256=hashlib.sha256(raw).hexdigest(),residual_rank=10,quadratic_rank=qrank,quadratic_B_coefficients=hex(coeffmask),hyperplanes=found,normal_rank=nrank,parity_equation_rank=31,q_cases=qcases,affine_configurations=controls,affine_hyperplanes_tested=affine_tests,constant_hyperplanes=constant_tests,rank_deficient_guard_periods=periods,q20_control_rank=9,q20_control_lift_bound_violations=len(violations),q20_control_periods=control_periods,scope='Fixed archived B, normalized even-subcode left projection kernel dimension one only. No global code-parameter or kernel-zero conclusion.',cpu_seconds=time.process_time()-start),indent=2))

if __name__ == '__main__':
    main()
