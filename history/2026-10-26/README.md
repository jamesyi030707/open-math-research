# 2026-10-26：枚举式条件的边界

[精选手记](../../notes/codes-enumerator-boundary.md)给出特定残余核维数1分支的形式分布见证。这不是码的构造，也不是全局不存在证明。

- `verify_enumerator_witness.py`：标准库精确核验，包含固定B、h配对、重量条件和158个MacWilliams系数。
- `enumerator_witness.json`：实际输出，含三组分布与全部变换系数。
- `AUDIT.md`：独立多项式乘法实现的审阅结果。
- `EXCHANGES.md`：真实取得交流的节选和边界。
- `LIMITATIONS.md`：生成脚本的错误与结论范围。
- `SOURCES.md`：一手参数表和公式来源。

重放：`python verify_enumerator_witness.py`。输出与JSON逐项一致。生成候选时的数值优化不作为证明；运行精确核验不需要SciPy。

本次没有重跑旧四列替换、共有子码或证明工具链扫描；没有遍历提升矩阵。
