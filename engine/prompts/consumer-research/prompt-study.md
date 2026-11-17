# {{REGION}} · {{TOPIC}} · 专题调研提示词（消费者·用户调研型 · 泛用版 · 项目制）

> **用途**：项目制专题调研统一入口——概念测试、满意度 / NPS 年度复测、画像刷新、决策路径研究（当次项目主题由 {{STUDY_TYPE}} 指定）。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：单份专题报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`。专题命名不在工具链标准正则内，validate 仅 WARN 不阻断，属预期；年度复测命名与标准正则兼容。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [专题调研类型模板（消费者·用户调研型）](../../templates/consumer-research/prompt-study-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{STUDY_TYPE}}            = 本次专题类型（概念测试 / 满意度复测 / 画像刷新 / 决策路径，TODO：按业务配置枚举）
{{BASELINE_REPORT_PATH}}  = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO）
{{OUTPUT_PATH}}           = 专题件 reports/{{YYYY-MM-DD}}-（TODO：主题）.md；年度复测 reports/{{YYYY}}_annual.md
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：按[专题类型模板](../../templates/consumer-research/prompt-study-template.md)项目协议执行「设计 → 采集 → 分析 → 建议」闭环；方法与口径与基线一致（变更显式声明并保留对照）；样本量不足或差异不显著时结论降级为「方向性发现」并标注；继承已修正事实清单；运行后回写设计档案。

---

## 一、项目协议要点

1. **读取锚**：读取 `{{BASELINE_REPORT_PATH}}` 与上一次同类专题报告（如有），继承细分框架与口径裁决。
2. **显著性纪律**：不夸大差异；纵向复测口径与上年一致。
3. **伦理与隐私**：知情同意、脱敏、不采集可识别个人身份的敏感信息。

## 二、各模块要点（业务实例化，TODO 按 {{STUDY_TYPE}} 展开）

- **概念 / 产品测试**（TODO：概念接受度、购买意向、价格敏感度、竞品对照）。
- **满意度 / NPS 复测**（TODO：口径与上年一致、分项满意度、驱动因素、贬损者归因）。
- **画像刷新**（TODO：细分维度有效性复核、新画像假设、触点迁移）。
- **决策路径**（TODO：触达 → 认知 → 比较 → 转化各环节行为与态度、关键决策因素排序）。

## 三、追踪表（设计档案联动）

运行前从 `{{REGISTRY_PATH}}` 读设计档案（抽样框与配额）→ 执行采集 → 运行后回写（方法版本、样本结构、复测读数）。

## 四、执行方式（建议）

1. 按模块并行启动采集与分析子代理；一手数据逐条附采集渠道与时间。
2. 主代理读取 `{{BASELINE_REPORT_PATH}}` 做口径对齐与差异合并；无法核实项单列「待复核清单」。

## 五、渲染与交付

- 交付包 = 报告 + 数据表附录（脱敏）+ 方法说明；事实发现与建议分离。
- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版专题调研提示词 |
