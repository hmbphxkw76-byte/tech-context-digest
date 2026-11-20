# AI 安全趋势周报（攻击面 · 红队 · 基准可信度）· 业务配置（business-config）

> **定位**：`content/tech/ai-security/weekly-roundup` 业务线的单一事实源。变量、受众、主题矩阵、来源分级、触发器、交付格式一律以本文件为准；周期提示词不复制这些内容，只给路径。
> **拆分说明**：本业务线由 `content/tech/weekly-roundup`（AI 趋势周报，安全 × Agent 生态合并线）拆分而来，承接原合并线的 **AI 安全侧** 板块（AI 安全与红队 / 基准与评估可信度）；AI 应用侧板块（大模型与 Agent 技术演进 / AI 编码与开发工具 / AI 应用与商业化）归 `content/tech/ai-application/weekly-roundup`。原合并周报（2026-11-13 / 2026-11-20）已移入 `sources/legacy/`，不再作为活跃报告。
> **类型继承声明（四层体系）**：业务提示词 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（行业趋势周报型 trend-weekly）](../../../../../engine/templates/trend-weekly/prompt-weekly-monitor-template.md) × 本文件。冲突时以业务提示词为准。

---

## 一、变量区（固定值）

```
{{REGION}}               = 全球
{{TOPIC}}                = AI 安全趋势周报
{{REPORT_TYPE}}          = trend-weekly
{{CADENCE}}              = 周（weekly，日历节拍）
{{REGISTRY_PATH}}        = data/processed/tech/ai-security/weekly-roundup/ai_security_trend_ledger.md
{{REGISTRY_FORMAT}}      = md-ledger
{{SOURCE_REGISTRY_PATH}} = data/processed/tech/ai-security/weekly-roundup/source_registry.json
{{BASELINE_REPORT_PATH}} = sources/legacy/2026-11-13_weekly.html（原合并首期，安全侧结构与结论锚；本线未单独出基线文档）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/ai-security/weekly-roundup
{{FRESHNESS_PRIORITY}}   = 最新官方页 > 上期值 > 预测值
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
```

## 二、受众定位

- **受众**：AI 安全技术负责人 · 红队工程（工具链：PyRIT / promptfoo / garak），兼及 AI 治理与合规读者。
- **视角**：从攻击面、评估基准、红队工程实践与标准框架出发，解读 LLM 与 Agent 生态的安全趋势。
- **结论边界**：可执行启示只给「条件 → 判读 → 框架性含义 → 风险提示」，不给具体买卖价位与仓位建议。

## 三、主题矩阵（固定 2 块，对应周报 s2–s3，不得增删）

| 板块 | 周报节 | 覆盖范围 | 不覆盖 |
|---|---|---|---|
| AI 安全与红队 | s2 | 攻击面与真实事件、标准与框架（EU AI Act / OWASP / NIST AI RMF）、安全市场与竞争 | 通用软件漏洞（非 AI 相关）；AI 应用商业化（归 AI 应用趋势周报） |
| 基准与评估可信度 | s3 | 基准版本/退役/污染审计、评估方法演进、人类基线、基准饱和 | 与具体模型能力无关的纯学术指标；AI 编码工具动态（归 AI 应用趋势周报） |

> **拆分依据**：原合并线 5 块中，大模型与 Agent 技术演进、AI 编码与开发工具、AI 应用与商业化三块划归 `content/tech/ai-application/weekly-roundup`；本线保留 AI 安全与红队、基准与评估可信度两块。

## 四、来源分级（四层实例化）

| 层级 | 机构清单（示例，持续维护） | 采信规则 |
|---|---|---|
| ① 官方一手 | Microsoft Security Blog、OpenAI、Anthropic、Google、Meta AI、Mistral、DeepSeek、SEC EDGAR、EU 官方（EUR-Lex）、METR、Stanford HAI、Notion | 唯一可直接采信层，标「已核验」 |
| ② 行业机构 | OWASP GenAI、Gartner、Grand View Research、SWE-bench / GAIA / HarmBench 等基准官方页、LangChain / LlamaIndex 官方文档 | 可采信；PDF 记录发布日期；预测分歧并列 |
| ③ 挂牌门户 / 数据库 | Arena 评分、Artificial Analysis、基准排行榜 | 仅作状态快照，须注日期与版本 |
| ④ 媒体转述 | 36kr、InfoQ、The Information、Reuters、钛媒体、新浪财经、CSDN、Bloomberg | 只作线索；数值标「需核实原文」并回官方页校验 |

## 五、触发器（`事件 → 受影响板块`）

- 重大安全事件 / 重大模型发布（涉及攻击面）→ s2 当期升级
- 监管与标准动作（法案生效节点、Top 10 更新）→ s2 当期升级
- 评估基准退役或缺陷披露 → s3 当期升级

## 六、交付格式与命名

