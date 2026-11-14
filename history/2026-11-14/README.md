# 2026年11月14日：完整标签分类排除核零q=28

[精选手记](../../notes/codes-kernel-zero-q28.md) · [结果与范围](RESULT.md) · [分类证明](CLASSIFICATION.md) · [实际交流](DIALOGUE.md)

只排除固定残余、核维数0的q=28。全局界仍26–27；q16、20、24以及其他残余仍未解决。

## 可复核证据

- [Bent截面检查](check_classification.py)、[结果](check_result.json)、[优化重放](check_optimized.json)。含一个真实单截面阳性行与损坏位反例。
- [独立直接字符检查](independent_check.py)、[结果](independent_result.json)、[优化重放](independent_optimized.json)。不读取第一份结果或几何数据，含100个真实符号多重集对照。
- [实际数学交流摘录与澄清](DIALOGUE.md)。答复未审后来的全标签排除。

## 复现

Python标准库，无安装依赖。在本目录运行，每项限60秒：

    timeout 60s python -I -B check_classification.py
    timeout 60s python -I -B -O check_classification.py
    timeout 60s python -I -B independent_check.py
    timeout 60s python -I -B -O independent_check.py

仅移除各输出的时间字段后比较。两套程序均硬编码与存档相同的十个残余生成行，来源仍见[既有输入](../2026-11-12/inputs/residual_candidate.json)。

[Grassl一手表](https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2)本次实际读取仍26–27。读取日期不是源站修订日期，也不代表全面文献查新。自有文字代码依仓库许可；第三方数据和构造署名保持既有来源。

[逐文件检查](PUBLIC_SAFETY_CHECK.json) · [文件哈希](SHA256SUMS.txt) · [来源与贡献](PROVENANCE.json)
