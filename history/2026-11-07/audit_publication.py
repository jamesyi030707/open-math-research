#!/usr/bin/env python3
"""Separate full-6D audit; integer-only, standard library, no search or writes."""
from collections import Counter
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent

def fwht(values):
    a = list(values)
    step = 1
    while step < len(a):
        for start in range(0, len(a), 2*step):
            for i in range(start, start+step):
                x, y = a[i], a[i+step]
                a[i], a[i+step] = x+y, x-y
        step *= 2
    return a

def pop(x):
    return bin(x).count('1')

def audit():
    raw = (HERE/'residual_candidate.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80'
    data = json.loads(raw)
    rows = [int(x, 16) for x in data['basis_hex']]
    words = [0]
    for row in rows:
        words += [x ^ row for x in words]
    assert len(set(words)) == 1024
    w = list(map(pop, words))
    assert Counter(w) == {0:1, 14:160, 16:142, 18:320, 20:160, 22:160, 24:80, 32:1}
    assert [i for i,x in enumerate(w) if x == 32] == [1008]
    h = 1008
    T = {0, h} | {i for i in range(1024) if w[i] == w[i^h] == 16}
    assert T == set(range(0, 1024, 16))
    assert all((x^y) in T for x in T for y in T)
    basis = [16,32,64,128,256,512]
    span = {0}
    for v in basis:
        span |= {x^v for x in span}
    assert span == T and len(T) == 64
    pairs = {tuple(sorted((u,u^h))) for u in T}
    assert len(pairs) == 32 and (0,h) in pairs
    assert all(w[u] == w[v] == 16 for u,v in pairs if u != 0)
    # Each restriction of an ambient column is zero or has weight 32 on T.
    column_weights = [sum(pop(u&v)%2 for u in T) for v in range(1024)]
    assert Counter(column_weights) == {0:16, 32:1008}
    allowed_q = [q for q in range(32) if (992-8*q)%32 == 0 and 0 <= (992-8*q)//32 <= 27]
    assert allowed_q == [16,20,24,28]
    assert (992-8*0)//32 == 31 > 27
    report = json.loads((HERE/'result.json').read_text())
    assert report['published_witness_q'] == 0
    # This first-moment obstruction is independent of which 31 pairs are chosen.
    control = report['control']
    cols = control['column_labels']
    weights = [sum(pop(u&v)%2 for v in cols) for u in range(32)]
    assert len(cols) == 27 and weights == control['labelled_weights']
    assert Counter(weights) == {0:1,12:16,16:15}
    assert len(set(tuple(pop(u&v)%2 for v in cols) for u in range(32))) == 32
    transformed = fwht([27-2*x for x in weights])
    assert transformed == [32*cols.count(v) for v in range(32)]
    assert sum(weights) == 432 == 16*27
    bad27 = fwht([27]+[-5]*31)
    good31 = fwht([31]+[-1]*31)
    assert bad27 == [-128]+[32]*31
    assert good31 == [0]+[32]*31
    return {'status':'pass', 'method':'full six-dimensional closure and per-column parity counts; butterfly Walsh control audit',
        'residual_messages_checked':1024, 'subspace_T_size':64,
        'subspace_T_basis':basis, 'closure_pairs_checked':4096,
        'ambient_column_types_checked':1024, 'column_weight_counts':dict(sorted(Counter(column_weights).items())),
        'quotient_nonzero_pairs':31, 'allowed_q_from_first_moment':allowed_q,
        'q0_forced_active_columns':31, 'available_columns':27,
        'q16_control':{'dimension':5, 'length':27, 'active_columns':27, 'distinct_columns':len(set(cols)),
                       'repeated_columns':{str(v):c for v,c in sorted(Counter(cols).items()) if c>1}, 'full_extension_claimed':False},
        'negative_q0_length27_zero_multiplicity':-4, 'positive_q0_simplex_length':31,
        'scope':'Only the published q=0 formal witness is excluded for the fixed residual and kernel-one branch; no branch-wide or global exclusion.'}

if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
