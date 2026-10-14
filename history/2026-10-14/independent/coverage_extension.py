#!/usr/bin/env python3
"""Exact, preregistered r=3,4 minimum-support coverage for the archived matrix.
Standard library only. Run: python3 coverage_extension.py
No heuristic, replacement-column search, or coverage search beyond r=4.
"""
import collections
import hashlib
import itertools
import json
import math
import pathlib
import resource
import time

# Fixed before execution: exactly these subset sizes, exhaustive lexicographic
# enumeration, no adaptation to results, at most 60 CPU seconds in this process.
SUBSET_SIZES = (3, 4)
CPU_LIMIT_SECONDS = 60
resource.setrlimit(resource.RLIMIT_CPU, (CPU_LIMIT_SECONDS, CPU_LIMIT_SECONDS))


def main():
    start_cpu = time.process_time()
    start_wall = time.perf_counter()
    matrix_file = pathlib.Path('generator_matrix.txt')
    rows = matrix_file.read_text().splitlines()
    assert len(rows) == 11 and all(len(r) == 64 and set(r) <= {'0','1'} for r in rows)
    generator = [sum(int(bit) << j for j,bit in enumerate(row)) for row in rows]
    words = []
    for message in range(2048):
        word = 0
        for i,row in enumerate(generator):
            if (message >> i) & 1:
                word ^= row
        words.append(word)
    assert len(set(words)) == 2048 and min(w.bit_count() for w in words[1:]) == 26
    minimum_messages = [m for m,w in enumerate(words) if w.bit_count() == 26]
    assert len(minimum_messages) == 234
    # Bit t of incidence[j] means minimum word t has a 1 at coordinate j.
    incidence = [sum(((words[m] >> j) & 1) << t for t,m in enumerate(minimum_messages))
                 for j in range(64)]
    full = (1 << len(minimum_messages)) - 1
    records = []
    uncovered_certificates = []
    for size in SUBSET_SIZES:
        histogram = collections.Counter()
        first_uncovered = None
        first_minimum = None
        min_coverage = len(minimum_messages)+1
        max_coverage = -1
        tested = 0
        for subset in itertools.combinations(range(64),size):
            mask = full
            for coordinate in subset:
                mask &= incidence[coordinate]
            count = mask.bit_count()
            histogram[count] += 1
            tested += 1
            if count < min_coverage:
                min_coverage = count
                first_minimum = [j+1 for j in subset]
            max_coverage = max(max_coverage,count)
            if count == 0 and first_uncovered is None:
                first_uncovered = [j+1 for j in subset]
        assert tested == math.comb(64,size) == sum(histogram.values())
        record = {'subset_size':size,'subsets_tested':tested,
                  'covered_subsets':tested-histogram[0],'uncovered_subsets':histogram[0],
                  'minimum_coverage':min_coverage,'maximum_coverage':max_coverage,
                  'lexicographically_first_minimum_coverage_set_1based':first_minimum,
                  'lexicographically_first_uncovered_set_1based':first_uncovered,
                  'coverage_count_histogram':dict(sorted(histogram.items()))}
        records.append(record)
        if first_uncovered is not None:
            mask = full
            for coordinate in first_uncovered:
                mask &= incidence[coordinate-1]
            assert mask == 0
            missing = []
            for m in minimum_messages:
                zeros = [j for j in first_uncovered if ((words[m] >> (j-1)) & 1) == 0]
                assert zeros
                missing.append({'message_integer':m,'zero_coordinates_in_set_1based':zeros})
            uncovered_certificates.append({'subset_size':size,'set_1based':first_uncovered,
                'incidence_intersection_hex':'0','per_minimum_word_missing_coordinates':missing})
    triple,quadruple = records
    if triple['uncovered_subsets'] == 0 and quadruple['uncovered_subsets'] > 0:
        threshold = {'minimum_uncovered_subset_size_exact':4,
                     'reason':'All triples are covered and at least one quadruple is uncovered. Every smaller set extends to a triple.'}
    elif quadruple['uncovered_subsets'] == 0:
        threshold = {'minimum_uncovered_subset_size_lower_bound':5,
                     'reason':'Every quadruple is covered; every smaller set extends to a quadruple. No larger sizes tested.'}
    else:
        threshold = {'minimum_uncovered_subset_size_upper_bound':3,
                     'reason':'At least one triple is uncovered; this extension alone makes no lower-size assertion.'}
    output = {'matrix_sha256':hashlib.sha256(matrix_file.read_bytes()).hexdigest(),
              'coordinate_convention':'1-based, matching generator_matrix.txt',
              'preregistered_subset_sizes':list(SUBSET_SIZES),
              'cpu_limit_seconds':CPU_LIMIT_SECONDS,'enumeration_order':'lexicographic',
              'minimum_weight':26,'minimum_word_count':len(minimum_messages),
              'minimum_messages_in_incidence_bit_order':minimum_messages,
              'coordinate_incidence_masks_hex':[hex(mask) for mask in incidence],
              'coverage_results':records,'threshold_statement':threshold,
              'first_uncovered_certificates':uncovered_certificates,
              'scope':'Coverage of minimum supports of this archived code only; uncovered sets do not establish an improving replacement.'}
    pathlib.Path('coverage_extension_results.json').write_text(json.dumps(output,indent=2)+'\n')
    log = ['PASS: archived generator gives 2048 distinct words, minimum weight26, exactly234 minimum words.',
           'Preregistered scope: exhaust all coordinate subsets of sizes3 and4; no other sizes or replacement columns.',
           'Each coordinate has a234-bit incidence mask; intersection population count is exact support coverage.']
    for record in records:
        log.append(f"r={record['subset_size']}: tested={record['subsets_tested']}; covered={record['covered_subsets']}; uncovered={record['uncovered_subsets']}; min_coverage={record['minimum_coverage']}; max_coverage={record['maximum_coverage']}; first_uncovered={record['lexicographically_first_uncovered_set_1based']}.")
    log.extend([f'Threshold: {threshold}',
                f'CPU seconds: {time.process_time()-start_cpu:.6f}; wall seconds: {time.perf_counter()-start_wall:.6f}.',
                'No heuristic, new-column search, or search beyond r=4.'])
    pathlib.Path('coverage_extension.log').write_text('\n'.join(log)+'\n')
    names = ['coverage_extension.py','coverage_extension_results.json','coverage_extension.log']
    pathlib.Path('coverage_extension_SHA256SUMS').write_text(''.join(f'{hashlib.sha256(pathlib.Path(n).read_bytes()).hexdigest()}  {n}\n' for n in names))
    print('\n'.join(log))


if __name__ == '__main__':
    main()
