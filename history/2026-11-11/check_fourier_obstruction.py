#!/usr/bin/env python3
"""Exact certificates for the fixed residual's kernel-one obstruction.

Standard library only. No solver, network, target-matrix search, or public write.
All acceptance tests use explicit exceptions, including under python -O.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import hashlib
import json
import time

ROOT = Path(__file__).resolve().parent
INPUT_SHA256 = '276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80'
INPUT_BLOB = '8f76beaa5994563a2980ea9cb87412640d6560b4'
CERT = [(2,22,0), (3,26,0), (5,8,0), (6,13,1), (8,10,1),
        (9,19,1), (10,14,0), (11,28,0), (12,29,0), (14,23,0)]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def parity(x):
    return x.bit_count() & 1

def rank(vectors):
    basis = {}
    for value in vectors:
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)

def codeword(message, rows):
    result = 0
    for i, row in enumerate(rows):
        if (message >> i) & 1:
            result ^= row
    return result

def verify_input(raw):
    require(hashlib.sha256(raw).hexdigest() == INPUT_SHA256, 'Pinned input SHA-256')
    require(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
            == INPUT_BLOB, 'Pinned Git blob')
    return json.loads(raw)

def read_input():
    raw = (ROOT / 'inputs' / 'residual_candidate.json').read_bytes()
    return raw, verify_input(raw)

def krawtchouk_coefficients(n, weight):
    coefficients = [1]
    for j in range(n):
        sign = -1 if j < weight else 1
        coefficients = [coefficients[0]] + [coefficients[i] + sign*coefficients[i-1]
                                            for i in range(1,len(coefficients))] + [sign*coefficients[-1]]
    return coefficients

def check_formal_survivor(q):
    p,y10,y14,z8,z12,z16 = q+4,100-q,32,18,44,18
    bounds = [p,80-p,q,31-q,y10,y14,160-y10-y14,z8,z12,z16,80-z8-z12-z16]
    require(min(bounds) >= 0, 'Eleven formal count bounds')
    joint = Counter({(0,0):1,(0,32):1})
    classes = [(14,22,14,160),(16,24,12,p),(16,24,16,80-p),
               (16,16,12,q),(16,16,16,31-q),
               (18,18,10,y10),(18,18,14,y14),(18,18,18,160-y10-y14),
               (20,20,8,z8),(20,20,12,z12),(20,20,16,z16),(20,20,20,80-z8-z12-z16)]
    for b,bh,a,count in classes:
        joint[a,b] += count
        joint[a,bh] += count
    require(sum(joint.values()) == 1024, 'Formal distribution mass')
    left = {a:krawtchouk_coefficients(27,a) for a,b in joint}
    right = {b:krawtchouk_coefficients(37,b) for a,b in joint}
    dual = {}
    for i in range(28):
        for j in range(38):
            numerator = sum(count*left[a][i]*right[b][j] for (a,b),count in joint.items())
            require(numerator >= 0 and numerator % 1024 == 0, 'Integral nonnegative split coefficient')
            dual[i,j] = numerator//1024
    require(sum(dual.values()) == 2**54, 'Split dual mass')
    slack = q//4-4-dual[1,0]-dual[1,1]
    require(slack == q//4-4 and slack >= 0, 'November 8 column-incidence cut')
    return {'counts':[p,q,y10,y14,z8,z12,z16], 'bounds_checked':11,
            'integral_nonnegative_split_coefficients':len(dual),
            'november_8_incidence_slack':slack, 'still_formally_feasible':True}

def check_certificate(windows, certificate):
    for t, n, c in certificate:
        for s in range(32):
            want = (14,) if parity(n & s) == c else (10,14,18)
            require(windows[t][s] == want, 'Exact labelled residual hyperplane')

def main():
    start = time.process_time()
    raw, data = read_input()
    rows = [int(s, 16) for s in data['basis_hex']]
    words = [codeword(u, rows) for u in range(1024)]
    weights = [w.bit_count() for w in words]
    require(rank(rows) == 10, 'Residual rank ten')
    require(Counter(weights) == {0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1},
            'Full residual distribution')
    h = 1008
    require([u for u in range(1,1024) if weights[u] >= 27] == [h], 'Unique possible nonzero kernel message')
    require(rank([16,32,64,128,256,h,1,2,4,8]) == 10, 'Direct quotient decomposition')
    monomials = [1 << i for i in range(10)]
    monomials += [(1 << i) | (1 << j) for i,j in combinations(range(10),2)]
    evaluation = [sum(int((u & m) == m) << j for j,m in enumerate(monomials))
                  for u in range(1024) if weights[u] == 14]
    require(len(evaluation) == 160 and rank(evaluation) == 55, 'Inherited double-even rigidity')
    require(all(weights[s << 4] == weights[(s << 4) ^ h] == 16 for s in range(1,32)),
            'S residual pairs have weights sixteen')
    windows = []
    for t in range(16):
        coset = []
        for s in range(32):
            u = t ^ (s << 4)
            if u == 0:
                coset.append((0,))
                continue
            b, bh = weights[u], weights[u ^ h]
            coset.append(tuple(a for a in range(28)
                               if max(27-b,27-bh) <= a <= min(b,bh)
                               and (a+b) % 4 == 0 and (a+bh) % 4 == 0))
        windows.append(coset)
    check_certificate(windows, CERT)
    require(all(windows[0][s] == (12,16) for s in range(1,32)), 'S left-weight choices')
    normals = [n for t,n,c in CERT]
    require(rank(normals) == 5, 'Forced hyperplane normals span the dual space')
    selected = []
    for entry in CERT:
        if rank([n for t,n,c in selected] + [entry[1]]) > len(selected):
            selected.append(entry)
    require(len(selected) == 5, 'Five-hyperplane certificate')
    reached = {0}
    for t,n,c in selected:
        reached |= {v ^ n for v in reached}
    require(reached == set(range(32)), 'All translations generated')

    # These are all possibilities from q integer, L=31-q/4 integer, and L<=27.
    cases = []
    for q in range(32):
        if q % 4:
            continue
        L = 31-q//4
        if L > 27:
            continue
        moment2 = 992-14*q-L*L
        if L % 2:
            require(L < 31, 'Odd parity contradicts thirty-one active labels')
            reason = 'All 31 nonzero labels would have odd multiplicity, requiring at least 31 active columns.'
        else:
            require(moment2 < 2*L, 'Even multiplicities contradict second moment')
            reason = 'Every multiplicity would be even, so sum(m_v^2)>=2L, contrary to the exact second moment.'
        cases.append({'q':q, 'active_columns':L, 'zero_columns':27-L,
                      'sum_multiplicity_squared':moment2,
                      'repeated_pairs':(moment2-L)//2, 'contradiction':reason})
    require([case['q'] for case in cases] == [16,20,24,28], 'All possible q values covered')

    # Exhaustive small real-code controls for the exact Fourier criterion.
    # Dimension 3, every multiset of 0..4 columns, every affine offset per column.
    # The check includes zero/repeated columns and constant functions.
    configurations = hyperplanes = constant_hyperplanes = 0
    for length in range(5):
        for columns in combinations_with_replacement(range(8), length):
            L = sum(v != 0 for v in columns)
            mult = Counter(columns)
            f = [L % 2] + [mult[v] % 2 for v in range(1,8)]
            for offsets in range(1 << length):
                bits = [(offsets >> j) & 1 for j in range(length)]
                z = sum(b for v,b in zip(columns,bits) if v == 0)
                a = [0] * 8
                for v,b in zip(columns,bits):
                    if v:
                        a[v] += 1-2*b
                w = [sum(b ^ parity(s & v) for v,b in zip(columns,bits)) for s in range(8)]
                for s in range(8):
                    require(2*w[s] == L+2*z-sum(a[v]*(1-2*parity(s&v)) for v in range(1,8)),
                            'Exact Fourier expansion on actual affine code')
                for n in range(1,8):
                    for c in range(2):
                        H = [s for s in range(8) if parity(n&s) == c]
                        K = w[H[0]]
                        actual_constant = all(w[s] == K for s in H)
                        sign = 1-2*c
                        coefficient_condition = (a[n] == (L+2*z-2*K)*sign
                            and all(a[v]+sign*a[v^n] == 0 for v in range(1,8) if v != n))
                        require(actual_constant == coefficient_condition, 'Constancy iff exact paired Fourier cancellation')
                        if actual_constant:
                            require(all(f[v] == f[v^n] for v in range(8)), 'Constancy implies multiplicity-parity period')
                            constant_hyperplanes += 1
                        hyperplanes += 1
                configurations += 1
    require(configurations == 6401 and hyperplanes == 89614, 'Complete finite control counts')

    # A real q20 restriction, found by a bounded structural construction, is
    # explicitly recorded instead of rerunning any search. It is not a lift.
    active = [1,3,5,7,9,11,13,14,14,15,17,19,21,22,22,23,25,26,26,27,28,28,29,30,30,31]
    local_weights = [sum(parity(s&v) for v in active) for s in range(32)]
    mult = Counter(active)
    require(Counter(local_weights) == {0:1,12:20,16:11}, 'Genuine q20 local control')
    require(sum(v*v for v in mult.values()) == 36, 'Actual q20 second moment')
    columns = [(v << 4) | (parity(v) << 9) for v in active]
    doubles = sorted(v for v,count in mult.items() if count == 2)
    for bit,v in zip((1,2,4,8), doubles):
        j = max(j for j,value in enumerate(active) if value == v)
        columns[j] ^= bit
    columns.append(0)
    require(len(columns) == 27 and rank(columns) == 9, 'Actual rank-nine, length-27 left control')
    require(all(parity(h&v) == 0 for v in columns), 'Control kernel contains h and has dimension one')
    violations = [u for u in range(1,1024)
                  if not 27-weights[u] <= sum(parity(u&v) for v in columns) <= weights[u]]
    require(bool(violations), 'Local control is not a target lift')
    f = [0] + [mult[v] % 2 for v in range(1,32)]
    periods = [n for n in range(32) if all(f[v] == f[v^n] for v in range(32))]
    require(any(n not in periods for n in normals), 'Actual q20 control fails the forced-period condition')

    # Negative controls do not rely on assert and remain enabled under -O.
    bad_cert = [(t,n,c ^ (t == 2)) for t,n,c in CERT]
    try:
        check_certificate(windows, bad_cert)
    except ValueError:
        changed_offset_rejected = True
    else:
        raise ValueError('Corrupted hyperplane certificate was accepted')
    try:
        verify_input(raw+b' ')
    except ValueError:
        changed_input_rejected = True
    else:
        raise ValueError('Changed input accepted')
    # f(0)=L mod2, not 0 unconditionally: one nonzero column has a constant
    # restriction to either of its two singleton hyperplanes in dimension one.
    one_columns = [1]
    one_L = sum(v != 0 for v in one_columns)
    one_mult = Counter(one_columns)
    one_column_weights = [sum(parity(s&v) for v in one_columns) for s in range(2)]
    require(one_column_weights == [0,1], 'Actual one-column control')
    require(all(len({one_column_weights[s] for s in range(2) if parity(s&1) == c}) == 1
                for c in range(2)), 'Both one-dimensional affine hyperplanes are constant')
    correct_f = [one_L % 2, one_mult[1] % 2]
    wrong_f = correct_f[:]
    wrong_f[0] = 0
    require(all(correct_f[v] == correct_f[v^1] for v in range(2))
            and not all(wrong_f[v] == wrong_f[v^1] for v in range(2)),
            'Wrong zero-label parity is detected on a genuine constant-hyperplane control')
    formal_survivors = [check_formal_survivor(q) for q in (16,20)]

    print(json.dumps({
        'verified':True,
        'result':'The archived residual has no normalized even-subcode lift with one-dimensional left-projection kernel.',
        'input_sha256':INPUT_SHA256, 'input_git_blob':INPUT_BLOB,
        'source_commit':'3229383ae26e6c445adf62f70545553fcc5d2055',
        'residual_messages':1024, 'residual_rank':10, 'quadratic_evaluation_rank':55,
        'hyperplane_certificate':CERT, 'five_hyperplane_subcertificate':selected,
        'normal_rank':5, 'translation_orbit_size':32, 'q_cases':cases,
        'controls':{'affine_multiset_configurations':configurations,
                    'hyperplanes_checked':hyperplanes, 'constant_hyperplanes':constant_hyperplanes,
                    'q20_actual_restricted_columns':active,
                    'q20_local_distribution':dict(sorted(Counter(local_weights).items())),
                    'q20_actual_left_columns':columns, 'q20_actual_left_rank':9,
                    'q20_control_lift_bound_violations':len(violations),
                    'q20_parity_periods':periods, 'not_target':True,
                    'changed_hyperplane_offset_rejected':changed_offset_rejected,
                    'changed_input_detected':changed_input_rejected, 'wrong_zero_label_parity_detected':True},
        'old_formal_survivors':formal_survivors,
        'scope':'Only the fixed archived residual, normalized even-subcode representation, and kernel-one branch. Kernel-zero, other residuals and global binary [64,11,27] existence are unresolved. No novelty, publication, external peer review, or proof-kernel certification claim.',
        'cpu_seconds':time.process_time()-start,
    }, indent=2))

if __name__ == '__main__':
    main()
