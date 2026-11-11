# 2026年11月11日：列重数奇偶性排除固定核维数1分支

[精选手记](../../notes/codes-kernel-one-obstruction.md) · [完整证明](RESULT.md) · [范围与澄清](LIMITATIONS.md) · [真实交流](DIALOGUE.md) · [来源](SOURCES.md)

固定存档残余B、归一化偶子码的左投影核维数1分支被排除。五个线性无关的恒重超平面法向量成为同一个列重数奇偶函数的周期，使q=16、20、24、28全部产生矛盾。核维数0、其他残余和全局二元[64,11,27]存在性仍未解决。

## 证据分工

- [完整推导](RESULT.md)、[初始检查器](check_fourier_obstruction.py)、[实际结果](result.json)及[优化模式结果](result_optimized.json)：固定输入、秩55、十个超平面、全部q值；6401个真实仿射列配置、89614个超平面对照；旧q16/q20形式见证回归及损坏测试。
- [第一份独立审计](independent/AUDIT.md)、[程序](independent/audit_fourier_branch.py)、[实际结果](independent/audit_result.json)：重新发现超平面，186个实际矩阵对照、不同的q20左矩阵扩展，以及另用三项递推计算全部旧分割系数。
- [第二份独立审阅](second_review/REVIEW.md)、[程序](second_review/review.py)、[实际结果](second_review/result.json)：全部奇偶等式秩31、4845个真实仿射配置和67830个超平面对照；检查缺少满秩时不能排除的反例。
- [真实交流及审阅边界](DIALOGUE.md)只有一轮：审查q20重数类型与分类，明确未声称排除；后来的奇偶周期证明未送交Claude。

“独立”指分开编写的AI辅助实现与审阅，不是外部人类同行评审，也不是形式证明内核认证。两种小型穷尽对照采用不同计数方式，配置数不能混用。真实q20局部码并非完整提升，详见范围说明。

## 复现

将整个本日目录复制到临时目录。Python 3.10+，只需标准库；每项限60秒：

    timeout 60s python -I -B check_fourier_obstruction.py > initial.rerun.json
    timeout 60s python -I -B independent/audit_fourier_branch.py > audit.rerun.json
    timeout 60s python -I -B second_review/review.py > review.rerun.json

三项也均在增加-O参数的优化模式下重放通过。比较时只排除cpu_seconds，所有数学字段必须一致。程序使用显式异常，不依赖会被-O关闭的assert。实际发布复跑见[PUBLICATION_CHECK.json](PUBLICATION_CHECK.json)。不运行历史大型实验、数值求解器或完整目标矩阵搜索。

[PROVENANCE.json](PROVENANCE.json)记录来源和编辑变更，[SHA256SUMS.txt](SHA256SUMS.txt)校验本日文件字节；哈希不证明数学正确。
