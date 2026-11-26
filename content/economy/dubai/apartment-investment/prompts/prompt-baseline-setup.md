# 迪拜（阿联酋） · 公寓住宅市场投资分析 · 首次覆盖提示词（投资分析与尽调型）

> **用途**：执行「迪拜公寓住宅市场投资分析机制」的**机制建立**任务：产出首期标的覆盖报告（首次覆盖）与配套标的档案。建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文八节覆盖报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/2026-11_baseline_report.md` → `reports/2026-11_baseline_report.html`）+ 标的档案（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [基线报告类型模板（投资分析与尽调型）](../../../../../engine/templates/investment-research/prompt-baseline-setup-template.md) × [业务专属配置](./business-config.md)。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 迪拜（阿联酋） / 公寓住宅市场投资分析（见 business-config 第一节）
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{BASELINE_DATE}}         = 2026-11-26
{{OUTPUT_PATH}}           = reports/2026-11_baseline_report.md（HTML 由 md2html.py 同步生成）
{{REGISTRY_PATH}}         = data/processed/economy/dubai/apartment-investment/dubai_apartment_investment_registry.md
{{REGISTRY_FORMAT}}       = md-table
{{SOURCE_LANGUAGE_RULE}}  = 仅英文（默认；中国宏观例外见 engine/docs/source-language-policy.md）
{{REPORT_VERSION}}        = v1.0（首期基线固定）
```

**任务目标**：产出八节首次覆盖报告（投资要点、标的概况、行业与市场输入、财务分析与估值模型、风险清单、情景与敏感性、合规与边界）与标的档案首建；**结论必须明确**（评级 / 建议 / 估值区间）且与完整风险清单并存；运行后回写 `{{REGISTRY_PATH}}`；基线报告**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`。

---

## 一、项目专属硬性约束

1. **结论边界**：报告声明「不构成对不特定公众的投资邀约」，仅服务授权决策方；重大未决事项存在时结论降级为「有条件结论」并披露；遵守通用基座第三节第 5 条（不给具体买卖价位、杠杆比例、仓位建议）。
2. **估值纪律**：估值模型全假设可审计；估值区间多方法并列；情景为三档（乐观 / 基准 / 悲观）；自算值标「假设乘积」并区间化。
3. **合规**：信息来源合法性声明、利益冲突声明；非公开信息使用逐处标注授权依据（本项目仅使用公开资料，非公开信息不使用）。
4. **受众定位**：拟赴迪拜置业 / 持有公寓资产的投资者（详见 business-config 第二节）。

## 二、来源优先级

见 [business-config 第四节](./business-config.md)（① 官方一手 ＞ ② 行业机构 ＞ ③ 挂牌门户 ＞ ④ 媒体转述；P0–P5 估值输入选择）。事件核实以官方披露原文为准，媒体转述仅作线索。

## 三、基线锚定

对比锚属性、标的档案首建等通用差异见 [基线类型模板第一节](../../../../../engine/templates/investment-research/prompt-baseline-setup-template.md)。基线产出后，`{{BASELINE_REPORT_PATH}}` 即指向本报告；节标题为固化锚，正常运行**永不重跑**基线提示词。

## 四、追踪表（标的档案联动）

标的监测项、估值假设、风险登记定义见 [business-config 第五 / 六节](./business-config.md)（I01–I08 + K/RL/G 指针）；基线运行后逐项回写 `{{REGISTRY_PATH}}`，每格活值附 `[来源, 时点]`，prompt 模板内严禁填写活值。

## 五、报告结构骨架

八节固定骨架见 [基线类型模板第三节](../../../../../engine/templates/investment-research/prompt-baseline-setup-template.md)；业务固化锚节标题见 [business-config 第八节](./business-config.md)，逐字继承。

## 六、执行方式（建议）

1. 财务与估值模块并行启动子代理；估值假设逐条审计。
2. 主代理合并差异；重大未决事项显式披露；无法核实项单列「待复核清单」。

## 七、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`；基线导航采用简化锚点目录。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版首次覆盖提示词 |
| v1.1 | 2026-11-26 | 业务线实例化 | 复制至 content/economy/dubai/apartment-investment/prompts/，替换运行变量、来源优先级、追踪表与八节固化锚（指向 business-config） |
