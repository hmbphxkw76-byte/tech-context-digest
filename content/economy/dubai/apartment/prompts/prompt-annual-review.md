# 迪拜公寓住宅市场 · 年度策略复盘提示词（市场指标监测型）

> **用途**：周期性（每年）执行《迪拜公寓住宅市场年度策略复盘》，动态获取英文权威数据，产出年度 HTML 报告 + 新版指标台账。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：中文 HTML 年度报告（本项目为纯图表型简报，只出 HTML）（`{{OUTPUT_PATH}}`）+ 新版指标台账（`{{OUTPUT_REGISTRY}}`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [年度复盘类型模板](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md) × [业务专属配置](./business-config.md)。质量规则见通用基座与通用规范；年度方法论（五态定义、回测校准、预测偏离、多年情景框架）见年度类型模板；业务变量、K01–K15 / RL 阈值、触发器、政策清单 G01–G05、口径冲突清单、台账工作表、渲染差异见业务配置；冲突时以本文件为准。

---

## 运行变量（每次运行前填写）

固定值见[业务配置](./business-config.md)第一节；运行时变量：

```
{{CURRENT_DATE}}         = 本次执行日期，格式 YYYY-MM-DD
{{YEAR}}                 = 被复盘的年份
{{NEXT_YEAR}}            = 台账新版生效年份
{{DATA_CUTOFF}}          = 数据截止日（未发布时写最近已发布周期）
{{OUTPUT_REGISTRY}}      = data/processed/economy/dubai/apartment/dubai_apartment_indicator_registry_{{NEXT_YEAR}}-01.xlsx
{{PREVIOUS_REPORT_PATH}} = reports/ 最近一期月度/季度报告
{{OUTPUT_PATH}}          = reports/{{YEAR}}_annual.html
{{REPORT_VERSION}}       = vYYYY.MM.DD
```

**命名规则**：报告用「被复盘年份」；台账用「生效年份」。例如 2026 年度复盘 → `reports/2026_annual.html` + `data/processed/economy/dubai/apartment/dubai_apartment_indicator_registry_2027-01.xlsx`。

**任务目标**：作为迪拜公寓住宅市场的量化研究分析师，执行年度策略复盘。目标不是写一篇市场评论，而是：① 复盘全年（价格、成交、供给、租赁、收益率路径）；② 检验预测（偏离 >30% 必须重设假设）；③ 重置基线（人口、FDI、GDP/CPI、利率、供给兑现率等长期锚）；④ 校准信号（回测 15 条规则，新增/校准预警红线）；⑤ 更新情景（按最新兑现率重算未来 3 年实际交付区间，输出条件化决策矩阵）；⑥ 更新台账（生成新版 Excel，说明全部变更）。

---

## 一、项目专属硬性约束

通用约束自动继承[通用基座第三节](../../../../../engine/templates/prompt-generic-base.md)；来源语言规则、受众定位、术语口径见[业务配置](./business-config.md)第二、三节；政策复核规则见年度类型模板第一节。本项目额外强制：

- **结论边界**：不给出具体买卖价位、杠杆比例、仓位建议；只给「条件 → 周期判读 → 框架性含义 → 风险提示」。年度报告必须包含至少一条**反向声音**，并做「已定价 / 未定价」分析。明确 AED 钉住美元，对人民币投资者本质是美元资产。

## 二、来源优先级

见[业务配置第四节](./business-config.md)。

---

## 三、基线锚定（防止已修正事实回退）

协议见[通用基座第五节](../../../../../engine/templates/prompt-generic-base.md)。更新时必须**读取 `{{PREVIOUS_REPORT_PATH}}`** 与基线报告 `reports/2026-11_baseline_report.html`，继承其结构与全部已核实结论。本清单随每次修正持续追加：

```
【已修正事实清单 — 首期为空，产生修正后逐条补记，格式如下】
- ❌ 不得再称"…"——正确结论为…。[Source: URL, 年份]
```

---

## 四、更新协议（本项目触发器）

刷新窗口与差异对比规则继承通用基座第六节；本项目触发器见[业务配置第七节「年度」](./business-config.md)。命中任一触发器即触发对应模块重点更新；无触发则降级为核验/收敛型轻运行，**不得为制造变化而虚构变化**。

---

## 五、年度必查内容（五项）

### 5.1 全年复盘
逐项还原并对比：

1. **公寓价格**：表观成交均价、同质化价格变动、成交中位价、混合调整指数、估值型指数。
2. **成交量 / 金额**：季度与全年、同比与环比；不同机构统计域并列，不混算。
3. **期房 / 现房结构**：期房成交占比、现房成交金额与笔数、二手/转售占比。
4. **交付量与兑现率**：实际交付（多口径）、计划交付、兑现率、历史兑现率区间。
5. **新推盘**：季度与累计、同比；区分「主动刹车」与「需求崩塌」。
6. **租金与收益率**：新签/续约中位、同质化变动、降租续约占比、毛/净收益率。
7. **分区表现**：核心区 vs 价值区收益率、挂牌租金跌幅、毛净差。

