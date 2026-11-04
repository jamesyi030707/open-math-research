#!/usr/bin/env python3
"""Audit the 2026-11-04 affine lattice transport using only Python's standard library.

No import or execution of build_model.py, verify_model.py, or affine_split.py.
The default model directory is this script's directory, for public distribution
beside lattice_certificate.json. Use --model PATH for a separate artifact tree.
An optional --prior-table PATH checks a separately held copy of the pinned source.
This is an exact symbolic check, not a parameter-domain enumeration or solver.
"""
import argparse
import csv
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import time

PIN = 'c49805f554e88c468d92d1835fb19f47480295a95eb32f5c18e53db05277323c'
OLD = ['p', 'q', 'y10', 'y14', 'z8', 'z12', 'z16']
NEW = list('abcdefg')

def require(condition, message):
    if not condition:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def expression(constant=0, **terms):
    """Constant-first affine row in the variable order currently named by AXES."""
    require(set(terms) <= set(AXES), 'Unknown polynomial variable')
    return tuple(Q(constant) if j == 0 else Q(terms.get(AXES[j-1], 0)) for j in range(8))

def substitute(row, replacements):
    # This explicitly retains the constant in an affine composition.
    return tuple((row[0] if j == 0 else Q(0)) +
                 sum(row[k+1] * replacements[k][j] for k in range(7))
                 for j in range(8))

def linear_combination(rows, weights):
    return tuple(sum(row[j] * weight for row, weight in zip(rows, weights)) for j in range(8))

def divided(row, denominator):
    return tuple(v / denominator for v in row)

def read_rows(path, fields):
    with path.open(newline='') as source:
        reader = csv.DictReader(source)
        require(reader.fieldnames == fields, 'Unexpected CSV columns: ' + path.name)
        return list(reader)

def constant_last(row):
    return list(row[1:]) + [row[0]]

def determinant_by_definition(matrix):
    """Leibniz determinant over 7! permutations; no floating-point elimination."""
    total = 0
    for permutation in itertools.permutations(range(7)):
        inversions = sum(permutation[i] > permutation[j] for i in range(7) for j in range(i+1, 7))
        term = -1 if inversions % 2 else 1
        for i, j in enumerate(permutation):
            term *= matrix[i][j]
        total += term
    return total

