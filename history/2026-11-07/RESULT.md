# A message subspace excludes the published q = 0 witness

## Result and scope

For the archived residual code B, in the projection-kernel-one branch, every actual lift must satisfy **q >= 16**. Here q is the number of residual message pairs of type (16,16) assigned left weight 12; the other 31-q pairs have left weight 16.

Consequently, the seven-count formal witness (28,0,100,32,4,62,0), published on 2026-11-05, has **no message labelling realizable by a length-27 matrix A** for this fixed residual and branch. The earlier statement that this point satisfies all 1075 aggregate constraints remains correct. This is a new restriction relative to that model, not a correction of its feasible-point arithmetic.

This does not exclude all other count points, the entire kernel-one branch, the kernel-zero branch, other residual codes, or binary [64,11,27] codes in general. No search or infeasibility solver was run.

## The message structure that the aggregate table omitted

Use the original ten message coordinates of the archived B basis. Its unique weight-32 message is h = 1008. In the kernel-one branch, hA = 0, so messages u and u+h have the same left word.

The 31 pairs whose residual weights are (16,16) have representatives

16, 32, 48, ..., 496.

Together with zero, these form the actual message subspace

S = span over F_2 of (16,32,64,128,256), of dimension 5.

Every nonzero s in S has wt(sB) = wt((s+h)B) = 16. The verification obtains this set from the original residual basis, checks every element and all 1024 XOR closures, and checks rank 5. Thus this is not an arbitrary assignment of weight labels to a generic set of 31 objects.

Equivalently, the entire preimage T = S + span(h) is the dimension-6 subspace consisting of all multiples of 16 between 0 and 1023. An independent check uses this full preimage rather than selecting quotient representatives.

## The short obstruction

The existing residual-lift conditions and double-evenness give a(s) = wt(sA) in {12,16} on S minus {0}. By the archived definition of q, exactly q of these 31 messages have weight 12. Hence

sum over s in S of wt(sA) = 12q + 16(31-q) = 496 - 4q.

On a dimension-5 message subspace, each matrix coordinate restricts either to the zero functional or to a nonzero linear functional. A nonzero functional is 1 on exactly 16 of the 32 messages. If N is the number of coordinates nonzero on S, double-counting gives

496 - 4q = 16N, with 0 <= N <= 27.

Therefore N = 31 - q/4, so q >= 16 and q is divisible by 4. The divisibility was already known in the aggregate model; the lower bound is the added restriction. Combined with its old upper bound q <= 31, the only possible q values are 16,20,24,28, with no existence assertion for any of them.

For q = 0 the identity demands 31 active coordinates in a length-27 matrix. This contradiction is independent of how the other message weights are assigned, and therefore excludes every labelling of the published seven-count witness.

The same contradiction appears in the 2026-11-06 character inversion criterion restricted to S: the prescribed weights (0,16,...,16) at length 27 give zero-column multiplicity -4 and multiplicity 1 for each of the 31 nonzero restricted columns.

## Controls

A genuine standalone [27,5,12] control achieves the new local boundary q=16. In five message bits let

f(s) = x0*x1 + x2*x3 + x4 over F_2.

Set a(0)=0 and a(s)=16-4f(s) for s nonzero. The following 27 binary column labels realize all 32 prescribed weights exactly:

1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,19,19,23,23,27,27,28,28,29,29,30,30.

Its weight enumerator is 1+16z^12+15z^16, and it has rank 5. This verifies that the bound is sharp for the restricted five-dimensional problem only. It is not an extension to the full fixed residual B and not a target-code construction.

For a second positive control, the 31 nonzero five-bit columns form the length-31 simplex code, which realizes q=0 with all nonzero weights 16. The same labelled weights fail at length 27 with the explicit multiplicity -4. The checker thus accepts the valid construction and rejects the genuinely too-short one.

## Evidence and what should happen next

`check_subspace.py` uses exact integer and rational arithmetic and finishes in about 0.002 CPU seconds. Its certificate, the original input basis, and actual run log are supplied. The separate audit uses the six-dimensional full preimage and direct codeword checks for the controls.

This is a classical first-moment/double-counting argument applied to an explicitly verified target-specific subspace, not an originality claim or an external peer-review claim. The useful change is that message incidence identifies a real subcode whose first moment was absent from the previous full-code aggregate transform.

The published witness should remain archived as a valid formal feasible point, with this later realizability obstruction linked alongside it. The remaining region q >= 16 has not been solved. A subsequent task should first decide what independently checkable evidence it would produce, rather than repeat the old 1075-constraint solve or enlarge a search without a new certificate goal.

## Pinned sources

- Residual input basis, checked against GitHub at commit `816784cce71a4acd3b10fc9b42392716f1cb7fe0`: https://github.com/jamesyi030707/open-math-research/blob/816784cce71a4acd3b10fc9b42392716f1cb7fe0/history/2026-10-24/independent/residual_candidate.json
- Exact definition of q: https://github.com/jamesyi030707/open-math-research/blob/816784cce71a4acd3b10fc9b42392716f1cb7fe0/history/2026-10-28/category_cut.py
- Published aggregate witness: https://github.com/jamesyi030707/open-math-research/blob/816784cce71a4acd3b10fc9b42392716f1cb7fe0/notes/codes-split-feasible-witness.md
- Previous message-level criterion and its limits: https://github.com/jamesyi030707/open-math-research/blob/816784cce71a4acd3b10fc9b42392716f1cb7fe0/history/2026-11-06/RESULT.md

The copied basis retains its archived source provenance. No new claim is made about the live global parameter table or unseen literature in this bounded check.
