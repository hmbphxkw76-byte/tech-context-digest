# 迪拜 AI 网安竞争格局 · 竞争情报登记册

> **格式**：md-table ｜ **用途**：存放 11 项监测玩家的档案活值、多口径份额读数与 R1–R6 信号状态，供提示词运行前读取、运行后回写。
> **维护规则**：单元格内数值后附 `[来源, 年份]` 与来源编号 `[S-…]`；未核实字段保留「待核实」，不补值、不外推；周期提示词模板内严禁填写活值。
> **初始值**：首轮运行前从基线报告 `content/tech/ai-security/competitive-intelligence/dubai/reports/2026-11_baseline_report.html` 提取填入（2026-11 基线期）。
> **来源登记**：`data/processed/tech/ai-security/competitive-intelligence/dubai/source_registry.json`（S-001–S-045，共 45 条）。
> **官方来源快照**：`data/raw/tech/ai-security/competitive-intelligence/dubai/`（含 `official_snapshot_manifest.json`）。
> **量化台账**：`quant_model_layer_share.csv`、`quant_enterprise_ai_deploy_spend.csv`（同目录）。

## 一、监测玩家档案（11 项：直接 6 / 间接 3 / 潜在 2）

| # | 玩家 | 分层 | 定位 | 监测重点 | 优先信息渠道 | 基线期信号 |
|---|---|---|---|---|---|---|
| 1 | G42 集团（Core42、CPX、Khazna、M42） | 直接 | 算力—云—安全—应用垂直整合的主权 AI 平台 | 算力 / 主权云 / MSSP 交付 | g42.ai / core42.ai / cpx.net；WAM 英文 | 未触发 |
| 2 | e& enterprise / Help AG | 直接 | 本地 MSSP 头部；IDC MarketScape 领导者（MSS 2026 / MDR 2025） | 托管安全 / 区域合作 | eand.com 新闻页；IDC MarketScape；lumitech.co 转述 | 未触发 |
| 3 | Moro Hub（DEWA 子公司） | 直接 | 全栈主权 AI 平台；迪拜 AI Seal Tier S（转述，待核实原文） | 主权 AI 平台 / 资质 | brief.news / lumitech.co（聚合源）；Digital Dubai 复核 | 未触发 |
| 4 | Cloud4C | 直接 | 自由区托管 SOC / MSSP | 托管 SOC / 自由区渠道 | cloud4c.com/uae；招聘页 | 未触发 |
| 5 | Microsoft（区域总部 + G42 投资） | 直接 | 全球云与安全厂商区域总部；G42 股权投资方 | 云 / 安全产品 / 资本联动 | blogs.microsoft.com；新闻室；SEC 文件 | 未触发 |
| 6 | Palo Alto Networks、Fortinet、Kaspersky、Cisco | 直接 | 全球网安厂商区域总部（DIC / JLT 自由区） | 产品组合 / 自由区渠道 | 区域官网与新闻室；自由区公告 | 未触发 |
| 7 | Hub71 生态 | 间接 | AI 原生初创池 | 初创池 / 融资 | hub71.com 官网与 FAQ；批次公告 | 未触发 |
| 8 | 四大、Accenture、EY | 间接 | AI 治理与合规咨询 | 咨询 / 合规交付 | 官网洞察页；招标与案例页 | 未触发 |
| 9 | DarkMatter / Digital14 | 间接 | 历史玩家，动态待核实；与 CPX 的渊源未获官方证实 | 事件触发 | 官网；第三方转述（需核实） | 未触发 |
| 10 | Presight | 潜在 | G42 系 AI 分析，安全延展待核实 | 安全产品线 | 官网；G42 系公告 | 未触发 |
| 11 | 中国开源模型厂商（Kimi、DeepSeek、GLM、Qwen） | 潜在 | 以模型能力入模方式渗透（推断） | 模型能力 / 区域渗透 | 官方平台文档；Menlo 等第三方研究 | 未触发 |

## 二、多口径份额与规模读数（并列不合并）

| 口径 | 读数 | 机构 | 统计周期 / 发布 | 核验状态 | 事实卡片 | 来源 |
|---|---|---|---|---|---|---|
| 全球企业 LLM API 支出份额 | Anthropic 55% / OpenAI 31% / Google 9%（合计 86%） | Menlo Ventures | 2026-11 | 部分核验 | [FC-CI-001] | [S-006] |
| 企业 AI 部署支出 | 2025 年 330 亿 → 2026-09 1768 亿美元（5.4 倍，原报告口径） | Menlo Ventures | 2025 全年 / 2026-09 月度 | 部分核验 | [FC-CI-002] | [S-006] |
| MENA 信息安全终端支出 | 2025 年增长 14%（预测值 F） | Gartner | 2025 全年预测 / 2025-04-08 | 已核验 | [FC-CI-005] | [S-005] |
| 阿联酋网安市场规模 | 以 Mordor / Global Market Insights 报告页为准（基线未摘引点值） | Mordor / GMI | 行业报告 | 已核验（来源页） | — | [S-011][S-024] |
| 全球 AI in cybersecurity 市场 | 以 Grand View Research 报告页为准（基线未摘引点值） | Grand View Research | 行业报告 | 已核验（来源页） | — | [S-025] |

