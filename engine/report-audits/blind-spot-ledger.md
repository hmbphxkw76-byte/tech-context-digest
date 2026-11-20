# 盲区滚动台账（BLIND-SPOT-LEDGER）

> **状态**：现行台账（每月复盘会审一次；季度报告公布状态）
> **依据**：决策交付规范第六节 / `blind_spot_check.py`（BS-01–05）
> **机制**：每项盲区有优先级、责任周期与消号条件；未消号项须更新责任周期。
> **消号条件**（任一满足）：① 取得官方一手数值并双源确认；② 确认该变量永远无官方序列，并以高频代理替代（须记录代理与校准方式）；③ 证明对结论无实质影响（须给出敏感性证明）。
> **初始来源**：`content/economy/dubai/apartment/reports/2026_annual.html` 未核验清单（14 项）+ 收入 / 薪资序列（新增）。
> **优先级**：**P0 = 就业、收入、空置、竣工四类**（优先补充）；其余 P1 / P2。
> **目标**：盲区数 15 → ≤6（KPI-5，Phase 3 末）；P0 四类先行消号。
> **校验**：`python engine/tools/blind_spot_check.py`（字段 / 状态 / 责任周期 / P0 四类）。
> **最后更新**：2026-11-20（E3 浏览器渲染取数：**B12 利率期限结构消号**（1/15）；DLD 官方年报路径排除；B07 官方未公布 Base Rate 现值。见「定向取数留痕（E3）」）

| ID | 项目 | 优先级 | 影响 | 发现日期 | 责任周期 | 消号条件 | 状态 | 关联 KPI |
|---|---|---|---|---|---|---|---|---|
| B01 | 官方住宅空置率序列 | P0 | 供给—租金传导核心中间变量缺失 | 2026-11-14 | 2027-03 | ②代理替代（ValuStrat/REIDIN + DLD 单元数据集自建） | open | KPI-5 |
| B02 | 就业 / 失业率数值 | P0 | 需求侧判断滞后（K13 灰灯） | 2026-11-14 | 2027-03 | ①2026 劳动力调查结果发布后双源入库 | in_progress | KPI-5 / KPI-2 |
| B03 | 迪拜官方竣工登记 | P0 | 供给兑现无法官方锚定 | 2026-11-14 | 2027-03 | ②代理替代（DM 竣工证书 + 机构三口径并列） | open | KPI-5 |
| B04 | DLD Smart Rental Index 可下载时间序列 | P1 | 租金周期无法官方锚定 | 2026-11-14 | 2027-01 | ①取得可下载序列；或②代理替代（Ejari 复算 + Peak/DXBinteract） | open | KPI-5 |
| B05 | 签证门槛 / LTV / 过户费 / 托管法条 | P1 | 政策不可量化（G01–G04） | 2026-11-14 | 2026-12 | ①官方英文条款页 / PDF 哈希存档 | in_progress | KPI-2 / KPI-5 |
| B06 | FCSC 官方 CPI/GDP 英文序列 URL | P1 | 宏观口径核验 | 2026-11-14 | 2027-01 | ①取得官方序列 | open | KPI-5 |
| B07 | 2026-09 加息生效日（3.65%→3.90%） | P1 | 利率路径时点 | 2026-11-14 | 2026-12 | ①CBUAE 官方页面核验 | open | KPI-2 |
| B08 | 2026-09 迪拜人口「约 4.8m」 | P1 | 需求分母 | 2026-11-14 | 2027-01 | ①DDSE 官方英文页核验 | open | KPI-5 |
| B09 | 家庭户数 858,000 | P1 | 户均需求分母 | 2026-11-14 | 2027-01 | ①DSC 官方英文页核验 | open | KPI-5 |
| B10 | 迪拜 2026H1 GDP 细项（AED473bn 标题） | P2 | 增长结构判断 | 2026-11-14 | 2027-02 | ①取得细项；或②标注标题口径 | open | KPI-5 |
| B11 | UNCTAD WIR 2026 PDF 直连 | P2 | FDI 长期基线可复核性 | 2026-11-14 | 2027-01 | ①官方 PDF 直连；或②保留索引文本核验记录 | open | KPI-5 |
| B12 | 利率期限结构（3M/6M/1Y 利差） | P1 | 融资条件与衰退预期 | 2026-11-14 | 2026-12 | ①CBUAE / 定盘日度序列入库 | closed | KPI-5 / KPI-3 |
| B13 | 信贷结构（按揭余额 / 不良率 / LTV 分布） | P1 | 杠杆风险不可测 | 2026-11-14 | 2027-02 | ①CBUAE 货币与信贷统计入库 | open | KPI-5 |
| B14 | 汇率 / 资本流动序列 | P2 | 跨境资金对楼市边际影响 | 2026-11-14 | 2027-02 | ①CBUAE / UNCTAD 序列入库 | open | KPI-5 |
| B15 | 收入 / 薪资序列（迪拜 LFS / 薪酬指南） | P0 | 可负担性只能算月供，不能算月供 / 收入比 | 2026-11-15 | 2027-03 | ①LFS / 薪酬指南官方英文页双源入库 | open | KPI-5 / KPI-2 |

