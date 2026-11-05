#!/usr/bin/env python3
"""Audit one fixed formal split enumerator, using only the standard library.

No solver, discovery module, prior checker, or source-model module is imported
or executed. The numeric primal table is reconstructed explicitly below, and
the Krawtchouk transform uses a recurrence instead of the source's binomial sum.
Default inputs are relative to this file as installed in history/2026-11-05.
"""
import argparse
import csv
import hashlib
import io
import json
from collections import defaultdict
from pathlib import Path


X_NAMES = ("p", "q", "y10", "y14", "z8", "z12", "z16")
U_NAMES = ("a", "b", "c", "d", "e", "f", "g")
X = (28, 0, 100, 32, 4, 62, 0)
U = (6, 14, 4, 0, 31, 2, 0)
PINS = {
    "affine_coefficients.csv": "c49805f554e88c468d92d1835fb19f47480295a95eb32f5c18e53db05277323c",
    "affine_split.py": "b24e554a9a6a17fa79b89b060f7f09107970690ca16a55e163cb3941687fa7dc",
    "integer_coefficients.csv": "0677ea7f6268cf3af33adb979a6c837f4bdd8b3a0b2b244657bd8bc15808c3c0",
    "domain_inequalities.csv": "861e23b73b1a4456d9ba8f6b2d80a7037a71543c9b43fe59762d5810bc99aa14",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned_bytes(directory, name):
    raw = (directory / name).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PINS[name],
            "Pinned SHA-256 mismatch: " + name)
    return raw


def read_csv(directory, name, header):
    reader = csv.DictReader(io.StringIO(pinned_bytes(directory, name).decode("utf-8")))
    require(reader.fieldnames == list(header), "Unexpected columns: " + name)
    return list(reader)


def dot(row, names, values):
    return int(row["constant"]) + sum(int(row[k]) * v for k, v in zip(names, values))


