# 2026-11-15：q=24的完整局部h标记

先读[手记](../../notes/codes-kernel-zero-q24.md)。正式结论限于标准S标签的277个局部限制；不排除q=24或全局目标码。

- [证明与完整性](H_CLASSIFICATION.md)：复用旧S分类，新增h标记分类。
- [第二实现与局部轨道说明](REVIEW.md)。
- [真实交流与纠错](DIALOGUE.md)。
- `check_h.py` / `h.json`：按多重集与双列预算枚举10,861项；直接重算64个重量。
- `local.py` / `local.json`：独立按27个实际位置枚举小侧，再合并同标签坐标置换。
- `orbits.py` / `orbits.json`：144个局部稳定子作用得到9轨道；单实现补充结果。
- 各程序均保留普通与`-O`输出；`validate.py`逐一比较完整277向量而不只是总数，并核对模式一致性与破坏对照。

仅Python标准库。从本目录运行：

```sh
python check_h.py > h.json
python -O check_h.py > h_optimized.json
python local.py > local.json
python -O local.py > local_optimized.json
python orbits.py > orbits.json
python -O orbits.py > orbits_optimized.json
python validate.py
sha256sum -c SHA256SUMS.txt
```

最后一项哈希用于核对存档原文件；重跑产生不同CPU计时后，输出文件哈希会自然改变。运行比较忽略计时。每项预算60秒，实际均远低于预算；无随机求解器、浮点判断或外部软件包。

来源：Grassl二元线性码表[64,11]条目（2026-11-15实际读取，26–27），仓库11月10日S分类、11月12日重复列预算、11月14日q28排除。新计算不重跑历史排除，不代表穷尽文献的新颖性审查。
