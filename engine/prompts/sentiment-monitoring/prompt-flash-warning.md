# {{REGION}} · {{TOPIC}} · 预警专项提示词（舆情传播监测型 · 泛用版）

> **用途**：突发负面热点当期核实（确认非机器人 / 断章取义）与专项预警，不等待月度窗口。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：专项预警件 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM-DD}}-主题.md`）+ 台账增量回写。命名不在工具链标准正则内，validate 仅 WARN 不阻断，属预期。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [周期更新类型模板（舆情传播监测型）](../../templates/sentiment-monitoring/prompt-monthly-update-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期
{{EVENT_NAME}}            = 本次触发热点名称（TODO）
{{PREVIOUS_REPORT_PATH}}  = 最近一期月报路径
{{BASELINE_REPORT_PATH}}  = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO）
{{OUTPUT_PATH}}           = reports/{{YYYY-MM-DD}}-（TODO：事件主题）.md
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：按[周期类型模板第一节事件触发档](../../templates/sentiment-monitoring/prompt-monthly-update-template.md)执行对应模块重点刷新；完成人工复核与台账回写；预警只描述舆论态势与风险信号，不基于舆情给出投资或决策建议。

---

## 一、执行要点

1. 先核验热点真实性（机器人 / 水军 / 断章取义排查，方法与抽样比例 TODO：业务配置规定）。
2. 只刷新受影响模块，其余模块沿用上期值并注明。
3. 关键参与方观点摘编逐条附原文链接；无法核实项单列「待复核清单」。

## 二、联动与交付

- 台账增量回写 `{{REGISTRY_PATH}}`；月度窗口到达时本专项内容并入月报风险预警模块。
- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版预警提示词 |
