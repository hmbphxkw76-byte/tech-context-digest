# {{REGION}} · {{TOPIC}} · 月度监测提示词（政策法规解读型 · 泛用版）

> **用途**：执行政策法规解读型业务线的**月度监测**任务：以基线与上期台账为对比锚，逐月检测政策变更、回溯官方原文、增量解读并回写台账。泛用版业务提示词：建新业务线时复制本文件至业务线 `prompts/`，替换变量与 TODO 后即可运行。
> **产出**：中文九节月度报告（md 源稿 + 同目录自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_monthly.md`）+ 政策台账增量（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [月度监测类型模板（政策法规解读型）](../../templates/policy-analysis/prompt-monthly-monitor-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，实例化时写入 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{OUTPUT_PATH}}           = reports/{{YYYY-MM}}_monthly.md
{{BASELINE_REPORT_PATH}}  = sources/{{YYYY-MM}}_baseline_report.md
{{PREVIOUS_REPORT_PATH}}  = sources/{{上一期}}_monthly.md（如有）
{{REGISTRY_PATH}}         = data/（TODO：政策台账文件名）
{{REGISTRY_FORMAT}}       = md-table（TODO：按业务配置）
{{SOURCE_LANGUAGE_RULE}}  = 仅英文（默认；中国宏观例外见 engine/docs/source-language-policy.md）
{{REPORT_VERSION}}        = vYYYY.MM.DD（写入报告内，不进文件名）
```

**任务目标**：产出九节月度监测报告；**变更检测先行**，仅对有变更的政策 / 通道展开解读，无变更项标注「截至本期无更新」；**官方原文铁律**：变更条目回溯官方公报 / 法规数据库原文并附 URL，媒体转述仅作线索；运行后回写 `{{REGISTRY_PATH}}`。

---

## 一、项目专属硬性约束

1. **只盯官方文本**：不采集舆论反应（边界归舆情监测型）；原文有歧义处并列多解，不静默择一。
2. **结论边界**：不构成法律意见；合规应对建议标「建议」；重大合规决策提示咨询执业法律专业人士。
3. **无变更不展开**：无触发时仅在台账标注，不重新解读、不堆砌旧结论。

## 二、变更检测（TODO：按业务配置实例化）

逐主体检测本期是否有：通道新增 / 关闭 / 改名；薪资门槛与配额调整；职业清单调整；积分 / 抽签规则变化；永居 / 居住年限变化；定向人才政策；官方统计更新。检测命中后才启动增量采集。

## 三、来源优先级

（TODO：按业务配置实例化渠道清单）默认层级：① 官方公报 / 法规数据库（唯一采信层） ② 立法记录 ③ 媒体转述仅作线索；每格活值附 `[官方原文 URL, 版本日期]`。

## 四、追踪表（政策台账联动）

监测法规清单（名称 / 发布机构 / 发布与生效日期 / 状态）、官方发布渠道清单（逐渠道 URL 与更新机制）、影响对象矩阵（TODO：业务配置定义逐项）；月度运行后逐项回写 `{{REGISTRY_PATH}}`，prompt 模板内严禁填写活值。

## 五、报告结构骨架

九节固定骨架见[月度监测类型模板第三节](../../templates/policy-analysis/prompt-monthly-monitor-template.md)；业务固化锚节标题（TODO：实例化后声明并逐字继承）。

## 六、执行方式（建议）

1. 变更检测先行：先比对上期台账与本期官方发布，锁定变更清单，再启动增量采集子代理。
2. 解读逐条附条款定位；新旧制度冲突并列对照；无法核实项单列「待复核清单」。

## 七、渲染与交付

- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`；月度报告顶部导航为强制项。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-21 | 初始版本 | 政策法规解读型扩展月度节拍；从类型模板拆出独立泛用版月度提示词 |
