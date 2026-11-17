# {{REGION}} · {{TOPIC}} · 首期基线报告提示词（舆情传播监测型 · 泛用版）

> **用途**：执行「{{REGION}} {{TOPIC}} 舆情持续监测机制」的**机制建立**任务：产出首期舆论场基线报告与配套舆情台账。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文九节基线报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_baseline_report.md`）+ 舆情台账（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [基线报告类型模板（舆情传播监测型）](../../templates/sentiment-monitoring/prompt-baseline-setup-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，实例化时写入 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{BASELINE_DATE}}         = 首期基线日期
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：舆情台账文件名）
{{REGISTRY_FORMAT}}       = md-table（TODO：按业务配置）
{{SOURCE_LANGUAGE_RULE}}  = （TODO：来源语言规则）
{{REPORT_VERSION}}        = v1.0（首期基线固定）
```

**任务目标**：产出九节舆论场基线报告（渠道声量结构、议题基线声量、情感分布）与舆情台账首建；固定声明「舆情热度不等于市场真实状况」，重大结论与量化指标交叉验证；运行后回写 `{{REGISTRY_PATH}}`；基线报告**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`。

---

## 一、项目专属硬性约束

1. **言论≠事实**：报告输出舆论态势与风险预警，不输出「公众必然如何反应」断言；不基于舆情给出投资或决策建议。
2. **情感判定**：工具辅助 + 人工复核的混合结果，方法与误差边界须声明。
3. **受众定位**：（TODO：按业务配置实例化，默认品牌公关 / 政府事务 / IR）报告须明确声明受众与视角。

## 二、来源优先级

（TODO：按业务配置实例化渠道清单）默认层级：① 媒体数据库 ② 社交平台 ③ 公开抓取（每格活值附 `[来源, 抓取日期]`）。

## 三、基线锚定

对比锚属性、台账首建等通用差异见[基线类型模板第一节](../../templates/sentiment-monitoring/prompt-baseline-setup-template.md)。基线产出后，`{{BASELINE_REPORT_PATH}}` 即指向本报告；节标题为固化锚，正常运行**永不重跑**基线提示词。

## 四、追踪表（台账联动）

渠道清单、议题与关键词组、基线声量读数、情感判定规则、预警触发器（TODO：业务配置定义逐项）；基线运行后逐项回写 `{{REGISTRY_PATH}}`，未核实项注明「待核实」，prompt 模板内严禁填写活值。

## 五、报告结构骨架

九节固定骨架见[基线类型模板第三节](../../templates/sentiment-monitoring/prompt-baseline-setup-template.md)；业务固化锚节标题（TODO：实例化后声明并逐字继承）。

## 六、执行方式（建议）

1. 按渠道并行启动抓取与判定子代理，全部限定公开来源、逐点附抓取时间与 URL（TODO：按业务配置调整）。
2. 情感判定结果抽样人工复核（比例 TODO：业务配置规定）；无法核实项单列「待复核清单」。

## 七、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`；基线导航采用简化锚点目录。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版基线提示词 |
