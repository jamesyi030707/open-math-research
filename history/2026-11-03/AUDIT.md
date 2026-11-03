# Independent congruence audit

Status: PASS. Performed with Python integer arithmetic and the standard library only, without importing or executing the reducer, its verifier, or the affine generator.

## Inputs and exact checks

CSV: `../2026-10-29/affine_coefficients.csv`.
SHA-256: `c49805f554e88c468d92d1835fb19f47480295a95eb32f5c18e53db05277323c`.
Certificate: `certificate.json`.

The CSV contains 1064 rows, seven variable coefficients and an affine constant. All denominators are 1024, and all eight numerator columns are divisible by 16. Let A be these eight-column rows divided by 16, reduced modulo 64. Let B be the six certificate rows. The independently checked certificate gives B=TA and A=CB over Z/64Z. All 48 entries of the first identity and all 8512 entries of the second identity passed. Indexing of the sparse T witnesses is zero-based CSV data-row indexing (excluding the header).

For every integer variable vector x and augmented vector z=(x,1), these identities imply Az=0 iff Bz=0 modulo 64. Since each original row is exactly divisible by 16, its numerator vanishes modulo 1024 iff its divided row vanishes modulo 64. Thus the certificate proves equivalence to the supplied CSV integrality conditions for all integer inputs, not merely sampled inputs.

## Equivalent six relations

With variable order p,q,y10,y14,z8,z12,z16:

1. p+q+2y10+y14+3z8+2z12+z16 = 12 (mod 64).
2. 2q+2y10+y14 = 8 (mod 16).
3. q+y10-z12-z16 = 6 (mod 8).
4. q+2z8+2z16 = 0 (mod 4).
5. z12+z16 = 0 (mod 2).
6. z8+z16 = 0 (mod 2).

The checker verifies the scaled augmented coefficient vector of each relation equals its certificate row modulo 64. Scaling by 64/m converts a relation modulo m into an equivalent relation modulo 64, so this proves their exact equivalence. In the presence of relation 6, relation 4 may equivalently be replaced by q=0 (mod 4). These are six generating relations; this audit does not claim that this list is a Smith normal form or prove minimality.

## Claude example and integer bounds

For M=[[2,4],[0,8],[2,12]], U=[[1,0,0],[0,1,0],[-1,-1,1]], V=[[1,-2],[0,1]], and b=(6,8,14), direct integer multiplication gives UMV=[[2,0],[0,8],[0,0]], Ub=(6,8,0). U and V have determinant 1 (triangular with diagonal entries 1). Writing x=Vy gives y1=3 (mod 8) and y2=1 (mod 2). Enumeration of all 256 pairs modulo 16 confirms exactly 16 solution residues and the bijection induced by V.

For the integer point x=(1,9), V^{-1}x=(19,9). Replacing it by its canonical residue representative (3,9) and applying V gives (-15,9), not the original integer point. Both have the same residue modulo 16. Consequently modular equivalence alone does not preserve an integer box under canonicalization. For example, x lies in [0,15]^2 whereas (-15,9) does not. Bounds must be transported as inequalities on Vy, or the relevant lifts retained. In general, if y=y0+16k, then x=Vy0+16Vk; discarding k can discard the bounded representative. Canonicalizing x again restores the residue-class representative in [0,15]^2, but arbitrary integer bounds need separate treatment.

## Scope and reproduction

Run `python -I -B history/2026-11-03/independent_verify.py` from the repository root. Recorded output is in `independent_result.json`. The script uses assertions and should be run without Python's `-O` option.

This proves only the congruence equivalence for the supplied CSV and the stated toy example. It does not independently derive the CSV from the underlying mathematical model, verify positivity or other inequalities, establish realizability or code existence, or validate provenance beyond the pinned input digest. The audit does not attest to the publication process.
