# 2026-10-22：两谱兼容性与重复约束的停止点

先读精选手记：[两个谱真的相容，为什么仍没有加强？](../../notes/codes-pairwise-compatibility.md)

## 本日结论

精确 Walsh 卷积关系由共同真值表直接推出，对既有64变量、512个谱界模型是冗余改写。经典二元矩阵行列和条件可区分抽离的合法纤维投影，但没有排除任何剩余目标分布。

另写检查复核四个64点函数的256个卷积坐标、512个带符号投影坐标、16个真实网格和3个行列和对照。昨日十五步函数的八谱最大绝对值为(10,10,10,10,18,18,10,18)，故不是固定母码扩展见证。没有新码、完整不可行证书或首创声明。

## 证据入口

1. [真实交流及范围](EXCHANGES.md)、[最终可见答复](claude/response-1-visible.txt)、[数学问题节录](claude/prompt-1-math.txt)。
2. [Claude 实际源码](claude/translate_relation_check.py)与[生成时日志](claude/translate_relation_check_log.txt)。
3. [另写证明与核查](independent/README.md)、[检查器](independent/audit_pairwise.py)、[实际报告](independent/pairwise_report.json)。
4. [边界与注意事项](LIMITATIONS.md)、[来源](SOURCES.md)、[逐文件来源](PROVENANCE.json)、[公开检查](PUBLIC_SAFETY_CHECK.json)、[校验清单](SHA256SUMS.txt)。

## 最小复现

在仓库根目录，使用 Python 3 标准库：

    python3 -I -B history/2026-10-22/independent/audit_pairwise.py > pairwise_report.rerun.json

数学字段应与存档报告相同；cpu_seconds随运行变化，比较时须排除。发布检查另行重跑并比较数学字段。Claude 原脚本仅作 AST 语法检查，生成时日志不是本次发布重新运行；不重复其1500个抽样。

[前一日边界](../2026-10-21/README.md) · [所有日期](../../archive/README.md)
