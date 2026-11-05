# 2026-11-05：完整形式模型有整数解

[精选研究手记](../../notes/codes-split-feasible-witness.md)。见证为七计数(28,0,100,32,4,62,0)，对应七整数参数(6,14,4,0,31,2,0)。全部1075条必要条件成立，不代表真实码存在。

## 证据入口

- [精确证书](certificate.json)、[完整证明说明](FEASIBILITY.md)、[1075条逐行余量](slacks.csv)。
- [标准库证书检查器](check_certificate.py)、[小控制](controls.json)、[损坏测试](test_checker.py)。
- [独立审计说明](AUDIT.md)、[独立实现](audit.py)、[结果](audit_result.json)：从原始分母1024表与数值原分布分别核查完整分割变换、逆变换和合块。
- [真实交流](DIALOGUE.md)、[来源与范围](SOURCES.md)、[溯源](PROVENANCE.json)、[公开检查](PUBLIC_SAFETY_CHECK.json)、[文件哈希](SHA256SUMS.txt)。

## 从仓库根目录复现

只需Python标准库，逐个任务限时60秒，不重新搜索候选：

```sh
timeout 60s python -I -B history/2026-11-05/check_certificate.py history/2026-11-05/controls.json
timeout 60s python -I -B history/2026-11-05/check_certificate.py history/2026-11-05/certificate.json --model-dir history/2026-11-04
timeout 60s python -I -B history/2026-11-05/test_checker.py --model-dir history/2026-11-04
mkdir -p replay-2026-11-05
timeout 60s python -I -B history/2026-11-05/audit.py --output-dir replay-2026-11-05
```

独立审计的默认输入是此前两个日期的归档目录，输出另放，避免改写历史结果。可用归档中的SHA-256比较三个输出文件。另有[直接原始表复核](audit_original.py)与[结果](original_audit_result.json)，不依赖求解器。

[可选发现脚本](discover.py)仅用于候选发现，依赖SciPy；原运行设110秒求解器限制、120秒外部进程上限，实际求解调用约0.018秒。证明无需安装或调用求解器。

检查器只支持整数可行见证与实不可行的精确Farkas证书，不支持整数不可行树。本次有可行见证，不需要否定证书。历史代码与记录保持不变。
