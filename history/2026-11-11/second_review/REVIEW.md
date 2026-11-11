# Independent review: fixed-residual kernel-one parity obstruction

## Verdict

**The proposed exclusion is valid for the archived residual B and the one-dimensional left-projection-kernel branch.** I found no missing assumption or incorrect inference. The Fourier argument excludes all four possible q values directly. In particular it closes q=16 and q=20, without extrapolating the q=24 restriction classification or treating numerical infeasibility as a certificate.

It does not exclude the kernel-zero branch, other [37,10,14] residuals, or all binary [64,11,27] codes. It does not establish novelty, a parameter improvement, external peer review, or proof-assistant certification.

The current public source was checked at commit `3229383ae26e6c445adf62f70545553fcc5d2055`, whose latest published result is q=24. The archived residual was fetched through the GitHub connector and compared with the local pinned bytes. Its Git blob is `8f76beaa5994563a2980ea9cb87412640d6560b4`, SHA-256 `276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80`.

## Hypotheses and their justification

1. Write a hypothetical lift as the span of c=(1^27,0^37) and (A,B). The pinned B has rank ten, and every B word is even. Adding c to selected generator rows normalizes the ten rows to span the unique even subcode D. Thus every uA is even; this normalization loses no candidate lift.

2. For every nonzero u, the two words associated with u and c+u give exactly `27-wt(uB) <= wt(uA) <= wt(uB)`. When wt(uB)=14, evenness forces wt(uA)=14, so wt(uD)=28.

3. On an even binary code, Q(u)=wt(uD)/2 modulo two is a quadratic function in the ten message variables, with no constant term. The 160 minimum-weight messages of B give Q=0. Their evaluation matrix on the ten linear and 45 square-free quadratic monomials has rank 55, independently recomputed. Hence Q=0 everywhere, and D is doubly even. In particular `wt(uA)+wt(uB)=0 mod 4`. The replay also reconstructs Q_B on all 1,024 messages and recovers coefficient mask `0x10080a` in the stated monomial order.

4. The only nonzero message of residual weight at least 27 is h=1008, of weight 32. In the kernel-one branch, therefore, ker(A)=span(h). The left-projection kernel in the full code agrees with that in D: any word with left part zero has even weight because its right part is in B. Thus the branch terminology is consistent.

5. With S=span(16,32,64,128,256), S, span(h), and span(1,2,4,8) form a direct sum of the ten-dimensional message space. The representatives `t XOR (s<<4)` therefore cover every h-pair once. Independently, all residual (16,16) pairs are exactly the 31 nonzero elements of S and their h-translates. On S the allowed left weights are precisely 12 and 16, so q denotes the same count of weight-12 pairs as in the existing aggregate model.

## The new step, including the artificial origin

Let m_v be the number of coordinate positions with nonzero restricted column label v in S*=F2^5, and let L=sum m_v. Zero-on-S columns are not part of L. For a quotient representative t, write z_t for their left weight and a_v(t) for the signed sum of the columns with label v. Then a_v(t)=m_v modulo two and

    w_t(s) = L/2 + z_t - (1/2) sum_(v != 0) a_v(t) (-1)^(v dot s).

Suppose w_t is constant K on the affine hyperplane n dot s=c. Restricting characters to that hyperplane identifies exactly the pairs {v,v+n}, with relative sign (-1)^c. All nonconstant restricted-character coefficients must vanish, so

    a_v(t) + (-1)^c a_(v+n)(t) = 0,  v not in {0,n}.

The constant coefficient gives

    a_n(t) = (-1)^c (L + 2z_t - 2K).

Modulo two these say m_v=m_(v+n) for nonzero paired labels, and m_n=L. Therefore the auxiliary function

    f(0)=L mod 2; f(v)=m_v mod 2 for v != 0

is invariant under translation by n. This origin is a legitimate auxiliary definition, not an assumption about a physical zero-column multiplicity. In fact the physical zero-column count is 27-L and has the opposite parity. Confusing those two quantities would invalidate the proof. The candidate uses the correct one.

Direct exhaustive reconstruction from B gives exactly the ten hyperplanes from the q=24 archive, each with K=14 and complementary allowed weights {10,14,18}:

    (t,n,c) = (2,22,0), (3,26,0), (5,8,0), (6,13,1), (8,10,1),
              (9,19,1), (10,14,0), (11,28,0), (12,29,0), (14,23,0).

