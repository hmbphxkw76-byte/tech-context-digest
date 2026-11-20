# {{REGION}} · {{TOPIC}} · 首期基线报告提示词（竞争情报监测型 · 泛用版）

> **用途**：执行「{{REGION}} {{TOPIC}} 竞争情报持续监测机制」的**机制建立**任务：产出首期竞争格局基线报告与配套竞品档案库。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文九节基线报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_baseline_report.md`）+ 竞品档案库（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [基线报告类型模板（竞争情报监测型）](../../templates/competitive-intelligence/prompt-baseline-setup-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，实例化时写入 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{BASELINE_DATE}}         = 首期基线日期
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：竞品档案库文件名）
{{REGISTRY_FORMAT}}       = md-table（TODO：按业务配置）
{{SOURCE_LANGUAGE_RULE}}  = 仅英文（默认；中国宏观例外见 engine/docs/source-language-policy.md）
{{REPORT_VERSION}}        = v1.0（首期基线固定）
```

**任务目标**：产出九节竞争格局基线报告与竞品档案库首建。覆盖业务配置声明的全部监测竞品（逐家档案卡，每格附 `[来源, 日期]`）；运行后回写 `{{REGISTRY_PATH}}`；基线报告**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`；「已修正事实清单」为空，产生修正后逐条补记（格式见通用基座第五节）。

---

## 一、项目专属硬性约束

通用约束（逐点引用、事实与推断分离、口径标注、数据纪律）自动继承通用基座第三节。本类型额外强制：

1. **信息边界**：只采集公开合法信息（官网、财报、招聘、应用商店、专利、公开社媒）；不使用非公开渠道，不伪造无法核实的动作记录。
2. **结论边界**：威胁 / 机会提示标「判断 / 推断」，与事实分离；不做对手成败断言。
3. **受众定位**：（TODO：按业务配置实例化，默认产品 / 市场 / 战略团队）报告须明确声明受众与视角。

## 二、来源优先级

（TODO：按业务配置实例化机构清单）默认层级：① 官网 / 财报 / 公告 ② 招聘 / 应用商店 / 专利 ③ 第三方研究 ④ 公开社媒。关键动作至少 2 家独立来源确认，单源标「单源待证」。

## 三、基线锚定

对比锚属性、无上期报告、档案库首建等通用差异见[基线类型模板第一节](../../templates/competitive-intelligence/prompt-baseline-setup-template.md)。本项目实例化：

- 基线产出后，`{{BASELINE_REPORT_PATH}}` 即指向本报告；后续周期提示词的该变量值保持不变。
- 已产出基线的节标题为固化锚，正常运行**永不重跑**基线提示词；本文件仅用于结构重置时参照。

## 四、追踪表（档案库联动）

监测竞品清单、信号规则与「监测竞品 × 优先信息渠道」追踪表（TODO：业务配置定义逐项）见实例化后的 business-config；基线运行后逐项回写 `{{REGISTRY_PATH}}`，未核实项注明「待核实」，prompt 模板内严禁填写活值。

## 五、报告结构骨架

九节固定骨架见[基线类型模板第三节](../../templates/competitive-intelligence/prompt-baseline-setup-template.md)；业务固化锚节标题（TODO：实例化后声明并逐字继承）。

## 六、执行方式（建议）

1. 按信息渠道并行启动研究子代理（官网与财报 / 招聘与组织 / 应用商店与产品 / 公开社媒与专利），全部限定公开来源、逐点引用 URL（TODO：按业务配置调整分工）。
2. 主代理合并差异，冲突信息保留双份引用；无法核实项单列「待复核清单」。

## 七、渲染与交付

- 交付格式：md + 同目录自包含 HTML（仓库根目录执行 `python engine/tools/md2html.py`）。
- HTML 须通过 `python engine/tools/lint_reports.py`（表格标签配对强制）。
- 基线导航采用简化锚点目录，不升级为 `.report-nav`。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版基线提示词 |
