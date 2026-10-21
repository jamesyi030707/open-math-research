# Radius-thirteen endpoint audit

Date: 2026-10-21. AI-assisted independent verification. No originality claim.

## Result

The published endpoint argument is sound under its stated hypotheses. For an odd Boolean function u whose Walsh coefficients have absolute value at most 10, its distance from a rank-four quadratic h cannot be 13.

At distance 13 the sixteen aligned nonzero-support coefficients sum to 152. Each is at most 10 and congruent to 2 modulo 4, so the deficit from 160 is either one deficit of 8 or two deficits of 4. The restricted inverse Walsh transform must be a signed average of four signs, hence half-integral. In the first case it has illegal values at exactly 24 positions. In the second case the two exceptional signed characters cancel at 32 positions, giving illegal values of magnitude 5/8 there.

This argument applies also to an affine Walsh support: the signs in the four-point average do not affect half-integrality. The accompanying new checker audits all 136 endpoint profiles for each of the 128 affine perturbations of h=x0*x1+x2*x3. All 17,408 cases fail. Of these, 13,056 have genuinely affine rather than linear support. The exact observed invalid-position counts are 24 for a single defect and 40 for a double defect.

## Important stopping boundary

The single-spectrum obstruction is sharp at radius 15. Put u=h+x4*x5+delta_48, with x0 the least significant bit. This explicit odd function has weight 27, distance 15 from h, and maximum absolute Walsh coefficient 10. Its restricted aligned spectrum has ten entries equal to 10 and six equal to 6. Therefore a stronger bound cannot follow from this same single-spectrum condition alone. A further improvement would have to couple the translated spectra or use another condition.

This control is not a witness for the fixed BCH extension problem. No test of all eight translated spectra is asserted for it.

## Reproduction

Requires Node.js with BigInt support. No packages or downloads are needed.

    node audit_radius_thirteen.js > endpoint_audit_report.json

The program writes only JSON to standard output and throws on failure. All transform arithmetic uses exact integers of small magnitude. Its BigInt value is used only to encode the 64-bit control truth table.

## Source and scope

Reviewed source commit: a8c9ee90272b3c5f525e00a65b8667a97dc75172.

- [Original endpoint supplement](https://github.com/jamesyi030707/open-math-research/blob/a8c9ee90272b3c5f525e00a65b8667a97dc75172/history/2026-10-20/independent/radius_thirteen_supplement.md)
- [Original base proof](https://github.com/jamesyi030707/open-math-research/blob/a8c9ee90272b3c5f525e00a65b8667a97dc75172/history/2026-10-20/independent/quadratic_neighborhood_proof.md)

The full fixed-parent conclusion d(f,RM(2,6))>=15 also uses the earlier complete check that each quadratic has a rank-at-most-four translate in the specified three-dimensional quadratic space. That 32,768-form check was inspected but not rerun here. This audit does not remove the seven remaining aggregate profiles, solve the full fixed-parent model, prove global nonexistence of a binary [64,11,27] code, or constitute formal proof-assistant verification.
