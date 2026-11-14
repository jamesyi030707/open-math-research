# Actual visible final answer

2026-11-14. Transcribed from the final reply, with mathematical typography and list layout normalized. This is not reasoning-panel content.

Both statements hold, with converses, for the W-level weight conditions. I ran nothing here. The count of 64 per case is confirmed by a subspace count (155 − 91 = 64).

## Setup

The active columns are v ∈ F₂⁵∖U, each once. For s ≠ 0, w(s) = 16 − 4[s ∉ U^⊥], so w(s) = 16 on the 3 nonzero s ∈ U^⊥ and 12 on the other 28. Let E be the set of active columns carrying the h-bit, let z ∈ {0..3} be the number of zero columns carrying it, and put r = z + |E| = w(h). Then, with e_s = #{v ∈ E : s·v = 1}, w(s+h) = r + w(s) − 2e_s. The windows require w(s+h) ∈ {12,16} for all s ≠ 0. I take r ∈ {4,24} from your earlier proven moment coupling. I did not re-derive that.

## r = 4

- For s ∈ U^⊥∖0, 20 − 2e_s ∈ {12,16} gives e_s = 2 (4 is impossible because |E| ≤ 3).
- For the other s, e_s ∈ {0,2}.
- So every e_s is even, which means XOR(E) = 0.
- |E| = 4 is impossible: four distinct nonzero vectors summing to 0 have any three independent, so some s has e_s = 4.
- |E| ≤ 2 is impossible, since distinct nonzero vectors cannot sum to 0 and E would not give e_s = 2 on U^⊥∖0.
- Hence |E| = 3, z = 1 (derived here, not assumed), and E = {a, b, a+b} is a line P∖0.
- Then e_s = 2 exactly when s is not orthogonal to P, and e_s = 0 otherwise.
- The condition e_s = 2 on U^⊥∖0 means U^⊥ ∩ P^⊥ = 0, equivalently U + P = F₂⁵, i.e. P ∩ U = {0}.
- So the three marked labels form a line whose span is disjoint from U and meets all three nonzero cosets of U.
- Converse: for such P, every w(s+h) is 16 or 12 (equal to 16 on U^⊥∖0), and w(h) = 4.

## r = 24

Let G be the unmarked active columns, so |G| = z. With g_s = w(s) − e_s, the conditions become g_s ∈ {0,2}, with g_s = 2 on U^⊥∖0. The same argument gives z = 3 and G = P∖0 with P ∩ U = 0. The converse also holds.

## Count for fixed U = {0,…,7}

The number of 2-dimensional P with P ∩ U = 0 is 155 − 7 − 7·12 = 64. That gives 64 controls for r = 4 and 64 for r = 24, 128 in total. The identical zero columns add no extra choice.

## Transport criterion

Column permutations of A are free. A message-coordinate change g ∈ GL(10,2) preserves the fixed B only if wt(g(u)B) = wt(uB) for all u. Since B has 37 distinct nonzero columns, such g come from automorphisms of the code B (MacWilliams extension). To transport an obstruction between W-controls, g must also stabilize W. Arbitrary GL(5,2) changes of S are not allowed: they would alter weights outside W.

## Gaps

- The slice U = {0,…,7} is 1 of 155 choices of U. Unless Aut(B)∩Stab(W) acts transitively on them, which I have not shown, 154 other U’s remain.
- Equivalence of controls under Aut(B)∩Stab(W) is not computed.
- Nothing is proved about the 15 outside cosets of W. That is where any obstruction would have to come from.
- No q = 28 exclusion is claimed.
