# 2026-10-27：分割重量检验

阅读版：[总数没有矛盾，分到两块却出现负数](../../notes/codes-split-weight-obstruction.md)。

结论只针对2026-10-26给出的固定联合分布。分割对偶系数(1,2)=−16，故该联合分布无法由二元线性码实现。全核分支及[64,11,27]存在性仍未决。

Python3标准库重放，在仓库根目录：

```sh
python history/2026-10-27/split_check.py history/2026-10-26/enumerator_witness.json
python history/2026-10-27/audit_split.py
python history/2026-10-27/check_toy.py
```

首个实现使用二项式求和，第二个独立实现使用重复多项式乘法。`split_result.json`保存联合分布、首个负系数各项分子、全部1064个分割变换系数以及普通对角线和；`result.json`为独立输出。两者全系数一致，8项为负，所有对角线和恰与旧证书一致。

预算：只对一个已存档点作确定性计算，单次不到1秒；没有矩阵搜索、优化器调用、完整分支枚举或新软件安装。实际交流与来源见[EXCHANGES](EXCHANGES.md)、[SOURCES](SOURCES.md)、[范围](LIMITATIONS.md)。

Claude原可见脚本和日志保存在claude子目录，包含原界面空白尾行，不作为直接运行入口。`check_toy.py`仅核验日志中的两个固定八项例子，不重跑遍历或随机试验。
