# {{REGION}} · {{TOPIC}} · 首期基准测算提示词（市场规模测算与预测型 · 泛用版）

> **用途**：执行「{{REGION}} {{TOPIC}} 市场测算机制」的**机制建立**任务：产出首期基准测算报告与配套测算模型档案。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文九节基线报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_baseline_report.md`）+ 测算模型档案（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [基线报告类型模板（市场规模测算与预测型）](../../templates/market-sizing/prompt-baseline-setup-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，实例化时写入 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{BASELINE_DATE}}         = 首期基线日期
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：模型档案文件名）
{{REGISTRY_FORMAT}}       = md-table（TODO：按业务配置）
{{SOURCE_LANGUAGE_RULE}}  = （TODO：来源语言规则）
{{REPORT_VERSION}}        = v1.0（首期基线固定）
```

**任务目标**：产出九节基准测算报告（方法与模型结构、口径底座、基准年测算、三情景预测、敏感性分析）与模型档案首建；**核心交付物是可审计的测算模型**——每个数字可追溯到假设与来源；运行后回写 `{{REGISTRY_PATH}}`；基线报告**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`。

---

## 一、项目专属硬性约束

1. **区间纪律**：测算与预测一律以区间 + 三情景（乐观 / 基准 / 悲观）呈现，不给单一「神数字」；全部预测标「推断」。
2. **结论边界**：不做投资评级、不出具进入决策建议（边界归投资尽调型、可行性型）。
3. **口径纪律**：多口径并列不合并，选用口径声明理由；无依据参数标「估计值 + 估计方法」。
4. **受众定位**：（TODO：按业务配置实例化，默认创业者 / 投资人 / 产品战略）。

## 二、来源优先级

（TODO：按业务配置实例化数据源清单）默认层级：① 官方统计 ② 第三方数据 ③ 自建假设（逐条附依据）；模型透明度优先于数字精确度。

## 三、基线锚定

对比锚属性、模型档案首建等通用差异见[基线类型模板第一节](../../templates/market-sizing/prompt-baseline-setup-template.md)。基线产出后，`{{BASELINE_REPORT_PATH}}` 即指向本报告；节标题为固化锚，正常运行**永不重跑**基线提示词。

## 四、追踪表（模型档案联动）

市场定义与边界、测算路径、假设清单（依据 / 强度 / 失效信号）、参数取值依据、回测规则（TODO：业务配置定义逐项）；基线运行后逐项回写 `{{REGISTRY_PATH}}`，prompt 模板内严禁填写活值。

## 五、报告结构骨架

九节固定骨架见[基线类型模板第三节](../../templates/market-sizing/prompt-baseline-setup-template.md)；业务固化锚节标题（TODO：实例化后声明并逐字继承）。

## 六、执行方式（建议）

1. 测算路径逐条推演（公式 + 参数 + 取值依据 + 来源），多路径交叉验证（TODO：按业务配置调整）。
2. 主代理合并差异；无依据参数标「估计值」；无法核实项单列「待复核清单」。

## 七、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`；基线导航采用简化锚点目录。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版基线提示词 |
