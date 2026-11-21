# 迪拜（阿联酋） · AI 网安行业 · 首期基线报告提示词（行业深度研究型）

> **用途**：执行「迪拜（阿联酋） AI 网安行业 行业研究机制」的**机制建立**任务：产出首期行业全景基线报告与配套研究边界档案。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：中文九节基线报告（canonical 富样式自包含 HTML 为主交付物，落盘 `reports/{{YYYY-MM}}_baseline_report.html`；md 源稿存 `sources/` 同名存档）+ 研究边界档案（`{{REGISTRY_PATH}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../../engine/templates/monitoring-common-spec.md) × [基线报告类型模板（行业深度研究型）](../../../../../../engine/templates/industry-research/prompt-baseline-setup-template.md) × [业务专属配置](./business-config.md)。冲突时以本文件为准。

## 运行变量（每次运行前填写）

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = AI 网安行业
{{CURRENT_DATE}}         = 本次执行日期，格式 YYYY-MM-DD（运行填写）
{{BASELINE_DATE}}        = 2026-11（首份基线报告完稿日期）
{{OUTPUT_PATH}}          = reports/{{YYYY-MM}}_baseline_report.html（主交付物）；md 源稿存 sources/{{YYYY-MM}}_baseline_report.md（同名存档，不参与 md2html.py 自动转换）
{{BASELINE_REPORT_PATH}} = reports/2026-11_baseline_report.html
{{REGISTRY_PATH}}        = data/processed/tech/ai-security/industry-research/dubai/ai_cybersecurity_indicator_registry.md
{{REGISTRY_FORMAT}}      = md-table
{{FRESHNESS_PRIORITY}}   = 近 12 个月内数据优先；超过 24 个月须标注年份并谨慎使用
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/ai-security/industry-research/dubai
{{REPORT_VERSION}}       = v1.0（首期基线固定）
```

**任务目标**：产出九节行业全景基线报告（产业链图谱、市场规模与格局、头部玩家、驱动因素与风险、趋势判断）与边界档案首建；多口径规模并列不合并；运行后回写 `{{REGISTRY_PATH}}`；基线报告**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`。

## 一、项目专属硬性约束

1. **中性立场**：不给投资评级、不出具 Go/No-Go 决策建议（边界归投资尽调型、可行性型）。
2. **结论边界**：趋势判断一律标「推断」并配反向声音（至少 2 条）；口径冲突并列呈现。
3. **受众定位**：面向关注「迪拜（阿联酋）AI 网安行业」的产业研究与决策读者，兼具行业分析与市场进入参考视角，保持**中性全景刻画**（见[业务配置](./business-config.md)第二节）。
4. **术语口径**：严格执行[业务配置](./business-config.md)第三节——「AI 网安行业」= AI 系统安全（模型 / Agent / 数据 / 供应链安全）+ AI 用于安全运营（智能 SOC、威胁情报、MDR/XDR）+ 网安市场中 AI 相关支出与采购，**不含**无 AI 维度的传统网安市场测算；Gartner（终端支出）≠ Mordor / GMI（含服务总收入），口径不同不可直接比较；全球口径与本地口径分列，禁止混算；招聘机构抽样 ≠ 官方或权威机构口径（标「抽样」并谨慎引用）；汇率固定 1 USD = 3.6725 AED。
5. **已修正事实清单**：基线报告须完整收录[业务配置](./business-config.md)第七节「已修正事实清单」全部条目（含各自来源），作为防回退锚；无来源不得追加，基线期不新造数值。

## 二、来源优先级

实例化自[业务配置](./business-config.md)第四节，层级从高到低：

① 阿联酋/迪拜政府官方（u.ae、desc.gov.ae、tdra.gov.ae、mediaoffice.ae、icp.gov.ae、WAM 英文、各自由区官网）
＞ ② 国际权威组织与分析机构（ISC2、ISACA、Gartner、IDC、SANS/GIAC、MITRE、OWASP、NIST、Mordor Intelligence、Global Market Insights）
＞ ③ 头部薪酬指南与招聘平台抽样（Hays、Michael Page、Cooper Fitch、Charterhouse；LinkedIn、Bayt、GulfTalent、foundit Gulf——仅作市场信号）
＞ ④ 英文行业/主流媒体（Khaleej Times、The National、Gulf News、Zawya、Reuters——只用于发现线索，数值须回官方/原始页校验）
＞ ⑤ 同源已核实资产：`content/tech/ai-security/security/dubai/` 业务线的基线报告、md 源稿与指标登记册，以及 `content/tech/weekly-roundup/reports/2026-11-13_weekly.html`（全球趋势转引，须标注「经周报转引」）。

- 每格活值附 `[来源, 年份]`；冲突时报双份并标注；`{{SOURCE_LANGUAGE_RULE}}` 强制执行，不符合者一律排除。

## 三～九、结构骨架与联动

- 九节固定骨架见[基线类型模板第三节](../../../../../../engine/templates/industry-research/prompt-baseline-setup-template.md)。
- 业务固化锚节标题（逐字继承，顺序与编号不变）：

| 节 | 固化锚标题 |
|---|---|
| 1 | 一、执行摘要 |
| 2 | 二、研究范围与方法 |
| 3 | 三、产业链图谱 |
| 4 | 四、市场规模与格局 |
| 5 | 五、头部玩家与竞争格局 |
| 6 | 六、驱动因素与风险 |
| 7 | 七、趋势判断（推断） |
| 8 | 八、数据治理与局限 |
| 9 | 九、参考来源清单 |

- 追踪表：研究维度 × 优先来源实例化自[业务配置](./business-config.md)第六节（9 项监测指标，活值维护于 `{{REGISTRY_PATH}}`，格式 `{{REGISTRY_FORMAT}}`）；基线期先引用 `data/processed/tech/ai-security/security/dubai/ai_cybersecurity_indicator_registry.md` 的已核实活值，不新造数值。

## 十、渲染与交付

- 主交付物：canonical 富样式自包含 HTML，落盘 `reports/{{YYYY-MM}}_baseline_report.html`；md 源稿存 `sources/` 同名存档，不参与 `md2html.py` 自动转换（防止覆盖手工渲染）。
- HTML 须通过 `python engine/tools/lint_reports.py`（表格标签配对强制）；页面构建遵循 PAGE-BUILD-SPEC v1.0，只用 canonical 设计令牌；基线导航采用简化锚点目录。
- `.nav-url` 使用 `{{REPO_RAW_URL_BASE}}` + 业务目录相对路径。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 依 business-prompt-scaffold.md 第三节与 business-config.md 实例化首期基线提示词；写入变量固定值、来源优先级、九节固化锚与已修正事实清单继承要求 |
