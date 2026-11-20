# {{REGION}} · {{TOPIC}} · 首期基线调研提示词（消费者·用户调研型 · 泛用版）

> **用途**：执行「{{REGION}} {{TOPIC}} 消费者调研机制」的**机制建立**任务：产出首期基线调研报告与配套调研设计档案。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文八节基线报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_baseline_report.md`）+ 调研设计档案（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [基线报告类型模板（消费者·用户调研型）](../../templates/consumer-research/prompt-baseline-setup-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，实例化时写入 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{BASELINE_DATE}}         = 首期基线日期
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：设计档案文件名）
{{REGISTRY_FORMAT}}       = md-table（TODO：按业务配置）
{{SOURCE_LANGUAGE_RULE}}  = 仅英文（默认；中国宏观例外见 engine/docs/source-language-policy.md）
{{REPORT_VERSION}}        = v1.0（首期基线固定）
```

**任务目标**：产出八节基线调研报告（调研设计与方法论、人群细分框架、首期结果、交叉分析）与设计档案首建；样本量、抽样方式、回收率、置信水平完整声明；运行后回写 `{{REGISTRY_PATH}}`；基线报告**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`。

---

## 一、项目专属硬性约束

1. **一手数据为主**：核心结论以一手调研为证据；无一手数据支撑的结论标「二手推断」。
2. **结论边界**：不输出「市场必然接受」断言；画像标「假设 / 验证状态」；行动建议标「建议」。
3. **伦理与隐私**：遵守知情同意与隐私保护；不采集或留存可识别个人身份的敏感信息；定性材料引用脱敏。
4. **受众定位**：（TODO：按业务配置实例化，默认产品 / 营销 / 用户体验团队）。

## 二、来源与抽样

抽样框与配额（TODO：目标人群定义、抽样方式、样本量下限、配额表）见实例化后的 business-config；二手数据仅作背景与交叉验证（冲突并列呈现）。

## 三、基线锚定

对比锚属性、设计档案首建等通用差异见[基线类型模板第一节](../../templates/consumer-research/prompt-baseline-setup-template.md)。基线产出后，`{{BASELINE_REPORT_PATH}}` 即指向本报告；节标题为固化锚，正常运行**永不重跑**基线提示词。

## 四、追踪表（设计档案联动）

细分维度、调研日历与「调研追踪项 × 方法」追踪表（TODO：业务配置定义逐项）；基线运行后逐项回写 `{{REGISTRY_PATH}}`，每格活值附 `[数据来源, 采集时间]`，prompt 模板内严禁填写活值。

## 五、报告结构骨架

八节固定骨架见[基线类型模板第三节](../../templates/consumer-research/prompt-baseline-setup-template.md)；业务固化锚节标题（TODO：实例化后声明并逐字继承）。

## 六、执行方式（建议）

1. 项目设计经业务提示词确认后，按模块并行启动采集与分析子代理；一手数据逐条附采集渠道与时间（TODO：按业务配置调整）。
2. 定性材料（深访 / 焦点小组）引用须脱敏；无法核实项单列「待复核清单」。

## 七、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`；基线导航采用简化锚点目录。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版基线提示词 |
