# {{REGION}} · {{TOPIC}} · 首次覆盖提示词（投资分析与尽调型 · 泛用版）

> **用途**：执行「{{REGION}} {{TOPIC}} 标的覆盖机制」的**机制建立**任务：产出首期标的覆盖报告（首次覆盖）与配套标的档案。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文八节覆盖报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_baseline_report.md`）+ 标的档案（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [基线报告类型模板（投资分析与尽调型）](../../templates/investment-research/prompt-baseline-setup-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，实例化时写入 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{BASELINE_DATE}}         = 首期基线日期
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：标的档案文件名）
{{REGISTRY_FORMAT}}       = md-table（TODO：按业务配置）
{{SOURCE_LANGUAGE_RULE}}  = 仅英文（默认；中国宏观例外见 engine/docs/source-language-policy.md）
{{REPORT_VERSION}}        = v1.0（首期基线固定）
```

**任务目标**：产出八节首次覆盖报告（投资要点、标的概况、行业与市场输入、财务分析与估值模型、风险清单、情景与敏感性、合规与边界）与标的档案首建；**结论必须明确**（评级 / 建议 / 估值区间）且与完整风险清单并存；运行后回写 `{{REGISTRY_PATH}}`；基线报告**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`。

---

## 一、项目专属硬性约束

1. **结论边界**：报告声明「不构成对不特定公众的投资邀约」，仅服务授权决策方；重大未决事项存在时结论降级为「有条件结论」并披露。
2. **估值纪律**：估值模型全假设可审计；估值区间多方法并列；情景为三档（乐观 / 基准 / 悲观）。
3. **合规**：信息来源合法性声明、利益冲突声明；非公开信息使用逐处标注授权依据（TODO：授权规则按业务配置）。
4. **受众定位**：（TODO：按业务配置实例化，明确授权决策方）。

## 二、来源优先级

（TODO：按业务配置实例化）默认层级：① 官方披露（公告 / 财报 / 监管文件） ② 授权数据室 / 管理层访谈 ③ 行业二手数据；事件核实以官方披露原文为准，媒体转述仅作线索。

## 三、基线锚定

对比锚属性、标的档案首建等通用差异见[基线类型模板第一节](../../templates/investment-research/prompt-baseline-setup-template.md)。基线产出后，`{{BASELINE_REPORT_PATH}}` 即指向本报告；节标题为固化锚，正常运行**永不重跑**基线提示词。

## 四、追踪表（标的档案联动）

标的监测项、估值假设、风险登记与「标的监测项 × 信息渠道」追踪表（TODO：业务配置定义逐项）；基线运行后逐项回写 `{{REGISTRY_PATH}}`，每格活值附 `[来源, 时点]`，prompt 模板内严禁填写活值。

## 五、报告结构骨架

八节固定骨架见[基线类型模板第三节](../../templates/investment-research/prompt-baseline-setup-template.md)；业务固化锚节标题（TODO：实例化后声明并逐字继承）。

## 六、执行方式（建议）

1. 财务与估值模块并行启动子代理（TODO：按业务配置调整）；估值假设逐条审计。
2. 主代理合并差异；重大未决事项显式披露；无法核实项单列「待复核清单」。

## 七、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`；基线导航采用简化锚点目录。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版首次覆盖提示词 |
