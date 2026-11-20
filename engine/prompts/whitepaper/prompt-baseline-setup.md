# {{REGION}} · {{TOPIC}} · 首份白皮书提示词（白皮书·专题深度型 · 泛用版）

> **用途**：执行「{{REGION}} {{TOPIC}} 白皮书机制」的**机制建立**任务：产出首份白皮书与配套选题与品牌规范档案。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文八节白皮书（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_baseline_report.md`）+ 选题与品牌规范档案（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [基线报告类型模板（白皮书·专题深度型）](../../templates/whitepaper/prompt-baseline-setup-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，实例化时写入 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{BASELINE_DATE}}         = 首期基线日期
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：选题与品牌规范档案文件名）
{{REGISTRY_FORMAT}}       = md-table（TODO：按业务配置）
{{SOURCE_LANGUAGE_RULE}}  = 仅英文（默认；中国宏观例外见 engine/docs/source-language-policy.md）
{{REPORT_VERSION}}        = v1.0（首期基线固定）
```

**任务目标**：产出八节首份白皮书（问题定义与原创框架、主题深度论证、案例佐证、观点与倡议、品牌合规审校记录）与选题档案首建；**必须提出原创框架或鲜明主张**（与行业研究的中性全景不同），事实论据仍逐点附来源；运行后回写 `{{REGISTRY_PATH}}`；基线报告**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`。

---

## 一、项目专属硬性约束

1. **观点与事实分离**：观点部分标「本报告观点」；不借白皮书输出投资评级或法律意见（边界归投资尽调型、政策解读型）。
2. **对外发布标准**：须通过品牌与合规审校（审校清单 TODO：业务配置定义）后才可发布；已发布白皮书不得改动，勘误以勘误件形式发布。
3. **受众定位**：（TODO：按业务配置实例化，默认行业公众 / 客户 / 决策者）。

## 二、来源优先级

（TODO：按业务配置实例化）默认层级：① 自有数据 ② 一手访谈 ③ 二手研究（逐点引用）；自有数据与二手数据边界声明须写入报告。

## 三、基线锚定

对比锚属性、选题档案首建等通用差异见[基线类型模板第一节](../../templates/whitepaper/prompt-baseline-setup-template.md)。基线产出后，`{{BASELINE_REPORT_PATH}}` 即指向本报告；节标题为固化锚，正常运行**永不重跑**基线提示词。

## 四、追踪表（选题档案联动）

选题库与准入标准、原创框架登记（名称 / 要素 / 版本）、审校清单、「核心论据 × 来源」追踪表（TODO：业务配置定义逐项）；基线运行后逐项回写 `{{REGISTRY_PATH}}`，未核实项注明「待核实」，prompt 模板内严禁填写活值。

## 五、报告结构骨架

八节固定骨架见[基线类型模板第三节](../../templates/whitepaper/prompt-baseline-setup-template.md)；业务固化锚节标题（TODO：实例化后声明并逐字继承）。

## 六、执行方式（建议）

1. 按论证模块并行启动研究子代理，事实论据逐点引用（TODO：按业务配置调整）。
2. 主代理合并差异；审校清单成稿后集中执行并留痕；无法核实项单列「待复核清单」，重大未决项存在时不发布。

## 七、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`；基线导航采用简化锚点目录。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版首份白皮书提示词 |
