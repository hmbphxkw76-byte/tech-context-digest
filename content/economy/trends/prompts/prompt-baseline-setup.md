# 经济趋势周报 · 基线机制建立提示词（行业趋势周报型）

> **用途**：首期机制建立（一次性）。**本业务线基线模式**：与 `content/tech/weekly-roundup` 同款——以首期周报为结构锚，首期周报产出后其八节结构与结论即为锚；机制定义由 [business-config.md](./business-config.md) 承载，**未单独产出九节基线文档**。正常运行永不重跑本提示词；仅当八节结构经维护规范批准变更、或报告与台账全部丢失（灾难恢复）时允许启动，届时须按[基线类型模板](../../../../engine/templates/trend-weekly/prompt-baseline-setup-template.md)补建九节机制文档。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../engine/templates/monitoring-common-spec.md) × [基线类型模板（行业趋势周报型）](../../../../engine/templates/trend-weekly/prompt-baseline-setup-template.md) × [业务专属配置](./business-config.md)。

---

## 运行变量（必填）

```
{{CURRENT_DATE}}   = 本次执行日期
{{CADENCE}}        = 固定填「周」（基线不区分节拍）
{{OUTPUT_PATH}}    = reports/{{YYYY-MM}}_baseline_report.html
{{REPORT_VERSION}} = 固定 v1.0；灾难恢复重建时按版本记录递增
```

## 执行步骤

1. 核对业务配置第三节主题矩阵三块定义完整、互不重叠；第四节来源清单逐机构有官方 URL 与发布节奏。
2. 核对台账 `{{REGISTRY_PATH}}` 已存在（骨架已于业务线建立时首建，v1.0）；缺失时按台账章节定义重建（数据看板追踪表 / 已修正事实清单 / 来源清单 / 触发器登记 / 版本记录）。
3. 按[基线类型模板第二节](../../../../engine/templates/trend-weekly/prompt-baseline-setup-template.md)撰写九节机制文档（顺序、标题逐字固化），落盘 `{{OUTPUT_PATH}}`；八节周报骨架在机制文档第五节逐字固化。
4. 将业务配置第一节 `{{BASELINE_REPORT_PATH}}` 指向新报告。

## 结果验证

```powershell
python engine/tools/validate.py
python engine/tools/lint_reports.py
python engine/tools/build_index.py && python engine/tools/build_hub.py
```

人工核对：九节标题与基线类型模板第二节逐字一致；台账章节定义与机制文档第四节一致；八节周报骨架与首期周报逐字一致。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 基线提示词占位建档；本业务线采用「首期周报即结构锚」模式，机制定义由 business-config 承载，台账骨架已预建 |
