# AI 应用趋势周报（大模型 · Agent · 编码 · 商业化）· 业务配置（business-config）

> **定位**：`content/tech/ai-application/weekly-roundup` 业务线的单一事实源。变量、受众、主题矩阵、来源分级、触发器、交付格式一律以本文件为准；周期提示词不复制这些内容，只给路径。
> **拆分说明**：本业务线由 `content/tech/weekly-roundup`（AI 趋势周报，安全 × Agent 生态合并线）拆分而来，承接原合并线的 **AI 应用侧** 板块（大模型与 Agent 技术演进 / AI 编码与开发工具 / AI 应用与商业化）；AI 安全侧板块（AI 安全与红队 / 基准与评估可信度）归 `content/tech/ai-security/weekly-roundup`。原合并周报（2026-11-13 / 2026-11-20）已移入 `sources/legacy/`，不再作为活跃报告。
> **类型继承声明（四层体系）**：业务提示词 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（行业趋势周报型 trend-weekly）](../../../../../engine/templates/trend-weekly/prompt-weekly-monitor-template.md) × 本文件。冲突时以业务提示词为准。

---

## 一、变量区（固定值）

```
{{REGION}}               = 全球
{{TOPIC}}                = AI 应用趋势周报
{{REPORT_TYPE}}          = trend-weekly
{{CADENCE}}              = 周（weekly，日历节拍）
{{REGISTRY_PATH}}        = data/processed/tech/ai-application/weekly-roundup/ai_application_trend_ledger.md
{{REGISTRY_FORMAT}}      = md-ledger
{{SOURCE_REGISTRY_PATH}} = data/processed/tech/ai-application/weekly-roundup/source_registry.json
{{BASELINE_REPORT_PATH}} = sources/legacy/2026-11-13_weekly.html（原合并首期，结构与结论锚；本线以首期应用侧板块为锚，未单独出基线文档）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/ai-application/weekly-roundup
{{FRESHNESS_PRIORITY}}   = 最新官方页 > 上期值 > 预测值
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
```

## 二、受众定位

- **受众**：AI Agent 开发团队 · 大模型应用工程（Agent Dev），兼及关注 AI 应用商业化的产品与战略读者。
- **视角**：从 Agent 架构 / 编码工具链 / 应用采用与商业模式出发，解读 LLM 与 Agent 生态的可落地趋势。
- **结论边界**：可执行启示只给「条件 → 判读 → 框架性含义 → 风险提示」，不给具体买卖价位与仓位建议。

## 三、主题矩阵（固定 3 块，对应周报 s2–s4，不得增删）

| 板块 | 周报节 | 覆盖范围 | 不覆盖 |
|---|---|---|---|
| 大模型与 Agent 技术演进 | s2 | 新模型发布与能力基准、Agent 架构与协议（MCP / A2A / 工具调用 / 记忆）、成本与效率 | 非 LLM 的传统 ML 进展；AI 安全攻击面（归 AI 安全趋势周报） |
| AI 编码与开发工具 | s3 | AI IDE、编码 Agent 与 CLI、开发工作流变化 | 非开发类通用应用与消费级产品动态 |
| AI 应用与商业化 | s4 | 应用产品采用与支出、定价与商业模式、垂直与区域落地、融资并购 | 未落数据的传闻与未发布产品爆料；通用软件漏洞（非 AI 相关） |

> **拆分依据**：原合并线 5 块中，AI 安全与红队、基准与评估可信度两块划归 `content/tech/ai-security/weekly-roundup`；本线保留大模型与 Agent 技术演进、AI 编码与开发工具、AI 应用与商业化三块。

## 四、来源分级（四层实例化）

| 层级 | 机构清单（示例，持续维护） | 采信规则 |
|---|---|---|
| ① 官方一手 | OpenAI、Anthropic、Google、Meta AI、Mistral、DeepSeek、阿里（Qwen）、智谱、Moonshot、字节（豆包）、百度、GitHub、Cursor、Anysphere、Cognition、SEC EDGAR、LangChain / LlamaIndex / Dify 官方文档 | 唯一可直接采信层，标「已核验」 |
| ② 行业机构 | OWASP GenAI、Gartner、Grand View Research、SWE-bench / GAIA 等基准官方页 | 可采信；PDF 记录发布日期；预测分歧并列 |
| ③ 挂牌门户 / 数据库 | Arena 评分、Artificial Analysis、基准排行榜 | 仅作状态快照，须注日期与版本 |
| ④ 媒体转述 | 36kr、InfoQ、The Information、Reuters、钛媒体、新浪财经、腾讯云社区、CSDN、Bloomberg | 只作线索；数值标「需核实原文」并回官方页校验 |

## 五、触发器（`事件 → 受影响板块`）

- 重大模型发布 / 重大 Agent 协议或框架更新（MCP / A2A 新版本、框架大版本）→ s2 当期升级
- 编码工具重大发布、定价调整或基准成绩突破 → s3 当期升级
- 头部厂商融资 / IPO / 定价重构 / 采用数据披露 → s4 当期升级

## 六、交付格式与命名

