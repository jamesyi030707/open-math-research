"""Optional bounded numerical discovery, never an exact proof by solver status.

First run check_certificate.py controls.json. This script uses SciPy HiGHS
only to propose a point; all 1075 integer inequalities are checked before
writing an exact certificate. Variables a through g have no implicit bounds.
Usage: python discover.py --model-dir DIRECTORY --output-dir DIRECTORY
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
import scipy
from scipy.optimize import milp, Bounds, LinearConstraint

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--model-dir', type=Path, required=True)
p.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
args = p.parse_args()
subprocess.run([sys.executable, str(Path(__file__).with_name('check_certificate.py')),
                str(Path(__file__).with_name('controls.json'))], check=True, capture_output=True)
files = ['domain_inequalities.csv', 'integer_coefficients.csv']
keys = ['constant'] + list('abcdefg')
records = [r for name in files for r in csv.DictReader((args.model_dir / name).open())]
rows = [[int(r[k]) for k in keys] for r in records]
coeff = np.asarray([r[1:] for r in rows], dtype=float)
constants = np.asarray([r[0] for r in rows], dtype=float)
scale = np.maximum(1, np.max(np.abs(coeff), axis=1))
t0 = time.monotonic()
result = milp(np.zeros(7), integrality=np.ones(7),
              bounds=Bounds(np.full(7, -np.inf), np.full(7, np.inf)),
              constraints=LinearConstraint(coeff / scale[:, None], -constants / scale, np.inf),
              options={'time_limit': 110, 'mip_rel_gap': 0.0})
elapsed = time.monotonic() - t0
out = {'solver': 'scipy.optimize.milp / HiGHS', 'scipy_version': scipy.__version__,
       'solver_time_limit_seconds': 110, 'solver_elapsed_seconds': elapsed,
       'status': int(result.status), 'message': result.message,
       'has_candidate': result.x is not None,
       'proof_warning': 'Solver status alone is not a proof.'}
if result.x is not None:
    u = [int(round(float(x))) for x in result.x]
    values = [r[0] + sum(a*x for a, x in zip(r[1:], u)) for r in rows]
    out['rounded_candidate'] = u
    out['exact_minimum_slack'] = min(values)
    out['exact_violations'] = sum(v < 0 for v in values)
    if all(v >= 0 for v in values):
        cert = {'format_version': 1, 'system': 'fixed_seven_integer_model',
                'variables': list('abcdefg'),
                'files_sha256': {name: hashlib.sha256((args.model_dir/name).read_bytes()).hexdigest() for name in files},
                'proof': {'kind': 'integer_feasible', 'point': u},
                'slacks_sha256': hashlib.sha256(('\n'.join(str(v) for v in values)+'\n').encode()).hexdigest()}
        serialized = json.dumps(cert, indent=2)+'\n'
        if len(serialized.encode()) > 8192:
            raise ValueError('Certificate exceeds 8192-byte discovery bound')
        (args.output_dir/'certificate.json').write_text(serialized)
        with (args.output_dir/'slacks.csv').open('w', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['source', 'row', 'value'])
            for k, (r, v) in enumerate(zip(records, values)):
                writer.writerow(['domain' if k < 11 else 'table',
                                 r['name'] if k < 11 else r['i']+','+r['j'], v])
(args.output_dir/'discovery_result.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