**预测 vs 实际偏离**：方法见[年度类型模板第一节](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md)（偏离度 =（实际 ÷ 对照）− 1；绝对值 >30% 必须重设假设并列出「重设了哪三项假设」；不做事后拟合）。

英文机构清单：Savills、CBRE、JLL、C&W Core、Cavendish Maxwell、ValuStrat、Knight Frank、PropertyIndex、Peak Trust、DXBinteract。

官方锚：
- DLD 成交登记：`https://www.dubaipulse.gov.ae/data/dld-transactions/dld_transactions-open`
- DLD 租约登记：`https://www.dubaipulse.gov.ae/data/dld-registration/dld_rent_contracts-open`
- 官方价格指数：`https://dubailand.gov.ae/en/open-data/indexes-home/`

### 5.2 官方年度数据与长期基线
逐项取最近已发布年度值：

| 机构 | 数据 | URL |
|---|---|---|
| UNCTAD | World Investment Report：UAE FDI 流入/存量/绿地项目 | `https://unctad.org/system/files/non-official-document/wir_fs_qa_en.pdf` |
| Digital Dubai / DDSE | 年度人口基准、家庭户数、劳动力调查 | `https://www.digitaldubai.ae/` |
| Dubai Statistics Centre | 人口与生命统计、住房与建筑年度表 | `https://www.dsc.gov.ae/` |
| IMF | WEO、Article IV、UAE 国别页 | `https://imf.org/external/country/are/index.htm` |
| CBUAE | Quarterly Economic Review、信贷景气调查 | `https://centralbank.ae/en/news-and-publications/publications/` |
| U.S. EIA | STEO：Brent 现货与预测 | `https://www.eia.gov/outlooks/steo/report/global_oil.php` |
| Dubai DET / Media Office | 全年游客、酒店入住率、客房夜 | `https://mediaoffice.ae/en` |

要求（年度通用纪律见年度类型模板第一节）：GDP/CPI 在 CBUAE 与 IMF 之间分歧**并列呈现**；分歧 >2pp 触发 K15；年度数据 6–9 个月时滞不得用于月度择时；人口「实时值」与「年度基准」不得混用。

### 5.3 政策框架复核
政策项清单（G01–G05）与官方入口见[业务配置第十节](./business-config.md)；复核规则（只核验官方英文页面、入口页 ≠ 条款页、未核验禁止引用中介数值、任一变更立即重算需求情景）见[年度类型模板第一节](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md)。

### 5.4 机制自检
回测方法与校准规则（持续型 / 年度型 / 高频型 / 单源 / 无法回测 / 计数呈现）见[年度类型模板第二节](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md)。本项目实例化：

1. **回测 15 条信号规则**（阈值见[业务配置第五节](./business-config.md)）：触发过密（>6 次/年）或过疏（0 次/年）须校准。机制运行不足 12 个月时，**如实标注「无法完成频率回测」**，只做「预校准（ex-ante）」。持续型规则（K02/K04/K06）改为「状态首次进入 + 持续月数」；年度型规则（K11/K12/K15）改用「可判定期数」。
2. **来源巡检**：逐条复核官方来源清单的 URL 路径、最近核验时间、最新已发布周期、发布频率变化；记录 404、聚合页替代、停更、版本延迟、降频；明确「桌面巡检 / 联网复测」。
3. **数据盲区**：官方住宅空置率、官方竣工登记、就业/失业序列、可下载的官方租金指数时间序列；每年检查是否补齐，未补齐写明替代方案（Ejari 自主复算、DLD transactions 自建口径、dld_units 自建存量）。
4. **增删指标**：新增派生指标或官方指标；合并重复指标；降级仅有二手转载的指标。
5. **生成台账新版本**：文件名带新年份，写明版本号与变更点。

### 5.5 三年供给情景
方法框架（计划锚 × 兑现率、三情景、末年残差推导、利率路径、决策矩阵、禁止事项）见[年度类型模板第三节](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md)。本项目实例化：兑现率运行前从 `{{REGISTRY_PATH}}` 读取最近已核验值填入，不得硬编码；利率路径为 Fed → CBUAE → EIBOR → 按揭月供 → 可负担房价；需求变量含人口、家庭形成、FDI、就业（就业为数据缺口时明确标注）。

---

## 六、预警红线体系（类型模板方法论 + 业务阈值）

### 6.1 五态定义与阈值重叠处理
五态定义表与重叠处理规则见[年度类型模板第二节](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md)。

