# 盲区滚动台账（BLIND-SPOT-LEDGER）

> **状态**：现行台账（每月复盘会审一次；季度报告公布状态）
> **依据**：决策交付规范第六节 / `blind_spot_check.py`（BS-01–05）
> **机制**：每项盲区有优先级、责任周期与消号条件；未消号项须更新责任周期。
> **消号条件**（任一满足）：① 取得官方一手数值并双源确认；② 确认该变量永远无官方序列，并以高频代理替代（须记录代理与校准方式）；③ 证明对结论无实质影响（须给出敏感性证明）。
> **初始来源**：`content/economy/dubai/apartment/reports/2026_annual.html` 未核验清单（14 项）+ 收入 / 薪资序列（新增）。
> **优先级**：**P0 = 就业、收入、空置、竣工四类**（优先补充）；其余 P1 / P2。
> **目标**：盲区数 15 → ≤6（KPI-5，Phase 3 末）；P0 四类先行消号。
> **校验**：`python engine/tools/blind_spot_check.py`（字段 / 状态 / 责任周期 / P0 四类）。
> **最后更新**：2026-11-19（E1/F1 定向取数留痕，见「阻塞与取数记录」）

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
| B12 | 利率期限结构（3M/6M/1Y 利差） | P1 | 融资条件与衰退预期 | 2026-11-14 | 2026-12 | ①CBUAE / 定盘日度序列入库 | open | KPI-5 / KPI-3 |
| B13 | 信贷结构（按揭余额 / 不良率 / LTV 分布） | P1 | 杠杆风险不可测 | 2026-11-14 | 2027-02 | ①CBUAE 货币与信贷统计入库 | open | KPI-5 |
| B14 | 汇率 / 资本流动序列 | P2 | 跨境资金对楼市边际影响 | 2026-11-14 | 2027-02 | ①CBUAE / UNCTAD 序列入库 | open | KPI-5 |
| B15 | 收入 / 薪资序列（迪拜 LFS / 薪酬指南） | P0 | 可负担性只能算月供，不能算月供 / 收入比 | 2026-11-15 | 2027-03 | ①LFS / 薪酬指南官方英文页双源入库 | open | KPI-5 / KPI-2 |

## 状态汇总

- open：12 项；in_progress：2 项（B02、B05）；closed：0 项。
- **当前盲区数 = 15**（目标 ≤6，需逐项取得证据后消号；本台账为机制落地，不虚报消号）。
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

## 变更记录

| 日期 | 变更 | 说明 |
|---|---|---|
| 2026-11-14 | 建立台账 | 由年度未核验清单 14 项转入；机制上线 |
| 2026-11-15 | 优先级 + 收入项 | 新增「优先级」列；P0 四类（就业 / 收入 / 空置 / 竣工）；新增 B15 收入 / 薪资序列；接入 `blind_spot_check.py` 校验 |
| 2026-11-19 | P0 四类阻塞登记 | 取数尝试未获官方一手来源（检索未命中）；按「不虚报消号」不消号，责任周期 2026-12 → 2027-03；新增「阻塞与取数记录」节 |
| 2026-11-19 | E1/F1 定向取数留痕 | 复核命中：DDSE 官方 LFS 2026 启动公告（结果未发布）、ValuStrat 官方季报入口（正文拦截）、WAM 转述 DLD 2025 竣工数据；四类均不满足消号条件，维持 open / in_progress 与责任周期 2027-03；新增「定向取数留痕」表 |
