# {{REGION}} · {{TOPIC}} · 年度假设刷新提示词（市场规模测算与预测型 · 泛用版）

> **用途**：每年固定窗口对模型假设做刷新与回测；关键假设失效信号触发器命中时专项插刷。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：刷新版报告落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY}}_annual.md`）+ 模型档案年度新版（`{{OUTPUT_REGISTRY}}`，另存不覆盖历史）；插刷件 `reports/{{YYYY-MM-DD}}-主题.md`（命名不在标准正则内，validate 仅 WARN 不阻断，属预期）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [年度刷新类型模板（市场规模测算与预测型）](../../templates/market-sizing/prompt-annual-refresh-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{PREVIOUS_REPORT_PATH}}  = 上一年度刷新版路径（首年刷新时为空，仅锚定基线）
{{BASELINE_REPORT_PATH}}  = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：模型档案文件名）
{{OUTPUT_PATH}}           = reports/{{YYYY}}_annual.md
{{OUTPUT_REGISTRY}}       = data/（TODO：模型档案年度新版文件名）
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：完成「假设审计 → 回测对照 → 参数刷新 → 预测修订」闭环；上年预测（各情景）逐条与实际值对照，偏差归因（假设失效 / 口径修订 / 结构突变），**上年预测原文保留不删除**；只修参数与假设、不推翻模型结构（结构变更走新基线）；继承已修正事实清单；无失效信号且窗口未到时不启动，不得虚构变化。

---

## 一、节拍与触发

年度假设刷新 + 失效信号插刷设计见[年度刷新类型模板第一节](../../templates/market-sizing/prompt-annual-refresh-template.md)；失效信号清单（TODO：`失效信号 → 受影响模块`）由业务配置维护。

## 二、项目专属硬性约束

1. **区间纪律**：修订后预测仍为区间 + 三情景，不给单一「神数字」。
2. **回测纪律**：归因结论与依据并列；上年原文保留，不删除不篡改。

## 三、各模块更新要点（业务实例化，TODO 按九节展开）

- **口径底座**（TODO：最新可得口径、口径修订留痕、新数据源评估）。
- **假设审计**（TODO：每条假设现状——成立 / 弱化 / 失效、依据更新、失效信号命中）。
- **参数刷新**（TODO：取值更新附新依据、敏感性重算、最敏感参数复判）。
- **预测修订**（TODO：三情景区间修订、与上年偏差归因）。

## 四、追踪表（模型档案联动）

运行前从 `{{REGISTRY_PATH}}` 读模型档案 → 假设逐条审计 → 运行后回写（假设版本、参数变更留痕、回测记录）；假设变更摘要覆盖全部假设的变更与回测结论。

## 五、执行方式（建议）

1. 回测先行：先用实际值完成上年预测对照与归因，再启动数据刷新子代理（口径底座 / 假设依据 / 参数依据）。
2. 主代理读取 `{{PREVIOUS_REPORT_PATH}}` 做差异合并；无法核实项单列「待复核清单」。

## 六、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`。
- 命名遵循仓库统一约定；基线报告常驻 `reports/` 顶层，不进入归档；模型档案年度新版另存，不覆盖历史。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版年度刷新提示词 |
