# 全球 AI 应用竞争格局 · 业务专属配置（business-config）

> **定位**：本文件是 `content/tech/ai-application/trends` 业务线的**单一业务事实源**：运行变量固定值、来源优先级实例化、受众定位、术语口径、监测竞品清单、信号规则阈值、追踪表全部集中于此。周期提示词（基线 / 月度）引用本文件，业务参数只在这里维护一份。
>
> **继承声明（四层体系）**：周期提示词 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [类型模板（竞争情报监测型）](../../../../../engine/templates/competitive-intelligence/) × 本文件。通用层修改自动对本业务线生效；本文件修改只影响本业务线。冲突时以周期提示词 ＞ 本文件 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、运行变量固定值

```
{{REGION}}               = 全球（Global）
{{TOPIC}}                = AI 应用竞争格局
{{REPORT_TYPE}}          = competitive-intelligence
{{BASELINE_DATE}}        = 2026-11（首期基线报告落款周期）
{{REGISTRY_PATH}}        = data/processed/tech/ai-application/trends/ai_application_competition_registry.md（运行期创建，基线可缺）
{{REGISTRY_FORMAT}}      = md-table
{{SOURCE_REGISTRY_PATH}} = data/processed/tech/ai-application/trends/source_registry.json
{{BASELINE_REPORT_PATH}} = reports/2026-11_baseline_report.html
{{FRESHNESS_PRIORITY}}   = 最新官方 / 一手发布 > 上期值 > 第三方研究 > 媒体转述
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/ai-application/trends
```

**各周期落盘规则**（竞争情报监测型类型模板第一、四节的实例化；命名对齐仓库工具链）：

| 节拍 | 输出路径 | 定位 | 上期报告 |
|---|---|---|---|
| 基线 | `reports/2026-11_baseline_report.html` | 对比锚，常驻顶层；无上期报告 | 无 |
| 月度 | `reports/{{YYYY-MM}}_monthly.html` | 主更新节拍：动态矩阵全量刷新 + 档案卡增量修订 | 最近一期月度报告 + 基线 |
| 事件触发 | `reports/{{YYYY-MM-DD}}-主题.html`（追加件） | 重大竞品动作（新模型发布 / 定价重构 / 融资并购）当期升级 | 最近一期月度报告 + 基线 |

**输出格式**：纯 HTML 交付（自包含 canonical 富样式；业务配置声明，走 monitoring-common-spec 第 1 节例外条款），落盘 `reports/{{周期}}.html`；md 源稿为可选存档，**不参与 `md2html.py` 自动转换**（防止覆盖手工渲染）。

## 二、受众定位

面向关注全球 AI 应用市场的**产品、市场与战略团队**，兼及投资者与政策研究者。报告对竞品动作只做事实记录与影响提示，不做「对手必然失败 / 必然成功」式断言；威胁 / 机会提示一律标「判断 / 推断」，与事实数据分离。

## 三、术语与口径（表格与正文中不得混用）

- **口径并列不合并**：模型能力（基准跑分）≠ 产品活跃用户 ≠ API 支出份额 ≠ 企业部署支出份额 ≠ 应用收入。不同口径并列登记，不互换。
- **动作登记字段**：编号 + 玩家 + 动作 + 日期 + 来源 URL；单源动作标「单源待证」，关键动作须至少 2 家独立来源确认。
- **玩家分层定义**：模型层（基础模型厂商）｜应用层（AI 原生应用 / 编码工具 / 生产力套件）｜云与基础设施（托管与分发）｜开源生态（模型与工具链）。
- **地区口径**：全球数据为主；区域市场（含中国）单独标注，不与全球口径合并。
- 「政策乘数」指监管与政策对产品准入、资质与采购的放大效应，正文使用须与「政策」背景句同现。

## 四、来源优先级（通用基座第四节的实例化，冲突时报双份并标注）

① **官方一手**：各玩家官网 / 官方博客 / 财报 / SEC EDGAR / 官方平台文档 —— 唯一可直接采信层，标「已核验」。
＞ ② **行业机构 / 第三方研究**：Menlo Ventures、a16z、Gartner、IDC、Sensor Tower、data.ai、Similarweb、Grand View Research —— 可采信；预测分歧并列。
＞ ③ **基准与评测**：LMArena、OpenRouter、Hugging Face Open LLM Leaderboard、SWE-bench —— 仅作能力信号，标注版本与口径。
＞ ④ **媒体转述**：TechCrunch、The Information、Reuters、Bloomberg、官方转述 —— 只用于发现线索；数值标「需核实原文」，须回官方 / 原始页校验。