- **纯 HTML 交付**（业务配置声明，走 monitoring-common-spec 第 1 节例外条款）：富样式手写自包含 HTML 为主交付物，落盘 `reports/{{YYYY-MM-DD}}_weekly.html`（日期 = 数据截止日）；md 源稿存 `sources/` 同名存档，**不参与 `md2html.py` 自动转换**（防止覆盖手工渲染）。
- 周报按归档保留策略滚动（weekly 12 期，超限移入 `reports/archives/`）。

## 七、信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：四级标注与摘要引用约束见 `engine/templates/information-layering-spec.md` 第二 / 四节；新增信息统计模块见第四节。
- **指针引用**：事实唯一定义于台账 / 事实卡片（`[FC-…]`），正文用「指标编号 + 指针」。
- **决策卡与行动协议**：核心判断输出决策卡；行动项字段与三档优先级见 `engine/templates/decision-delivery-spec.md` 第三节。
- **阈值校准**：首次中期回测 2027-06；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节。
- **场景切片**：主场景 **政策制定**；次场景 **投资决策**。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」。
- **盲区**：P0 四类（就业 / 收入 / 空置 / 竣工）优先消号。

---

<!-- VOCAB-SYNC:BEGIN topic=tech do-not-edit -->
## 词汇速览（词汇库自动同步）

> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 tech v1.4，共 49 条（同步于 2026-11-20T15:48:13）。标记区间内请勿手工编辑；词条变更走词汇库导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。

- **攻击技术**（13）：提示注入（Prompt Injection、PI）；间接提示注入（Indirect Prompt Injection、IPI）；越狱（Jailbreak、LLM 越狱）；数据投毒（Data Poisoning、训练数据投毒）；模型投毒（Model Poisoning、权重投毒）；后门攻击（Backdoor Attack、木马化模型）；模型窃取（Model Extraction、Model Theft、模型提取攻击）；训练数据提取（Training Data Extraction、模型反演、Model Inversion）；成员推断（Membership Inference）；Agent 工具滥用（Agent Tool Abuse、Confused Deputy、越权工具调用）；多模态注入（Multimodal Injection、跨模态注入）；提示词泄露（Prompt Leaking、系统提示提取）；凭据窃取（Credential Theft、凭据盗取）
- **防御与检测**（11）：威胁情报（Threat Intelligence、CTI）；护栏（Guardrails、LLM Guardrails、安全护栏）；提示注入检测（Prompt Injection Detection）；RAG 安全（检索增强生成安全、RAG Security）；DLP（Data Loss Prevention、数据防泄漏）；DSPM（Data Security Posture Management、数据安全态势管理）；Shadow AI（影子 AI、未申报 AI 使用）；零信任（Zero Trust、ZT）；EDR（Endpoint Detection and Response、端点检测与响应）；AI 事件响应（AI Incident Response）；模型水印（Model Watermarking、AI 内容溯源）
- **工具与平台**（3）：PyRIT（Microsoft PyRIT）；promptfoo；garak（LLM vulnerability scanner）
- **框架与标准**（8）：模型上下文协议（MCP、Model Context Protocol）；OWASP Top 10 for LLM Applications（LLM Top 10、OWASP LLM Top 10）；OWASP Agentic Top 10（Agentic AI Top 10）；NIST AI RMF（AI 风险管理框架、AI Risk Management Framework）；EU AI Act（欧盟人工智能法案、Regulation (EU) 2024/1689）；ISO/IEC 42001（AI 管理体系、AIMS）；MITRE ATT&CK（ATT&CK）；MITRE ATLAS（ATLAS、Adversarial Threat Landscape for AI Systems）
- **认证与资质**（4）：AI 红队认证考试（AI Red Team Certification、AI 红队认证）；AAIS（ISACA Advanced in AI Security、ISACA AI 安全高级认证）；AIGP（AI Governance Professional、IAPP AIGP）；CISSP（注册信息系统安全专家）
- **组织与岗位**（5）：红队（Red Team、攻击模拟队）；蓝队（Blue Team、防御团队）；紫队（Purple Team）；AI 红队（AI Red Team、LLM 红队、AI Red Teaming）；SOC（Security Operations Center、安全运营中心）
- **基准与评估**（5）：SWE-bench（SWE-bench Verified、SWE-bench 基准）；OSWorld（OSWorld 基准）；HarmBench（HarmBench 基准）；人类基线（Human Baseline）；基准饱和（Benchmark Saturation）
<!-- VOCAB-SYNC:END -->

## 八、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 由 trends/ai-security 与 trends/ai-agent 合并建立：五主题矩阵（s2–s6）、来源分级与触发器并集、共用台账与词汇库；原两线历史报告与 md 源稿迁移至 `reports/legacy/` 与 `sources/legacy/` |
| v1.1 | 2026-11-20 | 拆分 | 由合并线 `content/tech/weekly-roundup` 拆分：本线承接 AI 安全侧两板块（AI 安全与红队 / 基准与评估可信度），主题矩阵收敛为 2 块；AI 应用侧归 `content/tech/ai-application/weekly-roundup`；原合并周报移入 `sources/legacy/` |
