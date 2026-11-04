# Independent computational audit of the integer lattice transport

**Result: passed, 2026-11-04.** A separately written standard-library checker verifies the exact affine reformulation. This is an independent implementation, not an external peer review or a feasibility result.

## Checks completed

- The source table is byte-identical to the separately held 2026-11-03 audit input, with SHA-256 `c49805f554e88c468d92d1835fb19f47480295a95eb32f5c18e53db05277323c`.
- The previous modular certificate is rechecked in both directions against all 1,064 original rows, including affine constants: 48 entries of `B=UA` and 8,512 entries of `A=VB`, modulo 64. Its six rows encode precisely the six original congruences.
- Every integer parameter tuple maps to a congruence solution. The inverse has integer coordinates on that solution set: the first three quotients are the original congruences; `q=C4-2C6` is divisible by four; subtracting `2*z16` from each parity residual yields the other two quotients. Both affine compositions are exactly the identity.
- The linear determinant is **+131072 = 2^17**, independently calculated from the determinant definition. The mapping is a bijection from `Z^7` onto the affine congruence solution set, **not** a unimodular change of basis of all `Z^7`.
- All **1,064** transported table rows, comprising **8,512** affine entries, agree exactly with substitution into the pinned source and have integer coefficients. Reverse substitution also recovers every original row. All `(i,j)` labels and the complete `28 x 38` row coverage are retained.
- All **11** original domain halfspaces are reconstructed from the original bounds and verified in both directions, including the exact upper bound `31-4d`. These and the table rows give 1,075 preserved nonnegativity inequalities, without asserting irredundancy.
- The inherited tuple `(0,0,140,16,8,6,64)` has new coordinates `(6,18,8,0,-29,-28,64)`. It satisfies the original bounds and congruences but still has exactly eight negative table cells, with values `-16` or `-1` at the reported positions.

No defect was found in the mathematical statements in [the model README](README.md), [the public note](../../notes/codes-integer-lattice.md), or [the mathematical dialogue](DIALOGUE.md). In particular, the dialogue's parameter order `(a,b,c,t,u,v,w)` and the artifact order `(a,b,c,d,e,f,g)` are correctly related by `(c,b,a,w,u,v,t)`. The dialogue's enumeration suggestion is identified as a possible future step, not as work completed here.

## Reproduction

From the repository root:

```
timeout 60s python -I -B history/2026-11-04/independent_audit.py
```

The [checker](independent_audit.py) constructs the displayed affine formulas itself and does not import or execute `build_model.py`, `verify_model.py`, or `affine_split.py`. It uses exact integers and rational arithmetic. It reads the date-relative source files and certificate, so it is reusable from the published repository. `--model`, `--source-dir`, and `--integrality-certificate` allow alternate layouts; `--prior-table` optionally compares an additional separately held source copy.

[The recorded result](independent_audit_result.json) includes that optional comparison and completed in approximately **0.24 seconds**, under a 60-second process limit. A second run using the public default paths also passed. The determinant calculation sums 7! terms in one fixed 7-by-7 matrix; it does not enumerate any parameter or count domain.

## Scope

This audit checks exact representation, integrality equivalence, and preservation of inequalities. It uses no solver, assignment-domain enumeration, random sampling, or code search. It does not decide whether the fixed model is feasible, construct or exclude a code, or establish novelty. The external code-table observation and the provenance of the external dialogue require their separate source records; they are not verified by this algebraic checker.
