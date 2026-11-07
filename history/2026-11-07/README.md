# 2026-11-07：消息子空间排除q=0见证

[精选手记](../../notes/codes-subspace-obstruction.md)。固定残余、左投影核维数1分支的新必要条件为q≥16，排除11月5日形式见证的所有标签实现。旧模型的形式可行性仍成立，整个分支和全局问题未决。

## 证据

- [完整证明](RESULT.md)、[原始残余基](residual_candidate.json)。
- [初始精确检查器](check_subspace.py)、[实际结果](result.json)、[实际日志](run.log)。
- [分开编写的完整六维检查](audit_subspace.py)、[结果](audit_result.json)。
- [另写发布核验](audit_publication.py)、[结果](publication_audit_result.json)。
- [真实数学交流](DIALOGUE.md)、[结论边界](LIMITATIONS.md)、[来源](SOURCES.md)。
- [溯源](PROVENANCE.json)、[公开检查](PUBLIC_SAFETY_CHECK.json)、[哈希](SHA256SUMS.txt)。

## 复现

将本目录复制到临时目录，在副本运行：

```sh
timeout 60s python -I -B check_subspace.py
timeout 60s python -I -B audit_subspace.py
timeout 60s python -I -B audit_publication.py
```

仅Python标准库，不需安装、求解器或网络。不要使用禁用assert的-O。第一项重写result.json，cpu_seconds随机器变化，其余数学字段应一致。后两项输出JSON，可与存档比较；具体核验范围见各程序。发布阶段重跑初始检查器，数学字段完全一致；另写发布核验通过。没有重复旧搜索，也没有求解剩余q值的可行性。
