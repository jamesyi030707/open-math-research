# 2026-11-16：共同延伸条件

本轮取得一份完整Claude回复，随后显示免费额度已用完；未继续发送。以下为真实关键正文摘录，数学符号整理。结果计数由另写程序取得，不是Claude给出的计数或审阅结论。

## 提问摘录

> Derive precise necessary/sufficient compatibility conditions for four independent quotient representatives, describe why per-coset tests are insufficient, and a cheap pair obstruction certificate.

提问给出固定canonical S、277标记、18个截面幸存者及双偶规约，明确不扩展到其他取向。

## 回复摘录

> (raw window) 27 − b(a+s) ≤ wt(x + y_s) ≤ b(a+s)
>
> (premise-dependent) wt(x + y_s) ≡ −b(a+s) (mod 4), which holds only given the rank-55 evaluation result forcing the even subcode doubly even.
>
> The raw window comes straight from d(C) ≥ 27. The mod-4 condition uses that evaluation certificate, so it must be reported separately. Without it the retained sets are larger.

关于拼接，回复写道：

> The quotient map φ: u ↦ uA is linear
>
> the row Σλ_i x_{a_i} + y_{s(λ)} satisfies all 64 windows at that coset for some s(λ) ∈ W.

并指出：

> The per-coset condition is a necessary condition. It is not sufficient because the 15 sets of retained rows are joined by these linear relations, which per-coset tests never see.

## 校正与采用范围

`u↦uA`是整个消息空间上的线性映射；W上的像不为零时，它不直接下降成取值于F₂²⁷的商空间映射。若选择非线性截面ρ，修正消息必须精确等于 `ρ(a)+ρ(b)+ρ(a+b)`，不能任意寻找“某个s”。回复前一句有“determined by the section”，后面的“for some”容易掩盖这一限制。

本次代码取线性补空间：代表0至15的低四位，W消息低四位全零。所以所有修正均为0；只需检验实际行向量的异或。任何四个选定基行与已知W行都唯一规定一个线性A，充分性要检验其全部诱导余类窗口，而不是只检查四个基余类。本轮仅用前三个方向就得到必要条件矛盾，因此不依赖一个未经检验的充分性断言。

Claude建议的任意W平移搜索可作为较弱必要测试，但不作为本次固定标签的精确兼容定义。没有后续回复确认该校正，不补写对话。
