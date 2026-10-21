# 真实交流节选：2026-10-21

一次数学提问实际产生了 Python 源码与运行日志，未取得最终文字答复。下文只引用已取得内容，不补写缺失答复。完整数学问题的删节版本见 [prompt-1-math.txt](claude/prompt-1-math.txt)：删除了非数学流程表述，保留的英文段落未改写；本页引文也均为原文中的连续片段。

## 提问中的关键限定

> “This is NOT a fixed-E witness. Audit the short proof and this witness, then suggest one genuinely stronger low-cost constraint coupling different q translates, with a concrete small verification target and stop condition. Clearly separate the single-spectrum sharpness from all512 constraints.”

编者说明：距离15的显式对照先由独立核查提出，再交给 Claude 审查，不是 Claude 独立发现。被审查的是半径13排除论证、单谱对照，以及是否存在更强跨谱条件这三个不同问题。

## 实际输出：生成日志，不是最终答复

以下摘自 [rank4_r15_audit_log.txt](claude/rank4_r15_audit_log.txt)：

> “r=13 deficit patterns tested: 40800; patterns whose projection leaves the allowed set: 40800 (all must fail)”

> “witness: wt(u)=27, d(u,h)=15, max|W_u|=10, aligned values on S: ten 10s=10, six 6s=6, aligned sum=136 (=256-8*15=136), |S|=16”

> “single translate only; not a statement about all 512 coefficients of a fixed E”

编者说明：40,800=300×136，其中300个秩4型是固定种子抽样，并非所有秩4型。另写 JavaScript 检查器的17,408例则穷尽了一个标准秩4型的128个仿射扰动与136个端点配置。这是两项覆盖范围不同的检查，不能把数字合并成一般穷举证明。

## 没有得到的新条件

[生成代码](claude/rank4_r15_audit.py)对所谓耦合条件的原文是：

> “coupling: for a quadratic g, (f+q)+(g+q) = f+g, so ALL eight pairs have the same r.  A translate of rank <=2 forces r >= 23; rank 0: r>=27.”

编者说明：这个共同距离观察及所附秩计数已经出现在昨日证据中，不是新的排除。代码重跑已有32,768型秩枚举，不能计为新的研究推进。所请求的更强跨谱测试没有交付，也没有因此减少七种剩余必要分布。

代码、日志按实际取得的字节保留；生成脚本对仿射支持的抽样诊断以及重跑范围，见 [LIMITATIONS.md](LIMITATIONS.md)。研究评注是本次整理，不伪装为对话原话。
