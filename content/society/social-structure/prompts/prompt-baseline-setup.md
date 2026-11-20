# 全球 · 社会结构与分层 · 首期基线报告提示词（政策法规解读型 · social-structure）

> **用途**：执行「全球 社会结构与分层 政策解读机制」的**机制建立**任务：产出首期社会结构基线报告与配套社会台账。
> **产出**：中文九节基线报告（md 源稿 + 同目录自包含 HTML），落盘 `reports/{{YYYY-MM}}_baseline_report.html` + 台账（`data/processed/society/social-structure/social_structure_ledger.md`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../engine/templates/monitoring-common-spec.md) × [基线报告类型模板（政策法规解读型）](../../../../engine/templates/policy-analysis/prompt-baseline-setup-template.md) × [业务专属配置](./business-config.md)。冲突时以本文件 ＞ business-config ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 全球 / 社会结构与分层（固定值，见 business-config 第一节）
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{BASELINE_DATE}}         = 首期基线日期
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_baseline_report.html
{{REGISTRY_PATH}}         = data/processed/society/social-structure/social_structure_ledger.md
{{REGISTRY_FORMAT}}       = md-ledger
{{SOURCE_REGISTRY_PATH}}  = data/processed/society/social-structure/source_registry.json
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPORT_VERSION}}        = v1.0（首期基线固定）
```

**任务目标**：产出九节社会结构基线报告（结构地图、重点群体与分层逐条解读、影响对象矩阵、应对建议、时间线）与台账首建；**官方原文铁律**：全部引用回溯官方统计 / 调查微观数据并附 URL，媒体转述仅作线索；运行后回写 `{{REGISTRY_PATH}}`；基线报告**无上期报告**。

业务参数（受众、术语口径、来源分级、K/RL/G 阈值、触发器、渲染差异、信息分层）**一律以 [business-config.md](./business-config.md) 为准**，本文件不复制。

---

## 一、项目专属硬性约束

1. **只盯官方统计与政策文本**：不采集舆论反应；口径有歧义处并列多解，不静默择一。
2. **结论边界**：不构成心理、法律、医疗个案意见；不外推个体行为。
3. **受众定位**：社会政策研究者、人口与劳动统计分析者、公共服务与福利机构（详见 business-config 第二节）。

## 二、来源优先级

按 [business-config 第四节](./business-config.md) 的四层分级与 P0–P5 获取优先级执行；每格活值附 `[官方原文 URL, 版本日期]`。

## 三、基线锚定

对比锚属性、台账首建等通用差异见 [基线类型模板第一节](../../../../engine/templates/policy-analysis/prompt-baseline-setup-template.md)。基线产出后，`{{BASELINE_REPORT_PATH}}` 即指向本报告；正常运行**永不重跑**基线提示词。

## 四、追踪表（台账联动）

人口与家庭、收入与分配、就业、社会保障、城镇化清单按 [business-config 第十节](./business-config.md)（G01–G05）与第九节专题配置定义；基线运行后逐项回写 `{{REGISTRY_PATH}}`，本提示词内严禁填写活值。

## 五、报告结构骨架

九节固定骨架见 [基线类型模板第三节](../../../../engine/templates/policy-analysis/prompt-baseline-setup-template.md)；业务固化锚节标题见 business-config 第十二节。

## 六、执行方式（建议）

1. 原文回溯先行：逐渠道核对官方统计与方法文件，完成台账登记后才进入解读环节。
2. 解读逐条附口径与表号；不同口径并列对照；无法核实项单列「待复核清单」。

## 七、渲染与交付

- 交付格式：md 源稿 + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`。
- 渲染差异实例化见 [business-config 第十二节](./business-config.md)。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-18 | 初始版本 | 四主题接入就绪化（P1-9）：由 policy-analysis 泛用版实例化，变量与 TODO 收口到 business-config |
