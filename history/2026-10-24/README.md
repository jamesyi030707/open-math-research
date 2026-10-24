# 2026-10-24：残余码提升入口

先读[精选手记](../../notes/codes-residual-lift.md)。本日只有一次未完成文字答复的真实交流，原生成脚本和独立核验分开保存。

- [实际交流](EXCHANGES.md)、[范围与勘误](LIMITATIONS.md)、[来源](SOURCES.md)。
- [派生残余生成基](independent/residual_candidate.json)、[可移植枚举器](independent/audit_candidate_public.py)。
- [64例玩具穷举](independent/audit_toy.py)、[结果](independent/toy_result.json)。
- [原生成脚本](claude/residual_lift_control.py)、[独立重跑输出](independent/claude_script_rerun.txt)。原脚本的距离标签须结合勘误阅读。
- [独立数学审阅](independent/AUDIT.md)、[来源与哈希](PROVENANCE.json)。

精确提升条件与候选分布已核验；两个投影核分支均未排除。没有新的[64,11,27]构造。
