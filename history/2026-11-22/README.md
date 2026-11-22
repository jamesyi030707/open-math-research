# 2026-11-22：两个实际外截面的 345 张支集表

[精选手记](../../notes/codes-singleton-support-catalog.md) · [证明与范围](PROOF.md) · [会话状态](DIALOGUE.md)。

- `check.py` 与 `result.json`：逐个组合和四维商两种方法核对每个截面 345 张支集；60 个局部代表及逐项见证。
- `independent.py` 与 `independent_result.json`：另写实现复算两个截面、候选、命中及证书覆盖。
- `validation.json` / `SHA256SUMS.txt`：正常与优化模式结果、输入哈希和证据边界。

在本目录运行 `python check.py`、`python independent.py`，分别与对应 JSON 比较；加 `-O` 复验。两个实现均只用 Python 标准库。依赖 [h.json](../2026-11-15/h.json) 及 [11 月 21 日 result.json](../2026-11-21/result.json)。

本日复核 [Grassl 参数表](https://www.codetables.de/BKLC/BKLC.php?q=2&n=64&k=11)：二元 [64,11] 最小距离下界 26，上界 27。此次只给固定残余、固定规约下的有限排除，未更新距离界。
