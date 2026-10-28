# 2026-10-28：分割变换的真码控制与计数约束

阅读版：[先让检验器认出真码](../../notes/codes-split-controls.md)。

- `control_check.py`：两个显式生成矩阵，直接枚举对偶与分割变换的39个位置；精确分数，不依赖优化器。
- `control_result.json`：生成矩阵、位序、分割分布与全部检查结果。
- `category_cut.py`、`category_cut.json`：固定残余的核维数1七计数参数及同一(1,2)必要条件的仿射展开；不枚举整数域。
- `audit_controls.py`、`audit_result.json`：另写的多项式实现与独立参数核对。
- `EXCHANGES.md`：实际完整回复与提示；非自对偶控制、计数式不是Claude审阅结论。

在仓库根目录运行：

```sh
python history/2026-10-28/control_check.py
python history/2026-10-28/category_cut.py
python history/2026-10-28/audit_controls.py
```

计算预算为一分钟内的固定确定性控制；没有求解器、随机实验、新软件安装、目标矩阵搜索或全分支排除。旧日期证据不改写。来源和范围见[SOURCES](SOURCES.md)、[LIMITATIONS](LIMITATIONS.md)。
