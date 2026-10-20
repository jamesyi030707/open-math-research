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

## 2026-10-14：已知纠错码与局部证书

先把 `history/2026-10-14/independent` 复制到临时工作目录，再在副本中运行以下存档证书检查入口：

    python3 -I -B check_certificates.py
    python3 -I -B coverage_extension_check.py
    python3 -I -B four_column_circuit_check.py

这些入口只依赖 Python 标准库及同目录中的矩阵和证书。具体范围、生成器与原始核查日志见 [当日说明](history/2026-10-14/README.md)及 [独立核查说明](history/2026-10-14/independent/README.md)。生成器、部分证书检查器和参考程序会重写产物、时间日志或检查清单；运行时应使用临时副本，重新生成后须重新计算哈希。集成归档时未重复运行研究测试。

上述局部证书只涉及该已知基准码的至多四列替换，不证明全局不存在；当日精确 Collatz 参考函数不认证旧 C 程序，也不代表重跑 J92。

## 其他依赖与历史限制

C 代码使用 GCC/Clang 的 unsigned __int128 扩展；原 Claude 悖常轨迹检查器需要 NumPy。部分驱动从环境变量取编译器产物路径；日期目录保留历史文件分布，不能假设单目录包含每个阶段全部依赖。

10 月 13 日驱动引用若干旧证书、qmax 文件与旧日志；仅下载/保留了选定产物，部分 J65/J72/J80 证书未在本包取得。原完整流水线并非开箱即跑。不得以现有 J92 命中列表取代这些缺失的完整性依赖。可先使用上面的已备齐独立检查。

10 月 11 日独立检查的旧绝对路径已改为本地 reference/paradox_cert_J92_previous.json，保留其后备逻辑。其他少量原执行路径改为相对目录；参见 PROVENANCE.json。所有发生变化的文件已记录原始与公开 SHA256。历史日志中的源哈希指原始版本，可能不同于脱敏后的源码。

SHA256SUMS.txt 校验本公开包除自身以外的全部文件。它验证字节一致性，不证明数学正确性或软件安全。

## 2026-10-15：短谱证书检查

将 `history/2026-10-15/independent` 复制到临时目录，在副本中运行：

    python3 -I -B codim2_compact_verify.py

只依赖 Python 3 标准库和同目录矩阵。直接检查全部 2,047 个非零字符和与 125 个等号情形，无需重新枚举 698,027 个子空间。勿使用禁用 assert 的 -O。完整枚举及不同实现的历史日志保留于 [当日记录](history/2026-10-15/README.md)。集成发布未重复大枚举。

## 2026-10-16：BCH 母码与共同 Walsh 模型

将 `history/2026-10-16/independent` 复制到临时目录，在副本中运行：

    python3 -I -B verify.py
    python3 -I -B certificate.py
    python3 -I -B verify_rm_model.py

Python 3.10+，仅标准库；不要使用禁用 assert 的 -O。程序会重写同目录结果。第一个程序构造 1,024 个码字并检查全部必要整数分布；第二个检查端点及整斜率；第三个核查 RM 包含、互补基、七个 bent 二次函数和三个固定向量的距离接口。模型可行性没有求解，三个接口样例不是搜索。参见 [当日说明](history/2026-10-16/README.md)。

## 2026-10-17：精确模型、商空间与 LP 审查

将 `history/2026-10-17` 整个目录复制到临时目录，在副本的 `independent` 中运行：

    python3 -I -B model_check.py
    python3 -I -B quotient_check.py
    python3 -I -B audit_lp.py
    python3 -I -B literature_mapping.py

检查程序只用标准库，不搜索余类；保留相邻 `claude` 目录以供 LP 审查。程序会重写本地结果，不要使用禁用 assert 的 -O。审查覆盖全部 1,024 个标量界、奇偶条件、变量类型和十位信息集规范化；不是不可行证明。`solve_scipy.py` 只是语法检查过的可选求解器入口，不属于上述已核查运行；集成未运行任何 MILP。原日志的 59.6 进程 CPU 秒及 infeasible 是未认证报告，单工作线程与控制实验向量均未独立确认。详见 [验证边界](history/2026-10-17/LIMITATIONS.md)。

## 2026-10-18：精确 OPB 输入

[本日独立复现说明](history/2026-10-18/independent/README.md)提供生成器、逐项审查及阳性对照入口。保留原59变量与压缩57变量模型。复跑在临时副本中执行；不需运行完整实例求解器。这些审查证明模型编码与所述固定问题等价，不证明完整实例不可满足。

## 2026-10-19：联合第四矩与设计约束

[完整推导和标准库检查器](history/2026-10-19/independent/README.md)核查固定母码的二次结构、63个导数秩、1,008个四元块及全部点对度数。请在临时副本运行，程序会写出JSON。四个向量仅为实现对照；七种必要分布的普遍结论来自所列代数证明，不来自抽样，也不代表已构造七个码。

## 2026-10-20：二次函数邻域排除

[本日证明、代码与复现说明](history/2026-10-20/README.md)提供三个独立标准库检查器：MacWilliams审计、32,768个齐次二次型的极化秩枚举、136个半径13边界谱的精确逆变换核验。请在临时副本运行，程序会覆盖相邻报告。最终至少15的界限须同时阅读基础证明和半径13补充证明；136项检查仅佐证一般的四点带符号平均论证。无完整目标函数空间搜索。
