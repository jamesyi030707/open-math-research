"""Independent direct evaluation in the original seven coordinates.

Does not import the discovery script or exact certificate checker. Uses only
integer division and the original table pinned by SHA-256, so it does not
re-prove or depend on coordinate-change identities for this witness.
Usage: python audit_original.py --original-csv PATH
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

INPUT_HASH = 'c49805f554e88c468d92d1835fb19f47480295a95eb32f5c18e53db05277323c'
OLD = ['p', 'q', 'y10', 'y14', 'z8', 'z12', 'z16']
WITNESS = [28, 0, 100, 32, 4, 62, 0]


def require(condition, message):
    if not condition:
        raise ValueError(message)


p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--original-csv', type=Path, required=True)
args = p.parse_args()
data = args.original_csv.read_bytes()
require(hashlib.sha256(data).hexdigest() == INPUT_HASH, 'Wrong original input hash')
reader = csv.DictReader(data.decode().splitlines())
require(reader.fieldnames == ['i','j','constant'] + OLD + ['denominator'], 'Header')
rows = list(reader)
require([(int(r['i']), int(r['j'])) for r in rows] ==
        [(i,j) for i in range(28) for j in range(38)], 'Complete original table')
values = []
for row in rows:
    require(int(row['denominator']) == 1024, 'Original denominator')
    numerator = int(row['constant']) + sum(int(row[k])*x for k,x in zip(OLD,WITNESS))
    quotient, remainder = divmod(numerator, 1024)
    require(remainder == 0, 'Nonintegral table coefficient')
    require(quotient >= 0, 'Negative table coefficient')
    values.append(quotient)
p0,q,y10,y14,z8,z12,z16 = WITNESS
domain = [p0,80-p0,q,31-q,y10,y14,160-y10-y14,z8,z12,z16,80-z8-z12-z16]
require(all(x>=0 for x in domain), 'Original domain violation')
# An independent, fixed expected transcript hash connects the direct original
# evaluations with the published seven-integer-coordinate slack transcript.
slacks_hash = hashlib.sha256(('\n'.join(str(v) for v in domain+values)+'\n').encode()).hexdigest()
require(slacks_hash == 'dbf81b0711ea9ba46fad929571c1a175f7babbe82cdf355357320d0a7d70d372',
        'Original and integer-coordinate slack transcripts disagree')
print(json.dumps({'verified':True, 'original_input_sha256':INPUT_HASH,
                  'original_coordinates':dict(zip(OLD,WITNESS)),
                  'original_domain_slacks':domain,
                  'original_table_coefficients_checked':len(values),
                  'nonintegral_coefficients':0, 'negative_coefficients':0,
                  'zero_coefficients':values.count(0),
                  'positive_coefficients':sum(x>0 for x in values),
                  'minimum_positive_coefficient':min(x for x in values if x>0),
                  'maximum_coefficient':max(values), 'table_coefficient_sum':sum(values),
                  'slacks_sha256':slacks_hash,
                  'scope':'Feasibility of the fixed necessary-condition model; no code construction.'},
                 indent=2, sort_keys=True))
