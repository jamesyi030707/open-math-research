# Corrections and limits

1. The previous discussion's final LP statement was wrong. A real relaxation's infeasibility excludes its integer subset. Real feasibility does not establish integer feasibility or realizability. This was explicitly corrected in round 1, continuing the October 15 erratum.
2. Round 1's prose unextended weight enumerator omitted the zero word. Its count is one; the attached numerical results include it. Round 2 corrects the prose.
3. Random odd cosets of minimum weight 17–21 passed only general transform constraints. They do not meet the target support restriction 27–37. Round 2 explicitly corrects this ambiguity.
4. “512 inequalities” means 512 two-sided absolute-value bounds, or 1,024 one-sided inequalities, together with shared binary variables and odd parity. The continuous relaxation alone is not the exact model.
5. Fourth moments are not universal constants. For each translate h=f+q the identity uses its own autocorrelation: sum W_h^4 = 64 sum C_h^2. The displayed general bounds are coarse, not an existence certificate.
6. All 25 distributions satisfy the stated necessary model, not all possible combinatorial constraints. Neither a distance-27 code nor a nonexistence proof was produced. The fixed-parent coupled feasibility problem remains unsolved here.

Downloaded mathematical files are preserved verbatim. Filename prefixes label their source; original references to unprefixed companion filenames are descriptive. Generated code has been inspected, while claims are checked using the separate independent implementation. No external formal verification is asserted.
