# 迪拜 AI 网安竞争格局 · 业务专属配置（business-config）

> **定位**：本文件是 `content/tech/ai-security/competitive-intelligence/dubai` 业务线的**单一业务事实源**：运行变量固定值、来源优先级实例化、受众定位、术语口径、监测竞品清单、信号规则阈值、追踪表全部集中于此。周期提示词（基线 / 月度）引用本文件，业务参数只在这里维护一份。
>
> **继承声明（四层体系）**：周期提示词 = [通用基座](../../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../../engine/templates/monitoring-common-spec.md) × [类型模板（竞争情报监测型）](../../../../../../engine/templates/competitive-intelligence/) × 本文件。通用层修改自动对本业务线生效；本文件修改只影响本业务线。冲突时以周期提示词 ＞ 本文件 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、运行变量固定值

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = AI 网安竞争格局
{{REPORT_TYPE}}          = competitive-intelligence
{{BASELINE_DATE}}        = 2026-12（首期基线报告落款周期）
{{REGISTRY_PATH}}        = data/processed/tech/ai-security/competitive-intelligence/dubai/ai_cyber_competition_registry.md（运行期创建，基线可缺）
{{REGISTRY_FORMAT}}      = md-table
{{SOURCE_REGISTRY_PATH}} = data/processed/tech/ai-security/competitive-intelligence/dubai/source_registry.json
{{BASELINE_REPORT_PATH}} = reports/2026-12_baseline_report.html
{{FRESHNESS_PRIORITY}}   = 最新官方 / 一手发布 > 上期值 > 第三方研究 > 媒体转述
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/ai-security/competitive-intelligence/dubai
```

**各周期落盘规则**（竞争情报监测型类型模板第一、四节的实例化；命名对齐仓库工具链）：

| 节拍 | 输出路径 | 定位 | 上期报告 |
|---|---|---|---|
| 基线 | `reports/2026-12_baseline_report.html` | 对比锚，常驻顶层；无上期报告 | 无 |
| 月度 | `reports/{{YYYY-MM}}_monthly.html` | 主更新节拍：动态矩阵全量刷新 + 档案卡增量修订 | 最近一期月度报告 + 基线 |
| 事件触发 | `reports/{{YYYY-MM-DD}}-主题.html`（追加件） | 重大竞品动作（融资 / 并购 / 换帅 / 定价重构 / 新产品线）当期升级 | 最近一期月度报告 + 基线 |

**输出格式**：纯 HTML 交付（自包含 canonical 富样式；业务配置声明，走 monitoring-common-spec 第 1 节例外条款），落盘 `reports/{{周期}}.html`；md 源稿为可选存档，**不参与 `md2html.py` 自动转换**（防止覆盖手工渲染）。

## 二、受众定位

面向在迪拜 / 阿联酋市场参与或拟参与 AI 网安竞争的**产品、市场与战略团队**，兼及投资者与政策研究者。报告对竞品动作只做事实记录与影响提示，不做「对手必然失败 / 必然成功」式断言；威胁 / 机会提示一律标「判断 / 推断」，与事实数据分离。

## 三、术语与口径（表格与正文中不得混用）

- **份额口径并列不合并**：全球企业 LLM API 支出份额（Menlo Ventures）≠ 企业 AI 部署支出份额（Menlo Ventures）≠ 阿联酋网安市场规模（Mordor / Global Market Insights）≠ MENA 信息安全终端支出（Gartner）≠ 全球 AI in cybersecurity 市场规模（Grand View Research）。
- **动作登记字段**：编号 + 玩家 + 动作 + 日期 + 来源 URL；单源动作标「单源待证」，关键动作须至少 2 家独立来源确认。
- **玩家分层定义**：直接（在迪拜 / 阿联酋有 AI 网安产品或交付能力）｜间接（生态、咨询、资本相邻）｜潜在进入者（有抓手但尚未在区域形成 AI 网安交付）。
- **汇率固定**：1 USD = 3.6725 AED（钉住）。
- 「政策乘数」指监管与政策对产品准入、资质与采购的放大效应，正文使用须与「政策」背景句同现。

## 四、来源优先级（通用基座第四节的实例化，冲突时报双份并标注）

① **官方一手**：u.ae、desc.gov.ae、tdra.gov.ae、mediaoffice.ae、ai.gov.ae、SEC EDGAR、各玩家官网 / 官方博客 / 财报 —— 唯一可直接采信层，标「已核验」。
＞ ② **行业机构 / 第三方研究**：Gartner、Mordor Intelligence、Global Market Insights、Grand View Research、Menlo Ventures、ISC2、IDC、MITRE、OWASP —— 可采信；预测分歧并列。
＞ ③ **招聘 / 门户抽样**：hiredeveloper.ae、Bayt、GulfTalent、LinkedIn、foundit Gulf —— 仅作市场信号，不与官方 / 行业机构同等采信。
＞ ④ **媒体转述**：Khaleej Times、The National、Gulf News、gulftime.ae、telecomreview、Zawya、searchinform —— 只用于发现线索；数值标「需核实原文」，须回官方 / 原始页校验。

**来源语言规则**：仅英文（`{{SOURCE_LANGUAGE_RULE}}`），严禁中文来源；若某数据点仅在中文源出现，标注「未找到英文权威来源，已剔除」并说明。政策见 `engine/docs/source-language-policy.md`（门禁 `source_check` R9）。

## 五、监测竞品清单与入选标准

**入选标准**：在迪拜 / 阿联酋有 AI 网安产品或交付能力，或具主权资本 / 算力抓手，或正进入区域市场；每家均有可追溯公开来源。

| 分层 | 玩家 | 入选依据（来源） |
|---|---|---|
| 直接 | G42 集团（Core42、CPX、Khazna、M42） | 算力—云—安全—应用垂直整合；官网与官方合作披露充分 [g42.ai, 2026] |
| 直接 | e& enterprise / Help AG | 本地 MSSP 头部，IDC MarketScape 领导者（MSS 2026 / MDR 2025）[eand.com, 2026] |
| 直接 | Moro Hub（DEWA 子公司） | 全栈主权 AI 平台；迪拜 AI Seal Tier S [brief.news, 2026] |
| 直接 | Cloud4C | 自由区托管 SOC / MSSP [security 基线报告, 2026] |
| 直接 | Microsoft（区域总部 + G42 投资） | 15 亿美元股权投资 + 10 亿美元开发者基金；Stargate UAE 生态 [blogs.microsoft.com, 2024] |
| 直接 | Palo Alto Networks、Fortinet、Kaspersky、Cisco | DIC / JLT 区域总部，产品组合覆盖 AI 网安 [security 基线报告, 2026] |
| 间接 | Hub71 生态 | AI 原生初创池（第 19 批 90% AI 原生、40 家、累计融资 2.96 亿美元）[hub71.com, 2026] |
| 间接 | 四大、Accenture、EY | AI 治理与合规咨询需求高 [security 基线报告, 2026] |
| 间接 | DarkMatter / Digital14 | 历史玩家，动态待核实；与 CPX 的渊源未获官方证实 [security 基线报告, 2026] |
| 潜在 | Presight | G42 系 AI 分析，安全延展待核实 [security 基线报告, 2026] |
| 潜在 | 中国开源模型厂商（Kimi、DeepSeek、GLM、Qwen） | 占开源支出 89%，以模型能力入模方式渗透（推断）[menlovc.com, 2026] |

## 六、追踪表（监测竞品 × 优先信息渠道）

| 玩家 | 优先信息渠道 | 更新频率 |
|---|---|---|
| G42 集团 | g42.ai / core42.ai / cpx.net 官网与官方博客；WAM 英文；官方合作披露 | 月度 + 事件触发 |
| e& / Help AG | eand.com 新闻页；IDC MarketScape（第三方）；lumitech.co 转述 | 月度 |
| Moro Hub | brief.news / lumitech.co（聚合源）；Digital Dubai 复核 | 月度 |
| Cloud4C | cloud4c.com/uae；招聘页 | 月度 |
| Microsoft | blogs.microsoft.com；新闻室；SEC 文件 | 月度 + 事件触发 |
| Palo Alto / Fortinet / Kaspersky / Cisco | 区域官网与新闻室；DIC / JLT 自由区公告 | 月度 |
| Hub71 | hub71.com 官网与 FAQ；批次公告 | 月度 |
| 咨询（四大 / Accenture / EY） | 官网洞察页；招标与案例页 | 月度 |
| DarkMatter / Digital14 | 官网；第三方转述（需核实） | 事件触发 |
| Presight | 官网；G42 系公告 | 事件触发 |
| 中国开源模型厂商 | 官方平台文档（platform.kimi.com 等）；Menlo 等第三方研究 | 月度 |

> 追踪表活值运行后逐项回写 `{{REGISTRY_PATH}}`；未变动项注明「截至本次运行日期无更新」。

## 七、信号触发器（事件 → 受影响模块）

| 触发事件 | 受影响模块 |
|---|---|
| 任一直接玩家定价重构或套餐调整 | 竞品档案卡、动态矩阵、月度报告升级 |
| 并购 / 收购 / 合资（如 CPX 收购 spiderSilk、TSI Tech 类动作） | 竞品档案卡、格局分层、影响提示 |
| 关键人事变动（区域总经理 / CISO 级） | 竞品档案卡、组织与人事 |
| 新产品线或新模型版本发布（含模型入模、分级开放） | 竞品档案卡、动态矩阵、影响提示 |
| 合规资质获取 / 吊销（ISR 审核员、NCAP、AI Seal 等） | 格局分层、影响提示 |
| 融资 / 注资 / IPO 进展（如微软–G42 类动作、Anthropic IPO） | 资本维度、格局分层 |
| GITEX / GISEC 等旗舰活动发布重大合作或产品 | 本期动作热点、动态矩阵 |

## 八、信号规则阈值（R1–R6，由本配置定义）

| 编号 | 监测对象 | 触发条件 | 确认标准 | 动作 |
|---|---|---|---|---|
| R1 | 全部直接玩家 | 公开调价 / 套餐重构 | 2 家独立来源 | 更新档案卡与矩阵；月度报告升级 |
| R2 | 全部监测玩家 | 并购 / 收购 / 合资公告 | 官方或监管披露 | 重估分层；事件触发专项 |
| R3 | 直接玩家 | 区域总经理 / CISO 级人事变动 | 官方或招聘信号交叉 | 更新档案卡组织栏 |
| R4 | 模型层与直接玩家 | 新模型 / 新产品线发布（含入模、分级开放） | 官方发布页 | 矩阵登记；影响提示（标推断） |
| R5 | 直接玩家 | ISR / NCAP / AI Seal 等资质获取或吊销 | 官方名单 / 公告 | 更新合规栏；格局演变判断复核 |
| R6 | 全部监测玩家 | 融资 / 注资 / IPO / 大额合同 | 官方 / SEC / 交易所披露 | 资本维度登记；格局分层复核 |

## 九、已修正事实清单

首期为空；产生修正后逐条补记，格式：`- ❌ 不得再称"…"——正确结论为…。[Source: URL, 年份]`。无来源不得入清单；基线报告的结构与结论一经产出即为锚。

## 十、基线九节结构固化锚

基线报告 `reports/2026-12_baseline_report.html` 九节结构为该业务线固化锚，后续报告逐字继承：

1. 执行摘要｜2. 监测机制设计｜3. 竞争格局总览｜4. 竞品档案首建｜5. 动态矩阵与信号规则｜6. 来源与核验治理｜7. 风险与盲区｜8. 交付物与后续运行方式｜9. 参考来源清单

---

## 信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：四级标注与摘要引用约束见 `engine/templates/information-layering-spec.md` 第二 / 四节；新增信息统计模块见第四节。
- **事实卡片**：本业务线为共享事实域（CI），正文以 `[FC-CI-…]` 引用 `engine/fact_cards/competitive_intelligence_fact_cards.json`。
- **决策卡与行动协议**：核心判断输出决策卡；行动项五要素 + 三档优先级（规范：`engine/templates/decision-delivery-spec.md`）。
- **阈值校准**：首次中期回测 2027-06；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节。
- **场景切片**：主场景 **投资决策**；次场景 **政策制定**。
- **影响分级**：`impact_tier = high`（高影响，强制披露矩阵见 `engine/templates/information-layering-spec.md` §七）。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」。
- **盲区**：P0 四类（就业 / 收入 / 空置 / 竣工）优先消号。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-12 | 初始版本 | 建立竞争情报监测型业务配置：四层继承声明指向 engine/templates/competitive-intelligence/；定义 {{REGION}}={{TOPIC}} 固定值、来源优先级实例化、11 家监测玩家分层与入选标准、追踪表、7 类信号触发器、R1–R6 信号规则阈值、九节固化锚 |
