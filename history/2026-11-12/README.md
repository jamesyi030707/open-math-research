# 2026年11月12日：核维数0的重复列预算

[精选手记](../../notes/codes-kernel-zero-pairs.md) · [完整推导](RESULT.md) · [范围](LIMITATIONS.md) · [真实交流](DIALOGUE.md) · [来源](SOURCES.md)

固定残余的核维数0分支中，相反h位的重复列对数由二阶矩差决定：q=28只留下(r,z)=(4,1)、(24,3)，q=24排除r=12、16，q=16、20的r取值未减少。两个秩6局部控制可实现剩余q=28参数，但不是完整提升。

## 证据入口

- [初始检查器](check.py)、[实际结果](result.json)及[优化模式结果](result_optimized.json)：固定输入、全部消息窗口、秩55刚性、列对公式、小整数参数筛选、两个真实W限制和4241个小维数列多重集对照。
- [分开编写的审核说明](independent/REVIEW.md)与[程序](independent/review.py)、[结果](independent/result.json)及[优化模式结果](independent/result_optimized.json)：重新推导和枚举参数、核查两个真局部矩阵及异或条件。

- [真实交流](DIALOGUE.md)仅一轮，审查整体限制矩及必要结构；本日独立列对筛选未送Claude审阅。

两份实现都不依赖会被-O关闭的assert。独立指分别编写的AI辅助检查，并非外部人类同行评审。代码不替代一般证明。

## 复现

复制整个本日目录到临时目录，使用Python标准库，每项限60秒：

    timeout 60s python -I -B check.py
    timeout 60s python -I -B independent/review.py

两项也增加-O重复核验，只排除cpu_seconds后与存档结果逐字段比较。无完整矩阵搜索。实际发布重放见[PUBLICATION_CHECK.json](PUBLICATION_CHECK.json)，文件校验见[SHA256SUMS.txt](SHA256SUMS.txt)。
