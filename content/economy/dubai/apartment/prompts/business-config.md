# 迪拜公寓住宅市场 · 业务专属配置（business-config）

> **定位**：本文件是 `content/economy/dubai/apartment` 业务线的**单一业务事实源**：运行变量固定值、来源优先级实例化、术语口径、受众定位、信号阈值（K 系 / RL 系）、仓库链接基址全部集中于此。四份周期提示词（基线 / 月 / 季 / 年）引用本文件，业务参数只在这里维护一份。
>
> **继承声明（四层体系）**：周期提示词 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [类型模板](../../../../../engine/templates/market-monitoring/) × 本文件。通用层修改自动对本业务线生效；本文件修改只影响本业务线。冲突时以周期提示词 ＞ 本文件 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、运行变量固定值

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = 公寓住宅市场
{{REPORT_TYPE}}          = market-monitoring
{{BASELINE_DATE}}        = 2026-11-10（首期基线日期）
{{REGISTRY_PATH}}        = data/processed/economy/dubai/apartment/dubai_apartment_indicator_registry_2027-01.xlsx
{{REGISTRY_FORMAT}}      = xlsx-ledger
{{SOURCE_REGISTRY_PATH}} = data/processed/economy/dubai/apartment/source_registry.json
{{BASELINE_REPORT_PATH}} = reports/2026-11_baseline_report.html
{{FRESHNESS_PRIORITY}}   = 最新官方页 > 上期值 > 预测值（本项目时效优先级）
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/economy/dubai/apartment
```

**各周期落盘规则**（通用规范第 1 节的实例化）：

| 周期 | 输出路径 | 版本号 | 上期报告 |
|---|---|---|---|
| 基线 | `reports/2026-11_baseline_report.html` | v1.0（首期固定） | 无 |
| 月度 | `reports/{{YYYY-MM}}_monthly.html` | vYYYY.MM.DD | `reports/` 最近一期月度简报 |
| 季度 | `reports/{{YYYY-Qn}}_quarterly.html` | vYYYY.MM.DD | `reports/` 最近一期季度报告 |
| 年度 | `reports/{{YEAR}}_annual.html` + `data/processed/economy/dubai/apartment/dubai_apartment_indicator_registry_{{NEXT_YEAR}}-01.xlsx` | vYYYY.MM.DD | `reports/` 最近一期月度 / 季度报告 |

**输出格式**：纯图表型简报，只出 HTML（通用规范第 1 节双格式交付的业务例外，本业务线声明适用）。

---

## 二、受众定位

面向拟赴迪拜置业 / 租赁的读者，兼具投资决策与风险预警视角。年度报告须明确：AED 钉住美元，对人民币投资者本质是美元资产。

## 三、术语口径区分（表格与正文中不得混用）

- 均价 ≠ 中位价 ≠ 混合调整指数（成交结构效应）
- 挂牌 ≠ 成交；期房 ≠ 一手；转售 ≠ 现房
- 毛收益率 ≠ 净收益率（净口径仅扣物业费）
- 全市住宅 ≠ 公寓专属；迪拜酋长国 ≠ UAE 联邦

---

## 四、来源优先级（通用基座第四节的实例化，冲突时报双份并标注）

① 官方一手：CBUAE、Federal Reserve、U.S. EIA、Dubai DET / Media Office、DLD / Dubai Pulse、Digital Dubai / DDSE、Dubai Statistics Centre、Dubai Municipality、UNCTAD、IMF
＞ ② 行业机构：Savills、CBRE、JLL、Cushman & Wakefield Core、Cavendish Maxwell、ValuStrat、Knight Frank、Peak Trust、DXBinteract、Property Monitor、PropertyIndex、DRED
＞ ③ 挂牌门户：Bayut、Property Finder（仅作卖方预期，不得替代成交 / 登记数据）
＞ ④ 媒体转述：Zawya、Reuters、Khaleej Times、Gulf News、The National（须标「需核实原文」，不得与官方一手同等处理）

**机构获取优先级 P0–P5**（季度报告替代方案选择）：

| 层级 | 渠道 | 使用规则 |
|---|---|---|
| P0 | CBRE / JLL / Knight Frank 官方研究页 | 可直接采信，标"已核验" |
| P1 | 官方 PDF / 报告下载 | 记录 PDF 哈希、发布日期、页码 |
| P2 | 官方研究订阅 / 新闻稿 | 用于第一时间获取新报告 |
| P3 | 英文媒体 | 只用于发现线索；数值标"需核实原文"，再回官方页/PDF 校验 |
| P4 | 其他英文行业机构 | 交叉验证方向；不替代 P0 |
| P5 | DLD 官方锚（transactions / rent contracts / units / price index） | 最终裁决成交量、租金、存量口径 |

**季度必查机构获取路径**：

- **CBRE**：研究总入口 `https://www.cbre.ae/insights`；最新季度报告页（如 `.../insights/figures/uae-real-estate-market-review-q3-2026`）；优先读报告页 "Latest Market Reports"，PDF 直链失效则回报告页点 "Download"。宏观预测（GDP/CPI/Brent）与 CBUAE/IMF/EIA 并列，不得合并。
- **JLL**：`https://www.jll.com/en-ae/insights`；Market Dynamics：`.../insights/market-dynamics`；UAE Living：`.../insights/market-dynamics/uae-living`（常在同一 URL 原地更新，每周检查）。滞后一期只能标"滞后一期"；UAE-wide 口径不得与 Dubai-only 数据合并。
- **Knight Frank**：新闻稿入口 `https://www.knightfrank.ae/newsroom/press-release`。豪宅门槛 `>US$10m`（约 AED36.7m）与 Savills `>AED10m` 不是同一门槛，禁止直接比较。当季新闻稿未发布则用上一季并标"滞后"，不得外推。

