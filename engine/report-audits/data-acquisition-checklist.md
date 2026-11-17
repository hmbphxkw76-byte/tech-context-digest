# 11 维数据采集清单（可执行版）

> **状态**：现行清单
> **依据**：[量化研究体系优化实施方案](quant-system-optimization-plan-2026-11-14.md) 第二章
> **使用方式**：逐项登记 → 取数 → 双源 → 入库 → 消号。状态取值：`pending` / `in_progress` / `done` / `blocked`。
> **来源分级**：① 官方一手 > ② 行业机构 > ③ 挂牌门户 > ④ 媒体转述（须标「需核实原文」）。
> **优先级**：P0 = Phase 1 必须上线；P1 = Phase 2；P2 = Phase 3。
> **最后更新**：2026-11-16

| # | 维度 | 核心指标 | 权威来源 | 频率 | 优先级 | 口径说明 | 获取方式 | 状态 |
|---|---|---|---|---|---|---|---|---|
| 1 | 就业 | 失业率 / 劳动参与 / 净迁入 / 行业就业 | Dubai LFS（DDSE/Digital Dubai）、FCSC、GASTAT | 月/季 | **P0** | 调查 vs 行政登记口径不可混用；禁用无官方依据的商业失业率 | 官方报告 PDF + 新闻稿；LFS 与 FCSC 双源 | in_progress |
| 2 | 收入 | 薪资中位数 / 行业薪资 / 实际工资 | LFS、薪酬指南（Michael Page/Hays/Robert Half）、CBUAE QER | 半年/年 | **P0** | 税前/税后、AED 月/年、basic vs total 须声明 | 报告 PDF；多源区间并列 | pending |
| 3 | 空置 | 住宅空置率 / 存量—吸纳 | ValuStrat、REIDIN、CBRE/JLL、DLD 单元数据集 | 季 | **P0** | 无全市统一官方序列；第三方为模型估算，标「参考」，不进信号合成 | 机构季报 + DLD open dataset 自建 | pending |
| 4 | 竣工 | 竣工登记 / 交付量 | Dubai Municipality（竣工证书）、C&W Core、Cavendish Maxwell、ValuStrat | 月/季 | **P0** | 三机构定义不同，不可加总 | 官方季度新闻稿 + 机构季报并列 | pending |
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

- P0 维度：就业、收入、空置、竣工、政策原文、宏观高频（6 项），其中 3 项 in_progress。
- 目标：Phase 1 末 P0 数据层上线；Phase 2 末 P1 数据层上线。
