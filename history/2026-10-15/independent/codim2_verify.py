#!/usr/bin/env python3
"""Independent exact checker using coordinate arrays, Walsh sums, and RREF.

Does not import codim2_enumerate.py, does not use minimum-word bitsets, and
enumerates dual subspaces by a different unique normal form. Read-only except
for stdout. Standard library only.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from time import process_time


HERE = Path(__file__).resolve().parent


def rank_binary(vectors):
    pivots = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in pivots:
                vector ^= pivots[pivot]
            else:
                pivots[pivot] = vector
                break
    return len(pivots)


def verify():
    started = process_time()
    result = json.loads((HERE / "codim2_results.json").read_text())
    raw = (HERE / "codim2_generator_matrix.txt").read_bytes()
    assert sha256(raw).hexdigest() == result["matrix_sha256"]
    lines = raw.decode("ascii").splitlines()
    assert len(lines) == 11 and all(len(s) == 64 for s in lines)
    assert all(set(s) <= {"0", "1"} for s in lines)
    rows = [tuple(map(int, s)) for s in lines]
    # Literal column-by-column encoding, independent of integer-word recurrence.
    words = [tuple(sum(rows[r][c] for r in range(11) if (m >> r) & 1) % 2
                   for c in range(64)) for m in range(2048)]
    assert len(set(words)) == 2048
    weights = [sum(word) for word in words]
    expected_distribution = {int(k): v for k, v in result["weight_distribution"].items()}
    assert Counter(weights) == expected_distribution
    assert min(weights[1:]) == 26
    indicator = [int(w == 26) for w in weights]
    size = sum(indicator)
    assert size == result["weight26_message_count"] == 234

    # F(a) = sum_{m: weight(mG)=26} (-1)^(a dot m).
    walsh = indicator.copy()
    half = 1
    while half < 2048:
        for start in range(0, 2048, 2 * half):
            for i in range(start, start + half):
                x, y = walsh[i], walsh[i + half]
                walsh[i], walsh[i + half] = x + y, x - y
        half *= 2
    assert walsh[0] == size
    assert sum(x * x for x in walsh) == 2048 * size
    assert Counter(walsh[1:]) == {int(k): v for k, v in result["nonzero_dual_character_sum_histogram"].items()}
    assert min(walsh[1:]) == result["minimum_nonzero_dual_character_sum"] == -30
    assert max(walsh[1:]) == result["maximum_nonzero_dual_character_sum"] == 48
    assert [a for a in range(1, 2048) if walsh[a] == -30] == result["dual_vectors_with_minimum_character_sum"]
    assert (size + 7 * min(walsh[1:])) // 8 == result["dimension8_weight26_count_certified_lower_bound"] == 3
    assert result["maximum_intersection_dimension_with_any_distance_at_least27_code"] == 7

    histogram = Counter()
    minimum = size + 1
    minimizing_spaces = []
    # Every rank-2 row space has one RREF matrix (leftmost = lowest index bit).
    # Its pivot columns are p<q. Row 1 has pivot p, row 2 has pivot q.
    for p, q in combinations(range(11), 2):
        first_free = [i for i in range(p + 1, 11) if i != q]
        first_rows = [(1 << p) | sum(((x >> j) & 1) << i
                                    for j, i in enumerate(first_free))
                      for x in range(1 << len(first_free))]
        second_rows = [(1 << q) | (x << (q + 1))
                       for x in range(1 << (10 - q))]
        for a in first_rows:
            for b in second_rows:
                numerator = size + walsh[a] + walsh[b] + walsh[a ^ b]
                assert numerator % 4 == 0
                count = numerator // 4
                assert 0 <= count <= size
                histogram[count] += 1
                if count < minimum:
                    minimum = count
                    minimizing_spaces = []
                if count == minimum:
                    minimizing_spaces.append(sorted([a, b, a ^ b]))
    assert sum(histogram.values()) == result["enumerated_dual_dimension2_subspaces"] == 698027
    assert histogram == {int(k): v for k, v in result["intersection_histogram"].items()}
    assert minimum == result["minimum_weight26_words_in_dimension9_subcode"] == 36
    assert max(histogram) == result["maximum_weight26_words_in_dimension9_subcode"] == 87
    assert sorted(minimizing_spaces) == result["minimizing_dual_subspaces_nonzero_messages"]
    assert len(minimizing_spaces) == result["count_achieving_minimum"] == 125
    assert sum(n * v for n, v in histogram.items()) == result["first_incidence_moment"] == size * 174251
    assert sum(n * (n - 1) // 2 * v for n, v in histogram.items()) == result["second_binomial_incidence_moment"] == size * (size - 1) // 2 * 43435

    example = result["first_minimizer"]
    a, b = example["dual_basis"]
    assert a and b and a != b
    assert sorted([a, b, a ^ b]) == example["dual_nonzero_messages"] == [41, 460, 485]
    kernel = [m for m in range(2048) if not ((a & m).bit_count() % 2)
              and not ((b & m).bit_count() % 2)]
    assert len(kernel) == 512
    basis = example["kernel_message_basis"]
    assert len(basis) == rank_binary(basis) == 9
    assert all(m in kernel for m in basis)
    assert ["".join(map(str, words[m])) for m in basis] == example["kernel_generator_rows"]
    assert Counter(weights[m] for m in kernel) == {int(k): v for k, v in example["weight_distribution"].items()}
    assert [m for m in kernel if weights[m] == 26] == example["weight26_messages"]
    assert len(example["weight26_messages"]) == 36
    print("PASS: independent literal-coordinate encoding and rank check.")
    print("PASS: character-sum certificate F(a) >= -30 for all nonzero a.")
    print("PASS: codimension-3 orthogonality lower bound (234-210)/8 = 3.")
    print("PASS: Walsh-transform/RREF enumeration of all 698,027 dual 2-spaces.")
    print("PASS: complete intersection histogram and all 125 minimizing dual spaces.")
    print("PASS: minimum 36, maximum 87, both incidence identities.")
    print("PASS: explicit sharp dimension-9 example, basis and full weight distribution.")
    print(f"CPU seconds: {process_time() - started:.6f}.")


if __name__ == "__main__":
    verify()
