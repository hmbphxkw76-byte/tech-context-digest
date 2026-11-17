# AI 趋势周报（安全 × Agent 生态）· 指标台账（md-ledger）

> **定位**：`content/tech/trends/global` 业务线的活值登记载体（业务配置 `{{REGISTRY_PATH}}`）。运行前读 → 核验 → 运行后回写；prompt 模板内严禁预填活值。
> **格式**：md-ledger。台账修改采用增量方式：报告层补充与台账更新严格区分。
> **合并说明**：本台账由原 ai-security 与 ai-agent 两条业务线台账合并（历史版本见 `reports/legacy/{ai-security,ai-agent}/`）；两线重复指标（SWE-bench Verified 状态、组织 AI 采用率）已去重保留单行。

---

## 一、数据看板追踪表（周报 s7 联动）

| 板块 | 指标 | 上期值 | 本期值 | 变化 | 来源 | 口径 | 是否更新（2026-11-13 期） | 是否更新（2026-11-14 期） |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 基准与评估 | SWE-bench Verified 最高分 | 60%（2024） | 接近 100%（2025） | 一年后饱和 | Stanford HAI | 基准自报 | 首期 | 截至 2026-11-13 无更新 |
| 基准与评估 | SWE-bench Verified 状态 | 在役 | 2026-02 退役 | 数据污染 + 59.4% 测试缺陷 | OpenAI（需核实） | 审计子集 27.6% | 首期 | 截至 2026-11-13 无更新 |
| 基准与评估 | OSWorld | 12%（2024） | 66.3%（2025） | +54.3pp | Stanford HAI | 人类基线 72.35% | 首期 | 截至 2026-11-13 无更新 |
| AI 安全与红队 | AI 安全事故数 | 233（2024） | 362（2025） | +55.4% | Stanford HAI | 已报告事件 | 首期 | 截至 2026-11-13 无更新 |
| AI 安全与红队 | 投毒 ASR（移除推理链） | 94.8%（4B）/ 84.1%（9B） | 1.0% / 0% | -93.8pp / -84.1pp | Microsoft | 500 次试验 | 首期 | 截至 2026-11-13 无更新 |
| AI 安全与红队 | AI in cybersecurity 市场 | $31.5B（2025） | $39.1B（2026） | +24.1% | Grand View Research | 含服务与软件 | 首期 | 截至 2026-11-13 无更新 |
| 大模型与 Agent | Claude Fable 5.2 FrontierCode 2.0 | —（首期） | 49.1%（Xhigh） | 本期新增 | Anthropic | Agent 编码基准；官方自报 | 首期登记 | — |
| 大模型与 Agent | Claude Fable 5.2 价格（输入/输出） | —（首期） | $8 / $40（较 5.1 降 20%） | 本期新增 | Anthropic | 标准 API；Fast Mode $16/$80 | 首期登记 | — |
| 大模型与 Agent | Fable 5.2 多智能体编排规模 | —（首期） | 1000+ 子智能体 / 8 天 | 本期新增 | Anthropic | 官方演示；构建可启动 OS | 首期登记 | — |
| 大模型与 Agent | Meta Muse Ember 综合智能指数 | —（首期） | 36（追平 Haiku 5.5） | 本期新增 | Meta（需核实原文） | Artificial Analysis Index | 首期登记 | — |
| 大模型与 Agent | Kimi K3.1 Pro 参数规模 | —（首期） | 3 万亿级（MoE） | 本期新增 | Moonshot | 100 万 token 上下文 | 首期登记 | — |
| AI 编码与开发工具 | SWE-bench Pro 任务损坏率 | —（首期） | 约 30%（2026-07 审计） | 本期新增 | OpenAI | 自动 27.4% / 人工 34.1% | 首期登记 | — |
| AI 编码与开发工具 | Terminal-Bench 2.0 问题比例 | —（首期） | 约 30% → 修复为 2.1 | 本期新增 | arXiv:2611.08417 | 准确率 +10pp；排名最多变 3 位 | 首期登记 | — |
| AI 应用与商业化 | 企业 AI 部署支出 | —（首期） | $1768 亿（2026-09） | 本期新增 | Menlo Ventures | 5.4x YoY；VC 估算 | 首期登记 | — |
| AI 应用与商业化 | OpenRouter Agent token 占比 | —（首期） | 80%（约人类 7 倍） | 本期新增 | Menlo Ventures | 130.9 万亿 token/周 | 首期登记 | — |
| AI 应用与商业化 | 前沿实验室部署支出份额 | —（首期） | 69%（$1227 亿） | 本期新增 | Menlo Ventures | 上一年 50% | 首期登记 | — |
| AI 应用与商业化 | Anthropic 企业 LLM API 份额 | —（首期） | 55%（上一年 40%） | 本期新增 | Menlo Ventures | 企业 API 支出 | 首期登记 | — |
| AI 应用与商业化 | Claude Code + Codex 编码支出 | —（首期） | $240 亿（占编码 70%） | 本期新增 | Menlo Ventures | 编码应用市场 $340 亿 | 首期登记 | — |
| AI 应用与商业化 | Anthropic Q3 收入 | $13.82B（2025 Q3） | $169.56B（2026 Q3） | 12x | SEC EDGAR S-1/A | GAAP | 首期 | 截至 2026-11-13 无更新 |
| 跨板块 | 组织 AI 采用率 | — | 88%（2025） | 本期新增 | Stanford HAI | 企业调查 | 首期 | 截至 2026-11-13 无更新 |
| 跨板块 | 美国私人 AI 投资 | — | $285.9B（2025） | 为中国 23 倍 | Stanford HAI | 股权融资 | 首期 | 截至 2026-11-13 无更新 |
| 跨板块 | GenAI 人口采用率 | — | 53%（3 年内） | 本期新增 | Stanford HAI | 跨国调查 | 首期 | 截至 2026-11-13 无更新 |