**季度最小可替代集**（CBRE / JLL / Knight Frank 均未取得时）：DLD 官方锚、Savills、C&W Core、Cavendish Maxwell、ValuStrat、PropertyIndex / DXBinteract；结论置信度降为「方向高、幅度中、时点低」。

---

## 五、信号规则阈值（K01–K15，年度校准版）

> 阈值为本项目自设（非官方）；运行前以 `{{REGISTRY_PATH}}`「信号规则」表为准。年度复盘校准后在此同步更新并记录版本，硬红线变更不得事后改写。

**三级分组**：

- **一级（定价直接约束，5 条）**：K01 3M EIBOR、K02 Fed 票型、K04 交付兑现率、K06 降租续约占比、K08 成交量同比。触发硬红即重算情景。
- **二级（结构假设，6 条）**：K03 许可面积、K07 价格同比、K10 毛收益率、K11 FDI、K12 人口/家庭、K15 官方预测分歧。触发后调整假设，不即时交易。
- **三级（趋势与情绪，4 条）**：K05 新推盘、K09 现房占比、K13 就业、K14 旅游/入住率。触发仅记录并提高监测频率。

| 编号 | 监测对象 | 等级 | 绿灯 | 黄灯 | 预警红线 | 硬红线 | 升级条件 |
|---|---|---|---|---|---|---|---|
| K01 | 3M EIBOR | 一级 | <3.50% 或连续 3 月下行 | 3.50–4.50% 横盘 | >4.35% 或 3 月累计上行 >40bp | >4.50% 或 3 月上行 >50bp | 月均连续 2 期 ≥4.50% → 硬红 |
| K02 | Fed 票型 / 点阵图 | 一级 | 转向降息 | 维持不变 | ≥1 票主张加息 | 加息倾向或 ≥2 票主张加息 | 纪要双确认 → 硬红·完全 |
| K03 | 许可建筑面积同比 | 二级 | <0% | 0–20% | >20% 单季 | >30% 连续 2 季 | 第 2 季 >30% → 硬红 |
| K04 | 交付兑现率 | 一级 | >65% | 50–65% | <50% | <45% 且计划量创高 | 补同口径双源 → 硬红·完全 |
| K05 | 新推盘量同比 | 三级 | <−50% | −50%～0% | >+10% 单季 | >+20% 连续 2 季 | 维持绿灯 |
| K06 | 降租续约占比 | 一级 | <10% | 10–15% | >15% | >20% 或单季 +5pp | 补 Q2 与原始 PDF → 硬红·完全 |
| K07 | 公寓中位价同比 | 二级 | >+3% | −3%～+3% | <−3% 连续 2 月 | <−5% 连续 3 月 | 3 月 + 2 指数 → 硬红 |
| K08 | 成交量同比 | 一级 | >−10% | −10%～−20% | <−20% | <−30% 连续 2 季 | 连续 2 季 → 硬红 |
| K09 | 现房成交金额占比 | 三级 | 持续上升 | 横盘 | 单季下滑 | 连续 2 季下滑 | 按金额复核 |
| K10 | 登记口径毛收益率 | 二级 | >7.0% | 6.0–7.0% | <6.0% | <5.5% | 同口径连续 2 期 |
| K11 | FDI 流入同比 | 二级 | >+5% | 0～+5% | <+2% | <0% | 年度值观察 |
| K12 | 人口 / 家庭增速 | 二级 | >5% | 3–5% | <5% | <3% 或家庭显著低于人口 | 年度基准 |
| K13 | 就业 / 失业 | 三级 | 就业净增 | 待发布 | 结果发布后 30 日未入库 | 失业率连续 2 期上行 | 发布后立即入库 |
| K14 | 酒店入住率 / 游客 | 三级 | >75% 且同比正增 | 65–75% | <65% | <60% 连续 3 月 | 剔除大型活动扰动 |
| K15 | 官方 GDP/CPI 分歧 | 二级 | <1pp | 1–1.5pp | >1.5pp | >2pp 或方向相反 | 并列呈现，区间替代点值 |

