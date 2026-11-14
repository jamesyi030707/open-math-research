# A complete q=28 local classification, followed by four section tests

2026-11-14. For the pinned residual B, the normalized kernel-zero lift cannot have q=28. This does not exclude q=16,20,24, other residuals, or global binary [64,11,27] existence. The accessible Grassl table still lists26–27.

## Fixed inputs and inherited premises

B is the unchanged rank-ten length37 residual, identified by the [November12 input](../2026-11-12/inputs/residual_candidate.json), SHA-256 `276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80`. Both new programs reconstruct words directly from its ten rows. Prior double-even rigidity and the lift inequalities are reused:

    27-wt(uB) <= wt(uA) <= wt(uB),
    wt(uA) = -wt(uB) mod4.

Let S={s<<4}, h=1008 and W=S+<h>. All62 messages of W other than0,h have residual weight16. Thus their left weights are12 or16. q counts the weight12 messages among the31 nonzero messages of this fixed S. Kernel zero gives nonzero hA. [November12](../2026-11-12/RESULT.md) already proves that q28 has24 distinct nonzero S columns and3 zero columns, with (r,z)=(4,1) or(24,3). No hA=0 argument is imported.

## Why a finite list really covers the question

Delete the24 present nonzero labels from the five-dimensional simplex. The7 deleted distinct labels produce a code with message weights0 or4; exactly3 nonzero messages have weight0, so its kernel has dimension2 and its rank is3. Those7 labels are exactly U\{0} for a three-dimensional U. Thus the present labels are F2^5\U.

In the r4 case exactly3 present nonzero labels have h-bit1. In r24 exactly3 have h-bit0. Self-orthogonality gives zero XOR of these labels, so they are T\{0} for a two-dimensional T. Since they are all outside U, T∩U={0}. The zero S-label multiplicities are already fixed by z. Conversely these choices satisfy the W windows, although necessity alone suffices to cover every possible lift.

There are155 U and64 complementary T for each U, hence9920 labeled pairs in each of two branches. Zero columns and coordinate permutations cause no extra feasibility cases. This is enumeration in the fixed coordinates of B, **not** reduction using an unproved automorphism of B. A full proof and the complement count are in [CLASSIFICATION.md](CLASSIFICATION.md).

## Exact obstruction tests

For each a in(2,3,5,6), obtain the16 W coordinates t with wt((a+W(t))B)=14. The left character sum must be−1 at each of them. The actual sets are quadratic graphs over affine four-dimensional hyperplanes, not affine flats in W.

The first implementation rederives their small Walsh matrices and uses

    4c0 + Kc1 = -4 delta0,   KK^T=16I.

For each signed column multiplicity c with ordinary multiplicity M, exact attainability is |c|≤M and c≡M mod2. r4 has only4 h-bit1 columns, so at most16 sign assignments; r24 has only3 h-bit0 columns, so at most8. The other signed multiplicities are then uniquely determined and checked. No unknown full matrix is searched.

The independently written program does not read the geometry or the first result. It forms the original16×64 character table directly from B, groups the large-side characters up to sign into16 orthogonal classes, and recovers each signed count by integer inner products divided by16. The same small-side choices are exhaustive. This supplies a different representation of the same necessary equations.

In each branch, the first failed section counts are:

| a | rejected labeled pairs |
|---|---:|
| 2 | 8960 |
| 3 | 880 |
| 5 | 76 |
| 6 | 4 |
| total | 9920 |

Every candidate has a section with no possible signs, even when its outside row is allowed to be arbitrary. Hence no full linear extension exists in this q28 case. A successful section would not establish a full extension, because other sections and their common linear dependence remain necessary.

## Controls and reproducibility

The first program checks512 one-column transform identities and supplies an explicit27-column,27-bit outside-row control satisfying all16 equations of one section. Flipping one bit breaks the equalities. It is a genuine local positive control, **not** a complete target lift. The independent implementation adds100 actual signed-multiset controls including repeated and zero labels. Neither test is an always-reject predicate.

Both self-contained standard-library programs passed normal and optimized Python replays, four runs in total, each below2 CPU seconds and limited to60 wall-clock seconds. Their first-failure tables agree; normal/optimized outputs agree after removing only timing. There is no numerical solver status, floating-point pruning, random failure inference, external peer review or proof-assistant certification.

## Research commentary and stopping point

The new step is coverage: yesterday excluded two displayed restrictions; the classification now proves that all possible q28 restrictions appear in a short exact list. The four residual sections then eliminate the list. The count alone would mean little without the necessity proof, just as a failure of two displayed matrices said nothing about the other labels.

Stop q28 here. The next small target is the q24 kernel-zero restriction: derive its repeated-column/h-bit possibilities without borrowing this distinct-column classification, then decide whether the same exact section test can yield a bounded, checkable new certificate. Keep each deterministic check within60 seconds. If there is no finite classified input or nonredundant consequence, do not enlarge a full-matrix search. q16,q20,q24 remain unresolved in this record.
