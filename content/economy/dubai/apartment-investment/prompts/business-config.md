# 迪拜公寓住宅市场投资分析 · 业务专属配置（business-config）

> **定位**：本文件是 `content/economy/dubai/apartment-investment` 业务线的**单一业务事实源**：运行变量固定值、来源优先级实例化、术语口径、受众定位、投资监测阈值（I 系 / 引用 K·RL 系）、标的档案结构、仓库链接基址全部集中于此。周期提示词（基线 / 标的复核）引用本文件，业务参数只在这里维护一份。
>
> **继承声明（四层体系）**：周期提示词 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [类型模板](../../../../../engine/templates/investment-research/)（投资分析与尽调型）× 本文件。通用层修改自动对本业务线生效；本文件修改只影响本业务线。冲突时以周期提示词 ＞ 本文件 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、运行变量固定值

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = 公寓住宅市场投资分析
{{REPORT_TYPE}}          = investment-research
{{BASELINE_DATE}}        = 2026-11-26（基线报告完稿日期）
{{REGISTRY_PATH}}        = data/processed/economy/dubai/apartment-investment/dubai_apartment_investment_registry.md
{{REGISTRY_FORMAT}}      = md-table
{{SOURCE_REGISTRY_PATH}} = data/processed/economy/dubai/apartment-investment/source_registry.json
{{BASELINE_REPORT_PATH}} = reports/2026-11_baseline_report.html
{{FRESHNESS_PRIORITY}}   = 最新官方页 > 上期值 > 预测值（本项目时效优先级）
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/economy/dubai/apartment-investment
```

**各周期落盘规则**（投资分析与尽调型类型模板第一 / 七节的实例化）：

| 节拍 | 输出路径 | 定位 | 上期报告 |
|---|---|---|---|
| 基线 | `reports/2026-11_baseline_report.html`（md 源稿同目录同名） | 首次覆盖，对比锚，常驻顶层 | 无 |
| 季度复核 | `reports/{{YYYY-Qn}}_quarterly.html` | 定期复核（事件核验 → 假设复核 → 估值更新 → 结论修订） | 基线 + 最近一期复核 |
| 年度复核 | `reports/{{YYYY}}_annual.html` | 年度全面复核 + 模型再校准检查 | 基线 + 最近一期复核 |
| 事件触发专项 | `reports/{{YYYY-MM-DD}}-<slug>.html` | 重大政策 / 市场冲击的结论修订件 | 基线 + 最近一期复核 |

**输出格式**：md 源稿 + 同目录自包含 HTML（`python engine/tools/md2html.py` 同步生成），双格式交付为默认，不适用纯图表例外。

---

## 二、受众定位

面向**拟赴迪拜置业 / 持有公寓资产的投资者**（含人民币投资者视角：AED 钉住美元，本质是美元资产），兼具组合配置与风险预警视角。报告允许给出**条件化框架结论**（估值区间、情景、触发条件），但遵守通用基座第三节第 5 条：不给出具体买卖价位、杠杆比例、仓位建议；报告声明「不构成对不特定公众的投资邀约」，不构成法律、税务或投资顾问意见。

与既有 `content/economy/dubai/apartment`（市场指标监测型）分工：该线管**市场数据监测**（价格 / 成交 / 租赁 / 供给信号），本线管**投资决策输入**（估值、情景、风险与结论修订），两线共享来源体系与台账口径，本线不重复监测明细，只做投资视角的收敛与再解释。

---

## 三、术语口径区分（表格与正文中不得混用）

- 均价 ≠ 中位价 ≠ 混合调整指数（成交结构效应）；挂牌 ≠ 成交；期房 ≠ 一手；转售 ≠ 现房。
- 毛收益率 ≠ 净收益率（净口径仅扣物业费；cap rate 另计持有成本与空置）。
- **资本化率（cap rate）= 净营运收入 / 资产价值**，与「登记口径毛收益率」不是同一指标，禁止互换。
- 全市住宅 ≠ 公寓专属；迪拜酋长国 ≠ UAE 联邦。
- 豪宅门槛口径：Savills `> AED 10m` 与 Knight Frank `> US$10m`（约 AED 36.7m）不是同一门槛，禁止直接比较。
- **AED 钉住美元**：1 USD = 3.6725 AED（CBUAE 官方汇率安排）；对人民币投资者的汇率风险实质是 USD/CNY，正文涉及汇率换算只作参考，不作结论依据。

---

## 四、来源优先级（通用基座第四节的实例化，冲突时报双份并标注）

① 官方一手：CBUAE、Federal Reserve、U.S. EIA、Dubai DET / Media Office、DLD / Dubai Pulse、Digital Dubai / DDSE、Dubai Statistics Centre、Dubai Municipality、UNCTAD、IMF、RERA / DLD 法规与费率页
＞ ② 行业机构：Savills、CBRE、JLL、Cushman & Wakefield Core、Cavendish Maxwell、ValuStrat、Knight Frank、Peak Trust、DXBinteract、Property Monitor、PropertyIndex、DRED
＞ ③ 挂牌门户：Bayut、Property Finder（仅作卖方预期，不得替代成交 / 登记数据）
＞ ④ 媒体转述：Zawya、Reuters、Khaleej Times、Gulf News、The National（须标「需核实原文」，不得与官方一手同等处理）

**机构获取优先级 P0–P5**（估值输入选择）：

| 层级 | 渠道 | 使用规则 |
|---|---|---|
| P0 | CBRE / JLL / Knight Frank 官方研究页与 PDF | 可直接采信，标「已核验」 |
| P1 | 官方 PDF / 报告下载（DLD / CBUAE / EIA / IMF / UNCTAD） | 记录发布日期、页码、口径 |
| P2 | 官方研究订阅 / 新闻稿 | 用于第一时间获取新报告 |
| P3 | 英文媒体 | 只用于发现线索；数值标「需核实原文」，再回官方页 / PDF 校验 |
| P4 | 其他英文行业机构（ValuStrat / Cavendish Maxwell / Peak Trust / DXBinteract / PropertyIndex） | 交叉验证方向；不替代 P0 |
| P5 | DLD 官方锚（transactions / rent contracts / units / price index） | 最终裁决成交量、租金、存量口径 |

**来源语言规则**：仅英文（{{SOURCE_LANGUAGE_RULE}}），严禁中文来源；若某数据点仅在中文源出现，标注「未找到英文权威来源，已剔除」并说明。政策见 `engine/docs/source-language-policy.md`（门禁 `source_check` R9）。

---

## 五、投资监测指标与阈值（I01–I08，ex-ante 预校准）

> 阈值为本项目自设（非官方）；运行前以 `{{REGISTRY_PATH}}`「监测阈值」表为准。与公寓监测线共享的 K 系 / RL 系编号不在此重复，正文以指针引用（K01–K15、RL-01–RL-09）。首次中期回测 **2027-06**；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节（指针，不复述）。

| 编号 | 监测对象 | 口径 | 绿灯 | 黄灯 | 预警红线 | 硬红线 |
|---|---|---|---|---|---|---|
| I01 | 3M EIBOR | % | <3.50% 或连续 3 月下行 | 3.50–4.50% 横盘 | >4.35% 或 3 月累计上行 >40bp | >4.50% 或 3 月上行 >50bp |
| I02 | 登记口径毛收益率（中位） | % | >7.0% | 6.0–7.0% | <6.0% | <5.5% |
| I03 | 公寓价格同比（PIX / ValuStrat VPI 并列） | % | >+3% | −3%～+3% | <−3% 连续 2 月 | <−5% 连续 3 月 |
| I04 | 成交量同比（DLD 口径） | % | >−10% | −10%～−20% | <−20% | <−30% 连续 2 季 |
| I05 | 毛净收益率差（持有成本代理） | pp | <1.2pp | 1.2–1.8pp | >1.8pp | >2.2pp 连续 2 期 |
| I06 | 交付兑现率 | % | >65% | 50–65% | <50% | <45% 且计划量创高 |
| I07 | 许可建筑面积同比（供给先行） | % | <0% | 0–20% | >20% 单季 | >30% 连续 2 季 |
| I08 | 租金同比（Ejari / 登记口径） | % | >+5% | 0～+5% | <−5% 连续 2 月 | <−8% 连续 3 月 |

**三层归属**：领先 I01 / I07；同步 I02 / I03 / I04 / I08；滞后 I05 / I06。任一硬红线触发 → 重算情景与估值区间，结论降级复核。

---

## 六、标的档案结构（{{REGISTRY_PATH}}，md-table）

标的 = **迪拜公寓资产类别（市场级标的，非单一开发商 / 项目）**。档案首建于基线运行，含五张表：

1. **标的概况表**：资产类别定义、产权制度（freehold / leasehold 区域口径）、交易机制（DLD 过户、Oqood、按揭 LTV）、政策门槛（黄金签证房产门槛 AED 2,000,000）。
2. **市场序列表**：价格 / 成交 / 租金 / 供给 / 融资成本的关键读数（指标编号 + 值 + 时点 + 来源）。
3. **估值假设表**：收益法（cap rate、空置率、持有成本、租金增速）与可比法（价格租金比、相对指数）全假设逐条列示，每格附 `[来源, 时点]`。
4. **风险登记表**：风险 / 触发条件 / 影响量级 / 缓解依赖（与报告第五节同步）。
5. **追踪表**：监测项 × 信息渠道 × 当前状态（I01–I08 + K/RL 指针）。

> prompt 模板内严禁填写活值；每格活值附 `[来源, 时点]`，未核实项注明「待核实」，不补值、不外推。

---

## 七、已修正事实清单（基线锚，防回退；无来源不得追加）

```
- 首期为空；后续运行产生修正后逐条补记（格式：❌ 不得再称「旧说法」——实际为「新说法」。[Source: URL, 年份]）。
```

---

## 八、八节结构固化锚

基线报告 `reports/2026-11_baseline_report.html` 八节结构为该业务线固化锚，后续报告逐字继承：

1. 投资要点（决策摘要）｜2. 标的概况｜3. 行业与市场输入｜4. 财务分析与估值模型｜5. 风险清单｜6. 情景与敏感性｜7. 合规与边界｜8. 参考来源清单

---

## 九、信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：四级标注与摘要引用约束见 `engine/templates/information-layering-spec.md` 第二 / 四节；新增信息统计模块见第四节。
- **指针引用**：事实唯一定义于指标台账 / 事实卡片（`[FC-…]`），正文用「指标编号 + 指针」（I01–I08、K01–K15、RL-01–RL-09、G01–G05）。
- **决策卡与行动协议**：决策卡字段与行动项五要素见 `engine/templates/decision-delivery-spec.md` 第一 / 三节；三档优先级（立即行动 / 持续观察 / 仅记录存档）。
- **阈值校准**：首次中期回测 **2027-06**；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节。
- **场景切片**：主场景 **投资决策**；次场景 **置产研究 / 比较**。
- **影响分级**：`impact_tier = high`（高影响，强制披露矩阵见 `engine/templates/information-layering-spec.md` §七）。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」；仅核心事实修正才升级版本号。
- **盲区**：沿用 `engine/report-audits/blind-spot-ledger.md` P0 四类（就业 / 收入 / 空置 / 竣工），投资视角新增盲区：净收益率口径、持有成本明细、美元 / AED 汇率路径（均在报告第五节与 registry 待核实清单显式披露）。

---

## 十、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-26 | 初始版本 | 建立投资分析业务线：运行变量、来源优先级实例化、术语口径（cap rate / 收益率 / 门槛）、I01–I08 投资监测阈值、标的档案结构、八节固化锚；节拍为基线 + 季度 / 年度复核 + 事件触发专项 |