**来源语言规则**：仅英文（`{{SOURCE_LANGUAGE_RULE}}`），严禁中文来源；若某数据点仅在中文源出现，标注「未找到英文权威来源，已剔除」并说明。政策见 `engine/docs/source-language-policy.md`（门禁 `source_check` R9）。

## 五、监测竞品清单与入选标准

**入选标准**：在全球 AI 应用市场有可追溯公开来源的模型层 / 应用层 / 云与基础设施 / 开源生态玩家；每家均有官方或权威第三方来源。

| 分层 | 玩家 | 入选依据（来源） |
|---|---|---|
| 模型层 | OpenAI | GPT 系列与 API 生态；官方平台文档与博客 [openai.com, 2026] |
| 模型层 | Anthropic | Claude 系列；企业合作与安全研究 [anthropic.com, 2026] |
| 模型层 | Google DeepMind | Gemini 系列与 Workspace 集成 [deepmind.google, 2026] |
| 模型层 | Meta | Llama 开源系列与生态 [ai.meta.com, 2026] |
| 模型层 | xAI | Grok 系列 [x.ai, 2026] |
| 模型层 | Mistral AI | 开源 + 商用模型 [mistral.ai, 2026] |
| 模型层 | DeepSeek / Qwen / Kimi / Zhipu | 中国开源与商用模型（区域口径单独标注）[官方平台, 2026] |
| 应用层 | Microsoft Copilot / GitHub Copilot | 生产力与编码套件；官方发布 [microsoft.com, 2026] |
| 应用层 | Cursor（Anysphere） | AI 原生 IDE；定价与产品发布 [cursor.com, 2026] |
| 应用层 | Perplexity | AI 搜索；官方发布与融资 [perplexity.ai, 2026] |
| 应用层 | Adobe Firefly / Midjourney | 图像生成应用 [官方平台, 2026] |
| 云与基础设施 | AWS / Azure / GCP | 模型托管与分发 [官方平台, 2026] |
| 开源生态 | Hugging Face | 模型与工具链分发 [huggingface.co, 2026] |

## 六、追踪表（监测竞品 × 优先信息渠道）

| 玩家 | 优先信息渠道 | 更新频率 |
|---|---|---|
| 模型层各厂商 | 官方平台文档 / 博客 / 发布页；SEC 文件；第三方研究 | 月度 + 事件触发 |
| 应用层各厂商 | 官方发布页 / 定价页；产品更新日志 | 月度 + 事件触发 |
| 云与基础设施 | 官方公告 / 合作伙伴页 | 月度 |
| 开源生态 | 官方仓库 / 模型卡；Hugging Face 榜单 | 月度 |
| 基准与评测 | LMArena / OpenRouter / SWE-bench 榜单 | 月度 |

> 追踪表活值运行后逐项回写 `{{REGISTRY_PATH}}`；未变动项注明「截至本次运行日期无更新」。

## 七、信号触发器（事件 → 受影响模块）

| 触发事件 | 受影响模块 |
|---|---|
| 新模型 / 新版本发布（含分级开放、入模） | 竞品档案卡、动态矩阵、月度报告升级 |
| 定价重构或套餐调整 | 竞品档案卡、动态矩阵、影响提示 |
| 融资 / 并购 / IPO 进展 | 资本维度、格局分层 |
| 关键人事变动（区域 / 产品线负责人） | 竞品档案卡、组织与人事 |
| 用户规模 / 活跃 / 留存重大披露 | 市场格局、影响提示 |
| 合规资质 / 内容安全 / 版权争议 | 风险与盲区、影响提示 |
| 基准评测排名重大变动 | 能力信号、动态矩阵 |

## 八、信号规则阈值（R1–R6，由本配置定义）

| 编号 | 监测对象 | 触发条件 | 确认标准 | 动作 |
|---|---|---|---|---|
| R1 | 全部监测玩家 | 新模型 / 新版本发布 | 官方发布页 | 矩阵登记；影响提示（标推断） |
| R2 | 全部监测玩家 | 公开调价 / 套餐重构 | 2 家独立来源 | 更新档案卡与矩阵；月度报告升级 |
| R3 | 全部监测玩家 | 融资 / 并购 / IPO / 大额合同 | 官方 / SEC / 交易所披露 | 资本维度登记；格局分层复核 |
| R4 | 应用层玩家 | 用户规模 / 活跃 / 留存重大披露 | 官方或权威第三方 | 市场格局登记；影响提示 |
| R5 | 模型层玩家 | 基准评测排名重大变动 | 榜单原始页 | 能力信号登记；口径标注 |
| R6 | 全部监测玩家 | 合规 / 内容安全 / 版权争议 | 官方或监管披露 | 风险与盲区登记；影响提示 |

