#!/usr/bin/env python3
"""Independently authored binary [64,11,26] verification; Python standard library.
Mathematical source, accessed 2026-10-14: Markus Grassl's Code Tables,
https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2
No MAGMA or database source code is included. Run: python3 verify_code64.py
Coordinate j is coefficient of x^(j-1); appended parity is coordinate 66.
Message integer bit i selects row i+1; bit strings are printed low to high.
"""
import collections
import hashlib
import itertools
import json
import pathlib
import time

SOURCE = 'https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2'
EXPONENTS = [52,51,50,49,47,45,44,43,40,38,37,34,33,32,28,26,24,20,19,18,15,14,12,9,8,7,5,3,2,1,0]


def parity(x):
    return x.bit_count() & 1


def bits(x, width):
    return ''.join(str((x >> j) & 1) for j in range(width))


def rref(rows, width):
    rows = [r for r in rows if r]
    pivots = []
    at = 0
    for column in range(width):
        p = next((i for i in range(at,len(rows)) if (rows[i] >> column) & 1), None)
        if p is None:
            continue
        rows[at], rows[p] = rows[p], rows[at]
        for i in range(len(rows)):
            if i != at and ((rows[i] >> column) & 1):
                rows[i] ^= rows[at]
        pivots.append(column)
        at += 1
    return rows[:at], pivots


def nullspace(equations, width):
    reduced, pivots = rref(equations,width)
    basis = []
    for f in range(width):
        if f in pivots:
            continue
        v = 1 << f
        for equation,p in zip(reduced,pivots):
            if (equation >> f) & 1:
                v |= 1 << p
        assert all(parity(v & e) == 0 for e in equations)
        basis.append(v)
    return basis


def encode(message, rows):
    result = 0
    for i,row in enumerate(rows):
        if (message >> i) & 1:
            result ^= row
    return result


