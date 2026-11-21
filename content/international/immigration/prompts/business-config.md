# 高技能移民政策 · 业务专属配置（business-config）

> **定位**：本文件是 `content/international/immigration` 业务线的**单一业务事实源**：运行变量固定值、来源优先级实例化、受众定位、术语口径、触发器、指标追踪清单、已修正事实清单全部集中于此。周期提示词（基线 / 月度）引用本文件，业务参数只在这里维护一份。
>
> **继承声明（四层体系）**：周期提示词 = [通用基座](../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../engine/templates/monitoring-common-spec.md) × [类型模板](../../../../engine/templates/policy-analysis/)（政策法规解读型）× 本文件。通用层修改自动对本业务线生效；本文件修改只影响本业务线。冲突时以周期提示词 ＞ 本文件 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、运行变量固定值

```
{{REGION}}               = 无（九国横向：新西兰 / 荷兰 / 澳大利亚 / 爱尔兰 / 加拿大 / 美国 / 新加坡 / 德国 / 法国）
{{TOPIC}}                = 高技能移民政策
{{REPORT_TYPE}}          = policy-analysis
{{BASELINE_DATE}}        = 2026-11-21（基线报告完稿日期）
{{REGISTRY_PATH}}        = data/processed/international/immigration/immigration_ledger.md
{{REGISTRY_FORMAT}}      = md-table
{{SOURCE_REGISTRY_PATH}} = data/processed/international/immigration/source_registry.json
{{BASELINE_REPORT_PATH}} = sources/2026-11_baseline_report.md
{{FRESHNESS_PRIORITY}}   = 近 12 个月内数据优先；超过 24 个月须标注年份并谨慎使用
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/international/immigration
```

**各周期落盘规则**（policy-analysis 类型模板第四节的实例化；命名对齐仓库工具链，版本号写入报告内）：

| 节拍 | 输出路径 | 定位 | 上期报告 |
|---|---|---|---|
| 基线 | `reports/2026-11_baseline_report.html`（md 源稿存 `sources/`） | 对比锚，常驻顶层 | 无 |
| 月度 | `reports/{{YYYY-MM}}_monthly.html`（md 源稿存 `sources/`） | 主更新节拍，九节全模块刷新 | 最近一期月度报告 + 基线 |
| 事件触发解读 | `reports/{{YYYY-MM-DD}}-<slug>.html`（md 源稿存 `sources/`） | 单国政策变更解读 | 基线 + 相关月度 |

**输出格式**：纯 HTML 交付（业务配置声明，走 monitoring-common-spec 第 1 节例外条款）：canonical 富样式自包含 HTML 为主交付物，落盘 `reports/{{周期}}.html`；md 源稿存 `sources/` 同名存档，**不参与 `md2html.py` 自动转换**（防止覆盖手工渲染）。

## 二、受众定位

面向「拟赴九国从事高技能 / 技术岗位就业或定居」的读者，兼具政策研究与职业规划顾问视角。报告允许给出框架性路径建议（标「建议 / 推断」），不承诺签证结果、不保证薪资水平、不构成法律意见。

## 三、术语口径区分（表格与正文中不得混用）

- **工作许可 ≠ 永居 ≠ 入籍**：三者法律地位与权利不同，逐条分列。
- **雇主担保类 ≠ 积分制类 ≠ 人才类**：担保义务、计分维度与提名要求不同，不得合并登记。
- **薪资门槛 ≠ 市场工资 ≠ 现行工资（prevailing wage）**：门槛口径（年毛 / 月毛 / 小时）与适用年份必须标注。
- **职业清单 ≠ 紧缺清单**：SOL / Green List / CSOL / STEM 类别口径不同，分列。
- **通道生效 ≠ 政策公布 ≠ 实施细则**：公布、生效、配套细则三阶段分列，附各自日期。
- **「高技能 / 高度技术人才」口径**：本业务线指各国面向高技能 / 技术职业的工签与人才类永居通道，含雇主担保类、积分制技术类与人才类；不含旅游、投资移民与低技能季节工。

## 四、来源优先级（通用基座第四节的实例化，冲突时报双份并标注）

① 九国官方政府 / 移民局 / 内政部页面（immigration.govt.nz、ind.nl、homeaffairs.gov.au、enterprise.gov.ie、canada.ca、uscis.gov / travel.state.gov / federalregister.gov、mom.gov.sg、make-it-in-germany.com / gesetze-im-internet.de、service-public.fr / france-visas.gouv.fr）；国际权威组织（EU 官方 europa.eu、OECD、UN、World Bank）
＞ ② 官方统计与职业清单（BAMF、Statistics NZ、ABS、Census）
＞ ③ 英文行业媒体（Reuters、Times of India、Aftenposten 等——只用于发现线索，数值须回官方 / 原始页校验）
＞ ④ 英文大众媒体转述（Bloomberg 等——只作线索，须标「需核实原文」）

