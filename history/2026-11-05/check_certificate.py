"""Verify exact integer feasibility witnesses or rational Farkas certificates.

Uses Python's standard library only. No optimizer, numerical tolerance or search.
Usage: python check_certificate.py certificate.json [--model-dir DIRECTORY]
"""
import argparse
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path

VARIABLES = list('abcdefg')
DOMAIN_NAMES = ['p_lower', 'p_upper', 'q_lower', 'q_upper', 'y10_lower',
                'y14_lower', 'y_sum_upper', 'z8_lower', 'z12_lower',
                'z16_lower', 'z_sum_upper']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(x):
    require(type(x) is int, 'Expected integer, not float or boolean')
    return x


def rational(x):
    require(type(x) in (int, str), 'Rational must be integer or exact string')
    return Fraction(x)


def load_model(root, pins):
    rows, names = [], []
    expected_files = ['domain_inequalities.csv', 'integer_coefficients.csv']
    require(set(pins) == set(expected_files), 'Pin both complete model files')
    for name in expected_files:
        data = (root / name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == pins[name], 'SHA-256 mismatch: ' + name)
        reader = csv.DictReader(data.decode().splitlines())
        expected_header = (['name', 'constant'] + VARIABLES + ['relation'] if name.startswith('domain')
                           else ['i', 'j', 'constant'] + VARIABLES)
        require(reader.fieldnames == expected_header, 'Unexpected header')
        records = list(reader)
        if name.startswith('domain'):
            require([r['name'] for r in records] == DOMAIN_NAMES, 'Domain row inventory')
            require(all(r['relation'] == '>=0' for r in records), 'Domain relation')
            names.extend('domain:' + r['name'] for r in records)
        else:
            require([(int(r['i']), int(r['j'])) for r in records] ==
                    [(i, j) for i in range(28) for j in range(38)], 'Complete table row inventory')
            names.extend('table:' + r['i'] + ',' + r['j'] for r in records)
        rows.extend([int(r[k]) for k in ['constant'] + VARIABLES] for r in records)
    require(len(rows) == 1075, 'Expected all 1075 inequalities')
    return rows, names


def verify(rows, proof):
    require(bool(rows), 'Empty system')
    dimension = len(rows[0]) - 1
    require(all(len(r) == dimension + 1 for r in rows), 'Ragged rows')
    for row in rows:
        for x in row:
            integer(x)
    kind = proof['kind']
    if kind == 'integer_feasible':
        point = [integer(x) for x in proof['point']]
        require(len(point) == dimension, 'Point dimension')
        values = [r[0] + sum(a * u for a, u in zip(r[1:], point)) for r in rows]
        require(all(v >= 0 for v in values), 'At least one violated inequality')
        return {'kind': kind, 'point': point, 'inequalities_checked': len(rows),
                'minimum_slack': min(values), 'zero_slack_count': values.count(0),
                'strictly_positive_count': sum(v > 0 for v in values)}, values
    if kind == 'rational_infeasible':
        total = [Fraction(0)] * (dimension + 1)
        seen = set()
        require(bool(proof['multipliers']), 'Empty Farkas certificate')
        for idx, val in proof['multipliers']:
            integer(idx)
            require(0 <= idx < len(rows) and idx not in seen, 'Bad or repeated row index')
            seen.add(idx)
            weight = rational(val)
            require(weight > 0, 'Sparse weights must be strictly positive')
            total = [x + weight * y for x, y in zip(total, rows[idx])]
        require(all(x == 0 for x in total[1:]), 'Variable coefficients do not cancel')
        require(total[0] < 0, 'Combined constant must be negative')
        return {'kind': kind, 'inequalities_checked': len(rows),
                'support_size': len(seen), 'combined_constant': str(total[0])}, None
    raise ValueError('Unsupported proof kind')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('certificate', type=Path)
    p.add_argument('--model-dir', type=Path)
    args = p.parse_args()
    cert = json.loads(args.certificate.read_text())
    require(cert['format_version'] == 1, 'Version')
    result = {'verified': True}
    if cert['system'] == 'controls':
        results = []
        for case in cert['cases']:
            outcome, _ = verify(case['rows'], case['proof'])
            results.append({'name': case['name'], **outcome})
        result['controls'] = results
    elif cert['system'] == 'fixed_seven_integer_model':
        require(args.model_dir is not None, 'Supply --model-dir')
        require(cert['variables'] == VARIABLES, 'Coordinate order')
        rows, names = load_model(args.model_dir, cert['files_sha256'])
        outcome, values = verify(rows, cert['proof'])
        result.update(outcome)
        if values is not None:
            slacks_digest = hashlib.sha256(('\n'.join(str(v) for v in values) + '\n').encode()).hexdigest()
            require(slacks_digest == cert['slacks_sha256'], 'Slack transcript digest')
            result['domain_slacks'] = dict(zip(DOMAIN_NAMES, values[:11]))
            result['slacks_sha256'] = slacks_digest
    else:
        raise ValueError('Unknown system')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
