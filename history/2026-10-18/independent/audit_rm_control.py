#!/usr/bin/env python3
"""Audit the downloaded RM-only OPB control and its planted near-codeword.

Uses the independent auditor's parser and GF(2) polynomial-convolution code.
Never imports the downloaded generator/verifier and never invokes a solver.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from audit_fixed_opb import independent_code, parse_opb, require, value


def integer(word):
    return sum(bit * 2 ** i for i, bit in enumerate(word))


def audit(path):
    raw = path.read_bytes()
    nvars, parsed, source_rows, equality_rows = parse_opb(raw.decode("ascii"), allow_equality=True)
    require(nvars == 69 and source_rows == 129 and equality_rows == 1 and len(parsed) == 130,
            "Expected 69 variables, 128 distance rows, and one parity equality")
    words = independent_code()
    code = {integer(word) for word in words}
    rm_words = [word for word in words if sum(word) in (0, 32, 64)]
    rm = {integer(word) for word in rm_words}
    require(len(rm) == 128, "Expected 128 words in the RM control")
    require(all(a ^ b in rm for a in rm for b in rm), "RM weight layers are not a subspace")
    one = (1 << 64) - 1
    basis = [one]
    span = {0, one}
    for word in sorted(rm):
        if word not in span:
            basis.append(word)
            span.update({v ^ word for v in span})
    require(len(basis) == 7 and span == rm, "Expected seven-dimensional RM subspace")
    coordinate_labels = {tuple((b >> i) & 1 for b in basis[1:]) for i in range(64)}
    require(len(coordinate_labels) == 64, "RM coordinate labels are not all of F_2^6")
    # The all-ones generator plus six generators whose 64 column labels are
    # exactly F_2^6 proves this subcode is RM(1,6) up to coordinate relabeling.
    expected = [({i + 1: 1 - 2 * word[i] for i in range(64)}, 27 - sum(word))
                for word in rm_words]
    parity = {i: 1 for i in range(1, 65)}
    parity.update({i: -(2 ** (i - 64)) for i in range(65, 70)})
    expected += [(parity, 1), ({i: -v for i, v in parity.items()}, -1)]
    signature = lambda row: (tuple(sorted(row[0].items())), row[1])
    require(Counter(map(signature, expected)) == Counter(map(signature, parsed)),
            "RM control constraints do not match independent expectations")
    q1 = int("172e5cb972e5cb97", 16)
    require(q1 in code, "Supplied q1 is not a word of E")
    f = q1 ^ 1
    weight = f.bit_count()
    require(weight % 2 == 1, "Planted word is not odd")
    t = (weight - 1) // 2
    assignment = tuple((f >> i) & 1 for i in range(64)) + tuple((t >> i) & 1 for i in range(5))
    require(all(value(terms, assignment) >= rhs for terms, rhs in parsed), "Planted word fails RM OPB")
    rm_distance = min((f ^ word).bit_count() for word in rm)
    full_distance = min((f ^ word).bit_count() for word in code)
    require(rm_distance == 27 and full_distance == 1, "Unexpected planted-word distances")
    prefix = f & 1023
    normalizer = next(word for word in code if word & 1023 == prefix)
    reduced = f ^ normalizer
    require(reduced & 1023 == 0, "Gauge normalization failed")
    require(reduced.bit_count() % 2 == 1, "Gauge changed oddness")
    reduced_distances = {(reduced ^ word).bit_count() for word in code}
    require(min(reduced_distances) == 1, "Gauge changed code distance")
    violated = sum((reduced ^ word).bit_count() < 27 for word in code)
    require(violated == 1, "Expected exactly one failed full-code distance row")
    return {
        "status": "PASS",
        "input": str(path),
        "opb_sha256": hashlib.sha256(raw).hexdigest(),
        "opb_bytes": len(raw),
        "variables": nvars,
        "source_rows": source_rows,
        "independent_exact_distance_rows": 128,
        "independent_exact_distance_coefficients": 128 * 64,
        "rm_dimension": len(basis),
        "rm_closure_pairs_checked": 128 * 128,
        "rm_six_bit_coordinate_labels": len(coordinate_labels),
        "q1_hex": hex(q1),
        "q1_weight": q1.bit_count(),
        "f_hex": hex(f),
        "f_weight": weight,
        "parity_auxiliary_t": t,
        "distance_to_RM": rm_distance,
        "distance_to_E": full_distance,
        "rm_opb_witness_satisfies_every_row": True,
        "gauge_normalizer_hex": hex(normalizer),
        "gauged_f_hex": hex(reduced),
        "gauged_f_weight": reduced.bit_count(),
        "gauged_f_full_code_distance": min(reduced_distances),
        "gauged_f_full_model_distance_rows_violated": violated,
        "solver_invoked": False,
        "full_problem_status": "NOT DETERMINED",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("opb", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = audit(args.opb)
    rendered = json.dumps(result, indent=2) + "\n"
    if args.report:
        args.report.write_text(rendered, encoding="ascii")
    print(rendered, end="")


if __name__ == "__main__":
    main()
