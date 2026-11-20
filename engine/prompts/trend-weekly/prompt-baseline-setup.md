# {{REGION}} · {{TOPIC}} · 基线机制建立提示词（行业趋势周报型 · 泛用版）

> **用途**：首期机制建立（一次性，正常运行永不重跑）。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文九节机制文档（基线报告），落盘 `{{OUTPUT_PATH}}`。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [基线类型模板（行业趋势周报型）](../../templates/trend-weekly/prompt-baseline-setup-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{CADENCE}}               = 固定填「周」（基线不区分节拍）
{{REGISTRY_PATH}}         = data/（TODO：台账文件名）
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.html
{{REPORT_VERSION}}        = 固定 v1.0；灾难恢复重建时按版本记录递增
```

**任务目标**：建立周报运行机制——受众定位、三大主题板块、来源分级、台账协议与八节周报骨架逐字固化。基线一经产出即为锚；仅台账与报告全部丢失（灾难恢复）或八节结构经批准变更时允许重建。

---

## 一、执行步骤

1. 完成监测范围与主题矩阵调研（TODO：三大板块定义，覆盖受众决策需求、互不重叠）。
2. 完成来源清单与发布节奏调研（TODO：逐机构官方 URL / 发布频率 / 语言；按通用基座四层分级实例化）。
3. 首建台账 `{{REGISTRY_PATH}}`（数据看板追踪表 / 已修正事实清单 / 来源清单 / 触发器清单 / 版本记录）。
4. 按基线类型模板第二节撰写九节机制文档（顺序、标题逐字固化），落盘 `{{OUTPUT_PATH}}`；八节周报骨架在机制文档第五节逐字固化。

## 二、项目专属硬性约束

1. **结论边界**：周报正文只给「条件 → 判读 → 框架性含义 → 风险提示」，不给买卖价位、仓位建议。
2. **来源语言**：`{{SOURCE_LANGUAGE_RULE}}` 强制执行（默认仅英文，业务配置可加严；政策：engine/docs/source-language-policy.md）。
3. **事实与推断分离**：【事实】/【预测】/「推断」显式标注；转述标「需核实原文」。

## 三、结果验证

```powershell
python engine/tools/validate.py          # 0 错误
python engine/tools/lint_reports.py      # 0 错误
python engine/tools/build_index.py && python engine/tools/build_hub.py
```

人工核对：九节标题与基线类型模板第二节逐字一致；主题矩阵三块互不重叠；台账章节定义与机制文档第四节一致。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版基线提示词 |
