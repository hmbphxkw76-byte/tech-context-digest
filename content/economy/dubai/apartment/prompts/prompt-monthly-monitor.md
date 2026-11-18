# 迪拜公寓住宅市场 · 月度监测提示词（市场指标监测型）

> **用途**：周期性（每月）刷新《迪拜公寓住宅市场月度监测简报》，动态获取英文权威数据。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：中文 HTML《月度监测简报》（本项目为纯图表型简报，只出 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_monthly.html`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [月度监测类型模板](../../../../../engine/templates/market-monitoring/prompt-monthly-monitor-template.md) × [业务专属配置](./business-config.md)。质量规则（中文输出、逐点引用、事实与推断分离、口径标注、来源分级框架、基线锚定、更新协议、执行方式、输出要求、质量自检）见通用基座与通用规范；月度差异（9 节结构、T+1 判定、预警六件套框架）见月度类型模板；业务变量、来源优先级、术语口径、K01–K15 阈值、触发器、渲染差异见业务配置；冲突时以本文件为准。

---

## 运行变量（每次运行前填写）

固定值见[业务配置](./business-config.md)第一节；运行时变量：

```
{{CURRENT_DATE}}         = 本次执行日期，格式 YYYY-MM-DD
{{PREVIOUS_REPORT_PATH}} = reports/ 最近一期月度简报（首期除外）
{{OUTPUT_PATH}}          = reports/{{YYYY-MM}}_monthly.html
{{REPORT_VERSION}}       = vYYYY.MM.DD
```

**任务目标**：执行「迪拜公寓住宅市场持续监测机制」的月度监测任务，产出中文 HTML《月度监测简报》。以英文一手/权威来源为依据、以指标台账为编号骨架、以上一期报告与首期基线为对比锚，完成「核验 → 判定 → 偏离 → 缺口 → 观察」闭环，产出可直接用于下期对比的报告。

---

## 一、项目专属硬性约束

通用约束自动继承[通用基座第三节](../../../../../engine/templates/prompt-generic-base.md)；来源语言规则、受众定位、术语口径见[业务配置](./business-config.md)第二、三节。

## 二、来源优先级

见[业务配置第四节](./business-config.md)。

---

## 三、基线锚定（防止已修正事实回退）

协议见[通用基座第五节](../../../../../engine/templates/prompt-generic-base.md)。更新时必须**读取 `{{PREVIOUS_REPORT_PATH}}`**（首期除外）与基线报告 `reports/2026-11_baseline_report.html`，继承其结构与全部已核实结论。本清单随每次修正持续追加：

```
【已修正事实清单 — 首期为空，产生修正后逐条补记，格式如下】
- ❌ 不得再称"…"——正确结论为…。[Source: URL, 年份]
```

---

## 四、更新协议（本项目触发器）

刷新窗口与差异对比规则继承通用基座第六节；本项目触发器见[业务配置第七节「月度」](./business-config.md)。命中任一触发器即触发对应模块重点更新；无触发则降级为核验/收敛型轻运行，**不得为制造变化而虚构变化**。

---

## 五、本月必覆盖指标（五组）

### 5.1 融资条件
- CBUAE 基准利率（Base Rate）
- EIBOR 全期限（重点 3M；能取得则列 1W/1M/2M/6M/1Y）
- AED/USD 参考汇率
- 美联储 FOMC 决议 / 纪要 / 票型 / 目标区间

官方源：`https://centralbank.ae/en`、`https://www.centralbank.ae/en/forex-eibor/eibor-rates/`、`https://centralbank.ae/en/forex-eibor/exchange-rates/`、`https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm`

### 5.2 货币与信用（滞后约 5–6 周）
- 银行信贷、存款、M1/M2/M3

官方源：`https://centralbank.ae/en/research-and-statistics/`

### 5.3 价格
- PIX© 混合调整指数
- ValuStrat VPI
- Property Monitor 城市指数
- DLD 登记成交中位价

英文机构：PropertyIndex、ValuStrat、DXBinteract、Savills、CBRE、Knight Frank、Cavendish Maxwell

### 5.4 成交与租赁
- DLD / Dubai Pulse 成交与 Ejari 租约增量
- 新签与续约租金中位数
- 降租续约占比、涨租/持平占比
- 同质化新签租约价差
- 挂牌量与单盘询盘

官方源：`https://www.dubaipulse.gov.ae/data/dld-transactions/dld_transactions-open`、`https://www.dubaipulse.gov.ae/data/dld-registration/dld_rent_contracts-open`

### 5.5 宏观与外需
- EIA STEO 油价：`https://www.eia.gov/outlooks/steo/report/global_oil.php`
- DET / Media Office 国际游客与酒店入住率（含后续发布）
- UNCTAD / IMF 年度数据（若有更新）

---

## 六、关键监测指标追踪表（每次运行逐项核对）

> prompt 模板内严禁填写活值；运行前从 `{{REGISTRY_PATH}}` 读取、运行后回写（协议见通用基座第七节）。

