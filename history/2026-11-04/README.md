# A denominator-free integer model for the fixed affine split table

## Theorem

Let `x=(p,q,y10,y14,z8,z12,z16)` be integral. The 1,064 split coefficients of the supplied fixed residual/kernel-one model are all integers if and only if `x` has the following representation for a **unique** integer tuple `u=(a,b,c,d,e,f,g)`:

```
p   =  4 + 64a - 16b       + 4d - 4e - 6f - 6g
q   =                       4d
y10 =  6             + 8c - 4d + 2e      + 2g
y14 = -4       + 16b - 16c      - 4e      - 4g
z8  =                                2f +  g
z12 =                           2e      +  g
z16 =                                     g
```

The inverse is

```
a = (p + q + 2y10 + y14 + 3z8 + 2z12 + z16 - 12)/64
b = (2q + 2y10 + y14 - 8)/16
c = (q + y10 - z12 - z16 - 6)/8
d = q/4
e = (z12 - z16)/2
f = (z8 - z16)/2
g = z16.
```

Thus the integrality locus is the affine lattice `x0 + M Z^7`, where `x0=(4,0,6,-4,0,0,0)` and `M` is the displayed linear coefficient matrix. Its index in `Z^7` is `|det M|=131072=2^17`. The base point is an affine-lattice origin, **not** a domain-feasible point. The coordinates `a` through `g` are unrestricted integers until the bounds below are imposed; in particular, `e` and `f` must not be constrained to be nonnegative.

Every table entry becomes an integer affine form `T_ij(u)`. The CSV `integer_coefficients.csv` stores **all 1,064** such forms with header `i,j,constant,a,b,c,d,e,f,g`; there is no hidden denominator. The original model consisting of integral counts, original domain bounds, and nonnegative integral split coefficients is therefore equivalent, bijectively, to

```
u in Z^7,
the eleven inequalities below,
T_ij(u) >= 0 for every 0 <= i <= 27 and 0 <= j <= 37.
```

No cells, including zero, constant, or complement-repeated cells, are dropped.

## All transported original bounds

These are direct substitutions, not added cuts or a relaxation:

```
0 <= 4 + 64a - 16b + 4d - 4e - 6f - 6g <= 80
0 <= 4d <= 31
6 + 8c - 4d + 2e + 2g >= 0
-4 + 16b - 16c - 4e - 4g >= 0
2 + 16b - 8c - 4d - 2e - 2g <= 160
2f + g >= 0
2e + g >= 0
g >= 0
2e + 2f + 3g <= 80.
```

There are eleven one-sided inequalities because the first two lines each encode two. The second line can equivalently be written `0 <= d <= 7` for integer `d`; the machine-readable certificate keeps the exact original upper expression `31-4d`. `domain_inequalities.csv` contains the eleven left-hand sides in `>=0` form. Together with all 1,064 coefficient inequalities, this is an exact 1,075-halfspace integer description, without a feasibility decision.

## Proof

The supplied two-way modular certificate establishes that integrality of all original table entries is equivalent to these six residual expressions vanishing modulo the indicated numbers:

```
C1 = p+q+2y10+y14+3z8+2z12+z16-12      (mod 64)
C2 = 2q+2y10+y14-8                     (mod 16)
C3 = q+y10-z12-z16-6                   (mod 8)
C4 = q+2z8+2z16                        (mod 4)
C5 = z12+z16                           (mod 2)
C6 = z8+z16                            (mod 2).
```

The current checker rechecks that certificate rather than assuming its conclusion. Its two matrix identities include the affine constant column and are verified in both directions against all 1,064 original rows.

Suppose the congruences hold. The formulas for `a,b,c` are integral immediately. Since `q=C4-2C6`, `q` is divisible by four and `d` is integral. Since `z12-z16=C5-2z16` and `z8-z16=C6-2z16`, `e,f` are integral, and `g` is integral by hypothesis. Solving these seven definitions yields the forward formulas. Conversely, substituting the forward formulas into each `Cr` makes every coefficient, including the constant, divisible by its prescribed modulus, so every integer `u` gives an integral split table. The forward and inverse affine matrices multiply to the identity in both orders, proving uniqueness and surjectivity onto the integrality locus.

