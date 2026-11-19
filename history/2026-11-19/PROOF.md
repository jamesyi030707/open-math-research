# Counting true translation orbits on a non-invariant slice

## Precisely defined set
Fix B, W, h and the normalized doubly-even kernel-zero setting of November 14–18. Let X comprise ALL locally valid q24 W-column multisets satisfying a(0)+max b<=2. Message labels are retained; column order is ignored. X has 69,440*276=19,165,440 elements. It is **not** the set left after all previous external-extension exclusions.

The verified 32-element residual translation group G acts by (v,e)->(v+et,e). It fixes a and translates b. This preserves full-lift extendability by actual B coordinate equivalence. Arbitrary GL(5,2) is used below only for local classification, not for full-lift equivalence.

## Counting a slice of each orbit
For c in X, its stabilizer is H={t: b(v+t)=b(v) for every v}. Its full orbit has 32/|H| column multisets. By the previously proved moment identity q(t)=16+4(a(0)+b(t)), precisely T={t:a(0)+b(t)=2} sends c into q24. The obstruction a(0)+max b is translation invariant, so these q24 images all belong to X. Each image has |H| preimages; hence
N(c)=|G.c intersect X|=|T|/|H|.

Every orbit meeting X contributes N copies of 1/N to sum over c in X. Therefore that sum counts orbits exactly, despite X not being invariant. This is not Burnside applied incorrectly to a non-invariant set.

The r value is fixed throughout a full orbit. The z=b(0) value may change outside X, but inside X it equals 2-a(0), so (r,z) layers do not mix within the slice.

## Exact local table
|r|z|markings at each E|T size|H size|N|
|---|---|---|---|---|---|
|4|1|18|4|4|1|
|8|1|96|8|1|8|
|8|2|24|1|1|1|
|20|1|24|20|1|20|
|20|2|96|1|1|1|
|24|2|18|3|1|3|

Changing S labels by GL permutes translation parameters and conjugates H. It preserves |T| and |H|, so the canonical table holds at all 69,440 E. We do not identify any two actual B problems using this GL.

The full weighted sum is
69,440*(18+96/8+24+24/20+96+18/3)=10,915,968.
The per-E subtotal 786/5 is not an orbit count on canonical E. In fact its 276 patterns lie in 276 different full translation orbits. Multiplication completes the weighted sum over the entire X.

## Canonical representative and limits
Sort each translated 27-column list. Among translations with q24, select the lexicographically least list, retaining a t and the associated actual B automorphism as witness. This is a unique representative of each nonempty intersection with X; precomposition transports any full extension to that representative. A local stabilizer need not act trivially on external rows. Do not discard external extensions merely because the local restriction is fixed.

This reduces duplicate local restriction cases, not the number of possible full matrices by the same factor, and gives no new impossibility certificate. In particular r4,z1 sees no reduction within q24. Even the reduced count exceeds ten million, so no brute-force enumeration is started.

## Verification
Two separately written integer implementations reconstruct all 32 images of each of the 276 canonical survivors, directly count nonzero-S weights, compare stabilizer and slice formulas, and check canonical keys. Normal and optimized Python runs agree. The existing classification supplies all E and its GL equivalence, previously independently enumerated on November 18. Today's programs do not generate ten million representatives or re-run the old external exclusions.
