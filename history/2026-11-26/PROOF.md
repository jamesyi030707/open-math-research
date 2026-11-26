# Where the binary restriction enters

## Input

Use a=3 and the two zero-based catalogue indices 115 and 139, each in its original orientation and with column-label bits 0 and 2 exchanged. The source is [the fixed catalogue](../2026-11-15/h.json), blob `6c2f005c33236b54ed1850f78b7700fcb44b7237`. Keep the 27 column positions distinct, including equal labels. Use the [same fourteen original equations](../2026-11-24/PROOF.md), omitting labels 25 and 60 from the full sixteen. The [explicit integer witnesses](../2026-11-25/PROOF.md) satisfy these fourteen equations but are not binary.

At position j of column label c_j, for row label t define A[t,j] = 1 − 2 parity(t AND c_j). Expanding the Hamming-weight equation gives A[t]·x = (1 + sum_j A[t,j])/2, with x in {0,1}^27. Each stored derived equation is a signed sum of all fourteen rows, including their right sides.

## Proof rule and replay

For an equation f·x=b, let P be assigned positions and F the still-free positions. Its possible value lies between sum over P of f_j x_j plus sum over F of min(0,f_j), and the same assigned sum plus sum over F of max(0,f_j). If b falls outside the interval, the partial assignment is impossible. If fixing the opposite of a proposed bit makes b fall outside, the bit is proved. Otherwise, a recorded split covers both values of an unset bit. Induction on the explicit tree rules out every binary assignment.

The generator sorts normalized signed sums by number of nonzero coefficients, then by sum of absolute coefficients minus the absolute sum of signs, then by sign mask. It tries the first sixteen alongside the originals, repeatedly propagates bounds, and branches on an unassigned bit favored by sparse, tight equations. The fixed certificate discards equations never cited. The independent Python checker does not run this search or use its ordering.

| Case | Orientations | Used signed sums per tree | Nodes | Conflicting leaves | Branch depth |
|---|---:|---:|---:|---:|---:|
| 115 | 2 | 14 | 35 | 18 | 6 |
| 139 | 2 | 16 | 79 | 40 | 6 |

Depth counts splits on a path, not forced assignments; nodes include the internal splits. Both orientations use the same combination vectors in each case but have separate proof trees. The checker also rejects each tree with its leftmost leaf reason changed to an out-of-range reference. Neither the number of signed sums nor the tree sizes are asserted minimal.

## One-equation control

For every combination with first sign +1 and remaining thirteen signs ±1, compute its exact attainable set. A negative coefficient c is handled by replacing x with 1−x, shifting the target by c and using the positive coefficient −c. The integer bitset starts at 1 and each coefficient w updates it to B OR (B shifted left by w). The resulting bitset contains the target for all 8,192 choices in every instance. Thus no single equality from this family suffices, even when tested against exact subset sums rather than only interval endpoints. This does not test arbitrary combination coefficients or arbitrary subsets of original equations.

This supplies a transparent proof for four existing exclusions. It does not explain the uniqueness of the two omitted labels, extend to other catalogue indices, or change the [known distance bounds](https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2).
