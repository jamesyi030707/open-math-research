# Independent audit of the fixed formal split witness

## Finding

The integer tuple

```
u = (a,b,c,d,e,f,g) = (6,14,4,0,31,2,0)
x = (p,q,y10,y14,z8,z12,z16) = (28,0,100,32,4,62,0)
```

is feasible for the **fixed seven-variable formal split-enumerator model**. Direct evaluation of all 1,064 original numerator rows gives nonnegative multiples of 1,024. This independently establishes feasibility of that specific necessary-condition system, rather than merely checking the transformed integer inequalities.

The audit imports no solver, discovery program, previous checker, or source-model module. It performs no candidate search and does not execute `affine_split.py`. It reconstructs the numeric primal split array from the twelve source category counts and uses an independently implemented three-term Krawtchouk recurrence to reproduce all original numeric numerators.

## Exact checks

- Both coordinate substitutions recover the displayed tuples exactly.
- The original eleven domain slacks, in the published order, are `(28,52,0,31,100,32,28,4,62,0,14)`. All are nonnegative, and each equals its transported inequality evaluated at `u`.
- The six original congruence expressions are `(384,224,32,8,62,4)` with moduli `(64,16,8,4,2,2)`. All six remainders are zero.
- All 1,064 original denominators are 1,024, all numerators are divisible by 1,024, and all normalized coefficients are nonnegative.
- Each original coefficient equals the corresponding transported integer coefficient.
- Reconstructing the numeric primal and applying its split transform reproduces every original numerator. Applying the inverse transform recovers the primal on the entire `28 x 38` grid, including zero cells.
- Both block-complement symmetries and all 65 ordinary diagonal transform identities hold.

Input files are pinned by SHA-256. In particular, the original `affine_coefficients.csv` has hash `c49805f554e88c468d92d1835fb19f47480295a95eb32f5c18e53db05277323c`. Complete input and output hashes appear in `audit_result.json`.

## The formal enumerators

The twelve source category counts, in the original `GROUPS` order, are

```
160, 28, 52, 0, 31, 100, 32, 28, 4, 62, 0, 14.
```

Each category contributes at both specified residual weights, including a doubled contribution when those two weights coincide. After merging coincident cells and adding `(0,0)` and `(0,32)`, the primal has 14 positive cells and total 1,024. Its ordinary weight enumerator is

```
1 + 396 z^28 + 303 z^32 + 244 z^36 + 80 z^40.
```

The complete nonzero primal split array is in `audited_primal.csv`.

The formal dual has:

- 1,064 cells: 32 zero and 1,032 positive;
- coefficient sum `18014398509481984 = 2^54`;
- original numerator sum `18446744073709551616 = 2^64`;
- smallest positive coefficient 1;
- largest coefficient 346,296,402,343,800;
- no total-weight-1 or total-weight-2 terms;
- total-weight-3 coefficient 2, entirely at `T(1,2)=2`;
- total-weight-4 coefficient 496, with `T(0,4)=40`, `T(1,3)=154`, `T(2,2)=212`, `T(3,1)=59`, and `T(4,0)=31`.

`audited_table.csv` lists every original numerator, denominator, and normalized coefficient. `audit_result.json` additionally records all zero cells and all 65 ordinary dual coefficients. “Formal dual” here denotes a normalized MacWilliams transform of a formal array; it does not assert that a linear code with that enumerator exists.

## Reproduction

Install the four audit artifacts and this report directly in `history/2026-11-05/`, beside that day's feasibility certificate. The default layout expects the original files under `history/2026-10-29/` and the integer-model CSVs under `history/2026-11-04/`.

From `history/2026-11-05/`, run:

```
timeout 60s python audit.py
```

Only Python's standard library is required. The script deterministically writes `audit_result.json`, `audited_table.csv`, and `audited_primal.csv`. For a different layout, `--source-dir`, `--model-dir`, and `--output-dir` accept explicit directories. There are no machine-specific paths in the outputs. All validation uses explicit checks rather than Python `assert`, so it remains enabled under `python -O`.

## Logical limits

This point proves the fixed domain, split nonnegativity, and integrality conditions are jointly satisfiable. Consequently, this exact collection of constraints cannot by itself yield an infeasibility exclusion. It does **not** prove the formal arrays are realizable by a binary linear code, construct a generator matrix, establish the underlying residual/kernel structure in an actual code, prove the existence of the target code, or settle the open problem. Additional structural constraints or a genuine construction may change what is possible.

The audit independently verifies this one supplied witness. It does not reprove the general lattice-integrality equivalence for all tuples, classify feasible tuples, establish optimality or uniqueness, or search for further examples.

## Sources

- [Original affine coefficient table](https://github.com/jamesyi030707/open-math-research/blob/main/history/2026-10-29/affine_coefficients.csv)
- [Original exact split model](https://github.com/jamesyi030707/open-math-research/blob/main/history/2026-10-29/affine_split.py)
- [Denominator-free model](https://github.com/jamesyi030707/open-math-research/blob/main/history/2026-11-04/README.md)
