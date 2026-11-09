# Independent review of the q=28 exclusion

Verdict: PASS for the fixed archived residual B, left-projection-kernel-one branch. No fatal defect or circularity found. This excludes q=28, not the other q values or the whole branch. It does not address other residuals, the kernel-zero branch, or global binary [64,11,27] existence.

## Inputs and prior premises

The public residual file was fetched at commit 74a2d33c0f9536100a7bed277db521b2707bdfd0; its Git blob 8f76beaa5994563a2980ea9cb87412640d6560b4 matches the local input exactly. Independent computation confirms rank 10, the published 1,024-word spectrum, and h=1008 as the only nonzero message with residual weight at least 27. Thus an actual kernel-one lift has hA=0.

The even-subcode normalization is legitimate: adding c=(1^27,0^37) to individual generator rows makes the left rows even because c has odd weight and all B words have even weight. On the 160 residual weight-14 messages the distance windows force left weight 14. The no-constant quadratic evaluation matrix on these messages has rank 55, independently rechecked. Therefore q_A=q_B and all normalized lifted words have weight divisible by four. This is a prior necessary theorem, not an assumption of q=28 or any conjectured exclusion.

S={0,16,...,496} is five-dimensional and disjoint from span(h). Its 31 nonzero elements represent exactly the 31 residual (16,16) pairs. The low four message bits provide a complement to S+span(h), so all quotient messages are uniquely t+(s<<4), with t in F2^4 and s in F2^5. No unproved symmetry normalization is used.

## Why 155 cases are exhaustive

For q=28, S has 28 words of weight 12 and three of weight 16. The first moment gives 24 nonzero restricted columns and three zero restricted columns. Let H be the three heavy messages. For nonzero restricted column label v, Fourier inversion gives

m(v) = (12 - 4 sum_{s in H} (-1)^(s dot v))/16.

Nonnegative integrality for every v forces the three messages in H to sum to zero. Hence H=K minus {0} for a two-dimensional K. Conversely every such K gives one occurrence of each of the 24 labels outside K-perp, and no occurrence of any nonzero label in K-perp. The zero label has multiplicity three. Independently checking all binomial(31,3)=4,495 heavy triples finds exactly 155 valid K. K is two-dimensional; K-perp is three-dimensional. Calling K itself a three-dimensional annihilator would be a notation error, not a missing case.

## Required identities and corrected moments

Let z(t) be the weight contributed by the three columns vanishing on S. These are three linear functionals of t, possibly repeated or zero. Each of the other 24 columns restricts nontrivially to K. Consequently every affine K coset has total left weight 48+4z(t). Distinct restricted labels and character orthogonality give

sum_{s in F2^5} (wt((t+(s<<4))A)-12-z(t))^2 = 192.

This equality, not an upper bound, is essential. It does not assume that any candidate extension exists, beyond the hypothetical lift whose necessary consequences are being tested.

For T={2,3,5,6,8,9,10,11,12,14}, the exact distance-plus-double-even windows consist of sixteen {14} and sixteen {10,14,18}. The broad locations form an affine hyperplane in s. For any K, their intersections with its eight cosets have either sizes 0,0,0,0,4,4,4,4 or sizes 2,2,2,2,2,2,2,2.

In the first case a coset with four narrow windows forces z(t)=2. In the second case the coset sums force total centered second moments 128 for z=0 and 96 for z=1 or 3. None equals 192. Thus z(t)=2 for all ten t in T. The corrected z=0 value is **128**, not 96. It still contradicts 192, so the correction does not weaken the exclusion.

The independent checker recomputed all 1,550 K/t cases, with 350 first-type and 1,200 second-type cases. It also verified the moment identity directly on a concrete arbitrary quotient lift for each K and every t, as an implementation control.

## Three-column contradiction without exhaustive search

Write L:F2^4 -> F2^3 for the three zero-on-S columns. Its weight is two at all ten points of T. The parity of L is a linear functional; if nonzero it vanishes at exactly eight inputs. Since it vanishes at ten, it is zero, so rank(L)<=2 and dim ker(L)>=2.

However, the complement Z=F2^4 minus T={0,1,4,7,13,15} contains no two-dimensional subspace: every sum of two distinct nonzero elements of Z is in T. Since ker(L) must be contained in Z, this is impossible. As a separate finite control, all 816 unordered triples of four-bit column labels were tested and none has weight two on all T. Zero and repeated columns are included.

## Limitations and minor presentation issue

The exploratory scripts construct an empty window at t=s=0 by applying a distance inequality intended only for nonzero messages. Their actual loops use t=1,...,15, so this has no effect. A publication should omit the zero-message entry or explicitly override it by left weight zero, rather than describe the entire raw array as valid target windows.

No split-MacWilliams feasibility assumption, November 8 column cut, numerical solver result, candidate full matrix, or external parameter table is needed for this proof. The exclusion is therefore not circular with those earlier formal-model results. The old q=28 formal survivor remains a valid formal-distribution witness, now shown not realizable by a target lift in this branch.

Confidence is high at the mathematical and exact finite-check levels. This is not formal proof-assistant certification or external peer review. The verification itself does not publish or alter repository content.

## Verification artifacts and public sources

- [review.py](review.py): independently written standard-library checker, with explicit exceptions instead of assert.
- [result.json](result.json): actual PASS output; approximately 0.63 CPU seconds in this run.
- https://github.com/jamesyi030707/open-math-research/blob/74a2d33c0f9536100a7bed277db521b2707bdfd0/history/2026-11-07/residual_candidate.json
- https://github.com/jamesyi030707/open-math-research/blob/main/notes/codes-residual-lift.md
- https://github.com/jamesyi030707/open-math-research/blob/main/notes/codes-quadratic-rigidity.md
- https://github.com/jamesyi030707/open-math-research/blob/main/notes/codes-subspace-obstruction.md
- https://github.com/jamesyi030707/open-math-research/blob/main/notes/codes-message-realization.md

Publication normalization: local absolute artifact paths were replaced by relative links, and the checker input path was changed to the pinned sibling input. Mathematical code and results are otherwise unchanged.
