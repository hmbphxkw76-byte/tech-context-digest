# AI 应用就业监测 · 指标登记册

> **格式**：md-table ｜ **用途**：存放 14 项监测指标的活值，供提示词运行前读取、运行后回写。
> **维护规则**：单元格内数值后附 `[来源, 年份]`；未核实项留空并注明"待核实"；prompt 模板内严禁填写活值。
> **初始值**：首轮运行前从基线报告 `reports/2026-11_baseline_report.html` 提取填入。

| # | 监测指标 | 口径/单位 | 优先数据源（英文） | 当前值 | 最近核实 |
|---|---|---|---|---|---|
| 1 | UAE AI 市场规模 & CAGR | 亿美元 / % | imarcgroup.com | 2025 年 7.057 亿 → 2026 年 8.598 亿 → 2034 年 43.873 亿美元，CAGR 21.84% [IMARC, 2026] | 2026-11 |
| 2 | 迪拜占 UAE AI 市场份额 | % | imarcgroup.com | 45.6%（2025）[IMARC, 2026] | 2026-11 |
| 3 | LinkedIn UAE 招聘率（同比） | % | linkedin-workforcereadiness.com | 2026-08 同比 -18%；2026-04 低点 -40% [LinkedIn, 2026] | 2026-11 |
| 4 | AI 工程岗需求增速 & 岗位占比 | % / % | linkedin-workforcereadiness.com | 同比 +232.4%；占 UAE 岗位发布 4.1% [LinkedIn, 2026] | 2026-11 |
| 5 | AI 工程人才集中度 & AI 素养人才增速 | % / % | linkedin-workforcereadiness.com | 人才集中度 +27.0%（占劳动力 0.75%）；AI 素养 +113.7% [LinkedIn, 2026] | 2026-11 |
| 6 | 阿联酋最快增长职业（AI 相关） | 排名 / 计数 | linkedin-workforcereadiness.com | 10 席中 4 席 AI 专属（AI Engineer 第 3、Head of AI 第 6、AI Consultant 第 8、Manager of AI 第 10）[LinkedIn, 2026] | 2026-11 |
| 7 | 国际申请占比 | % | linkedin-workforcereadiness.com | 37.6%（2026-08）vs 35.6%（2026-02）[LinkedIn, 2026] | 2026-11 |
| 8 | Michael Page AI/Data 最热岗位 | 排名 | michaelpage.ae | Agentic AI Engineer、Applied AI Engineer、Data Scientist / Applied Data Scientist、AI / ML Platform Engineer、AI Product Manager [Michael Page, 2026] | 2026-11 |
| 9 | Michael Page AI/Data 最缺技能 | 排名 | michaelpage.ae | Agentic AI & Multi-Agent Systems；Applied Data Science & Machine Learning；AI-Assisted Software Development；Production AI Engineering；AI Platform Engineering [Michael Page, 2026] | 2026-11 |
| 10 | 薪酬指南最新版次（AI/Data 分表） | 年版 | michaelpage.ae / charterhouseme.ae / hays.ae / cooperfitch.ae | Michael Page 2027；Charterhouse 2026；Hays GCC 2026；Cooper Fitch 2026（分表 gated，数值待核实）[各指南, 2026] | 2026-11 |
| 11 | AI 应用岗薪资抽样 | AED/月 | 待核实 | 待核实（公开指南 gated；相邻 AI 安全岗抽样 35,000–75,000 / 负责人 80,000–140,000）[Source: https://hiredeveloper.ae/employer-blog/how-to-hire-ai-security-engineers-dubai-after-meta-breach-7-steps, 2026] | 2026-11 |
| 12 | ILOE 费率 & 黄金签证门槛 | AED/月 / AED | iloe.ae / u.ae / icp.gov.ae | ILOE 每月 5 / 10（+5% VAT）；黄金签证门槛待核实（u.ae 页面未列 30,000 阈值）[Source: https://iloe.ae/pdf/Involuntary-Loss-of-Employment-Brochure-ILOE-V2.pdf, 2025；https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/golden-visa, 2026] | 2026-11 |
| 13 | 迪拜 AI 园区 / 自由区企业数 | 家 | dub.ai / difc.ae | DIFC Innovation Hub 2,000+ AI / 创新 / 科技企业；Dubai AI Campus 为 MENA 最大 AI 公司集群 [Source: https://www.difc.ae/ecosystem/innovation-hub, 2026；https://dub.ai/, 2026] | 2026-11 |
| 14 | 代表性 AI 应用雇主动态 | — | 各公司官网 / WAM | G42 23,000+ 员工 [FC-SEC-010]；Careem / Talabat / noon 待核实 | 2026-11 |

> 每次运行须逐项核对：未变动项保留本册值并注明"截至本次运行日期无更新"；变动项更新"当前值"与"最近核实"，并在报告"数据变更摘要"中体现。
