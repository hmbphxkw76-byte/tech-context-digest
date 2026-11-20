# 迪拜（阿联酋） · AI 网安竞争格局 · 首期基线报告提示词（竞争情报监测型）

> **用途**：执行「迪拜（阿联酋） AI 网安竞争格局 竞争情报持续监测机制」的**机制建立**任务：产出首期竞争格局基线报告与配套竞品档案库。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：中文九节基线报告（canonical 富样式自包含 HTML），落盘 `reports/2026-12_baseline_report.html` + 竞品档案库（`data/processed/tech/ai-security/competitive-intelligence/dubai/ai_cyber_competition_registry.md`，md-table）；md 源稿为可选存档，不参与 `md2html.py` 自动转换。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../../engine/templates/monitoring-common-spec.md) × [基线报告类型模板（竞争情报监测型）](../../../../../../engine/templates/competitive-intelligence/prompt-baseline-setup-template.md) × [业务专属配置](./business-config.md)。质量规则见通用基座与通用规范；基线差异与九节骨架见基线类型模板；业务变量、监测竞品清单、触发器、来源优先级见业务配置；冲突时以本文件为准。

---

## 运行变量（每次运行前填写）

固定值（见[业务配置第一节](./business-config.md)）：

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = AI 网安竞争格局
{{BASELINE_DATE}}        = 2026-12（首期基线报告落款周期）
{{REGISTRY_PATH}}        = data/processed/tech/ai-security/competitive-intelligence/dubai/ai_cyber_competition_registry.md
{{REGISTRY_FORMAT}}      = md-table
{{BASELINE_REPORT_PATH}} = reports/2026-12_baseline_report.html
{{FRESHNESS_PRIORITY}}   = 最新官方 / 一手发布 > 上期值 > 第三方研究 > 媒体转述
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/ai-security/competitive-intelligence/dubai
```

运行时变量：

```
{{CURRENT_DATE}}         = 本次执行日期，格式 YYYY-MM-DD
{{OUTPUT_PATH}}          = reports/2026-12_baseline_report.html
{{REPORT_VERSION}}       = v1.0（首期基线固定）
```

**任务目标**：产出九节竞争格局基线报告与竞品档案库首建。覆盖[业务配置第五节](./business-config.md)声明的全部监测玩家（11 项分层条目，逐家档案卡，每格附 `[来源, 日期]`）；运行后回写 `data/processed/tech/ai-security/competitive-intelligence/dubai/ai_cyber_competition_registry.md`；基线报告**无上期报告**，不读取 `{{PREVIOUS_REPORT_PATH}}`；「已修正事实清单」首期为空，产生修正后逐条补记（格式见[通用基座第五节](../../../../../../engine/templates/prompt-generic-base.md)）。

---

## 一、项目专属硬性约束

通用约束（逐点引用、事实与推断分离、口径标注、数据纪律）自动继承[通用基座第三节](../../../../../../engine/templates/prompt-generic-base.md)；基线特殊定位见[基线类型模板第一、二节](../../../../../../engine/templates/competitive-intelligence/prompt-baseline-setup-template.md)。本项目额外强制：

1. **信息边界**：只采集公开合法信息（官网、财报、招聘、应用商店、专利、公开社媒）；不使用非公开渠道，不伪造无法核实的动作记录。
2. **来源语言规则**：仅英文（`{{SOURCE_LANGUAGE_RULE}}`），严禁中文来源；若某数据点仅在中文源出现，标注「未找到英文权威来源，已剔除」并说明。政策见 `engine/docs/source-language-policy.md`（门禁 `source_check` R9）。
3. **结论边界**：威胁 / 机会提示标「判断 / 推断」，与事实分离；不做「对手必然失败 / 必然成功」式断言。
4. **受众定位**：面向在迪拜 / 阿联酋市场参与或拟参与 AI 网安竞争的产品、市场与战略团队，兼及投资者与政策研究者（[业务配置第二节](./business-config.md)）。
5. **口径纪律**：份额口径并列不合并（全球企业 LLM API 支出份额 ≠ 企业 AI 部署支出份额 ≠ 阿联酋网安市场规模 ≠ MENA 信息安全终端支出 ≠ 全球 AI in cybersecurity 市场规模）；动作登记字段 = 编号 + 玩家 + 动作 + 日期 + 来源 URL；单源动作标「单源待证」，关键动作须至少 2 家独立来源确认；汇率固定 1 USD = 3.6725 AED（钉住）。

## 二、来源优先级

见[业务配置第四节](./business-config.md)（① 官方一手 ＞ ② 行业机构 / 第三方研究 ＞ ③ 招聘 / 门户抽样 ＞ ④ 媒体转述）；关键动作至少 2 家独立来源确认，单源标「单源待证」。机构清单以业务配置为准，冲突时报双份并标注：

| 层级 | 机构清单 |
|---|---|
| ① 官方一手 | u.ae、desc.gov.ae、tdra.gov.ae、mediaoffice.ae、ai.gov.ae、SEC EDGAR、各玩家官网 / 官方博客 / 财报 |
| ② 行业机构 / 第三方研究 | Gartner、Mordor Intelligence、Global Market Insights、Grand View Research、Menlo Ventures、ISC2、IDC、MITRE、OWASP |
| ③ 招聘 / 门户抽样 | hiredeveloper.ae、Bayt、GulfTalent、LinkedIn、foundit Gulf |
| ④ 媒体转述 | Khaleej Times、The National、Gulf News、gulftime.ae、telecomreview、Zawya、searchinform |

## 三、监测竞品清单与入选标准

入选标准：在迪拜 / 阿联酋有 AI 网安产品或交付能力，或具主权资本 / 算力抓手，或正进入区域市场；每家均有可追溯公开来源（[业务配置第五节](./business-config.md)）。

| 分层 | 玩家 |
|---|---|
| 直接 | G42 集团（Core42、CPX、Khazna、M42）；e& enterprise / Help AG；Moro Hub（DEWA 子公司）；Cloud4C；Microsoft（区域总部 + G42 投资）；Palo Alto Networks、Fortinet、Kaspersky、Cisco |
| 间接 | Hub71 生态；四大、Accenture、EY；DarkMatter / Digital14 |
| 潜在 | Presight；中国开源模型厂商（Kimi、DeepSeek、GLM、Qwen） |

> 逐家入选依据（来源）与「监测竞品 × 优先信息渠道」追踪表见[业务配置第五、六节](./business-config.md)；档案卡逐家维护，每格附 `[来源, 日期]`，未核实项注明「待核实」，不补值、不外推。

## 四、九节固化锚（结构骨架）

九节固定骨架见[基线类型模板第三节](../../../../../../engine/templates/competitive-intelligence/prompt-baseline-setup-template.md)。本业务线节标题固化锚**逐字取自已产出基线报告** `reports/2026-12_baseline_report.html` 的 h2 标题，后续报告逐字继承：

| 节 | 固化锚标题（逐字） |
|---|---|
| 1 | 一、执行摘要 |
| 2 | 二、监测机制设计 |
| 3 | 三、竞争格局总览 |
| 4 | 四、竞品档案首建 |
| 5 | 五、动态矩阵与信号规则 |
| 6 | 六、来源与核验治理 |
| 7 | 七、风险与盲区 |
| 8 | 八、交付物与后续运行方式 |
| 9 | 九、参考来源清单 |

## 五、追踪表与信号规则

- **追踪表**（监测竞品 × 优先信息渠道）见[业务配置第六节](./business-config.md)；基线运行后逐项回写 `{{REGISTRY_PATH}}`（md-table 格式），未核实项注明「待核实」，prompt 模板内严禁填写活值。
- **信号触发器**（事件 → 受影响模块）与**信号规则阈值 R1–R6**（监测对象 / 触发条件 / 确认标准 / 动作）见[业务配置第七、八节](./business-config.md)；动态矩阵与信号规则表须完整呈现，编号与业务配置一致。

## 六、渲染与交付

- **交付格式**：纯 HTML 交付（canonical 富样式自包含 HTML；走[监测报告通用规范第 1 节](../../../../../../engine/templates/monitoring-common-spec.md)例外条款，由[业务配置第一节](./business-config.md)声明）；md 源稿为可选存档，**不参与 `md2html.py` 自动转换**（防止覆盖手工渲染）。
- **页面规范**：遵循 `engine/docs/page-build-spec.md`（PAGE-BUILD-SPEC v1.0）与 `engine/docs/page-build-governance.md`；只用 canonical 令牌（`--navy:#16324f` 等，事实源 `engine/tools/report_style.py`），结构统一 `header.report-head`/`.hero` + `nav.report-nav`（`.nav-url` + `.nav-tabs`）+ `main.wrap` + `h2.sec`；`lang`/`viewport`/`.skip-link`/焦点环/`prefers-reduced-motion`/`@media print` 为强制项。
- **门禁**：`python engine/tools/lint_reports.py`（表格标签配对强制）与 `python engine/tools/page_build_check.py` 必须零 `[E]`。
- 基线导航采用简化锚点目录。

## 七、质量自检

通用自检见[通用基座第九节](../../../../../../engine/templates/prompt-generic-base.md)与[基线类型模板第六节](../../../../../../engine/templates/competitive-intelligence/prompt-baseline-setup-template.md)。本项目额外确认：

- [ ] 九节齐全、顺序正确、编号连续；节标题与已产出基线报告 h2 逐字一致
- [ ] 全部监测玩家档案卡覆盖，每格附来源与日期
- [ ] 事实与判断分离；威胁 / 机会提示标「判断 / 推断」
- [ ] 信号规则 R1–R6 全部登记，编号与动态矩阵一致
- [ ] 仅使用公开合法英文信息；信息边界与来源语言规则已写入
- [ ] 档案库与登记册已首建并回写；prompt 模板无硬编码活值
- [ ] HTML 通过 lint 与 page_build_check（零 [E]）

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 依竞争情报监测型脚手架第三节实例化：填入业务配置固定值、11 项监测玩家分层、来源优先级、R1–R6 信号规则与九节固化锚；纯 HTML 交付 |
