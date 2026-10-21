# 2026-10-21：半径13审查与单谱十五步边界

先读精选手记：[十五步恰好可达，为什么还不是一个码？](../../notes/codes-single-spectrum-limit.md)

## 已得到什么

- 独立复核半径13排除论证，包括仿射 Walsh 支持。标准秩4型的128个仿射扰动乘136个端点谱型，共17,408例全部违反纤维整性；其中13,056例的支持不经过原点。
- 显式单谱对照 u=x₀x₁+x₂x₃+x₄x₅+δ₄₈，重量27，与 h=x₀x₁+x₂x₃ 的距离15，最大 Walsh 绝对值10。它说明同一单谱前提不能推出距离至少17。
- 一次真实 Claude 交流留下了 Python 源码与日志，验证了预先提供的对照，并在300个抽样秩4型上核查40,800个端点配置。没有最终文字答复，也没有新的跨谱排除条件。

固定母码结论仍是 d(f,RM(2,6))≥15。七种必要分布未进一步缩减。单谱对照不是固定 E 的扩展见证；无新码或完整不可行证书。

## 按证据阅读

1. [真实交流节选](EXCHANGES.md)：数学提问与生成日志，明确区分原文和编者说明。
2. [独立论证说明](independent/README.md)、[JavaScript 检查器](independent/audit_radius_thirteen.js)、[实际 JSON 报告](independent/endpoint_audit_report.json)。
3. [Claude 实际源码](claude/rank4_r15_audit.py)与[实际日志](claude/rank4_r15_audit_log.txt)；[数学问题节录](claude/prompt-1-math.txt)是标注过删节的研究内容，不是完整对话转储。
4. [边界与实现注意事项](LIMITATIONS.md)、[来源与许可范围](SOURCES.md)。
5. [逐文件来源](PROVENANCE.json)、[公开内容检查](PUBLIC_SAFETY_CHECK.json)、[日期校验清单](SHA256SUMS.txt)。

## 最小复现

使用支持 BigInt 的 Node.js，无外部依赖。在仓库根目录运行：

    node history/2026-10-21/independent/audit_radius_thirteen.js > endpoint_audit_report.rerun.json
    cmp endpoint_audit_report.rerun.json history/2026-10-21/independent/endpoint_audit_report.json

这只审查17,408个端点配置与64位显式对照，不搜索函数空间。发布前独立重跑结果与存档报告逐字节一致。

Claude 源码通过 Python AST 语法检查，但发布检查没有再次执行它：其末段重复了昨日的32,768型枚举。原生成日志保留；不要把该日志冒充发布阶段的新运行。若要完整重放，标准库 Python 3 即可，在临时副本运行原脚本；其中的抽样检查不能代替一般证明。

[前一日证明](../2026-10-20/README.md) · [所有日期](../../archive/README.md)
