# 迪拜 AI 网络安全 · 月度核验提示词（职业就业调研型 · 核验轻运行）

> **用途**：月度窗口的**核验型轻运行**：核验登记册活值与触发器状态。**无触发不启动新报告**——仅在登记册标注「截至 {{CURRENT_DATE}} 无更新」；命中任一触发器（见[业务配置第五节](./business-config.md)）时升级为季度重点更新（走 [季度更新提示词](./prompt-quarterly-analysis.md)）。
> **产出**：登记册核对记录（不产出新报告文件）；如触发升级则按季度提示词产出 `reports/{{YYYY-Qn}}_quarterly.html`。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（职业就业调研型）](../../../../../../engine/templates/employment-research/prompt-update-template.md) × [业务专属配置](./business-config.md)。冲突时以本文件为准。

<!-- report-output: none -->

---

## 运行变量（每次运行前填写）

```
{{CURRENT_DATE}}         = 本次执行日期，格式 YYYY-MM-DD
{{REGISTRY_PATH}}        = data/processed/tech/ai-security/security/dubai/ai_cybersecurity_indicator_registry.md
{{BASELINE_REPORT_PATH}} = sources/2026-11_baseline_report.md
```

**任务目标**：逐项核对登记册 14 项指标（清单见[业务配置第六节](./business-config.md)）的官方页面是否更新；核对七条触发器是否命中。全部未变动 → 登记册标注「截至 {{CURRENT_DATE}} 无更新」并结束；任一变动/命中 → 更新登记册对应项（附 `[来源, 年份]`）并触发季度重点更新。

## 执行步骤

1. **读取锚**：读取 `{{REGISTRY_PATH}}` 与 `{{BASELINE_REPORT_PATH}}`（继承已修正事实清单，见[业务配置第七节](./business-config.md)，严禁回退）。
2. **核验**：按 14 项追踪表逐项访问优先数据源；来源语言规则仅英文（{{SOURCE_LANGUAGE_RULE}}）。
3. **回写**：变动项更新「当前值」与「最近核实」；未变动项注明「截至 {{CURRENT_DATE}} 无更新」。不得为制造变化而虚构变化。
4. **判定**：对照[业务配置第五节](./business-config.md)触发器表；命中即升级季度更新。

## 质量自检

- [ ] 登记册 14 项逐项核对并留痕
- [ ] 已修正事实清单无回退
- [ ] prompt 模板无硬编码活值
- [ ] 未启动不必要的报告产出

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 按employment-research类型三档节拍设计建立，月度档定位核验轻运行 |
