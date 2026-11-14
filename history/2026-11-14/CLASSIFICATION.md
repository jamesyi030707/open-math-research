# q=28 kernel-zero local classification and finite compatibility

Scope: only the fixed residual B and its normalized doubly-even lift, kernel-zero branch, q=28. This is not a classification of residual codes or a claim about the global [64,11,27] problem.

## Necessary local classification

The archived q=28 moment calculation gives24 nonzero S columns, all distinct, and three zero S columns. Of the31 nonzero S messages, exactly three have left weight16 and the rest weight12.

Start with all31 nonzero labels of the five-dimensional simplex, whose nonzero weights are16. Deleting the seven absent nonzero labels leaves weights12 or16, so the deleted seven-coordinate code has nonzero-message weights4 or0. Exactly three nonzero messages have weight0, together with0 forming a two-dimensional kernel. Its image therefore has dimension3, so the seven deleted labels span a three-dimensional space U. As they are distinct and nonzero, they equal U minus zero. Thus the present S labels are F2^5 minus U.

An equivalent character proof: let E be the three weight16 messages. For each nonzero column label v, exact character inversion gives m(v)=(3−sum_{s in E}(-1)^(s dot v))/4. Since m(v) is0 or1, every v is negative on an even number of E's three characters. Characters separate points, so the XOR of E is0. E together with0 is a two-dimensional space and U=E^perp.

Previous exact pair-budget and parity constraints leave(r,z)=(4,1) or(24,3), where r=wt(hA) and z counts zero-S columns selected by h. Self-orthogonality of the doubly-even W restriction says the XOR of h-selected nonzero S labels is0; the XOR of all24 labels is also0. Therefore:

- r=4: exactly three nonzero labels are h-selected, and their XOR is0. They are T minus zero for a two-dimensional subspace T disjoint from U.
- r=24: exactly three nonzero labels are h-unselected; the same argument makes them T minus zero with T intersect U={0}.

Column order does not affect feasibility. Zero-label h multiplicities are respectively(2,1) and(0,3). Every possible q=28 W restriction is thus included among these(U,T,r) cases, with original fixed message coordinates retained. No symmetry of B or unproved equivalence between U choices is used.

There are155 three-dimensional U and64 complements T per U, hence9920 pairs. The complement count follows by writing each complement as the graph of a linear map from a fixed two-dimensional quotient complement into U, yielding2^(2*3). Explicit subspace enumeration checks these counts.

## Small compatibility test

For each external coset a in(2,3,5,6), take the16 messages with residual weight14. Their S projections have coordinates o+sum x_i b_i, and their h bits form a quadratic bent graph g(x). The previous exact Fourier representation is

    4 c0 + K c1 = -4 delta0,
    K K^T = 16 I.

Here ce are signed multiplicities aggregated by lambda(v)=(v dot b_i)_i; the sign includes(-1)^(v dot o). For each label, |ce|<=Me and ce=Me mod2 are necessary and sufficient for individual signs realizing the aggregate. Repeated and zero columns count with multiplicity.

For r=4 there are only four h=1 columns: the three T labels and one zero. Enumerate all16 sign assignments; compute c0=−delta0−Kc1/4, and test integrality, bounds and parity for the other23 columns.

For r=24 there are only three h=0 columns: the T labels. Enumerate all8 sign assignments; compute c1=−K^T(c0+delta0)/4, and test the other24 columns.

Failure means no arbitrary outside row satisfies the section's16 weight14 equalities, so there is no full linear extension. Success is only success of this necessary single-section condition. Different sections are permitted unrelated outside signs in this relaxation; even success in all would not prove a full extension.

## Exhaustive result and verification

Both branches have the same first-failure counts: a=2:8960; a=3:880; a=5:76; a=6:4. No pair survives these four sections. The classification and exact finite verifier therefore close q=28 in the fixed-residual kernel-zero branch. q=16,20,24, other residuals and global existence remain unresolved. The known26–27 bound is unchanged.

`check_classification.py` reconstructs the four sections from the ten residual rows, checks512 single-column transform identities, enumerates155×64 pairs in both branches, and retains explicit checks under Python `-O`. It constructs an actual27-bit outside row satisfying all16 equations of one section and rejects a deliberately changed bit. This is a positive control for one section, not a full lift.

Normal and optimized replays take under one CPU second and agree after removing only `cpu_seconds`. Every run has a60-second timeout. A separate reviewer using full64-row character tables instead of the bent representation independently reproduced all19840 rejections and the first-failure counts. These are AI-assisted independent implementations, not external peer review or proof-assistant certification.
