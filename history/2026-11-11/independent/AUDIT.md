# Independent audit: parity periods exclude the fixed kernel-one branch

## Outcome and precise scope

The proposed proof is valid under its stated fixed-residual and normalized even-subcode assumptions. It excludes the entire one-dimensional left-projection-kernel branch for the archived residual B. It does not address the zero-kernel branch, other residual codes, or global binary [64,11,27] existence. It does not construct a new code or establish priority, novelty, external peer review, or proof-assistant certification.

This is a separately written AI-assisted mathematical and exact-computation audit, not independent human peer review. The proof outline and candidate restricted q20 columns were supplied by the investigator. This checker does not import the investigator's code. Its residual expansion, rank elimination, certificate discovery, actual-matrix controls, q20 extension and three-term Krawtchouk recurrence are separately implemented.

## Premises independently reconstructed

The input SHA-256 is `276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80`, matching the archived residual at source commit `3229383ae26e6c445adf62f70545553fcc5d2055`.

All 1,024 residual words were reconstructed. The residual has dimension ten, and h=1008 is the sole nonzero message with residual weight at least 27. A nonzero left-kernel vector must therefore be h. The chosen S consists of messages s<<4, has dimension five, and does not contain h. The t, s and h coordinates cover the complete message space.

Double-even rigidity has a necessary premise: D is the normalized even subcode. At every residual weight 14 message, the lift bounds and evenness force left weight 14 and total weight 28. For an even binary code, total weight divided by two modulo two is a quadratic polynomial in the message bits, with zero constant. The 160 weight 14 messages give rank 55 on all ten linear and 45 quadratic monomials. Hence every coefficient vanishes and D is doubly even.

All actual left-weight windows were then recalculated using both u and u+h. The zero message is handled separately as weight 0; applying the nonzero distance bound there would be incorrect. The ten recovered forced-14 hyperplanes are exactly:

`(t,n,c) = (2,22,0), (3,26,0), (5,8,0), (6,13,1), (8,10,1), (9,19,1), (10,14,0), (11,28,0), (12,29,0), (14,23,0)`.

Their normals span F2^5. Already 22,26,8,13,10 are independent. The other 16 messages in each listed coset permit exactly 10, 14, 18. The proof needs the constant14 half, not an assumed arbitrary weight histogram.

## Fourier signs and the artificial zero entry

Let L count columns nonzero on S, and let z be the weight on the 27-L zero-on-S positions in a fixed quotient coset. For v nonzero, a_v is the signed multiplicity, so a_v=m_v modulo two, regardless of repeats or triples. The true zero coefficient is a_0=27-L-2z.

The full sign sum is F(s)=27-2w(s). On n dot s=c, forced weight 14 gives F=-1. Restrictions of characters with labels v and v+n differ by the factor (-1)^c. Orthogonality on this sixteen-point affine hyperplane therefore gives

- a_v+(-1)^c a_(v+n)=0 for v not in {0,n}.
- a_0+(-1)^c a_n=-1, equivalently a_n=(L+2z-28)(-1)^c.

Thus m_n=L modulo two. Defining f(v)=m_v modulo two for v nonzero and **artificially defining f(0)=L modulo two** makes n a translation period of f. This is not the parity of the number of zero columns: that number is27-L and has the opposite parity. Confusing those two zero entries invalidates the argument. The independent real-matrix controls reject that incorrect substitution in every case.

Each forced hyperplane applies to the same actual restriction multiplicities. Quotient offsets and repeated-column signs disappear modulo two. Since the normals span the full five-dimensional space, their translation periods force f to be constant on all 32 labels. No orientation classification or canonical-coordinate assumption is being smuggled in.

## The final contradictions cover every possible q

On S, all 31 nonzero weights are 12 or 16. If q of them are12, the first moment gives L=31-q/4. Integrality, q between 0 and 31, and L at most 27 leave precisely q=16,20,24,28.

The zero-coset centered second moment independently gives sum(m_v^2)=992-14q-L^2, yielding:

- q=16: L=27, squared sum 39.
- q=20: L=26, squared sum 36.
- q=24: L=25, squared sum 31.
- q=28: L=24, squared sum 24.

If L is odd, every one of the31 nonzero multiplicities is odd and positive, impossible with L<31. If L is even, every multiplicity is even and nonnegative, so m_v^2>=2m_v. Summing requires squared sum at least 2L, contradicted by 36<52 and 24<48. This proof covers the whole kernel-one branch directly; it does not depend on rerunning the older q24/q28 exclusions.

## Controls, old witnesses and measured coverage

The independent checker builds 186 actual binary length 27 matrices: all 31 nonzero normals, both affine offsets, and three repeated-column patterns. The matrices have ranks five or six. Their real coset weights are 14 on the specified affine hyperplane. Full character expansion, both special-coefficient signs, zero-on-S positions, repeated multiplicities up to four and parity-period identities all pass. These are controls for the general lemma, not asserted q16/q20 target restrictions.

A separate genuine q20 local restriction is extended to a rank-nine length 27 left matrix with exact kernel {0,h}. It realizes local distribution 1+20z^12+11z^16, squared multiplicity sum 36, and all 16 coset-energy identities. This independently chosen extension violates 164 full residual-lift inequalities, 736 double-even conditions and 142 forced-14 point constraints. It is not a target code. The originator's different extension has a different failure count; the two are not interchangeable.

The older formal points with seven counts `(20,16,84,32,18,44,18)` and `(24,20,80,32,18,44,18)` are independently reconstructed. Both pass all 11 domain bounds and 1,064 integral nonnegative split-transform coefficients, calculated by a three-term Krawtchouk recurrence. The November 8 incidence slacks are 0 and 1. Thus the new message-level obstruction is nonredundant with those old aggregate conditions; it does not retract their formal feasibility.

A changed affine-hyperplane offset is rejected. The wrong zero-parity normalization is rejected in all 186 real-matrix controls.

Run from this directory:

```sh
timeout 60s python -I -B audit_fourier_branch.py > replay.json
timeout 60s python -I -O -B audit_fourier_branch.py > replay_optimized.json
```

Both recorded runs passed in about 0.08 CPU seconds apiece. Output is identical except the machine-dependent CPU time. No numerical solver, target-matrix search, installation, network mutation or older large search was run by this audit.

## Sources

- [Archived residual input](https://github.com/jamesyi030707/open-math-research/blob/3229383ae26e6c445adf62f70545553fcc5d2055/history/2026-11-10/inputs/residual_candidate.json)
- [Inherited q24 proof and fixed-input premises](https://github.com/jamesyi030707/open-math-research/blob/3229383ae26e6c445adf62f70545553fcc5d2055/history/2026-11-10/RESULT.md)
- [Earlier aggregate survivors and incidence cut](https://github.com/jamesyi030707/open-math-research/blob/3229383ae26e6c445adf62f70545553fcc5d2055/history/2026-11-08/RESULT.md)
- [Repository scope and errata](https://github.com/jamesyi030707/open-math-research/blob/3229383ae26e6c445adf62f70545553fcc5d2055/ERRATA.md)

The first-party Grassl [64,11] page accessed November 11 still displays 26–27; the web tool labels that response as crawled the preceding day. This mathematical audit does not make a comprehensive current-literature or novelty claim.
