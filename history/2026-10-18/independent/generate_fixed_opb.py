#!/usr/bin/env python3
"""Generate the exact fixed-code odd-coset OPB feasibility instance.

Python standard library only.  No solver and no imported audit code.
Coordinates and polynomial exponents are zero based; OPB variable names are
one based.  The output is deterministic ASCII with LF newlines.
"""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


N = 64
K = 10
G = 0x2759262D5D506D
TARGET = 27
FREE_COORDS = tuple(range(K, N))
PARITY_BITS = 5


def codewords():
    basis = []
    for shift in range(K):
        word = G << shift
        if word >= 1 << (N - 1):
            raise ValueError("Polynomial shift reaches the reserved parity bit")
        basis.append(word | ((word.bit_count() & 1) << (N - 1)))
    words = []
    for message in range(1 << K):
        word = 0
        for j, row in enumerate(basis):
            if message & (1 << j):
                word ^= row
        words.append(word)
    return basis, words


def format_row(coefficients, rhs):
    return " ".join(f"{c:+d} x{v}" for v, c in coefficients) + f" >= {rhs};"


def generate(compact=False):
    basis, words = codewords()
    parity_bits = 3 if compact else PARITY_BITS
    parity_offset = 27 if compact else 1
    variable_count = 54 + parity_bits
    if len(set(words)) != 1024:
        raise ValueError("The basis does not have rank ten")
    if {w & 1023 for w in words} != set(range(1024)):
        raise ValueError("Coordinates 0..9 are not an information set")
    if any(w.bit_count() % 2 for w in words):
        raise ValueError("The code is not even")
    if min(w.bit_count() for w in words if w) != 28:
        raise ValueError("Unexpected minimum distance")
    lines = [
        f"* #variable= {variable_count} #constraint= 1026",
        "* Fixed binary E=[64,10,28]; generator polynomial 0x2759262d5d506d.",
        "* Polynomial bit i means x^i; extended parity occupies coordinate 63.",
        "* Gauge: f_0=...=f_9=0, eliminated, not solver variables.",
        f"* OPB x1..x54 = f_10..f_63; x55..x{variable_count} = auxiliary binary bits.",
        f"* a=sum(2^j a_j), sum(f)-2a={parity_offset}. Every OPB variable is Boolean.",
        "* Zero and all-ones codeword rows imply 27<=sum(f)<=37.",
        "* Rows 1..1024 use message masks 0..1023 in increasing order.",
        "* Rows 1025..1026 are the two directions of the parity equality.",
    ]
    for word in words:
        coefficients = [
            (index + 1, 1 - 2 * ((word >> coordinate) & 1))
            for index, coordinate in enumerate(FREE_COORDS)
        ]
        lines.append(format_row(coefficients, TARGET - word.bit_count()))
    parity = [(v, 1) for v in range(1, 55)] + [
        (55 + j, -(1 << (j + 1))) for j in range(parity_bits)
    ]
    lines.append(format_row(parity, parity_offset))
    lines.append(format_row([(v, -c) for v, c in parity], -parity_offset))
    output = ("\n".join(lines) + "\n").encode("ascii")
    manifest = {
        "format": "OPB feasibility; Boolean variables; no objective",
        "n": N,
        "dimension": K,
        "minimum_distance": 28,
        "generator_polynomial_hex": hex(G),
        "basis_hex": [f"0x{w:016x}" for w in basis],
        "coordinate_convention": "least-significant bit is coordinate 0",
        "distance_threshold": TARGET,
        "gauge_zero_coordinates": list(range(10)),
        "variables": variable_count,
        "distance_inequalities": 1024,
        "parity_inequalities": 2,
        "total_inequalities": 1026,
        "auxiliary_integer_range": [0, (1 << parity_bits) - 1],
        "parity_offset": parity_offset,
        "weight_enumerator": dict(sorted(Counter(w.bit_count() for w in words).items())),
        "opb_sha256": hashlib.sha256(output).hexdigest(),
        "opb_bytes": len(output),
        "claim_scope": "Exact encoding only; no satisfiability or nonexistence claim.",
    }
    return output, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--compact", action="store_true", help="Use 57 variables and sum(f)-2u=27 with a three-bit u")
    args = parser.parse_args()
    stem = "fixed_E_odd_d27_compact57" if args.compact else "fixed_E_odd_d27"
    args.output = args.output or Path(stem + ".opb")
    args.manifest = args.manifest or Path(stem + ".manifest.json")
    output, manifest = generate(compact=args.compact)
    args.output.write_bytes(output)
    args.manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="ascii")
    print(json.dumps({"opb": str(args.output), "manifest": str(args.manifest), **manifest}, indent=2))


if __name__ == "__main__":
    main()
