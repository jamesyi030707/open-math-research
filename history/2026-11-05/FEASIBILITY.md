# Exact feasibility of the fixed seven-integer model

## Result

**The fixed 1,075-inequality integer model is feasible.** An exact witness is

```
(a,b,c,d,e,f,g) = (6,14,4,0,31,2,0).
```

In the original coordinates this is

```
(p,q,y10,y14,z8,z12,z16) = (28,0,100,32,4,62,0).
```

The eleven domain slacks, in the published CSV order, are

```
(28,52,0,31,100,32,28,4,62,0,14).
```

All 1,064 split-table entries are nonnegative integers: 1,032 are positive and
32 are zero. Together with the eleven domain rows, this gives 1,041 positive
slacks and 34 zero slacks. There are no negative slacks. The smallest positive
table entry is 1, the largest is 346296402343800, and the table sum is
18014398509481984 = 2^54. These are exact integer evaluations, not rounded
solver residuals.

This establishes feasibility of the supplied **fixed necessary-condition
model**. It does not construct a code, show that the split table is realizable
by a code, prove existence of the target code, exclude any target code, or
settle the surrounding open problem. In particular, this feasible model cannot
provide an infeasibility certificate for the target without additional valid
constraints or a stronger model.

## Exact proof and certificate semantics

Each input row has the form

```
r_0 + r_a a + r_b b + r_c c + r_d d + r_e e + r_f f + r_g g >= 0.
```

The certificate supplies the seven integers above. The checker reads all
1,064 table rows and all eleven domain rows and evaluates each affine form
with Python integers. It rejects the certificate if any evaluation is negative.
There is no optimizer, search, floating-point operation, numerical tolerance,
or assumption about solver success in the verifier. The full table position
inventory `(i,j)`, 0 <= i <= 27 and 0 <= j <= 37, is checked in order; all
constant, zero, and repeated rows are retained. Both input files are pinned
with SHA-256. The resulting ordered list of all 1,075 slacks has digest

```
dbf81b0711ea9ba46fad929571c1a175f7babbe82cdf355357320d0a7d70d372
```

The 596-byte `certificate.json` contains the witness, input hashes and this
slack digest. `slacks.csv` is the complete human-readable transcript; it is
auxiliary, because the checker recomputes every value from the source CSVs.

The checker implements exactly two proof types:

1. `integer_feasible`: an integer tuple and exact nonnegativity of every row.
2. `rational_infeasible`: a sparse list of strictly positive rational row
   multipliers. For rows `c + A u >= 0`, it requires `lambda^T A = 0` and
   `lambda^T c < 0`, a contradiction valid over the reals and hence integers.
   Omitted rows have multiplier zero. All rational arithmetic uses `Fraction`.

**No integer-infeasibility branch proof is implemented or claimed.** A system
such as `2u=1` is rationally feasible and integer-infeasible, so it has neither
of the two supported certificate types. Its exclusion would require an
additional valid integrality argument, such as an exhaustive split tree with
exact certificates at every leaf. No such machinery is needed for the present
positive witness.

## Controls and rejection tests

Before the actual model attempt, `controls.json` and the standard-library
checker verified:

- Feasible control: `u >= 0`, `2-u >= 0`, witnessed by the integer `u=1`.
- Infeasible control: `u-1 >= 0`, `-u >= 0`, whose sum is `-1 >= 0`.

`test_checker.py` also checks nine deliberately invalid inputs: a negative
Farkas multiplier; failure to cancel the variable; combined constant zero;
a repeated sparse row index; a noninteger witness; a wrong-dimensional
witness; the inherited rejected model tuple; a corrupted table with the old
hash; and a missing table row even after its hash is updated. All nine are
rejected. The constant mutation is specifically chosen to make the combined
constant zero; no claim is made that every arbitrary constant perturbation
must invalidate a certificate.

## Discovery versus proof

One bounded SciPy 1.17.0 `milp` / HiGHS call proposed the witness. The internal
solver time limit was **110 seconds**, inside an external **120-second process
limit**. The measured solver-call elapsed time was approximately **0.017703
seconds**, not 120 seconds. There was no further solver search. All seven
coordinates were explicitly unbounded in both directions before imposing the
published inequalities; in particular, no artificial nonnegativity bound was
put on `e` or `f`.

The numerical call is optional discovery only. Its status is retained in
`discovery_result.json`, but neither the theorem nor either exact checker
relies on that status. The optional discovery script accepts a candidate only
after exact integer evaluation and bounds a generated proof certificate at
8,192 bytes. The actual certificate is 596 bytes. The discovery budget is not
a claim to enumerate feasible tuples or to classify all possible witnesses.

## Reproduction

Run from this directory with Python 3. No third-party package is needed for
proof verification. Set `MODEL_DIR` to the directory containing the published
2026-11-04 `domain_inequalities.csv` and `integer_coefficients.csv`:

```
python -I -B check_certificate.py controls.json
python -I -B check_certificate.py certificate.json --model-dir "$MODEL_DIR"
python -I -B test_checker.py --model-dir "$MODEL_DIR"
```

The tests use explicit checks, not Python `assert`, and also work under `-O`.
For an optional independent direct evaluation of the original denominator-1024
table, set `ORIGINAL_CSV` to the 2026-10-29 `affine_coefficients.csv` and run:

```
python -I -B audit_original.py --original-csv "$ORIGINAL_CSV"
```

This second checker does not import the numerical search or the primary
certificate checker. It directly evaluates all original affine numerator rows
at the original-coordinate witness, checks divisibility by 1024, checks
nonnegativity, checks the original eleven bounds, and matches the ordered slack
digest. It does not repeat the earlier coordinate-transformation proof.

Only if repeating numerical discovery is desired, install SciPy separately
and use an output directory that does not overwrite archived results:

```
timeout 120s python discover.py --model-dir "$MODEL_DIR" --output-dir "$OUTPUT_DIR"
```

The output directory must already exist. A rerun may discover a different
valid witness and produce different timing; numerical reproducibility is not
required for exact verification of the archived witness.

## Input provenance

- `integer_coefficients.csv` SHA-256:
  `0677ea7f6268cf3af33adb979a6c837f4bdd8b3a0b2b244657bd8bc15808c3c0`.
- `domain_inequalities.csv` SHA-256:
  `861e23b73b1a4456d9ba8f6b2d80a7037a71543c9b43fe59762d5810bc99aa14`.
- Original `affine_coefficients.csv` SHA-256:
  `c49805f554e88c468d92d1835fb19f47480295a95eb32f5c18e53db05277323c`.

Inputs are the previously published model files in
`history/2026-11-04/` and original affine table in `history/2026-10-29/` of
[jamesyi030707/open-math-research](https://github.com/jamesyi030707/open-math-research).
The preceding lattice equivalence theorem is separate prior work; this
package contributes the feasibility witness and exact verification.
