# 来源、署名与研究范围

访问与整理日期：2026-10-21。

- Markus Grassl，[二元线性码 n=64、k=11 参数条目](https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2)。当日访问仍显示下界26、上界27；不意味着条目当日更新，也不等于穷尽查新。仅引用参数和链接，不镜像数据库或 MAGMA 实现。
- Wilfried Meidl、Alexandr A. Polujan、Alexander Pott，[*Linear codes and incidence structures of bent functions and their generalizations*](https://arxiv.org/html/2012.06866v2)，arXiv:2012.06866v2，2023-05-10。作为 Walsh 变换、非线性度、线性码与可扩展性的背景；来源标示 CC BY 4.0。本日未复制其正文或代码，不声称本文证明了固定实例的更强结论。
- 本项目[10月20日基础证明](https://github.com/jamesyi030707/open-math-research/blob/a8c9ee90272b3c5f525e00a65b8667a97dc75172/history/2026-10-20/independent/quadratic_neighborhood_proof.md)、[半径13补充](https://github.com/jamesyi030707/open-math-research/blob/a8c9ee90272b3c5f525e00a65b8667a97dc75172/history/2026-10-20/independent/radius_thirteen_supplement.md)与[完整秩报告](https://github.com/jamesyi030707/open-math-research/blob/a8c9ee90272b3c5f525e00a65b8667a97dc75172/history/2026-10-20/independent/quadratic_neighborhood_report.json)，固定在审查时的提交，避免后续修订混淆来源。

## 各部分由谁产生

- Claude：实际生成的 Python 检查脚本及日志；原件字节不变。提问只公开带删节说明的数学内容，精选引用来自实际取得的输出。
- 独立 AI 辅助核查：单谱距离15对照、另写的整数 JavaScript 端点检查器、实际 JSON 报告与论证审查。对照随后由 Claude 检查，不归为其独立发现。
- 编辑整理：中文研究手记、引文选择、范围说明、导航和逐文件记录。不伪称人类实验经历、外部同行评审或新的 Claude 答复。

“独立”指实现分开编写；理论框架仍共享，可能有共同逻辑风险。Walsh 谱、二次型秩和 bent 函数均属已有理论，本项目不主张首创。本次未得到新码或全局否定定理。

沿用仓库 [许可范围](../../LICENSING.md)：自有代码按 MIT、自有可授权文字与整理按 CC BY 4.0；第三方材料仍由其原有权利控制。没有打包论文全文、外部仓库或许可不明源码。建议署名 Open Math Research contributors，user-directed, AI-assisted research；不暗示工具厂商背书。
