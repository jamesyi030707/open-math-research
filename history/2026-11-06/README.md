# 2026-11-06：同一个重量分布，不同的消息标签

[精选手记](../../notes/codes-message-realization.md)。本日给出指定消息重量函数的精确列重数判据，以及保留完整分割分布、却不能实现的错误标签对照。没有排除11月5日七计数见证，也没有新目标码或参数界限。

## 证据

- [证明与完整对照](RESULT.md)、[标准库检查器](check_message_columns.py)、[原实际结果](message_columns_result.json)。
- [分开编写的发布核验](audit_publication.py)、[实际核验结果](publication_audit_result.json)。
- [真实交流及编辑纠正](DIALOGUE.md)、[范围与勘误](LIMITATIONS.md)、[来源](SOURCES.md)。
- [溯源](PROVENANCE.json)、[公开检查](PUBLIC_SAFETY_CHECK.json)、[哈希](SHA256SUMS.txt)。

## 复现

将本目录复制到临时目录后，分别运行：

```sh
timeout 60s python -I -B check_message_columns.py
timeout 60s python -I -B audit_publication.py
```

只依赖Python标准库，不使用求解器。第一个脚本会重写相邻结果JSON；数学字段应一致，cpu_seconds会变化。第二个脚本读取结果，用另一种蝶形Walsh变换与直接列枚举复核。不要用禁用assert的-O。发布阶段在临时副本重跑第一个程序，除计时外所有字段一致；第二个程序另行运行通过。无需重跑历史搜索。
