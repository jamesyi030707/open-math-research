# 2026年11月13日：两个局部控制的外部余类障碍

[精选手记](../../notes/codes-local-extension-obstruction.md) · [完整证明](RESULT.md) · [真实交流与校正](DIALOGUE.md) · [几何检查](GEOMETRY.md)

仅排除11月12日两个具体带标签W限制的延伸。每个证书由八条重量等式组成，迫使一个±1符号为零。不排除所有q=28局部限制、核维数0分支或全局目标码。

## 证据入口

- [整数检查](integer_verify.py)：直接核对八个残余重量与全部27列的组合系数。
- [分开编写的审核](review.py)、[结果](review_replay.json)与[优化结果](review_optimized_replay.json)：生成行、64个局部字、秩、证书、损坏测试及实际外部偏移对照。
- [几何程序](check_geometry.py)、[发布重放](check_geometry_replay.json)与[优化重放](check_geometry_optimized_replay.json)：十个非平坦截面、640个单列变换及真正平坦集对照。
- [原始可见答复](CLAUDE_REPLY.md)与[实际提示](PROMPT.txt)：仅一轮。未让Claude审阅独立证书，未执行其全部仿射3flat枚举建议。

## 复现

Python标准库，无安装依赖。将本目录复制到临时目录后，每项限60秒：

    timeout 60s python -I -B integer_verify.py
    timeout 60s python -I -B review.py
    timeout 60s python -I -B check_geometry.py

对每项增加`-O`复跑。含CPU时间的结果仅去除cpu_seconds后比较，其他字段保持一致。核验是AI辅助的分开实现，不是外部同行评议或形式证明内核认证。

## 来源与适用范围

- 当前读取的[Grassl二元[64,11]参数条目](https://www.codetables.de/BKLC/BKLC.php?k=11&n=64&q=2)仍列下界26、上界27。下界构造与上界引文归原作者；未镜像数据库，抓取日不代表源站修订日，也不是全面查新。
- 固定B与局部控制继承[11月12日档案](../2026-11-12/README.md)，输入来源署名不变。
- 本日新推导、独立代码与编辑文字为AI协作研究记录；遵守仓库既有许可说明，不对第三方内容另行宣称所有权。
- [校验清单](SHA256SUMS.txt)与[逐文件公开检查](PUBLIC_SAFETY_CHECK.json)。
