# 迪拜（阿联酋） · AI 网安竞争格局 · 事件触发专项提示词（竞争情报监测型）

> **用途**：重大竞品动作（融资 / 并购 / 换帅 / 定价重构 / 新产品线 / 合规资质 / 旗舰活动）当期核实与专项更新，不等待月度窗口。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：专项更新件 `reports/{{YYYY-MM-DD}}-主题.html` + 档案库增量回写。命名不在工具链标准正则内，validate 仅 WARN 不阻断，属预期。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（竞争情报监测型）](../../../../../engine/templates/competitive-intelligence/prompt-monthly-update-template.md) × [业务专属配置](./business-config.md)。冲突时以本文件为准。

---

## 运行变量（每次运行前填写）

固定值（见[业务配置第一节](./business-config.md)）：

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = AI 网安竞争格局
{{REGISTRY_PATH}}        = data/processed/tech/competitive-intelligence/dubai/ai_cyber_competition_registry.md
{{REGISTRY_FORMAT}}      = md-table
{{BASELINE_REPORT_PATH}} = reports/2026-12_baseline_report.html
{{FRESHNESS_PRIORITY}}   = 最新官方 / 一手发布 > 上期值 > 第三方研究 > 媒体转述
{{SOURCE_LANGUAGE_RULE}} = 仅英文（官方与权威英文页优先；中文源仅作线索，须标「需核实原文」）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/competitive-intelligence/dubai
```

运行时变量：

```
{{CURRENT_DATE}}         = 本次执行日期
{{EVENT_NAME}}           = 本次触发事件名称（运行填写）
{{PREVIOUS_REPORT_PATH}} = 最近一期月度报告路径
{{OUTPUT_PATH}}          = reports/{{YYYY-MM-DD}}-主题.html（运行填写事件主题）
{{REPORT_VERSION}}       = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：按[周期类型模板第一节事件触发档](../../../../../engine/templates/competitive-intelligence/prompt-monthly-update-template.md)执行对应模块重点刷新；事实与判断分离；完成档案库回写与升级记录；无触发时在登记册标注「截至 {{CURRENT_DATE}} 无更新」。触发事件 → 受影响模块对照见[业务配置第七节](./business-config.md)。

---

## 一、执行要点

1. 触发事件先经 2 家独立来源核实（单源标「单源待证」），核实后才进入刷新。
2. 只刷新受影响模块，其余模块沿用上期值并注明；全量刷新仍归月度窗口。
3. 影响提示标「判断 / 推断」；无法核实项单列「待复核清单」。

## 二、联动与交付

- 档案库增量回写 `{{REGISTRY_PATH}}`（md-table）；月度窗口到达时本专项内容并入月度报告动态矩阵。
- 交付格式同[基线提示词](./prompt-baseline-setup.md)：纯 HTML 交付（canonical 富样式自包含），md 源稿可选存档、不参与 `md2html.py` 自动转换；遵循 `engine/docs/page-build-spec.md` 与 `engine/docs/page-build-governance.md`；`python engine/tools/lint_reports.py` 与 `python engine/tools/page_build_check.py` 必须零 `[E]`。
- 命名 `reports/{{YYYY-MM-DD}}-主题.html`（追加件）；命名不在工具链标准正则内，validate 仅 WARN 不阻断，属预期。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 依竞争情报监测型脚手架第五节实例化：填入业务配置固定值、事件触发执行要点与档案库回写；纯 HTML 交付 |