def main():
    global AXES
    started = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--prior-table', type=Path)
    parser.add_argument('--source-dir', type=Path)
    parser.add_argument('--integrality-certificate', type=Path)
    args = parser.parse_args()
    root = args.model
    source_dir = args.source_dir or root.parent / '2026-10-29'
    prior_path = args.integrality_certificate or root.parent / '2026-11-03/certificate.json'
    table_path = source_dir / 'affine_coefficients.csv'
    require(digest(table_path) == PIN, 'Pinned source table SHA-256 mismatch')
    if args.prior_table:
        require(digest(args.prior_table) == PIN, 'Separately held prior table SHA-256 mismatch')
        require(args.prior_table.read_bytes() == table_path.read_bytes(), 'Prior/source bytes differ')

    # Build the forward affine forms directly from the published formulas,
    # independently of the supplied generator and certificate matrices.
    AXES = NEW
    forward = [
        expression(4, a=64, b=-16, d=4, e=-4, f=-6, g=-6),
        expression(d=4),
        expression(6, c=8, d=-4, e=2, g=2),
        expression(-4, b=16, c=-16, e=-4, g=-4),
        expression(f=2, g=1),
        expression(e=2, g=1),
        expression(g=1),
    ]
    new_unit_rows = [expression(**{name: 1}) for name in NEW]
    AXES = OLD
    # Residuals are the six literal congruences in the 2026-11-03 README.
    residuals = [
        expression(-12, p=1, q=1, y10=2, y14=1, z8=3, z12=2, z16=1),
        expression(-8, q=2, y10=2, y14=1),
        expression(-6, q=1, y10=1, z12=-1, z16=-1),
        expression(q=1, z8=2, z16=2),
        expression(z12=1, z16=1),
        expression(z8=1, z16=1),
    ]
    moduli = [64, 16, 8, 4, 2, 2]
    inverse_numerators = residuals[:3] + [
        expression(q=1), expression(z12=1, z16=-1),
        expression(z8=1, z16=-1), expression(z16=1)]
    divisors = [64, 16, 8, 4, 2, 2, 1]
    inverse = [divided(row, d) for row, d in zip(inverse_numerators, divisors)]
    old_unit_rows = [expression(**{name: 1}) for name in OLD]

    # These exact identities establish integrality of every inverse coordinate
    # for a tuple satisfying the six original congruences. In particular,
    # residual_4 - 2*residual_6 = q, and subtracting 2*z16 preserves parity.
    require(inverse_numerators[3] == linear_combination([residuals[3], residuals[5]], [1, -2]),
            'q/4 is not implied by original residuals')
    for index, residue in [(4, residuals[4]), (5, residuals[5])]:
        require(inverse_numerators[index] == linear_combination([residue, old_unit_rows[6]], [1, -2]),
                'Parity quotient is not implied by original residuals')
    for row, modulus in zip(residuals, moduli):
        require(all(v.denominator == 1 and v.numerator % modulus == 0
                    for v in substitute(row, forward)), 'Forward image fails a congruence')
    require([substitute(row, forward) for row in inverse] == new_unit_rows, 'Inverse after forward fails')
    require([substitute(row, inverse) for row in forward] == old_unit_rows, 'Forward after inverse fails')
    det = determinant_by_definition([row[1:] for row in forward])
    require(det == 131072, 'Incorrect determinant')

    certificate = json.loads((root / 'lattice_certificate.json').read_text())
    require(certificate['format_version'] == 1, 'Unknown certificate format')
    require(certificate['old_columns'] == OLD + ['constant'], 'Old columns differ')
    require(certificate['new_columns'] == NEW + ['constant'], 'New columns differ')
    affine_identity_tail = [0]*7 + [1]
    require(certificate['forward_matrix'] == [constant_last(row) for row in forward] + [affine_identity_tail],
            'Certificate forward matrix differs from formulas')
    require(certificate['inverse_numerators'] == [constant_last(row) for row in inverse_numerators] + [affine_identity_tail],
            'Certificate inverse differs from independently reconstructed inverse')
    require(certificate['inverse_divisors'] == divisors + [1], 'Certificate inverse divisors differ')
    require(certificate['lattice_index'] == abs(det), 'Certificate lattice index differs')
    for name, path in [('affine_coefficients.csv', table_path),
                       ('affine_split.py', source_dir / 'affine_split.py'),
                       ('integrality_certificate.json', prior_path)]:
        require(digest(path) == certificate['source_sha256'][name], 'Source hash mismatch: ' + name)
    for name, expected in certificate['files_sha256'].items():
        require(digest(root / name) == expected, 'Certificate file hash mismatch: ' + name)

    # Recheck the prior modular certificate against the pinned source,
    # rather than taking integrality equivalence as an unchecked premise.
    source = read_rows(table_path, ['i', 'j', 'constant'] + OLD + ['denominator'])
    require(len(source) == 1064, 'Wrong source row count')
    positions = [(int(row['i']), int(row['j'])) for row in source]
    require(positions == list(itertools.product(range(28), range(38))), 'Source cell coverage differs')
    require(all(int(row['denominator']) == 1024 for row in source), 'Denominator differs')
    numerators = [tuple(Q(int(row[key])) for key in ['constant'] + OLD) for row in source]
    require(all(v.denominator == 1 and v.numerator % 16 == 0 for row in numerators for v in row),
            'Prior common-divisor reduction fails')
    A = [[int(v / 16) % 64 for v in constant_last(row)] for row in numerators]
    prior = json.loads(prior_path.read_text())
    require(prior['input_sha256'] == PIN and prior['columns'] == OLD + ['constant'], 'Prior provenance differs')
    require((prior['original_modulus'], prior['common_divisor'], prior['modulus']) == (1024, 16, 64),
            'Prior modular problem differs')
    B, U, V = prior['basis'], prior['basis_from_input_sparse'], prior['input_from_basis']
    require(len(B) == len(U) == 6 and len(V) == 1064, 'Prior witness dimensions differ')
    require(all(len(row) == 8 for row in B) and all(len(row) == 6 for row in V), 'Prior witness row dimensions differ')
    expected_basis = [[int(v * (64 // m)) % 64 for v in constant_last(row)]
                      for row, m in zip(residuals, moduli)]
    require([[v % 64 for v in row] for row in B] == expected_basis, 'Prior basis does not encode six literal congruences')
    for b, terms in zip(B, U):
        require(all(type(i) is int and 0 <= i < 1064 and type(c) is int for i, c in terms), 'Invalid sparse prior witness')
        for column in range(8):
            require((sum(c * A[i][column] for i, c in terms) - b[column]) % 64 == 0, 'Prior B=UA identity fails')
    for a, weights in zip(A, V):
        require(all(type(v) is int for v in weights), 'Noninteger prior reverse witness')
        for column in range(8):
            require((sum(weights[i] * B[i][column] for i in range(6)) - a[column]) % 64 == 0,
                    'Prior A=VB identity fails')

    transported = read_rows(root / 'integer_coefficients.csv', ['i', 'j', 'constant'] + NEW)
    require(len(transported) == 1064, 'Wrong transported row count')
    require([(int(row['i']), int(row['j'])) for row in transported] == positions, 'Transported cell labels differ')
    transport_rows = [tuple(Q(int(row[key])) for key in ['constant'] + NEW) for row in transported]
    for position, original, saved in zip(positions, numerators, transport_rows):
        expected = divided(substitute(original, forward), 1024)
        require(all(v.denominator == 1 for v in expected), 'A transported affine coefficient is noninteger')
        require(saved == expected, 'Transported row differs: ' + str(position))
        require(substitute(saved, inverse) == divided(original, 1024), 'Reverse row transport differs: ' + str(position))

    # Construct all eleven original halfspaces independently from their meaning.
    domain = [
        ('p_lower', expression(p=1)), ('p_upper', expression(80, p=-1)),
        ('q_lower', expression(q=1)), ('q_upper', expression(31, q=-1)),
        ('y10_lower', expression(y10=1)), ('y14_lower', expression(y14=1)),
        ('y_sum_upper', expression(160, y10=-1, y14=-1)),
        ('z8_lower', expression(z8=1)), ('z12_lower', expression(z12=1)),
        ('z16_lower', expression(z16=1)), ('z_sum_upper', expression(80, z8=-1, z12=-1, z16=-1)),
    ]
    expected_domain = [{'name': name, 'old_row': constant_last(row)} for name, row in domain]
    require(certificate['domain_inequalities'] == expected_domain, 'Certificate original domain differs')
    saved_domain = read_rows(root / 'domain_inequalities.csv', ['name', 'constant'] + NEW + ['relation'])
    require(len(saved_domain) == 11, 'Wrong domain row count')
    for (name, row), saved in zip(domain, saved_domain):
        require(saved['name'] == name and saved['relation'] == '>=0', 'Domain name or sense differs')
        saved_row = tuple(Q(int(saved[key])) for key in ['constant'] + NEW)
        require(substitute(row, forward) == saved_row, 'Domain transport differs: ' + name)
        require(substitute(saved_row, inverse) == row, 'Domain reverse transport differs: ' + name)

    # A single inherited regression example, not feasibility testing of a domain.
    old_point = (0, 0, 140, 16, 8, 6, 64)
    evaluate = lambda row, point: row[0] + sum(v * x for v, x in zip(row[1:], point))
    point = tuple(evaluate(row, old_point) for row in inverse)
    require(point == (6, 18, 8, 0, -29, -28, 64), 'Regression inverse differs')
    require(all(evaluate(row, old_point) >= 0 for _, row in domain), 'Regression point outside original domain')
    require(all(evaluate(row, old_point) % modulus == 0 for row, modulus in zip(residuals, moduli)),
            'Regression point fails congruences')
    negative_cells = [[*position, int(evaluate(row, point))] for position, row in zip(positions, transport_rows)
                      if evaluate(row, point) < 0]
    require(negative_cells == [[1,2,-16], [1,35,-16], [3,1,-1], [3,36,-1],
                               [24,1,-1], [24,36,-1], [26,2,-16], [26,35,-16]], 'Regression negative cells differ')
    report = {
        'audit_passed': True,
        'source_sha256': PIN,
        'separately_held_prior_table_compared': args.prior_table is not None,
        'prior_modular_certificate_rechecked': True,
        'bijection_target': 'The integer solutions of the six original congruences, not all of Z^7.',
        'both_symbolic_affine_compositions_are_identity': True,
        'forward_image_and_inverse_integrality_checked': True,
        'linear_determinant': int(det),
        'lattice_index': int(abs(det)),
        'transported_integer_affine_rows': 1064,
        'transported_integer_affine_entries': 8512,
        'transported_domain_halfspaces': 11,
        'regression_coordinates': [int(v) for v in point],
        'regression_negative_cells': negative_cells,
        'solver_or_domain_enumeration_used': False,
        'scope': 'Exact representation and transport only. No feasibility decision or code existence/exclusion claim.',
        'elapsed_seconds': round(time.perf_counter() - started, 6),
    }
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
