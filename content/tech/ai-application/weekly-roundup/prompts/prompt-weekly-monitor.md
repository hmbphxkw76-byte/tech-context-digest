# AI 应用趋势周报（大模型 · Agent · 编码 · 商业化）· 周报提示词（行业趋势周报型）

> **用途**：周期性（每周）刷新三大主题板块与数据看板，产出周报；触发器命中时对应板块重点更新。
> **产出**：自包含 HTML 周报，落盘 `{{OUTPUT_PATH}}`（`reports/{{DATA_CUTOFF}}_weekly.html`，日期 = 数据截止日）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（行业趋势周报型）](../../../../../engine/templates/trend-weekly/prompt-weekly-monitor-template.md) × [业务专属配置](./business-config.md)。冲突时以本文件为准。
>
> **过程来源**：通用执行步骤、渲染交付与结果验证以 [通用泛用版周报提示词](../../../../../engine/prompts/trend-weekly/prompt-weekly-monitor.md) 与 [通用运维手册](../../../../../engine/templates/trend-weekly/operations-guide.md) 为准；本文件只承载业务实例化差异，不复制通用过程。

---

## 运行变量（每次运行前填写）

```
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{DATA_CUTOFF}}           = 数据截止日（周报命名与标题锚定此日期，非执行日）
{{PREVIOUS_REPORT_PATH}}  = reports/ 中最近一期周报（首期为空，仅锚定首期周报）
{{BASELINE_REPORT_PATH}}  = sources/legacy/2026-11-13_weekly.html（原合并首期，应用侧结构锚；固定值，见 business-config.md）
{{REGISTRY_PATH}}         = data/processed/tech/ai-application/weekly-roundup/ai_application_trend_ledger.md（业务配置固定值）
{{OUTPUT_PATH}}           = reports/{{DATA_CUTOFF}}_weekly.html
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

其余固定值（`{{REGION}}` / `{{TOPIC}}` / `{{CADENCE}}` / `{{REPO_RAW_URL_BASE}}` / `{{FRESHNESS_PRIORITY}}` / `{{SOURCE_LANGUAGE_RULE}}`）读自 business-config.md 第一节。

**任务目标**：以公开来源为依据、以上期周报为对比锚，完成「采集 → 核验 → 看板刷新 → 可执行启示」闭环；结构对齐原合并首期应用侧板块；继承已修正事实清单；无实质变化时降级为核验轻运行（台账标注「截至 {{CURRENT_DATE}} 无更新」），不得虚构变化；与上期数据截止日仅隔 1 日时在报告头部标注「T+1 刷新」。

---

## 一、节拍与触发

周节拍 + 事件触发升级设计见[周期类型模板第一节](../../../../../engine/templates/trend-weekly/prompt-weekly-monitor-template.md)；触发器清单见 business-config 第五节，命中即当期核实并升级对应板块，不等待下周窗口。

## 二、业务硬性约束

1. **事实与推断分离**：【事实】/【预测】（带来源与置信度）/「推断」显式标注；媒体转述标「需核实原文」并回官方页校验。
2. **口径纪律**：同一指标多口径并列，不平均、不静默择一；跨机构数字不可相加。
3. **反方证据**：对核心结论的公开质疑必须收录进「风险与不确定性」。
4. **结论边界**：可执行启示标「推断」，只给「条件 → 判读 → 框架性含义 → 风险提示」；不给选型背书与仓位建议。
5. **范围边界**：只覆盖 AI 应用侧三板块；AI 安全与红队、基准与评估可信度归 `content/tech/ai-security/weekly-roundup`，不重复跟踪。

## 三、报告固定结构（8 节，不得增删节、调整顺序）

1. **本周要点 Top5**：每条 = 结论一句话 + 关键数字 + 来源；【事实】/【预测】标注。
2. **大模型与 Agent 技术演进**：新模型与基准 / Agent 架构与协议 / 成本与效率（business-config 主题矩阵 s2）。
3. **AI 编码与开发工具**：AI IDE / 编码 Agent 与 CLI / 编码基准与工作流（s3）。
4. **AI 应用与商业化**：采用与支出 / 定价与商业模式 / 垂直与区域 / 融资并购（s4）。
5. **数据看板表格**：指标 × 上期值 × 本期值 × 变化 × 来源 × 口径，逐行与台账联动。
6. **风险与不确定性**：来源可靠性 / 反向证据 / 口径冲突 / 基准自报。
7. **可执行启示**：面向 Agent Dev / 应用工程，标「推断」。
8. **参考来源**：逐条 URL；转述标「需核实原文」。

## 四、执行步骤

按 [通用泛用版周报提示词第四节](../../../../../engine/prompts/trend-weekly/prompt-weekly-monitor.md)执行；采集来源按 business-config 第四节机构清单，建议按渠道并行研究子代理，逐点引用 URL。

## 五、渲染与交付

- 纯 HTML 交付（business-config 第六节声明）；md 源稿同步存 `sources/{{DATA_CUTOFF}}_weekly.md`，不参与 md2html 自动转换。
- 命名遵循仓库统一约定；周报按归档保留策略执行（weekly 12 期）。

## 六、结果验证

```powershell
python engine/tools/validate.py                    # 0 错误
python engine/tools/lint_reports.py                # 0 错误
python engine/tools/compliance_check.py --file content/tech/ai-application/weekly-roundup/reports/<本期文件名>.html
python engine/tools/build_index.py && python engine/tools/build_hub.py
```

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-20 | 初始版本 | 由 `content/tech/weekly-roundup` 拆分：AI 应用侧三板块（s2–s4）、8 节骨架；通用过程引用类型通用层 |
