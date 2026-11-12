# 2026-11-12: actual Claude exchange

One completed round. The following is a transcription of the visible final answer, not hidden reasoning. Paragraph and list formatting are normalized; mathematical wording is preserved.

## Prompt

Continue on Nov 12, without repeating closed branches. The public archive now independently excludes the entire fixed-residual kernel-one branch using common parity periods from five constant hyperplanes; that later proof was not reviewed by you. Grassl's primary [64,11] entry read today still displays 26–27 (search marked crawled yesterday), not a novelty claim. Today's target is a genuinely new necessary condition for kernel zero, not a large search. Work without tools, <=550 words.

Normalize the putative code by c=(1^27,0^37) and its even subcode [A|B], where B is the fixed rank-10 even length-37 residual. For all nonzero messages u: 27-wt(uB)<=wt(uA)<=wt(uB). The rank-55 evaluation certificate at B's 160 weight-14 messages forces the even subcode doubly even, hence wt(uA)=-wt(uB) mod4. In kernel zero, A has rank10 and hA is nonzero. The unique residual message of weight>=27 is h=1008, wt(hB)=32. Let S=span(16,32,64,128,256). Every u in U=span(S,h) except 0,h has residual weight16; dim U=6. Thus the genuine left restriction A|U is a rank-6 binary length-27 code: 62 messages have weights12 or16, and h has weight 4j in {4,8,12,16,20,24}. No hA=0 pairing/window intersection is permissible.

Can these facts alone exclude any j, or force a checkable structure strictly stronger than the first two moments? Start by checking the premises and exact first/second/third character or MacWilliams constraints for this restriction; distinguish formal distributions from realizability. If using an external classification, label it unverified rather than cite from memory. Give one small deterministic certificate target with a real-code positive control and <=60-second verification budget; stop if only redundant consequences. No global exclusion claim.

## Final reply

Premises (checked).

• For u ∈ U∖{0,h}, t = 16, so 11 ≤ s ≤ 16. With s ≡ −t ≡ 0 (mod 4), s ∈ {12, 16}.
• For h, t = 32 gives s ≡ 0 (mod 4) and s ≤ 27. Kernel zero gives s ≠ 0, so s = 4j with j = 1..6.
• A|U is injective, and all weights are ≡ 0 (mod 4), so C_U is a doubly-even [27,6] code.
• I take the exact enumeration of U (62 messages of t = 16) as given. Nothing else of B enters at U-level.

First moment. Let N_U be the number of columns nonzero on U, and x the number of weight-12 messages among the 62. Each active column is 1 on 32 messages, so 12x + 16(62−x) + 4j = 32N_U. Hence x = 248 + j − 8N_U, which forces N_U ∈ {24,…,27}.

Second moment. For m_v the multiplicity of column v ∈ U*∖0, with Σm_v = N_U, we get Σm_v² = 16⁻¹Σ_u wt² − N_U², since pairs of equal columns contribute 32 and distinct pairs 16. This gives
Σm_v² − N_U = (j − (3−z))(j − (4+z)), where z = 27 − N_U is the number of columns zero on U.
Since Σm_v² − N_U = 2ΣC(m_v,2) ≥ 0:
• z = 3 is impossible.
• z = 2 forces j ∈ {1,6}.
• z = 1 forces j ∈ {1,2,5,6}.
• z = 0 allows every j. For j = 3 or 4 it forces all m_v ≤ 1 (27 distinct nonzero columns).
So the moments give no outright exclusion of any j.

Message-level structure (stronger than moments).
• For any hyperplane H of U, integrality of m_v = N_U − (Σ_H wt)/16 requires Σ_{u∈H} wt(uA) ≡ 0 (mod 16). If h ∉ H, the number of weight-12 messages is ≡ 0 (mod 4). If h ∈ H, it is ≡ j (mod 4) among the 30 other messages.
• Because the code is doubly even, ι(u) = wt(uA)/4 mod 2 has degree ≤ 3 in the six message bits. This follows from inclusion–exclusion, with the |S| = 4 term −8|r_S|/4 even. That is a parity condition on every 4-flat.
• Both are the d = 4 subspace identities, i.e. consequences of the labeled Fourier model. They depend on which messages carry weight 12, which the histogram does not record. So they go beyond the moments but are not independent of full realizability.

S-level coupling (kernel zero). The earlier S-restriction analysis used no hA = 0 pairing, so it applies to each of the 32 complements S″ of ⟨h⟩ in U. For ε with kernel S″, q_{S″} = 124 − 4N_U + 4m_ε. For N_U = 27 and j ∈ {3,4}, all m_ε ≤ 1, so every complement has q ∈ {16, 20}.

Certificate target. A multiplicity function m: F₂⁶ → ℤ≥0 with 27 columns whose induced weights satisfy the windows (12 or 16 on 62 messages, 4j at h). Positive control by hand: extended Hamming [8,4,4], with h = 1111 giving weight 8 and the other 14 messages weight 4. Negative control: change one multiplicity, and a window breaks. A certificate is either an explicit m or an exhaustive proof, pruned by the (N_U, j) table and the S″-types.

Stop rule. If only consequences redundant with the table and the Fourier model remain, stop. I computed no third moment, and I claim no exclusion of any j or of the branch.

## Editorial scope note

The Hamming-code control does not specify a generator or message basis, so its particular label h=1111 is not a basis-independent assertion. The proposed single-multiplicity negative control was not supplied as an explicit test. The claims of hyperplane integrality and cubic divided-weight parity are necessary labeled-code conditions, not an exclusion of the current target. No third-moment computation or complete local classification is furnished by this reply. Subsequent independent results must be identified separately.


## Attribution and notation boundary

The independent opposite-h-bit pair identity, finite parameter filter, XOR refinement and two explicit rank-six local controls in RESULT.md were not submitted to Claude. They are not attributed to this reply. Claude uses z for the number of columns zero on U; RESULT.md uses z=m[0,1], a different quantity. Neither uses hA=0. The search-freshness wording in the exact prompt records the earlier retrieval available when sent; the later independent source read was marked crawled today, without implying a source revision.
