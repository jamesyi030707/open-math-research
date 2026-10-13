# 可复现说明

先读 ERRATA.md。源代码是研究原型，有已知输入/溢出/依赖问题；不要不加检查地对任意大 J 运行。历史日志是此前真实运行记录，本次归档不将它们冒充新运行。

## 轻量独立检查

Python 3 标准库：在 history/2026-10-08 目录运行：

    python3 -I -B dot_independent_symbolic_k12_20261008.py
    python3 -I -B claude_check_cert_k12_20261008.py claude_cert_k12_20261008.json --selftest --N=200000

在 history/2026-10-11 目录运行：

    python3 -I -B audit_candidate_output_j92.py claude_original/paradox_cert_J92.json --selftest

在 history/2026-10-13 目录运行：

    python3 -I -B independent_exact_audit.py

最后一项完整枚举 J46、核查 J92 命中与必要路径，不完整枚举 J92。不要用 Python -O，部分检查依赖 assert。检查器可能写出日志/JSON；建议复制到临时工作目录后运行，以免改变历史文件。

## 其他依赖与历史限制

C 代码使用 GCC/Clang 的 unsigned __int128 扩展；原 Claude 悖常轨迹检查器需要 NumPy。部分驱动从环境变量取编译器产物路径；日期目录保留历史文件分布，不能假设单目录包含每个阶段全部依赖。

10 月 13 日驱动引用若干旧证书、qmax 文件与旧日志；仅下载/保留了选定产物，部分 J65/J72/J80 证书未在本包取得。原完整流水线并非开箱即跑。不得以现有 J92 命中列表取代这些缺失的完整性依赖。可先使用上面的已备齐独立检查。

10 月 11 日独立检查的旧绝对路径已改为本地 reference/paradox_cert_J92_previous.json，保留其后备逻辑。其他少量原执行路径改为相对目录；参见 PROVENANCE.json。所有发生变化的文件已记录原始与公开 SHA256。历史日志中的源哈希指原始版本，可能不同于脱敏后的源码。

SHA256SUMS.txt 校验本公开包除自身以外的全部文件。它验证字节一致性，不证明数学正确性或软件安全。
