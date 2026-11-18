# AI 趋势周报（安全 × Agent 生态）· 操作手册（业务差异）

> **定位**：本文件是 [类型通用运维手册](../../../engine/templates/trend-weekly/operations-guide.md) 的**业务实例**，只写本线差异；通用执行步骤、变量表、校验关卡、异常排查与 Agent 约定以通用手册为准。
> **单一事实源**：业务参数以 [prompts/business-config.md](./prompts/business-config.md) 为准。

---

## 0. 本线目录速查

| 资产 | 路径 |
|---|---|
| 周报提示词（启动入口） | `prompts/prompt-weekly-monitor.md` |
| 基线机制建立提示词（占位） | `prompts/prompt-baseline-setup.md` |
| 业务参数 | `prompts/business-config.md` |
| 指标台账 | `data/processed/tech/weekly-roundup/ai_trend_ledger.md` |
| 报告产物 / 归档 | `reports/` / `reports/archives/` |
| md 源稿 / 历史迁移 | `sources/` / `sources/legacy/{ai-security,ai-agent}/` |
| 历史报告 HTML | 已于 2026-11-17 全量重生成时清理（原 `reports/legacy/{ai-security,ai-agent}/`，tech-debt-ledger B12–B14 closed）；快照见 git 历史 |
| 通用层（只读） | `engine/templates/trend-weekly/` |

## 1. 本线要点

- **主题矩阵**：固定 5 块（s2–s6），周报共 10 节；结构与首期周报 `reports/2026-11-13_weekly.html` 逐字一致。
- **来源语言**：官方一手以英文为准；中文媒体仅作线索，数值须回官方页核验。
- **交付**：纯 HTML（business-config 第六节声明）；md 源稿存 `sources/`，不参与 md2html 自动转换。
- **触发器**：见 business-config 第五节。
- **合规**：本线 10 节结构在 `compliance-rules.json` 的 `business_overrides.content/tech/weekly-roundup` 登记，compliance_check 自动套用。

## 2. 本线特有排查项

| 现象 | 处置 |
|---|---|
| 两线同类指标口径不同（如市场口径） | 并列呈现，不静默择一、不相加 |
| 基准成绩跨版本横比 | 注版本与发布日期；基准退役/污染时以「基准与评估可信度」板块显式披露 |
| 合并前历史报告导航链接失效 | 历史报告 HTML 已于 2026-11-17 清理（tech-debt-ledger B12–B14 closed），仅 md 源稿留存于 `sources/legacy/`；若历史产物内 `.nav-url` 指向旧路径，属已知迁移遗留，勿手工改写历史产物 |
| 词汇速览出现两个区块 | 正常：本线同时绑定 `ai-security` 与 `ai-agent` 两个词汇主题，各自维护 |

其余通用异常（validate/lint/compliance/classify/build_hub 退出码、上期报告缺失、T+1 刷新等）见 [类型通用运维手册第 7 节](../../../engine/templates/trend-weekly/operations-guide.md)。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 新增 | 由 trends/ai-security 与 trends/ai-agent 操作手册合并；通用流程下沉至类型通用层 |
| v1.1 | 2026-11-18 | 修正 | 目录速查与排查项中 `reports/legacy/` 指向已不存在（2026-11-17 清理），改为实际状态 |