> 合并时点（2026-11-14）：原 ai-security 台账 10 行（含 2026-11-14 T+1 期列）与原 ai-agent 台账 14 行合并；重复项「SWE-bench Verified 状态」「组织 AI 采用率」各保留单行。口径警示：Grand View Research（$31.5B/$39.1B，含服务与软件）与 Gartner（AI 模型/平台）口径不同，不可相加；基准成绩须注版本与发布日期，禁止跨基准横比。

## 二、已修正事实清单（首期为空，产生修正后逐条补记）

```
【已修正事实清单 — 首期为空，产生修正后逐条补记，格式如下】
- ❌ 不得再称"…"——正确结论为…。[Source: URL, 年份]
```

- 防回退规则：每期周报运行前必须完整继承本清单；与清单冲突的旧结论不得复活。

## 三、来源清单（持续维护）

| # | 来源 | 层级 | 官方 URL | 状态 |
|---|---|---|---|---|
| 1 | Microsoft Security Blog — Trained to betray（2026-11-12） | ① | https://www.microsoft.com/en-us/security/blog/2026/11/12/trained-to-betray-dataset-poisoning-and-model-poisoning/ | 已核验 |
| 2 | Microsoft Security Blog — Detecting sleeper agents（2026-11-10） | ① | https://www.microsoft.com/en-us/security/blog/2026/11/10/detecting-sleeper-agents/ | 已核验 |
| 3 | Stanford HAI — AI Index Report 2026 | ① | https://hai.stanford.edu/ai-index/2026-ai-index-report | 已核验 |
| 4 | EU AI Act — Regulation (EU) 2024/1689 | ① | https://eur-lex.europa.eu/eli/reg/2024/1689/oj | 已核验 |
| 5 | OWASP — Top 10 for LLM Applications / Agentic Top 10 | ② | https://genai.owasp.org/agentic-top-10/ | 需核实原文 |
| 6 | Grand View Research — AI in Cybersecurity Market Report | ② | https://www.grandviewresearch.com/industry-analysis/ai-in-cybersecurity-market-report | 已核验 |
| 7 | Gartner — Newsroom / Press Releases | ② | https://www.gartner.com/en/newsroom/press-releases/ | 需核实原文（反爬，媒体转述） |
| 8 | OpenAI — Separating Signal from Noise in Coding Evaluations | ① | https://openai.com/index/separating-signal-from-noise-coding-evaluations/ | 需核实原文（反爬） |
| 9 | Anthropic — News / Research / Policies | ① | https://www.anthropic.com/news | 部分需核实原文 |
| 10 | METR — Blog | ① | https://metr.org/blog/ | 需核实原文 |
| 11 | Anthropic PBC — Form S-1/A（SEC EDGAR，2026-11-10） | ① | https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/anthropicpbc-sx1ax2.htm | 已核验 |
| 12 | 36kr — Anthropic 报告质疑报道（2025-11-17） | ④ | https://36kr.com/p/3556763628502150 | 线索（反向证据） |
| 13 | 央广网 — Anthropic IPO 定价报道（2026-11-10） | ④ | https://www.cnr.cn/jingji/ycbd/20261110/t20261110_527868436.shtml | 线索（已回 SEC 原文） |
| 14 | GitHub — anthropics/claude-code issues #50702 等 | ① | https://github.com/anthropics/claude-code/issues/50702 | 需核实原文 |
| 15 | Nikken Sekkei（日建设计）— Notion AI 信息泄露公告（2026-11-13） | ① | https://www.nikken.jp/en/news/news/20261113j.html | 已核验 |
| 16 | Notion — Security Advisory: third-party AI vendor incident（2026-11-09，11-11 更新） | ① | https://www.notion.com/security/advisories/security-incident-involving-a-third-party-ai-vendor-nov9 | 已核验 |
| 17 | SEC EDGAR — Anthropic PBC submissions（CIK 2130357） | ① | https://data.sec.gov/submissions/CIK0002130357.json | 已核验 |
| 18 | Anthropic — Fable 5.2 / Mythos 5.2 | ① | https://www.anthropic.com/claude-fable-and-mythos-5-2 | 已核验（2026-11-09） |
| 19 | Anthropic — IPO 路演启动 | ① | https://www.anthropic.com/news/roadshow-launch | 已核验（2026-11-10） |
| 20 | Anthropic — Early progress in drug development | ① | https://www.anthropic.com/research/early-progress-drug-development | 已核验（2026-11） |
| 21 | Menlo Ventures — 2026 State of Enterprise AI | ② | https://menlovc.com/perspective/2026-the-state-of-enterprise-ai/ | 已核验（2026-11-03） |
| 22 | OpenAI — Why we no longer evaluate SWE-bench Verified | ① | https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ | 已核验（2026-02-23） |
| 23 | arXiv:2611.08417 — Benchmarks as Software（Terminal-Bench） | ② | https://arxiv.org/abs/2611.08417 | 已核验（2026-11-05） |
| 24 | Kimi 开放平台 — 托管智能体产品概览 / 模型列表 | ① | https://platform.kimi.com/docs/hosted-agents/overview | 已核验（2026-11-05） |
| 25 | Cursor — Changelog | ① | https://cursor.com/changelog | 已核验（2026-11-05/06/10-20） |
| 26 | Anthropic — Claude Code Changelog | ① | https://docs.anthropic.com/en/docs/claude-code/changelog | 已核验（2026-11-12） |
| 27 | GitHub — Changelog | ① | https://github.blog/changelog/ | 已核验（2026-11-03~10） |
| 28 | Codeium — Changelog | ① | https://www.codeium.com/changelog | 已核验（2026-11-09） |
| 29 | 钛媒体 / 新浪财经 — Meta Muse Ember 报道 | ④ | https://www.tmtpost.com/agent/ai-article/22497 | 需核实原文（2026-11-09/10） |
| 30 | 腾讯云社区 / 网易 — 腾讯混元 Hy4 / NVIDIA GR00T 2 | ④ | https://cloud.tencent.com/developer/article/2777813 | 需核实原文（2026-11-04/09） |
| 31 | CSDN / 百度百科 — MCP 与 A2A 治理 | ④ | https://blog.csdn.net/shaobingj126/article/details/164249861 | 需核实原文（2026-07/08） |
| 32 | 博客园 — Anthropic Message Threads 公测 | ④ | https://www.cnblogs.com/itech/category/2501460.html | 需核实原文（2026-11-02） |
| 33 | 17173 — Gartner AI 支出预测转述 | ④ | https://news.17173.com/content/07212026/120235804.shtml | 需核实原文（2026-07-20） |
| 34 | Bloomberg — OpenAI 完成 110 亿美元融资 | ④ | https://www.bloomberg.com/news/articles/2026-11-06/openai-completes-11-billion-portion-of-funding-at-1-25-trillion-value | 需核实原文（2026-11-06） |

