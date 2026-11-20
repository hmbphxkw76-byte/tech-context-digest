# {{REGION}} · {{TOPIC}} · 首期可行性论证提示词（可行性与市场进入型 · 泛用版）

> **用途**：执行「{{REGION}} {{TOPIC}} 可行性评估机制」的**机制建立**任务：产出首期可行性论证报告与配套评估框架档案。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文九节论证报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_baseline_report.md`）+ 评估框架档案（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [基线报告类型模板（可行性与市场进入型）](../../templates/feasibility-study/prompt-baseline-setup-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，实例化时写入 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{BASELINE_DATE}}         = 首期基线日期
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：框架档案文件名）
{{REGISTRY_FORMAT}}       = md-table（TODO：按业务配置）
{{SOURCE_LANGUAGE_RULE}}  = 仅英文（默认；中国宏观例外见 engine/docs/source-language-policy.md）
{{REPORT_VERSION}}        = v1.0（首期基线固定）
```

**任务目标**：产出九节可行性论证报告（评估框架、市场 / 技术运营 / 财务 / 法规可行性、风险与缓解、结论与实施路线图）与框架档案首建；**必须收敛到单一 Go / No-Go / 有条件 Go 建议**（不允许双向平衡不表态），与完整风险清单并存；运行后回写 `{{REGISTRY_PATH}}`；基线报告**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`。

---

## 一、项目专属硬性约束

1. **集成纪律**：市场、规模、政策输入优先引用本仓其他类型报告的最新版（注明来源报告与口径），不重复推导；缺口项专项补充并标注「本项目专项调研」。
2. **结论边界**：仅对授权决策方负责；「有条件 Go」须列明条件清单与验证时点；财务测算全假设可审计、三情景呈现。
3. **受众定位**：（TODO：按业务配置实例化，明确授权决策方）。

## 二、来源优先级

（TODO：按业务配置实例化）默认层级：① 本仓类型报告引用 ② 实地 / 当地访谈 ③ 二手行业数据 ④ 财务假设；每格活值附 `[来源, 时点]`。

## 三、基线锚定

对比锚属性、框架档案首建等通用差异见[基线类型模板第一节](../../templates/feasibility-study/prompt-baseline-setup-template.md)。基线产出后，`{{BASELINE_REPORT_PATH}}` 即指向本报告；节标题为固化锚，正常运行**永不重跑**基线提示词。

## 四、追踪表（框架档案联动）

评估维度与权重、Go/No-Go 判定标准与阈值、财务测算假设清单、可引用报告清单、复盘时点（TODO：业务配置定义逐项）；基线运行后逐项回写 `{{REGISTRY_PATH}}`，prompt 模板内严禁填写活值。

## 五、报告结构骨架

九节固定骨架见[基线类型模板第三节](../../templates/feasibility-study/prompt-baseline-setup-template.md)；业务固化锚节标题（TODO：实例化后声明并逐字继承）。

## 六、执行方式（建议）

1. 输入收集先行：盘点可引用的既有类型报告，缺口项启动专项调研子代理，逐点引用（TODO：按业务配置调整）。
2. 财务假设逐条审计；重大未决项存在时结论降级为「有条件 Go」；无法核实项单列「待复核清单」。

## 七、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`；基线导航采用简化锚点目录。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版基线提示词 |
