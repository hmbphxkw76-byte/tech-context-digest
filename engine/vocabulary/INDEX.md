# 词汇库索引（vocabulary）

> 由 `script/vocab_tool.py index` 自动生成，请勿手工编辑。生成时间：2026-11-14T13:24:40

## 主题总览

| 主题 | 名称 | ID 前缀 | 词条数 | 分类分布 | 词库版本 | 存储路径 | 最近更新 |
|---|---|---|---|---|---|---|---|
| ai-security | AI 安全 | AIS | 49 | 攻击技术 12 / 防御与检测 11 / 框架与标准 8 / 基准与评估 6 / 组织与岗位 5 / 认证与资质 4 / 工具与平台 3 | v1.3 | data/ai-security/terms.md | 2026-11-13 |
| financial-markets | 金融市场 | FIN | 49 | 宏观与经济指标 10 / 金融工具与产品 10 / 市场机制与交易 8 / 金融机构与组织 8 / 估值与风险 7 / 监管与政策 6 | v1.1 | data/financial-markets/terms.md | 2026-11-13 |
| cybersecurity | 网络安全 | CYB | 153 | 防御与安全运营 47 / 网络攻击技术 44 / 密码与身份认证 20 / 框架与合规 19 / 认证与岗位 12 / 漏洞与漏洞管理 11 | v1.4 | data/cybersecurity/terms.md | 2026-11-13 |
| economy | 经济 | ECO | 48 | 经济体与国家 22 / 经济概念 16 / 区域经济组织 10 | v1.3 | data/economy/terms.md | 2026-11-13 |
| ai-agent | AI Agent 与大模型 | AAG | 73 | 模型与厂商 19 / 应用与产品 15 / Agent 技术与框架 14 / 编码工具与 IDE 13 / 概念与评估 12 | v1.2 | data/ai-agent/terms.md | 2026-11-13 |

合计：5 个主题，372 条词条。

## 上层对接

- 结构化导出：各主题 `data/<topic>/exports/` 下的 JSON / JSONL / CSV（数据契约见 README 第六节）。
- 检索建议：以词条 ID 为主键，别名与标签作为索引字段，分类作为过滤面。
