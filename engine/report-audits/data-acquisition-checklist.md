# 11 维数据采集清单（可执行版）

> **状态**：现行清单
> **依据**：[量化研究体系优化实施方案](quant-system-optimization-plan-2026-11-14.md) 第二章
> **使用方式**：逐项登记 → 取数 → 双源 → 入库 → 消号。状态取值：`pending` / `in_progress` / `done` / `blocked`。
> **来源分级**：① 官方一手 > ② 行业机构 > ③ 挂牌门户 > ④ 媒体转述（须标「需核实原文」）。
> **优先级**：P0 = Phase 1 必须上线；P1 = Phase 2；P2 = Phase 3。
> **最后更新**：2026-11-20（E2 复查：官方站可达性改善，命中 DLD 官方年报与 CBUAE 官方利率入口；仍无新增消号）

| # | 维度 | 核心指标 | 权威来源 | 频率 | 优先级 | 口径说明 | 获取方式 | 状态 |
|---|---|---|---|---|---|---|---|---|
| 1 | 就业 | 失业率 / 劳动参与 / 净迁入 / 行业就业 | Dubai LFS（DDSE/Digital Dubai）、FCSC、GASTAT | 月/季 | **P0** | 调查 vs 行政登记口径不可混用；禁用无官方依据的商业失业率 | 官方报告 PDF + 新闻稿；LFS 与 FCSC 双源 | blocked |
| 2 | 收入 | 薪资中位数 / 行业薪资 / 实际工资 | LFS、薪酬指南（Michael Page/Hays/Robert Half）、CBUAE QER | 半年/年 | **P0** | 税前/税后、AED 月/年、basic vs total 须声明 | 报告 PDF；多源区间并列 | blocked |
| 3 | 空置 | 住宅空置率 / 存量—吸纳 | ValuStrat、REIDIN、CBRE/JLL、DLD 单元数据集 | 季 | **P0** | 无全市统一官方序列；第三方为模型估算，标「参考」，不进信号合成 | 机构季报 + DLD open dataset 自建 | blocked |
| 4 | 竣工 | 竣工登记 / 交付量 | Dubai Municipality（竣工证书）、C&W Core、Cavendish Maxwell、ValuStrat | 月/季 | **P0** | 三机构定义不同，不可加总 | 官方季度新闻稿 + 机构季报并列 | blocked |
| 5 | 利率结构 | 3M/6M/1Y EIBOR、利差与倒挂、Base Rate、Fed 路径 | CBUAE、Federal Reserve（H.15/SEP）、EIBOR 定盘 | 日 | P1 | 定盘 vs 月均；4 位小数 | CBUAE 公报 + Fed 发布；日度抓取 | pending |
| 6 | 信贷 | 按揭余额 / 不良率 / LTV 分布 / 信贷景气 | CBUAE（货币与信贷统计、CSS）、QER | 月/季 | P1 | 全行业 vs 房地产分项；无独立科目时并列总量 | QER/CSS 官方 PDF；统计 + 调查双源 | pending |
| 7 | 资本流动 | FDI 分行业 / 证券投资 / 主权基金流向 | UNCTAD WIR、UAE Ministry of Investment、IMF CDIS、CBUAE | 季/年 | P1 | 流量 vs 存量；绿地公告 ≠ 实际到账 | WIR PDF + 官方新闻稿；口径并列 | pending |
| 8 | 政策原文 | LTV / 黄金签证 / 过户费 / 托管 / 租金规则 | u.ae、centralbank.ae、dubailand.gov.ae、RERA | 事件 | **P0** | 入口页 ≠ 条款页；未取得条款页一律「未核验」 | 官方条款页 + PDF 哈希存档 | in_progress |
| 9 | 高频代理 | 搜索指数 / 挂牌量 / 航班 / 信用卡消费 / 询盘 | Google Trends、Bayut/Property Finder、DEX、银行/卡组织 | 周 | P1 | 代理仅作方向，须与低频官方锚双层校准 | API/导出 + 周度抓取；代理层独立存储 | pending |
| 10 | 竞争 | 份额 / 定价 / 管线 / 招聘 | 公司财报、Menlo/Gartner/IDC、CBRE/JLL | 季 | P1 | 份额口径（支出/收入/部署）须声明；单源标「单源」 | 财报 + 机构报告；建份额时序表 | pending |
| 11 | 宏观高频 | PMI / 薪资增速 / 期限利差 / 油价 / 汇率 | S&P Global、EIA、CBUAE、Federal Reserve、BIS | 月/周 | **P0** | 官方 vs 市场分歧并列；油价用 Brent/WTI；AED 钉住 3.6725 | 官方发布 + 发布日历；周度快照 | in_progress |

## 采集 SOP（每项统一执行）

1. **登记**：台账新增行（指标 ID、来源 ID、频率、滞后、口径、核验状态、URL）。
2. **取数**：优先官方一手；记录发布日期、页码、PDF SHA-256。
3. **双源**：进入信号合成的数值须 ≥2 个独立来源方向一致。
4. **入库**：写入归一化 CSV；`status ∈ {已核验, 部分核验, 未核验}`。
5. **消号**：未核验项转入盲区台账（[blind-spot-ledger.md](blind-spot-ledger.md)）。
6. **巡检**：每季度核对来源 URL 可达性。

## 进度汇总

- P0 维度：就业、收入、空置、竣工、政策原文、宏观高频（6 项）。
- **2026-11-19 取数阻塞**：就业 / 收入 / 空置 / 竣工四项状态转 `blocked`——本环境检索未命中可核验的官方一手来源（DDSE、DLD、DM、ValuStrat / REIDIN 官方页）；待官方发布或可核验机构页后解除，对应盲区 B01 / B02 / B03 / B15（责任周期顺延至 2027-03）。
- 目标：Phase 1 末 P0 数据层上线；Phase 2 末 P1 数据层上线。

