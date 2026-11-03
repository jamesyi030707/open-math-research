# 2026-11-03：整除条件的双向证书

[研究手记](../../notes/codes-integrality-certificate.md)给出六条同余及其范围。完整1064行输入复用[10月29日数表](../2026-10-29/affine_coefficients.csv)，不另复制。

- `certificate.json`：常数列在内的 B=LA、A=RB 模64证书。
- `reduce_congruences.py`：可选重新生成器，整数模环消元，无变量域搜索。
- `verify_certificate.py`：只检查证书，不执行消元。
- `independent_verify.py`：另写检查器，不导入前两份程序，另核查真实对话的小例。
- `verification_result.json`、`independent_result.json`：实际执行结果。
- `DIALOGUE.md`：实际数学提示及完整最终答复转录；省略展示指令，无推理面板内容。
- `AUDIT.md`、`SOURCES.md`：审查范围和来源。

## 复现

Python3标准库。保留相邻10月29日输入目录，在仓库根运行：

    python -I -B history/2026-11-03/verify_certificate.py
    python -I -B history/2026-11-03/independent_verify.py

两者只读输入并输出JSON。不要加`-O`，检查依赖assert。每份核验在一分钟预算内完成。若重跑生成器，请使用临时副本，因为它会重写相邻certificate.json：

    python -I -B history/2026-11-03/reduce_congruences.py

生成结果已验证与存档字节一致。证书的48项前向和8512项反向标量恒等式分别验证。原数表通过旧生成器重新生成并字节比较一致；没有重跑大规模历史枚举。

六条只是等价整除条件，原边界和所有非负性要求仍在。旧形式点仍有八个负位置。不证明整数域可行、生成矩阵存在、分支不可能或参数界限改进。
