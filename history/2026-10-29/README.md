# 2026-10-29：完整分割仿射表示

[精选手记](../../notes/codes-split-affine-model.md)。固定残余、核维数1的必要条件表示；不求解计数域，不搜索矩阵。

- [生成器](affine_split.py)：`python history/2026-10-29/affine_split.py`输出[摘要](affine_summary.json)；加`--table`输出[1064行整数系数表](affine_coefficients.csv)。
- [独立多项式检查](audit_affine.py)：`python history/2026-10-29/audit_affine.py`读取相邻CSV，输出[审计结果](audit_result.json)。不导入生成器、不写文件。
- [来源](SOURCES.md)；[交流状态](DIALOGUE.md)；[溯源](PROVENANCE.json)；[逐文件检查](PUBLIC_SAFETY_CHECK.json)；[哈希](SHA256SUMS.txt)。

仅需Python标准库。两个程序验证全部八列的逆变换、65个合块恒等式、归一化及266个互补轨道；不把轨道数称独立约束数。计数可行性及消息级线性实现均未解决。较早日期记录未改写。
