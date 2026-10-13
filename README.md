# 有界数学实验与核查档案

用户主导、AI 辅助的研究记录：HoTT 回答协议与 Collatz 有限证书、逆轨道搜索、阈值动态规划。保存成功、错误、撤回、负面结果和复核边界，让他人能够检查与复现。

**这是研究档案，不是 Collatz/CST 猜想证明，也不是 HoTT 不一致性的证明。没有建立原创性、同行评审或学术资历主张。** 历史原文的“定理”“已证明”“精确”等标签不代表本仓库认可；请先读 [ERRATA.md](ERRATA.md)。

## English abstract

This archive records user-directed, AI-assisted mathematical exploration of HoTT answer protocols and finite Collatz certificates. It preserves historical model answers, experimental source code, data, negative benchmarks, and separately authored checks. Results are finite, often reproductions of established work. No global Collatz or CST proof, HoTT inconsistency claim, novelty claim, or academic credential claim is made. Historical errors remain visible and are qualified by the errata. The archive is partial: missing dialogue is explicitly documented, never reconstructed.

## 导航

- [日期与主题索引](INDEX.md)
- [勘误与证据等级](ERRATA.md)
- [可复现步骤及局限](REPRODUCING.md)
- [建议下一研究：纠错码等小证书问题（尚未启动）](NEXT_RESEARCH_PROPOSAL.md)
- [当前主题的后续问题](FRONTIERS.md)
- [对话覆盖与缺口](dialogues/README.md)
- [来源与署名](SOURCES.md)
- [许可状态](LICENSING.md)
- [逐文件来源与变更](PROVENANCE.json)
- [公开包检查清单](SAFETY_MANIFEST.json)

## 最重要的结论

1. k=12 首次严格下降分类：57 个前缀、3870/4096 覆盖类、226 个未覆盖类，密度 1935/2048。独立符号检查补足原检查器仅抽查若干 lifts 的局限。它不保证未覆盖类最终下降。
2. J≤300 的有限悖常轨迹复现：593 个三元组、550 个起点。该范围弱于既有文献，不算新发现。
3. 10 月 12 日 J=92 逆树访问 1,095,960,493 节点；10 月 13 日阈值剪枝降至 22,000,065 节点，保持已知命中集合。单次计时仍逊于同轮正向基线。减少节点约 49.82 倍，不等于普遍加速或复杂度改进。
4. 原 C 叶阈值含浮点修正，尚未成为全范围认证实现。独立整数实现完整重跑到 J=46；J=92 仅检查命中与必要路径，没有独立重跑全部枚举。
5. HoTT 新增内容是纸笔草案和有限 Python 演示；没有本次新增 Agda/Lean 形式化编译证据。

历史文件按原研究批次存放。相同文件跨日重复有意保留；缺失依赖、运行预算和复用关系请见复现说明。公开版移除了非研究性账户信息，少数路径改为相对路径；逐文件哈希记录是否修改。
