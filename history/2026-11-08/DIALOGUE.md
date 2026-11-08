# 真实数学交流与编辑澄清

本日记录一轮实际数学提问与完整可见回复。提问保留数学部分，省略开场衔接、停止搜索和输出形式要求；回复原文完整保留。没有补写后续交流。更强的列关联限制来自后续独立推导，未提交给Claude。

## 实际数学提问节选

Exact bounded checks now found formal feasible seven-count tuples for every survivor q: q16=(22,16,86,28,16,46,18); q20=(24,20,80,32,18,44,18); q24=(28,24,76,32,18,44,18); q28=(32,28,72,32,18,44,18). Each passes all original 1075 conditions by integer arithmetic; none is a code. For S≈F2^5, the restricted code has nonzero weights 12 (q times) or16 (31−q times), effective length N=31−q/4. Please scrutinize the second moment: if m_v counts nonzero columns after deleting zero columns, sum_v binom(m_v,2)=[992−14q−N²−N]/2, hence values 6,5,3,0 for q16,20,24,28. For q28, does the resulting projective [24,5] two-weight code necessarily equal a simplex [31,5,16] code with the seven nonzero vectors of a 3-dimensional column subspace removed? Prove or disprove the precise classification, and give a target-relevant extension consequence without claiming a full code exclusion.

## Claude reply

Second moment.
Let S ≅ T/⟨h⟩ ≅ F₂⁵ with 31 nonzero messages, and let N = 31 − q/4 be the number of columns of A that are nonzero on S. These columns have multiplicities m_v at nonzero v ∈ S*. For distinct nonzero v, v′, exactly 8 messages u have u·v = u·v′ = 1. For a single v the count is 16. So Σ_u wt(u)² = 8Σm_v² + 8N². The weights give Σ_u wt(u)² = 144q + 256(31−q) = 7936 − 112q. Hence Σm_v² = 992 − 14q − N², and Σ C(m_v,2) = (992 − 14q − N² − N)/2. This is 6, 5, 3, 0 for q = 16, 20, 24, 28, with N = 27, 26, 25, 24. Your formula is confirmed.

Classification for q = 28 (proved).
Because Σ C(m_v,2) = 0, the 24 columns are distinct nonzero points of PG(4,2), with complement R of size 7.
- Every nonzero u has weight 16 − r_u, where r_u = |R ∩ {v : u·v = 1}|.
- The window {12,16} forces r_u ∈ {0,4}.
- Exactly 3 nonzero u have r_u = 0. These u are exactly W^⊥∖{0} for W = span R, so 2^{5−dim W} − 1 = 3 and dim W = 3.
- A 3-dimensional W has only 7 nonzero vectors, and |R| = 7, so R = W∖{0}.

So the restricted code is the simplex [31,5,16] code with the seven nonzero column vectors of a 3-dimensional subspace removed. The converse also holds, since each such configuration gives weights 12 (28 times) and 16 (3 times). All 3-dimensional W are equivalent under GL(5,2). The statement is that the column set is the complement of a Fano plane; I made no claim about q = 16, 20, 24.

Extension consequence (q = 28).
- Exactly 3 columns of A annihilate T (they lie in S^⊥ ⊂ V*).
- For u ∉ S, the weights on the coset u+S are a(u+s) = κ(u) + (24 − Σ_c σ_c(u)(−1)^{s·v_c})/2, with σ_c(u) = (−1)^{u·c} and κ(u) ∈ {0,…,3}.
- Parseval over s ∈ S gives, for each of the 15 nonzero cosets: Σ_s (a(u+s) − 12 − κ) = 0 and Σ_s (a(u+s) − 12 − κ)² = 192.

Each a(u+s) must also lie in its window 27 − t ≤ a ≤ t with a ≡ t (mod 4). Checking this per coset needs the actual messages of B and was not run. No full branch or code exclusion is claimed.

## Editorial clarification (not Claude's words)

The 15 nonzero cosets are in Q=F₂¹⁰/⟨h⟩ (dimension9), modulo S=T/⟨h⟩ (dimension5). Equivalently choose a five-dimensional complement to h in T. Annihilating that complement and h is equivalent to annihilating T. This resolves the reply's compressed S/T notation. Full lift windows must hold for both original messages in every h-pair, not just one arbitrarily chosen residual weight. The classification concerns only this five-dimensional restriction. It does not identify its placement relative to B or construct a full A. The proposed formula originated in the outgoing prompt; Claude supplied a proof and the Parseval consequence. Separate exact computation verified these claims. The later column-geometry cut and related target-specific refinements were not sent to Claude.

