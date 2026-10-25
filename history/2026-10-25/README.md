# 2026-10-25：最小字的二次型刚性

先读[精选手记](../../notes/codes-quadratic-rigidity.md)。

- [精确核验器](verify_quadratic_rigidity.js)：无依赖、无网络、无随机搜索。可用支持BigInt的Node.js运行。
- [结果与55个独立消息证书](result.json)。
- [独立审阅](AUDIT.md)、[来源及范围](SOURCES.md)、[逐文件来源](PROVENANCE.json)。
- 输入复用[10月24日残余基](../2026-10-24/independent/residual_candidate.json)，未改写该历史数据。

实际运行方式为JavaScript隔离环境执行同一脚本正文并捕获输出；本日未执行Node.js命令行。一次记录的计算墙钟为13毫秒，仅是小型核验的环境记录，不作性能结论。没有新Claude对话或回复；没有新码、全局排除或新颖性主张。
