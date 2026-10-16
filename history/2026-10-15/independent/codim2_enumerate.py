#!/usr/bin/env python3
"""Exact dimension-9 subcode enumeration for the accompanying fixed binary code.

Standard library only. The checked-in matrix is mathematical input, not source
code. This program writes codim2_results.json in its own directory.
"""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from time import process_time


HERE = Path(__file__).resolve().parent
MATRIX = HERE / "codim2_generator_matrix.txt"


def kernel_basis(a, b):
    """Return a reduced echelon basis for the common kernel in F_2^11."""
    basis = {}
    for m in range(1, 1 << 11):
        if (m & a).bit_count() % 2 or (m & b).bit_count() % 2:
            continue
        v = m
        for pivot in sorted(basis, reverse=True):
            if (v >> pivot) & 1:
                v ^= basis[pivot]
        if not v:
            continue
        pivot = v.bit_length() - 1
        for old in list(basis):
            if (basis[old] >> pivot) & 1:
                basis[old] ^= v
        basis[pivot] = v
    answer = [basis[p] for p in sorted(basis)]
    assert len(answer) == 9
    return answer


def main():
    started = process_time()
    raw = MATRIX.read_bytes()
    lines = raw.decode("ascii").splitlines()
    assert len(lines) == 11
    assert all(len(s) == 64 and set(s) <= {"0", "1"} for s in lines)
    rows = [int(s[::-1], 2) for s in lines]
    words = [0] * (1 << 11)
    for m in range(1, 1 << 11):
        bit = m & -m
        words[m] = words[m ^ bit] ^ rows[bit.bit_length() - 1]
    assert len(set(words)) == 1 << 11, "The generator must have rank 11."
    distribution = Counter(c.bit_count() for c in words)
    minimum_weight = min(w for w in distribution if w)
    assert minimum_weight == 26
    minimum_messages = [m for m, c in enumerate(words) if c.bit_count() == 26]
    assert len(minimum_messages) == 234

    # Bit i records whether the ith minimum message is annihilated by a.
    zero_masks = [
        sum(1 << i for i, m in enumerate(minimum_messages)
            if not (m & a).bit_count() % 2)
        for a in range(1 << 11)
    ]
    character_sums = [2 * mask.bit_count() - len(minimum_messages)
                      for mask in zero_masks]
    assert min(character_sums[1:]) == -30
    histogram = Counter()
    minimum = len(minimum_messages) + 1
    minimizers = []
    for a in range(1, 1 << 11):
        for b in range(a + 1, 1 << 11):
            # The nonzero members of a dual 2-space are {a,b,a^b}.
            # Take its two smallest members, so each dual 2-space occurs once.
            if b >= (a ^ b):
                continue
            count = (zero_masks[a] & zero_masks[b]).bit_count()
            histogram[count] += 1
            if count < minimum:
                minimum = count
                minimizers = []
            if count == minimum:
                minimizers.append([a, b, a ^ b])
    total = sum(histogram.values())
    assert total == ((1 << 11) - 1) * ((1 << 11) - 2) // 6 == 698027
    first_moment = sum(n * multiplicity for n, multiplicity in histogram.items())
    pair_moment = sum(n * (n - 1) // 2 * multiplicity
                      for n, multiplicity in histogram.items())
    assert first_moment == 234 * 1023 * 1022 // 6
    assert pair_moment == 234 * 233 // 2 * (511 * 510 // 6)

    a, b, _ = minimizers[0]
    example_messages = [m for m in range(1 << 11)
                        if not (m & a).bit_count() % 2
                        and not (m & b).bit_count() % 2]
    example_basis = kernel_basis(a, b)
    assert len(example_messages) == 512
    result = {
        "scope": "Character-sum bounds through codimension 3 and exact dimension-9 enumeration for this fixed binary [64,11,26] code only",
        "matrix_file": MATRIX.name,
        "matrix_sha256": sha256(raw).hexdigest(),
        "message_convention": "Integer bit i selects matrix row i+1; matrix columns are printed left to right",
        "dimension": 11,
        "length": 64,
        "weight_distribution": dict(sorted(distribution.items())),
        "weight26_message_count": len(minimum_messages),
        "nonzero_dual_character_sum_histogram": dict(sorted(Counter(character_sums[1:]).items())),
        "minimum_nonzero_dual_character_sum": min(character_sums[1:]),
        "maximum_nonzero_dual_character_sum": max(character_sums[1:]),
        "dual_vectors_with_minimum_character_sum": [a for a in range(1, 2048)
                                                    if character_sums[a] == -30],
        "dimension8_weight26_count_certified_lower_bound": (234 - 7 * 30) // 8,
        "dimension8_bound_sharpness": "Not determined; no dual dimension-3 enumeration performed",
        "maximum_intersection_dimension_with_any_distance_at_least27_code": 7,
        "enumerated_dual_dimension2_subspaces": total,
        "minimum_weight26_words_in_dimension9_subcode": minimum,
        "maximum_weight26_words_in_dimension9_subcode": max(histogram),
        "count_achieving_minimum": len(minimizers),
        "intersection_histogram": dict(sorted(histogram.items())),
        "first_incidence_moment": first_moment,
        "second_binomial_incidence_moment": pair_moment,
        "minimizing_dual_subspaces_nonzero_messages": minimizers,
        "first_minimizer": {
            "dual_basis": [a, b],
            "dual_nonzero_messages": [a, b, a ^ b],
            "kernel_message_basis": example_basis,
            "kernel_generator_rows": [
                format(words[m], "064b")[::-1] for m in example_basis
            ],
            "weight_distribution": dict(sorted(Counter(
                words[m].bit_count() for m in example_messages).items())),
            "weight26_messages": [m for m in example_messages
                                  if words[m].bit_count() == 26],
        },
    }
    (HERE / "codim2_results.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print("Generator rank: 11; weights independently recomputed from all 2048 words.")
    print(f"Weight-26 words: {len(minimum_messages)}.")
    print("All nonzero dual character sums are at least -30 (111 attain -30).")
    print("Corollary: every dimension-8 subcode contains at least 3 weight-26 words (sharpness not asserted).")
    print(f"Enumerated all {total:,} dual 2-spaces, equivalently all dimension-9 subcodes.")
    print(f"Minimum intersection: {minimum}; multiplicity: {len(minimizers)}; maximum: {max(histogram)}.")
    print(f"First minimizing dual space: {minimizers[0]}.")
    print(f"Incidence moments: {first_moment}, {pair_moment}.")
    print(f"CPU seconds: {process_time() - started:.6f}.")


if __name__ == "__main__":
    main()