> **口径警示**：以上五个口径统计域不同（全球 API 支出 / 企业 AI 部署 / MENA 终端支出 / 阿联酋网安市场 / 全球 AI in cybersecurity），不可相加、不可静默择一；跨机构数字不可合并。
> **点值缺口**：阿联酋网安市场与全球 AI in cybersecurity 的点值由 `industry-research/dubai` 业务线登记（见该线指标登记册），本线不重复维护。

## 三、动态矩阵（维度 × 玩家，2026-12 基线首期）

| 玩家 | 定价 | 产品 / 能力 | 渠道 | 组织 / 人事 | 合规资质 | 资本 | 近期活动 | 信号 |
|---|---|---|---|---|---|---|---|---|
| G42 集团 | 待核实 | 算力 / 云 / MSSP | 官网 + 合作披露 | 待核实 | Stargate UAE 生态 | 微软 15 亿美元 | 微软合作 | 未触发 |
| e& / Help AG | 待核实 | MSSP 头部 | eand.com | 待核实 | IDC 领导者 | — | Sergas 合作 | 未触发 |
| Moro Hub | 待核实 | 主权 AI 平台 | 聚合源 | 待核实 | AI Seal Tier S | — | 资质披露（转述） | 未触发 |
| Cloud4C | 待核实 | 托管 SOC | 自由区 | 待核实 | 待核实 | — | 待核实 | 未触发 |
| Microsoft | 待核实 | 云 / 安全 | 官方博客 | 待核实 | — | G42 投资 | 安全研究发布 | 未触发 |
| 全球四家 | 待核实 | AI 网安组合 | DIC / JLT | 待核实 | 待核实 | — | 待核实 | 未触发 |
| Hub71 | 不适用 | 初创池 | 官网 / FAQ | 待核实 | — | 累计 2.96 亿美元 | 第 19 批 | 未触发 |
| 咨询（四大等） | 待核实 | 治理咨询 | 洞察页 | 待核实 | — | — | 待核实 | 未触发 |
| DarkMatter / Digital14 | 待核实 | 待核实 | 官网 / 转述 | 待核实 | 待核实 | — | 待核实 | 未触发 |
| Presight | 待核实 | 待核实 | G42 系公告 | 待核实 | 待核实 | — | 待核实 | 未触发 |
| 中国开源厂商 | 待核实 | 开源模型 | 官方平台 | 不适用 | — | — | 待核实 | 未触发 |

## 四、信号规则状态（R1–R6，预校准 ex-ante）

| 编号 | 监测对象 | 触发条件 | 确认标准 | 当前状态 | 最近判定 |
|---|---|---|---|---|---|
| R1 | 全部直接玩家 | 公开调价 / 套餐重构 | 2 家独立来源 | 未触发 | 2026-12 基线 |
| R2 | 全部监测玩家 | 并购 / 收购 / 合资公告 | 官方或监管披露 | 未触发 | 2026-12 基线 |
| R3 | 直接玩家 | 区域总经理 / CISO 级人事变动 | 官方或招聘信号交叉 | 未触发 | 2026-12 基线 |
| R4 | 模型层与直接玩家 | 新模型 / 新产品线发布（含入模、分级开放） | 官方发布页 | 未触发 | 2026-12 基线 |
| R5 | 直接玩家 | ISR / NCAP / AI Seal 等资质获取或吊销 | 官方名单 / 公告 | 未触发 | 2026-12 基线 |
| R6 | 全部监测玩家 | 融资 / 注资 / IPO / 大额合同 | 官方 / SEC / 交易所披露 | 未触发 | 2026-12 基线 |

> 阈值由业务配置 `content/tech/ai-security/competitive-intelligence/dubai/prompts/business-config.md` 第八节定义；首次中期回测 2027-06，校准完成前全部信号灯不得作为已校准规则使用。

## 五、已修正事实清单（防回退锚）

- ❌ 不得再将 CPX 与 DarkMatter 绑定——CPX 为 2022 年成立的 G42 子公司，与 DarkMatter → Digital14 系不同实体。[FC-CI-004]
- ❌ 不得将「中国开源模型厂商占开源支出 89%」当作确定份额——该值为 Menlo Ventures 估算，区域网安渗透为推断。[FC-CI-001]
- ❌ 不得以媒体转述的「政策松动」作为政策口径结论——须回 DESC / TDRA 官方页校验。[S-002][S-004]

## 六、运行留痕

- **2026-12 基线首期**：本登记册由基线报告第三节 / 第四节 / 第五节提取建立；R1–R6 全部「未触发」。
- 后续运行：未变动项注明「截至 {{CURRENT_DATE}} 无更新」；实质变化按「玩家 + 动作 + 日期 + 来源 URL」登记，并同步来源登记 `verify_status`。
