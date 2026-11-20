# 迪拜（阿联酋）AI 网安行业 · 指标登记册

> **格式**：md-table ｜ **用途**：存放本业务线 14 项监测指标的活值，供提示词（基线 / 年度刷新）运行前读取、运行后回写。
> **维护规则**：单元格内数值后附 `[来源, 年份]` 与来源编号 `[S-…]`；未核实项留空并注明「待核实」；prompt 模板内严禁填写活值。
> **初始值**：首轮运行前从基线报告 `content/tech/ai-security/industry-research/dubai/reports/2026-12_baseline_report.html` 提取填入（2026-12 基线期）。
> **来源登记**：`data/processed/tech/ai-security/industry-research/dubai/source_registry.json`（S-001–S-041，共 41 条）。
> **官方来源快照**：`data/raw/tech/ai-security/industry-research/dubai/`（含 `official_snapshot_manifest.json`）。
> **量化台账**：`quant_ai_cyber_market_size.csv`（同目录）。

| # | 监测指标 | 口径 / 单位 | 优先数据源（英文） | 当前值 | 最近核实 |
|---|---|---|---|---|---|
| 1 | MENA 信息安全终端支出 & 增速 | 亿美元 / 同比 % | gartner.com/newsroom | 2025 年 33 亿美元，同比 +14%（预测值 F）[Gartner, 2025] | 2026-12 |
| 2 | 阿联酋网安市场（Mordor 口径） | 亿美元 / CAGR | mordorintelligence.com | 2025 年 8.2 亿 → 2031 年 15.1 亿，CAGR 10.66% [Mordor, 2025] | 2026-12 |
| 3 | 阿联酋网安市场（GMI 口径，含硬件与服务） | 亿美元 / CAGR | gminsights.com | 2025 年约 34 亿，CAGR 12.29% [GMI, 2025] | 2026-12 |
| 4 | 全球 AI in cybersecurity 市场 | 亿美元 / CAGR | grandviewresearch.com | 2025→2033 年 315 亿 → 1,829 亿，CAGR 24.7% [Grand View, 2026] | 2026-12 |
| 5 | 市场集中度 CRn / 价值链分布 | — | 无公开可核实来源 | 未核验（不估算未文档化的集中度） | 2026-12 |
| 6 | DESC ISR 版本与控制域 | 版本 / 个 | desc.gov.ae | ISR v3.1，13 个控制域；适用所有迪拜政府实体及处理政府数据的第三方 [DESC, 2026] | 2026-12 |
| 7 | NCAP 未认证 MSSP 限制 | — | desc.gov.ae | 限制未认证 MSSP 服务关键基础设施 [DESC, 2026] | 2026-12 |
| 8 | G42 集团规模口径 | 人 / 国 | g42.ai | 23,000+ 员工、30 国 [G42, 2026] | 2026-12 |
| 9 | CPX 规模口径 | 人 / 客户 | cpx.net | 约 600 名专家、200+ 客户 [CPX, 2026] | 2026-12 |
| 10 | e& / Help AG 规模口径 | 人 | eand.com | 200+ SOC 分析师；迪拜 HQ + 阿布扎比双城 [e&, 2026] | 2026-12 |
| 11 | 微软–G42 投资 | 亿美元 | blogs.microsoft.com | 15 亿美元股权投资 + 10 亿美元开发者基金（2024-04）[Microsoft, 2024] | 2026-12 |
| 12 | Hub71 第 19 批创业池 | 家 / 亿美元 | hub71.com | 90% AI 原生、40 家初创、累计融资 2.96 亿美元（2026-10）[Hub71, 2026] | 2026-12 |
| 13 | 威胁国家化与泄露成本 | % / 万美元 | khaleejtimes.com | 日均约抵御 20 万次攻击；71.4% 追踪威胁行为体为国家背景 APT；中东平均数据泄露成本 792 万（全球 488 万）[Khaleej Times, 2026] | 2026-12 |
| 14 | 人才缺口与 AI 技能紧缺度 | % | isc2.org | 87% 阿联酋企业难以招募合格网安人员；AI 为最急需技能（41%）[ISC2, 2025] | 2026-12 |

> **口径并列不合并**：第 1 项（终端支出）≠ 第 2 / 3 项（含服务总收入）≠ 第 4 项（全球 AI in cybersecurity）；统计域与地域不同，禁止相加、静默择一或混算。
> **同源已核实资产**：第 1 / 6 / 7 / 8 / 9 / 10 / 11 / 13 / 14 项与 `content/tech/ai-security/security/dubai/` 业务线指标登记册同值；本册为行业研究型口径的独立维护副本，冲突时并列登记，不覆盖 security 线。

> 每次运行须逐项核对：未变动项保留本册值并注明「截至 {{CURRENT_DATE}} 无更新」；变动项更新「当前值」与「最近核实」，并在报告「数据变更摘要」中体现。
