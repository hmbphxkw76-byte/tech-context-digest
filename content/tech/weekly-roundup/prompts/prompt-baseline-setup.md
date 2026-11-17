# AI 趋势周报（安全 × Agent 生态）· 基线机制建立提示词（行业趋势周报型）

> **用途**：首期机制建立（一次性，正常运行永不重跑）。
> **产出**：中文机制文档（基线报告），落盘 `{{OUTPUT_PATH}}`。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../engine/templates/monitoring-common-spec.md) × [基线类型模板（行业趋势周报型）](../../../../engine/templates/trend-weekly/prompt-baseline-setup-template.md) × [业务专属配置](./business-config.md)。冲突时以本文件为准。
>
> **过程来源**：通用执行步骤与质量自检以 [通用泛用版基线提示词](../../../../engine/prompts/trend-weekly/prompt-baseline-setup.md) 为准；本文件只承载业务实例化差异。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 全球 / Weekly Roundup，见 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{CADENCE}}               = 固定填「周」（基线不区分节拍）
{{REGISTRY_PATH}}         = data/processed/tech/weekly-roundup/ai_trend_ledger.md
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.html
{{REPORT_VERSION}}        = 固定 v1.0；灾难恢复重建时按版本记录递增
```

**任务目标**：建立周报运行机制——受众定位、五大主题板块、来源分级、台账协议与报告骨架逐字固化。基线一经产出即为锚；仅台账与报告全部丢失（灾难恢复）或结构经批准变更时允许重建。

> **本业务线实际模式**：以首期周报（`reports/2026-11-13_weekly.html`）为结构锚，未单独出九节基线文档；本文件仅用于结构重置时参照。

## 业务专属硬性约束

1. **结论边界**：周报正文只给「条件 → 判读 → 框架性含义 → 风险提示」，不给买卖价位、仓位建议。
2. **来源语言**：`{{SOURCE_LANGUAGE_RULE}}` 强制执行（官方一手以英文为准；中文媒体仅作线索）。
3. **事实与推断分离**：【事实】/【预测】/「推断」显式标注；转述标「需核实原文」。
4. **主题矩阵**：固定 5 块（见 business-config 第三节），互不重叠。

## 结果验证

```powershell
python engine/tools/validate.py          # 0 错误
python engine/tools/lint_reports.py      # 0 错误
python engine/tools/build_index.py && python engine/tools/build_hub.py
```

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 由 trends/ai-security 与 trends/ai-agent 基线提示词合并；通用过程改为引用类型通用层 |
