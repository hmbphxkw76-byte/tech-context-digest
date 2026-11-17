# {{REGION}} · {{TOPIC}} · 舆情月报提示词（舆情传播监测型 · 泛用版）

> **用途**：周期性（每月）刷新声量与情感读数、热点事件榜与预警状态。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文九节更新版报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_monthly.md`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [周期更新类型模板（舆情传播监测型）](../../templates/sentiment-monitoring/prompt-monthly-update-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{PREVIOUS_REPORT_PATH}}  = 最近一期月报路径（首期更新时为空，仅锚定基线）
{{BASELINE_REPORT_PATH}}  = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：舆情台账文件名）
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_monthly.md
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：完成「抓取 → 判定 → 对比 → 预警」闭环；环比须与基线期同渠道、同关键词组、同口径对比（口径变更显式标注并保留新旧对照）；九节结构与基线逐字一致；继承已修正事实清单；无预警命中时降级为核验轻运行，不得虚构变化。

---

## 一、节拍与触发

月度月报 + 事件触发预警升级两档设计见[周期类型模板第一节](../../templates/sentiment-monitoring/prompt-monthly-update-template.md)；预警触发器清单（TODO：声量阈值 / 情感阈值 / 突发负面）由业务配置维护；突发负面热点须当期核实（确认非机器人 / 断章取义）并升级。

## 二、项目专属硬性约束

1. **言论≠事实**：重大结论须与量化指标交叉验证；不基于舆情给出投资或决策建议。
2. **口径纪律**：环比口径变更须显式标注并保留新旧对照。

## 三、各模块更新要点（业务实例化，TODO 按九节展开）

- **舆论场结构**（TODO：渠道声量变化、新渠道出现、关键参与方变动）。
- **议题声量**（TODO：环比 / 同比、新议题登记、旧议题降温归档）。
- **情感判定**（TODO：分布变化、判定规则命中、人工复核抽样结果）。
- **风险预警**（TODO：信号命中状态、热点事件榜、意见领袖观点摘编附原文链接、交叉验证结论）。

## 四、追踪表（台账联动）

运行前从 `{{REGISTRY_PATH}}` 读议题与渠道活值 → 抓取核验 → 运行后回写；逐项填写「是否更新」，未变动项注明「截至 {{CURRENT_DATE}} 无更新」。舆情变更摘要覆盖全部监测议题（声量 / 情感 / 预警状态）。

## 五、执行方式（建议）

按渠道并行启动抓取与判定子代理，逐点附抓取时间与 URL；主代理读取 `{{PREVIOUS_REPORT_PATH}}` 做差异合并；情感判定抽样人工复核；无法核实项单列「待复核清单」。

## 六、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`。
- 命名遵循仓库统一约定；基线报告常驻 `reports/` 顶层，不进入归档；周期报告按归档保留策略执行。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版月报提示词 |
