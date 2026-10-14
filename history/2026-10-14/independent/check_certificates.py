#!/usr/bin/env python3
"""Independent certificate checker; no imports from the construction script.
Run in the artifact directory: python3 check_certificates.py
Uses only the public generator matrix, certificates, and tabulations.
"""
import collections
import csv
import itertools
import json
import pathlib


def main():
    rows = pathlib.Path('generator_matrix.txt').read_text().splitlines()
    assert len(rows) == 11 and all(len(r) == 64 and set(r) <= {'0','1'} for r in rows)
    matrix = [[int(c) for c in row] for row in rows]
    words = []
    for message in range(2048):
        word = [0] * 64
        for i in range(11):
            if (message // (2**i)) % 2:
                for j in range(64):
                    word[j] = (word[j] + matrix[i][j]) % 2
        words.append(tuple(word))
    assert len(set(words)) == 2048  # injectivity proves rank 11.
    weights = [sum(w) for w in words]
    assert weights[0] == 0 and min(weights[1:]) == 26
    expected_minimum = {m for m in range(1,2048) if weights[m] == 26}
    expected_distribution = collections.Counter(weights)
    with open('weight_distribution.tsv') as handle:
        actual_distribution = {int(r['weight']):int(r['count']) for r in csv.DictReader(handle,delimiter='\t')}
    assert expected_distribution == actual_distribution
    def check_word(message, hexadecimal):
        integer = int(hexadecimal,16)
        assert tuple((integer // (2**j)) % 2 for j in range(64)) == words[message]
    with open('minimum_messages.tsv') as handle:
        minimum_records = list(csv.DictReader(handle,delimiter='\t'))
    assert {int(r['message_integer']) for r in minimum_records} == expected_minimum
    assert len(minimum_records) == len(expected_minimum)
    for record in minimum_records:
        m = int(record['message_integer'])
        assert record['message_bits_low_to_high'] == ''.join(str((m // (2**i)) % 2) for i in range(11))
        assert int(record['weight']) == 26
        check_word(m,record['codeword_hex'])
    certificate = json.loads(pathlib.Path('obstruction_certificate.json').read_text())
    single = certificate['single_column_witnesses']
    assert len(single) == 64 and {w['coordinate_1based'] for w in single} == set(range(1,65))
    for witness in single:
        m = witness['message_integer']
        assert m in expected_minimum
        assert words[m][witness['coordinate_1based']-1] == witness['deleted_bit'] == 1
        assert witness['weight'] == 26
        check_word(m,witness['codeword_hex'])
    pairs = certificate['pair_witnesses']
    assert len(pairs) == 2016
    assert {tuple(w['coordinates_1based']) for w in pairs} == set(itertools.combinations(range(1,65),2))
    for witness in pairs:
        m = witness['message_integer']
        j,k = witness['coordinates_1based']
        assert m in expected_minimum and words[m][j-1] == words[m][k-1] == 1
        assert witness['weight'] == 26 and witness['deleted_weight'] == 2
        check_word(m,witness['codeword_hex'])
    relation = certificate['odd_minimum_message_relation']
    selected = relation['message_integers']
    assert len(selected) % 2 == 1 and all(m in expected_minimum for m in selected)
    assert len(set(selected)) == len(selected)
    for i in range(11):
        assert sum((m // (2**i)) % 2 for m in selected) % 2 == 0
    for j in range(64):
        assert sum(words[m][j] for m in selected) % 2 == 0
    # Exhaustively verify every possible linear functional fails all-one values
    # on the minimum words; this independently verifies hyperplane obstruction.
    for h in range(2048):
        assert any(sum(((h // (2**i)) % 2)*((m // (2**i)) % 2) for i in range(11)) % 2 == 0
                   for m in selected)
    assert not certificate['eligible_deleted_coordinates']
    assert not certificate['pairs_without_support_witness']
    assert not certificate['successful_replacements']
    assert certificate['explicit_new_column_tests_after_pruning'] == 0
    assert certificate['single_column_candidate_space_size'] == 64*2048
    assert certificate['two_column_candidate_space_size'] == 2016*2048**2
    print('PASS: independent checker verified generator rank11, all2048 words, weight distribution,')
    print('all234 minimum messages, all64 coordinate witnesses, all2016 pair witnesses,')
    print('odd XOR circuit, and all2048 linear functionals against that circuit.')


if __name__ == '__main__':
    main()