> **阈值重叠处理**：同一指标同时落入黄灯与预警红区间（K01 4.50/4.35、K11 +5/+2、K12 5/3 重叠）时，按「更严状态优先」处理并标注重叠区间；不得因黄灯区间覆盖而降级。

**三层重组（领先 / 同步 / 滞后，2026-11-14 起）**：K 系由单一红绿灯升级为三层合成（工具 `engine/tools/signal_synth.py`）。层权重：领先 0.50 / 同步 0.35 / 滞后 0.15；层内按等级 0.5/0.3/0.2 归一。

| 层 | K 编号 | 监测对象 |
|---|---|---|
| 领先 | K01、K02、K03、K05、K06、K11、K12、K13 | EIBOR / Fed / 许可面积 / 新推盘 / 降租续约 / FDI / 人口家庭 / 就业 |
| 同步 | K04、K07、K08、K09、K14 | 交付兑现 / 价格 / 成交量 / 现房占比 / 旅游入住 |
| 滞后 | K10、K15 | 毛收益率 / 官方 GDP·CPI 分歧 |

> 合成输出「周期阶段 + 信号一致性」；与 `cycle_clock.py` 阶段交叉校验，冲突即告警。

---

## 六、结构红线登记簿（RL-01–RL-09）

> 硬阈值本项目自设；运行前从 `{{REGISTRY_PATH}}`「信号规则」表读取。RL-01 与 K01 的关系：K01 是信号灯（机械阈值），RL-01 是更严格的结构红线；K01 触发只作信号灯判定，RL-01 触发须启动升级复核并重算情景。

| 编号 | 监测对象 | 硬阈值 | 触发后动作 |
|---|---|---|---|
| RL-01 | 融资成本 | 3M EIBOR 月均 ≥4.75% 连续 2 个月；或 Fed 单次加息 ≥25bp 且点阵图上移 | 重算月供/可负担性/收益利差；升级复核；暂停新增杠杆类建议 |
| RL-02 | 房东定价权 | 降租续约占比 ≥25% 连续 2 季；或涨租续约占比 <35% | 下修租金与毛收益率；重算次年登记租金情景 |
| RL-03 | 资产价格 | PIX 同比 ≤−8% 连续 3 个月；或同质化环比 ≤−3% 连续 2 季 | 切换同质化指数复核；重算估值 |
| RL-04 | 成交量 | 季度成交同比 ≤−45% 连续 2 季 | 下修去化速度与开发商现金流 |
| RL-05 | 供给兑现 | 兑现率 ≤35% 且次年计划 ≥150,000 套 | 重算次年实际交付区间 |
| RL-06 | 中期供给 | 许可建筑面积同比 ≥+60% 连续 2 季 | 上修中期供给；重算空置与租金压力 |
| RL-07 | 收益安全垫 | 登记口径毛收益率中位 ≤5.0%；或毛净差 ≥1.8pp | 重算相对无风险利率溢价；复核持有成本 |
| RL-08 | 外需/短租 | 酒店入住率 <55% 连续 3 个月；或游客连续 3 月同比负增 | 下修短租收益与旅游就业假设 |
| RL-09 | 就业/净迁入 | 调查失业率 >4.0% 连续 2 期 | 发布后 30 日内设定基线并纳入信号合成 |

