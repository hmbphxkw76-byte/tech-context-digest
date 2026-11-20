# AI 应用趋势周报（大模型 · Agent · 编码 · 商业化）· 业务线说明

> **类型**：行业趋势周报型（trend-weekly） · **地区**：全球 · **节拍**：周（数据截止日命名）
> **通用指南**：接入与使用见 [类型通用接入指南](../../../../engine/templates/trend-weekly/README.md)；生命周期与校验见 [类型通用运维手册](../../../../engine/templates/trend-weekly/operations-guide.md)。本文件只写本业务线身份与差异。
> **拆分来源**：由 `content/tech/weekly-roundup`（AI 趋势周报，安全 × Agent 生态合并线）拆分，承接 AI 应用侧三板块；AI 安全侧归 `content/tech/ai-security/weekly-roundup`。原合并周报（2026-11-13 / 2026-11-20）存于 `sources/legacy/`。

## 一、业务身份

- **定位**：面向 AI Agent 开发团队 · 大模型应用工程（Agent Dev）的 AI 应用侧周报。
- **结构锚**：原合并首期 `sources/legacy/2026-11-13_weekly.html` 的应用侧板块。
- **台账**：`data/processed/tech/ai-application/weekly-roundup/ai_application_trend_ledger.md`（md-ledger）。
- **主题矩阵**：固定 3 块 —— 大模型与 Agent 技术演进 / AI 编码与开发工具 / AI 应用与商业化。
- **交付**：富样式自包含 HTML（`reports/{YYYY-MM-DD}_weekly.html`）+ md 源稿（`sources/`）。

## 二、与类型通用模板的差异（本线特有）

| 维度 | 本线规则 |
|---|---|
| 报告结构 | 8 节（Top5 + 3 主题板块 + 数据看板 + 风险 + 启示 + 来源） |
| 受众 | Agent Dev / 大模型应用工程 |
| 来源优先级 | 官方一手（OpenAI/Anthropic/Google/Meta/GitHub/Cursor 等）＞ 行业机构 ＞ 挂牌门户 ＞ 媒体转述 |
| 触发器 | 模型/Agent 协议 → s2；编码工具/基准 → s3；融资/定价/采用 → s4 |
| 结论边界 | 不给选型背书、买卖价位与仓位建议 |

## 三、快速上手

1. 前置检查（`validate.py` / `classify_reports.py` / `build_hub.py --check`）通过。
2. 打开 `prompts/prompt-weekly-monitor.md` 填写运行变量并执行。
3. 落盘后收尾：`lint_reports.py` → `compliance_check.py` → `classify_reports.py` → `build_index.py` + `build_hub.py` → `archive_reports.py`。

完整执行步骤、变量表与异常排查见 [operations-guide.md](./operations-guide.md) 与 [类型通用运维手册](../../../../engine/templates/trend-weekly/operations-guide.md)。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-20 | 新增 | 由 `content/tech/weekly-roundup` 拆分建立；通用接入指南沿用类型通用层 |
