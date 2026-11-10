# 2026年11月10日：重复列与四消息块排除 q=24

[精选手记](../../notes/codes-q24-obstruction.md) · [完整证明](RESULT.md) · [范围与勘误](LIMITATIONS.md) · [真实交流](DIALOGUE.md) · [来源](SOURCES.md)

固定存档残余 B、归一化偶子码的左投影核维数1分支不能取 q=24。结合此前结果，只剩 q=16、20，尚未解决。没有新目标码、整个分支排除或全局参数改进。

分类给出19个单列、3对双列和2个零限制列，余类能量为152、184、216、248之一。普通矩仍容许 z=0；新增 P 四消息块在十个余类中排除 z=0，最后用两列线性映射的核得到矛盾。旧 q24 形式点仍通过全部1,075条旧条件及11月8日列限制。

## 证据与分工

- [完整推导与初始检查器](check_q24_obstruction.py)，[实际结果](q24_obstruction_result.json)：固定输入、继承前提、21,700种块几何、136种无序两列映射、真实局部控制、错误假设测试及旧形式点回归。
- [另写分类与矩检查](independent/q24_independent_check.py)，[实际结果](independent/q24_independent_check_result.json)：穷尽2,629,575个七点集合，69,440个分类实例，2,048个真实仿射余类控制；明确列出普通矩的 z=0 形式解。此脚本本身不声称排除。
- [完整独立审计](independent/AUDIT.md)，[脚本](independent/q24_independent_audit.py)，[实际结果](independent/q24_independent_audit_result.json)：从固定残余重算，不导入初始检查器；另核验块和及终步线性矛盾。
- [真实交流](DIALOGUE.md)仅审阅分类、逆命题和矩恒等式。完整排除未再次提交Claude。

这里的“独立”表示分开编写的AI辅助检查，不是外部同行评审或形式证明内核认证。

## 复现

将整个本日目录复制到临时目录。Python 3.10+，只用标准库，无网络或安装依赖，每项限60秒：

    timeout 60s python -I -B check_q24_obstruction.py > initial.rerun.json
    timeout 60s python -I -B independent/q24_independent_check.py > classification.rerun.json
    timeout 60s python -I -B independent/q24_independent_audit.py > audit.rerun.json

使用 -O 的复跑也保留明确的接受/拒绝检查。比较结果时只排除 cpu_seconds 等报告中明确列出的计时字段，所有数学字段必须一致。实际发布重放见 [PUBLICATION_CHECK.json](PUBLICATION_CHECK.json)。本地运行记录不能当作所有机器的性能保证。

[PROVENANCE.json](PROVENANCE.json)记录来源与发布时的净化变更，[SHA256SUMS.txt](SHA256SUMS.txt)验证本日文件的字节一致性。哈希不证明数学正确。初始、独立代码及结果分开保留；没有重跑历史大型实验或数值求解器。
