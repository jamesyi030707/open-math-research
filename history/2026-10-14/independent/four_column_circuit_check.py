#!/usr/bin/env python3
"""Read-only independent checker for all552 four-column circuit certificates."""
import collections
import hashlib
import json
import pathlib
import resource
import time

resource.setrlimit(resource.RLIMIT_CPU,(60,60))
start=time.process_time()
raw=pathlib.Path('generator_matrix.txt').read_bytes()
matrix=[[int(c) for c in row] for row in raw.decode().splitlines()]
assert len(matrix)==11 and all(len(row)==64 for row in matrix)
result=json.loads(pathlib.Path('four_column_circuit_results.json').read_text())
assert result['matrix_sha256']==hashlib.sha256(raw).hexdigest()
uncovered=json.loads(pathlib.Path('coverage_extension_uncovered_sets.json').read_text())['4']
witnesses=result['witnesses']
assert len(witnesses)==552
assert {tuple(w['deleted_coordinates_1based']) for w in witnesses}=={tuple(d) for d in uncovered}
cache={}
def word(m):
    if m not in cache:
        cache[m]=tuple(sum(matrix[i][j]*((m//(2**i))%2) for i in range(11))%2 for j in range(64))
    return cache[m]
for witness in witnesses:
    deletion=witness['deleted_coordinates_1based']
    messages=witness['message_integers']
    assert len(deletion)==4 and len(set(deletion))==4 and all(1<=j<=64 for j in deletion)
    assert len(messages)==3 and len(set(messages))==3 and all(1<=m<2048 for m in messages)
    for i in range(11):
        assert sum((m//(2**i))%2 for m in messages)%2==0
    triple=[word(m) for m in messages]
    assert [sum(w) for w in triple]==[26,26,26]==witness['old_weights']
    for j in range(64):
        assert sum(w[j] for w in triple) in (0,2)
    for w,hexadecimal in zip(triple,witness['codeword_hex']):
        assert int(hexadecimal,16)==sum(bit*(2**j) for j,bit in enumerate(w))
    deleted=[sum(w[j-1] for j in deletion) for w in triple]
    assert deleted==witness['deleted_weights']
    assert sum(deleted)==witness['deleted_weight_total']>=6
    assert 78-sum(deleted)+8==witness['maximum_new_weight_sum']<81
    assert witness['required_new_weight_sum']==81 and witness['maximum_new_column_total']==8
    assert all(26-d>=22 for d in deleted)
    assert witness['minimum_unchanged_weight']==22
    # A new coordinate has one of four even-parity binary triples:
    # 000,011,101,110, each with weight at most2.
    assert all(a+b+((a+b)%2)<=2 for a in (0,1) for b in (0,1))
histogram=dict(sorted(collections.Counter(w['deleted_weight_total'] for w in witnesses).items()))
assert histogram=={int(k):v for k,v in result['witness_deleted_total_histogram'].items()}
assert result['unresolved_quadruples']==[] and result['quadruples_excluded_by_circuit']==552
assert result['support_coverage_threshold_unchanged']==4
log=['PASS: all552 uncovered quadruples have valid three-minimum-word circuit certificates.',
     'PASS: each circuit XOR is0 in both message and coordinate representations.',
     'PASS: every deleted total is6 or8; new total weight bound is80 or78, below81.',
     'PASS: each modified witness stays nonzero, retaining at least22 unchanged ones.',
     f'PASS: deleted-total histogram {histogram}.',f'CPU seconds:{time.process_time()-start:.6f}.']
pathlib.Path('four_column_circuit_check.log').write_text('\n'.join(log)+'\n')
print('\n'.join(log))