| # | 监测指标 | 优先数据源 | 上次值（运行前从 {{REGISTRY_PATH}} 读取填入） | 本次是否更新 |
|---|---|---|---|---|
| 1 | CBUAE 基准利率 | centralbank.ae |  | ☐ |
| 2 | 3M EIBOR | centralbank.ae |  | ☐ |
| 3 | AED/USD | centralbank.ae |  | ☐ |
| 4 | 银行信贷 | CBUAE 统计公报 |  | ☐ |
| 5 | PIX© 混合调整指数 | propertyindex.ae |  | ☐ |
| 6 | ValuStrat VPI | valustrat.com |  | ☐ |
| 7 | DLD 登记成交中位价 | dubaipulse.gov.ae |  | ☐ |
| 8 | 新签公寓租金中位 | peaktrust.ae |  | ☐ |
| 9 | 降租续约占比 | Cavendish Maxwell |  | ☐ |
| 10 | Brent 油价 | eia.gov |  | ☐ |
| 11 | 国际游客 | mediaoffice.ae |  | ☐ |
| 12 | 酒店入住率 | mediaoffice.ae |  | ☐ |

> 每次运行须逐项填写"是否更新"，未变动项保留登记载体值并注明"截至 {{CURRENT_DATE}} 无更新"。

---

## 七、发布日历判定（项目专属，执行前置必做）

按[月度类型模板第一节](../../../../../engine/templates/market-monitoring/prompt-monthly-monitor-template.md)执行 T+0 / T+1 / 空窗判定，本项目的官方页面依据：

1. **CBUAE 统计公报**：查看官网首页最新一期标题与发布日期（例：`Statistical Bulletin August 2026` + `06 October 2026` ⇒ 9 月期未发布）。
2. **FOMC 纪要**：查看 FOMC 日历对应会议条目下**是否存在 Minutes 链接**；无链接 ⇒ 未发布，按 3 周惯例推算应发布日。
3. **EIA STEO**：查看页面顶部 **Release Date / Next Release Date**，据此判断当期版本归属。
4. **DET 旅游**：查看 Media Office 最新旅游稿件日期，判断数据截止月。

> 若本期与上期同日或仅隔 1 日：明确写「本期为 T+1 刷新，官方发布窗口未开，价值在于核验、口径澄清与阈值距离」，**不得为了"看起来有变化"而制造变化**。时效取舍遵循业务配置 `{{FRESHNESS_PRIORITY}}`。

---

## 八、项目专属专题预警：利率风险（触发时启用）

**触发条件**（注册于[业务配置第九节](./business-config.md)）：当 3M EIBOR 距 K01 红线 **≤25bp**（红线值见[业务配置第五节](./business-config.md)），或单月上行 **≥20bp** 时，必须在「融资条件」下新增 `风险预警` 小节，包含月度类型模板第三节的六件套；本项目适配：

1. **预警面板（四个距离同时看）**：距红线 bp 数 / 相对幅度 % / 部分样本均值距红线 / 近两日累计变动。
2. **关键区分**：仪表盘距离 ≠ 风险发生点；说明确认标准（月均连续 2 期）与单日破线的差别。
3. **四条证据**（至少覆盖）：斜率（近若干交易日累计变动、单日最大变动）；期限结构（3M/6M/1Y 利差、是否倒挂）；政策约束（Fed 票型、下次决议与 SEP、AED 钉住）；银行资金成本相对政策利率的溢价（EIBOR − Base Rate）。
4. **传导量化表 + 图**：至少四档利率（当前 / 红线 / +25bp / 更高），列出月供、月供变化、同等月供可负担房价、房价上限变化、毛收益率利差。**必须写明全部假设**（贷款额、期限、还款方式、利率全额传导、未计 margin 与重定价周期）。
5. **三情景**：只给可观测触发条件、EIBOR 路径、K01 判定、对公寓市场的影响；**不赋予概率**（无官方可校准的利率期货序列）。
6. **反向校准 + 来源核查表**：每项校准写明"应有权威来源 / 本期核查结果 / 核验状态 / 对预警的影响"；**"没有数据"要写成可核验的陈述**（例如"核对公报目录共 38 张表，无该分项"）；盲区统一按「方向确定、幅度未知」处理，不做点估计，不以中介口径替代。

---

## 九、报告结构（9 节，类型模板骨架的本项目实例）

骨架见[月度类型模板第二节](../../../../../engine/templates/market-monitoring/prompt-monthly-monitor-template.md)；本项目实例化：

