# 真实数学交流与编辑澄清

本日取得一轮完整可见回复。下方问题为实际发送内容的数学节选，省略开场回顾和输出形式要求；回复文字完整保留，仅规范段落、项目符号与数学排版。没有补写第二轮交流。代码核验与局部真码控制另行记录。

## 实际数学提问节选

For the archived full-rank 10x37 residual matrix B, h=1008 is its unique weight-32 message. Direct exact enumeration finds T={0,16,32,...,1008} is a dimension-6 subspace: apart from 0,h, all 62 messages have wt(uB)=wt((u+h)B)=16. In the kernel-one branch hA=0 for a 10x27 matrix A. The 31 nonzero h-pairs in T/<h> have common A-weight either 12 or 16; q counts those of weight 12, and the Nov 5 feasible formal witness has q=0. Thus sum_(u in T) wt(uA)=2[12q+16(31-q)]=992-8q. For any actual binary matrix A, the same sum is 32N_T, where N_T counts columns whose restricted linear functional on T is nonzero, so N_T<=27. Therefore N_T=31-q/4, q≡0 mod4, and q>=16; with 0<=q<=31, q∈{16,20,24,28}. Please scrutinize this proof and its assumptions, explain why actual subspace closure is essential and not implied by an unlabeled split histogram, and delimit exactly what is excluded.

## Claude实际可见回复

The proof is correct as stated, under the assumptions below.

Check of the algebra.

- T has dimension 6 and contains h. Since hA = 0, the map u ↦ wt(uA) factors through T/⟨h⟩ ≅ F₂⁵. That quotient has 31 nonzero classes, so the 62 messages other than 0 and h form 31 h-pairs.
- Each pair has a common A-weight s ∈ {12,16}. With q pairs at s = 12, Σ_{u∈T} wt(uA) = 2[12q + 16(31−q)] = 992 − 8q. The pair {0,h} contributes 0.
- For a real matrix A, each column c gives a linear functional u ↦ u·c on T. If that functional is nonzero it equals 1 on exactly 32 of the 64 messages of T, and 0 on all 64 if it is zero. So Σ_{u∈T} wt(uA) = 32·N_T, where N_T counts columns with nonzero restriction. Hence N_T = 31 − q/4.
- N_T ≤ 27 gives q ≥ 16. Integrality of N_T gives 4 | q. With q ≤ 31, q ∈ {16, 20, 24, 28}.
- The formal witness has q = 0, so it fails this test.

Assumptions.

- The exact enumeration of T for the archived matrix B, which I take as given.
- The window s ∈ {12,16} for t = 16 pairs, which comes from the earlier doubly-even normalization. It uses 27 − t ≤ s ≤ t and s ≡ t (mod 4).
- Ah = 0 (kernel-one branch).

Why subspace closure matters.

The identity 32·N_T uses that T is a subspace, so the 64 messages sum with the columns’ linear functionals. An unlabeled split histogram records only how many messages have each weight. It does not record which messages form a subspace, so it cannot see this relation.

What is excluded.

Only a q = 0 completion (formal witness with 31 pairs at s = 16) is excluded. Branch-level conclusions need q ∈ {16,20,24,28} tested against the other constraints. This does not exclude the branch, nor any [64,11,27] code.

## 编辑澄清，不是Claude原话

- 假设列表的“Ah = 0”是维度不合的笔误。消息为行向量，正确写法是hA=0；回复前面的代数段落采用了正确写法。
- “Only a q = 0 completion”若按字面理解过窄。必要条件排除q<16，以及不满足整除条件的q；本日特别应用于原q=0见证。整除条件早已有于原模型，本日新增的是下界。
- “nor any [64,11,27] code”应理解为没有全局不存在结论。固定B、固定分支及指定见证的补全确实已被本论证排除。
- “real matrix A”在此指实际实现的二元矩阵，不是任意实数矩阵。
- Claude明确把T的具体枚举作为给定前提，没有独立运行残余核验；本日q=16的独立局部控制未提交给Claude审阅。实际计算证据在独立脚本与日志中，不以条件性文字认可代替。
