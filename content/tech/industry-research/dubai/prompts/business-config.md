# 迪拜（阿联酋）AI 网安行业 · 业务专属配置（business-config）

> **定位**：本文件是 `content/tech/industry-research/dubai` 业务线的**单一业务事实源**：运行变量固定值、来源优先级实例化、受众定位、术语口径、触发器、指标追踪清单、已修正事实清单全部集中于此。周期提示词（基线 / 年度刷新）引用本文件，业务参数只在这里维护一份。
>
> **继承声明（四层体系）**：周期提示词 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [类型模板](../../../../../engine/templates/industry-research/)（行业深度研究型）× 本文件。通用层修改自动对本业务线生效；本文件修改只影响本业务线。冲突时以周期提示词 ＞ 本文件 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、运行变量固定值

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = AI 网安行业
{{REPORT_TYPE}}          = industry-research
{{BASELINE_DATE}}        = 2026-12（首份基线报告完稿日期）
{{REGISTRY_PATH}}        = data/processed/tech/industry-research/dubai/ai_cybersecurity_indicator_registry.md（运行期创建，基线可缺）
{{REGISTRY_FORMAT}}      = md-table
{{SOURCE_REGISTRY_PATH}} = data/processed/tech/industry-research/dubai/source_registry.json
{{BASELINE_REPORT_PATH}} = reports/2026-12_baseline_report.html
{{FRESHNESS_PRIORITY}}   = 近 12 个月内数据优先；超过 24 个月须标注年份并谨慎使用
{{SOURCE_LANGUAGE_RULE}} = 仅英文（全部取自英文网站，严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/industry-research/dubai
```

**类型与周期**：`industry-research`（行业深度研究型），周期 `baseline`（九节固定骨架）与 `annual`（年度刷新，结构逐字继承基线）。模板入口：`engine/templates/industry-research/prompt-baseline-setup-template.md`。

**输出格式**：canonical 富样式自包含 HTML 为主交付物，落盘 `reports/{{周期}}.html`；md 源稿存 `sources/` 同名存档，不参与 `md2html.py` 自动转换（防止覆盖手工渲染）。

## 二、受众定位

面向关注「迪拜（阿联酋）AI 网安行业」的产业研究与决策读者，兼具行业分析与市场进入参考视角。报告保持**中性全景刻画**：不给投资评级、不出具 Go/No-Go 决策建议（那是投资分析与尽调型、可行性型的边界）；趋势判断一律标「推断」，多口径规模数据并列不合并。

## 三、术语口径区分（表格与正文中不得混用）

- **AI 网安行业** = AI 系统安全（模型 / Agent / 数据 / 供应链安全）+ AI 用于安全运营（智能 SOC、威胁情报、MDR/XDR）+ 网安市场中 AI 相关支出与采购；**不含**无 AI 维度的传统网安市场测算。
- MENA 信息安全**终端支出**（Gartner）≠ 阿联酋市场**含服务总收入**（Mordor / GMI），口径不同不可直接比较。
- **全球口径**（如全球 AI in cybersecurity 市场）与**本地口径**（迪拜 / 阿联酋）必须分列，禁止混算。
- 招聘机构抽样 ≠ 官方或权威机构口径（前者标注「抽样」并谨慎引用）。
- 汇率固定：1 USD = 3.6725 AED（钉住）。

## 四、来源优先级（通用基座第四节的实例化，冲突时报双份并标注）

① 阿联酋/迪拜政府官方（u.ae、desc.gov.ae、tdra.gov.ae、mediaoffice.ae、icp.gov.ae、WAM 英文、各自由区官网）
＞ ② 国际权威组织与分析机构（ISC2、ISACA、Gartner、IDC、SANS/GIAC、MITRE、OWASP、NIST、Mordor Intelligence、Global Market Insights）
＞ ③ 头部薪酬指南与招聘平台抽样（Hays、Michael Page、Cooper Fitch、Charterhouse；LinkedIn、Bayt、GulfTalent、foundit Gulf——仅作市场信号）
＞ ④ 英文行业/主流媒体（Khaleej Times、The National、Gulf News、Zawya、Reuters——只用于发现线索，数值须回官方/原始页校验）
＞ ⑤ 同源已核实资产：`content/tech/security/dubai/` 业务线的基线报告、md 源稿与指标登记册，以及 `content/tech/weekly-roundup/reports/2026-11-13_weekly.html`（全球趋势转引，须标注「经周报转引」）。

## 五、重大事件触发器（事件 → 受影响模块）

| 触发事件 | 受影响模块 |
|---|---|
| GITEX Global / GISEC Global 新一届举办（日期、主题、官方发布） | 产业链、头部玩家、趋势 |
| 阿联酋/迪拜新网络安全法规或 AI 安全政策生效（含 ISR 修订、NCAP、SBOM、PQC 计划） | 驱动因素、产业链下游、趋势 |
| Stargate UAE / 主权云（Core42 等）建设或运营状态更新 | 产业链上游、驱动因素 |
| ISC2《Cybersecurity Workforce Study》或 Gartner 中东安全支出预测更新 | 驱动因素、趋势 |
| 头部薪酬指南或招聘机构薪资抽样更新 | 头部玩家、驱动因素 |
| OWASP / MITRE / NIST 框架版本更新 | 产业链中游、趋势 |

## 六、指标追踪表（活值维护于 {{REGISTRY_PATH}}）

| # | 监测指标 | 口径/单位 | 优先数据源（英文） |
|---|---|---|---|
| 1 | MENA 信息安全支出 & 增速 | 亿美元 / 同比 % | gartner.com/newsroom |
| 2 | 阿联酋网安市场规模 & CAGR | 亿美元 / % | mordorintelligence.com / gminsights.com |
| 3 | 日均攻击量 / 国家背景占比 | 次/日 / % | khaleejtimes.com / uaecsc.gov.ae |
| 4 | ISC2 人力研究（技能缺口/AI 占比） | % / 人数 | isc2.org/Insights |
| 5 | Stargate UAE 状态 | — | openai.com / coloprice.com |
| 6 | GISEC / GITEX 最新届次 | 日期 | gisec.ae / gitex.com |
| 7 | G42/Core42/CPX/e&/Moro Hub 动态 | — | 各公司官网 / WAM |
| 8 | OWASP LLM Top 10 / MITRE ATLAS 版本 | 版本/计数 | genai.owasp.org / atlas.mitre.org |
| 9 | DESC ISR v3.1 / ISR 审核员计划 | 版本/控制域 | desc.gov.ae |

> 首份基线运行后回写登记册；基线期先引用 `data/processed/tech/security/dubai/ai_cybersecurity_indicator_registry.md` 的已核实活值，不新造数值。

## 七、已修正事实清单（基线锚，防回退；无来源不得追加）

```
- ❌ 不得再称"Black Hat MEA 在阿布扎比"——该会议 2025 年起已在沙特利雅得举办。[Source: https://www.blackhatmea.com/about-us/key-information, 2026]
- ❌ 不得再称 ILOE 失业险"每周 AED 5/10"——实为每月 AED 5（基本≤1.6万）/ AED 10（基本>1.6万）+5% VAT。[Source: https://www.iloe.ae/pdf/Involuntary-Loss-of-Employment-Brochure-ILOE-V2.pdf, 2025]
- ❌ 不得再将 CPX 与 DarkMatter 绑定——CPX 为 2022 年成立的 G42 子公司，与 DarkMatter→Digital14 系不同实体。[Source: https://www.cpx.net, 2025]
- ❌ 不得再引用微软–G42「152 亿美元」broad 投资计划——经复核未获英文权威来源证实（微软官方仅确认 2024.4 的 15 亿美元股权注资与 10 亿美元开发者基金）。[Source: https://blogs.microsoft.com/blog/2024/04/15/microsoft-and-g42-partner, 2024]
- ❌ 不得将 Gartner（终端支出）与 Mordor/GMI（含服务总收入）口径直接比较或合并——并列呈现并标注口径。
- ❌ 不得估算本报告未文档化的集中度（CRn）或价值链分布数值——无公开可核实来源时标注「未核验」。
```

## 八、基线九节结构固化锚

基线报告九节结构为该业务线固化锚，后续报告逐字继承：

1. 执行摘要｜2. 研究范围与方法｜3. 产业链图谱｜4. 市场规模与格局｜5. 头部玩家与竞争格局｜6. 驱动因素与风险｜7. 趋势判断（推断）｜8. 数据治理与局限｜9. 参考来源清单

---

## 信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：已核验 / 部分核验 / 推断 / 假设；决策摘要仅引用已核验 + 部分核验；新增信息模块「本期新增 X / 修正 Y / 无变化 Z / 假设核验进度 k/n」。
- **事实卡片**：本业务线为共享事实域（IND），正文以 `[FC-IND-…]` 引用 `engine/fact_cards/industry_research_fact_cards.json`。
- **决策卡与行动协议**：核心判断输出决策卡；行动项五要素 + 三档优先级（规范：`engine/templates/decision-delivery-spec.md`）。
- **阈值校准**：首次中期回测 2027-06；校准完成前信号灯标注「预校准（ex-ante）」。
- **场景切片**：主场景 **投资决策**；次场景 **政策制定**。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」。
- **盲区**：P0 四类（就业 / 收入 / 空置 / 竣工）优先消号。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-12 | 初始版本 | 建立 `content/tech/industry-research/dubai` 业务线；四层继承体系指向 `engine/templates/industry-research/`（行业深度研究型）；定义 {{REGION}} / {{TOPIC}}、来源优先级、触发器、指标追踪表、已修正事实清单与九节固化锚 |
