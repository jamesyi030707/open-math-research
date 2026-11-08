# 2026-11-08：列关联与更强的必要条件

[精选手记](../../notes/codes-column-incidence.md)。固定残余、核维数1分支新增必要条件2a+d−b−2≥0，严格加强旧1075条形式条件加q≥16。它排除一个q=16形式点的所有标签实现；四个q值仍各有形式存活点，没有目标码或分支排除。

## 证据入口

- [独立列论证与证书](RESULT.md)、[初始检查器](check_column_cut.py)、[实际结果](column_cut_result.json)。
- [另写的坐标/多项式审计](audit_column_obstruction.py)、[结果](audit_column_obstruction_result.json)。
- [固定历史输入及远端身份](input_sources.json)。
- [真实数学交流](DIALOGUE.md)：重复列二阶矩、q=28限制码分类和余类矩；未讨论后续更强的列限制。
- [分开编写的限制码证明](subspace/audit_subspace_extensions.md)、[检查器](subspace/audit_subspace_extensions.py)、[实际结果](subspace/audit_subspace_extensions_result.json)。
- [最先取得的四个形式点](subspace/intersection_result.json)。它们来自[有界候选生成](subspace/check_intersection.py)，同样已由精确检查独立接受。
- [后续候选生成](discover_column_cut.py)、[实际数值日志](discovery_result.json)。这两份数值程序不属于证明依赖。
- [范围与澄清](LIMITATIONS.md)、[来源](SOURCES.md)、[发布核验](PUBLICATION_CHECK.json)、[公开检查](PUBLIC_SAFETY_CHECK.json)、[溯源](PROVENANCE.json)、[哈希](SHA256SUMS.txt)。

## 确定性复现

将本目录复制到临时目录，在副本中运行：

```sh
timeout 60s python -I -B check_column_cut.py > check_replay.json
timeout 60s python -I -B audit_column_obstruction.py > column_audit_replay.json
cd subspace
timeout 60s python -I -B audit_subspace_extensions.py > subspace_audit_replay.json
```

仅需Python标准库，无安装、求解器或网络。不要用禁用assert的-O。第一项只有cpu_seconds随机器变化；后两项会重写相邻结果JSON。发布核验在临时副本中重跑三项，数学字段全部一致，两个独立审计输出逐字节一致。

原始数值候选生成使用NumPy/SciPy，保留源码和实际日志供追溯；本次发布未重复数值搜索。subspace/check_intersection.py须在其目录中以普通Python运行，因其导入同目录affine_split.py，不是上述隔离模式检查入口。求解器状态不构成数学证明。