## 取数留痕（2026-11-19，E1/F1）

> 目标来源级别：官方一手；原则：不放宽来源级别、不虚报消号。

- **#1 就业**：命中 DDSE 官方 LFS 2026 启动公告（2026-10-28，样本 5,000 户，覆盖就业 / 失业 / 职业 / 行业分项），**结果未发布** → 维持 `blocked`。[Source: https://www.digitaldubai.ae/newsroom/news/digital-dubai-launches-the-labour-force-survey-2026-to-strengthen-data-driven-labour-market-planning-and-decision-making, 2026]
- **#2 收入**：LFS 收入分项随 LFS 2026 结果待发布；Michael Page / Hays 未获 UAE 2026 官方页 → 维持 `blocked`。
- **#3 空置**：ValuStrat 官方报告列表命中（《Dubai Real Estate Review Q3 2026》，2026-10-21），正文被浏览器验证拦截；REIDIN 被 Cloudflare 拦截 → 维持 `blocked`。[Source: https://www.valustrat.com/, 2026]
- **#4 竣工**：WAM 通讯稿转述 DLD 2025 竣工数据（124 个项目 / AED27.5bn，2026-02-24）；DLD 官方页与 DM 竣工证书序列未取得，且非双源 → 维持 `blocked`。[Source: https://www.chinadaily.com.cn/a/202602/24/WS699d6545a310d6866eb3a085.html, 2026]
- **结论**：P0 四项均未取得「官方一手数值 + 双源」，按「不虚报消号」维持 `blocked`；对应盲区 B01 / B02 / B03 / B15 责任周期维持 2027-03。

## 取数留痕（2026-11-20，E2 复查）

> 官方站可达性较 2026-11-19 改善（CBUAE / DLD / Digital Dubai 可达）；原则不变：不放宽来源级别、不虚报消号。

- **#1 就业 / #2 收入**：Digital Dubai 新闻室仅见 LFS 2026 启动公告（2026-09-17），**结果未发布** → 维持 `blocked`。[Source: https://www.digitaldubai.ae/newsroom/news, 2026]
- **#3 空置 / #4 竣工**：命中 DLD 官方《Dubai Real Estate Market — Annual Data Review 2025》（2026-10-12）及历年《Real Estate Sector Performance》年报列表；列表为 JS 渲染，**正文直链与数值未取得** → 维持 `blocked`，登记为解除路径。[Source: https://dubailand.gov.ae/en/open-data/research/, 2026]
- **#5 利率结构（B07 / B12）**：CBUAE 官方站可达，Base Rate 机制与 EIBOR 官方入口（Regulations PDF、Daily Liquidity Indicators xlsx）已核验；页面 JS 渲染，**静态抓取未取得 3M/6M/1Y 与 Base Rate 现值** → 维持 `open`，登记为解除路径。[Source: https://www.centralbank.ae/en/our-operations/monetary-policy-and-domestic-markets/, 2026]
- **交叉印证（非官方）**：聚合站点录得 CBUAE 基准利率 2026-09-16 由 3.65% 升至 3.90%，与盲区 B07 描述方向一致；非官方一手，不满足消号条件。[Source: https://tradingeconomics.com/united-arab-emirates/interest-rate, 2026]
- **结论**：本轮**无新增消号**；B01 / B02 / B03 / B15 与 B07 / B12 责任周期不变（2027-03 / 2026-12）。

## 取数留痕（2026-11-20，E3 浏览器渲染取数）

> 手段：妙手浏览器渲染（CBUAE / DLD 官方站为 JS 渲染页，静态抓取为空）+ 官方文件直取 + PDF 逐页文本提取。

- **#7 利率期限结构（B12）→ 命中并消号**：CBUAE 官方 EIBOR Rates 页含日度期限结构表（O/N、1W、1M、3M、6M、1Y），页面标注「Last updated: Thursday 19 November 2026 12:15:20 PM」；已从 DOM 结构化抽取 2026-11 月 14 个定盘日（11-02 … 11-19），入库 `data/processed/economy/dubai/apartment/eibor_2026.xlsx`（新增 `November 2026` 工作表）。官方来源已在 `source_registry.json`（S-007 / S-028 / S-077）。[Source: https://centralbank.ae/en/forex-eibor/eibor-rates/, 2026]
- **#3 空置 / #4 竣工（B01 / B03）→ 路径排除**：DLD 官方《Dubai Real Estate Market — Annual Data Review 2025》（54 页 / 13.2 MB PDF）正文已逐页提取，内容为交易量 / 价格 / 租金 / 投资者结构；`vacant` 仅指「vacant land（空地）」交易类别，**不含全市空置率序列**，亦**不含竣工量 / 新增供应** → 该解除路径排除。[Source: https://dubailand.gov.ae/en/open-data/research/dubai-real-estate-market-annual-data-review-2025/, 2026]
- **#5 利率结构（B07）→ 部分命中**：CBUAE 官方明确 Base Rate 定义（anchored to Fed IORB）与机制，但**未公布现值数值**（仅 2020 年机制通知 Notice 3082/2020）；Daily Liquidity Indicators（2026-11-19 官方 xlsx，7 张表）无 Base Rate 字段 → 维持 `open`。[Source: https://www.centralbank.ae/en/our-operations/monetary-policy-and-domestic-markets/, 2026]
- **结论**：**新增消号 1 项（B12）**，I-08 由 0/15 → **1/15 = 0.0667**；未消号盲区数 15 → **14**。