## 四、触发器登记（业务配置第五节执行记录）

| 日期 | 事件 | 受影响板块 | 处置 |
|---|---|---|---|
| 2026-11-13 | 新模型发布：Claude Fable 5.2 / Mythos 5.2（2026-11-09）、Meta Muse Ember（11-09）、Kimi K3.1 Pro（11-05） | s3 | 当期升级：新模型与基准全量更新 |
| 2026-11-13 | Agent 协议与框架：MCP/A2A 统一治理（2026-08-17）、Message Threads 公测（11-02） | s3 | 当期升级：协议与架构更新 |
| 2026-11-13 | 编码工具重大发布：Cursor Build Live Apps（11-05）、Claude Code Code Mode（11-12）、GitHub Copilot 新模型（11-09/10） | s4 | 当期升级：AI IDE 与编码 Agent 更新 |
| 2026-11-13 | 编码基准：SWE-bench Verified 弃用（2026-02）、SWE-bench Pro 撤回推荐（2026-07）、Terminal-Bench 2.1（11-05） | s4/s6 | 当期升级：基准与工作流更新 |
| 2026-11-13 | 头部应用产品 IPO：Anthropic 路演启动（2026-11-10） | s5 | 当期升级：融资并购更新 |
| 2026-11-13 | 采用数据披露：Menlo Ventures 企业 AI 现状（2026-11-03） | s5 | 当期升级：采用与支出更新 |
| 2026-11-13 | 定价重构：Fable 5.2 降价 20%、Kimi Hosted Agents 按量计费 | s5 | 当期升级：定价与商业模式更新 |
| 2026-11-13 | 安全事件：Notion AI 供应链事件新增受影响方披露（日建设计 2026-11-13）；T+1 复核无其他重大触发 | s2 | T+1 核验轻运行，s2 增补 1 条，其余板块继承 |

## 五、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 首建台账（两条业务线） | ai-security 从首期周报播种 10 项指标、17 条来源；ai-agent 播种 14 项指标、23 条来源 |
| v1.1 | 2026-11-13 | 原 ai-security T+1 期回写 | 核验轻运行：10 项全部无更新（新增 2026-11-14 期列）；来源增 3 条 |
| v1.2 | 2026-11-14 | 合并 | 两条业务线台账合并为 `data/processed/tech/trends/global/ai_trend_ledger.md`：看板 22 行（去重 2 项）、来源 34 条、触发器 8 条；板块列对应五主题矩阵 |
