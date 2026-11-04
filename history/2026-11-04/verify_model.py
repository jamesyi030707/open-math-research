"""Independent exact certificate checker. No generator import, solver or search.

Verifies the prior modular equivalence, all affine coordinate identities,
all original bounds, and all 1,064 transported split coefficients.
"""
import argparse
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OLD = ['p', 'q', 'y10', 'y14', 'z8', 'z12', 'z16', 'constant']
NEW = list('abcdefg') + ['constant']
INPUT_HASH = 'c49805f554e88c468d92d1835fb19f47480295a95eb32f5c18e53db05277323c'
# Residual expressions, required to vanish modulo the accompanying modulus.
E = [
    ([1, 1, 2, 1, 3, 2, 1, -12], 64),
    ([0, 2, 2, 1, 0, 0, 0, -8], 16),
    ([0, 1, 1, 0, 0, -1, -1, -6], 8),
    ([0, 1, 0, 0, 2, 0, 2, 0], 4),
    ([0, 0, 0, 0, 0, 1, 1, 0], 2),
    ([0, 0, 0, 0, 1, 0, 1, 0], 2),
]


def mul(row, matrix):
    return [sum(row[k] * matrix[k][j] for k in range(len(row)))
            for j in range(len(matrix[0]))]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant(matrix):
    """Exact rational elimination on one 7 by 7 matrix, not domain search."""
    work = [[Fraction(v) for v in row] for row in matrix]
    answer = Fraction(1)
    for j in range(len(work)):
        pivot = next((i for i in range(j, len(work)) if work[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            work[j], work[pivot] = work[pivot], work[j]
            answer = -answer
        answer *= work[j][j]
        for i in range(j + 1, len(work)):
            scale = work[i][j] / work[j][j]
            work[i] = [x - scale * y for x, y in zip(work[i], work[j])]
    assert answer.denominator == 1
    return int(answer)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, default=ROOT.parent / '2026-10-29')
    parser.add_argument('--integrality-certificate', type=Path,
                        default=ROOT.parent / '2026-11-03/certificate.json')
    args = parser.parse_args()
    cert = json.loads((ROOT / 'lattice_certificate.json').read_text())
    assert cert['format_version'] == 1
    assert cert['old_columns'] == OLD and cert['new_columns'] == NEW
    for name, digest in cert['files_sha256'].items():
        assert sha(ROOT / name) == digest, name
    for key, path in {
        'affine_coefficients.csv': args.source_dir / 'affine_coefficients.csv',
        'affine_split.py': args.source_dir / 'affine_split.py',
        'integrality_certificate.json': args.integrality_certificate,
    }.items():
        assert sha(path) == cert['source_sha256'][key]
    data = (args.source_dir / 'affine_coefficients.csv').read_bytes()
    assert hashlib.sha256(data).hexdigest() == INPUT_HASH
    source_rows = list(csv.DictReader(data.decode().splitlines()))
    positions = [(int(r['i']), int(r['j'])) for r in source_rows]
    assert positions == [(i, j) for i in range(28) for j in range(38)]
    assert all(int(r['denominator']) == 1024 for r in source_rows)
    A = [[int(r[k]) for k in OLD] for r in source_rows]
    assert all(v % 16 == 0 for r in A for v in r)
    A64 = [[v // 16 % 64 for v in r] for r in A]
    prior = json.loads(args.integrality_certificate.read_text())
    assert prior['input_sha256'] == INPUT_HASH and prior['columns'] == OLD
    assert (prior['original_modulus'], prior['common_divisor'], prior['modulus']) == (1024, 16, 64)
    B, U, V = prior['basis'], prior['basis_from_input_sparse'], prior['input_from_basis']
    assert len(B) == len(U) == 6 and len(V) == 1064
    assert all(len(r) == 8 for r in B) and all(len(r) == 6 for r in V)
    for b, u in zip(B, U):
        assert all(0 <= i < 1064 and isinstance(c, int) for i, c in u)
        assert all((sum(c * A64[i][j] for i, c in u) - b[j]) % 64 == 0 for j in range(8))
    for a, v in zip(A64, V):
        assert all((sum(v[i] * B[i][j] for i in range(6)) - a[j]) % 64 == 0 for j in range(8))
    for (e, m), b in zip(E, B):
        assert all((v * (64 // m) - w) % 64 == 0 for v, w in zip(e, b))

    F, N, D = cert['forward_matrix'], cert['inverse_numerators'], cert['inverse_divisors']
    assert len(F) == len(N) == len(D) == 8
    assert all(len(row) == 8 and all(isinstance(x, int) for x in row) for row in F + N)
    assert D == [64, 16, 8, 4, 2, 2, 1, 1]
    assert F[-1] == N[-1] == [0] * 7 + [1]
    # Check the inverse numerators are precisely the stated congruence quotients.
    assert N[:3] == [e for e, m in E[:3]]
    assert N[3] == [x - 2 * y for x, y in zip(E[3][0], E[5][0])]
    twice_z16 = [0, 0, 0, 0, 0, 0, 2, 0]
    assert N[4] == [x - y for x, y in zip(E[4][0], twice_z16)]
    assert N[5] == [x - y for x, y in zip(E[5][0], twice_z16)]
    assert N[6] == [0, 0, 0, 0, 0, 0, 1, 0]
    G = [[Fraction(v, d) for v in row] for row, d in zip(N, D)]
    for i in range(8):
        identity = [int(i == j) for j in range(8)]
        assert mul(G[i], F) == identity
        assert mul(F[i], G) == identity
    for e, m in E:
        assert all(v % m == 0 for v in mul(e, F))
    det = determinant([r[:7] for r in F[:7]])
    assert abs(det) == cert['lattice_index'] == 2 ** 17

    transformed = list(csv.DictReader((ROOT / 'integer_coefficients.csv').open()))
    assert len(transformed) == 1064
    assert [(int(r['i']), int(r['j'])) for r in transformed] == positions
    T = [[int(r[k]) for k in NEW] for r in transformed]
    for original, transported in zip(A, T):
        assert mul(original, F) == [1024 * v for v in transported]
        # Independently check transport back, with the affine constant retained.
        assert mul(transported, G) == [Fraction(v, 1024) for v in original]

    # Construct exactly the original eleven halfspaces from their definitions.
    domain = []
    for j, name, cap in [(0, 'p', 80), (1, 'q', 31)]:
        row = [0] * 8
        row[j] = 1
        domain.append((name + '_lower', row))
        domain.append((name + '_upper', [-v for v in row[:7]] + [cap]))
    for j, name in [(2, 'y10'), (3, 'y14')]:
        row = [0] * 8
        row[j] = 1
        domain.append((name + '_lower', row))
    domain.append(('y_sum_upper', [0, 0, -1, -1, 0, 0, 0, 160]))
    for j, name in [(4, 'z8'), (5, 'z12'), (6, 'z16')]:
        row = [0] * 8
        row[j] = 1
        domain.append((name + '_lower', row))
    domain.append(('z_sum_upper', [0, 0, 0, 0, -1, -1, -1, 80]))
    assert cert['domain_inequalities'] == [{'name': n, 'old_row': r} for n, r in domain]
    bounds = list(csv.DictReader((ROOT / 'domain_inequalities.csv').open()))
    assert len(bounds) == 11
    for (name, row), result in zip(domain, bounds):
        assert result['name'] == name and result['relation'] == '>=0'
        assert mul(row, F) == [int(result[k]) for k in NEW]

    # One inherited regression example, not a search or a feasible witness.
    old = [0, 0, 140, 16, 8, 6, 64, 1]
    coordinates = [sum(x * y for x, y in zip(row, old)) for row in G]
    assert coordinates == [6, 18, 8, 0, -29, -28, 64, 1]
    assert all(sum(x * y for x, y in zip(row, old)) >= 0 for _, row in domain)
    values = [sum(x * y for x, y in zip(row, coordinates)) for row in T]
    negatives = [[i, j, int(value)] for (i, j), value in zip(positions, values) if value < 0]
    assert len(negatives) == 8 and [1, 2, -16] in negatives and [3, 1, -1] in negatives

    # Regenerate source independently, using its full original model checks.
    regenerated = subprocess.run([sys.executable, str(args.source_dir / 'affine_split.py'), '--table'],
                                 check=True, capture_output=True, timeout=60)
    assert regenerated.stdout == data
    result = {
        'verified': True, 'source_regeneration_identical': True,
        'prior_congruence_forward_entries': 48, 'prior_congruence_reverse_entries': 8512,
        'coordinate_round_trip_entries': 128, 'integer_image_congruence_entries': 48,
        'lattice_determinant': det, 'lattice_index': abs(det),
        'transported_table_rows': 1064, 'transported_affine_entries': 8512,
        'transported_domain_halfspaces': 11, 'total_preserved_nonnegativity_halfspaces': 1075,
        'regression_coordinates': [int(v) for v in coordinates[:7]],
        'regression_negative_cells': negatives,
        'scope': 'Exact fixed-model reformulation only; no feasibility decision, search, or code-existence claim.',
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
