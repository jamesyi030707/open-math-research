# Actual external sections isolate one column on six noncanonical q24 controls

## Fixed premises

Fix the [37,10,14] residual B, the doubly-even normalization and kernel-zero case of the putative [64,11,27] lift. Use the same 6-dimensional W marking as on [November 20](../2026-11-20/PROOF.md), with `W(t) = ((t & 31) << 4) ^ (1008 if t & 32 else 0)`. Start from the November 15 marking at zero-based index 1. In its 27 column labels exchange one pair among bits 0,…,4, leaving bit 5 unchanged. This constructs test restrictions, not symmetries of B. Each set of actual local weights is checked from its new column labels and the unchanged B embedding.

For an external representative $a$, write $H_a=\{t:\operatorname{wt}((a+W(t))B)=14\}$, where message addition is XOR. For $t\in H_a$, the raw A-side weight window is 13–14. Divisibility of the full even-subcode word by four forces the A-side weight to be 14. Thus the hypothetical offset signs $\epsilon_j\in\{-1,1\}$ satisfy
$$
\sum_j \chi_t(c_j)\epsilon_j=-1\qquad$t\in H_a$,
\quad \chi_t$v$=(-1)^{\langle t,v\rangle}.
$$
For $F_a$v$=\sum_{t\in H_a}\chi_t$v$$, multiplication of these equations by $\chi_t$u$$ and summation gives
$$
\sum_j F_a(u+c_j)\epsilon_j=-F_a$u$.
$$
In particular, if a pair of projected equations, combined with sign $s\in\{-1,1\}$, has left coefficients $16e_j$ and right-hand side zero, it implies $16\epsilon_j=0$. No signed-sum search is then required to check the contradiction.

## Six one-column certificates

For the actual section $a=2$, $H_2=(0,1,6,8,9,15,18,19,20,28,39,46,53,58,59,61)$. The following table uses zero-based bit and column positions. The equation for $u$ is combined with $s$ times that for $v$; all other column coefficients and the combined target are zero.

| Low-bit swap | $u$ | $v$ | $s$ | Isolated $j$ | Coefficient |
|---|---:|---:|---:|---:|---:|
| 0,2 | 1 | 6 | −1 | 14 | 16 |
| 0,3 | 2 | 10 | +1 | 12 | 16 |
| 0,4 | 2 | 5 | +1 | 11 | 16 |
| 1,2 | 4 | 5 | +1 | 12 | 16 |
| 1,3 | 2 | 5 | +1 | 15 | 16 |
| 1,4 | 1 | 6 | −1 | 14 | 16 |

Example: for (0,2), dividing the individual equations by 4 on positions (0,14,16,24,26) gives coefficient rows (1,4,−1,1,1) and (1,0,−1,1,1), both with target zero. Their difference forces $4\epsilon_{14}=0$. Independently, all 64 individual character targets are attainable for each of the six controls (384 individual tests). A single character does not require consistency with the signs for any other character.

## Separation from prior certificates and scope

The batch includes ten distinct column multisets from all low-bit swaps, including one whose multiset coincides with the original seed and three other already covered multisets. On each, some actual minimum section rejects the fixed pair (0,1), even though both scalar coordinates separately pass in every tested minimum section. The six rows above give a simpler obstruction at the same external representative $a=2$, with the character pair allowed to vary.

For each of the six: all 63 nonzero W windows and doubly-even congruences hold, $(q,r,z)=(24,4,1)$, and $a(0)+\max b=2$. Thus the earlier multiplicity bound does not reject it. The full old set of 8,408 explicit translated multisets is regenerated from the 277 canonical restrictions and checked for nonmembership. Independently, their q24 E labels cannot become the canonical E under any true B translation. The six are distinct true translation orbits; each has exactly one q24 multiset and seven q20 multisets. The table reports six added q24 exclusions relative to the named November 16–18 coverage, not an exhaustive count across all previous results, and does not add translated q20 images to the headline count.

This is about a fixed residual and six concrete local controls; it does not rule out the q24 branch, every such local coordinate relabeling, other residuals, or a [64,11,27] code. No large candidate scan was performed.
