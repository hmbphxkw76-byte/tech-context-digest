# 迪拜（阿联酋） · AI 网安行业 · 年度刷新提示词（行业深度研究型）

> **用途**：每年固定窗口对行业全景做全量刷新；重大结构性事件触发器命中时提前插刷对应模块。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：刷新版报告落盘 `{{OUTPUT_PATH}}`（`reports/{{YEAR}}_annual.html`；md 源稿存 `sources/` 同名存档）；插刷件 `reports/{{YYYY-MM-DD}}-主题.html`（命名不在标准正则内，validate 仅 WARN 不阻断，属预期）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [年度刷新类型模板（行业深度研究型）](../../../../../engine/templates/industry-research/prompt-annual-refresh-template.md) × [业务专属配置](./business-config.md)。冲突时以本文件为准。

## 运行变量（每次运行前填写）

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = AI 网安行业
{{CURRENT_DATE}}         = 本次执行日期，格式 YYYY-MM-DD（运行填写）
{{YEAR}}                 = 刷新年份（4 位）
{{PREVIOUS_REPORT_PATH}} = 上一年度刷新版路径（首年刷新时为空，仅锚定基线）
{{BASELINE_REPORT_PATH}} = reports/2026-12_baseline_report.html
{{REGISTRY_PATH}}        = data/processed/tech/industry-research/dubai/ai_cybersecurity_indicator_registry.md
{{REGISTRY_FORMAT}}      = md-table
{{OUTPUT_PATH}}          = reports/{{YEAR}}_annual.html（md 源稿存 sources/ 同名存档）
{{FRESHNESS_PRIORITY}}   = 近 12 个月内数据优先；超过 24 个月须标注年份并谨慎使用
{{SOURCE_LANGUAGE_RULE}} = 仅英文（全部取自英文网站，严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/industry-research/dubai
{{REPORT_VERSION}}       = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：完成「口径复核 → 数据刷新 → 格局更新 → 趋势复判」闭环；上年趋势判断逐条对照实际进展（命中 / 部分命中 / 未命中），复判结论与依据并列，**上年判断原文保留不删除**；九节结构与基线逐字一致；无触发且窗口未到时不启动，不得虚构变化。

## 一、各模块更新要点（按九节展开）

**重大事件插刷触发器**（[业务配置](./business-config.md)第五节；命中即提前刷新对应模块，无触发则按年度窗口执行，不得为制造变化而虚构变化）：

| 触发事件 | 受影响模块 |
|---|---|
| GITEX Global / GISEC Global 新一届举办（日期、主题、官方发布） | 产业链、头部玩家、趋势 |
| 阿联酋/迪拜新网络安全法规或 AI 安全政策生效（含 ISR 修订、NCAP、SBOM、PQC 计划） | 驱动因素、产业链下游、趋势 |
| Stargate UAE / 主权云（Core42 等）建设或运营状态更新 | 产业链上游、驱动因素 |
| ISC2《Cybersecurity Workforce Study》或 Gartner 中东安全支出预测更新 | 驱动因素、趋势 |
| 头部薪酬指南或招聘机构薪资抽样更新 | 头部玩家、驱动因素 |
| OWASP / MITRE / NIST 框架版本更新 | 产业链中游、趋势 |

- **产业链**：环节进出（上游算力与主权基建 / 中游平台·产品·服务与集成 / 下游监管与行业客户三层口径）、价值分布迁移、传导关系变化。
- **规模与格局**：最新口径规模与增速（Gartner 终端支出 / Mordor·GMI 含服务总收入 / 全球 AI in cybersecurity 等多口径并列不合并）、集中度变化（无公开可核实 CRn 或份额时标注「未核验」）、口径修订留痕。
- **玩家**：清单复核与进出登记（主权科技 / 托管安全 MSSP / 全球厂商区域总部 / 监管与政府 / 自由区·生态 / 咨询·集成分层）、逐家要点更新（业务、规模口径、定位，附来源）。
- **驱动与风险**：证据更新（威胁态势、ISR / NCAP / SBOM / PQC 合规、Stargate UAE / Core42 主权云、ISC2 / Gartner 人才数据）、新增风险、失效驱动归档。
- **趋势**：上年判断复判 + 新趋势推导（依据 → 推断 → 反向声音至少 2 条）。

## 二～六、协议与交付

- 更新协议与命名见[年度刷新类型模板](../../../../../engine/templates/industry-research/prompt-annual-refresh-template.md)第二、四节。
- **九节固化锚**（逐字继承基线，顺序与编号不变）：一、执行摘要；二、研究范围与方法；三、产业链图谱；四、市场规模与格局；五、头部玩家与竞争格局；六、驱动因素与风险；七、趋势判断（推断）；八、数据治理与局限；九、参考来源清单。
- 读取锚：`{{PREVIOUS_REPORT_PATH}}`（上年版）+ `{{BASELINE_REPORT_PATH}}`，继承九节结构、口径裁决与全部已核实结论；已修正事实清单（见[业务配置](./business-config.md)第七节）逐条继承并续写，无回退。
- 边界档案闭环：运行前从 `{{REGISTRY_PATH}}` 读边界档案（行业边界、产业链口径、玩家清单）→ 复核有效性 → 运行后回写（口径变更留痕、玩家进出登记）；数据变更摘要至少覆盖全部研究维度与口径清单。
- 趋势复判：上年趋势判断逐条对照实际进展（命中 / 部分命中 / 未命中），复判结论与依据并列，原文保留不删除。
- 渲染交付同基线提示词第十节：主交付物 canonical 富样式自包含 HTML（`reports/`），md 源稿存 `sources/`；HTML 须通过 `python engine/tools/lint_reports.py`。
- 质量自检追加项见[年度刷新类型模板第六节](../../../../../engine/templates/industry-research/prompt-annual-refresh-template.md)。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 依 business-prompt-scaffold.md 第四节与 business-config.md 实例化年度刷新提示词；写入变量固定值、插刷触发器与九节固化锚继承要求 |