- **纯 HTML 交付**（业务配置声明，走 monitoring-common-spec 第 1 节例外条款）：富样式手写自包含 HTML 为主交付物，落盘 `reports/{{YYYY-MM-DD}}_weekly.html`（日期 = 数据截止日）；md 源稿存 `sources/` 同名存档，**不参与 `md2html.py` 自动转换**（防止覆盖手工渲染）。
- 周报按归档保留策略滚动（weekly 12 期，超限移入 `reports/archives/`）。

## 七、信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：四级标注与摘要引用约束见 `engine/templates/information-layering-spec.md` 第二 / 四节；新增信息统计模块见第四节。
- **指针引用**：事实唯一定义于台账 / 事实卡片（`[FC-…]`），正文用「指标编号 + 指针」。
- **决策卡与行动协议**：核心判断输出决策卡；行动项字段与三档优先级见 `engine/templates/decision-delivery-spec.md` 第三节。
- **阈值校准**：首次中期回测 2027-06；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节。
- **场景切片**：主场景 **投资决策**；次场景 **政策制定**。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」。
- **盲区**：P0 四类（就业 / 收入 / 空置 / 竣工）优先消号。

---

<!-- VOCAB-SYNC:BEGIN topic=tech do-not-edit -->
## 词汇速览 · 科技（词汇库自动同步）

> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 tech v1.4，共 71 条（同步于 2026-11-20T15:48:13）。标记区间内请勿手工编辑；词条变更走词汇库导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。

- **模型与厂商**（19）：多模态模型（Multimodal Model、多模态）；推理模型（Reasoning Model、推理增强模型、思维链模型）；OpenAI（openai.com）；Anthropic（anthropic.com）；Google DeepMind（谷歌deepmind、Google AI）；Meta AI（Meta、Facebook AI）；xAI（X.AI、xAI 公司）；Mistral AI（Mistral）；DeepSeek（深度求索）；阿里通义千问（Qwen、通义千问）；智谱 GLM（GLM、Zhipu AI、智谱AI）；月之暗面 Kimi（Moonshot AI、Kimi）；字节豆包（Doubao、豆包大模型）；百度文心（ERNIE、文心一言）；GPT（GPT 系列、GPT-4、GPT-5）；Claude（Claude 系列、Claude Sonnet、Claude Opus）；Gemini（Gemini 系列）；Llama（Llama 系列、Llama 开源）；Grok（Grok 系列）
- **Agent 技术与框架**（13）：AI Agent（智能体、Agent）；多智能体系统（Multi-Agent System、MAS、多智能体协作）；工具调用（Function Calling、Tool Use、函数调用）；A2A（Agent-to-Agent、Agent2Agent 协议）；ReAct（Reasoning and Acting）；Agent 记忆（Agent Memory、长期记忆）；Computer Use（计算机使用、屏幕操作 Agent）；LangChain（LangChain 框架）；LangGraph（LangGraph 编排）；LlamaIndex（LlamaIndex 框架）；AutoGen（Microsoft AutoGen）；CrewAI（CrewAI 框架）；Dify（Dify 平台）
- **编码工具与 IDE**（13）：AI IDE（AI 集成开发环境、AI-native IDE）；AI 编码助手（Coding Assistant、代码助手）；Cursor（Cursor IDE、Anysphere Cursor）；GitHub Copilot（Copilot）；Windsurf（Windsurf IDE、Codeium）；Trae（Trae IDE）；Claude Code（Claude Code CLI）；Codex（OpenAI Codex、Codex CLI）；Devin（Devin AI）；OpenHands（OpenHands 框架、原 OpenDevin）；Aider（Aider CLI）；Cline（Cline 插件）；Vibe Coding（氛围编程）
- **应用与产品**（15）：ChatGPT（chatgpt.com）；Perplexity（Perplexity AI）；NotebookLM（NotebookLM 产品）；Microsoft 365 Copilot（M365 Copilot、Office Copilot）；Deep Research（深度研究）；AI 搜索（AI Search、答案引擎）；Midjourney（MJ）；Sora（OpenAI Sora）；Suno（Suno AI）；ElevenLabs（ElevenLabs 语音）；Lovable（Lovable.dev）；Bolt.new（Bolt）；v0（v0.dev）；Replit Agent（Replit）；Manus（Manus AI）
- **概念与评估**（11）：大语言模型（LLM、Large Language Model、大模型）；生成式 AI（Generative AI、AIGC）；开源权重模型（Open-Weights Model、开放权重）；上下文窗口（Context Window、上下文长度）；Token（词元）；幻觉（Hallucination、模型幻觉）；微调（Fine-tuning、SFT、监督微调）；RLHF（基于人类反馈的强化学习、Reinforcement Learning from Human Feedback）；蒸馏（Distillation、模型蒸馏）；Prompt 工程（Prompt Engineering、提示词工程）；GAIA（GAIA 基准）
<!-- VOCAB-SYNC:END -->

## 八、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-20 | 初始版本 | 由 `content/tech/weekly-roundup` 拆分建立：承接 AI 应用侧三板块（大模型与 Agent 技术演进 / AI 编码与开发工具 / AI 应用与商业化）；原合并周报移入 `sources/legacy/`；AI 安全侧归 `content/tech/ai-security/weekly-roundup` |
