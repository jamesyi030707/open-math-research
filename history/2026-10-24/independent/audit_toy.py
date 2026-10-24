"""Independent exhaustive check of the residual-lift criterion on a tiny code."""
from itertools import product
import json
B = (3, 5)  # binary [3,2,2]
passes = mismatches = 0
for A in product(range(8), repeat=2):
    rows = (7, A[0] | (B[0] << 3), A[1] | (B[1] << 3))
    weights = []
    for coeff in range(1, 8):
        word = 0
        for i, row in enumerate(rows):
            if coeff & (1 << i):
                word ^= row
        weights.append(word.bit_count())
    actual = min(weights) >= 3
    expected = True
    for coeff in range(1, 4):
        left = right = 0
        for i in range(2):
            if coeff & (1 << i):
                left ^= A[i]
                right ^= B[i]
        expected &= 3-right.bit_count() <= left.bit_count() <= right.bit_count()
    passes += actual
    mismatches += actual != expected
result = dict(total=64, passes=passes, failures=64-passes, mismatches=mismatches)
print(json.dumps(result, indent=2))
assert result == dict(total=64, passes=24, failures=40, mismatches=0)
