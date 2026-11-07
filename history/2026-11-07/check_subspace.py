#!/usr/bin/env python3
"""Bounded exact target-specific subspace check. No candidate search or solver."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent

def rank(vectors):
    pivots = {}
    for x in vectors:
        while x:
            j = x.bit_length()-1
            if j in pivots:
                x ^= pivots[j]
            else:
                pivots[j] = x
                break
    return len(pivots)

def word(u, rows):
    out = 0
    for j, row in enumerate(rows):
        if u >> j & 1:
            out ^= row
    return out

def inverse(weights, n):
    return [Fraction(sum((n-2*a) * (-1 if (u&v).bit_count()%2 else 1)
                         for u, a in enumerate(weights)), len(weights))
            for v in range(len(weights))]

def main():
    t = time.process_time()
    source = HERE / 'residual_candidate.json'
    data = json.loads(source.read_text())
    rows = [int(s, 16) for s in data['basis_hex']]
    assert rank(rows) == 10
    words = [word(u, rows) for u in range(1024)]
    r = [x.bit_count() for x in words]
    assert Counter(r) == {0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1}
    heavy = [u for u in range(1024) if r[u] == 32]
    assert heavy == [1008]
    h = heavy[0]
    pair_reps = sorted({min(u,u^h) for u in range(1024) if r[u] == r[u^h] == 16})
    S = [0] + pair_reps
    basis = [16,32,64,128,256]
    span = sorted({word(s,basis) for s in range(32)})
    assert S == span == list(range(0,512,16))
    assert rank(S) == 5 and rank(S+[h]) == 6
    assert all((u^v) in S for u in S for v in S)
    assert all(r[u] == r[u^h] == 16 for u in S[1:])
    # Nonzero linear functionals on F_2^5 are 1 at exactly 16 messages.
    column_weights = [sum((u&v).bit_count()%2 for u in range(32)) for v in range(32)]
    assert column_weights == [0]+[16]*31
    # A true standalone length-27, dimension-5 control at the new q=16 boundary.
    # f=x0*x1+x2*x3+x4 is balanced and f(0)=0.
    f = [((u&1)*((u>>1)&1)) ^ (((u>>2)&1)*((u>>3)&1)) ^ ((u>>4)&1)
         for u in range(32)]
    a = [0]+[16-4*f[u] for u in range(1,32)]
    mult = inverse(a, 27)
    assert all(x>=0 and x.denominator == 1 for x in mult)
    cols = [v for v,m in enumerate(mult) for _ in range(int(m))]
    assert len(cols) == 27 and rank(cols) == 5
    direct = [sum((u&v).bit_count()%2 for v in cols) for u in range(32)]
    assert direct == a and Counter(a) == {0:1,12:16,16:15}
    assert sum(a) == 16*27
    # q=0 demands constant weight16 on every nonzero 5-dimensional message.
    rejected = inverse([0]+[16]*31,27)
    assert rejected == [Fraction(-4)]+[Fraction(1)]*31
    # Honest positive q=0 control at length31: the binary simplex code.
    simplex = list(range(1,32))
    assert [sum((u&v).bit_count()%2 for v in simplex) for u in range(32)] == [0]+[16]*31
    assert inverse([0]+[16]*31,31) == [0]+[1]*31
    out = {
        'status':'pass',
        'source_commit':'816784cce71a4acd3b10fc9b42392716f1cb7fe0',
        'residual_basis_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'heavy_message':h,
        'type_16_16_pair_representatives':pair_reps,
        'subspace_basis_messages':basis,
        'subspace_size':len(S), 'subspace_rank':5,
        'closure_pairs_checked':len(S)**2,
        'identity':'12q+16(31-q) = 16*N_active; 0 <= N_active <= 27',
        'necessary_consequence':'q >= 16 and q is divisible by 4',
        'published_witness_q':0,
        'published_witness_forced_active_columns':31,
        'published_witness_negative_zero_column_multiplicity':-4,
        'control':{'length':27,'dimension':5,'column_labels':cols,
                   'weight_histogram':dict(sorted(Counter(a).items())),
                   'labelled_weights':a,'q':16,'active_columns':27},
        'simplex_positive_control':{'length':31,'dimension':5,'q':0,'zero_columns':0},
        'scope':'Every labelling of the published q=0 witness is impossible for this fixed residual/kernel-one branch. Other q values, the whole branch, kernel-zero lifts, other residuals and global [64,11,27] existence remain undecided.',
        'cpu_seconds':time.process_time()-t,
    }
    (HERE/'result.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__ == '__main__':main()
