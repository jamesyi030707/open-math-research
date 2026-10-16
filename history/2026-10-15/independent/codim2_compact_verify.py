#!/usr/bin/env python3
"""Small standalone certificate verifier; no 698,027-space enumeration.

Input: only codim2_generator_matrix.txt. Requires ordinary Python 3. Does not
import another script or read the claimed results. All dot products are
computed directly. The mathematical implication is proved in codim2_proof.md.
"""

from collections import Counter
from functools import reduce
from itertools import combinations
from operator import xor
from pathlib import Path
from time import process_time


started = process_time()
lines = (Path(__file__).resolve().parent / "codim2_generator_matrix.txt").read_text().splitlines()
assert len(lines) == 11 and all(len(s) == 64 and set(s) <= {"0", "1"} for s in lines)
# Reversing coordinates is immaterial to weights, so parse strings as printed.
rows = [int(s, 2) for s in lines]
code = [reduce(xor, (r for i, r in enumerate(rows) if (m >> i) & 1), 0)
        for m in range(2048)]
assert len(set(code)) == 2048, "Generator rank must be 11."
assert min(c.bit_count() for c in code[1:]) == 26
minimum_messages = [m for m, c in enumerate(code) if c.bit_count() == 26]
assert len(minimum_messages) == 234

# Direct character sums, without bitsets, transforms, or rank-2 enumeration.
F = [sum(1 if (a & m).bit_count() % 2 == 0 else -1
         for m in minimum_messages) for a in range(2048)]
assert F[0] == 234 and min(F[1:]) == -30
assert (234 + 3 * min(F[1:])) // 4 == 36
assert 234 + 7 * min(F[1:]) == 24
assert (234 + 7 * min(F[1:])) // 8 == 3
assert 41 ^ 460 == 485 and F[41] == F[460] == F[485] == -30
sharp = [m for m in minimum_messages if (41 & m).bit_count() % 2 == 0
         and (460 & m).bit_count() % 2 == 0]
assert len(sharp) == 36

# Equality holds exactly when a,b,a+b all attain the character minimum.
minimum_dual = {a for a in range(1, 2048) if F[a] == -30}
assert len(minimum_dual) == 111
sharp_spaces = [(a, b, a ^ b) for a, b in combinations(sorted(minimum_dual), 2)
                if b < (a ^ b) and (a ^ b) in minimum_dual]
assert len(sharp_spaces) == 125
print("PASS: rank 11, distance 26, exactly 234 minimum messages.")
print("PASS: all 2,047 nonzero character sums >= -30.")
print("PROVED: every dimension-9 subcode has at least (234-90)/4 = 36 minimum words.")
print("PROVED: every dimension-8 subcode has at least (234-210)/8 = 3 minimum words; sharpness not asserted.")
print("PROVED: any binary linear code of distance at least 27 intersects this C in dimension at most 7.")
print("PASS: characters at 41, 460, 485 are all -30; their kernel has exactly 36.")
print("PASS: exactly 125 dimension-9 subcodes attain equality.")
print("Nonzero character histogram:", sorted(Counter(F[1:]).items()))
print(f"CPU seconds: {process_time() - started:.6f}.")
