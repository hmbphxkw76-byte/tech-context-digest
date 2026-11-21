# 迪拜（阿联酋）AI 应用行业 · 指标登记册

> **格式**：md-table ｜ **用途**：存放本业务线 14 项监测指标的活值，供提示词（基线 / 月度刷新）运行前读取、运行后回写。
> **维护规则**：单元格内数值后附 `[来源, 年份]` 与来源编号 `[S-…]`；未核实项留空并注明「待核实」；prompt 模板内严禁填写活值。
> **初始值**：首轮运行前从基线报告 `content/tech/ai-application/industry-research/dubai/reports/2026-11_baseline_report.html` 提取填入（2026-11 基线期）。
> **来源登记**：`data/processed/tech/ai-application/industry-research/dubai/source_registry.json`（待建）。
> **官方来源快照**：`data/raw/tech/ai-application/industry-research/dubai/`（待建）。

| # | 监测指标 | 口径 / 单位 | 优先数据源（英文） | 当前值 | 最近核实 |
|---|---|---|---|---|---|
| 1 | UAE AI 市场规模（全口径，IMARC） | 亿美元 / CAGR | imarcgroup.com | 2025 年 7.057 亿 → 2026 年 8.598 亿 → 2034 年 43.873 亿美元，CAGR 21.84% [IMARC, 2026] | 2026-11 |
| 2 | UAE AI 市场结构（IMARC） | % | imarcgroup.com | 软件 48.7%、窄 / 弱 AI 78.6%、迪拜占全国市场 45.6%（2025）[IMARC, 2026] | 2026-11 |
| 3 | 全球企业 AI 市场（Grand View） | 亿美元 / CAGR | grandviewresearch.com | 2024 年 239 亿 → 2030 年 1,552 亿美元，CAGR 37.6% [Grand View, 2026] | 2026-11 |
| 4 | 全球 AI 市场（TBRC） | 亿美元 / CAGR | thebusinessresearchcompany.com | 2025 年 2,453.4 亿 → 2030 年 9,196.2 亿美元，CAGR 30.4% [TBRC, 2026] | 2026-11 |
| 5 | UAE AI 市场（Mordor / GMI 口径） | 亿美元 / CAGR | mordorintelligence.com / gminsights.com | 待核实（未取得可核实英文页面，不补值、不外推） | 2026-11 |
| 6 | Dubai Universal Blueprint for AI 目标 | 亿 AED/年 / % | dub.ai | 每年为迪拜经济贡献 1,000 亿 AED（约 272 亿美元）、生产力提升 50% [dub.ai, 2025] | 2026-11 |
| 7 | 迪拜 AI 战略举措 | — | dub.ai | Dubai AI Campus（MENA 最大 AI 公司集群）、Dubai AI Seal（可信 AI 公司认证）、首席 AI 官机制 [dub.ai, 2025] | 2026-11 |
| 8 | 迪拜政府 AI 部署 | 人 / 个 | digitaldubai.ae | 22 名首席 AI 官、100+ 在用 AI 用例（2025，媒体转述，待以 Digital Dubai 官方报告复核）[Digital Dubai, 2025] | 2026-11 |
| 9 | G42 集团规模口径 | 人 / 国 | g42.ai | 23,000+ 员工、30 国 [G42, 2026] [FC-IND-003] | 2026-11 |
| 10 | Core42 主权云状态 | — | core42.ai / news.microsoft.com | 基于 Microsoft Azure 的主权公有云 + 签名私有云；FAB 合作（2024-03）[Core42 / Microsoft, 2024] | 2026-11 |
| 11 | 微软–G42 投资 | 亿美元 | blogs.microsoft.com | 15 亿美元股权投资 + 10 亿美元开发者基金（2024-04）[Microsoft, 2024] | 2026-11 |
| 12 | Hub71 创业池 | 家 / 亿美元 | hub71.com | 第 19 批（2026-10）90% AI 原生、40 家初创、累计融资 2.96 亿美元 [Hub71, 2026] [FC-IND-005] | 2026-11 |
| 13 | Moro Hub 主权 AI 平台 | — | morohub.ae | DEWA 子公司；全栈主权 AI 平台（区域产品细节待核实）[Moro Hub, 2026] | 2026-11 |
| 14 | Stargate UAE 状态 | GW | openai.com | 阿布扎比园区规划 5GW、一期 1GW（运营状态待官方确认）[OpenAI, 2025] | 2026-11 |
| 15 | 云厂商 UAE 区域 AI 服务 | — | learn.microsoft.com / aws.amazon.com | Azure UAE North / UAE Central 区域；AWS 中东（阿联酋）区域（区域服务清单待核实）[Microsoft / AWS, 2026] | 2026-11 |

> **口径并列不合并**：第 1 / 2 项（UAE 全口径 AI）≠ 第 3 项（全球企业 AI）≠ 第 4 项（全球 AI 总体）；统计域与地域不同，禁止相加、静默择一或混算。
> **同源已核实资产**：第 9 / 12 项与 `content/tech/ai-security/industry-research/dubai/` 业务线指标登记册同值；本册为 AI 应用行业口径的独立维护副本，冲突时并列登记，不覆盖 ai-security 线。

> 每次运行须逐项核对：未变动项保留本册值并注明「截至 {{CURRENT_DATE}} 无更新」；变动项更新「当前值」与「最近核实」，并在报告「数据变更摘要」中体现。
