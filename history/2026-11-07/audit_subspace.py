"""Independent exact audit of the fixed residual kernel-one q constraint.

No search, solver, network request, or changes to the source repository.
The archived residual basis is from:
https://github.com/jamesyi030707/open-math-research/blob/main/history/2026-10-24/independent/residual_candidate.json
The q category is from history/2026-10-28/category_cut.py in the same repository.
"""
import json
import ast
import hashlib
from pathlib import Path
from collections import Counter

BASIS = [
    0x17e7146801, 0x6293dc808, 0xf714c2017, 0x35dfc802d, 0xb1f3485c,
    0x63e6a0ae, 0x65be14f, 0x196fc233, 0x3e690ce6, 0xcb73897,
]

ROOT = Path(__file__).resolve().parent
source_basis = json.loads((ROOT / "residual_candidate.json").read_text())
assert [int(row, 16) for row in source_basis["basis_hex"]] == BASIS
witness = json.loads((ROOT / "source_witness_certificate.json").read_text())
lattice = json.loads((ROOT / "source_lattice_certificate.json").read_text())
assert lattice["old_columns"] == ["p", "q", "y10", "y14", "z8", "z12", "z16", "constant"]
assert lattice["new_columns"] == ["a", "b", "c", "d", "e", "f", "g", "constant"]
point = witness["proof"]["point"] + [1]
old_point = [sum(x*y for x, y in zip(row, point)) for row in lattice["forward_matrix"]]
assert old_point == [28, 0, 100, 32, 4, 62, 0, 1]
assert lattice["forward_matrix"][1] == [0, 0, 0, 4, 0, 0, 0, 0]

# Inspect the two original q categories without executing source code.
tree = ast.parse((ROOT / "source_category_cut.py").read_text())
joint = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "joint")
groups = next(node.value for node in joint.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "groups" for target in node.targets))
category_strings = [ast.unparse(item).replace(" ", "") for item in groups.elts]
assert "(16,16,12,q)" in category_strings
assert "(16,16,16,31-q)" in category_strings

def xor_image(u, basis):
    word = 0
    for i, row in enumerate(basis):
        if u & (1 << i):
            word ^= row
    return word

def rank(vectors):
    pivots = {}
    for x in vectors:
        while x:
            bit = x.bit_length() - 1
            if bit not in pivots:
                pivots[bit] = x
                break
            x ^= pivots[bit]
    return len(pivots)

words = [xor_image(u, BASIS) for u in range(1024)]
weights = [word.bit_count() for word in words]
assert rank(BASIS) == 10
assert Counter(weights) == {0: 1, 14: 160, 16: 142, 18: 320, 20: 160, 22: 160, 24: 80, 32: 1}
heavy = [u for u, w in enumerate(weights) if w == 32]
assert heavy == [1008]
h = heavy[0]
pair_members = {u for u in range(1024) if weights[u] == weights[u ^ h] == 16}
T = pair_members | {0, h}
assert T == set(range(0, 1024, 16))
assert len(T) == 64 and rank(T) == 6
assert all(u ^ v in T for u in T for v in T)
S = {min(u, u ^ h) for u in T}
assert S == set(range(0, 512, 16))
assert len(S) == 32 and rank(S) == 5
assert all(u ^ v in S for u in S for v in S)

# Every column has either zero or sixteen ones on the five-dimensional S.
column_sums = [sum((u & v).bit_count() % 2 for u in S) for v in range(1024)]
assert set(column_sums) == {0, 16}
admissible_q = []
for q in range(32):
    total = 12*q + 16*(31-q)
    if total % 16 == 0 and total // 16 <= 27:
        admissible_q.append(q)
assert admissible_q == [16, 20, 24, 28]

# Standalone restricted-space control only. Repeated columns are permitted.
columns = list(range(1, 16)) + [19, 19, 23, 23, 27, 27, 28, 28, 29, 29, 30, 30]
control_weights = [sum((s & v).bit_count() % 2 for v in columns) for s in range(32)]
expected = [0]
for s in range(1, 32):
    bits = [(s >> i) & 1 for i in range(5)]
    b = (bits[0]*bits[1]) ^ (bits[2]*bits[3]) ^ bits[4]
    expected.append(16-4*b)
assert control_weights == expected
assert len(columns) == 27 and rank(columns) == 5
assert Counter(control_weights) == {0: 1, 12: 16, 16: 15}

print(json.dumps({
    "status": "PASS",
    "residual_rank": 10,
    "heavy_message": h,
    "subspace_T": {"size": len(T), "rank": rank(T), "basis": [16, 32, 64, 128, 256, 512], "closure_pairs": len(T)**2},
    "quotient_representative_subspace_S": {"size": len(S), "rank": rank(S), "basis": [16, 32, 64, 128, 256], "closure_pairs": len(S)**2},
    "necessary_q_values": admissible_q,
    "old_witness_counts_from_archived_affine_map": old_point[:-1],
    "already_existing_congruence": "q=4d, hence q divisible by 4; only q>=16 is new here",
    "november_5_q": 0,
    "november_5_required_active_columns": 31,
    "available_columns": 27,
    "control_columns": columns,
    "control_weight_distribution": dict(sorted(Counter(control_weights).items())),
    "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in ["residual_candidate.json", "source_category_cut.py", "source_witness_certificate.json", "source_lattice_certificate.json"]},
    "scope": "Excludes all message labelings of the November 5 witness in this fixed residual kernel-one model. Does not exclude other q values, other kernel branches, other residual codes, or all binary [64,11,27] codes. The q=16 control is only a standalone subspace code, not an extension certificate."
}, indent=2))
