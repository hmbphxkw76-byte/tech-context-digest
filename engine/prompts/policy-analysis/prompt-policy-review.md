# {{REGION}} · {{TOPIC}} · 政策解读提示词（政策法规解读型 · 泛用版 · 事件触发 + 年度复盘）

> **用途**：事件触发单份解读（新政策 / 修订 / 配套细则出台后）与年度台账复盘统一入口。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：单份解读件 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM-DD}}-主题.md`）或年度复盘（`reports/{{YYYY}}_annual.md` + 台账年度新版 `{{OUTPUT_REGISTRY}}` 另存不覆盖）。解读件命名不在标准正则内，validate 仅 WARN 不阻断，属预期。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [事件触发解读类型模板（政策法规解读型）](../../templates/policy-analysis/prompt-policy-review-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{TRIGGER_TYPE}}          = 本次触发类型（新政策 / 修订 / 细则 / 年度复盘，TODO）
{{BASELINE_REPORT_PATH}}  = reports/{{YYYY-MM}}_baseline_report.md
{{PREVIOUS_REPORT_PATH}}  = 上期解读 / 复盘路径（如无则空，仅锚定基线）
{{REGISTRY_PATH}}         = data/（TODO：政策台账文件名）
{{OUTPUT_PATH}}           = 由 {{TRIGGER_TYPE}} 决定（见用途）
{{OUTPUT_REGISTRY}}       = 年度复盘时填写（台账年度新版路径）
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：完成「原文回溯 → 逐条解读 → 影响评估 → 台账更新」闭环；新政策先登记发布与生效日期、官方 URL 后才可进入解读；征求意见稿登记但标注「非最终文本，以正式发布为准」；无触发时不启动新解读，台账标注「截至 {{CURRENT_DATE}} 无更新」。

---

## 一、节拍与触发

事件触发解读 + 年度台账复盘设计见[事件触发解读类型模板第一节](../../templates/policy-analysis/prompt-policy-review-template.md)；监测触发器清单（TODO：`渠道 / 政策名称 → 动作`）由业务配置维护。

## 二、项目专属硬性约束

1. **官方原文铁律**：媒体转述仅作线索；引用逐条附官方原文 URL 与版本日期。
2. **结论边界**：不构成法律意见；应对建议标「建议」；歧义条款多解并列。

## 三、各模块要点（业务实例化，TODO 按类型模板第三节框架展开）

- **政策原文**（TODO：发布机构、文号、日期、适用范围、关键条款摘编逐条附 URL）。
- **逐条解读**（TODO：条款含义、新旧制度衔接对照、歧义多解、官方答问与细则对照）。
- **影响评估**（TODO：影响对象矩阵增量、过渡期与合规时点）。
- **应对建议**（TODO：合规要点、待明确事项清单，标「建议」）。

## 四、追踪表（政策台账联动）

运行前从 `{{REGISTRY_PATH}}` 读台账 → 增量登记 / 状态变更 → 运行后回写；逐项填写「是否更新」，未变动项注明「截至 {{CURRENT_DATE}} 无更新」。政策变更摘要覆盖本期新增 / 修订 / 生效 / 废止清单及影响方向。

## 五、执行方式（建议）

1. 原文回溯先行：完成官方原文登记（URL、版本日期、文本完整性）后再启动逐条解读子代理。
2. 主代理读取 `{{BASELINE_REPORT_PATH}}` 做框架对齐；无法核实项单列「待复核清单」。

## 六、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`。
- 命名遵循仓库统一约定；基线报告常驻 `reports/` 顶层，不进入归档；解读件按归档保留策略执行。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版政策解读提示词 |
