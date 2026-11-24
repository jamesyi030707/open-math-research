# 2026-11-24：十四条还是十六条？

[精选手记](../../notes/codes-minimal-original-sections.md) · [证明与范围](PROOF.md)。

- `witnesses.json`：八项的可行见证。最低规模为 16 的四项各用 16 个掩码；最低规模为 14 的四项用 37、51、34、38 个掩码，覆盖所有更小的子集和其余最小规模子集。
- `verify.cjs` / `result.json`：重新由 B 构造实际截面，检查见证，再以偶/奇列 14+13 分半精确核验指定无解集合，并复核 a=2 阳性对照。
- 输入：[原目录](../2026-11-15/h.json) 与 [11 月 23 日主结果](../2026-11-23/check.json)、[阳性掩码](../2026-11-23/independent_joint.json)，均不改动。

在仓库内运行 `node history/2026-11-24/verify.cjs`，输出应与 `result.json` 一致。脚本只用 Node.js 标准库。

本日结论来自独立推导和精确复算，没有新增 Claude 对话。复核 [Grassl 参数表](https://www.codetables.de/BKLC/BKLC.php?q=2&n=64&k=11) 仍列二元 [64,11] 的距离界 26–27。