### 6.2 三级红线组
见[业务配置第五节](./business-config.md)（一级 K01/K02/K04/K06/K08；二级 K03/K07/K10/K11/K12/K15；三级 K05/K09/K13/K14）。

### 6.3 K01–K15 红线值（年度校准版）
阈值表见[业务配置第五节](./business-config.md)；运行前以 `{{REGISTRY_PATH}}`「信号规则」表为准；硬红线数值变更须记录版本，不得事后改写。

> **RL-01 与 K01 的关系**：K01 是信号规则灯（机械阈值）；RL-01 是更严格的结构红线（3M EIBOR 月均 ≥4.75% 连续 2 个月，见[业务配置第六节](./business-config.md)）。二者均为本项目自设；K01 触发只作信号灯判定，RL-01 触发须启动升级复核并重算情景。

### 6.4 校准规则
见[年度类型模板第二节](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md)（持续型 / 年度型 / 高频型 / 单源 / 无法回测 / 计数呈现六条）。

---

## 七、关键监测指标追踪表（每次运行逐项核对）

> prompt 模板内严禁填写活值；运行前从 `{{REGISTRY_PATH}}` 读取、运行后回写。

| # | 监测指标 | 优先数据源 | 上次值（运行前从 {{REGISTRY_PATH}} 读取填入） | 本次是否更新 |
|---|---|---|---|---|
| 1 | 表观成交均价（全年） | CBRE / JLL / Savills |  | ☐ |
| 2 | 同质化价格变动 | ValuStrat VPI / PIX |  | ☐ |
| 3 | 成交量（套/金额） | DLD / Dubai Pulse |  | ☐ |
| 4 | 交付量与兑现率 | Cavendish Maxwell / C&W |  | ☐ |
| 5 | 新推盘量 | 各机构 |  | ☐ |
| 6 | 新签/续约租金中位 | DLD / Peak Trust |  | ☐ |
| 7 | 降租续约占比 | Cavendish Maxwell |  | ☐ |
| 8 | 分区毛/净收益率 | 各机构 |  | ☐ |
| 9 | 3M EIBOR / CBUAE 基准利率 | centralbank.ae |  | ☐ |
| 10 | GDP / CPI | CBUAE / IMF |  | ☐ |
| 11 | FDI 流入 | UNCTAD |  | ☐ |
| 12 | 人口 / 家庭户数 | DDSE / DSC |  | ☐ |
| 13 | Brent 油价 | eia.gov |  | ☐ |
| 14 | 国际游客 / 酒店入住率 | mediaoffice.ae |  | ☐ |
| 15 | 建筑许可 / 许可面积 | Dubai Municipality |  | ☐ |

> 每次运行须逐项填写"是否更新"，未变动项保留登记载体值并注明"截至 {{CURRENT_DATE}} 无更新"。

---

## 八、报告结构（11 节固定顺序，类型模板骨架的本项目实例）

骨架与标准列结构见[年度类型模板第四、五节](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md)；本项目实例化：

### 1 · 年度结论
结论先行（一句话周期判断）；证据边界（机制运行几期、目录内有哪些报告、哪些缺失；不虚构序列）；5 条年度结论（价格、成交、供给、租金、宏观）；8 张 KPI 卡（带来源、周期、日期、内嵌链接）；五态计数与核心 8 项矩阵；本节数据来源注。

### 2 · 全年关键数字
四张表：2.1 价格与成交 / 2.2 供需、交付与管道 / 2.3 租赁与收益 / 2.4 宏观与外部需求；配套图表 2–3 张 + 图注。

### 3 · 预测 vs 实际偏离
方法说明（机制首年无自有年初预测，用三类替代对照）；偏离 >30% 的三项假设重设；明确「不做事后拟合」。

### 4 · 四维年度全景
4.1 价格与成交 / 4.2 供需与管道 / 4.3 租赁与收益 / 4.4 宏观先行 / 4.5 传导链复盘（哪条链主导？至少一条反向声音；已定价/部分定价/未定价三行表）。4.1–4.4 来源注。

### 5 · 官方先行指标年度基线
官方读数表；GDP/CPI 分歧表（CBUAE / IMF / DDSE 并列）；5.1 长期基线（12 项）。图表：FDI 年度序列。

### 6 · 三年供给情景与决策矩阵
方法：计划锚 × 兑现率；低/中/高。利率路径：Fed → CBUAE → EIBOR → 月供，三种条件不赋概率；附月供/可负担房价/收益利差敏感度（机制自算）。决策矩阵 4 行。边界说明：不构成买卖/价位/仓位建议。

### 7 · 政策框架与未核验清单
G01–G05 表（清单见业务配置第十节）；未核验清单（至少 8 项）与年度必查要求。

### 8 · 信号阈值回测与预警红线
8.1 五态定义 + 三级红线组 + 统计条；8.2 15 条规则表；8.3 当前状态计数；8.4 校准。图表：EIBOR 与硬红/预警红/绿灯线。

