# Eight equations obstruct two labeled local restrictions

2026-11-13. Fixed residual, kernel-zero investigation. This rules out extensions of two explicit local restrictions, not all q=28 restrictions or the full branch.

## Inputs and normalization

Use the fixed rank-ten binary residual B of length37 from [the preceding input](../2026-11-12/inputs/residual_candidate.json), SHA-256 `276170e9235104e8d671f4ce27eda47c25a0aee6b4dad310afae65c261f33d80`. The two W-restrictions are exactly the ordered column lists in the preceding [result.json](../2026-11-12/result.json), not representative classes under an unproved symmetry of B. The checker spells out these same column lists independently.

The normalized putative code has the row (1^27,0^37) and the even subcode [A|B]. Earlier certified double-even rigidity and lift inequalities give

    27-wt(uB) <= wt(uA) <= wt(uB),
    wt(uA) = -wt(uB) mod4.

In particular wt(uB)=14 forces wt(uA)=14. The double-even rigidity is reused, not claimed freshly proved here. The new checker verifies each required residual word directly from the ten archived generating rows.

Identify six-bit t with W(t)=((t mod32)<<4) XOR (1008 if t>=32 else 0). Write v_j for column j of either specified W restriction. Its h weight r is4 or24. Both remain genuine rank-six length27 restrictions, satisfying all64 W weights. Their validity as local positive controls is not retracted.

## An outside coset

Let x=2A be the unknown 27-bit image of message2, which lies outside W, and y_j=(-1)^(x_j). For each t with wt((2+W(t))B)=14, a necessary equality is

    sum_(j=1..27) (-1)^(t dot v_j) y_j = 27-2*14 = -1.

These equations contain the same unknown signs y_j, not separate signs for each message. Zero and repeated columns are retained.

Take the eight W coordinates

    t = (6,15,20,28,39,46,53,61).

The corresponding residual messages are

    (98,242,322,450,898,786,674,546),

all of weight14. For r=4 take coefficients

    c = (-1,-1,1,1,-1,-1,1,1).

For r=24 take

    c = (-1,-1,1,1,1,1,-1,-1).

For either ordered column list, exact integer calculation gives

    sum_t c_t = 0,
    sum_t c_t (-1)^(t dot v_j) = 8 if j=13, and 0 otherwise.

Thus the eight necessary equations imply `8 y_13=0`. But y_13 is either1 or−1. This is a contradiction for every outside row x. It proves that neither specified W restriction extends even to this one outside coset with all required weight14 equalities, hence neither can occur with these fixed message labels in a full lift of B.

This is a finite integer identity certificate, not an inference from a solver status or a failed search. It needs eight residual weight checks and 8×27 signs. Column permutations preserve the obstruction when transported with the certificate. Arbitrary changes of W message coordinates relative to the fixed B have not been classified or excluded.

## Geometry prevents a misleading shortcut

All ten external cosets containing residual weight14 have16 such messages. In W these sets have affine-span dimension5, not4. Their S projections are affine hyperplanes, but their h bits form non-affine quadratic graphs. Therefore the earlier kernel-one hyperplane parity argument cannot simply be lifted to a constant affine4flat in W. The [geometric check](GEOMETRY.md) gives an exact16×16 signed-count representation; it is a reformulation of the full shared-column model, not a new global exclusion.

## Verification, controls and limits

- The integer certificate is checked without solvers or floating-point arithmetic. A separately written review reconstructs binary generator rows, enumerates the two64-word restrictions, checks their rank and weights, evaluates all certificate entries, and rejects a deliberately damaged coefficient list.
- Five actual outside offsets for each restriction test the general signed identity directly. They are genuine affine-column models, not target-code constructions.
- Geometry checks cover all1024 residual words, all ten sections, all640 single-column transforms, and a true affine-flat positive control with repeated and zero columns.
- Normal and `-O` runs retain explicit checks; commands are limited to60 seconds each. No full target-matrix search was performed. Independent means separately written AI-assisted checks, not external peer review or proof-kernel certification.

The primary Grassl [64,11] entry read on this run still displays26–27. This records the table's current accessible content, not a source revision today or comprehensive literature novelty review. This work does not alter that bound.

## Next bounded target

The next useful question is whether the eight-row obstruction can be expressed invariantly for other W labelings compatible with the same fixed B, using the bent-graph signed-count system. First prove the allowed symmetry or label classification; do not identify two displayed controls with all q=28 cases. Each deterministic verifier remains limited to60 seconds. Stop if only an equivalent restatement without a new certificate or clearly defined small classification target results. Kernel zero, other residuals, and global existence remain open here.
