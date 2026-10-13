#!/usr/bin/env python3
"""Exact output/bound audit; no scan through [3,X].

Accept a JSON list of [n,j,q] or a dictionary with a `hits` list.
This independently checks validity of the emitted triples and equality with
an already audited reference. It does NOT itself establish that a new
inverse enumerator traverses every required branch; inspect its proof and
pruning invariants separately.
"""
import argparse
import hashlib
import json
from pathlib import Path

BUNDLED_REFERENCE = Path(__file__).resolve().parent / 'reference' / 'paradox_cert_J92_previous.json'
PREVIOUS_REFERENCE = Path('reference/paradox_cert_J92_previous.json')
REFERENCE = BUNDLED_REFERENCE if BUNDLED_REFERENCE.is_file() else PREVIOUS_REFERENCE

def step(x):
    return (3*x+1)//2 if x % 2 else x//2

def triples(obj):
    raw = obj['hits'] if isinstance(obj, dict) else obj
    assert isinstance(raw, list), 'hits must be a list'
    out = []
    for entry in raw:
        assert isinstance(entry, list) and len(entry) == 3, f'bad triple: {entry}'
        assert all(type(x) is int for x in entry), f'noninteger triple: {entry}'
        out.append(tuple(entry))
    assert len(out) == len(set(out)), 'duplicate triples'
    return set(out)

def check_actual_hits(hits, J):
    for n,j,q in hits:
        assert n > 2 and 1 <= j <= J and 0 <= q <= j, (n,j,q)
        x,odd = n,0
        for _ in range(j):
            odd += x % 2
            x = step(x)
        assert odd == q, ('wrong odd count',n,j,q,odd)
        assert 3**q < 2**j, ('coefficient not below 1',n,j,q)
        assert x >= n, ('endpoint below start',n,j,q,x)

def check_bound_fields(c):
    J = c['J']
    assert J == 92 and len(c['H']) == len(c['qmax']) == J
    for j,(q,h) in enumerate(zip(c['qmax'],c['H']),1):
        assert type(q) is int and type(h) is int and h >= 0
        assert 3**q < 2**j <= 3**(q+1), ('bad qmax',j)
        if h == 0:
            assert q == 0 or 4**q < 2**j, ('bad zero bound',j)
        else:
            assert (3*h+1)**q >= 2**j * h**q, ('bad H lower boundary',j)
            assert (3*(h+1)+1)**q < 2**j * (h+1)**q, ('bad H upper boundary',j)
    H = max(c['H'])
    assert H == c['Hmax'] == 1192
    peak = 0
    for m in range(3,H+1,2):
        x = m
        for k in range(J+1):
            peak = max(peak,x)
            if k != J:
                x = step(x)
    assert peak == c['X'] == 125252, ('bad finite-J excursion bound',peak)
    return H,peak

def compare(hits,expected):
    assert hits == expected, {'missing': sorted(expected-hits)[:10], 'extra': sorted(hits-expected)[:10]}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate',type=Path)
    parser.add_argument('--reference',type=Path,default=REFERENCE)
    parser.add_argument('--selftest',action='store_true')
    args = parser.parse_args()
    ref = json.loads(args.reference.read_text())
    H,X = check_bound_fields(ref)
    expected = triples(ref)
    assert len(expected) == 593 and len({n for n,_,_ in expected}) == 550
    check_actual_hits(expected,92)
    raw = args.candidate.read_bytes()
    candidate = json.loads(raw)
    if isinstance(candidate,dict) and 'J' in candidate:
        assert candidate['J'] == 92, 'candidate J must be 92'
    if isinstance(candidate,dict) and all(k in candidate for k in ['J','qmax','H','Hmax','X']):
        check_bound_fields(candidate)
        fields = ['J','qmax','H','Hmax','X','hits']
        changed = [k for k in fields if candidate[k] != ref[k]]
        assert not changed, ('certificate fields differ from reference',changed)
        print('PASS: exact certificate-field equality (J,qmax,H,Hmax,X,hits); x_definition excluded')
    got = triples(candidate)
    check_actual_hits(got,92)
    compare(got,expected)
    roots,depths = set(),[]
    for n,j,q in got:
        x,d = n,0
        while not (x % 2 and 3 <= x <= H):
            assert d < j, ('no small odd hit',n,j,q)
            x = step(x); d += 1
        roots.add(x); depths.append(d)
    print(f'PASS: {len(got)} exact triples, {len({n for n,_,_ in got})} distinct starts; reference set equality')
    print(f'PASS: exact adjacent q/H inequalities; Hmax={H}; finite 92-step X={X}')
    print(f'Canonical earliest-small-odd statistics: roots={len(roots)}, max_depth={max(depths)} (not completeness cutoffs)')
    print('Candidate SHA256:',hashlib.sha256(raw).hexdigest())
    print('Reference SHA256:',hashlib.sha256(args.reference.read_bytes()).hexdigest())
    if args.selftest:
        dropped = set(got); dropped.remove(min(got))
        fake = set(got); fake.add((3,5,2))
        for name,wrong in [('missing hit',dropped),('extra fake hit',fake)]:
            try:
                check_actual_hits(wrong,92); compare(wrong,expected)
            except AssertionError:
                print('PASS: rejected mutation:',name)
            else:
                raise AssertionError('accepted mutation: '+name)
    print('LIMIT: traversal completeness and branch-pruning soundness require separate audit.')

if __name__ == '__main__':
    main()