### 9 · 官方来源巡检
来源逐项表；发布频率变化；四大数据盲区 n/4 补齐；「桌面巡检 / 联网复测」声明。

### 10 · 台账修订说明
版本、基线日、工作表数量、指标数量、信号规则、来源清单、监测日历、基线值的变化；新增/合并/降级指标；交付空缺；声明为本地版本记录。

---

## 九、表格与来源排版规范（项目专属）

通用规范见[监测报告规范第 3、4、5 节](../../../../../engine/templates/monitoring-common-spec.md)与[年度类型模板第五节](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md)标准列结构。本项目实例化：

- 数据表的「指标名称」或「机构名称」本身即链接（通用规范第 4 节 B 式）：`href` 完整 URL，链接文字保持原样 + `↗`，新窗口打开。适用：第 2 节四张表、第 5 节、第 5.1 长期基线、第 9 节、第 3 节来源列、第 8 节读数来源列。
- 来源注：第 1 节 KPI 卡后加「本节数据来源」；第 4 节 4.1–4.4 各加来源注；4.5 标注「机制分析判断，不新增外部数值」；第 6 节供给情景表后加来源注；图表图注必须含来源、统计周期、口径警示。
- 媒体转述标注与口径冲突并列：清单见[业务配置第十一节](./business-config.md)。
- 顶部导航：`.nav-url` = `{{REPO_RAW_URL_BASE}}`/reports/{{YEAR}}_annual.html；`.nav-tabs` 列出 11 节锚点。

---

## 十、新版台账规范（项目专属）

工作表框架（9 个）见[年度类型模板第六节](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md)；本项目工作表清单见[业务配置第十二节](./business-config.md)。本项目指标增删与版本记录：

### 10.1 指标增删
- 新增：期房-现房成交中位价差（派生）、Ejari 自主复算降租续约占比（派生，待执行）、Fed SEP 点阵图中位数（官方）。
- 合并：许可建筑面积并入建筑许可，作为同一次发布的子项，不单独计权。
- 降级：Property Monitor 城市指数降为参考序列，不进入信号合成；家庭户数保留但降权，维持「未核验」。

### 10.2 版本记录
在「使用说明」中写：版本号 / 基线日 / 生效年份、新增工作表、指标增删、阈值校准、来源巡检列、日历行数。历史记录保留。文件名用新年份，避免与旧版混淆。

---

## 十一、质量自检（项目专属）

通用自检见[通用基座第九节](../../../../../engine/templates/prompt-generic-base.md)与[年度类型模板第八节](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md)。本项目额外确认：

- [ ] 全篇无中文来源数据，URL 均为英文站
- [ ] 术语口径未混用（口径清单见业务配置第三节）
- [ ] 全年复盘七项齐全，预测 vs 实际偏离已计算
- [ ] 政策框架 G01–G05 复核状态明确（未核验项未引用具体门槛数值）
- [ ] 机制自检完成（15 条回测、来源巡检、盲区、增删指标）
- [ ] 三年供给情景三档兑现率取自 `{{REGISTRY_PATH}}`，未在模板内硬编码
- [ ] 五态计数与核心 8 项矩阵一致
- [ ] 追踪表 15 项均已核对并填"是否更新"
- [ ] 新版台账 `{{OUTPUT_REGISTRY}}` 已生成，工作表数量与版本记录正确
- [ ] 内联 JS 通过 `node --check`；ECharts 浅底深字研报风；图注含来源
- [ ] 顶部导航常驻可见，锚点标签与 10 节标题逐字对应、跳转准确，报告 URL 正确
- [ ] 所有含来源列的表逐行至少 1 个 `href`；KPI 卡全部有链接；媒体转述行全部有「需核实原文」
- [ ] 覆盖输出前已备份旧版；未删除历史报告
- [ ] 已产出"数据变更摘要"与"待复核清单"

---

## 十二、Agent 执行约定（项目专属）

通用约定见[通用基座第八节](../../../../../engine/templates/prompt-generic-base.md)与[年度类型模板第九节](../../../../../engine/templates/market-monitoring/prompt-annual-review-template.md)。本项目额外：

- 台账修改采用增量方式：复制旧表 → 修订 → 另存新版本，不覆盖旧版。
- 不得引用中文网站或中文转载作为数值依据；不得把商业中介/经纪商口径当作官方事实。
- 不得把计划量当交付量、把预测当实绩、把 YTD 当全年；多源冲突时不得静默择一或取均值。
- 在政策未核验时不得引用具体门槛数值；不得给出具体买卖价位、杠杆、仓位建议。
- 在机制不足 12 个月时不得伪造年度触发频次；不得事后拟合「年初预测」。

**结束提示词。**
