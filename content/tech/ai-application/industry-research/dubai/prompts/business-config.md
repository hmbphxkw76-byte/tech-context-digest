# 迪拜（阿联酋）AI 应用行业 · 业务专属配置（business-config）

> **定位**：本文件是 `content/tech/ai-application/industry-research/dubai` 业务线的**单一业务事实源**：运行变量固定值、来源优先级实例化、受众定位、术语口径、触发器、指标追踪清单、已修正事实清单全部集中于此。周期提示词（基线 / 月度刷新）引用本文件，业务参数只在这里维护一份。
>
> **继承声明（四层体系）**：周期提示词 = [通用基座](../../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../../engine/templates/monitoring-common-spec.md) × [类型模板](../../../../../../engine/templates/industry-research/)（行业深度研究型）× 本文件。通用层修改自动对本业务线生效；本文件修改只影响本业务线。冲突时以周期提示词 ＞ 本文件 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、运行变量固定值

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = AI 应用行业
{{REPORT_TYPE}}          = industry-research
{{BASELINE_DATE}}        = 2026-11（首份基线报告完稿日期）
{{REGISTRY_PATH}}        = data/processed/tech/ai-application/industry-research/dubai/ai_application_industry_indicator_registry.md（运行期创建，基线可缺）
{{REGISTRY_FORMAT}}      = md-table
{{SOURCE_REGISTRY_PATH}} = data/processed/tech/ai-application/industry-research/dubai/source_registry.json
{{BASELINE_REPORT_PATH}} = reports/2026-11_baseline_report.html
{{FRESHNESS_PRIORITY}}   = 近 12 个月内数据优先；超过 24 个月须标注年份并谨慎使用
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/ai-application/industry-research/dubai
```

**类型与周期**：`industry-research`（行业深度研究型），周期 `baseline`（九节固定骨架）与 `monthly`（月度刷新，结构逐字继承基线）。模板入口：`engine/templates/industry-research/prompt-baseline-setup-template.md`。

**输出格式**：canonical 富样式自包含 HTML 为主交付物，落盘 `reports/{{周期}}.html`；md 源稿存 `sources/` 同名存档，不参与 `md2html.py` 自动转换（防止覆盖手工渲染）。

## 二、受众定位

面向关注「迪拜（阿联酋）AI 应用行业」的产业研究与决策读者，兼具行业分析与市场进入参考视角。报告保持**中性全景刻画**：不给投资评级、不出具 Go/No-Go 决策建议（那是投资分析与尽调型、可行性型的边界）；趋势判断一律标「推断」，多口径规模数据并列不合并。

## 三、术语口径区分（表格与正文中不得混用）

- **AI 应用行业** = 上游模型 / 算力（基础模型、AI 芯片与云算力、主权 AI 基建）→ 中游平台与产品（主权 AI 平台、云厂商 AI 服务、AI 应用开发与代理、开发工具与 Agent 框架）→ 下游交付与采用（政府与大型企业 AI 采购、行业解决方案、创业池与生态）。**不含** AI 安全（属 `content/tech/ai-security/` 业务线），**不含**无 AI 维度的传统 IT / 数字化转型市场测算。
- **UAE AI 市场**（IMARC，全口径 AI 支出，含软件 / 硬件 / 服务）≠ **全球企业 AI 市场**（Grand View，全球 enterprise AI）≠ **全球 AI 市场**（The Business Research Company，全球 AI 总体）。统计域与地域不同，口径不可直接比较。
- **本地口径**（迪拜 / 阿联酋）与**全球口径**必须分列，禁止混算。
- **云厂商区域服务**（Azure UAE North / UAE Central、AWS 中东（阿联酋）区域）与**主权 AI 平台**（Core42、Moro Hub）为不同交付形态，并列呈现。
- 招聘机构抽样 ≠ 官方或权威机构口径（前者标注「抽样」并谨慎引用）。
- 汇率固定：1 USD = 3.6725 AED（钉住）。

## 四、来源优先级（通用基座第四节的实例化，冲突时报双份并标注）

① 阿联酋/迪拜政府官方（ai.gov.ae、dub.ai / Digital Dubai、u.ae、mediaoffice.ae、WAM 英文、各自由区官网）＋ 厂商官方（Microsoft、OpenAI、AWS、Google 官方）
＞ ② 国际权威组织与分析机构（Gartner、IDC、Grand View Research、IMARC Group、Mordor Intelligence、Global Market Insights、Omdia）
＞ ③ 主权平台与云厂商官方（G42、Core42、Moro Hub、Hub71、Khazna）
＞ ④ 英文行业/主流媒体（Khaleej Times、The National、Gulf News、Zawya、Reuters——只用于发现线索，数值须回官方/原始页校验）
＞ ⑤ 同源已核实资产：`content/tech/ai-security/industry-research/dubai/` 业务线的基线报告、md 源稿与指标登记册（仅共用 G42 / Hub71 等交叉事实，口径冲突时并列登记）。

## 五、重大事件触发器（事件 → 受影响模块）

| 触发事件 | 受影响模块 |
|---|---|
| GITEX Global / Dubai AI Week / GISEC Global 新一届举办（日期、主题、官方发布） | 产业链、头部玩家、趋势 |
| UAE AI Strategy 2031 / Dubai Universal Blueprint for AI 更新或阶段目标修订 | 驱动因素、产业链下游、趋势 |
| Stargate UAE / 主权云（Core42、Moro Hub）建设或运营状态更新 | 产业链上游、驱动因素 |
| 云厂商（Microsoft Azure / AWS / Google Cloud）UAE 区域 AI 服务上线或扩容 | 产业链中游、头部玩家 |
| Hub71 新批次创业池或 AI 原生初创融资披露 | 产业链下游、头部玩家 |
| 政府与大型企业 AI 采购 / Dubai AI Seal 名单更新 | 下游交付与采用、驱动因素 |

## 六、指标追踪表（活值维护于 {{REGISTRY_PATH}}）

| # | 监测指标 | 口径/单位 | 优先数据源（英文） |
|---|---|---|---|
| 1 | UAE AI 市场规模（全口径） | 亿美元 / CAGR | imarcgroup.com |
| 2 | UAE AI 市场结构（软件占比 / 类型 / 地区份额） | % | imarcgroup.com |
| 3 | 全球企业 AI 市场 | 亿美元 / CAGR | grandviewresearch.com |
| 4 | 全球 AI 市场 | 亿美元 / CAGR | thebusinessresearchcompany.com |
| 5 | UAE AI 市场（Mordor / GMI 口径） | 亿美元 / CAGR | mordorintelligence.com / gminsights.com |
| 6 | Dubai Universal Blueprint for AI 目标与举措 | 亿 AED/年 / % | dub.ai |
| 7 | 迪拜政府 AI 部署（首席 AI 官 / 在用用例） | 人 / 个 | digitaldubai.ae |
| 8 | G42 集团规模口径 | 人 / 国 | g42.ai |
| 9 | Core42 主权云状态 | — | core42.ai / news.microsoft.com |
| 10 | 微软–G42 投资 | 亿美元 | blogs.microsoft.com |
| 11 | Hub71 创业池 | 家 / 亿美元 | hub71.com |
| 12 | Moro Hub 主权 AI 平台 | — | morohub.ae |
| 13 | 云厂商 UAE 区域 AI 服务 | — | learn.microsoft.com / aws.amazon.com |
| 14 | Stargate UAE 状态 | GW | openai.com |

> 首份基线运行后回写登记册；基线期先引用 `data/processed/tech/ai-application/industry-research/dubai/ai_application_industry_indicator_registry.md` 的已核实活值，不新造数值。

## 七、已修正事实清单（基线锚，防回退；无来源不得追加）

```
- ❌ 不得再引用微软–G42「152 亿美元」broad 投资计划——经复核未获英文权威来源证实（微软官方仅确认 2024-04 的 15 亿美元股权注资与 10 亿美元开发者基金）。[Source: https://blogs.microsoft.com/blog/2024/04/15/microsoft-and-g42-partner, 2024]
- ❌ 不得将 CPX 与 DarkMatter 绑定——CPX 为 2022 年成立的 G42 子公司，与 DarkMatter → Digital14 系不同实体。[Source: https://www.cpx.net, 2025]
- ❌ 不得将不同口径 AI 市场规模（UAE 全口径 / 全球企业 AI / 全球 AI）相加、静默择一或混算——并列呈现并标注口径。
- ❌ 不得估算本报告未文档化的集中度（CRn）或价值链分布数值——无公开可核实来源时标注「未核验」。
- ❌ 不得把「AI 应用行业」与「AI 安全」混为一谈——AI 安全属 content/tech/ai-security/ 业务线，本报告只覆盖模型/算力 → 平台与产品 → 交付与采用的应用侧。
```

## 八、基线九节结构固化锚

基线报告九节结构为该业务线固化锚，后续报告逐字继承：

1. 执行摘要｜2. 研究范围与方法｜3. 产业链图谱｜4. 市场规模与格局｜5. 头部玩家与竞争格局｜6. 驱动因素与风险｜7. 趋势判断（推断）｜8. 数据治理与局限｜9. 参考来源清单

---

## 信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：四级标注与摘要引用约束见 `engine/templates/information-layering-spec.md` 第二 / 四节；新增信息统计模块见第四节。
- **事实卡片**：本业务线为共享事实域（IND），正文以 `[FC-IND-…]` 引用 `engine/fact_cards/industry_research_fact_cards.json`。
- **决策卡与行动协议**：核心判断输出决策卡；行动项五要素 + 三档优先级（规范：`engine/templates/decision-delivery-spec.md`）。
- **阈值校准**：首次中期回测 2027-06；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节。
- **场景切片**：主场景 **投资决策**；次场景 **政策制定**。
- **影响分级**：`impact_tier = high`（高影响，强制披露矩阵见 `engine/templates/information-layering-spec.md` §七）。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」。
- **盲区**：P0 四类（本地 AI 应用交付口径 / 政府 AI 采购金额 / 云厂商区域 AI 收入 / 创业池融资密度）优先消号。

---

<!-- VOCAB-SYNC:BEGIN topic=tech do-not-edit -->
## 词汇速览 · 科技（词汇库自动同步）

> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 tech v1.4，共 61 条（同步于 2026-11-21T16:53:17）。标记区间内请勿手工编辑；词条变更走词汇库导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。

- **模型与厂商**（19）：多模态模型（Multimodal Model、多模态）；推理模型（Reasoning Model、推理增强模型、思维链模型）；OpenAI（openai.com）；Anthropic（anthropic.com）；Google DeepMind（谷歌deepmind、Google AI）；Meta AI（Meta、Facebook AI）；xAI（X.AI、xAI 公司）；Mistral AI（Mistral）；DeepSeek（深度求索）；阿里通义千问（Qwen、通义千问）；智谱 GLM（GLM、Zhipu AI、智谱AI）；月之暗面 Kimi（Moonshot AI、Kimi）；字节豆包（Doubao、豆包大模型）；百度文心（ERNIE、文心一言）；GPT（GPT 系列、GPT-4、GPT-5）；Claude（Claude 系列、Claude Sonnet、Claude Opus）；Gemini（Gemini 系列）；Llama（Llama 系列、Llama 开源）；Grok（Grok 系列）
- **Agent 技术与框架**（13）：AI Agent（智能体、Agent）；多智能体系统（Multi-Agent System、MAS、多智能体协作）；工具调用（Function Calling、Tool Use、函数调用）；A2A（Agent-to-Agent、Agent2Agent 协议）；ReAct（Reasoning and Acting）；Agent 记忆（Agent Memory、长期记忆）；Computer Use（计算机使用、屏幕操作 Agent）；LangChain（LangChain 框架）；LangGraph（LangGraph 编排）；LlamaIndex（LlamaIndex 框架）；AutoGen（Microsoft AutoGen）；CrewAI（CrewAI 框架）；Dify（Dify 平台）
- **应用与产品**（15）：ChatGPT（chatgpt.com）；Perplexity（Perplexity AI）；NotebookLM（NotebookLM 产品）；Microsoft 365 Copilot（M365 Copilot、Office Copilot）；Deep Research（深度研究）；AI 搜索（AI Search、答案引擎）；Midjourney（MJ）；Sora（OpenAI Sora）；Suno（Suno AI）；ElevenLabs（ElevenLabs 语音）；Lovable（Lovable.dev）；Bolt.new（Bolt）；v0（v0.dev）；Replit Agent（Replit）；Manus（Manus AI）
- **概念与评估**（11）：大语言模型（LLM、Large Language Model、大模型）；生成式 AI（Generative AI、AIGC）；开源权重模型（Open-Weights Model、开放权重）；上下文窗口（Context Window、上下文长度）；Token（词元）；幻觉（Hallucination、模型幻觉）；微调（Fine-tuning、SFT、监督微调）；RLHF（基于人类反馈的强化学习、Reinforcement Learning from Human Feedback）；蒸馏（Distillation、模型蒸馏）；Prompt 工程（Prompt Engineering、提示词工程）；GAIA（GAIA 基准）
- **工具与平台**（3）：PyRIT（Microsoft PyRIT）；promptfoo；garak（LLM vulnerability scanner）
<!-- VOCAB-SYNC:END -->

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11 | 初始版本 | 建立 `content/tech/ai-application/industry-research/dubai` 业务线；四层继承体系指向 `engine/templates/industry-research/`（行业深度研究型）；定义 {{REGION}} / {{TOPIC}}、来源优先级、触发器、指标追踪表、已修正事实清单与九节固化锚 |
