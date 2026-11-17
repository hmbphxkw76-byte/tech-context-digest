# {{REGION}} · {{TOPIC}} · 月度更新提示词（竞争情报监测型 · 泛用版）

> **用途**：周期性（每月）刷新竞争动态矩阵与竞品档案；重大动作触发器命中时亦走本提示词做对应模块重点更新。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文九节更新版报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_monthly.md`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [周期更新类型模板（竞争情报监测型）](../../templates/competitive-intelligence/prompt-monthly-update-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{PREVIOUS_REPORT_PATH}}  = 最近一期月度报告路径（首期更新时为空，仅锚定基线）
{{BASELINE_REPORT_PATH}}  = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：竞品档案库文件名）
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_monthly.md
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：以公开来源为依据、以上一期报告与首期基线为对比锚，完成「采集 → 核验 → 矩阵刷新 → 影响提示」闭环；九节结构与基线逐字一致；继承已修正事实清单；无触发器命中且无新动作时降级为核验轻运行（登记册标注「截至 {{CURRENT_DATE}} 无更新」），不得虚构变化。

---

## 一、节拍与触发

月度主更新 + 事件触发升级两档设计见[周期类型模板第一节](../../templates/competitive-intelligence/prompt-monthly-update-template.md)；触发器清单（TODO：融资 / 并购 / 换帅 / 定价重构 / 新产品线等 `事件 → 受影响模块`）由业务配置维护，命中即当期核实并升级，不等待月度窗口。

## 二、项目专属硬性约束

1. **信息边界**：只用公开合法信息；关键动作至少 2 家独立来源确认，单源标「单源待证」。
2. **结论边界**：影响提示标「判断 / 推断」，与事实分离。

## 三、各模块更新要点（业务实例化，TODO 按九节展开）

- **竞争格局**（TODO：份额口径更新、新进入者 / 退出者、格局演变判断复核）。
- **竞品档案**（TODO：产品矩阵、定价与促销、渠道生态、组织与人事、招聘动向）。
- **动态矩阵**（TODO：本期动作逐条登记，编号 + 玩家 + 动作 + 日期 + 来源 URL；信号规则命中状态）。
- **影响提示**（TODO：对自身定位的威胁 / 机会，标「判断 / 推断」）。

## 四、追踪表（档案库联动）

运行前从 `{{REGISTRY_PATH}}` 读竞品档案活值 → 逐家核验 → 运行后回写；每期逐项填写「是否更新」，未变动项注明「截至 {{CURRENT_DATE}} 无更新」。数据变更摘要至少覆盖全部监测竞品与信号规则状态。

## 五、执行方式（建议）

按信息渠道并行启动研究子代理（TODO：分工按业务配置），全部限定公开来源、逐点引用 URL；主代理读取 `{{PREVIOUS_REPORT_PATH}}` 做差异合并，继承已修正事实清单；无法核实项单列「待复核清单」。

## 六、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`。
- 命名遵循仓库统一约定；基线报告常驻 `reports/` 顶层，不进入归档；周期报告按归档保留策略执行。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版月度提示词 |