## 状态汇总

- open：12 项；in_progress：2 项（B02、B05）；**closed：1 项（B12，2026-11-20 E3 消号）**。
- **当前未消号盲区数 = 14**（总登记 15 项，已消号 1）；**I-08 = 1/15 = 0.0667**（目标 ≤6 项未消号）。
- **已消号证据（B12）**：CBUAE 官方 EIBOR 日度期限结构（O/N、1W、1M、3M、6M、1Y）已入库 `data/processed/economy/dubai/apartment/eibor_2026.xlsx`（2026-01 … 2026-11），官方来源登记于同目录 `source_registry.json`（S-007 / S-028 / S-077）。
- **P0 四类**：B02 就业、B15 收入、B01 空置、B03 竣工——优先补充；受取数阻塞，责任周期均顺延至 **2027-03**（见下节）。

## 阻塞与取数记录（2026-11-19）

**P0 四类取数尝试（首轮）**：本环境检索（web 搜索 / 抓取）未返回可核验的官方一手来源——DDSE / Dubai Statistics Centre、DLD、DM、ValuStrat / REIDIN 官方页均未命中。按「不虚报消号」原则，四类均**不消号**，责任周期由 2026-12 顺延至 2027-03。

**E1/F1 定向取数（2026-11-19 复核）**：详见下方「定向取数留痕」。结论：B02 / B15 命中 DDSE 官方公告但**结果未发布**；B01 / B03 仅获机构入口或官方通讯稿转述，均未满足消号条件。四类维持不消号，责任周期维持 2027-03。

| 关联盲区 | 阻塞原因 | 解除条件 |
|---|---|---|
| B01（阻塞） | ValuStrat 官方季报入口已定位（《Dubai Real Estate Review Q3 2026》），但正文被浏览器验证拦截；REIDIN 被 Cloudflare 拦截；DLD 单元数据集入口未取得 | 取得 ≥1 机构季报可核验数值 + DLD 数据集，记录代理与校准方式（消号条件②） |
| B02（阻塞） | DDSE 官方已启动 LFS 2026（样本 5,000 户），**结果尚未发布**；无官方失业率数值 | 结果发布后双源入库（消号条件①） |
| B03（阻塞） | WAM 通讯稿转述 DLD 2025 竣工数据（124 个项目 / AED27.5bn）已获，但未获 DLD 官方页与 DM 竣工证书序列，且非双源 | 取得官方 / 机构序列并并列口径（消号条件②） |
| B15（阻塞） | LFS 2026 收入分项随结果待发布；Michael Page / Hays 未获 UAE 2026 官方页 | 双源入库（消号条件①） |

### 定向取数留痕（E1/F1，2026-11-19）

> 检索环境：web 搜索 + 页面抓取；目标来源级别：官方一手（DDSE / Digital Dubai、DLD、Dubai Municipality、ValuStrat / REIDIN 官方页、CBUAE、FCSC）。原则：不放宽来源级别、不虚报消号。