## 九、已修正事实清单

首期为空；产生修正后逐条补记，格式：`- ❌ 不得再称"…"——正确结论为…。[Source: URL, 年份]`。无来源不得入清单；基线报告的结构与结论一经产出即为锚。

## 十、基线九节结构固化锚

基线报告 `reports/2026-11_baseline_report.html` 九节结构为该业务线固化锚，后续报告逐字继承：

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

---

<!-- VOCAB-SYNC:BEGIN topic=tech do-not-edit -->
## 词汇速览 · 科技（词汇库自动同步）

> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 tech v1.4，共 71 条（同步于 2026-11-21T11:39:04）。标记区间内请勿手工编辑；词条变更走词汇库导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。

- **模型与厂商**（19）：多模态模型（Multimodal Model、多模态）；推理模型（Reasoning Model、推理增强模型、思维链模型）；OpenAI（openai.com）；Anthropic（anthropic.com）；Google DeepMind（谷歌deepmind、Google AI）；Meta AI（Meta、Facebook AI）；xAI（X.AI、xAI 公司）；Mistral AI（Mistral）；DeepSeek（深度求索）；阿里通义千问（Qwen、通义千问）；智谱 GLM（GLM、Zhipu AI、智谱AI）；月之暗面 Kimi（Moonshot AI、Kimi）；字节豆包（Doubao、豆包大模型）；百度文心（ERNIE、文心一言）；GPT（GPT 系列、GPT-4、GPT-5）；Claude（Claude 系列、Claude Sonnet、Claude Opus）；Gemini（Gemini 系列）；Llama（Llama 系列、Llama 开源）；Grok（Grok 系列）
- **Agent 技术与框架**（13）：AI Agent（智能体、Agent）；多智能体系统（Multi-Agent System、MAS、多智能体协作）；工具调用（Function Calling、Tool Use、函数调用）；A2A（Agent-to-Agent、Agent2Agent 协议）；ReAct（Reasoning and Acting）；Agent 记忆（Agent Memory、长期记忆）；Computer Use（计算机使用、屏幕操作 Agent）；LangChain（LangChain 框架）；LangGraph（LangGraph 编排）；LlamaIndex（LlamaIndex 框架）；AutoGen（Microsoft AutoGen）；CrewAI（CrewAI 框架）；Dify（Dify 平台）
- **编码工具与 IDE**（13）：AI IDE（AI 集成开发环境、AI-native IDE）；AI 编码助手（Coding Assistant、代码助手）；Cursor（Cursor IDE、Anysphere Cursor）；GitHub Copilot（Copilot）；Windsurf（Windsurf IDE、Codeium）；Trae（Trae IDE）；Claude Code（Claude Code CLI）；Codex（OpenAI Codex、Codex CLI）；Devin（Devin AI）；OpenHands（OpenHands 框架、原 OpenDevin）；Aider（Aider CLI）；Cline（Cline 插件）；Vibe Coding（氛围编程）
- **应用与产品**（15）：ChatGPT（chatgpt.com）；Perplexity（Perplexity AI）；NotebookLM（NotebookLM 产品）；Microsoft 365 Copilot（M365 Copilot、Office Copilot）；Deep Research（深度研究）；AI 搜索（AI Search、答案引擎）；Midjourney（MJ）；Sora（OpenAI Sora）；Suno（Suno AI）；ElevenLabs（ElevenLabs 语音）；Lovable（Lovable.dev）；Bolt.new（Bolt）；v0（v0.dev）；Replit Agent（Replit）；Manus（Manus AI）
- **概念与评估**（11）：大语言模型（LLM、Large Language Model、大模型）；生成式 AI（Generative AI、AIGC）；开源权重模型（Open-Weights Model、开放权重）；上下文窗口（Context Window、上下文长度）；Token（词元）；幻觉（Hallucination、模型幻觉）；微调（Fine-tuning、SFT、监督微调）；RLHF（基于人类反馈的强化学习、Reinforcement Learning from Human Feedback）；蒸馏（Distillation、模型蒸馏）；Prompt 工程（Prompt Engineering、提示词工程）；GAIA（GAIA 基准）
<!-- VOCAB-SYNC:END -->

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-21 | 初始版本 | 新建 `content/tech/ai-application/trends` 月度业务线（竞争情报监测型）；替代已停用的 `ai-application/weekly-roundup`；定义全球 AI 应用竞争格局监测玩家分层、追踪表、信号触发器与 R1–R6 阈值 |
