# 2026-11-15：真实交流摘录与校核

本页保留本轮已取得回答的正文转录（数学排版整理），提问只摘录核心数学部分，不是完整提示词转录。只完成一轮；免费额度提示随后出现，未继续发送。下列错误保留并紧接纠正；277计数与9轨道是另写程序的结果，不冒充Claude给出的结论或审阅。

## 提问摘录

> Can these force a compact complete classification of h assignments, especially r4 and r24, without enumerating 2^27 matrices? Derive exact small-side formulas: for marked weights e_s=sum b_v(s dot v), w(s+h)=r+w(s)-2e_s. State which small combinations must be checked and whether all r8/20 cases remain.

上下文明确给出了旧S分类、双列预算、q′公式、60秒局部检查目标，以及局部换基不等于固定残余自同构的限制。

## Claude回答正文

**Setting** (E = L ⊔ C, columns as in the Nov 10 classification: 19 singles, 3 doubles, 9 absent, plus 2 zero columns). Let w(s) = 16 if s ∈ E and 12 otherwise, for s ≠ 0. Take b_v ∈ [0, m_v], z ∈ {0,1,2}, and r = z + Σb_v. Define e_s = Σ_v b_v (s·v) and
w(s+h) = r + w(s) − 2e_s, w(h) = r. The unmarked column counts are m_v − b_v, and zero columns marked z of 2.

**Exact small-side formulas.** For s ≠ 0, the window ω(s) ∈ {12,16} requires e_s = (r + w(s) − ω(s))/2:
- s ∈ E: e_s = (r + 16 − ω)/2 ∈ {r/2, r/2 + 2}.
- s ∉ E: e_s = (r + 12 − ω)/2 ∈ {r/2 − 2, r/2}.

So e_s ∈ {r/2 − 2, r/2, r/2 + 2}, forced to lie in [0, r − z]. By Parseval over s,
Σ_s e_s = 16Σb_v and Σ_s e_s² = 8[(Σb_v)² + Σb_v],
since b_v ≥ 0 are multiplicities of the marked columns (zero columns are constant). The marked set Y has |Y| = r − z.

**r = 4.** Then e_s ∈ {0, 2, 4}, so |Y| ≤ 4 − z and 4 − z ≥ 2. Every e_s is even, so XOR(Y) = 0. With r = 4: z = 0 forces |Y| = 4, a circuit (any three independent), but then e_s = 4 is attained, and s ∈ E needs e_s ∈ {2, 4} while s ∉ E needs e_s ∈ {0, 2}. That is a finite check of which circuits (including repeated-multiplicity ones: a double with b = 2 counts twice) satisfy it. z = 1 forces |Y| = 3, a line. z = 2 forces |Y| = 2, which is XOR 0 only if Y is one repeated double (b_v = 2), so e_s ∈ {0, 2}·... — one more small case. All r = 4 cases are therefore finite assignments of ≤ 4 marked items.

**r = 24.** Replace b by the complement: unmarked items have total 3 − (2 − z) ... that is, 27 − 24 = 3 copies remain. So the unmarked set is again ≤ 3 items, by symmetry (h ↔ h + complement of all columns). It reduces to r = 4-type conditions on those ≤ 3 items. I stated this symmetry from the structure of w(s+h); I did not derive it independently.

**r = 8, 20.** These stay open. For r = 8: |Y| ≤ 8, e_s ∈ {2, 4, 6}. For r = 20 the complement has 7 copies, with e′_s ∈ {r′/2 ± 2, r′/2}. The marked sets can be quite large. They are not forced to be ≤ 3 items.

**Counts.** The assignment space is Π(m_v + 1)·3 for the marked multiplicities: 2¹⁹·... (19 singles, 3 doubles) × 3 zero-column choices. Simply enumerating 2¹⁹·3³·3 is about 4·10⁷ marked configurations, feasible in 60 s with an incremental e_s array, and the pruned cases above are tiny subsets of it.

**Algorithm (one canonical E, labels explicit).** For each (b, z) with r ∈ {4, 8, 20, 24}:
1. Compute w(s+h) for all s and test the windows 12/16.
2. Check XOR(Y) = 0.
3. Check the moment identity P and q′ = 24 + r/4 − 8z.
4. Keep the survivors with their b_v.

Transport to other E is not an automorphism of fixed B. No q = 24 exclusion claim here.

## 校核与勘误

1. 第一、二条逐消息窗口正确。二阶矩应为 `Σ_s e_s²=8[(Σ_v b_v)²+Σ_v b_v²]`，v遍历非零S标签。展开平方，单标签出现16次、不同非零标签同时出现8次，即得该式。重复标签不能丢掉平方。
2. 四份标签异或为零本身不保证是四点回路；例如两对重复标签。这里需先用P=3强制三个双列均被分裂，再由异或锁定28，才能得到唯一的四个互异标签。
3. 补集是枚举技巧，不是把r24无条件化成r4的对称性。令d_v=m_v−b_v、d_s=Σd_v(s·v)，则 `w(s+h)=r−w(s)+2d_s`。r=24时，对w(s)=16有d_s∈{2,4}，对w(s)=12有d_s∈{0,2}；还须保留未选非零列数1+z、未选零列数2−z。r20同理由原式重算，不采用回复中未定义的r′窗口。
4. “60秒可行”是未实测估计；本次实际采用更小侧的完整枚举，两种实现分别约0.07秒与3秒。真实运行证据另存。
5. 回复没有精确计数或目标码结论。所有局部标记列表、计数和轨道均由另写程序提供。
