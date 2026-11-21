# 迪拜 AI 应用就业 · 月度更新提示词（职业就业调研型 · 主更新节拍）

> **用途**：周期性（每月）刷新《迪拜 AI 应用就业行业调研报告》，动态获取英文权威数据；重大事件触发器命中时亦走本提示词做对应模块重点更新。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：中文九节调研报告（canonical 富样式自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_monthly.html`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（职业就业调研型）](../../../../../engine/templates/employment-research/prompt-update-template.md) × [业务专属配置](./business-config.md)。质量规则见通用基座与通用规范；更新协议、模块更新要点框架见周期类型模板；业务变量、来源优先级、触发器、已修正事实清单、九节固化锚见业务配置；冲突时以本文件为准。

---

## 运行变量（每次运行前填写）

```
{{CURRENT_DATE}}         = 本次执行日期，格式 YYYY-MM-DD
{{PREVIOUS_REPORT_PATH}} = 最近一期月度报告路径（首期更新时为空，仅锚定基线）
{{BASELINE_REPORT_PATH}} = reports/2026-11_baseline_report.html
{{REPORT_VERSION}}       = 本次版本号，格式 vYYYY.MM.DD（写入报告文首/文末，不进入文件名）
{{OUTPUT_PATH}}          = reports/{{YYYY-MM}}_monthly.html
{{REGISTRY_PATH}}        = data/processed/tech/ai-application/dubai/ai_application_employment_indicator_registry.md
```

**任务目标**：执行「迪拜 AI 应用就业行业调研」的月度更新任务。以英文一手/权威来源为依据、以上一期报告与首期基线为对比锚，完成「核验 → 更新 → 落地建议 → 可靠性」闭环；九节结构与基线逐字一致（见[业务配置第八节](./business-config.md)），继承已修正事实清单，产出可直接用于下期对比的报告。

---

## 一、项目专属硬性约束

通用约束自动继承[通用基座第三节](../../../../../engine/templates/prompt-generic-base.md)；来源语言规则、受众定位、术语口径见[业务配置](./business-config.md)第二、三节。本项目额外强制：

1. **来源语言规则**：仅英文（{{SOURCE_LANGUAGE_RULE}}），严禁中文来源；仅中文源数据标注「未找到英文权威来源，已剔除」。
2. **结论边界**：建议章标「建议 / 推断」，不承诺就业结果、不保证薪资水平。
3. **岗位边界**：只监测 AI 应用岗位，不混入 AI 安全攻防岗位。

## 二、来源优先级

见[业务配置](./business-config.md)第四节（① 政府官方 ＞ ② 国际权威组织 / 平台数据 ＞ ③ 薪酬指南 ＞ ④ 招聘平台抽样 ＞ ⑤ 英文媒体）；薪酬指南至少抓取 3 家独立来源交叉验证。

## 三、基线锚定与已修正事实清单

更新协议见[周期类型模板第二节](../../../../../engine/templates/employment-research/prompt-update-template.md)。更新时必须**读取 `{{PREVIOUS_REPORT_PATH}}`**（首期更新除外）与 `{{BASELINE_REPORT_PATH}}`，继承九节结构与全部已核实结论，严禁重新引入[业务配置第七节](./business-config.md)五条已修正事实（产生新修正后逐条追加，每条附 `[Source: URL, 年份]`）。

## 四、各模块更新要点（业务实例化，对应九节）

**第 2 节 · 行业与政策发展趋势**
- Dubai Universal Blueprint for AI 实施进展（Dubai AI Seal、Chief AI Officers、DCAI、Dubai AI Campus、Dubai AI Week）；UAE AI Strategy 2031 进展；Digital Dubai AI Lab 新动态。
- 动态获取：IMARC / 其他权威机构 UAE AI 市场规模与 CAGR（口径并列）；LinkedIn 招聘率、AI 工程岗需求与人才集中度；DIFC Innovation Hub / 自由区企业数。
- 双城对比：迪拜 vs 阿布扎比政策与生态差异（DCAI / G42 系 / DIFC / D33）。

**第 3 节 · 人才供需与薪酬（最高优先级）**
- LinkedIn 最新 UAE 劳动力报告（招聘率、AI 工程岗需求、AI 素养人才、国际申请占比）；ISC2 等技能缺口研究；Michael Page / Hays / Cooper Fitch / Charterhouse 最新年版 AI/Data 分表。
- 薪酬交叉验证：至少 3 家薪酬指南最新年版 + 招聘平台抽样；保持「岗位 × 职级」交叉分层表（AED/月 + USD 换算，1 USD = 3.6725 AED）。
- 保持：净薪模型（0% 个税、外籍 0% 社保、ILOE 唯一扣减）、总包模型、迪拜 vs 阿布扎比生活成本（Numbeo）、阿化配额与罚则。

**第 4 节 · 企业类型细分**
- 核实并更新：G42 / Core42 / e& / Dubai AI Campus / DIFC Innovation Hub / DCAI 最新动态；Careem / Talabat / noon 等本地平台经济 AI 岗位信号；未能核实的实体单列并给复核入口。

**第 5 节 · 岗位技能要求**
- 在招 AI 应用岗抽样（约 20–30 条，LinkedIn / Bayt / GulfTalent / foundit Gulf / 企业官网），更新分岗位要求表；保持工具栈与语言要求；跟踪 Agentic AI / RAG / MLOps / AI 治理技能演进。

**第 6 节 · 职业证书**
- 新发 AI 应用 / 数据 / 云认证（Microsoft / Google / AWS / Databricks / DASCA / ISO 42001 等）考试费、prerequisites、阿联酋市场认可证据；证书路线图与本地考点更新。

**第 7 节 · 就业落地建议**
- 黄金签证最新门槛（基本工资阈值、优先领域）；标准就业签证 / 自由区（DIFC / ADGM / IFZA）流程与费用；阿化配额；招聘机构评级复核；GITEX / Expand North Star / Dubai AI Week 档期。

## 五、指标追踪表（每次运行逐项核对回写）

14 项追踪表见[业务配置第六节](./business-config.md)；运行前从 `{{REGISTRY_PATH}}` 读「上次值」、运行后回写，逐项填写「是否更新」，未变动项注明「截至 {{CURRENT_DATE}} 无更新」。数据变更摘要至少覆盖 14 项，置于第 9 节之前。

## 六、执行方式（建议）

1. 启动 4–6 个并行研究子代理：① 市场政策 + 企业生态；② 人才供需 + 薪酬交叉验证 + 净薪/总包模型；③ 岗位技能 + AI 应用技术深度；④ 证书路线 + 本地考点；⑤ 落地签证 + 求职手册。全部限定英文源、逐点引用。
2. 子代理返回后由主代理读取 `{{PREVIOUS_REPORT_PATH}}` 与基线做差异合并，继承已修正事实、应用第四节更新要点。
3. 冲突数据保留双份引用；无法核实项单列「待复核清单」。
4. 产出后执行 `python engine/tools/lint_reports.py` 与 `python engine/tools/page_build_check.py` 验证。

## 七、输出格式要求

- 中文报告，九节结构与基线逐字一致；引用与版本规则遵循通用规范；版本号 `{{REPORT_VERSION}}` 写入报告文首/文末。
- 文末标注：`本报告为 {{REPORT_VERSION}} 动态更新版，数据基准 {{CURRENT_DATE}}，来源要求见项目提示词。`

## 八、质量自检

通用自检见[通用基座第九节](../../../../../engine/templates/prompt-generic-base.md)与[周期类型模板第六节](../../../../../engine/templates/employment-research/prompt-update-template.md)。本项目额外确认：

- [ ] 九节结构与基线逐字一致，无增删节
- [ ] 全篇零中文来源，URL 均为英文站
- [ ] 已继承五条已修正事实，无回退
- [ ] 薪资表保留「岗位 × 职级」交叉分层 + USD 换算；净薪 / 总包模型保留；未核实项标「待核实」
- [ ] 追踪表 14 项均已核对并回写登记册；prompt 模板无硬编码活值
- [ ] 已产出数据变更摘要与待复核清单
- [ ] HTML 通过 lint 与 page_build_check

## 九、Agent 执行约定

通用约定见[通用基座第八节](../../../../../engine/templates/prompt-generic-base.md)。本项目额外：

- 登记载体 `{{REGISTRY_PATH}}` 默认不改写；若需更新，先备份再增量修订，不得覆盖历史值。
- 不修改用户上传的只读附件；如需引用，先复制到可编辑目录。
- 不得编造任何缺失数据；不得用中文来源替代英文来源；所有结论可回溯到具体来源行与 URL。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-21 | 初始版本 | 新建业务线月度提示词：继承声明指向 employment-research 周期类型模板；节映射到基线九节固化锚；更新要点按 AI 应用岗位域实例化 |