Reordering the rows of `M` as `(p,y14,y10,q,z12,z8,z16)` gives an upper-triangular matrix with diagonal `(64,16,8,4,2,2,1)`. The row permutation is even. Hence the determinant is `131072`, and the full-rank lattice index is its absolute value.

For each original numerator row `A_ij`, exact substitution gives the identity `A_ij F = 1024 T_ij`, where `F` is the augmented forward matrix. Every one of the resulting 8,512 coefficients is integral after division by 1,024. The verifier checks these identities and their inverse substitutions entry by entry. Therefore the value, sign, and integrality of every individual table coefficient are preserved, not just aggregate conditions. Substitution into each of the eleven original domain halfspaces gives exactly the listed bounds. This proves equivalence of the whole fixed model.

## Reproduction and certificate

From the repository root, run with Python's standard library only (do not use Python's `-O` flag):

```
timeout 60s python -I -B history/2026-11-04/build_model.py
timeout 60s python -I -B history/2026-11-04/verify_model.py
```

`build_model.py` deterministically writes the two transformed CSV files and `lattice_certificate.json`. `verify_model.py` does not import the generator. It independently checks:

- The pinned original CSV hash and the full `28 x 38` row order.
- Both prior modular equivalence identities: 48 forward and 8,512 reverse entries.
- Both affine coordinate round trips: 128 exact rational identities.
- All six image congruences, including affine constants: 48 entries.
- The exact `7 x 7` determinant and lattice index.
- All 1,064 table rows, 8,512 affine entries, and their inverse transport.
- All eleven original domain halfspaces without omissions.
- Byte-identical regeneration of the original CSV from `../2026-10-29/affine_split.py`; that script also checks its original transform identities.
- The inherited rejected tuple as a fixed regression case, not as a search.

The verifier's result is recorded in `verification_result.json`. It completed in approximately 0.38 seconds on 2026-11-04, with a 60-second process limit. No solver, assignment-domain enumeration, random sampling, or code search is used. Loops visit only the fixed coefficient tables and certificate entries.

The default input paths are relative to the scripts: `../2026-10-29/affine_coefficients.csv`, `../2026-10-29/affine_split.py`, and `../2026-11-03/certificate.json`. For a different local layout, both scripts accept `--source-dir PATH` and `--integrality-certificate PATH`. The inputs are reused, not copied into this archive. The generator's outputs do not contain machine-specific absolute paths.

## Regression example and limits

The inherited tuple `(0,0,140,16,8,6,64)` maps to `(6,18,8,0,-29,-28,64)`. It satisfies all eleven domain inequalities, and the transformed table is integral, but eight cells are negative: `(1,2),(1,35),(26,2),(26,35)` have value `-16`, and `(3,1),(3,36),(24,1),(24,36)` have value `-1`. The transformation correctly preserves that failure.

This work removes modular constraints and denominators from an already fixed necessary-condition model. It neither establishes nor refutes feasibility of that model, constructs a code, proves code realizability from a feasible tuple, excludes a target code, nor settles the open problem.

## Provenance

Original model sources:

- [Affine coefficient table](https://github.com/jamesyi030707/open-math-research/blob/main/history/2026-10-29/affine_coefficients.csv), Git blob `adebcbe0c00c15a5d8695720713034d6689efcff`.
- [Exact source model](https://github.com/jamesyi030707/open-math-research/blob/main/history/2026-10-29/affine_split.py), Git blob `cf6a9d20e77a3fca30f0844e996c28f433c158d5`.

Original CSV SHA-256: `c49805f554e88c468d92d1835fb19f47480295a95eb32f5c18e53db05277323c`.

The supplied 2026-11-03 integrality certificate is read from `../2026-11-03/certificate.json`. All source and transformed data hashes appear in `lattice_certificate.json` for a pinned, repo-relative replay.

## Separate audit

A second implementation independently checked both affine compositions, the index, every table row and all original bounds. See [audit and replay](INDEPENDENT_AUDIT.md). From the repository root run `timeout 60s python -I -B history/2026-11-04/independent_audit.py`. Both implementations passed; this is implementation cross-checking, not external peer review.
