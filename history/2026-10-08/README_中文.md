# HoTT 与 Collatz 研究：核查附件

日期：2026-10-08

本包包含 HoTT 研究、Collatz k=12 有限证书及独立核查记录。五份 Claude 原产物保持字节不变。固定仓库提交仅用于 HoTT 源码核对。

## 文件
- claude_research_note_20261008.md：Claude 的英文研究草稿，讨论 Answer(C)、逐点判定器、LPO/LEM、编码引理及黑盒查询下界。
- claude_bb_demo_20261008.py：有限测试检查器，仅用 Python 标准库。可运行 python3 -I -B claude_bb_demo_20261008.py。

## 独立检查结果
先只读检查代码：未见网络访问、文件写入、外部进程执行或登录信息。随后独立运行，退出码为 0。

- 44,105 棵查询树：35,284 个在全 false 输入上错误，8,821 个在构造的尾部 true 输入上错误；locality 违例 0。
- 20,000 个固定种子确定性策略：对应为 5,947 与 14,053；locality 违例 0。
- 故意读取隐藏序列的白盒负控制正确触发 LOCALITY_VIOLATED。
- 承诺首个 true 位于 0 至 40 或全 false 时，scan(41) 正控制通过。

树的有限范围：深度至多 2，查询位置为 {0,1,2,3}，输出为 inr 或 inl 0 至 3。数量递推为 T0=5，T1=5+4×5²=105，T2=5+4×105²=44,105。固定种子策略至多执行 30 步；这些并不是对随机算法一般性质的验证。

## 证明状态与范围
- BB′ 的纸笔反例在确定性有限点查询与 locality 假设下成立，不需要统一运行时间上界。
- 最小见证抽取的纸笔论述在逐点可判定等所述前提下成立：最小见证类型为命题，允许消去命题截断，再忘掉最小性。
- 将 LEM 定义为函数后，LEM→Ψ 的纸笔论述不需要额外选择公理。
- 编码 E 的 h-level 偏移与 retract 思路未见逻辑错误；库引理衔接、宇宙层和形式化仍待验证。
- 本包新增论述没有编写或编译 Agda/Lean。Python 有限检查不是机器验证的一般数学证明，也没有证明相关原则的系统独立性。
- 仓库自身既有证明与本包新增研究必须分开：仓库历史运行记录不是本次独立重编译。

## 一处文字纠正
原研究草稿第 6 节把“白盒访问 judge 的代码或证明”括注为“恰好是目标 (b)”，这一表述不准确。目标 (b) 的输入是完整的全局 Dec(Σ n, P_C n)；仅能读取逐点判定器的代码或证明，不会自动获得这个全局证书。原文保留，以上述纠正为准。

BB′ 仅适用于其明确描述的查询模型，不能直接推出所有 Cubical Agda 闭项均不可定义，也不能据此宣称 HoTT 不一致或宇宙不存在。

## 原产物 SHA-256
- claude_research_note_20261008.md: fb575a727441d17cdcc323f408b4c8bc8b897cf589a2c89564d7a5f41cb8c842
- claude_bb_demo_20261008.py: e2ff0c2b5066c9db518fe2a79c4f6b863027741092985141fcbc04541456b151

## Collatz k=12 补充交付
Claude 第四轮完整文字推导被使用限额截断；本包保存其已产出的证书、检查器和日志，并补充独立核查，不能将其描述为 Claude 已完成全部文字论证。

- 原始文件：claude_cert_k12_20261008.json、claude_check_cert_k12_20261008.py、claude_check_log_k12_20261008.txt。
- 独立核查：dot_collatz_independent_audit_20261008.txt、dot_independent_symbolic_k12_20261008.py、dot_independent_symbolic_k12_log_20261008.txt、dot_claude_checker_rerun_20261008.txt。
- 对 T(n)=n/2（偶数）、(3n+1)/2（奇数），原检查器真实复跑 --selftest --N=200000，退出码 0；57 前缀、3870 覆盖类、226 剩余类、1935/2048 权重，以及九项篡改拒绝全部复现。
- 原检查器 C1/C3 仅抽查 4/5 个 lifts，不能单凭抽样推出整个无限同余类结论。独立符号检查器按 n=r+4096q 的精确整数仿射表示验证全类公式，并结合严格阈值补足该结论；运行退出码 0。详见中文审计说明。
- 结论仅为所有 n>1 的首次严格下降是否发生在 12 步内的精确分类，及该集合自然密度 1935/2048；不证明 Collatz 猜想，不保证 226 剩余类随后下降，也不是 Agda/Lean 内核验证。
- 原检查器部分 C4 的 PASS 打印并不代表最终成功，应查看最终结论及退出码。不要使用 Python -O，因为检查器使用 assert。

解压至同一目录后运行：
python3 -I -B claude_check_cert_k12_20261008.py claude_cert_k12_20261008.json --selftest --N=200000
python3 -I -B dot_independent_symbolic_k12_20261008.py

## 全部附加文件 SHA-256
- claude_research_note_20261008.md: fb575a727441d17cdcc323f408b4c8bc8b897cf589a2c89564d7a5f41cb8c842
- claude_bb_demo_20261008.py: e2ff0c2b5066c9db518fe2a79c4f6b863027741092985141fcbc04541456b151
- claude_cert_k12_20261008.json: 8189b40ceae982812f57b973985665751469cd7d7e55902401e3c96e8f88fa89
- claude_check_cert_k12_20261008.py: bfd990bda02d4453930cf537426789ed71aa34c9bdb97f6adeb7cc98298112a1
- claude_check_log_k12_20261008.txt: d8122cfcf6cb7377e7ed892bae348742eb0d66676bd81356214133e0deccab4d
- dot_collatz_independent_audit_20261008.txt: 7b4f568b701df02fdc97e1119c359575b2e8fc98264efae263917900ca3cb05b
- dot_independent_symbolic_k12_20261008.py: 33214fb3240bd4578f2db51c065d977e7e7ac3e6c209b4993da7a419f08710eb
- dot_independent_symbolic_k12_log_20261008.txt: 9e9baf29c7ca3a88b64e5d5d65f51e972314471dc4112c951d470aeac4e99b8a
- dot_claude_checker_rerun_20261008.txt: 66d0dbb3da0337e564d320640f37459493af50e0778ee987188afc98e4e7b868
