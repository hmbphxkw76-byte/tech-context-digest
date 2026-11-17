# {{REGION}} · {{TOPIC}} · 快评机制建立提示词（快评·事件点评型 · 泛用版）

> **用途**：执行「{{REGION}} {{TOPIC}} 快评机制」的**机制建立**任务：产出快评机制基线文档（事件监测日历、预期台账、快评框架）。**基线期不出快评正文**，只建机制。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：机制文档（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_baseline_report.md`）+ 预期台账（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [基线报告类型模板（快评·事件点评型）](../../templates/flash-commentary/prompt-baseline-setup-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，实例化时写入 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{BASELINE_DATE}}         = 首期基线日期
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：预期台账文件名）
{{REGISTRY_FORMAT}}       = md-table（TODO：按业务配置）
{{SOURCE_LANGUAGE_RULE}}  = （TODO：来源语言规则）
{{REPORT_VERSION}}        = v1.0（首期基线固定）
```

**任务目标**：产出八节机制文档（事件监测日历、预期台账首建、快评四段式框架、信号与升级规则、来源与时效治理）；**核验底线**为「官方发布稿 / 财报原文为准」，转述信息单源直引为硬性禁止；运行后回写 `{{REGISTRY_PATH}}`；基线文档**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`。

---

## 一、项目专属硬性约束

1. **初步判断纪律**：快评输出快速影响判断，一律标「初步判断，待后续报告验证」；单份快评不推翻既有深度结论，只登记偏离信号。
2. **时效底线**：即使时间压力最大，也须回溯一手发布物后才可引用；时效取舍遵循 {{FRESHNESS_PRIORITY}}。
3. **受众定位**：（TODO：按业务配置实例化，默认需要快速反应的决策者 / 投资者）。

## 二、来源与时效治理

官方发布渠道清单（逐渠道 URL）、事后补验流程、升级规则（偏离阈值 → 深度报告 / 期报联动）（TODO：业务配置定义逐项）。

## 三、基线锚定

机制文档属性、预期台账首建等通用差异见[基线类型模板第一节](../../templates/flash-commentary/prompt-baseline-setup-template.md)。基线产出后，`{{BASELINE_REPORT_PATH}}` 即指向本机制文档；节标题为固化锚，正常运行**永不重跑**基线提示词。

## 四、追踪表（预期台账联动）

事件类型清单、预期登记（事件类型 → 共识预期 / 官方目标值 → 依据来源 → 更新时效）、无预期项登记「无预期」（TODO：业务配置定义逐项，不虚构共识值）；基线运行后逐项回写 `{{REGISTRY_PATH}}`，prompt 模板内严禁填写活值。

## 五、结构骨架

八节固定骨架见[基线类型模板第三节](../../templates/flash-commentary/prompt-baseline-setup-template.md)；业务固化锚节标题（TODO：实例化后声明并逐字继承）。

## 六、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`；基线导航采用简化锚点目录。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版机制建立提示词 |
