# 迪拜 AI 网络安全 · 年度复盘提示词（职业就业调研型 · 年度节拍）

> **用途**：周期性（每年固定窗口）执行《迪拜 AI 网络安全行业调研》年度复盘：预测对照、已修正事实清单与待复核清单复审、证书路线图与落地路径重排，产出年度版报告 + 登记册年度新版（另存，不覆盖历史）。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：中文九节年度报告（canonical 富样式自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YEAR}}_annual.html`）+ 登记册年度新版（`{{OUTPUT_REGISTRY}}`）；md 源稿存 `sources/` 同名存档。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（职业就业调研型）](../../../../../engine/templates/employment-research/prompt-update-template.md) × [业务专属配置](./business-config.md)。冲突时以本文件为准。

---

## 运行变量（每次运行前填写）

```
{{CURRENT_DATE}}         = 本次执行日期，格式 YYYY-MM-DD
{{YEAR}}                 = 被复盘的年份（4 位）
{{NEXT_YEAR}}            = 登记册年度新版生效年份（= {{YEAR}} + 1）
{{PREVIOUS_REPORT_PATH}} = 最近一期季度报告路径
{{BASELINE_REPORT_PATH}} = sources/2026-11_baseline_report.md
{{REPORT_VERSION}}       = 本次版本号，格式 vYYYY.MM.DD（写入报告内，不进入文件名）
{{OUTPUT_PATH}}          = reports/{{YEAR}}_annual.html
{{OUTPUT_REGISTRY}}      = data/processed/tech/security/dubai/ai_cybersecurity_indicator_registry_{{NEXT_YEAR}}-01.md
{{REGISTRY_PATH}}        = data/processed/tech/security/dubai/ai_cybersecurity_indicator_registry.md
```

**任务目标**：年度复盘。以最近一期季度报告与基线为对比锚，完成「预测对照 → 清单复审 → 结构性判断重估 → 路线图重排」闭环；九节结构与基线逐字一致；登记册采用增量方式另存年度新版，不覆盖历史值。

---

## 一、年度特有任务（在季度更新协议之上的增量）

1. **预测对照**：对基线与各期报告中标注「预测 / 推断」的结构性判断（需求增速、AI 技能缺口走向、证书溢价、签证政策方向）逐条对照实际发布值，偏离度 =（实际 ÷ 对照）− 1；绝对值 >30% 必须重设假设并列出「重设了哪三项假设」，不做事后拟合。
2. **清单复审**：[业务配置第七节](./business-config.md)已修正事实清单逐条复核来源是否仍成立；待复核清单逐项给出去年建议复核入口的核验结果；新修正逐条追加（每条附 `[Source: URL, 年份]`）。
3. **路线图重排**：第 6 节证书路线图按新发证书、考试费变化、本地考点日程重排；第 7 节落地路径按最新签证规则重排。
4. **登记册年度版**：复制 `{{REGISTRY_PATH}}` → `{{OUTPUT_REGISTRY}}`，逐项更新「当前值」与「最近核实」；年度版成为下一年 `{{REGISTRY_PATH}}` 的事实来源（业务配置第一节同步改指向）。

## 二、更新协议与结构

更新协议（读取锚、来源优先级、追踪表闭环、数据变更摘要）见[季度更新提示词](./prompt-quarterly-analysis.md)第三、五节与[周期类型模板](../../../../../engine/templates/employment-research/prompt-update-template.md)第二节；九节骨架与业务实例化模块要点沿用[季度更新提示词](./prompt-quarterly-analysis.md)第四节，年度版须额外呈现「预测对照表」与「清单复审结果」。

## 三、输出格式要求

- 中文报告，九节结构与基线逐字一致；版本号写入报告文首/文末；文末标注年度版数据基准；。
- 产出后执行 `python engine/tools/lint_reports.py` 验证。

## 四、质量自检

通用自检见[通用基座第九节](../../../../../engine/templates/prompt-generic-base.md)与[周期类型模板第六节](../../../../../engine/templates/employment-research/prompt-update-template.md)。本项目额外确认：

- [ ] 预测对照表齐全，偏离度 >30% 的判断已重设假设
- [ ] 已修正事实清单与待复核清单完成年度复审并留痕
- [ ] 登记册年度版已另存（不覆盖历史），业务配置指向已同步
- [ ] 九节结构与基线逐字一致；追踪表 14 项已核对回写
- [ ] HTML 通过 lint

## 五、Agent 执行约定

同[季度更新提示词](./prompt-quarterly-analysis.md)第九节；登记册年度版采用「复制 → 修订 → 另存」增量方式，严禁覆盖历史值。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 按employment-research类型三档节拍设计建立，年度档定位复盘（预测对照 + 清单复审 + 路线图重排 + 登记册年度版） |
