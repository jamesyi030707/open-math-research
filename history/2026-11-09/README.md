# 2026-11-09：十个余类与三列障碍

[精选手记](../../notes/codes-q28-obstruction.md)。对存档残余B、核维数1分支，q=28不能实现；剩余q=16、20、24未解决。不是目标码构造、整个分支排除或全局不存在证明。

## 证明与证据

- [完整证明](RESULT.md)：q=28限制分类、两项余类恒等式、十个仿射超平面与五个二进制三元组矛盾。
- [初始检查器](check_q28_obstruction.py)、[实际结果](q28_obstruction_result.json)：155个二维子空间、816个无序三列映射、真实秩9局部控制、旧q=28形式点的1075条检查。
- [独立审阅](independent/INDEPENDENT_AUDIT.md)、[另写检查器](independent/independent_audit.py)、[实际结果](independent/independent_audit_result.json)：独立残余重建、全部155×15×4种必要条件、4096个有序三列映射、32个实际余类控制及三项损坏测试。
- [另写坐标审计](corroborating/independent_audit.py)、[结果](corroborating/independent_audit_result.json)：直接展开37个二进制坐标，独立恢复全部十个超平面、所有二维子空间的字符恒等式与4096个线性映射。
- [第二份独立审阅](review/REVIEW.md)、[检查器](review/review.py)、[结果](review/result.json)：4495种三重消息型与155个合法二维子空间的完整核验。
- [紧凑证明](corroborating/Q28_PROOF.md)、[最小证书检查](corroborating/minimal_q28_certificate.py)、[复跑结果](corroborating/minimal_q28_replay.json)。
- [先行动态规划](corroborating/initial_coset_dp.py)、[原始输出](corroborating/initial_coset_dp_original_output.json)、[另次复跑](corroborating/initial_coset_dp_replay.json)。其中155个平面“存活”只表示余类彼此独立时可行；加入同一个三列线性映射后才得到矛盾。
- [实际数学交流](DIALOGUE.md)：Claude只审阅条件性的最后一步；强制z=2的前提由另写证明与程序核验。
- [固定输入身份](input_sources.json)、[范围与澄清](LIMITATIONS.md)、[来源](SOURCES.md)、[发布检查](PUBLICATION_CHECK.json)、[公开内容检查](PUBLIC_SAFETY_CHECK.json)、[来源哈希](PROVENANCE.json)、[逐文件哈希](SHA256SUMS.txt)。

## 确定性复现

将本日期目录复制到临时目录，在副本中运行：

```sh
timeout 60s python -I -B check_q28_obstruction.py > replay_main.json
timeout 60s python -I -B independent/independent_audit.py > replay_independent.json
timeout 60s python -I -B corroborating/independent_audit.py > replay_coordinates.json
timeout 60s python -I -B corroborating/minimal_q28_certificate.py > replay_minimal.json
timeout 60s python -I -B corroborating/initial_coset_dp.py > replay_initial_dp.json
timeout 60s python -I -B review/review.py > replay_review.json
```

仅需Python标准库，不安装软件、不联网、不调用求解器。勿用禁用assert的-O。发布阶段在临时副本重跑六项，数学字段均与对应存档一致；cpu_seconds随机器和运行变化。坐标审计输出逐字节相同。

复现入口不是完整目标矩阵搜索。真实秩9控制在129个消息上违反完整提升界，不能当作目标码。此前日期的代码、数据、对话与许可保持不变。