| 关联盲区 | 查询词 | 命中 | 来源 / URL | 处置 |
|---|---|---|---|---|
| B02 / B15（就业 / 收入） | `Digital Dubai Labour Force Survey 2026` | 命中（官方） | [Source: https://www.digitaldubai.ae/newsroom/news/digital-dubai-launches-the-labour-force-survey-2026-to-strengthen-data-driven-labour-market-planning-and-decision-making, 2026] | DDSE 官方公告 LFS 2026 已启动（样本 5,000 户，覆盖就业 / 失业 / 职业 / 行业分项），**结果未发布** → 消号条件①未满足，维持 blocked |
| B01（空置） | `ValuStrat Dubai Real Estate Review Q3 2026` | 部分命中（机构） | [Source: https://www.valustrat.com/, 2026] | 官方列出《Dubai Real Estate Review Q3 2026》(2026-10-21)、《Dubai VPI Residential Values October 2026》(2026-11-10) 免费下载；正文页被浏览器验证拦截，未获空置率数值 → 消号条件②未满足 |
| B01（空置） | `REIDIN Dubai vacancy rate 2026` | 未命中 | https://www.reidin.com/（Cloudflare 拦截） | 无官方 / 机构空置序列 |
| B03（竣工） | `Dubai completed projects 2025 DLD` | 部分命中（官方通讯稿转述） | [Source: https://www.chinadaily.com.cn/a/202602/24/WS699d6545a310d6866eb3a085.html, 2026]（WAM 通讯稿转载，2026-02-24） | WAM 转述 DLD：2025 竣工项目 124 个（+7%）、价值 AED27.5bn（+23%）；未获 DLD 官方页 / DM 竣工证书序列，且非双源 → 消号条件②未满足 |
| B03（竣工） | `Dubai Municipality completion certificates statistics` | 未命中 | https://www.dm.gov.ae/municipality-business/buildings-regulation-permits-agency/ | DM 官方页仅列法规，无竣工统计 |
| B15（收入） | `Michael Page / Hays UAE salary guide 2026` | 未命中 | https://www.michaelpage.com/salary-guides | 仅见美国 / 中国 / 马来西亚版，无 UAE 2026 版 |

**处置说明**：P0 类别不得降级（`blind_spot_check` BS-04 要求四类恒为 P0），故不以「转 P1」方式处理；改为**更新责任周期 + 登记阻塞**。解除阻塞需官方发布或可核验的机构一手页（见[数据采集清单](data-acquisition-checklist.md)）。

### 定向取数留痕（E2，2026-11-20 复核）

> 目标：对 P0 四类与责任周期 2026-12 的 P1 项（B07 / B12）做一轮有界复查，确认是否有官方一手来源已发布。原则不变：不放宽来源级别、不虚报消号。
> 检索环境：web 搜索 + 页面抓取（CBUAE / DLD / Digital Dubai 官方站本轮**可达**，与 2026-11-19 相比有改善）。

| 关联盲区 | 查询 / 命中 | 来源 / URL | 处置 |
|---|---|---|---|
| B01 / B03（空置 / 竣工） | **命中（官方）**：DLD 官方研究列表列出《Dubai Real Estate Market — Annual Data Review 2025》（2026-10-12），另有历年《Real Estate Sector Performance》年报 | [Source: https://dubailand.gov.ae/en/open-data/research/, 2026]（列表为 JS 渲染，正文直链未取得） | **新线索**：该年报为 DLD 官方一手，可能含空置 / 竣工官方口径；本轮未取得正文数值（页面 JS 渲染 + 直链未解析）→ 消号条件①/②未满足，维持 open |
| B07 / B12（利率 / 期限结构） | **命中（官方入口）**：CBUAE 官方站可达——Monetary Policy 页明确 Base Rate 为「prevailing official monetary policy rate」，并给出 EIBOR Regulations PDF 与 Daily Liquidity Indicators（2026-11-19 xlsx）；FOREX & EIBOR 页存在 | [Source: https://www.centralbank.ae/en/our-operations/monetary-policy-and-domestic-markets/, 2026]；[Source: https://www.centralbank.ae/en/forex-eibor/, 2026] | **部分进展**：官方入口与机制表述已核验，但页面为 JS 渲染，静态抓取**未取得利率数值**（3M/6M/1Y 与 Base Rate 现值）→ 消号条件①未满足，维持 open |
| B07（交叉印证，非官方） | Trading Economics 录得 CBUAE 基准利率：2025-10-29 3.90% → 2025-12-10 3.65% → **2026-09-16 3.90%** | [Source: https://tradingeconomics.com/united-arab-emirates/interest-rate, 2026] | 与盲区描述「2026-09 加息 3.65%→3.90%」方向一致，仅作**方向印证**；聚合站点非官方一手，不满足消号条件 |
| B02 / B15（就业 / 收入） | Digital Dubai 新闻室仅见 LFS 2026 启动公告（**2026-09-17**，非首轮记录的 10-28），**结果仍未发布** | [Source: https://www.digitaldubai.ae/newsroom/news, 2026] | 维持 blocked；责任周期不变 |

**E2 结论**：本轮**无新增消号**——P0 四类与 B07 / B12 均未取得「官方一手数值 + 双源」。但官方可达性较 2026-11-19 明显改善，且定位到两条具体解除路径（DLD 官方年报正文、CBUAE EIBOR / Base Rate 数据直取），已登记为上表。责任周期维持 2027-03。

### 定向取数留痕（E3，2026-11-20 浏览器渲染取数）

> 手段：妙手浏览器渲染（CBUAE / DLD 官方站为 JS 渲染页，静态抓取为空）+ 官方文件直取 + PDF 逐页文本提取。原则不变：不放宽来源级别、不虚报消号。

| 关联盲区 | 手段 / 命中 | 来源 / URL | 处置 |
|---|---|---|---|
| **B12（利率期限结构）** | **命中并消号**：CBUAE 官方 EIBOR Rates 页含日度期限结构表（O/N、1W、1M、3M、6M、1Y），页面标注「Last updated: Thursday 19 November 2026 12:15:20 PM」；已从 DOM 结构化抽取 2026-11 月 **14 个定盘日**（11-02 … 11-19） | [Source: https://centralbank.ae/en/forex-eibor/eibor-rates/, 2026] | 入库 `data/processed/economy/dubai/apartment/eibor_2026.xlsx`，新增 `November 2026` 工作表（14 行，表头与原表一致）；官方来源已在 `source_registry.json` 登记 → **满足消号条件①，B12 → closed** |
| B01 / B03（空置 / 竣工） | **路径排除**：DLD 官方《Dubai Real Estate Market — Annual Data Review 2025》（54 页 / 13.2 MB PDF）正文已逐页提取——内容为**交易量 / 价格 / 租金 / 投资者结构**；`vacant` 仅指「vacant land（空地）」交易类别，**不含全市空置率序列**，亦**不含竣工量 / 新增供应** | [Source: https://dubailand.gov.ae/en/open-data/research/dubai-real-estate-market-annual-data-review-2025/, 2026]（PDF 直链 `/media/gpzjz0se/dubai-real-estate-market-annual-data-review-2025-english.pdf`） | **该解除路径排除**（避免后续重复尝试）；B01 / B03 维持 open，需另找 DLD 单元数据集 / DM 竣工证书序列 |
| B07（加息生效日） | **部分命中**：CBUAE 官方明确 Base Rate 定义（anchored to Fed IORB）与机制，但官方页面**未公布现值数值**（仅 2020 年机制通知 Notice 3082/2020）；Daily Liquidity Indicators（2026-11-19 官方 xlsx，7 张表）**无 Base Rate 字段**；站内搜索交互未成功 | [Source: https://www.centralbank.ae/en/our-operations/monetary-policy-and-domestic-markets/, 2026]；[Source: https://centralbank.ae/media/nj4dc0tj/daily-liquidity-indicators-19-nov-2026.xlsx, 2026] | 消号条件①「CBUAE 官方页面核验」**未取得 Base Rate 现值** → 维持 open；若 2026-12 前仍未取得，建议顺延 2027-03 |

**E3 结论**：**新增消号 1 项（B12）**，I-08 由 0/15 → **1/15 = 0.0667**；B01 / B03 的 DLD 年报路径**排除**；B07 维持 open。

## 变更记录

| 日期 | 变更 | 说明 |
|---|---|---|
| 2026-11-14 | 建立台账 | 由年度未核验清单 14 项转入；机制上线 |
| 2026-11-15 | 优先级 + 收入项 | 新增「优先级」列；P0 四类（就业 / 收入 / 空置 / 竣工）；新增 B15 收入 / 薪资序列；接入 `blind_spot_check.py` 校验 |
| 2026-11-19 | P0 四类阻塞登记 | 取数尝试未获官方一手来源（检索未命中）；按「不虚报消号」不消号，责任周期 2026-12 → 2027-03；新增「阻塞与取数记录」节 |
| 2026-11-19 | E1/F1 定向取数留痕 | 复核命中：DDSE 官方 LFS 2026 启动公告（结果未发布）、ValuStrat 官方季报入口（正文拦截）、WAM 转述 DLD 2025 竣工数据；四类均不满足消号条件，维持 open / in_progress 与责任周期 2027-03；新增「定向取数留痕」表 |
| 2026-11-20 | E2 定向取数复查 | 官方站可达性改善：命中 DLD 官方《Dubai Real Estate Market — Annual Data Review 2025》（2026-10-12）与 CBUAE 官方 Base Rate / EIBOR 入口（页面 JS 渲染，未取得数值）；LFS 2026 结果仍未发布。**无新增消号**，责任周期维持 2027-03；新增「定向取数留痕（E2）」表 |
| 2026-11-20 | **E3 浏览器渲染取数 + B12 消号** | 妙手浏览器渲染 CBUAE 官方 EIBOR Rates 页，结构化抽取 2026-11 月 14 个定盘日并入库 `eibor_2026.xlsx`（新增 `November 2026` 表）；**B12 转 closed**，I-08 = 1/15 = 0.0667；DLD 官方年报路径经 54 页 PDF 全文提取**排除**（不含空置率 / 竣工量）；B07 官方未公布 Base Rate 现值，维持 open |
