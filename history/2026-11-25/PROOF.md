# One parity certificate for eight full sections

Use the fixed residual and notation of the [November 24 analysis](../2026-11-24/PROOF.md). The zero-based q24 catalogue is pinned to commit [ec9d825](https://github.com/jamesyi030707/open-math-research/blob/ec9d825da2fa67afe2387c2cbb2d00541808fc9a/history/2026-11-15/h.json). The given 27 column positions remain distinct even when labels coincide.

For each label t in H = (0,4,5,10,11,15,18,19,23,25,33,46,54,56,60,61), let χ_t(c) = (−1)^parity(t & c). For x_j in {0,1}, set ε_j = 1 − 2x_j. A weight of 14 on 27 positions means Σ_j χ_t(c_j) ε_j = −1. Give rows 4,10,15,33 coefficient −1 and every other row coefficient +1. The sum of row coefficients is 8. Consequently F(c) = Σ_t λ_t χ_t(c) must satisfy Σ_j F(c_j) ε_j = −8.

The finite character evaluation gives F/8 supported on S = {0,7,10,13,16,23,26,29,33,36,40,45,50,55,59,62}. It equals −1 at {10,16,33,59}, +1 elsewhere on S, and zero outside. After division by 8 and reduction modulo 2, every supported position contributes 1 regardless of its sign and ε_j. Thus an **odd** number of positions must have labels in S.

| Catalogue index | Original positions in S | Swapped positions in S |
|---:|---:|---:|
| 19 | 8 | 8 |
| 115 | 6 | 6 |
| 139 | 8 | 8 |
| 163 | 6 | 6 |

Swapping bits 0 and 2 of a label preserves S, so hit counts agree for every paired marking. Among the 277 catalogue entries, exactly 128 indices in each orientation fail this rule. These are marked entries, not a count of distinct or newly excluded orbits. The proof uses all sixteen rows; it does not imply that any proper uncombined subset is inconsistent.

## Contrast: remove 25 and 60

For 115 and 139 in either orientation, the remaining fourteen rows are binary-infeasible by the [previous exact join](../2026-11-24/PROOF.md). Write A[t,j] = χ_t(c_j), b[t] = (1 + Σ_j A[t,j])/2. All four listed sparse witnesses solve Ax=b over the nonnegative integers, each with at least one coordinate greater than one. Here an extended variable merely satisfies the linear equalities; it is not a bit or an actual weight interpretation. Since there is an integer solution, these fourteen equalities alone cannot yield an integer-congruence contradiction. The binary exclusion needs a constraint absent from this relaxation. This does not explain why this deletion pair is unique.

## Modular comparison on the full sixteen rows

The exact finite checks leave all entries feasible modulo 4, and find the same 141 infeasible indices in each orientation modulo 8 and modulo 16. The same thirteen indices beyond the displayed parity rule are listed for both orientations. For each of these 26 marked entries, the supplied multiplier y satisfies yA = 0 mod 8 and yb = 4 mod 8 directly on the original integer matrix. Other modular rejections and positive residues are checked in the replay: an entry of smallest 2-adic valuation divides every remaining matrix entry, so its odd part can be normalized by a unit and its column cleared below. A right-hand side not divisible by the pivot's power of two (or a nonzero zero-row target) yields a congruence certificate; otherwise back-substitution yields residues that are checked against all original rows. The equality of exclusion counts at 8 and 16 is a finite observation, not a stabilization theorem for arbitrary moduli or sections.

All claims are limited to this actual section, catalogue and two markings. There is no new distance bound or exclusion of a whole branch.
