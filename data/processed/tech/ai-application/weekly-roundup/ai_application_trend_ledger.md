# AI 应用趋势周报 · 指标台账（md-ledger）

> **定位**：`content/tech/ai-application/weekly-roundup` 业务线的活值登记载体（业务配置 `{{REGISTRY_PATH}}`）。运行前读 → 核验 → 运行后回写；prompt 模板内严禁预填活值。
> **格式**：md-ledger。台账修改采用增量方式：报告层补充与台账更新严格区分。
> **拆分说明**：本台账由原合并线 `content/tech/weekly-roundup` 台账拆分，承接 **大模型与 Agent 技术演进 / AI 编码与开发工具 / AI 应用与商业化** 三类指标；AI 安全 / 基准指标见 `data/processed/tech/ai-security/weekly-roundup/ai_security_trend_ledger.md`。原合并周报（2026-11-13 / 2026-11-20）已移入 `sources/legacy/`。

---

## 一、数据看板追踪表（周报 s5 联动）

| 板块 | 指标 | 上期值 | 本期值 | 变化 | 来源 | 口径 | 是否更新（2026-11-13 期） | 是否更新（2026-11-14 期） |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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

> 拆分时点（2026-11-20）：原合并台账 22 行中，AI 应用侧 16 行归入本线；AI 安全 / 基准相关 6 行归 AI 安全线。口径警示：基准成绩须注版本与发布日期；跨机构支出数据口径不同、不可相加。

## 二、已修正事实清单（首期为空，产生修正后逐条补记）

```
【已修正事实清单 — 首期为空，产生修正后逐条补记，格式如下】
- ❌ 不得再称"…"——正确结论为…。[Source: URL, 年份]
```

- 防回退规则：每期周报运行前必须完整继承本清单；与清单冲突的旧结论不得复活。