---

## 七、重大事件触发器（按周期分表）

**月度**：

```
- CBUAE 利率决议 / FOMC 会议 → 融资条件
- EIA STEO 月报发布 → 宏观与外需
- DLD / Dubai Pulse 月度数据更新 → 成交与租赁
- CBUAE 统计公报发布 → 货币与信用
- DET / Media Office 旅游月度稿件 → 宏观与外需
```

**季度**：

```
- CBRE / JLL / Knight Frank 季度报告发布 → 四维必查
- CBUAE 季度经济评论 / 信贷景气调查 → 宏观先行
- CBUAE 利率决议 / FOMC 会议 → 宏观先行
- EIA STEO 月报发布 → 宏观先行
- DLD / Dubai Pulse 季度数据更新 → 价格成交、租赁收益
- DET / Media Office 旅游月度稿件 → 宏观先行
```

**年度**：

```
- CBRE / JLL / Knight Frank / Savills 年度或第四季度报告发布 → 全年复盘
- CBUAE 年度经济评论 / 信贷景气调查 → 官方年度数据
- UNCTAD WIR 新一期发布 → FDI 长期基线
- IMF WEO / Article IV 更新 → GDP/CPI 长期基线
- Dubai DET 年度旅游数据 → 外需基线
- 房地产相关政策变更（黄金签证、LTV、过户费、Oqood、租金规则）→ 政策框架复核
```

---

## 八、先行信号标准矩阵（8 项，月度 / 季度共用）

① CBUAE 基准利率 / 3M EIBOR；② Fed 政策倾向；③ 建筑许可 / 许可面积；④ 新推盘量；⑤ FDI 流入；⑥ 人口 / 家庭形成；⑦ 降租续约占比；⑧ 就业 / 失业率。

基线首期矩阵计数「4 红 3 绿 1 灰」为对比锚；重算不得机械沿用。

**失真信号清单**：EIBOR 季末/年末资金面扰动、单日跳价、季末集中续约、成交结构变化、单机构重设基线、个别 mega-project 一次性入市。

---

## 九、专题预警配置（月度）

**融资成本专题**（唯一注册专题）：当 3M EIBOR 距 K01 红线 **≤25bp**，或单月上行 **≥20bp** 时触发。六件套适配（通用月度模板第三节的实例化）：

- 传导量化表：至少四档利率（当前 / 红线 / +25bp / 更高），列月供、月供变化、同等月供可负担房价、房价上限变化、毛收益率利差；写明全部假设（贷款额、期限、还款方式、利率全额传导、未计 margin 与重定价周期）。
- 证据链覆盖：斜率（近若干交易日累计变动、单日最大变动）；期限结构（3M/6M/1Y 利差、是否倒挂）；政策约束（Fed 票型、下次决议与 SEP、AED 钉住）；银行资金成本溢价（EIBOR − Base Rate）。
- 三情景：只给可观测触发条件、EIBOR 路径、K01 判定、对公寓市场的影响；不赋概率。
- 反向校准：「没有数据」写成可核验陈述（如"核对公报目录共 38 张表，无该分项"）；盲区按「方向确定、幅度未知」处理。

---

## 十、政策框架复核清单（年度，G01–G05）

