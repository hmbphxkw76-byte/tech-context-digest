# {{REGION}} · {{TOPIC}} · 专题续作提示词（白皮书·专题深度型 · 泛用版 · 选题制）

> **用途**：专题续作统一入口——新选题白皮书、年度系列篇、框架修订篇（当次类型由 {{STUDY_TYPE}} 指定）。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：新选题件 `reports/{{YYYY-MM-DD}}-主题.md` 或框架修订件 `reports/{{YYYY-MM-DD}}-主题-修订.md`、年度系列篇 `reports/{{YYYY}}_annual.md`（+ 同名 html）。新选题与修订篇命名不在工具链标准正则内，validate 仅 WARN 不阻断，属预期。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [专题续作类型模板（白皮书·专题深度型）](../../templates/whitepaper/prompt-topic-study-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{STUDY_TYPE}}            = 本次类型（新选题 / 年度系列 / 框架修订，TODO：选题名称）
{{BASELINE_REPORT_PATH}}  = reports/{{YYYY-MM}}_baseline_report.md
{{PREVIOUS_REPORT_PATH}}  = 最近一篇同系列白皮书路径（如无则空）
{{REGISTRY_PATH}}         = data/（TODO）
{{OUTPUT_PATH}}           = 由 {{STUDY_TYPE}} 决定（见用途）
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：按[专题续作类型模板](../../templates/whitepaper/prompt-topic-study-template.md)续作协议执行「选题准入 → 框架复用 / 修订 → 深度论证 → 审校发布」闭环；系列篇与上年篇逐节对照，上年观点原文保留、复判结论（维持 / 修正 / 撤回）显式声明；框架修订篇须新旧框架对照，不静默替换；无准入选题不启动。

---

## 一、续作协议要点

1. **读取锚**：读取 `{{BASELINE_REPORT_PATH}}` 与最近同系列白皮书，继承原创框架、品牌规范与已核实结论。
2. **事实纪律**：观点可以鲜明，事实论据逐点附来源；新证据挑战既有观点时显式复判，不静默改口。
3. **发布纪律**：审校清单全部执行并留痕后才可发布；重大未决项存在时不发布。

## 二、各模块要点（业务实例化，TODO 按 {{STUDY_TYPE}} 展开）

- **问题与框架**（TODO：新选题问题定义、复用 / 扩展 / 新建框架决策、与基线框架关系声明）。
- **深度论证**（TODO：沿框架逐要素展开，事实论据逐点附来源，推断显式标注）。
- **案例佐证**（TODO：入选标准、逐案例分析对框架的支撑 / 修正）。
- **观点复判**（系列篇，TODO：上年观点逐条对照新证据）。
- **倡议**（TODO：面向受众的行动倡议，标「倡议」）。

## 三、追踪表（选题档案联动）

运行前从 `{{REGISTRY_PATH}}` 读选题库与审校标准 → 选题准入 → 运行后回写（选题状态、框架修订留痕、系列篇登记）。

## 四、执行方式（建议）

1. 选题准入先行：对照准入标准评审，通过后按论证模块并行启动研究子代理。
2. 主代理读取 `{{PREVIOUS_REPORT_PATH}}` 做框架对齐与差异合并；无法核实项单列「待复核清单」。

## 五、渲染与交付

- 交付包 = 报告 + 审校记录；已发布白皮书常驻 `reports/` 顶层，不进入归档；勘误以勘误件形式发布，不改原稿。
- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版专题续作提示词 |