def coordinate_implementation():
    """Independent tuple convolution, exhaustive filtering, literal shortening.
    Does not use integer polynomial arithmetic, nullspace, rref, or encode.
    """
    coefficients = [int(i in EXPONENTS) for i in range(53)]
    shortened = set()
    parent = collections.Counter()
    extended_hist = collections.Counter()
    for message in range(8192):
        message_bits = [(message // (2 ** i)) % 2 for i in range(13)]
        word = [0] * 65
        for i in range(13):
            if message_bits[i]:
                for j,c in enumerate(coefficients):
                    word[i+j] = (word[i+j] + c) % 2
        parent[sum(word)] += 1
        extended = word + [sum(word) % 2]
        extended_hist[sum(extended)] += 1
        if extended[64] == extended[65] == 0:
            shortened.add(tuple(extended[:64]))
    return shortened,dict(sorted(parent.items())),dict(sorted(extended_hist.items()))


def odd_relation(messages):
    pool = set(messages)
    for a,b in itertools.combinations(messages,2):
        c = a ^ b
        if b < c and c in pool:
            return [a,b,c]
    basis = {}
    for index,value in enumerate(messages):
        combination = 1 << index
        while value:
            p = value.bit_length()-1
            if p not in basis:
                basis[p] = (value,combination)
                break
            other,subset = basis[p]
            value ^= other
            combination ^= subset
        if value == 0 and combination.bit_count() % 2:
            return [m for i,m in enumerate(messages) if (combination >> i) & 1]
    return None


def write_json(name, data):
    pathlib.Path(name).write_text(json.dumps(data,indent=2)+'\n')


def main():
    wall = time.perf_counter()
    cpu = time.process_time()
    polynomial = sum(1 << e for e in EXPONENTS)
    remainder = (1 << 65) | 1
    while remainder.bit_length() >= polynomial.bit_length():
        remainder ^= polynomial << (remainder.bit_length()-polynomial.bit_length())
    assert remainder == 0
    cyclic = [polynomial << i for i in range(13)]
    extended = [r | (parity(r) << 65) for r in cyclic]
    equations = [sum(((r >> c) & 1) << i for i,r in enumerate(extended)) for c in (64,65)]
    kernel = nullspace(equations,13)
    assert len(kernel) == 11
    generator = [encode(m,extended) for m in kernel]
    assert all(r >> 64 == 0 for r in generator)
    rank = len(rref(generator,64)[0])
    assert rank == 11
    words = [encode(m,generator) for m in range(2048)]
    assert len(set(words)) == 2048
    weights = [w.bit_count() for w in words]
    assert min(weights[1:]) == 26
    minimum_messages = [m for m in range(1,2048) if weights[m] == 26]
    histogram = dict(sorted(collections.Counter(weights).items()))
    alternative, parent_hist, extended_hist = coordinate_implementation()
    assert alternative == {tuple(map(int,bits(w,64))) for w in words}
    assert len(alternative) == 2048
    assert sum(parent_hist.values()) == 8192 and min(w for w in parent_hist if w) == 25
    assert sum(extended_hist.values()) == 8192 and min(w for w in extended_hist if w) == 26

    # Any minimum word with deleted coordinate bit 1 becomes weight 25+b <=26.
    single_witnesses = []
    eligible = []
    for j in range(64):
        m = next((m for m in minimum_messages if (words[m] >> j) & 1),None)
        if m is None:
            eligible.append(j+1)
        else:
            single_witnesses.append({'coordinate_1based':j+1,'message_integer':m,
                                     'codeword_hex':f'{words[m]:016x}', 'weight':26,'deleted_bit':1})
    candidate_tests = 0
    successes = []
    for j in eligible:
        for new_column in range(2048):
            candidate_tests += 1
            if all(parity(m & new_column) == 1 for m in minimum_messages):
                d = min(weights[m]-((words[m] >> (j-1)) & 1)+parity(m & new_column) for m in range(1,2048))
                if d >= 27:
                    successes.append([j,new_column,d])
    assert not successes

    # Likewise, a minimum word having both deleted bits 1 gives new weight
    # 24+b1+b2 <=26 for every pair of new columns, independently of linearity.
    pair_witnesses = []
    uncovered_pairs = []
    for j,k in itertools.combinations(range(64),2):
        mask = (1 << j) | (1 << k)
        m = next((m for m in minimum_messages if words[m] & mask == mask),None)
        if m is None:
            uncovered_pairs.append([j+1,k+1])
        else:
            pair_witnesses.append({'coordinates_1based':[j+1,k+1],'message_integer':m,
                                   'codeword_hex':f'{words[m]:016x}','weight':26,'deleted_weight':2})
    assert len(pair_witnesses)+len(uncovered_pairs) == 2016
    relation = odd_relation(minimum_messages)
    relation_certificate = None
    if relation:
        xor_messages = 0
        xor_words = 0
        for m in relation:
            xor_messages ^= m
            xor_words ^= words[m]
        assert xor_messages == xor_words == 0 and len(relation) % 2 == 1
        relation_certificate = {'message_integers':relation,
          'message_bits_low_to_high':[bits(m,11) for m in relation],
          'codeword_hex':[f'{words[m]:016x}' for m in relation],
          'weights':[weights[m] for m in relation], 'xor_messages':0,'xor_codewords':0,
          'number_of_terms_mod_2':1,
          'coefficient_rank':len(rref(minimum_messages,11)[0]),
          'augmented_rank':len(rref([m | (1 << 11) for m in minimum_messages],12)[0]),
          'consequences':[
            'No linear one-coordinate extension of this particular code has distance at least 27.',
            'Every dimension-10 subcode of this code contains a word of weight 26.',
            'Any binary dimension-11 code intersecting this code in dimension at least 10 has distance at most 26.']}

    pathlib.Path('generator_matrix.txt').write_text('\n'.join(bits(r,64) for r in generator)+'\n')
    pathlib.Path('minimum_messages.tsv').write_text('message_integer\tmessage_bits_low_to_high\tcodeword_hex\tweight\n'+''.join(f'{m}\t{bits(m,11)}\t{words[m]:016x}\t26\n' for m in minimum_messages))
    pathlib.Path('weight_distribution.tsv').write_text('weight\tcount\n'+''.join(f'{w}\t{c}\n' for w,c in histogram.items()))
    certificate = {'coordinate_convention':'1-based; coefficient x^(j-1); parity appended at 66',
        'message_convention':'integer bit i selects generator row i+1; strings printed low to high',
        'single_column_witnesses':single_witnesses,'eligible_deleted_coordinates':eligible,
        'single_column_candidate_space_size':64*2048,
        'explicit_new_column_tests_after_pruning':candidate_tests,'successful_replacements':successes,
        'pair_witnesses':pair_witnesses,'pairs_without_support_witness':uncovered_pairs,
        'two_column_candidate_space_size':2016*(2048**2),
        'odd_minimum_message_relation':relation_certificate}
    write_json('obstruction_certificate.json',certificate)
    summary = {'construction_source':SOURCE,'source_access_date':'2026-10-14',
      'source_table_bounds':{'lower':26,'upper':27},'polynomial_exponents':EXPONENTS,
      'polynomial_divides_x65_plus_1':True,'shortening_coordinates_1based':[65,66],
      'shortening_constraint_rows_integer':equations,'shortening_constraint_rank':len(rref(equations,13)[0]),
      'shortening_kernel_basis_integer':kernel,
      'parameters':{'field':2,'length':64,'rank':rank,'minimum_distance':26},
      'enumerated_codewords':2048,'enumerated_nonzero_codewords':2047,
      'weight_distribution':histogram,'minimum_word_count':len(minimum_messages),
      'cyclic_parent_weight_distribution':parent_hist,'extended_parent_weight_distribution':extended_hist,
      'independent_coordinate_enumeration_matches':True,
      'single_column_experiment':{'candidate_space_size':64*2048,'old_columns_excluded_by_witness':len(single_witnesses),'eligible_old_coordinates':eligible,'explicit_candidate_tests_after_pruning':candidate_tests,'successful_replacements':len(successes)},
      'two_column_experiment':{'old_pairs_total':2016,'old_pairs_excluded_by_witness':len(pair_witnesses),'pairs_without_support_witness':uncovered_pairs,'candidate_space_size':2016*(2048**2)},
      'odd_minimum_message_relation':relation,
      'minimum_message_coefficient_rank':len(rref(minimum_messages,11)[0]),
      'minimum_message_augmented_rank':len(rref([m | (1 << 11) for m in minimum_messages],12)[0]),
      'scope':'Known lower-bound reproduction and specified local exclusions only; no global nonexistence proof for binary linear [64,11,27].'}
    write_json('results.json',summary)
    log = [
      'PASS: generating polynomial divides x^65 + 1 over GF(2).',
      'PASS: parent exhaustive enumeration: [65,13,25]; parity extension: [66,13,26].',
      'PASS: shortening constraint rank 2, kernel dimension 11.',
      'PASS: shortened rank 11, 2048 distinct words, 2047 nonzero words, distance 26.',
      'PASS: independent literal-coordinate enumeration agrees on entire codeword set.',
      f'Weight distribution: {histogram}', f'Minimum-word count: {len(minimum_messages)}.',
      f'Single-column exclusions: {len(single_witnesses)}/64 old columns; each excludes all 2048 new columns.',
      f'Eligible old columns: {eligible}; explicit candidate tests after pruning: {candidate_tests}.',
      f'Two-column support exclusions: {len(pair_witnesses)}/2016 old pairs; uncovered: {uncovered_pairs}.',
      f'Odd minimum-message XOR relation: {relation}.',
      f'Minimum-message equation coefficient rank: {len(rref(minimum_messages,11)[0])}; augmented rank: {len(rref([m | (1 << 11) for m in minimum_messages],12)[0])}.',
      'Global binary linear [64,11,27] existence is not settled by this computation.',
      f'CPU seconds: {time.process_time()-cpu:.6f}; wall seconds: {time.perf_counter()-wall:.6f}.',
      'No external dependencies, random search, or network access used by this script.'
    ]
    pathlib.Path('verification.log').write_text('\n'.join(log)+'\n')
    filenames = ['verify_code64.py','generator_matrix.txt','minimum_messages.tsv','weight_distribution.tsv','obstruction_certificate.json','results.json','verification.log','check_certificates.py','certificate_checker.log','README.md']
    pathlib.Path('SHA256SUMS').write_text('\n'.join(f'{hashlib.sha256(pathlib.Path(n).read_bytes()).hexdigest()}  {n}' for n in filenames)+'\n')
    print('\n'.join(log))


if __name__ == '__main__':
    main()