| 编号 | 政策项 | 官方入口 |
|---|---|---|
| G01 | 黄金签证房产门槛 | `https://u.ae/` |
| G02 | CBUAE 按揭 LTV 规则 | `https://centralbank.ae/en` |
| G03 | DLD 过户费与交易成本 | `https://dubailand.gov.ae/en/` |
| G04 | 期房资金托管 / Oqood | `https://dubailand.gov.ae/en/eservices/` |
| G05 | RERA 租金涨幅规则与 90 天通知 | `http://dubailand.gov.ae/en/frequently-asked-questions` |

规则：未取得官方英文条款页的标「未核验」，禁止引用商业中介网站数值；入口页 ≠ 条款页；任一变更 → 立即重算需求情景。

**政策乘数表（G01–G05，2026-11-14 起）**：每项政策维护「工具 → 中间目标 → 最终目标 → 时滞 → 乘数」链条。

- 数据源：`data/processed/economy/dubai/apartment/quant_policy_multipliers.csv`；工具：`engine/tools/policy_multiplier.py`。
- 硬规则：状态非「已核验」不得给乘数数值，只给 `reference_range`（文献/经验，未经本地回测）。
- 当前核验覆盖率：**1/5（20%）**（G05 已核验；G01–G04 未核验，见 `engine/report-audits/blind-spot-ledger.md` B05）。
- 目标：Phase 1 末 ≥4/5（80%）。

---

## 十一、口径冲突并列清单（年度第 4 节实例化）

- 成交量：Savills / Cavendish Maxwell / Springfield-DLD / DLD 全物业
- 交付：C&W Core / Cavendish Maxwell / ValuStrat
- 价格：Savills 均价 / 同质化 / PropertyIndex 中位 / PIX / ValuStrat VPI
- 收益率：DRED / Peak Trust / Cavendish Maxwell
- GDP/CPI：CBUAE / IMF / DDSE
- 顶级公寓：Savills 与 ValuStrat prime 方向相反（数值取自台账）

---

## 十二、渲染差异（相对通用规范的实例化）

- **导航基址**：`.nav-url` 链接 = `{{REPO_RAW_URL_BASE}}` + `/reports/{本期文件名}`。
- **关键数字卡**：月度 8 张；年度 8 张；季度 10–13 张。
- **图表清单**：月度至少 4 张（利率路径 / 租金结构 / 价格口径对照 / 利率敏感性）；季度至少 7 张（成交量结构 / 年度交付 / 续约租金结构 / 利率—收益率—通胀相对位置 / EIBOR 双阈值 / 红线归一化距离 / 次年供给情景）；基线至少 5 张（价格走势 / 成交量 / 续约结构 / 分区收益率 / FDI 序列）；年度 2–3 张配套图。
- **台账新版工作表（年度）**：9 个 — 看板 / 指标台账 / 预警红线 / 官方来源清单 / 监测日历 / 信号规则 / 首期基线值 / 年度基线 / 使用说明。
- **未核验清单下限（年度第 7 节）**：至少 8 项。

---

## 十三、信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层（逻辑）/ 原始层（台账与来源）；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：四级标注与摘要引用约束见 `engine/templates/information-layering-spec.md` 第二 / 四节；market-sizing 数值按同规范标「假设乘积」并区间化。
- **新增信息模块**：四要素模板见 `engine/templates/information-layering-spec.md` 第四节。
- **指针引用**：事实唯一定义于指标台账 / 事实卡片（`[FC-…]`），正文用「指标编号 + 指针」（K01–K15、RL-01–RL-09、G01–G05）。
- **决策卡与行动协议**：决策卡字段与行动项五要素见 `engine/templates/decision-delivery-spec.md` 第一 / 三节。
- **阈值校准**：首次中期回测 **2027-06**（提前于原计划 2027-12）；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节。
- **场景切片**：主场景 **投资决策**；次场景 **政策制定**。
- **影响分级**：`impact_tier = high`（高影响，强制披露矩阵见 `engine/templates/information-layering-spec.md` §七）。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「**本期读数时点**」；仅核心事实修正才升级版本号。
- **盲区**：P0 四类（就业 / 收入 / 空置 / 竣工）优先消号，台账 `engine/report-audits/blind-spot-ledger.md`。

---

<!-- VOCAB-SYNC:BEGIN topic=economy do-not-edit -->
## 词汇速览（词汇库自动同步）

> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 economy v1.5，共 55 条（同步于 2026-11-18T20:19:11）。标记区间内请勿手工编辑；词条变更走词汇库导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。

- **宏观与经济指标**（11）：CPI（消费者价格指数、Consumer Price Index）；核心CPI（Core CPI、核心消费者价格指数）；PPI（生产者价格指数、Producer Price Index）；GDP（国内生产总值、Gross Domestic Product）；PMI（采购经理人指数、Purchasing Managers' Index）；失业率（Unemployment Rate）；非农就业（Nonfarm Payrolls、NFP）；基准利率（政策利率、Policy Rate）；通胀率（Inflation、通货膨胀率）；收益率曲线（Yield Curve、利率期限结构）；贷款市场报价利率（LPR、Loan Prime Rate）
- **金融机构与组织**（8）：美联储（Federal Reserve、FED、美国联邦储备系统）；欧洲央行（ECB、European Central Bank）；中国人民银行（PBOC、央行）；国际货币基金组织（IMF、International Monetary Fund）；世界银行（World Bank、WB）；国际清算银行（BIS、Bank for International Settlements）；FOMC（联邦公开市场委员会、Federal Open Market Committee）；主权财富基金（Sovereign Wealth Fund、SWF）
- **金融工具与产品**（10）：国债（政府债券、Government Bond、Treasury）；EIBOR（Emirates Interbank Offered Rate、迪拜银行间同业拆借利率）；SOFR（担保隔夜融资利率、Secured Overnight Financing Rate）；LIBOR（伦敦银行间同业拆借利率、London Interbank Offered Rate）；掉期（互换、Swap）；利率互换（IRS、Interest Rate Swap）；期货（Futures）；期权（Options）；ETF（交易所交易基金、Exchange-Traded Fund）；REIT（房地产投资信托、Real Estate Investment Trust）
- **市场机制与交易**（9）：流动性（Liquidity）；做市商（Market Maker）；卖空（Short Selling、做空）；杠杆（Leverage）；保证金（Margin）；IPO（首次公开募股、Initial Public Offering）；市值（Market Capitalization、Market Cap）；基点（Basis Point、bp、bps）；成交（成交量、Transaction Volume）
- **估值与风险**（7）：市盈率（P/E、Price-to-Earnings Ratio）；市净率（P/B、Price-to-Book Ratio）；股息率（Dividend Yield）；风险溢价（Risk Premium）；信用评级（Credit Rating）；在险价值（VaR、Value at Risk）；波动率指数（VIX、恐慌指数）
- **监管与政策**（10）：量化宽松（QE、Quantitative Easing）；量化紧缩（QT、Quantitative Tightening）；巴塞尔协议III（Basel III、巴塞尔III）；反洗钱（AML、Anti-Money Laundering）；KYC（了解你的客户、Know Your Customer）；宏观审慎评估（MPA、Macroprudential Assessment）；阈值（Threshold、临界值）；台账（Ledger、登记册）；预校准（ex-ante、事前校准）；决策卡（Decision Card）
<!-- VOCAB-SYNC:END -->

## 十四、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从四份周期提示词中抽离业务共享配置（变量、来源、口径、K/RL 阈值、触发器、渲染差异），集中为单一事实源 |
| v1.1 | 2026-11-13 | 台账切换 | 年度复盘完成、v2.0 新版台账（registry_2027-01.xlsx）生效后，按 operations-guide 4.4 将 `{{REGISTRY_PATH}}` 语义切换到新版；旧版台账保留不删 |
| v1.2 | 2026-11-13 | 词汇库绑定机制 | 接入 `engine/vocabulary/script/sync_vocab.py` 自动同步：新增「词汇速览（词汇库自动同步）」标记区间，由脚本维护（金融市场宏观指标、利率与机构术语的速览源，与第三节术语口径区分互为补充）；区间外内容不受同步影响 |
| v1.3 | 2026-11-14 | 量化研究体系接入 | 新增 K 系三层重组（领先/同步/滞后）与政策乘数表（G01–G05）节；接入 `engine/tools/signal_synth.py`、`policy_multiplier.py`；版本记录保留 |
