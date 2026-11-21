# 迪拜 AI 应用就业 · 业务专属配置（business-config）

> **定位**：本文件是 `content/tech/ai-application/dubai` 业务线的**单一业务事实源**：运行变量固定值、来源优先级实例化、受众定位、术语口径、触发器、指标追踪清单、已修正事实清单全部集中于此。周期提示词（基线 / 月）引用本文件，业务参数只在这里维护一份。
>
> **继承声明（四层体系）**：周期提示词 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [类型模板](../../../../../engine/templates/employment-research/)（职业就业调研型）× 本文件。通用层修改自动对本业务线生效；本文件修改只影响本业务线。冲突时以周期提示词 ＞ 本文件 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、运行变量固定值

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = AI 应用就业
{{REPORT_TYPE}}          = employment-research
{{BASELINE_DATE}}        = 2026-11-21（基线报告完稿日期）
{{REGISTRY_PATH}}        = data/processed/tech/ai-application/dubai/ai_application_employment_indicator_registry.md
{{REGISTRY_FORMAT}}      = md-table
{{SOURCE_REGISTRY_PATH}} = data/processed/tech/ai-application/dubai/source_registry.json
{{BASELINE_REPORT_PATH}} = reports/2026-11_baseline_report.html
{{FRESHNESS_PRIORITY}}   = 近 12 个月内数据优先；超过 24 个月须标注年份并谨慎使用
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/ai-application/dubai
```

**各周期落盘规则**（employment-research 类型模板第四节的实例化；命名对齐仓库工具链，版本号写入报告内）：

| 节拍 | 输出路径 | 定位 | 上期报告 |
|---|---|---|---|
| 基线 | `reports/2026-11_baseline_report.html` | 对比锚，常驻顶层 | 无 |
| 月度 | `reports/{{YYYY-MM}}_monthly.html` | 主更新节拍，九节全模块刷新 | 最近一期月度报告 + 基线 |

**输出格式**：纯 HTML 交付（业务配置声明，走 monitoring-common-spec 第 1 节例外条款）：canonical 富样式自包含 HTML 为主交付物，落盘 `reports/{{周期}}.html`。本任务范围不含 md 源稿；后续如补 md 源稿，存 `sources/` 同名存档，**不参与 `md2html.py` 自动转换**（防止覆盖手工渲染）。

## 二、受众定位

面向「拟赴迪拜从事 AI 应用岗位就业」的读者（AI/ML 工程师、数据工程师 / 数据科学家、AI 产品经理、MLOps、AI 解决方案架构师、提示词 / AI 运营、AI 治理等），兼具行业分析与职业规划顾问视角。报告允许给出框架性求职路径建议（标「建议 / 推断」），不承诺就业结果、不保证薪资水平。

**与 AI 安全线的边界**：本业务线监测 **AI 应用**岗位（应用落地、数据与模型工程、产品与运营、治理），不监测 AI 安全攻防岗位；两线共享事实卡片库 `engine/fact_cards/security_fact_cards.json`，但岗位、薪酬、证书口径各自独立。

## 三、术语口径区分（表格与正文中不得混用）

- 基本工资 ≠ 总额（总包）：黄金签证门槛、离职补偿（Gratuity）均以**基本工资**计
- 名义薪资 ≠ 净薪（阿联酋 0% 个税、外籍 0% 社保，ILOE 为唯一强制扣减）≠ 总包价值（含房补 / 教育 / 机票 / 奖金）
- **UAE AI 市场全国规模** ≠ **迪拜 AI 市场份额**：IMARC 给出全国规模与「迪拜占全国 45.6%」两个口径，不可互相替代
- **岗位需求增速** ≠ **岗位总量**：LinkedIn「AI Engineering job demand +232.4%」为同比增速，非岗位数量
- **招聘机构抽样** ≠ **薪酬指南官方年版**（前者标注「抽样」并谨慎引用）
- 汇率固定：1 USD = 3.6725 AED（钉住）

## 四、来源优先级（通用基座第四节的实例化，冲突时报双份并标注）

① 阿联酋/迪拜政府官方（u.ae、dub.ai、digitaldubai.ae、difc.ae、dic.ae、dmcc.ae、adgm.com、mediaoffice.ae、WAM 英文、各自由区官网）
＞ ② 国际权威组织 / 平台经济数据（LinkedIn Economic Graph、IMARC、Michael Page、Hays、Cooper Fitch、Charterhouse、Robert Half）
＞ ③ 头部薪酬指南与招聘平台抽样（Michael Page、Hays、Cooper Fitch、Charterhouse、Robert Half；LinkedIn、Bayt、GulfTalent、Naukrigulf、foundit Gulf——仅作市场信号，不与官方 / 行业机构同等采信）
＞ ④ 英文行业/主流媒体（Khaleej Times、The National、Gulf News、Zawya、Reuters、Arab News——只用于发现线索，数值须回官方/原始页校验）

**来源语言规则**：仅英文（{{SOURCE_LANGUAGE_RULE}}），严禁中文来源；若某数据点仅在中文源出现，标注「未找到英文权威来源，已剔除」并说明。政策见 `engine/docs/source-language-policy.md`（门禁 `source_check` R9）。Michael Page / Hays / Cooper Fitch / Charterhouse 的薪酬分表若仅能经由非英文或二手摘要获取，须排除其未核实数字。

## 五、重大事件触发器（事件 → 受影响模块）

| 触发事件 | 受影响模块 |
|---|---|
| GITEX Global / Expand North Star 新一届举办（日期、主题、官方发布） | 市场趋势、雇主生态、落地路径 |
| Dubai AI Week / Global Prompt Engineering Championship 新一届 | 市场趋势、雇主生态、证书、落地路径 |
| Dubai Universal Blueprint for AI 新举措（Dubai AI Seal、Chief AI Officers、DCAI 进展） | 市场趋势、雇主生态 |
| UAE AI Strategy 2031 / 迪拜 AI 中心（DCAI）实施进展 | 市场趋势、人才供需 |
| LinkedIn《UAE Workforce Readiness Report》新年版发布 | 人才供需与薪酬 |
| 任一头部薪酬指南发布新年版（Michael Page / Hays / Cooper Fitch / Charterhouse） | 人才供需与薪酬 |
| 黄金签证 / MOHRE 职业分类 / 阿化（Emiratisation）规则变更 | 人才供需与薪酬、落地路径 |
| 新 AI 应用认证发布或云厂商（Microsoft / Google / AWS / Databricks）认证更新 | 技能要求、证书 |

## 六、指标追踪表（14 项，活值维护于 {{REGISTRY_PATH}}）

| # | 监测指标 | 口径/单位 | 优先数据源（英文） |
|---|---|---|---|
| 1 | UAE AI 市场规模 & CAGR | 亿美元 / % | imarcgroup.com |
| 2 | 迪拜占 UAE AI 市场份额 | % | imarcgroup.com |
| 3 | LinkedIn UAE 招聘率（同比） | % | linkedin-workforcereadiness.com |
| 4 | AI 工程岗需求增速 & 岗位占比 | % / % | linkedin-workforcereadiness.com |
| 5 | AI 工程人才集中度 & AI 素养人才增速 | % / % | linkedin-workforcereadiness.com |
| 6 | 阿联酋最快增长职业（AI 相关） | 排名 / 计数 | linkedin-workforcereadiness.com |
| 7 | 国际申请占比 | % | linkedin-workforcereadiness.com |
| 8 | Michael Page AI/Data 最热岗位 | 排名 | michaelpage.ae |
| 9 | Michael Page AI/Data 最缺技能 | 排名 | michaelpage.ae |
| 10 | 薪酬指南最新版次（AI/Data 分表） | 年版 | michaelpage.ae / charterhouseme.ae / hays.ae / cooperfitch.ae |
| 11 | AI 应用岗薪资抽样 | AED/月 | 待核实（公开指南 gated；相邻抽样 hiredeveloper.ae） |
| 12 | ILOE 费率 & 黄金签证门槛 | AED/月 / AED | iloe.ae / u.ae / icp.gov.ae |
| 13 | 迪拜 AI 园区 / 自由区企业数 | 家 | dub.ai / difc.ae |
| 14 | 代表性 AI 应用雇主动态 | — | 各公司官网 / WAM |

## 七、已修正事实清单（基线锚，防回退；无来源不得追加）

```
- ❌ 不得将 LinkedIn「AI Engineering job demand +232.4%」误读为「AI 应用岗位总量」——该数为 2026-08 阿联酋 AI 工程岗需求同比增速，同期仅占 UAE 岗位发布 4.1%。[Source: https://linkedin-workforcereadiness.com/, 2026]
- ❌ 不得将「UAE AI 市场规模」与「迪拜 AI 市场规模」混用——IMARC 2025 年全国 USD 705.7M，迪拜占全国 45.6%，两者口径不同。[Source: https://www.imarcgroup.com/uae-artificial-intelligence-market, 2026]
- ❌ 不得直接比较 Michael Page 与 Charterhouse 薪酬区间——Michael Page 为「含基本 + 房补 + 交通 + 津贴、不含奖金」的月薪；Charterhouse 为「gross monthly fixed compensation，不含福利」。[Source: https://www.michaelpage.ae/salary-guide, 2026；https://www.charterhouseme.ae/salary-levels-2026, 2026]
- ❌ 不得称「AI 应用岗薪资已核实」——公开薪酬指南 AI/Data 分表 gated，本基线薪资区间一律标「待核实」，仅给口径与相邻抽样。[Source: https://www.michaelpage.ae/salary-guide/uae/ai-data-and-analytics, 2026]
- ❌ 不得将 Dubai AI Campus 与 Dubai Silicon Oasis 混为一谈——Dubai AI Campus 为 Dubai Universal Blueprint for AI 的集群计划（MENA 最大 AI 公司集群），由 dub.ai 官方承载。[Source: https://dub.ai/, 2026]
```

## 八、基线九节结构固化锚

基线报告 `reports/2026-11_baseline_report.html` 九节结构为该业务线固化锚，后续报告逐字继承：

1. 核心结论（摘要）｜2. 行业与政策发展趋势｜3. 人才供需与薪酬（核心模块）｜4. 企业类型细分｜5. 岗位技能要求｜6. 行业认可的职业资质与证书｜7. 就业落地路径建议（结论章）｜8. 数据可靠性与局限说明｜9. 参考来源清单

---

## 九、信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：四级标注与摘要引用约束见 `engine/templates/information-layering-spec.md` 第二 / 四节；新增信息统计模块见第四节。
- **事实卡片**：本业务线为共享事实域（SEC），正文以 `[FC-SEC-…]` 引用 `engine/fact_cards/security_fact_cards.json`，不复制卡片全文。
- **决策卡与行动协议**：核心判断输出决策卡（结论 / 证据强度 / 触发条件 / 反向证据 / 信息充分度）；行动项五要素 + 三档优先级。
- **阈值校准**：首次中期回测 2027-06；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节。
- **场景切片**：主场景 **就业决策**；次场景 **政策制定** 与 **投资决策**。
- **影响分级**：`impact_tier = high`（高影响，强制披露矩阵见 `engine/templates/information-layering-spec.md` §七）。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」。
- **盲区**：P0 类别为「AI 应用岗薪酬区间」「MOHRE 职业分类与黄金签证门槛」「代表性雇主 AI 岗位动态」三类，优先消号。

---

<!-- VOCAB-SYNC:BEGIN topic=tech do-not-edit -->
## 词汇速览 · 科技（词汇库自动同步）

> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 tech v1.4，共 64 条（同步于 2026-11-21T16:53:17）。标记区间内请勿手工编辑；词条变更走词汇库导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。

- **模型与厂商**（19）：多模态模型（Multimodal Model、多模态）；推理模型（Reasoning Model、推理增强模型、思维链模型）；OpenAI（openai.com）；Anthropic（anthropic.com）；Google DeepMind（谷歌deepmind、Google AI）；Meta AI（Meta、Facebook AI）；xAI（X.AI、xAI 公司）；Mistral AI（Mistral）；DeepSeek（深度求索）；阿里通义千问（Qwen、通义千问）；智谱 GLM（GLM、Zhipu AI、智谱AI）；月之暗面 Kimi（Moonshot AI、Kimi）；字节豆包（Doubao、豆包大模型）；百度文心（ERNIE、文心一言）；GPT（GPT 系列、GPT-4、GPT-5）；Claude（Claude 系列、Claude Sonnet、Claude Opus）；Gemini（Gemini 系列）；Llama（Llama 系列、Llama 开源）；Grok（Grok 系列）
- **Agent 技术与框架**（13）：AI Agent（智能体、Agent）；多智能体系统（Multi-Agent System、MAS、多智能体协作）；工具调用（Function Calling、Tool Use、函数调用）；A2A（Agent-to-Agent、Agent2Agent 协议）；ReAct（Reasoning and Acting）；Agent 记忆（Agent Memory、长期记忆）；Computer Use（计算机使用、屏幕操作 Agent）；LangChain（LangChain 框架）；LangGraph（LangGraph 编排）；LlamaIndex（LlamaIndex 框架）；AutoGen（Microsoft AutoGen）；CrewAI（CrewAI 框架）；Dify（Dify 平台）
- **应用与产品**（15）：ChatGPT（chatgpt.com）；Perplexity（Perplexity AI）；NotebookLM（NotebookLM 产品）；Microsoft 365 Copilot（M365 Copilot、Office Copilot）；Deep Research（深度研究）；AI 搜索（AI Search、答案引擎）；Midjourney（MJ）；Sora（OpenAI Sora）；Suno（Suno AI）；ElevenLabs（ElevenLabs 语音）；Lovable（Lovable.dev）；Bolt.new（Bolt）；v0（v0.dev）；Replit Agent（Replit）；Manus（Manus AI）
- **组织与岗位**（5）：红队（Red Team、攻击模拟队）；蓝队（Blue Team、防御团队）；紫队（Purple Team）；AI 红队（AI Red Team、LLM 红队、AI Red Teaming）；SOC（Security Operations Center、安全运营中心）
- **认证与岗位**（12）：OSCP（攻击性安全认证专业人员、Offensive Security Certified Professional）；CEH（道德黑客认证、Certified Ethical Hacker）；CISM（注册信息安全管理师、Certified Information Security Manager）；安全运营分析师（SOC Analyst、安全分析师）；CompTIA Security+（Security Plus）；CISA 认证（注册信息系统审计师、Certified Information Systems Auditor）；CCSP（认证云安全专家、Certified Cloud Security Professional）；云安全架构师（Cloud Security Architect）；应用安全工程师（AppSec Engineer、安全开发工程师）；首席信息安全官（CISO）；安全研究员（漏洞研究员、Security Researcher）；安全合规官（GRC 经理、治理风险合规岗）
<!-- VOCAB-SYNC:END -->

## 十、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-21 | 初始版本 | 新建 `content/tech/ai-application/dubai` 业务线：补运行变量固定值、来源优先级实例化、触发器、14 项指标追踪表、已修正事实清单、九节固化锚；与 AI 安全线划清岗位边界 |
