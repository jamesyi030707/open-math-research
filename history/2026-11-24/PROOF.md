# Exact minimum infeasible subsets of eight original weight systems

## Fixed problem and result

Use the fixed residual B, kernel-zero branch and doubly-even normalization of the [November 23 proof](../2026-11-23/PROOF.md). The eight controls are zero-based November 15 catalog indices 19, 115, 139 and 163, each unmodified and with low bits 0 and 2 exchanged in its W-column labels. Preserve column order. These are the same eight existing exclusions, not eight new ones.

The actual a=3 section is H = (0,4,5,10,11,15,18,19,23,25,33,46,54,56,60,61). A putative offset m is a raw 27-bit mask. A row labeled t requires wt(m XOR y(t))=14, where bit j of y(t) is the parity of t AND c_j. These are the original sixteen equalities, before projecting or combining any of them.

| Catalog index | Both orientations: minimum size of an infeasible subset | Infeasible subsets attaining that minimum |
|---|---:|---|
| 19 | 16 | H |
| 115 | 14 | H without 25 and 60, unique |
| 139 | 14 | H without 25 and 60, unique |
| 163 | 16 | H |

## Feasible witnesses prove the lower bounds

The rows in `witnesses.json` are [catalog index, swapped, minimum, list of masks]. Check each mask by evaluating all sixteen original weights directly. For the four cases with minimum 16, mask j satisfies every row other than row j (zero-based in the displayed order). That covers every size-15 subset, hence every proper subset. For the four cases with minimum 14, take the union of the subsets supported by the witness masks: all 560 size-13 subsets and 119 of the 120 size-14 subsets are covered. The only missing 14-subset is H without 25 and 60 (positions 9 and 14, selection bitmask 48639). Inclusion in a feasible subset proves feasibility, so every subset of size at most 13 is feasible.

## Exact empty joins prove the upper bounds

For a tested subset T of rows, split m into its even and odd column positions (14+13 bits). In each half enumerate all bit masks. Record the mismatch-count vector of the even half with y(t) for t in T; on the odd half record the vector of 14 minus the corresponding mismatch counts. The row equations hold simultaneously if and only if the same vector occurs on both sides. Thus an empty join is a complete infeasibility proof for this particular T; it does not assume that a projection obstruction is necessary.

The JavaScript verifier serializes each vector as two delimited integers, each with eight base-32 digits. Every used digit is in [0,14] and each integer is below 2^40, so the keys are exact and collision-free. It finds zero matches for all eight full sections and the four designated 14-subsets. It also recomputes H from B and repeats the published positive-weight control a=2; the original/swapped raw full-section counts are 128/48, 64/16, 64/16, 128/48, in table order. All eight stored a=2 positive masks are directly checked.

The two parts together prove exact minima and the reported uniqueness at minimum size. This does not give a shortest transformed equation system or arithmetic certificate; linear combinations can depend on many original rows. There is no claim for other markings, the entire q24 branch or the global distance bound.
