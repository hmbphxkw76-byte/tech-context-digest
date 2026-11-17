# {{REGION}} · {{TOPIC}} · 周报提示词（行业趋势周报型 · 泛用版）

> **用途**：周期性（每周）刷新主题板块与数据看板，产出八节周报；触发器命中时对应板块重点更新。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文八节周报（落盘 `{{OUTPUT_PATH}}`，命名 `{{YYYY-MM-DD}}_weekly`，日期 = 数据截止日）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [周期更新类型模板（行业趋势周报型）](../../templates/trend-weekly/prompt-weekly-monitor-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{DATA_CUTOFF}}           = 数据截止日（周报命名与标题锚定此日期，非执行日）
{{PREVIOUS_REPORT_PATH}}  = 最近一期周报路径（首期为空，仅锚定基线）
{{BASELINE_REPORT_PATH}}  = reports/{{YYYY-MM}}_baseline_report.html
{{REGISTRY_PATH}}         = data/（TODO：台账文件名）
{{OUTPUT_PATH}}           = reports/{{DATA_CUTOFF}}_weekly.html
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：以公开来源为依据、以上期周报为对比锚，完成「采集 → 核验 → 看板刷新 → 可执行启示」闭环；八节结构与基线逐字一致；继承已修正事实清单；无实质变化时降级为核验轻运行（台账标注「截至 {{CURRENT_DATE}} 无更新」），不得虚构变化；与上期数据截止日仅隔 1 日时在报告头部标注「T+1 刷新」。

---

## 一、节拍与触发

周节拍 + 事件触发升级设计见[周期类型模板第一节](../../templates/trend-weekly/prompt-weekly-monitor-template.md)；触发器清单（TODO：重大发布 / 监管动作 / 安全事故 / 融资并购等 `事件 → 受影响板块`）由业务配置维护，命中即当期核实并升级，不等待下周窗口。

## 二、项目专属硬性约束

1. **事实与推断分离**：【事实】/【预测】（带来源与置信度）/「推断」显式标注；媒体转述标「需核实原文」并回官方页校验。
2. **口径纪律**：同一指标多口径并列，不平均、不静默择一；跨机构数字不可相加。
3. **反方证据**：对核心结论的公开质疑必须收录进「风险与不确定性」。
4. **结论边界**：可执行启示标「推断」，只给「条件 → 判读 → 框架性含义 → 风险提示」。

## 三、八节固定结构（不得增删节、调整顺序）

1. **本周要点 Top5**：每条 = 结论一句话 + 关键数字 + 来源；【事实】/【预测】标注。
2. **主题板块一**（TODO：按 business-config 主题矩阵实例化；按「新事实 → 机制解读（推断）→ 对受众的含义」组织）。
3. **主题板块二**（TODO）。
4. **主题板块三**（TODO）。
5. **数据看板**：指标 × 上期值 × 本期值 × 变化 × 来源 × 口径，逐行与台账联动。
6. **风险与不确定性**：来源可靠性 / 反向证据 / 口径冲突 / 基准自报。
7. **可执行启示**：面向受众（TODO：受众画像），标「推断」。
8. **参考来源**：逐条 URL；转述标「需核实原文」。

## 四、执行步骤

1. 填变量 → 读 `{{PREVIOUS_REPORT_PATH}}` 与基线，继承已修正事实清单（防回退）。
2. 按来源分级采集本周新事实（TODO：按 business-config 来源清单；建议按渠道并行研究子代理，逐点引用 URL）。
3. 逐块更新主题板块；数据看板逐行核对并回写台账（逐项填「是否更新」，未变动项注明「截至 {{CURRENT_DATE}} 无更新」）。
4. 撰写八节周报（顶部导航锚点与节标题逐字一致），落盘 `{{OUTPUT_PATH}}`。

## 五、渲染与交付

- 交付格式由业务配置声明：md 源稿 + 同目录自包含 HTML；或纯 HTML（md 源稿存 `sources/`，不参与 `md2html.py` 自动转换）。
- HTML 须通过 `python engine/tools/lint_reports.py` 与 `python engine/tools/compliance_check.py --file {{OUTPUT_PATH}}`。
- 周报按归档保留策略执行（weekly 保留 12 期）。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版周报提示词 |
