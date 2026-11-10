"""Independent q24 obstruction audit. Reads only the pinned residual JSON.

No imports from, or execution of, the candidate obstruction checker.
All arithmetic is exact and uses the Python standard library.
"""
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from time import process_time


def need(truth, description):
    if not truth:
        raise ValueError(description)


def bit(value, position):
    return (value >> position) & 1


def dot(left, right):
    return (left & right).bit_count() % 2


def binary_rank(rows):
    rows = list(rows)
    width = max(rows, default=0).bit_length()
    pivot = 0
    for column in range(width):
        chosen = next((j for j in range(pivot, len(rows))
                       if bit(rows[j], column)), None)
        if chosen is None:
            continue
        rows[pivot], rows[chosen] = rows[chosen], rows[pivot]
        for j in range(len(rows)):
            if j != pivot and bit(rows[j], column):
                rows[j] ^= rows[pivot]
        pivot += 1
    return pivot


started = process_time()
input_path = Path(__file__).resolve().parent / 'inputs' / 'residual_candidate.json'
raw = input_path.read_bytes()
blob_sha = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
need(blob_sha == '8f76beaa5994563a2980ea9cb87412640d6560b4', 'pinned Git blob identity')
source = json.loads(raw)
basis = [int(value, 16) for value in source['basis_hex']]
need(len(basis) == 10 and binary_rank(basis) == 10, 'residual rank')
need(all(0 <= row < 2**37 for row in basis), '37 residual coordinates')

# Expand the actual 37 coordinates separately, rather than reuse a candidate
# residual-weight function or its claimed distribution.
coordinate_columns = [sum(bit(basis[j], coordinate) << j for j in range(10))
                      for coordinate in range(37)]
residual_weight = [sum(dot(message, column) for column in coordinate_columns)
                   for message in range(1024)]
need(Counter(residual_weight) == {0:1,14:160,16:142,18:320,20:160,22:160,24:80,32:1},
     'full residual spectrum')
need([u for u in range(1, 1024) if residual_weight[u] >= 27] == [1008],
     'unique possible nonzero left-kernel message')
h = 1008

# Independent certificate for the inherited doubly-even rigidity. Evaluation
# at all residual weight-14 messages fixes the 55 quadratic coefficients.
monomials = [(j,) for j in range(10)] + list(itertools.combinations(range(10), 2))
evaluation_rows = []
for message in range(1024):
    if residual_weight[message] == 14:
        evaluation_rows.append(sum(int(all(bit(message, j) for j in monomial)) << k
                                   for k, monomial in enumerate(monomials)))
need(binary_rank(evaluation_rows) == 55, 'rank55 doubly-even certificate')
need(all(residual_weight[s << 4] == residual_weight[(s << 4) ^ h] == 16
         for s in range(1, 32)), 'S residual-pair weights')
representatives = [(t ^ (s << 4)) for t in range(16) for s in range(32)]
need(len(set(representatives + [u ^ h for u in representatives])) == 1024,
     'all message classes covered')

windows = {}
for t in range(1, 16):
    windows[t] = []
    for s in range(32):
        u = t ^ (s << 4)
        w0, w1 = residual_weight[u], residual_weight[u ^ h]
        windows[t].append(tuple(a for a in range(28)
                                if 27-w0 <= a <= w0 and 27-w1 <= a <= w1
                                and (a+w0) % 4 == (a+w1) % 4 == 0))

T = [2,3,5,6,8,9,10,11,12,14]
hyperplanes = {}
for t in T:
    solutions = []
    for normal in range(1,32):
        for offset in range(2):
            if all(windows[t][s] == ((14,) if dot(s,normal) == offset
                                     else (10,14,18)) for s in range(32)):
                solutions.append([normal,offset])
    need(len(solutions) == 1, 'unique exact forced14 hyperplane')
    hyperplanes[t] = solutions[0]

