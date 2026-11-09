# Independent audit of the fixed-residual q = 28 exclusion

## Verdict and scope

The corrected argument is valid for the archived residual B and the branch in
which the normalized even-subcode left matrix A has kernel span(1008). Within
that branch, q = 28 is impossible. This audit does not exclude q = 16, 20, 24,
the kernel-zero branch, any other residual, or all binary [64,11,27] codes.
It does not improve the published parameter bounds.

The baseline read from GitHub was commit
3157b1c81a69ddb061cc21f9aaeaac93eadd9a11. The archived residual file was checked
against Git blob 8f76beaa5994563a2980ea9cb87412640d6560b4, and its ten rows
match the independent auditor's constants. The independent enumeration was
written before reading the researcher's enumeration implementation. Both
implementations agree. This is separate implementation, not external peer
review or proof-kernel formalization.

## Hypotheses and inherited results rechecked

The auditor reconstructs all 1,024 residual words, verifies rank 10, and obtains
the distribution 0:1, 14:160, 16:142, 18:320, 20:160, 22:160, 24:80, 32:1.
The sole word of weight at least 27 has message h = 1008. It verifies the
specified five-dimensional S and its pairs modulo h. Independently generated
degree-one and degree-two evaluation vectors on the 160 weight-14 messages
have rank 55, validating the archived premise that the normalized even
subcode is doubly even.

The exact permitted left weights are computed from both members u and u+h:
27-wt(uB) <= a <= wt(uB), 27-wt((u+h)B) <= a <= wt((u+h)B), and
a+wt(uB) = a+wt((u+h)B) = 0 modulo 4. No h-pair inequality is omitted.

The q = 28 classification is algebraic: first and second moments imply 24
distinct nonzero restricted columns. Their seven-element complement in the
31 nonzero vectors spans a three-dimensional U and equals U minus zero.
There are also three columns zero on S. Thus K = U-perp has dimension two.
For every extension coset and zero-column weight z, every four-message K-block
has weight sum 48+4z, and the sum of (weight-12-z)^2 over all 32 messages is 192.
These are character-orthogonality identities, not extrapolations from controls.

## Short obstruction and correction

For each t in {2,3,5,6,8,9,10,11,12,14}, exactly one affine hyperplane of S
has forced left weight 14; the other 16 messages allow {10,14,18}. The ten
hyperplane equations are independently recovered and included in the result.

If K is contained in the hyperplane's direction, a whole K-block is forced to
weight 14 throughout. Its sum 56 implies z = 2. Otherwise each block has two
forced 14s. For z = 0 the remaining pair must be (10,10); centered squares sum
to 16 per block, hence 128 overall, not 192. For z = 1 or3 the remaining pair is
(10,14) or (14,18), respectively; centered squares sum to 12 per block, hence 96
overall, not 192. Consequently all ten cosets require z = 2.

An earlier scratch explanation incorrectly said z = 0 failed the minimum
block sum. It does not: its block sum 48 is attainable. The second-moment
contradiction 128 != 192 is the valid correction and is used in the final proof.

The ten coset labels are exactly the pairwise sums of {1,4,7,13,15}. The three
coordinates zero on S define a linear map from the four-dimensional quotient
to F2^3. The images of these five labels would be pairwise distance two. They
must be distinct and of the same parity, yet a parity class of F2^3 has only
four elements. This contradiction proves the stated exclusion.

## Finite checks and controls

The independent auditor enumerates all 155 two-dimensional K, all 15 nonzero
quotient cosets, and all 4 values of z. For each four-message block it enumerates
all tuples from the exact weight windows, then uses exact integer sets of
reachable square sums. It agrees for every K: the ten specified cosets permit
only z = 2; the other five are not eliminated at this necessary-condition level.
All4,096 ordered triples of four-bit column labels, covering every linear map
F2^4 -> F2^3, fail the ten required weight-two evaluations.

A real [27,5,12] q = 28 restriction with 24 distinct active columns and 3 zero
columns supplies a positive control. Eight specified sign assignments times
four zero-coordinate weights verify 32 actual extension-coset identities.
These controls do not claim exhaustive sign-assignment coverage. Four
three-bit vectors {000,011,101,110} supply a tight positive control for the
terminal distance-two bound. Three explicit corruptions are rejected.

Run `python independent_audit.py`. It uses only the standard library and no
solver. The recorded run completed in about 0.5 CPU seconds. Runtime is not a
mathematical guarantee; the finite domains and exact integers define coverage.

## First-party table check

On 2026-11-09 the first-party Grassl entry was directly retrieved and marked
"Crawled: today" by the web reader:
https://www.codetables.de/BKLC/BKLC.php?q=2&n=64&k=11

It displays lower bound 26 and upper bound 27. Its construction timestamp is
2001-01-30 and its footer says last change 30.12.2011. This is confirmation of
what the retrieved table displays, not comprehensive literature verification.
