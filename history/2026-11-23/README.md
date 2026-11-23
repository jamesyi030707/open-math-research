# 2026-11-23：任意一对可满足，整组却无解

[精选手记](../../notes/codes-pairwise-section-gap.md) · [证明](PROOF.md) · [会话状态](DIALOGUE.md)。

- `check.py` / `check.json`：十二个固定对照的短筛、八项的精确双字符投影与实际重量截面核验。
- `independent_arithmetic.py` / `independent_arithmetic.json`：独立复算单列、同余以及先前运输覆盖。
- `independent_joint.py` / `independent_joint.json`：单独实现两截面的精确双字符与原始重量十六维分半搜索，提供阳性掩码。
- `validation.json` / `SHA256SUMS.txt`：输入、证据边界和复验记录。

在本目录分别运行三个 Python 脚本，把标准输出与同名 JSON 比较。均只用标准库。主实现依赖 [11 月 15 日分类](../2026-11-15/h.json) 和 [11 月 22 日证据](../2026-11-22/result.json)；独立脚本只读前者。普通与 `-O` 输出一致。

[Grassl 参数表](https://www.codetables.de/BKLC/BKLC.php?q=2&n=64&k=11) 今日仍列 26–27。本结果仅针对固定残余的十二个真局部对照。