Their normals span all of F2^5; the first five listed already form a basis. Although the signed coefficients a_v depend on t, their parities are the same fixed m_v, which is why periods from different t can be combined. The resulting 320 parity equalities have rank 31 on the 32 values of f, leaving exactly the constant functions. Consequently every nonzero m_v has parity L.

This argument needs neither a particular q=24 orientation nor its classification, nor the complementary window beyond establishing the forced hyperplane. It applies to every candidate in the branch.

## Exhaustive parameter conclusion from first two moments

The distribution on S is one weight zero, q weights 12, and 31-q weights 16. First-moment orthogonality gives L=31-q/4. Since 0<=q<=31 and L is an integer at most 27, the only possible q are 16,20,24,28. This deduction is self-contained and does not import an aggregate-model feasibility claim.

The raw second moment gives

    sum m_v^2 = (144q+256(31-q))/8 - L^2 = 992-14q-L^2.

The independently recomputed triples (q,L,sum m_v^2) are

    (16,27,39), (20,26,36), (24,25,31), (28,24,24).

Their repeated-pair counts are respectively 6,5,3,0. For q=16 or q=24, all 31 nonzero labels would have odd, hence positive, multiplicity. This needs L>=31, contradicting L=27 or 25. For q=20 or q=28, every multiplicity would be even, so m_v^2>=2m_v termwise. Thus sum m_v^2>=2L, contrary to 36<52 or 24<48. No case remains.

## Independent computation and controls

`review.py` is separately written and does not import the producer's checker or its result. It uses a different elimination implementation, reconstructs the words by successive span expansion, rediscovers the hyperplanes rather than only checking the supplied table, checks the full parity-equation rank, and derives the moments directly as rational first/second sums. It passes under both ordinary Python and `python -O` in about 0.2 CPU seconds, with explicit exceptions retaining all checks.

A separate genuine-code control enumerates all multisets of up to four affine binary functions in dimension three, treating each function by its linear and constant parts together. This is 4,845 configurations, 67,830 hyperplanes, and 4,550 actually constant hyperplanes. For every hyperplane, the test verifies both directions of the exact paired-Fourier criterion. For constant hyperplanes it verifies the parity-period implication. It includes zero and repeated linear columns and affine offsets.

A rank-deficient guard uses the real restriction with columns {1,2,3} in F2^3. Its parity function has only the two-dimensional period space {0,1,2,3} and is nonconstant. It is not incorrectly excluded by omitting the spanning hypothesis. A one-column F2^1 control verifies why substituting physical zero-column parity for the auxiliary f(0) fails.

The producer's genuine q20 restriction was independently rebuilt and checked: length 27 after appending a zero-on-S column, local distribution 1+20z^12+11z^16, full left-matrix rank nine, kernel span(h), and 123 failures of the full residual lift inequalities. Its parity periods are the 16 even labels, a rank-four subspace, and therefore do not meet the rank-five requirement of the residual windows. This is a useful true local code, not a target lift. Its zero appended column does not create a false positive claim.

The producer's checker was also replayed successfully. It reports 6,401 affine configurations, 89,614 hyperplanes, and 8,862 constant hyperplanes in its differently indexed exhaustive control. Different counts from this review reflect the different enumeration, not a mathematical discrepancy.

## Reproduction and exact scope

Run from this directory:

    timeout 60s python -I -B review.py > result.json
    timeout 60s python -I -O -B review.py > result_optimized.json

All fields other than CPU time agree between ordinary and optimized runs. Source URLs:

- https://github.com/jamesyi030707/open-math-research/blob/3229383ae26e6c445adf62f70545553fcc5d2055/history/2026-11-10/inputs/residual_candidate.json
- https://github.com/jamesyi030707/open-math-research/blob/3229383ae26e6c445adf62f70545553fcc5d2055/notes/codes-q24-obstruction.md
- https://github.com/jamesyi030707/open-math-research/blob/3229383ae26e6c445adf62f70545553fcc5d2055/notes/codes-quadratic-rigidity.md
- https://github.com/jamesyi030707/open-math-research/blob/3229383ae26e6c445adf62f70545553fcc5d2055/notes/codes-residual-lift.md
- https://github.com/jamesyi030707/open-math-research/blob/3229383ae26e6c445adf62f70545553fcc5d2055/notes/codes-subspace-obstruction.md

All work was read-only with respect to public services; no public files or repository state were changed. The exclusion is a mathematical argument plus exact finite input checks, not a complete search of target matrices. The other fixed-B branch and the global existence question remain unresolved.
