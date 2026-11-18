# AI 趋势周报（安全 × Agent 生态）· 业务线说明

> **类型**：行业趋势周报型（trend-weekly） · **地区**：全球 · **节拍**：周（数据截止日命名）
> **通用指南**：接入与使用见 [类型通用接入指南](../../../engine/templates/trend-weekly/README.md)；生命周期与校验见 [类型通用运维手册](../../../engine/templates/trend-weekly/operations-guide.md)。本文件只写本业务线身份与差异。
> **合并来源**：由 `trends/ai-security`（AI 安全）与 `trends/ai-agent`（AI Agent 与大模型）合并；历史 md 源稿存于 `sources/legacy/{ai-security,ai-agent}/`。历史报告 HTML 已于 2026-11-17 全量重生成时清理（tech-debt-ledger B12–B14，closed），原快照见 git 历史。

## 一、业务身份

- **定位**：面向 ① AI 安全技术负责人 · 红队工程（RedTeam_AI）与 ② AI Agent 开发团队 · 大模型应用工程（Agent Dev）的双轨周报。
- **首期锚**：`reports/2026-11-13_weekly.html`（合并首期，10 节结构）。
- **台账**：`data/processed/tech/weekly-roundup/ai_trend_ledger.md`（md-ledger，22 项指标、34 条来源）。
- **主题矩阵**：固定 5 块 —— AI 安全与红队 / 大模型与 Agent 技术演进 / AI 编码与开发工具 / AI 应用与商业化 / 基准与评估可信度。
- **交付**：富样式自包含 HTML（`reports/{YYYY-MM-DD}_weekly.html`）+ md 源稿（`sources/`）。

## 二、与类型通用模板的差异（本线特有）

| 维度 | 本线规则 |
|---|---|
| 报告结构 | **10 节**（Top5 + 5 主题板块 + 数据看板 + 风险 + 启示 + 来源），与类型通用 8 节骨架不同，已在 `compliance-rules.json` 登记业务级规则 |
| 受众 | 双轨：RedTeam_AI（s2/s6）+ Agent Dev（s3–s5）；启示章分别给两类受众 |
| 来源优先级 | 官方一手（Microsoft/OpenAI/Anthropic/Google/Meta/ GitHub 等）＞ 行业机构（OWASP/Gartner/基准官方页）＞ 挂牌门户（Arena/Artificial Analysis）＞ 媒体转述 |
| 触发器 | 模型/安全事件 → s2、s3；监管标准 → s2；Agent 协议更新 → s3；编码工具发布 → s4；融资/定价/采用披露 → s5；基准退役 → s6 |
| 结论边界 | 不给选型背书、买卖价位与仓位建议 |

## 三、快速上手

1. 前置检查（`validate.py` / `classify_reports.py` / `build_hub.py --check`）通过。
2. 打开 `prompts/prompt-weekly-monitor.md` 填写运行变量并执行。
3. 落盘后收尾：`lint_reports.py` → `compliance_check.py` → `classify_reports.py` → `build_index.py` + `build_hub.py` → `archive_reports.py`。

完整执行步骤、变量表与异常排查见 [operations-guide.md](./operations-guide.md) 与 [类型通用运维手册](../../../engine/templates/trend-weekly/operations-guide.md)。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 新增 | 由 trends/ai-security 与 trends/ai-agent 合并建立；通用接入指南下沉至类型通用层 |
| v1.1 | 2026-11-18 | 修正 | 「合并来源」中 `reports/legacy/` 指向已不存在（2026-11-17 清理，tech-debt-ledger B12–B14 closed），改为实际状态 |
