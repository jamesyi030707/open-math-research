# A quotient-map obstruction at q = 28

## Statement and scope

For the archived 10 × 37 residual matrix B, no 10 × 27 left matrix A in the kernel-one branch can realize q = 28 and satisfy the required distance-27 lift conditions and the established doubly-even normalization.

This excludes only q = 28 for this B and this branch. It does not exclude q = 16, 20, 24, the kernel-zero branch, other residual matrices, or binary [64,11,27] codes in general.

The inherited input and normalization are recorded in the [November 8 checker](https://github.com/jamesyi030707/open-math-research/blob/3157b1c81a69ddb061cc21f9aaeaac93eadd9a11/history/2026-11-08/check_column_cut.py). The [residual JSON](https://github.com/jamesyi030707/open-math-research/blob/3157b1c81a69ddb061cc21f9aaeaac93eadd9a11/history/2026-11-08/inputs/residual_candidate.json) has Git blob 8f76beaa5994563a2980ea9cb87412640d6560b4. The classification and character identities used below have a [separate prior proof](https://github.com/jamesyi030707/open-math-research/blob/3157b1c81a69ddb061cc21f9aaeaac93eadd9a11/history/2026-11-08/subspace/audit_subspace_extensions.md).

## Coordinates and the classified restriction

Messages are row vectors, so the kernel condition is hA = 0, with h = 1008 in ten-bit notation. Let Q = F₂¹⁰/⟨h⟩. Representatives 0,…,511 give a nine-dimensional complement to h. Write each representative uniquely as t + 16s, where 0 ≤ t < 16 and 0 ≤ s < 32. The s coordinates represent the five-dimensional subspace S; t labels Q/S.

Under q = 28, the restriction to S has 24 distinct nonzero column functionals, namely S* minus a three-dimensional subspace U, together with three columns whose restrictions to S are zero. Put K = U⊥, a two-dimensional subspace of S. Its placement is unknown and is not fixed by a row-equivalence classification.

In a coset t + S, let a_s be the full left weight and let z be the weight on the three zero-on-S coordinates. Those three coordinates are constant along S. The classified active columns give the exact identities

- Σ_s a_s = 384 + 32z;
- Σ_s (a_s − 12 − z)² = 192;
- Σ_(s in b+K) a_s = 48 + 4z for every four-element K-coset b+K in S.

These follow from character orthogonality. In particular, the last identity holds for the actual unknown K, not just for one standard placement. The independent audit checks the corresponding character and Gram identities for all 155 two-dimensional subspaces.

## Exact residual certificate

Let F = {2,3,5,6,8,9,10,11,12,14}. For each t in F, the two residual messages u = t + 16s and u+h give the simultaneous necessary conditions

27 − wt(uB) ≤ a_s ≤ wt(uB),
27 − wt((u+h)B) ≤ a_s ≤ wt((u+h)B),

and a_s + wt(uB) ≡ a_s + wt((u+h)B) ≡ 0 modulo 4.

Exactly sixteen values of s force a_s = 14. The other sixteen allow a_s ∈ {10,14,18}. The forced positions are an affine hyperplane H_t = {s : v_t·s = c_t}. Their coefficients are:

| t | v_t | c_t |
|---|---|---|
| 2 | 22 | 0 |
| 3 | 26 | 0 |
| 5 | 8 | 0 |
| 6 | 13 | 1 |
| 8 | 10 | 1 |
| 9 | 19 | 1 |
| 10 | 14 | 0 |
| 11 | 28 | 0 |
| 12 | 29 | 0 |
| 14 | 23 | 0 |

All labels in this table are ordinary binary integers; the dot product is over F₂. The minimal certificate checks all 320 positions against both original-message windows. The separate audit reconstructs every residual codeword directly from its 37 binary coordinates and derives the hyperplanes afresh.

## Every t in F forces z = 2

Let n₁₀ and n₁₈ count the variable entries with those weights. The two full-coset moments imply

n₁₈ − n₁₀ = 8(z−2),
n₁₀ + n₁₈ = 12 + 2(z−2)².

Since there are only sixteen variable entries, z = 0 would require twenty non-14 entries and is impossible. It remains to exclude z = 1 and z = 3.

If K lies in ker(v_t), four of its eight affine blocks lie entirely in H_t. Such a block has four weights 14 and sum 56, which forces 48 + 4z = 56 and hence z = 2.

Otherwise each K-block meets H_t in exactly two positions. Its other two weights belong to {10,14,18}. At z = 1, their sum must be 24, so the pair is {10,14}. At z = 3, their sum must be 32, so it is {14,18}. In either case the block's squared deviations from 12+z sum to 12. Eight blocks would therefore give 96, contradicting the required 192.

Thus z(t) = 2 for every t in F, for every possible placement of K.

## The three coordinates cannot satisfy those weights

The three zero-on-S coordinates induce a linear map L : F₂⁴ → F₂³, with z(t) = wt(L(t)).

The weight-two vectors of F₂³, together with zero, form its two-dimensional even-weight subspace W. Since F spans F₂⁴, the condition z(t) = 2 on F forces the entire image of L into W. Hence ker(L) has dimension at least two.

No element of F belongs to ker(L), so all nonzero kernel elements must lie in E = {1,4,7,13,15}. But the ten pairwise sums of distinct elements of E are exactly F. In particular E cannot contain the three nonzero elements of any two-dimensional subspace. This is a contradiction.

This argument allows repeated or globally zero columns. As separate finite controls, the minimal checker tests all 816 unordered triples of four-bit coordinate functionals, and the independent audit tests all 4,096 ordered triples. Neither finds a map satisfying the ten forced weights.

## Computation and attribution boundaries

The initial dynamic program examines all 155 possible planes, 15 nonzero quotient cosets and four values of z. It leaves every plane feasible when cosets are treated independently, but forces z = 2 on F. The exclusion comes from the additional cross-coset linear-map argument, not from a negative solver status or a matrix search.

initial_coset_dp.py and initial_coset_dp_original_output.json preserve the original bounded experiment. Its measured CPU time was 0.625242789 seconds. The replay is separately named. The minimal checker first ran in 0.001647929 CPU seconds, with a separately recorded replay. Only Python's standard library is required. Run with python -I -B, not -O; an external timeout of 60 seconds suffices for each supplied check.

The actual Claude exchange reviewed the conditional linear-map contradiction while the forced-z premise was still preliminary. The hyperplane proof above and its independent audit were completed afterward and were not sent for another Claude review. The dialogue preserves that boundary. “Independent” means a separately written implementation, not external human peer review or formal proof-assistant certification.
