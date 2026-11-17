# 2026-11-17：真实残余对称与证书运输

阅读入口：[研究手记](../../notes/codes-residual-symmetry.md)。

- [完整性证明与范围](PROOF.md)：固定S稳定子阶1；W稳定子阶32；运输277个既有排除限制。
- [真实一轮交流与纠正](DIALOGUE.md)。免费额度耗尽后停止，后续计算未获Claude审阅。
- `transvections.py`：7,905个候选，无有效非恒等剪切。
- `stabilizer.py`：120个特殊列置换经极化根空间判据，完整S稳定子只剩恒等。
- `independent_stabilizer.py`：用异或闭包而非选基反演独立核验，检查全部1,024消息。
- `transport.py`（完整见证保存在 `transport.json.gz`，摘要在 `transport-summary.json`）：32个实际B列置换，277×32运输后保留8,408个不同W列多重集及来源见证。
- `independent_transport.py`：独立运输核验，具体方法见代码及输出。

所有代码只用Python标准库。运行每个 `.py` 到对应临时JSON文件，比较时忽略 `cpu_seconds`（若存在）。正常与 `python -O` 模式输出均核对；各项均在60秒预算内。`SHA256SUMS.txt`用于检查本次存档字节，不包含它自身。

来源：11月17日实际读取的[Grassl参数表](https://www.codetables.de/BKLC/BKLC.php?q=2&n=64&k=11)，仍为26–27；复用11月15日277条完整h分类和11月16日两套排除证书。不复制数据库或第三方论文。所有8,408项的不可提升性依赖这条明确的既有证书链，不声称重新运行8,408个外部域检查。固定残余、双偶规约和核零分支的边界不变；未排除任何新的整个q分支。

运行 `python validate.py` 自动执行两种模式并比较完整排序列模式摘要；验证报告为 `validation.json`。`transport.json.gz` 是确定性gzip压缩的完整JSON，可用 `gzip -dc transport.json.gz` 查看。
