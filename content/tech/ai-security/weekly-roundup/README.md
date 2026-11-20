# AI 安全趋势周报（攻击面 · 红队 · 基准可信度）· 业务线说明

> **类型**：行业趋势周报型（trend-weekly） · **地区**：全球 · **节拍**：周（数据截止日命名）
> **通用指南**：接入与使用见 [类型通用接入指南](../../../../engine/templates/trend-weekly/README.md)；生命周期与校验见 [类型通用运维手册](../../../../engine/templates/trend-weekly/operations-guide.md)。本文件只写本业务线身份与差异。
> **拆分来源**：由 `content/tech/weekly-roundup`（AI 趋势周报，安全 × Agent 生态合并线）拆分，承接 AI 安全侧两板块；AI 应用侧归 `content/tech/ai-application/weekly-roundup`。原合并周报（2026-11-13 / 2026-11-20）存于 `sources/legacy/`。

## 一、业务身份

- **定位**：面向 AI 安全技术负责人 · 红队工程（RedTeam_AI）的 AI 安全侧周报。
- **结构锚**：原合并首期 `sources/legacy/2026-11-13_weekly.html` 的安全侧板块。
- **台账**：`data/processed/tech/ai-security/weekly-roundup/ai_security_trend_ledger.md`（md-ledger）。
- **主题矩阵**：固定 2 块 —— AI 安全与红队 / 基准与评估可信度。
- **交付**：富样式自包含 HTML（`reports/{YYYY-MM-DD}_weekly.html`）+ md 源稿（`sources/`）。

## 二、与类型通用模板的差异（本线特有）

| 维度 | 本线规则 |
|---|---|
| 报告结构 | 7 节（Top5 + 2 主题板块 + 数据看板 + 风险 + 启示 + 来源） |
| 受众 | RedTeam_AI（s2）+ 安全工程 / 治理（s3） |
| 来源优先级 | 官方一手（Microsoft/OpenAI/Anthropic/Google/EU/METR/Stanford HAI）＞ 行业机构（OWASP/Gartner/基准官方页）＞ 挂牌门户 ＞ 媒体转述 |
| 触发器 | 安全事件/模型发布 → s2；监管标准 → s2；基准退役/缺陷 → s3 |
| 结论边界 | 不给选型背书、买卖价位与仓位建议 |

## 三、快速上手

1. 前置检查（`validate.py` / `classify_reports.py` / `build_hub.py --check`）通过。
2. 打开 `prompts/prompt-weekly-monitor.md` 填写运行变量并执行。
3. 落盘后收尾：`lint_reports.py` → `compliance_check.py` → `classify_reports.py` → `build_index.py` + `build_hub.py` → `archive_reports.py`。

完整执行步骤、变量表与异常排查见 [operations-guide.md](./operations-guide.md) 与 [类型通用运维手册](../../../../engine/templates/trend-weekly/operations-guide.md)。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 新增 | 由 trends/ai-security 与 trends/ai-agent 合并建立；通用接入指南下沉至类型通用层 |
| v1.1 | 2026-11-18 | 修正 | 「合并来源」中 `reports/legacy/` 指向已不存在（2026-11-17 清理，tech-debt-ledger B12–B14 closed），改为实际状态 |
| v1.2 | 2026-11-20 | 拆分 | 由 `content/tech/weekly-roundup` 拆分：收敛为 AI 安全侧两板块；AI 应用侧归 `content/tech/ai-application/weekly-roundup` |
