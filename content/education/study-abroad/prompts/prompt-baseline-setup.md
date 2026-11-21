# 14 国留学信息与决策 · 首期基线报告提示词（职业就业调研型）

> **用途**：执行「14 国留学信息与决策持续调研机制」的**机制建立**任务：产出首期基线（深度调研）报告与配套指标登记册，作为后续所有周期更新的对比锚与制度基础。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：中文九节调研报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/2026-11_baseline_report.html`）+ 指标登记册（`data/processed/education/study-abroad/study_abroad_ledger.md`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../engine/templates/monitoring-common-spec.md) × [基线报告类型模板（职业就业调研型）](../../../../engine/templates/employment-research/prompt-baseline-setup-template.md) × [业务专属配置](./business-config.md)。质量规则（中文输出、逐点引用、事实与推断分离、口径标注、来源分级框架、基线锚定、执行方式、质量自检）见通用基座与通用规范；基线差异与九节骨架见基线类型模板；业务变量、来源优先级、受众定位、触发器、已修正事实清单见业务配置；冲突时以本文件为准。

---

## 文档说明与版本标识

| 项 | 内容 |
|---|---|
| 文档名称 | 14 国留学信息与决策 · 首期基线报告提示词 |
| 文档版本 | v1.0 |
| 文档定位 | 本项目**首期基线报告**的结构标准与执行规范 |
| 适用范围 | 本项目机制建立阶段（首期）；后续周期更新引用本基线 |
| 上层依赖 | 通用基座、基线类型模板（employment-research）、监测报告通用规范、业务专属配置 |
| 同层关系 | 与 [月度更新提示词](./prompt-monthly-monitor.md) 互补：本文件管「机制建立」，月度提示词管「周期运行」 |
| 维护责任 | 项目维护者 |
| 冲突优先级 | 本文件 ＞ 业务配置 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范 |

> **固化结论**：本报告九节结构为强制结构（清单见[业务配置第八节](./business-config.md)），顺序、编号、层级不得调整，节标题与已产出基线报告逐字一致。结构变更须走基线类型模板维护规范。

---

## 运行变量（每次运行前填写）

固定值见[业务配置](./business-config.md)第一节；运行时变量：

```
{{CURRENT_DATE}}         = 本次执行日期，格式 YYYY-MM-DD
{{OUTPUT_PATH}}          = reports/2026-11_baseline_report.html
{{REPORT_VERSION}}       = v1.0（首期基线固定）
```

**任务目标**：执行「14 国留学信息与决策持续调研机制」的机制建立任务，产出中文九节基线调研报告与配套指标登记册。报告须覆盖业务配置声明的全部调研维度（覆盖矩阵 14 国 × 学位层级）并给出基线全量读数；运行后从报告提取全部 14 项追踪指标活值回写登记册（每格附 `[来源, 年份]`）。

---

## 一、项目专属硬性约束

通用约束（逐点引用、事实与推断分离、口径标注、数据纪律）自动继承通用基座第三节；来源语言规则、受众定位、术语口径见[业务配置](./business-config.md)第二、三节。本项目额外强制：

1. **来源语言规则**：仅英文（{{SOURCE_LANGUAGE_RULE}}），严禁中文来源；仅中文源数据标注「未找到英文权威来源，已剔除」。
2. **结论边界**：建议章标「建议 / 推断」，不承诺录取结果、不保证签证结果、不构成升学 / 留学 / 认证个案意见。
3. **覆盖完整**：14 国 × 学位层级 29 个组合逐一给 baseline 读数，无数据项标「待核实」并给出复核入口，不得跳过。

## 二、来源优先级

见[业务配置](./business-config.md)第四节（① 各国官方 ＞ ② 多边机构 ＞ ③ 官方统计与认证机构 ＞ ④ 英文行业媒体 ＞ ⑤ 英文大众媒体）。

---

## 三、首期基线锚定（本提示词的特殊定位）

基线报告的对比锚属性、无上期报告、登记册首建等通用差异见[基线类型模板第一节](../../../../engine/templates/employment-research/prompt-baseline-setup-template.md)。本项目实例化：

- 基线报告**无上期报告**：不读取 `{{PREVIOUS_REPORT_PATH}}`；「已修正事实清单」以[业务配置第七节](./business-config.md)为空初始锚，产生修正后逐条补记（每条附 `[Source: URL, 年份]`）。
- **已产出基线的维护**：基线报告产出后即为固化锚，正常运行**永不重跑**基线提示词；本文件仅用于结构重置（如年度复盘重置基线）时参照。

---

## 四、指标追踪表（登记册联动）

追踪表 14 项见[业务配置第六节](./business-config.md)；基线运行后逐项回写 `{{REGISTRY_PATH}}`（md-table 格式），未核实项注明「待核实」，prompt 模板内严禁填写活值。

---

## 五、报告结构骨架

九节固定骨架见[基线类型模板第三节](../../../../engine/templates/employment-research/prompt-baseline-setup-template.md)；本项目节标题固化锚见[业务配置第八节](./business-config.md)。

---

## 六、渲染与交付

- 交付格式见[业务配置第一节](./business-config.md)：md 源稿 + 同目录自包含 HTML（`python engine/tools/md2html.py`）。
- HTML 须通过 `python engine/tools/lint_reports.py` 与 `python engine/tools/page_build_check.py`。
- 导航采用简化锚点目录，不升级为 `.report-nav`。

---

## 七、质量自检

通用自检见[通用基座第九节](../../../../engine/templates/prompt-generic-base.md)与[基线类型模板第六节](../../../../engine/templates/employment-research/prompt-baseline-setup-template.md)。本项目额外确认：

- [ ] 九节齐全、顺序正确；节标题与已产出基线报告逐字一致
- [ ] 全篇零中文来源，URL 均为英文站
- [ ] 14 国 × 学位层级 29 个组合全部覆盖，缺项标「待核实」
- [ ] 追踪表 14 项均已回写登记册；prompt 模板自身无硬编码活值
- [ ] HTML 通过 lint 与 page_build_check

---

## 八、Agent 执行约定

通用约定见[通用基座第八节](../../../../engine/templates/prompt-generic-base.md)。本项目额外：

- 登记载体 `{{REGISTRY_PATH}}` 默认不改写；若需更新，先备份再增量修订，不得覆盖历史值。
- 不得编造任何缺失数据、URL、机构名；不得用中文来源替代英文来源。
- 所有结论可回溯到具体来源行与 URL。

---

## 九、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-21 | 初始版本 | 由 employment-research 泛用版实例化：14 国 × 学位层级矩阵、14 项追踪指标、变量与 TODO 收口到 business-config |
