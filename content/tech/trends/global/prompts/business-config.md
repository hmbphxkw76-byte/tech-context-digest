# AI 趋势周报（安全 × Agent 生态）· 业务配置（business-config）

> **定位**：`content/tech/trends/global` 业务线的单一事实源。变量、受众、主题矩阵、来源分级、触发器、交付格式一律以本文件为准；周期提示词不复制这些内容，只给路径。
> **合并说明**：本业务线由 `trends/ai-security`（AI 安全趋势周报）与 `trends/ai-agent`（AI Agent 与大模型趋势周报）合并而成，主题板块由两线各 3 块去重整合为 5 块，共用本台账与词汇库。
> **类型继承声明（四层体系）**：业务提示词 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（行业趋势周报型 trend-weekly）](../../../../../engine/templates/trend-weekly/prompt-weekly-monitor-template.md) × 本文件。冲突时以业务提示词为准。

---

## 一、变量区（固定值）

```
{{REGION}}               = 全球
{{TOPIC}}                = AI 行业趋势（安全 × Agent 生态）
{{REPORT_TYPE}}          = trend-weekly
{{CADENCE}}              = 周（weekly，日历节拍）
{{REGISTRY_PATH}}        = data/processed/tech/trends/global/ai_trend_ledger.md
{{REGISTRY_FORMAT}}      = md-ledger
{{SOURCE_REGISTRY_PATH}} = data/processed/tech/trends/global/source_registry.json
{{BASELINE_REPORT_PATH}} = reports/2026-11-13_weekly.html（首期周报，本业务线的结构与结论锚；机制建立走周报首期，未单独出九节基线文档）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/trends/global
{{FRESHNESS_PRIORITY}}   = 最新官方页 > 上期值 > 预测值
{{SOURCE_LANGUAGE_RULE}} = 官方一手以英文为准；中文媒体仅作线索，数值须回官方页核验
```

## 二、受众定位

- **受众**：① AI 安全技术负责人 · 红队工程（工具链：PyRIT / promptfoo / garak）；② AI Agent 开发团队 · 大模型应用工程（Agent Dev）。
- **视角**：从攻击面、评估基准、红队工程实践与 Agent 架构/编码工具链出发，解读 LLM 与 Agent 生态的可落地趋势。
- **结论边界**：可执行启示只给「条件 → 判读 → 框架性含义 → 风险提示」，不给具体买卖价位与仓位建议。

## 三、主题矩阵（固定 5 块，对应周报 s2–s6，不得增删）

| 板块 | 周报节 | 覆盖范围 | 不覆盖 |
|---|---|---|---|
| AI 安全与红队 | s2 | 攻击面与真实事件、标准与框架（EU AI Act / OWASP / NIST AI RMF）、安全市场与竞争 | 通用软件漏洞（非 AI 相关） |
| 大模型与 Agent 技术演进 | s3 | 新模型发布与能力基准、Agent 架构与协议（MCP / A2A / 工具调用 / 记忆）、成本与效率 | 非 LLM 的传统 ML 进展 |
| AI 编码与开发工具 | s4 | AI IDE、编码 Agent 与 CLI、开发工作流变化 | 非开发类通用应用与消费级产品动态 |
| AI 应用与商业化 | s5 | 应用产品采用与支出、定价与商业模式、垂直与区域落地、融资并购 | 未落数据的传闻与未发布产品爆料 |
| 基准与评估可信度 | s6 | 基准版本/退役/污染审计、评估方法演进、人类基线、基准饱和 | 与具体模型能力无关的纯学术指标 |

> **合并依据**：原 ai-security 的「LLM 与 Agent 技术演进」与原 ai-agent 的「大模型与 Agent 技术演进」合并为 s3；两线同名的「AI 应用与商业化」合并为 s5；两线共同密集跟踪的基准可信度问题（SWE-bench / OSWorld / HarmBench / GAIA / Terminal-Bench）独立为 s6，避免散落重复。

## 四、来源分级（四层实例化）

| 层级 | 机构清单（示例，持续维护） | 采信规则 |
|---|---|---|
| ① 官方一手 | Microsoft Security Blog、OpenAI、Anthropic、Google、Meta AI、Mistral、DeepSeek、阿里（Qwen）、智谱、Moonshot、字节（豆包）、百度、GitHub、Cursor、Anysphere、Cognition、SEC EDGAR、EU 官方（EUR-Lex）、METR、Stanford HAI、Notion | 唯一可直接采信层，标「已核验」 |
| ② 行业机构 | OWASP GenAI、Gartner、Grand View Research、SWE-bench / GAIA 等基准官方页、LangChain / LlamaIndex / Dify 官方文档 | 可采信；PDF 记录发布日期；预测分歧并列 |
| ③ 挂牌门户 / 数据库 | Arena 评分、Artificial Analysis、基准排行榜 | 仅作状态快照，须注日期与版本 |
| ④ 媒体转述 | 36kr、InfoQ、央广网、The Information、Reuters、钛媒体、新浪财经、腾讯云社区、网易、CSDN、百度百科、博客园、17173、Bloomberg | 只作线索；数值标「需核实原文」并回官方页校验 |

