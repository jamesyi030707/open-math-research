# A certificate gate before solving

2026-11-05. One complete mathematical answer was received in the existing Claude conversation. The free quota then ran out, so no further message was sent. The feasible tuple and the independent checks recorded elsewhere were obtained separately and were **not reviewed by Claude**. Account details, private conversation identifiers and interface material are omitted.

## Question: mathematical excerpt

> We now have seven unrestricted integers u and exactly 1075 affine inequalities c_i+A_i u>=0 (1064 split cells,11 original bounds), independently verified.

The question proposed exact integer witnesses, rational Farkas certificates and complete binary integer-split trees, and asked what controls, corruption tests and stopping semantics a checker needs. This paragraph summarizes the remainder of the question; it is not a quotation.

## Claude: complete final mathematical answer

Gate soundness.

(1) Feasible witness.

An integer u is accepted iff all 1075 inequalities c_i + A_i u ≥ 0 hold exactly, with Python integers or Fractions and no floats. Then map back through the inverse: (p,q,y10,y14,z8,z12,z16) must be integers satisfying the six congruences and the original 11 bounds. Conclusion: the formal split enumerator is feasible. It is not a code.

(2) Real infeasibility.

λ ∈ ℚ^1075, λ ≥ 0, with λᵀA = 0 and λᵀc < 0. Each inequality gives c_i + A_i u ≥ 0, so summing with weights λ gives λᵀc ≥ 0 for any feasible u. That contradicts λᵀc < 0, so no real feasible point exists, hence no integer point either. A checker verifies the three conditions exactly.

(3) Branch-and-bound tree.

Each leaf is a box defined by branch constraints u_j ≤ k or u_j ≥ k+1, together with a Farkas witness for the 1075 inequalities plus those branch inequalities. Every integer u satisfies exactly one branch at each split, so the leaves partition ℤ⁷. A complete tree with a valid certificate at every leaf proves integer infeasibility. A checker must also verify that the tree is complete, with no gaps or overlaps.

Controls.

One feasible toy system. One real-infeasible toy (a witness λ). One integer-infeasible but LP-feasible toy, e.g. 2u = 1. Corruption tests: flip a sign in λ, perturb one c, delete one leaf, and use overlapping splits. Each must be rejected.

Timeout or missing leaf.

A timeout is unresolved. A missing or invalid leaf means no integer exclusion. Nothing here concerns existence of a binary code.

## Editorial precision

The map from the new parameters to the old counts is the forward map in the November 4 notebook; Claude calls it the inverse when describing a return to the original variables. This is only a direction-of-naming issue. A branch leaf's region is its branch box intersected with the original polyhedron, not necessarily itself a box. A chosen mutation should invalidate a certificate; an arbitrary change to a constant need not do so. These are clarifications, not quotations or extra claims by Claude. The checker implementation and tested certificate types are documented separately.
