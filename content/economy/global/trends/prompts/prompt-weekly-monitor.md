# 经济趋势周报 · 周报提示词（行业趋势周报型）

> **用途**：周期性（每周）刷新三大主题板块与数据看板，产出八节周报；触发器命中时对应板块重点更新。
> **产出**：自包含 HTML 周报，落盘 `{{OUTPUT_PATH}}`（`reports/{{DATA_CUTOFF}}_weekly.html`，日期 = 数据截止日）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（行业趋势周报型）](../../../../../engine/templates/trend-weekly/prompt-weekly-monitor-template.md) × [业务专属配置](./business-config.md)。冲突时以本文件为准。

---

## 运行变量（每次运行前填写）

```
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{DATA_CUTOFF}}           = 数据截止日（周报命名与标题锚定此日期，非执行日）
{{PREVIOUS_REPORT_PATH}}  = reports/ 中最近一期周报（首期为空，仅锚定首期周报）
{{BASELINE_REPORT_PATH}}  = reports/ 首期周报（结构与结论锚；首期运行后回填实际文件名，见 business-config.md）
{{REGISTRY_PATH}}         = data/processed/economy/global/trends/economy_trend_ledger.md（业务配置固定值）
{{OUTPUT_PATH}}           = reports/{{DATA_CUTOFF}}_weekly.html
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

其余固定值（`{{REGION}}` / `{{TOPIC}}` / `{{CADENCE}}` / `{{REPO_RAW_URL_BASE}}` / `{{FRESHNESS_PRIORITY}}` / `{{SOURCE_LANGUAGE_RULE}}`）读自 business-config.md 第一节。

**任务目标**：以公开来源为依据、以上期周报为对比锚，完成「采集 → 核验 → 看板刷新 → 可执行启示」闭环；八节结构与首期周报逐字一致；继承已修正事实清单；无实质变化时降级为核验轻运行（台账标注「截至 {{CURRENT_DATE}} 无更新」），不得虚构变化；与上期数据截止日仅隔 1 日时在报告头部标注「T+1 刷新」。

---

## 一、节拍与触发

周节拍 + 事件触发升级设计见[周期类型模板第一节](../../../../../engine/templates/trend-weekly/prompt-weekly-monitor-template.md)；触发器清单见业务配置第五节，命中即当期核实并升级对应板块，不等待下周窗口。

## 二、业务硬性约束

1. **事实与推断分离**：【事实】/【预测】（带来源与置信度）/「推断」显式标注；媒体转述标「需核实原文」并回官方页校验。
2. **口径纪律**：同一指标多口径并列（名义 GDP 与 PPP 口径、Headline 与核心通胀等），不平均、不静默择一；跨机构数字不可相加；「全球主要经济体」范围口径须逐处注明（G20 / IMF WEO 等）。
3. **反方证据**：对核心结论的公开质疑必须收录进「风险与不确定性」。
4. **结论边界**：可执行启示标「推断」，只给「条件 → 判读 → 框架性含义 → 风险提示」；不给汇率点位与仓位建议；来源语言规则与全篇来源边界见业务配置第一、四节。

## 三、八节固定结构（不得增删节、调整顺序）

1. **本周要点 Top5**：每条 = 结论一句话 + 关键数字 + 来源；【事实】/【预测】标注。
2. **主要经济体宏观基本面**：GDP / 通胀 / 就业 / 货币政策与财政动态（业务配置主题矩阵 s2）。
3. **贸易、供应链与产业政策**：关税与协定 / 补贴与产业政策 / 供应链重构（s3）。
4. **新兴市场与大宗商品**：新兴与资源型经济体动态 / 能源与大宗商品价格影响（s4）。
5. **数据看板表格**：指标 × 上期值 × 本期值 × 变化 × 来源 × 口径，逐行与台账联动。
6. **风险与不确定性**：来源可靠性 / 反向证据 / 口径冲突 / 预测分歧。
7. **对 Macro Research 的可执行启示**：面向受众，标「推断」，条件 → 判读 → 框架性含义 → 风险提示。
8. **参考来源**：逐条 URL；转述标「需核实原文」。

## 四、执行步骤

1. 填变量 → 读 `{{PREVIOUS_REPORT_PATH}}` 与 `{{BASELINE_REPORT_PATH}}`（首期周报，结构与结论锚），提取台账「已修正事实清单」全部条目（防回退）。
2. 按来源分级采集本周新事实（业务配置第四节机构清单；建议按渠道并行研究子代理，逐点引用 URL）。
3. 逐块更新主题板块；数据看板逐行核对并回写台账（逐项填「是否更新」，未变动项注明「截至 {{CURRENT_DATE}} 无更新」）。
4. 撰写八节周报（顶部导航锚点与节标题逐字一致；表格 `class="fixed"` + 百分比列宽），落盘 `{{OUTPUT_PATH}}`。

## 五、渲染与交付

- 纯 HTML 交付（业务配置第六节声明）；md 源稿同步存 `sources/{{DATA_CUTOFF}}_weekly.md`，不参与 md2html 自动转换。
- 命名遵循仓库统一约定；周报按归档保留策略执行（weekly 12 期）。

## 六、结果验证

```powershell
python engine/tools/validate.py                    # 0 错误
python engine/tools/lint_reports.py                # 0 错误
python engine/tools/compliance_check.py --file content/economy/global/trends/{{OUTPUT_PATH 文件名}}
python engine/tools/build_index.py && python engine/tools/build_hub.py
```

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 按 trend-weekly 类型模板实例化业务周报提示词（八节骨架对齐业务配置主题矩阵） |
