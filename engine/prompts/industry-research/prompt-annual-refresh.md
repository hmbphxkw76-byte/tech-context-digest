# {{REGION}} · {{TOPIC}} · 年度刷新提示词（行业深度研究型 · 泛用版）

> **用途**：每年固定窗口对行业全景做全量刷新；重大结构性事件触发器命中时提前插刷对应模块。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：刷新版报告落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY}}_annual.md`）；插刷件 `reports/{{YYYY-MM-DD}}-主题.md`（命名不在标准正则内，validate 仅 WARN 不阻断，属预期）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [年度刷新类型模板（行业深度研究型）](../../templates/industry-research/prompt-annual-refresh-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{PREVIOUS_REPORT_PATH}}  = 上一年度刷新版路径（首年刷新时为空，仅锚定基线）
{{BASELINE_REPORT_PATH}}  = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：边界档案文件名）
{{OUTPUT_PATH}}           = reports/{{YYYY}}_annual.md
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：完成「口径复核 → 数据刷新 → 格局更新 → 趋势复判」闭环；上年趋势判断逐条对照实际进展（命中 / 部分命中 / 未命中），复判结论与依据并列，**上年判断原文保留不删除**；九节结构与基线逐字一致；继承已修正事实清单；无触发且窗口未到时不启动，不得虚构变化。

---

## 一、节拍与触发

年度刷新 + 重大事件插刷设计见[年度刷新类型模板第一节](../../templates/industry-research/prompt-annual-refresh-template.md)；插刷触发器清单（TODO：重大并购 / 监管重构 / 技术代际切换等 `事件 → 受影响模块`）由业务配置维护。

## 二、项目专属硬性约束

1. **中性立场**：不给投资评级、不出具 Go/No-Go 决策建议；趋势复判结论与依据并列。
2. **口径纪律**：多口径并列不合并；口径修订留痕。

## 三、各模块更新要点（业务实例化，TODO 按九节展开）

- **产业链**（TODO：环节进出、价值分布迁移、传导关系变化）。
- **规模与格局**（TODO：最新口径规模与增速、集中度变化、口径修订留痕）。
- **玩家**（TODO：清单复核与进出登记、逐家要点更新）。
- **驱动与风险**（TODO：证据更新、新增风险、失效驱动归档）。
- **趋势**（TODO：上年复判 + 新趋势推导，反向声音至少 2 条）。

## 四、追踪表（边界档案联动）

运行前从 `{{REGISTRY_PATH}}` 读边界档案（行业边界、产业链口径、玩家清单）→ 复核有效性 → 运行后回写（口径变更留痕、玩家进出登记）。数据变更摘要至少覆盖全部研究维度与口径清单。

## 五、执行方式（建议）

按研究维度并行启动研究子代理，全部逐点引用、二手数据交叉验证；主代理读取 `{{PREVIOUS_REPORT_PATH}}` 做差异合并；无法核实项单列「待复核清单」。

## 六、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`。
- 命名遵循仓库统一约定；基线报告常驻 `reports/` 顶层，不进入归档。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版年度刷新提示词 |
