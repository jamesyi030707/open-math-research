#!/usr/bin/env python3
"""Independently verify coverage by accumulating subsets of each support.
This uses no incidence-mask intersections and checks the complete histograms.
Run: python3 coverage_extension_check.py
"""
import collections
import hashlib
import itertools
import json
import math
import pathlib
import resource
import time

resource.setrlimit(resource.RLIMIT_CPU,(60,60))
start = time.process_time()
results = json.loads(pathlib.Path('coverage_extension_results.json').read_text())
raw = pathlib.Path('generator_matrix.txt').read_bytes()
assert hashlib.sha256(raw).hexdigest() == results['matrix_sha256']
matrix = [[int(c) for c in row] for row in raw.decode().splitlines()]
minimum_supports = []
minimum_messages = []
for m in range(1,2048):
    support = tuple(j+1 for j in range(64) if sum(matrix[i][j]*((m >> i)&1) for i in range(11)) % 2)
    assert len(support) >= 26
    if len(support) == 26:
        minimum_supports.append(support)
        minimum_messages.append(m)
assert len(minimum_supports) == 234
assert minimum_messages == results['minimum_messages_in_incidence_bit_order']
for j,mask in enumerate(results['coordinate_incidence_masks_hex'],1):
    assert int(mask,16) == sum((j in support) << t for t,support in enumerate(minimum_supports))
log = []
all_uncovered = {}
for record in results['coverage_results']:
    r = record['subset_size']
    assert r in (3,4)
    counts = collections.Counter()
    for support in minimum_supports:
        counts.update(itertools.combinations(support,r))
    histogram = collections.Counter(counts.values())
    uncovered = math.comb(64,r)-len(counts)
    if uncovered:
        histogram[0] = uncovered
    expected_histogram = {int(k):v for k,v in record['coverage_count_histogram'].items()}
    assert dict(histogram) == expected_histogram
    assert len(counts) == record['covered_subsets']
    assert uncovered == record['uncovered_subsets']
    assert min(histogram) == record['minimum_coverage']
    assert max(histogram) == record['maximum_coverage']
    missing = [list(subset) for subset in itertools.combinations(range(1,65),r) if subset not in counts]
    first = missing[0] if missing else None
    assert first == record['lexicographically_first_uncovered_set_1based']
    all_uncovered[str(r)] = missing
    log.append(f'PASS: r={r} independently counted by support subsets: covered={len(counts)}, uncovered={uncovered}, full histogram matches.')
for cert in results['first_uncovered_certificates']:
    subset = cert['set_1based']
    assert subset == all_uncovered[str(cert['subset_size'])][0]
    assert cert['incidence_intersection_hex'] == '0'
    assert len(cert['per_minimum_word_missing_coordinates']) == 234
    for record,m,support in zip(cert['per_minimum_word_missing_coordinates'],minimum_messages,minimum_supports):
        assert record['message_integer'] == m
        assert record['zero_coordinates_in_set_1based'] == [j for j in subset if j not in support]
        assert record['zero_coordinates_in_set_1based']
assert all_uncovered['3'] == [] and len(all_uncovered['4']) == 552
pathlib.Path('coverage_extension_uncovered_sets.json').write_text(json.dumps(all_uncovered,indent=2)+'\n')
log.append('PASS: all64 incidence masks and all234 first-uncovered witness records verified.')
log.append('PASS: exactly552 uncovered quadruples saved; no triples uncovered.')
log.append(f'CPU seconds: {time.process_time()-start:.6f}.')
pathlib.Path('coverage_extension_check.log').write_text('\n'.join(log)+'\n')
print('\n'.join(log))
