# Two simultaneous character sums: a short external obstruction

## Scope and exact premises
Fix the residual B, kernel-zero normalized doubly-even lift and W embedding recorded in the code. The 27-column local restriction is canonical q24 marking index 1 from November 15, with r=4,z=1. It is a genuine rank-six local restriction, not a target code. It already failed the November 16 external test; today's result compresses that failure, not a new nonexistence theorem.

Take external representative a=2 and H={t:wt((2+W(t))B)=14}. Its 16 labels are in result.json. The raw lift window is 13<=wt(x+y(t))<=14. The previously proved doubly-even normalization requires wt(x+y(t))+14 divisible by 4, so the weight equals 14. Put epsilon_j=(-1)^x_j and M_tj=(-1)^(t dot c_j). Then M epsilon=-1, since 27-2*14=-1. The congruence premise is essential: distance alone permits 13 as well.

For any two integer row multipliers lambda,mu, define the joint reachable set R of sums over j of epsilon_j*((lambda M)_j,(mu M)_j). The target is (-sum lambda,-sum mu). Every full extension places this target in R. Thus missing membership is a valid certificate at ANY labeling when its actual B section and coefficients are recomputed. No local GL symmetry of B is presumed, and passing a pair is not a sufficiency theorem.

## Concrete two-line certificate
Use lambda_t=1 and mu_t=(-1)^(t dot 1), then divide both integer equations by 4. With zero-based positions and every e_j in {-1,1}, the resulting equations are

-e0 + e16 + e24 + e26 + 4(e13+e25) = -4,
 e0 - e16 + e24 + e26 + 4e14 = 0.

The second equation forces its four unit terms to attain absolute sum four. Therefore e0=-e16=e24=e26=-e14. Their substitution cancels the four unit terms of the first equation, leaving e13+e25=-1, impossible for two signs. This is a hand-checkable contradiction using only seven column positions.

A separate exact enumeration of those seven signs gives 47 distinct reachable pairs. In the horizontal target slice y=0, x belongs to {-8,0,8}, excluding (-4,0). Each coordinate target separately is attainable.

## What the finite tests establish
At a=2 all 277 earlier canonical systems are consistent over unrestricted real variables: 269 have rank 16, eight rank 15. This is NOT a box-constrained linear-program feasibility claim. All 277*64=17,728 specified character-direction scalar signed-sum tests pass. Nevertheless the single pair (0,1) rejects 17 indexed restrictions, listed in result.json. All were already excluded in the earlier complete canonical proof.

The earlier count 259 is the cumulative failure count over ten tested external sections; a=2 alone first rejected 169. These must not be conflated. The single-control joint certificate is the main independently audited result; the 277-wide rank/scalar statistics are explicitly finite reproducible computations.

## Portability and limits
A real residual automorphism transports the full proof by precomposition. Arbitrary local relabeling does not: recompute its two coefficient rows and target first. Column permutations or independently negating a column coefficient pair preserve the joint reachable set, because epsilon_j is free to change sign. This gives a short coefficient signature to compare at other labelings, not an automatic claim that all 69,440 E are covered.

No all-pairs sufficiency, entire q24 exclusion, new distance bound or new-code construction follows. After finding this small certificate, no million-pattern search was launched.