1. **结论先行**：第一句给结论（市场状态 + 信号矩阵计数 + 是否翻转）；说明本期性质（T+0 / T+1 / 空窗）与本期价值；5–6 条要点（融资、货币信用、价格、租赁、成交供给、宏观外需）。
2. **关键数字卡**（8 张）：每张含指标名、数值（含单位）、统计周期、发布日期、来源简称 + 卡片内行内链接（完整 URL 写在 `href`，不占用表格列）；标注「实际值 / 预测值 F / 计划值」。
3. **月度指标逐项对比**：3.1 融资（含风险预警，如触发）/ 3.2 货币与信用 / 3.3 价格（含口径冲突并列）/ 3.4 成交与租赁 / 3.5 宏观与外需。每行：编号、指标、上期值、本期读数、方向、信号/阈值距离、来源（机构·周期·发布日·核验状态；不在单元格内书写 URL 全文）。
4. **信号灯判定**：4.1 先行信号矩阵（8 项，口径见[业务配置第八节](./business-config.md)，与基线同口径，注明"较上期是否变化"）；4.2 K01–K15 逐条判定（阈值取自[业务配置第五节](./business-config.md)与台账「信号规则」表、本期读数、判定、确认进度）。
5. **与首期基线的偏离**：逐项基线值、本期值、偏离度、性质（复核确认 / 修订 / 结构性 / 版本修正 / 无新期）；解释"零偏离"的含义。
6. **数据缺口与未核验项**：编号、缺口项、应为/预计时点、本期状态、影响与处理；状态标签：未发布 / 缺席 / 未取得 / 未重算 / 无官方值 / 未核验。
7. **下月观察清单**（8–10 条，带日期与触发条件）。
8. **台账更新编号与来源**：更新编号按五类分组（实质修订 / 新增口径记录 / 复核确认 / 未取得（维持上期值）/ 结论不变）；来源清单（级别、机构/文件、统计周期、发布日期），**不设独立「完整 URL」列**——全部来源链接以表头弹层承载（见第十一节）。

---

## 十、图表规范（项目专属）

通用规范见[监测报告通用规范第 2 节](../../../../../engine/templates/monitoring-common-spec.md)。本项目至少 4 张 ECharts：

1. **利率路径**：3M EIBOR 定盘折线 + K01 红线/绿线 markLine。
2. **租金结构**：按面积段的分组柱状图（多月对比），说明"表观跌 vs 同质化稳"。
3. **价格口径对照**：横向条形图，并列不同统计域（注明"不可相减"）。
4. **利率敏感性**：柱（月供）+ 双轴折线（可负担房价变化），标注"假设性测算"。

---

## 十一、HTML 交互与排版规范（项目专属）

### 11.1 固定顶部导航与锚点

按[通用规范第 5 节](../../../../../engine/templates/monitoring-common-spec.md)执行；本项目实例化：

- `.nav-url`：标签「报告 URL」+ 本报告仓库原始文件完整链接（`{{REPO_RAW_URL_BASE}}`（业务配置第一节）/reports/{{YYYY-MM}}_monthly.html）。
- `.nav-tabs`：8 个锚点标签，对应八节标题：1 结论先行 / 2 关键数字卡 / 3 月度指标逐项对比 / 4 信号灯判定 / 5 与首期基线的偏离 / 6 数据缺口与未核验项 / 7 下期观察清单 / 8 台账更新编号与来源。
- 标签文案须与章节标题一致；`href="#sN"` 的 `sN` 与对应 `<h2 class="sec" id="sN">` 逐字对应。

### 11.2 表格结构与列宽

按[通用规范第 3 节](../../../../../engine/templates/monitoring-common-spec.md)执行。信号矩阵（K01–K15，9 列）与逐项对比表（7 列）为高风险表，须逐表校验。

### 11.3 来源链接呈现

按[通用规范第 4 节 A 式](../../../../../engine/templates/monitoring-common-spec.md)执行：

- 第 8.2 节「本期引用来源清单」：「机构 / 文件」列表头加 `class="src-head" tabindex="0"`，悬停 / 聚焦展开 `.src-pop` 弹层，集中列出本期全部来源链接（每条 `target="_blank" rel="noopener"`，链接文本为机构 / 文件名）。
- 第 2 节关键数字卡：卡片内来源 URL 为行内链接，不占用表格列。
- 行内引用 `[Source: 完整URL, 年份]` 保持完整可访问。

---

## 十二、质量自检（项目专属）

通用自检见[通用基座第九节](../../../../../engine/templates/prompt-generic-base.md)与[月度类型模板第五节](../../../../../engine/templates/market-monitoring/prompt-monthly-monitor-template.md)。本项目额外确认：

- [ ] 全篇无中文来源数据；URL 均为英文站
- [ ] 术语口径未混用（口径清单见业务配置第三节）
- [ ] 每个关键数字标注来源机构·统计周期·发布日期·核验状态；完整 URL 以卡片内行内链接或 8.2 弹层承载，未写入表格单元格正文
- [ ] 信号判定执行"连续 2 期同向 + 排除失真信号 + 多指数互证"（失真清单见业务配置第八节）
- [ ] 追踪表 12 项均已核对并填"是否更新"
- [ ] 内联 JS 通过 `node --check`；表格/div 标签配对；锚点有效；浏览器打开预览
- [ ] 顶部导航常驻可见，9 个锚点全部跳转准确，报告 URL 与报告实际路径一致
- [ ] 表格内无独立「完整 URL」列；8.2 来源清单弹层链接数与来源条目一致、可点击访问
- [ ] 已产出"数据变更摘要"与"待复核清单"（通用规范）

**结束提示词。**