def krawtchouk_sequence(n, w):
    """Coefficients of (1-t)^w(1+t)^(n-w), by a three-term recurrence."""
    require(0 <= w <= n, "Weight outside its block")
    if n == 0:
        return [1]
    result = [1, n - 2 * w]
    for j in range(1, n):
        numerator = (n - 2 * w) * result[j] - (n - j + 1) * result[j - 1]
        require(numerator % (j + 1) == 0, "Nonintegral recurrence")
        result.append(numerator // (j + 1))
    return result


def build_primal():
    p, q, y10, y14, z8, z12, z16 = X
    # A row (r,s,a,count) contributes count at (a,r) AND at (a,s).
    # The contribution is doubled when r == s, not deduplicated.
    groups = [
        (14, 22, 14, 160),
        (16, 24, 12, p),
        (16, 24, 16, 80 - p),
        (16, 16, 12, q),
        (16, 16, 16, 31 - q),
        (18, 18, 10, y10),
        (18, 18, 14, y14),
        (18, 18, 18, 160 - y10 - y14),
        (20, 20, 8, z8),
        (20, 20, 12, z12),
        (20, 20, 16, z16),
        (20, 20, 20, 80 - z8 - z12 - z16),
    ]
    table = defaultdict(int, {(0, 0): 1, (0, 32): 1})
    for r, s, a, count in groups:
        require(count >= 0, "Negative source category")
        table[a, r] += count
        table[a, s] += count
    return dict(table), groups


def csv_bytes(header, rows):
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def audit(source_dir, model_dir):
    pinned_bytes(source_dir, "affine_split.py")  # Provenance only: never execute it.
    old = read_csv(source_dir, "affine_coefficients.csv",
                   ("i", "j", "constant") + X_NAMES + ("denominator",))
    new = read_csv(model_dir, "integer_coefficients.csv",
                   ("i", "j", "constant") + U_NAMES)
    domain_csv = read_csv(model_dir, "domain_inequalities.csv",
                          ("name", "constant") + U_NAMES + ("relation",))
    cells = [(i, j) for i in range(28) for j in range(38)]
    for name, rows in (("original", old), ("transported", new)):
        require([(int(r["i"]), int(r["j"])) for r in rows] == cells,
                "Wrong shape or order in " + name + " table")

    p, q, y10, y14, z8, z12, z16 = X
    a, b, c, d, e, f, g = U
    image = (4 + 64*a - 16*b + 4*d - 4*e - 6*f - 6*g,
             4*d, 6 + 8*c - 4*d + 2*e + 2*g,
             -4 + 16*b - 16*c - 4*e - 4*g, 2*f + g, 2*e + g, g)
    require(image == X, "Forward coordinate mismatch")
    inverse_numerators = (p+q+2*y10+y14+3*z8+2*z12+z16-12,
                          2*q+2*y10+y14-8, q+y10-z12-z16-6,
                          q, z12-z16, z8-z16, z16)
    inverse_denominators = (64, 16, 8, 4, 2, 2, 1)
    require(all(n % m == 0 for n, m in zip(inverse_numerators, inverse_denominators)),
            "Nonintegral inverse coordinate")
    preimage = tuple(n // m for n, m in zip(inverse_numerators, inverse_denominators))
    require(preimage == U, "Inverse coordinate mismatch")

    original_domain = [
        ("p_lower", p), ("p_upper", 80-p),
        ("q_lower", q), ("q_upper", 31-q),
        ("y10_lower", y10), ("y14_lower", y14),
        ("y_sum_upper", 160-y10-y14),
        ("z8_lower", z8), ("z12_lower", z12), ("z16_lower", z16),
        ("z_sum_upper", 80-z8-z12-z16),
    ]
    require(len(domain_csv) == 11, "Expected eleven domain inequalities")
    require(all(r["relation"] == ">=0" for r in domain_csv), "Wrong inequality direction")
    require([(r["name"], dot(r, U_NAMES, U)) for r in domain_csv] == original_domain,
            "Transported domain mismatch")
    require(all(v >= 0 for _, v in original_domain), "Domain inequality failed")
    congruences = [
        ("C1", p+q+2*y10+y14+3*z8+2*z12+z16-12, 64),
        ("C2", 2*q+2*y10+y14-8, 16),
        ("C3", q+y10-z12-z16-6, 8),
        ("C4", q+2*z8+2*z16, 4),
        ("C5", z12+z16, 2),
        ("C6", z8+z16, 2),
    ]
    require(all(v % m == 0 for _, v, m in congruences), "Congruence failed")

    require(all(int(r["denominator"]) == 1024 for r in old), "Wrong denominator")
    numerators = [dot(r, X_NAMES, X) for r in old]
    require(all(v % 1024 == 0 for v in numerators), "Nonintegral original coefficient")
    values = [v // 1024 for v in numerators]
    require(all(v >= 0 for v in values), "Negative original coefficient")
    require([dot(r, U_NAMES, U) for r in new] == values, "Transported table mismatch")
    dual = dict(zip(cells, values))

    primal, groups = build_primal()
    require(sum(primal.values()) == 1024, "Source mass is not 1024")
    left = {w: krawtchouk_sequence(27, w) for w in range(28)}
    right = {w: krawtchouk_sequence(37, w) for w in range(38)}
    direct_numerators = [sum(count * left[r][i] * right[s][j]
                             for (r, s), count in primal.items()) for i, j in cells]
    require(direct_numerators == numerators,
            "Independent numeric primal transform disagrees with original CSV")
    # Orthogonality: applying the unnormalized split transform to the normalized
    # dual must give 2^54 times the primal, including all zero source cells.
    intermediate = {(r, j): sum(left[i][r] * dual[i, j] for i in range(28))
                    for r in range(28) for j in range(38)}
    for r, s in cells:
        recovered = sum(right[j][s] * intermediate[r, j] for j in range(38))
        require(recovered == 2**54 * primal.get((r, s), 0), "Inverse transform failed")
    require(dual[0, 0] == 1 and sum(values) == 2**54, "Dual normalization failed")
    require(all(v == dual[27-i, j] == dual[i, 37-j] for (i, j), v in dual.items()),
            "A block complement symmetry failed")

    ordinary = {w: sum(v for (i, j), v in dual.items() if i+j == w) for w in range(65)}
    ordinary_primal = {w: sum(v for (i, j), v in primal.items() if i+j == w)
                       for w in range(65)}
    k64 = {w: krawtchouk_sequence(64, w) for w in range(65)}
    require(all(1024*ordinary[w] == sum(count*k64[r+s][w]
                                       for (r, s), count in primal.items())
                for w in range(65)), "Ordinary diagonal transform mismatch")

    table_raw = csv_bytes(("i", "j", "original_numerator", "denominator", "coefficient"),
                          [(i, j, n, 1024, v) for (i, j), n, v in zip(cells, numerators, values)])
    primal_raw = csv_bytes(("i", "j", "coefficient"),
                           [(i, j, v) for (i, j), v in sorted(primal.items()) if v])
    result = {
        "status": "pass",
        "scope": "One feasible nonnegative integral formal split enumerator in the fixed model; no code construction or realizability claim.",
        "original_variables": dict(zip(X_NAMES, X)),
        "lattice_variables": dict(zip(U_NAMES, U)),
        "input_sha256": PINS,
        "coordinate_round_trips": {"forward": list(image), "inverse": list(preimage)},
        "domain_slacks": dict(original_domain),
        "congruences": [{"name": n, "value": v, "modulus": m, "remainder": v % m}
                         for n, v, m in congruences],
        "dual": {
            "cells": len(values), "normalization": 1024,
            "nondivisible_numerators": sum(v % 1024 != 0 for v in numerators),
            "negative_coefficients": sum(v < 0 for v in values),
            "zero_coefficients": sum(v == 0 for v in values),
            "positive_coefficients": sum(v > 0 for v in values),
            "sum": sum(values), "numerator_sum": sum(numerators),
            "minimum": min(values), "maximum": max(values),
            "minimum_positive": min(v for v in values if v > 0),
            "minimum_positive_total_weight": min(w for w, v in ordinary.items() if w and v),
            "zero_cells": [[i, j] for (i, j), v in dual.items() if not v],
            "positive_cells_through_total_weight_4": [
                {"i": i, "j": j, "coefficient": v}
                for (i, j), v in dual.items() if i+j <= 4 and v],
            "ordinary_coefficients": [ordinary[w] for w in range(65)],
        },
        "primal": {
            "sum": sum(primal.values()), "positive_cells": sum(v > 0 for v in primal.values()),
            "zero_cells_in_full_grid": 1064-sum(v > 0 for v in primal.values()),
            "category_counts": [row[3] for row in groups],
            "ordinary_nonzero_coefficients": {str(w): v for w, v in ordinary_primal.items() if v},
        },
        "checks": {
            "original_csv_rows": 1064, "transported_csv_rows": 1064,
            "original_domain_inequalities": 11, "original_congruences": 6,
            "numeric_primal_transform_cells": 1064, "inverse_transform_cells": 1064,
            "block_complement_checks": 2128, "ordinary_diagonal_identities": 65,
            "solver_modules_imported": False, "source_model_executed": False,
            "candidate_search_performed": False,
        },
        "output_sha256": {
            "audited_table.csv": hashlib.sha256(table_raw).hexdigest(),
            "audited_primal.csv": hashlib.sha256(primal_raw).hexdigest(),
        },
    }
    return result, table_raw, primal_raw


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=here.parent / "2026-10-29")
    parser.add_argument("--model-dir", type=Path, default=here.parent / "2026-11-04")
    parser.add_argument("--output-dir", type=Path, default=here)
    args = parser.parse_args()
    result, table_raw, primal_raw = audit(args.source_dir, args.model_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "audited_table.csv").write_bytes(table_raw)
    (args.output_dir / "audited_primal.csv").write_bytes(primal_raw)
    (args.output_dir / "audit_result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
