# 2026-11-16：canonical q24的共同延伸检查

阅读入口：[数学手记](../../notes/codes-canonical-join.md)。

输入复用[昨日h.json](../2026-11-15/h.json)，其277条完整分类已有两套实现核验。固定B行、W嵌入、所有标签和窗口写在代码中。双偶前提见[二次型刚性](../../notes/codes-quadratic-rigidity.md)。

依次运行（Python 3.10及以上，仅标准库）：

```
python check.py > result.json
python compatibility.py > compatibility.json
python independent_equalities.py > independent_equalities_result.json
python independent_check.py > independent_result.json
python independent_join.py > independent_join_result.json
```

`check.py`用截面字符反演生成完整实际掩码，`compatibility.py`逐基方向检验共同延伸。`independent_check.py`用13/14列折半穷举独立核验18个余类域，`independent_join.py`直接检验2、3、5三个代表的组合。计时会随机器变化；比较时忽略CPU字段。无浮点、外部求解器或随机搜索。范围：固定B、canonical S、核0双偶规约；不覆盖其他取向。

[真实交流与校正](DIALOGUE.md) · [结果](result.json) · [兼容结果](compatibility.json) · [独立结果](independent_result.json)

独立折半实现从全部277标记重新核验259拒绝与18幸存，25.4 CPU秒；180个完整余类域的实际掩码与字符实现逐一相同。完整域约7.6秒，共同延伸检验小于0.1秒。普通与优化模式复算一致（不计计时）。
