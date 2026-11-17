# AI 网络安全监测 · 指标登记册

> **格式**：md-table ｜ **用途**：存放 14 项监测指标的活值，供提示词运行前读取、运行后回写。
> **维护规则**：单元格内数值后附 `[来源, 年份]`；未核实项留空并注明"待核实"；prompt 模板内严禁填写活值。
> **初始值**：首轮运行前从基线报告 `sources/2026-11_baseline_report.md` 提取填入。

| # | 监测指标 | 口径/单位 | 优先数据源（英文） | 当前值 | 最近核实 |
|---|---|---|---|---|---|
| 1 | MENA 信息安全支出 & 增速 | 亿美元 / 同比 % | gartner.com/newsroom | 33 亿美元，同比 +14% [Gartner, 2025] | 2026-11 |
| 2 | 阿联酋网安市场规模 & CAGR | 亿美元 / % | mordorintelligence.com / gminsights.com | 8.2 亿→15.1 亿，CAGR 10.66% [Mordor, 2025]；34 亿，CAGR 12.29% [GMI, 2025] | 2026-11 |
| 3 | 日均攻击量 / 国家背景占比 | 次/日 / % | khaleejtimes.com / uaecsc.gov.ae | 约 20 万次/日；71.4% 国家背景 [Khaleej Times, 2026] | 2026-11 |
| 4 | ISC2 人力研究（技能缺口/AI 占比） | % / 人数 | isc2.org/Insights | AI 为最缺技能（41%）；88% 遭遇安全后果 [ISC2, 2025] | 2026-11 |
| 5 | 五大薪酬指南最新年版网安分表 | 年版 | hays.ae / roberthalf.ae / cooperfitch.ae / michaelpage.ae / charterhouseme.ae | 2025 年版（Cooper Fitch、Charterhouse 已核实） | 2026-11 |
| 6 | AI 安全岗薪资抽样 | AED/月 | hiredeveloper.ae / gulftalent.com / bayt.com | 资深 5.5–7.5 万 [hiredeveloper.ae, 2026] | 2026-11 |
| 7 | Numbeo 迪拜 vs 阿布扎比生活成本 | 含租等效月度 | numbeo.com | 迪拜 26,000 vs 阿布扎比 22,175 [Numbeo, 2026] | 2026-11 |
| 8 | ILOE 费率 & 黄金签证门槛 | AED/月 / AED | iloe.ae / u.ae / icp.gov.ae | ILOE 每月 5/10（+5% VAT）；黄金签证基本月薪 ≥30,000 [ILOE/u.ae, 2026] | 2026-11 |
| 9 | Stargate UAE 状态 | — | openai.com / coloprice.com | 在建，首批 200MW 计划 2026 上线 [OpenAI, 2025] | 2026-11 |
| 10 | GISEC / GITEX 最新届次 | 日期 | gisec.ae / gitex.com | GISEC 2026-09-16–18；GITEX 2026-12-07–11 [GISEC/GITEX, 2026] | 2026-11 |
| 11 | G42/Core42/CPX/e&/Moro Hub 动态 | — | 各公司官网 / WAM | G42 23,000+ 员工；CPX ~600 专家 [各公司官网/WAM, 2026] | 2026-11 |
| 12 | OWASP LLM Top 10 / MITRE ATLAS 版本 | 版本/计数 | genai.owasp.org / atlas.mitre.org | LLM Top 10（2025）；ATLAS 16 战术/221 技术/44 缓解 [OWASP/MITRE, 2026] | 2026-11 |
| 13 | 新发 AI 安全证书 & 本地考点 | — | giac.org / isc2.org / comptia.org / eccouncil.org / sans.org | GIAC GAIPS/GASAE；CompTIA SecAI+；ISACA AAIA/AAIR/AAISM [各发证方, 2026] | 2026-11 |
| 14 | DESC ISR v3.1 / ISR 审核员计划 | 版本/控制域 | desc.gov.ae | ISR v3.1（13 控制域）；2026-09 发布 ISR 审核员认证 [DESC, 2026] | 2026-11 |

> 每次运行须逐项核对：未变动项保留本册值并注明"截至本次运行日期无更新"；变动项更新"当前值"与"最近核实"，并在报告"数据变更摘要"中体现。