**来源语言规则**：仅英文（{{SOURCE_LANGUAGE_RULE}}），严禁中文来源；若某数据点仅在中文源出现，标注「未找到英文权威来源，已剔除」并说明。政策见 `engine/docs/source-language-policy.md`（门禁 `source_check` R9）。

## 五、重大事件触发器（事件 → 受影响模块）

| 触发事件 | 受影响模块 |
|---|---|
| 任一国签证通道新增 / 关闭 / 改名 | 框架总览、逐国解读、台账 |
| 薪资门槛或配额调整生效 | 框架总览、逐国解读、影响矩阵 |
| 职业清单（SOL / Green List / CSOL / STEM 类别）调整 | 逐国解读、台账 |
| 积分制计分规则或抽签规则变更 | 框架总览、逐国解读 |
| 永居 / 入籍路径或居住年限变更 | 逐国解读、影响矩阵 |
| 针对 STEM / AI / IT 的定向政策出台 | 框架总览、逐国解读、建议章 |
| 官方统计（申请量 / 获批率 / 处理时长）年度更新 | 台账、数据治理 |

## 六、指标追踪表（活值维护于 {{REGISTRY_PATH}}）

| # | 监测指标 | 口径 / 单位 | 优先数据源（英文） |
|---|---|---|---|
| 1 | 九国高技能通道数量与状态 | 个 / 开放·关闭·待定 | 各国移民局官方页 |
| 2 | 各国薪资门槛（年 / 月 / 小时） | 本币 + 适用年份 | 各国移民局官方页 |
| 3 | 雇主担保与认证要求 | 是 / 否 + 条件 | 各国移民局官方页 |
| 4 | 积分制计分维度与门槛 | 分 / 维度 | 各国移民局官方页 |
| 5 | 永居 / 长期居留路径与居住年限 | 年 | 各国移民局 / 内政部 |
| 6 | 年度配额与抽签规则 | 个 / 轮次 | 各国移民局 / 官方公报 |
| 7 | 职业清单版本与调整 | 版本 / 条目数 | 各国官方清单 |
| 8 | 处理时长与申请量 | 工作日 / 件 | 各国官方统计 |
| 9 | STEM / AI / IT 定向安排 | 有 / 无 + 通道 | 各国移民局 |
| 10 | 已核实 / 部分核验 / 待核实项计数 | 项 | 本台账第八节 |

> **阈值口径示例（防报告阈值三处不一致）**：荷兰 HSM / EU Blue Card 2026 年年龄门槛 ≥30 岁 €5,942/月、<30 岁 €4,357、毕业生 €3,122（来源见报告第九节；各国分表口径以官方页为准）。

## 七、已修正事实清单（基线锚，防回退；无来源不得追加）

```
- 首期为空；后续运行产生修正后逐条补记（格式：❌ 不得再称「旧说法」——实际为「新说法」。[Source: URL, 年份]）。
```

## 八、基线九节结构固化锚

基线报告 `sources/2026-11_baseline_report.md` 九节结构为该业务线固化锚，后续报告逐字继承：

1. 执行摘要｜2. 政策台账与监测机制｜3. 高技能移民框架总览｜4. 重点国家政策逐条解读｜5. 影响对象矩阵｜6. 合规应对建议（建议章）｜7. 生效时间线｜8. 数据治理与局限｜9. 参考来源清单

---

## 九、信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：四级标注与摘要引用约束见 `engine/templates/information-layering-spec.md` 第二 / 四节；新增信息统计模块见第四节。
- **事实卡片**：本业务线暂不接入共享事实域；如后续接入，正文以 `[FC-…]` 引用，不复制卡片全文。
- **决策卡与行动协议**：核心判断输出决策卡（结论 / 证据强度 / 触发条件 / 反向证据 / 信息充分度）；行动项五要素 + 三档优先级。
- **阈值校准**：首次中期回测 2027-06；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节。
- **场景切片**：主场景 **赴外就业 / 定居决策**；次场景 **政策研究 / 比较**。
- **影响分级**：`impact_tier = high`（高影响，强制披露矩阵见 `engine/templates/information-layering-spec.md` §七）。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」。
- **盲区**：P0 四类（通道状态 / 薪资门槛 / 清单版本 / 处理时长）优先消号。

---

## 十、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-21 | 初始版本 | 建立 immigration 业务线：运行变量、来源优先级实例化、术语口径、触发器、10 项指标、九节固化锚；节拍为基线 + 月度主更新 + 事件触发解读 |
