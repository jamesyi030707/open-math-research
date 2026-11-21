# 2026-11-21：六个真实新标签的单列消去证书

入口：[精选手记](../../notes/codes-single-column-certificate.md) · [证明与范围](PROOF.md) · [真实会话状态](DIALOGUE.md)。

- `check.py` / `result.json`：十个低位交换控制、十个实际最低字外截面、旧8,408运输集回归，以及六个单列证书。
- `independent.py` / `independent_result.json`：自包含独立复算六项、384个单字符投影和实际平移轨道。
- `validation.json` / `SHA256SUMS.txt`：运行模式、证据边界、输出校验。输入沿用 [11 月 15 日 h.json](../2026-11-15/h.json)，Git blob `6c2f005c33236b54ed1850f78b7700fcb44b7237`。

在本目录执行 `python check.py` 和 `python independent.py`，输出分别与两个对应 JSON 比较；再以 `python -O` 检查。均只使用 Python 标准库。

[Grassl 参数表](https://www.codetables.de/BKLC/BKLC.php?q=2&n=64&k=11) 最近可读正文列下界 26、上界 27；11 月 21 日所读正文标注为前一日抓取，直接探测返回 429，勿当作当日实时刷新。没有新增距离界。
