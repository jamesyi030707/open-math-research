"""Independent standard-library verification of the q=24 restriction geometry.

No target-code search. No claim to exclude q=24 or any global code parameter.
"""
from collections import Counter
from itertools import combinations
import json
import time


def require(condition, label):
    if not condition:
        raise ValueError(label)


def rank(vectors):
    basis = {}
    for value in vectors:
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def parity(value):
    return value.bit_count() & 1


start = time.process_time()
seven_sets_tested = 0
admissible_sets = 0
for points in combinations(range(1, 32), 7):
    seven_sets_tested += 1
    total = 0
    for point in points:
        total ^= point
    if total or rank(points) != 5:
        continue
    admissible_sets += 1
    triangles = [triple for triple in combinations(points, 3)
                 if triple[0] ^ triple[1] ^ triple[2] == 0]
    require(len(triangles) == 1, "unique three-point dependence")
    triangle = triangles[0]
    remainder = [point for point in points if point not in triangle]
    require(rank(triangle) == 2 and rank(remainder) == 3,
            "complementary ranks two and three")
    require(rank(points) == rank(triangle) + rank(remainder),
            "direct sum")

require(seven_sets_tested == 2629575, "all seven-subsets covered")
require(admissible_sets == 69440, "number of classified restrictions")

E = [1, 2, 3, 4, 12, 20, 28]
r = {v: sum(parity(v & point) for point in E) for v in range(1, 32)}
require(all(value in (2, 4, 6) for value in r.values()), "allowed incidence")
m = {v: (value - 2) // 2 for v, value in r.items()}
require(Counter(m.values()) == {0: 9, 1: 19, 2: 3}, "multiplicity type")
singles = [v for v in m if m[v] == 1]
doubles = [v for v in m if m[v] == 2]
require(rank(doubles) == 3, "three repeated labels independent")
columns = singles + [v for v in doubles for _ in range(2)] + [0, 0]
weights = [sum(parity(s & v) for v in columns) for s in range(32)]
require(Counter(weights) == {0: 1, 12: 24, 16: 7}, "canonical spectrum")
require([s for s in range(1, 32) if weights[s] == 16] == E,
        "inverse reconstruction")

# Genuine 27-column affine cosets: all eight opposite-pair patterns,
# all four zero-coordinate patterns, and 64 fixed single-sign patterns.
# This finite control complements, rather than replaces, orthogonality proof.
controls = 0
for single_seed in range(64):
    single_signs = [parity((j + 1) & single_seed) for j in range(19)]
    for opposite_pattern in range(8):
        for zero_pattern in range(4):
            extension = single_signs[:]
            for j in range(3):
                extension += [0, (opposite_pattern >> j) & 1]
            extension += [zero_pattern & 1, zero_pattern >> 1]
            z = zero_pattern.bit_count()
            opposite = opposite_pattern.bit_count()
            coset_weights = [sum(e ^ parity(s & v)
                                 for e, v in zip(extension, columns))
                             for s in range(32)]
            require(sum(coset_weights) == 400 + 32 * z, "coset first moment")
            require(sum((2 * w - 25 - 2 * z) ** 2 for w in coset_weights)
                    == 4 * (248 - 32 * opposite), "coset centered second moment")
            controls += 1

# Necessary first/second moment compatibility with the ten known target
# windows: sixteen forced 14s and sixteen entries chosen from 10,14,18.
window_solutions = {}
for z in range(3):
    for opposite in range(4):
        solutions = []
        for n10 in range(17):
            for n18 in range(17 - n10):
                n14 = 16 - n10 - n18
                ws = [14] * (16 + n14) + [10] * n10 + [18] * n18
                if (sum(ws) == 400 + 32 * z
                    and sum((2 * w - 25 - 2 * z) ** 2 for w in ws)
                    == 4 * (248 - 32 * opposite)):
                    solutions.append([n10, n14, n18])
        window_solutions[f"z={z},r={opposite}"] = solutions
require(not window_solutions["z=0,r=0"]
        and not window_solutions["z=0,r=1"], "z zero forces r at least two")
require(window_solutions["z=0,r=2"] and window_solutions["z=0,r=3"],
        "do not overstate this as z nonzero")

print(json.dumps({
    "scope": "q24 restriction classification and coset moment checks; no q24 exclusion",
    "seven_sets_tested": seven_sets_tested,
    "admissible_sets": admissible_sets,
    "canonical_weight16_messages": E,
    "canonical_active_multiplicities": m,
    "double_column_labels": doubles,
    "double_column_rank": rank(doubles),
    "canonical_columns": columns,
    "affine_coset_controls": controls,
    "target_window_moment_solutions": window_solutions,
    "cpu_seconds": time.process_time() - start,
}, indent=2))