# Canonical q24 classification. Its completeness is also checked separately
# in q24_independent_check.py over all C(31,7) sets. The paper argument is the
# rank-five, total-XOR-zero seven-set's two-dimensional dependency space.
H = [1,2,3,4,12,20,28]
P = {0,1,2,3}
Q_points = [4,12,20,28]
need(binary_rank(H) == 5 and binary_rank(Q_points) == 3, 'canonical direct sum')
nullwords = [mask for mask in range(128)
             if all(sum(bit(mask,j)*bit(H[j],coordinate) for j in range(7)) % 2 == 0
                    for coordinate in range(5))]
need(Counter(mask.bit_count() for mask in nullwords) == {0:1,3:1,4:1,7:1},
     'two-dimensional dependency code')
incidence = {v:sum(dot(v,s) for s in H) for v in range(1,32)}
need(all(k in (2,4,6) for k in incidence.values()), 'even positive incidence')
multiplicities = {v:(k-2)//2 for v,k in incidence.items()}
active = [v for v in multiplicities for _ in range(multiplicities[v])]
need(len(active) == 25, '25 active coordinate positions')
zero_on_P = [v for v in active if all(dot(v,p) == 0 for p in P)]
need(zero_on_P == [4], 'exactly one active coordinate annihilates P')
need(Counter(multiplicities.values()) == {0:9,1:19,2:3}, 'multiplicity pattern')

# Every actual three-double-column sign choice gives these exact centered
# second moments. We enumerate all six signs rather than assume the minimum.
true_energy4 = set()
for signs in itertools.product((-1,1), repeat=6):
    coefficient_square_sum = 19 + sum((signs[2*j]+signs[2*j+1])**2 for j in range(3))
    true_energy4.add(32*coefficient_square_sum)
need(true_energy4 == {608,736,864,992}, 'true energies times four')

# Enumerate every two-dimensional P, and a superset of all possible special
# functionals v0 and affine offsets. All nonzero annihilators of P are used.
planes = {tuple(sorted((0,a,b,a^b))) for a in range(1,32) for b in range(a+1,32)}
need(len(planes) == 155, 'all 155 two-dimensional spaces')
local_cache = {}
cases = 0
parallel_cases = transverse_cases = 0
for plane in sorted(planes):
    blocks = sorted({tuple(sorted(s^p for p in plane)) for s in range(32)})
    need(len(blocks) == 8, 'eight four-message blocks')
    annihilators = [v for v in range(1,32) if all(dot(v,p) == 0 for p in plane)]
    need(len(annihilators) == 7, 'all seven nonzero special-function possibilities')
    for t in T:
        normal,offset = hyperplanes[t]
        parallel = all(dot(p,normal) == 0 for p in plane)
        for special in annihilators:
            for e in range(2):
                b_values = [dot(block[0],special)^e for block in blocks]
                need(Counter(b_values) == {0:4,1:4}, 'four blocks of each special bit')
                possible_energy4 = {0}
                for block,b_value in zip(blocks,b_values):
                    choices = tuple(windows[t][s] for s in block)
                    key = (choices,b_value)
                    if key not in local_cache:
                        local_cache[key] = {sum((2*w-25)**2 for w in ws)
                                            for ws in itertools.product(*choices)
                                            if sum(ws) == 48+4*b_value}
                    possible_energy4 = {left+right for left in possible_energy4
                                        for right in local_cache[key]}
                need(not possible_energy4.intersection(true_energy4),
                     'z0 incompatible with exact column energy')
                if parallel:
                    need(not possible_energy4, 'parallel case already impossible by blocks')
                    parallel_cases += 1
                else:
                    need(possible_energy4 == {480}, 'transverse case energy exactly 120')
                    transverse_cases += 1
                cases += 1
need(cases == 21700 and parallel_cases == 4900 and transverse_cases == 16800,
     'complete block-orientation coverage')

# Terminal map contradiction, checked over all ordered pairs of quotient
# coordinate functionals, with the five-versus-four pigeonhole certificate.
C = [1,4,7,13,15]
need(sorted(a^b for a,b in itertools.combinations(C,2)) == T, 'ten pair differences')
surviving_maps = []
for first in range(16):
    for second in range(16):
        if all(dot(first,t) or dot(second,t) for t in T):
            surviving_maps.append([first,second])
need(not surviving_maps, 'no two-coordinate quotient map')

# One genuine rank-nine binary 27-column control, with varying repeated-pair
# signs and zero-coordinate values. This is explicitly not a target lift.
singles = [v for v in multiplicities if multiplicities[v] == 1]
doubles = [v for v in multiplicities if multiplicities[v] == 2]
restricted_columns = singles + [v for v in doubles for _ in range(2)] + [0,0]
extension_columns = [(j*7+3) % 16 for j in range(19)] + [0,4,0,8,0,3] + [1,2]
control_columns = [s | (t<<5) for s,t in zip(restricted_columns,extension_columns)]
need(binary_rank(control_columns) == 9, 'actual control rank nine')
control_failures = 0
control_energies4 = set()
missing_special_term_rejected = False
constant_energy_rejected = False
for t in range(16):
    ws = [sum(dot(s,v)^dot(t,e) for v,e in zip(restricted_columns,extension_columns))
          for s in range(32)]
    z = dot(t,1)+dot(t,2)
    opposed = sum(dot(t,d) for d in (4,8,3))
    need(sum(ws) == 400+32*z, 'control exact mean')
    need(sum((2*w-25-2*z)**2 for w in ws) == 4*(248-32*opposed),
         'control exact centered moment')
    actual_energy4 = sum((2*w-25-2*z)**2 for w in ws)
    control_energies4.add(actual_energy4)
    constant_energy_rejected |= actual_energy4 != 4*248
    for block in sorted({tuple(sorted(s^p for p in P)) for s in range(32)}):
        special_index = singles.index(4)
        special_bit = dot(block[0],4)^dot(t,extension_columns[special_index])
        need(sum(ws[s] for s in block) == 48+4*z+4*special_bit,
             'control actual four-message block sum')
        missing_special_term_rejected |= sum(ws[s] for s in block) != 48+4*z
    for s,w in enumerate(ws):
        u = t ^ (s << 4)
        for actual_message in (u,u^h):
            if actual_message and not 27-residual_weight[actual_message] <= w <= residual_weight[actual_message]:
                control_failures += 1
need(control_failures > 0, 'positive local control is not target code')
need(control_energies4 == true_energy4, 'actual control realizes all four energies')

# Explicit damage rejection for the most error-prone new statements.
damaged_rejected = {
    'wrong_hyperplane_offset': any(windows[T[0]][s] != ((14,) if dot(s,hyperplanes[T[0]][0])
                                                       == 1-hyperplanes[T[0]][1]
                                                       else (10,14,18)) for s in range(32)),
    'omit_special_coordinate_block_term': missing_special_term_rejected,
    'constant_centered_moment': constant_energy_rejected,
    'misuse_q28_energy_192': 4*192 not in true_energy4,
}
need(all(damaged_rejected.values()), 'damaged claims rejected')
print(json.dumps({
    'conclusion': 'q24 excluded only for the pinned residual and left-kernel dimension one',
    'input_git_blob': blob_sha,
    'input_sha256': hashlib.sha256(raw).hexdigest(),
    'residual_spectrum': dict(Counter(residual_weight)),
    'quadratic_evaluation_rank': 55,
    'hyperplanes': hyperplanes,
    'classification': 'one GL(5,2) class; 19 single, 3 double, 2 zero columns',
    'canonical_special_column': 4,
    'plane_count': len(planes),
    'orientation_cases': cases,
    'parallel_block_contradictions': parallel_cases,
    'transverse_energy_contradictions': transverse_cases,
    'transverse_energy': 120,
    'actual_column_energy_values': sorted(value//4 for value in true_energy4),
    'ordered_two_column_maps_checked': 256,
    'surviving_maps': surviving_maps,
    'actual_control_columns_9bits': control_columns,
    'actual_control_rank': 9,
    'actual_control_centered_energies': sorted(value//4 for value in control_energies4),
    'actual_control_full_lift_bound_failures': control_failures,
    'damaged_claim_rejections': damaged_rejected,
    'cpu_seconds': process_time()-started,
},indent=2))
