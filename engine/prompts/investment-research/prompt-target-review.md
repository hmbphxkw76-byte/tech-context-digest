# {{REGION}} · {{TOPIC}} · 标的复核提示词（投资分析与尽调型 · 泛用版 · 定期复核 + 事件触发）

> **用途**：定期复核（财报 / 定期数据窗口）与事件触发复核（重大事项披露后）统一入口。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：更新版报告（`reports/{{YYYY-Qn}}_quarterly.md` 或 `reports/{{YYYY}}_annual.md`，由业务配置规定）或事件专项修订件 `reports/{{YYYY-MM-DD}}-主题.md`（命名不在标准正则内，validate 仅 WARN 不阻断，属预期）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [事件触发更新类型模板（投资分析与尽调型）](../../templates/investment-research/prompt-target-update-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{TRIGGER_TYPE}}          = 本次触发类型（定期复核 / 事件名称，TODO）
{{PREVIOUS_REPORT_PATH}}  = 最近一期更新版路径（首次复核时为空，仅锚定首次覆盖）
{{BASELINE_REPORT_PATH}}  = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：标的档案文件名）
{{OUTPUT_PATH}}           = 由 {{TRIGGER_TYPE}} 决定（见用途）
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：完成「事件核验 → 假设复核 → 估值更新 → 结论修订」闭环；估值假设变更逐条留痕（旧值 → 新值 → 依据）；只修参数与假设、不推翻模型结构（结构变更走重新覆盖）；结论变化方向（维持 / 上调 / 下调 / 降级为有条件）显式声明；无触发且窗口未到时登记册标注「截至 {{CURRENT_DATE}} 无更新」。

---

## 一、节拍与触发

定期复核 + 事件触发设计见[事件触发更新类型模板第一节](../../templates/investment-research/prompt-target-update-template.md)；触发器清单（TODO：并购 / 管理层变动 / 诉讼 / 政策冲击等 `事件 → 受影响模块`）由业务配置维护；重大事项当期核实并复核结论，不等待定期窗口。

## 二、项目专属硬性约束

1. **官方原文铁律**：事件核实以官方披露原文（公告、财报、监管文件）为准，媒体转述仅作线索。
2. **估值纪律**：假设变更逐条留痕；情景与敏感性重算；反向声音更新。

## 三、各模块更新要点（业务实例化，TODO 按八节展开）

- **标的概况**（TODO：股权与治理变动、关键合同与资质变化）。
- **财务与估值**（TODO：最新财务序列、估值假设逐条复核、估值区间更新）。
- **风险登记**（TODO：新增风险、已缓解风险归档、重大未决事项状态）。
- **结论复核**（TODO：投资要点逐条对照新证据、情景与敏感性重算、反向声音更新）。

## 四、追踪表（标的档案联动）

运行前从 `{{REGISTRY_PATH}}` 读标的档案 → 核验 → 运行后回写（财务序列、假设变更留痕、风险登记更新）。事件影响摘要覆盖本次触发事件、受影响假设与结论变化方向。

## 五、执行方式（建议）

1. 事件核验先行：以官方披露原文为准完成事件事实登记，再启动财务与估值复核子代理。
2. 主代理读取 `{{PREVIOUS_REPORT_PATH}}` 做差异合并；非公开信息使用逐处标注授权依据；无法核实项单列「待复核清单」。

## 六、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`。
- 命名遵循仓库统一约定；首次覆盖报告常驻 `reports/` 顶层，不进入归档；更新版按归档保留策略执行。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版标的复核提示词 |
