"""Generate exact integer-coordinate transport. Standard library; no search."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD = ['p', 'q', 'y10', 'y14', 'z8', 'z12', 'z16']
NEW = list('abcdefg')
# Column vectors include their constant coordinate last: x_aug = F * u_aug.
F = [
    [64, -16, 0, 4, -4, -6, -6, 4],
    [0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 8, -4, 2, 0, 2, 6],
    [0, 16, -16, 0, -4, 0, -4, -4],
    [0, 0, 0, 0, 0, 2, 1, 0],
    [0, 0, 0, 0, 2, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
]
# Each inverse row is a numerator in old coordinates, divided by its divisor.
N = [
    [1, 1, 2, 1, 3, 2, 1, -12],
    [0, 2, 2, 1, 0, 0, 0, -8],
    [0, 1, 1, 0, 0, -1, -1, -6],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, -1, 0],
    [0, 0, 0, 0, 1, 0, -1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
]
DIV = [64, 16, 8, 4, 2, 2, 1, 1]
DOMAIN = [
    ('p_lower', [1, 0, 0, 0, 0, 0, 0, 0]),
    ('p_upper', [-1, 0, 0, 0, 0, 0, 0, 80]),
    ('q_lower', [0, 1, 0, 0, 0, 0, 0, 0]),
    ('q_upper', [0, -1, 0, 0, 0, 0, 0, 31]),
    ('y10_lower', [0, 0, 1, 0, 0, 0, 0, 0]),
    ('y14_lower', [0, 0, 0, 1, 0, 0, 0, 0]),
    ('y_sum_upper', [0, 0, -1, -1, 0, 0, 0, 160]),
    ('z8_lower', [0, 0, 0, 0, 1, 0, 0, 0]),
    ('z12_lower', [0, 0, 0, 0, 0, 1, 0, 0]),
    ('z16_lower', [0, 0, 0, 0, 0, 0, 1, 0]),
    ('z_sum_upper', [0, 0, 0, 0, -1, -1, -1, 80]),
]


def mul(row, matrix):
    return [sum(row[k] * matrix[k][j] for k in range(8)) for j in range(8)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, default=ROOT.parent / '2026-10-29')
    parser.add_argument('--integrality-certificate', type=Path,
                        default=ROOT.parent / '2026-11-03/certificate.json')
    args = parser.parse_args()
    rows = list(csv.DictReader((args.source_dir / 'affine_coefficients.csv').open()))
    with (ROOT / 'integer_coefficients.csv').open('w', newline='') as out:
        writer = csv.writer(out, lineterminator='\n')
        writer.writerow(['i', 'j', 'constant'] + NEW)
        for row in rows:
            assert int(row['denominator']) == 1024
            transformed = mul([int(row[k]) for k in OLD + ['constant']], F)
            assert all(v % 1024 == 0 for v in transformed)
            transformed = [v // 1024 for v in transformed]
            writer.writerow([row['i'], row['j'], transformed[-1]] + transformed[:-1])
    with (ROOT / 'domain_inequalities.csv').open('w', newline='') as out:
        writer = csv.writer(out, lineterminator='\n')
        writer.writerow(['name', 'constant'] + NEW + ['relation'])
        for name, row in DOMAIN:
            transformed = mul(row, F)
            writer.writerow([name, transformed[-1]] + transformed[:-1] + ['>=0'])
    certificate = {
        'format_version': 1,
        'old_columns': OLD + ['constant'],
        'new_columns': NEW + ['constant'],
        'forward_matrix': F,
        'inverse_numerators': N,
        'inverse_divisors': DIV,
        'lattice_index': 131072,
        'domain_inequalities': [{'name': n, 'old_row': r} for n, r in DOMAIN],
        'source_sha256': {
            'affine_coefficients.csv': sha(args.source_dir / 'affine_coefficients.csv'),
            'affine_split.py': sha(args.source_dir / 'affine_split.py'),
            'integrality_certificate.json': sha(args.integrality_certificate),
        },
        'files_sha256': {name: sha(ROOT / name) for name in [
            'integer_coefficients.csv', 'domain_inequalities.csv']},
        'scope': 'Bijective coordinate transport only; no feasibility or code-existence decision.',
    }
    (ROOT / 'lattice_certificate.json').write_text(json.dumps(certificate, indent=2) + '\n')
    print(json.dumps({'generated': True, 'table_rows': len(rows),
                      'domain_halfspaces': len(DOMAIN), 'lattice_index': 131072}))


if __name__ == '__main__':
    main()
