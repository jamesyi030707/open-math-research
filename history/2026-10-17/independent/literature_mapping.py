#!/usr/bin/env python3
"""Small exact checks for the BCH/Norm-map identification; no radius search."""
import json

MODULUS = 0x43  # X^6 + X + 1
GENERATOR = 0x2759262D5D506D
ALPHA = 2


def mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 64:
            a ^= MODULUS
    return result


def power(a, exponent):
    result = 1
    while exponent:
        if exponent & 1:
            result = mul(result, a)
        a = mul(a, a)
        exponent >>= 1
    return result


def polynomial_value(polynomial, a):
    result = 0
    for i in range(polynomial.bit_length() - 1, -1, -1):
        result = mul(result, a) ^ ((polynomial >> i) & 1)
    return result


def trace(a, degree):
    result = 0
    for _ in range(degree):
        result ^= a
        a = mul(a, a)
    assert result in (0, 1)
    return result


def row_basis(rows):
    pivots = {}
    for row in rows:
        while row:
            position = row.bit_length() - 1
            if position in pivots:
                row ^= pivots[position]
            else:
                pivots[position] = row
                break
    return pivots


def in_span(row, pivots):
    while row:
        position = row.bit_length() - 1
        if position not in pivots:
            return False
        row ^= pivots[position]
    return True


def main():
    nonzero_points = [power(ALPHA, i) for i in range(63)]
    assert len(set(nonzero_points)) == 63
    roots = [j for j in range(63)
             if polynomial_value(GENERATOR, power(ALPHA, j)) == 0]
    missing = sorted(set(range(63)) - set(roots))
    support = [0, 1, 2, 4, 8, 16, 32, 9, 18, 36]
    expected_missing = sorted({(-e) % 63 for e in support})
    assert missing == expected_missing
    assert set(range(1, 27)) <= set(roots)
    subfield = [a for a in range(64) if power(a, 8) == a]
    gamma_basis = []
    for a in subfield:
        if a and not in_span(a, row_basis(gamma_basis)):
            gamma_basis.append(a)
    assert len(gamma_basis) == 3
    points = nonzero_points + [0]
    assert all(power(power(y, 36), 8) == power(y, 36) for y in points)
    assert all(power(y, 36) == power(power(y, 9), 4) for y in points)

    # Paper Eq. (1.1), with trace-dual input/output coordinate bases.
    trace_rows = [(1 << 64) - 1]
    for a in [1 << i for i in range(6)]:
        trace_rows.append(sum(trace(mul(a, y), 6) << i
                              for i, y in enumerate(points)))
    for gamma in gamma_basis:
        trace_rows.append(sum(trace(mul(gamma, power(y, 36)), 3) << i
                              for i, y in enumerate(points)))
    trace_span = row_basis(trace_rows)
    bch_rows = []
    for i in range(10):
        row = GENERATOR << i
        bch_rows.append(row | ((row.bit_count() & 1) << 63))
    bch_span = row_basis(bch_rows)
    assert len(trace_span) == len(bch_span) == 10
    spans_equal = (all(in_span(row, bch_span) for row in trace_rows)
                   and all(in_span(row, trace_span) for row in bch_rows))
    assert spans_equal
    assert all(row.bit_count() % 2 == 0 for row in trace_rows)

    result = {
        "field_modulus_hex": hex(MODULUS),
        "primitive_element": ALPHA,
        "primitive_order": len(set(nonzero_points)),
        "generator_hex": hex(GENERATOR),
        "generator_degree": GENERATOR.bit_length() - 1,
        "root_count": len(roots),
        "contains_roots_1_through_26": True,
        "nonroot_exponents": missing,
        "negative_trace_support_exponents": expected_missing,
        "gf8_elements_in_gf64_polynomial_basis": subfield,
        "gf8_gamma_basis": gamma_basis,
        "map_y36_equals_norm_y9_fourth_power": True,
        "trace_evaluation_rank": len(trace_span),
        "extended_bch_rank": len(bch_span),
        "trace_and_extended_bch_row_spaces_equal": spans_equal,
        "coordinate_order": "alpha^0,...,alpha^62,0 (parity at final coordinate)",
        "covering_radius_computed": False,
        "odd_coset_minimum_27_excluded": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