## 五、触发器（`事件 → 受影响板块`）

- 重大模型发布 / 重大安全事件 → s2、s3 当期升级
- 监管与标准动作（法案生效节点、Top 10 更新）→ s2 当期升级
- Agent 协议与框架重大更新（MCP / A2A 新版本、框架大版本发布）→ s3 当期升级
- 编码工具重大发布、定价调整或基准成绩突破 → s4 当期升级
- 头部厂商融资 / IPO / 定价重构 / 采用数据披露 → s5 当期升级
- 评估基准退役或缺陷披露 → s6 当期升级

## 六、交付格式与命名

- **纯 HTML 交付**（业务配置声明，走 monitoring-common-spec 第 1 节例外条款）：富样式手写自包含 HTML 为主交付物，落盘 `reports/{{YYYY-MM-DD}}_weekly.html`（日期 = 数据截止日）；md 源稿存 `sources/` 同名存档，**不参与 `md2html.py` 自动转换**（防止覆盖手工渲染）。
- 周报按归档保留策略滚动（weekly 12 期，超限移入 `reports/archives/`）。

<!-- VOCAB-SYNC:BEGIN topic=ai-security do-not-edit -->
## 词汇速览 · AI 安全（词汇库自动同步）

> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 ai-security v1.3，共 49 条（同步于 2026-11-14T15:24:27）。标记区间内请勿手工编辑；词条变更走词汇库导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。

- **攻击技术**（12）：提示注入（Prompt Injection、PI）；间接提示注入（Indirect Prompt Injection、IPI）；越狱（Jailbreak、LLM 越狱）；数据投毒（Data Poisoning、训练数据投毒）；模型投毒（Model Poisoning、权重投毒）；后门攻击（Backdoor Attack、木马化模型）；模型窃取（Model Extraction、Model Theft、模型提取攻击）；训练数据提取（Training Data Extraction、模型反演、Model Inversion）；成员推断（Membership Inference）；Agent 工具滥用（Agent Tool Abuse、Confused Deputy、越权工具调用）；多模态注入（Multimodal Injection、跨模态注入）；提示词泄露（Prompt Leaking、系统提示提取）
- **防御与检测**（11）：威胁情报（Threat Intelligence、CTI）；护栏（Guardrails、LLM Guardrails、安全护栏）；提示注入检测（Prompt Injection Detection）；RAG 安全（检索增强生成安全、RAG Security）；DLP（Data Loss Prevention、数据防泄漏）；DSPM（Data Security Posture Management、数据安全态势管理）；Shadow AI（影子 AI、未申报 AI 使用）；零信任（Zero Trust、ZT）；EDR（Endpoint Detection and Response、端点检测与响应）；AI 事件响应（AI Incident Response）；模型水印（Model Watermarking、AI 内容溯源）
- **工具与平台**（3）：PyRIT（Microsoft PyRIT）；promptfoo；garak（LLM vulnerability scanner）
- **框架与标准**（8）：OWASP Top 10 for LLM Applications（LLM Top 10、OWASP LLM Top 10）；OWASP Agentic Top 10（Agentic AI Top 10）；NIST AI RMF（AI 风险管理框架、AI Risk Management Framework）；EU AI Act（欧盟人工智能法案、Regulation (EU) 2024/1689）；ISO/IEC 42001（AI 管理体系、AIMS）；MITRE ATT&CK（ATT&CK）；MITRE ATLAS（ATLAS、Adversarial Threat Landscape for AI Systems）；模型上下文协议（MCP、Model Context Protocol）
- **认证与资质**（4）：AI 红队认证考试（AI Red Team Certification、AI 红队认证）；AAIS（ISACA Advanced in AI Security、ISACA AI 安全高级认证）；AIGP（AI Governance Professional、IAPP AIGP）；CISSP（注册信息系统安全专家）
- **组织与岗位**（5）：红队（Red Team、攻击模拟队）；蓝队（Blue Team、防御团队）；紫队（Purple Team）；AI 红队（AI Red Team、LLM 红队、AI Red Teaming）；SOC（Security Operations Center、安全运营中心）
- **基准与评估**（6）：SWE-bench Verified（SWE-bench）；OSWorld（OSWorld 基准）；HarmBench（HarmBench 基准）；人类基线（Human Baseline）；幻觉（Hallucination、模型幻觉）；基准饱和（Benchmark Saturation）
<!-- VOCAB-SYNC:END -->

<!-- VOCAB-SYNC:BEGIN topic=ai-agent do-not-edit -->
## 词汇速览 · AI Agent（词汇库自动同步）

> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 ai-agent v1.2，共 73 条（同步于 2026-11-14T15:24:27）。标记区间内请勿手工编辑；词条变更走词汇库导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。

- **模型与厂商**（19）：多模态模型（Multimodal Model、多模态）；推理模型（Reasoning Model、推理增强模型、思维链模型）；OpenAI（openai.com）；Anthropic（anthropic.com）；Google DeepMind（谷歌deepmind、Google AI）；Meta AI（Meta、Facebook AI）；xAI（X.AI、xAI 公司）；Mistral AI（Mistral）；DeepSeek（深度求索）；阿里通义千问（Qwen、通义千问）；智谱 GLM（GLM、Zhipu AI、智谱AI）；月之暗面 Kimi（Moonshot AI、Kimi）；字节豆包（Doubao、豆包大模型）；百度文心（ERNIE、文心一言）；GPT（GPT 系列、GPT-4、GPT-5）；Claude（Claude 系列、Claude Sonnet、Claude Opus）；Gemini（Gemini 系列）；Llama（Llama 系列、Llama 开源）；Grok（Grok 系列）
- **Agent 技术与框架**（14）：AI Agent（智能体、Agent）；多智能体系统（Multi-Agent System、MAS、多智能体协作）；工具调用（Function Calling、Tool Use、函数调用）；模型上下文协议（MCP、Model Context Protocol）；A2A（Agent-to-Agent、Agent2Agent 协议）；ReAct（Reasoning and Acting）；Agent 记忆（Agent Memory、长期记忆）；Computer Use（计算机使用、屏幕操作 Agent）；LangChain（LangChain 框架）；LangGraph（LangGraph 编排）；LlamaIndex（LlamaIndex 框架）；AutoGen（Microsoft AutoGen）；CrewAI（CrewAI 框架）；Dify（Dify 平台）
- **编码工具与 IDE**（13）：AI IDE（AI 集成开发环境、AI-native IDE）；AI 编码助手（Coding Assistant、代码助手）；Cursor（Cursor IDE、Anysphere Cursor）；GitHub Copilot（Copilot）；Windsurf（Windsurf IDE、Codeium）；Trae（Trae IDE）；Claude Code（Claude Code CLI）；Codex（OpenAI Codex、Codex CLI）；Devin（Devin AI）；OpenHands（OpenHands 框架、原 OpenDevin）；Aider（Aider CLI）；Cline（Cline 插件）；Vibe Coding（氛围编程）
- **应用与产品**（15）：ChatGPT（chatgpt.com）；Perplexity（Perplexity AI）；NotebookLM（NotebookLM 产品）；Microsoft 365 Copilot（M365 Copilot、Office Copilot）；Deep Research（深度研究）；AI 搜索（AI Search、答案引擎）；Midjourney（MJ）；Sora（OpenAI Sora）；Suno（Suno AI）；ElevenLabs（ElevenLabs 语音）；Lovable（Lovable.dev）；Bolt.new（Bolt）；v0（v0.dev）；Replit Agent（Replit）；Manus（Manus AI）
- **概念与评估**（12）：大语言模型（LLM、Large Language Model、大模型）；生成式 AI（Generative AI、AIGC）；开源权重模型（Open-Weights Model、开放权重）；上下文窗口（Context Window、上下文长度）；Token（词元）；幻觉（Hallucination、模型幻觉）；微调（Fine-tuning、SFT、监督微调）；RLHF（基于人类反馈的强化学习、Reinforcement Learning from Human Feedback）；蒸馏（Distillation、模型蒸馏）；Prompt 工程（Prompt Engineering、提示词工程）；SWE-bench（SWE-bench Verified、SWE-bench 基准）；GAIA（GAIA 基准）
<!-- VOCAB-SYNC:END -->

## 七、信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：已核验 / 部分核验 / 推断 / 假设；决策摘要仅引用已核验 + 部分核验；新增信息模块「本期新增 X / 修正 Y / 无变化 Z / 假设核验进度 k/n」。
- **指针引用**：事实唯一定义于台账 / 事实卡片（`[FC-…]`），正文用「指标编号 + 指针」。
- **决策卡与行动协议**：核心判断输出决策卡；行动项按「触发条件 + 阈值 + 责任角色 + 时限 + 验证指标」并分三档优先级（规范：`engine/templates/decision-delivery-spec.md`）。
- **阈值校准**：首次中期回测 2027-06；校准完成前信号灯标注「预校准（ex-ante）」。
- **场景切片**：主场景 **政策制定**；次场景 **投资决策**。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」。
- **盲区**：P0 四类（就业 / 收入 / 空置 / 竣工）优先消号。

---

## 八、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 由 trends/ai-security 与 trends/ai-agent 合并建立：五主题矩阵（s2–s6）、来源分级与触发器并集、共用台账与词汇库；原两线历史报告与 md 源稿迁移至 `reports/legacy/` 与 `sources/legacy/` |
