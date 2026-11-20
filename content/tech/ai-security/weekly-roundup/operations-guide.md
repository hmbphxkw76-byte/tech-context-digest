# AI 安全趋势周报（攻击面 · 红队 · 基准可信度）· 操作手册（业务差异）

> **定位**：本文件是 [类型通用运维手册](../../../../engine/templates/trend-weekly/operations-guide.md) 的**业务实例**，只写本线差异；通用执行步骤、变量表、校验关卡、异常排查与 Agent 约定以通用手册为准。
> **单一事实源**：业务参数以 [prompts/business-config.md](./prompts/business-config.md) 为准。

---

## 0. 本线目录速查

| 资产 | 路径 |
|---|---|
| 周报提示词（启动入口） | `prompts/prompt-weekly-monitor.md` |
| 基线机制建立提示词（占位） | `prompts/prompt-baseline-setup.md` |
| 业务参数 | `prompts/business-config.md` |
| 指标台账 | `data/processed/tech/ai-security/weekly-roundup/ai_security_trend_ledger.md` |
| 报告产物 / 归档 | `reports/` / `reports/archives/` |
| md 源稿 / 历史迁移 | `sources/` / `sources/legacy/` |
| 通用层（只读） | `engine/templates/trend-weekly/` |

## 1. 本线要点

- **主题矩阵**：固定 2 块（s2–s3），周报共 7 节；结构对齐原合并首期的安全侧板块。
- **来源语言**：仅英文，严禁中文来源（政策：`engine/docs/source-language-policy.md`）。
- **交付**：纯 HTML（business-config 第六节声明）；md 源稿存 `sources/`，不参与 md2html 自动转换。
- **范围边界**：AI 应用侧板块归 `content/tech/ai-application/weekly-roundup`，本线不重复跟踪。
- **合规**：结构变更需在 `compliance-rules.json` 登记业务级规则。

## 2. 本线特有排查项

| 现象 | 处置 |
|---|---|
| 与 AI 应用周报板块重叠 | 以 business-config 第三节矩阵为准；大模型/编码/应用商业化归 AI 应用线 |
| 原合并周报导航链接失效 | 历史合并周报存于 `sources/legacy/`，属存档，勿手工改写 |
| 词汇速览缺失 | 由 `engine/vocabulary/script/sync_vocab.py` 按 sync.json 绑定自动生成 |

其余通用异常（validate/lint/compliance/classify/build_hub 退出码、上期报告缺失、T+1 刷新等）见 [类型通用运维手册第 7 节](../../../../engine/templates/trend-weekly/operations-guide.md)。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 新增 | 由 trends/ai-security 与 trends/ai-agent 操作手册合并；通用流程下沉至类型通用层 |
| v1.1 | 2026-11-18 | 修正 | 目录速查与排查项中 `reports/legacy/` 指向已不存在（2026-11-17 清理），改为实际状态 |
| v1.2 | 2026-11-20 | 拆分 | 由 `content/tech/weekly-roundup` 拆分；通用流程沿用类型通用层 |
