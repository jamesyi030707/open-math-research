# Message-labelled weights: exact column criterion and a nonredundancy control

## Result and scope

For an explicitly assigned weight function a:F_2^k -> {0,...,n}, a(0)=0, define

m(v) = 2^(-k) sum_u (n-2a(u)) (-1)^(u dot v).

There exists a binary k by n matrix A such that wt(uA)=a(u) for every message u if and only if every m(v) is a nonnegative integer. Rank k is not asserted unless a(u)>0 for every nonzero u. This is the elementary character-inversion characterization of column multiplicities; no originality claim is made.

Proof: if column v occurs m(v) times, n-2wt(uA)=sum_v m(v)(-1)^(u dot v). Character orthogonality gives the formula. Conversely, form a matrix containing m(v) copies of v. Orthogonality reconstructs n-2a(u); the sum of multiplicities is n because a(0)=0. This proves the claimed equivalence, including zero columns and rank-deficient cases.

Thus positivity/integrality of the transform is a finite list of linear inequalities/congruences on message-labelled weights. It is not merely the ordinary or split MacWilliams transform, which has already forgotten message labels.

## Explicit real-code control and a false labelling

Take k=4, n_left=8, n_right=15. Binary column labels use the least significant bit for the first message coordinate.

Left columns: (1,1,2,2,4,4,8,8).
Right columns: (1,2,...,15), the binary simplex generator columns.

The left weights in message order 0 through 15 are:
(0,2,2,4,2,4,4,6,2,4,4,6,4,6,6,8).
Every nonzero right word has weight 8. The joint distribution is exactly
(0,0):1, (2,8):4, (4,8):6, (6,8):4, (8,8):1.

Now interchange the assigned left weights at messages 1 and 7, leaving the right code fixed. The joint distribution is unchanged. Every labelled left weight is also unchanged modulo 4, so the quadratic function a(u)/2 mod 2 is unchanged. Nevertheless the character-inversion multiplicities are
(0,2,1,1,1,1,0,0,2,0,-1,1,-1,1,0,0).
The negative entries at v=10 and v=12 exclude this labelled assignment. All entries are integers: there is no fractional coefficient in this control.

The common split MacWilliams transform has 144 entries, all nonnegative integral. An independent enumeration of all 2^19=524288 words in the actual control code's dual agrees in every cell. Therefore even complete nonnegative split transforms, together with an unchanged message-level weight-modulo-4 quadratic function, do not certify a prescribed weight labelling.

A second exhaustive control checks all 64 possible functions a on F_2^2 with a(0)=0 and 0<=a<=3 against all 64 ordered lists of three columns. Both methods give exactly 20 distinct realizable weight functions and no mismatches.

Total deterministic standard-library CPU time reported: approximately 0.40 seconds. No target-code search or solver was used.

## Application boundary for the published [64,11,27] branch

In the fixed kernel-one branch, k=10 and n=27. No target-specific labelled assignment is constructed here.

The published seven-count witness specifies how many message pairs get each possible left weight. It DOES NOT specify which messages get those weights. The present criterion applies only after this assignment is supplied, or to a new model retaining those assignments. It does not reject the seven-count witness, its entire set of labellings, the fixed residual candidate, or all [64,11,27] codes. A failed arbitrary labelling would not establish any of those claims.

The real-code control proves strict information loss from message labelling to split histograms in general, not strict strengthening within every fibre of the specific target model. A justified next bounded task would formulate the compatibility constraints on actual messages and check new target-specific consequences. Do not describe that formulation alone as a target-code breakthrough.

## Source record

Read latest repository README and notes/codes-split-feasible-witness.md (2026-11-05), plus notes/codes-residual-lift.md and notes/codes-quadratic-rigidity.md, from https://github.com/jamesyi030707/open-math-research . The latest next-step proposal asks for a message-level condition with a genuine small-code control, not another solve of the feasible aggregate model.

This derivation and code were independently generated in a bounded investigation. The actual Claude exchange is retained separately in [DIALOGUE.md](DIALOGUE.md); its numerical example errors are corrected there and in [LIMITATIONS.md](LIMITATIONS.md). No target-specific residual-incidence bridge is claimed.
