# Audit of the October 22 Claude response

The actual response, Python source and saved stdout were inspected. The independent checker does not import or rerun that source, and does not reproduce its 1,500-sample experiment.

## Accepted core statement

For **distinct** q,q' in the specified bent-difference quadratic family, their difference is nonzero bent and the coefficient factor is 1/8. For equal translates the exact convolution formula with factor 1/64 still applies, but the difference is zero, not bent, and the operator is the identity rather than a dense signed 1/8 matrix. The response's opening sentence needs the word “distinct.”

The exact relation and involution are correct. With H squared equal to 64I and sign diagonal D_q squared equal to I, M=H D_q H/64 gives M squared equal to I. This proof does not require sample tests, nor bentness; bentness makes all entries have magnitude 1/8. M is real symmetric, so involution also gives orthogonality.

The eight translated spectral bounds plus a realizable Boolean truth table are the existing full model in different coordinates. The relation alone excludes no additional function. It may restore missing compatibility in a relaxed formulation that treats spectra independently, but that is not a strengthening of the common-variable formulation and no new aggregate exclusion was shown. The agreed stopping condition is therefore reached.

## Actual finite coverage, not an inferred general test

The saved source and log show:

- 40 pseudorandom truth tables, with all seven nonzero translations and all 56 ordered distinct pairs checked per table.
- Involution tested on 40 pseudorandom integer vectors for the single operator indexed 3. The prose must not suggest that these tests checked every operator matrix exhaustively. The general statement instead follows from algebra.
- 30 wrong-dual comparisons, all mismatching in the saved log. This is a bounded negative control, not a general theorem that every input detects a wrong dual.
- 1,500 generated quadratics followed by one to three randomly chosen flip operations **with replacement**. Repeated points can cancel, so the resulting Hamming distance is not guaranteed to be one to three. The count histogram was 954,66,318,155,7 for respectively 0,1,3,5,7 satisfied translates. These are only sample diagnostics, not exhaustive candidates or evidence about global feasibility. This extra sampling was not needed after identifying the redundancy.

The code builds a finite-field trace realization using polynomial 0x43 and verifies that its seven nonzero quadratics are bent. It does not itself prove equivalence to the repository's particular BCH coordinate labeling. The independent audit instead reuses the already published BCH quotient masks and performs four explicit controls and a 64-shift involution test there. No new equivalence claim between the two coordinate systems is needed for the universal convolution identity.

The supplementary 4-by-4 margin proof and examples in this independent audit were not submitted to or reviewed by Claude. They must not be attributed to it. They are also redundant once a common Boolean truth table is present and do not justify further same-family enumeration.
