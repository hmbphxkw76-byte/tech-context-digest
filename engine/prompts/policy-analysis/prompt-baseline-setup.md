# {{REGION}} · {{TOPIC}} · 首期基线报告提示词（政策法规解读型 · 泛用版）

> **用途**：执行「{{REGION}} {{TOPIC}} 政策解读机制」的**机制建立**任务：产出首期监管框架基线报告与配套政策台账。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文九节基线报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_baseline_report.md`）+ 政策台账（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [基线报告类型模板（政策法规解读型）](../../templates/policy-analysis/prompt-baseline-setup-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，实例化时写入 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{BASELINE_DATE}}         = 首期基线日期
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO：政策台账文件名）
{{REGISTRY_FORMAT}}       = md-table（TODO：按业务配置）
{{SOURCE_LANGUAGE_RULE}}  = 仅英文（默认；中国宏观例外见 engine/docs/source-language-policy.md）
{{REPORT_VERSION}}        = v1.0（首期基线固定）
```

**任务目标**：产出九节监管框架基线报告（框架地图、重点政策逐条解读、影响对象矩阵、合规应对建议、生效时间线）与政策台账首建；**官方原文铁律**：全部引用回溯官方公报 / 法规数据库原文并附 URL，媒体转述仅作线索；运行后回写 `{{REGISTRY_PATH}}`；基线报告**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`。

---

## 一、项目专属硬性约束

1. **只盯官方文本**：不采集舆论反应（边界归舆情监测型）；原文有歧义处并列多解，不静默择一。
2. **结论边界**：不构成法律意见；合规应对建议标「建议」；重大合规决策提示咨询执业法律专业人士。
3. **受众定位**：（TODO：按业务配置实例化，默认合规团队 / 政府事务 / 受影响企业与个人）。

## 二、来源优先级

（TODO：按业务配置实例化渠道清单）默认层级：① 官方公报 / 法规数据库（唯一采信层） ② 立法记录 ③ 媒体转述仅作线索；每格活值附 `[官方原文 URL, 版本日期]`。

## 三、基线锚定

对比锚属性、政策台账首建等通用差异见[基线类型模板第一节](../../templates/policy-analysis/prompt-baseline-setup-template.md)。基线产出后，`{{BASELINE_REPORT_PATH}}` 即指向本报告；节标题为固化锚，正常运行**永不重跑**基线提示词。

## 四、追踪表（政策台账联动）

监测法规清单（名称 / 发布机构 / 发布与生效日期 / 状态）、官方发布渠道清单（逐渠道 URL 与更新机制）、影响对象矩阵（TODO：业务配置定义逐项）；基线运行后逐项回写 `{{REGISTRY_PATH}}`，prompt 模板内严禁填写活值。

## 五、报告结构骨架

九节固定骨架见[基线类型模板第三节](../../templates/policy-analysis/prompt-baseline-setup-template.md)；业务固化锚节标题（TODO：实例化后声明并逐字继承）。

## 六、执行方式（建议）

1. 原文回溯先行：逐渠道核对官方原文，完成台账登记后才进入解读环节（TODO：按业务配置调整）。
2. 解读逐条附条款定位；新旧制度冲突并列对照；无法核实项单列「待复核清单」。

## 七、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`；基线导航采用简化锚点目录。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版基线提示词 |
