"""Negative tests for the exact witness/Farkas checker, standard library only."""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('checker_under_test', ROOT/'check_certificate.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def must_reject(label, operation):
    try:
        operation()
    except (ValueError, TypeError, KeyError, IndexError):
        return label
    raise RuntimeError('Invalid certificate unexpectedly accepted: ' + label)


p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--model-dir', type=Path, required=True)
args = p.parse_args()
controls = json.loads((ROOT/'controls.json').read_text())
for case in controls['cases']:
    checker.verify(case['rows'], case['proof'])
rows = controls['cases'][1]['rows']
rejected = []
rejected.append(must_reject('negative Farkas multiplier', lambda: checker.verify(
    rows, {'kind':'rational_infeasible','multipliers':[[0,-1],[1,1]]})))
rejected.append(must_reject('uncancelled Farkas variable', lambda: checker.verify(
    rows, {'kind':'rational_infeasible','multipliers':[[0,1],[1,2]]})))
rejected.append(must_reject('nonnegative combined constant', lambda: checker.verify(
    [[0,1],[0,-1]], controls['cases'][1]['proof'])))
rejected.append(must_reject('repeated Farkas row', lambda: checker.verify(
    rows, {'kind':'rational_infeasible','multipliers':[[0,1],[0,1],[1,2]]})))
rejected.append(must_reject('noninteger witness', lambda: checker.verify(
    [[0,1],[2,-1]], {'kind':'integer_feasible','point':['1/2']})))
rejected.append(must_reject('wrong witness dimension', lambda: checker.verify(
    [[0,1],[2,-1]], {'kind':'integer_feasible','point':[1,1]})))
cert = json.loads((ROOT/'certificate.json').read_text())
model_rows, _ = checker.load_model(args.model_dir, cert['files_sha256'])
checker.verify(model_rows, cert['proof'])
rejected.append(must_reject('inherited rejected tuple violates eight table cells', lambda: checker.verify(
    model_rows, {'kind':'integer_feasible','point':[6,18,8,0,-29,-28,64]})))
# It is useful to reject missing rows even when the attacker recomputes a hash.
with tempfile.TemporaryDirectory() as d:
    root = Path(d)
    for name in cert['files_sha256']:
        (root/name).write_bytes((args.model_dir/name).read_bytes())
    path = root/'integer_coefficients.csv'
    path.write_text('\n'.join(path.read_text().splitlines()[:-1])+'\n')
    rejected.append(must_reject('modified table fails pinned hash', lambda: checker.load_model(
        root, cert['files_sha256'])))
    new_pins = deepcopy(cert['files_sha256'])
    new_pins[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    rejected.append(must_reject('missing table row despite updated hash', lambda: checker.load_model(
        root, new_pins)))
print(json.dumps({'verified':True, 'invalid_inputs_rejected':len(rejected), 'tests':rejected}, indent=2))
