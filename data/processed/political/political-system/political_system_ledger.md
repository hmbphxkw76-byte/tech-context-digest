# 政治制度与治理 · 指标台账（md-ledger）

> **定位**：`content/political/political-system` 业务线的活值登记载体（业务配置 `{{REGISTRY_PATH}}`）。运行前读 → 核验 → 运行后回写；prompt 模板内严禁预填活值。
> **格式**：md-ledger。台账修改采用增量方式：报告层补充与台账更新严格区分。
> **状态**：首期基线已播种（2026-11 基线运行）。

---

## 一、数据看板追踪表（年报 / 事件解读联动）

| 指标 | 上期值 | 本期值 | 变化 | 来源 | 口径 | 是否更新 |
| --- | --- | --- | --- | --- | --- | --- |
| K01 选举与投票率 | — | 未触发 | 基线 | 総務省選挙部 https://www.soumu.go.jp/senkyo/ | 选举制度 / 政党制度分列；投票率 ≠ 得票率 | 是 |
| K02 议会构成与席位 | — | 未触发（日本 465 / 248；英国 650；美国 435 / 100；德国基本 598） | 基线 | 衆議院 / 参議院 / parliament.uk / congress.gov / bundestag.de | 法定定额与实际议席并列 | 是 |
| K03 宪法 / 司法改革 | — | 未触发 | 基线 | 衆議院 / bundestag.de | 文本规定 / 实际运行分列 | 是 |
| K04 行政区划与地方分权 | — | 未触发 | 基线 | 各国政府官方站 | 中央 / 地方事权分列 | 是 |
| K05 廉政与透明度 | — | 未触发（CPI 0–100，约 180 经济体） | 基线 | Transparency International https://www.transparency.org/en/cpi | 廉政指数 ≠ 腐败案件数 | 是 |
| K06 公民社会与集会 | — | 未触发 | 基线 | UN OHCHR https://www.ohchr.org/ | 结社 / 集会 / 媒体自由度分列 | 是 |
| K07 政府组建与不信任案 | — | 未触发 | 基线 | 日本衆議院 https://www.shugiin.go.jp/ | 内阁改组 / 不信任案 / 政府解散分列 | 是 |
| K08 数字治理与数据制度 | — | 未触发（EGDI 落后人口 45.0%→22.4%） | 基线 | UN E-Government Survey https://publicadministration.un.org/egovkb/en-us/ | 版本 + 提取日期 | 是 |
| RL-01 宪政体制 | — | 未触发 | 基线 | 衆議院 / bundestag.de | 修宪变更权力结构或任期规则 | 是 |
| RL-02 选举制度 | — | 未触发 | 基线 | 総務省選挙部 | 选举法实质变更或选举取消 | 是 |
| RL-03 廉政治理 | — | 未触发 | 基线 | Transparency International | 系统性廉政倒退（指数与案件双证） | 是 |
| RL-04 公民社会 | — | 未触发 | 基线 | UN OHCHR | 结社 / 集会 / 媒体自由事实上受限 | 是 |
| RL-05 司法独立 | — | 未触发 | 基线 | bundestag.de | 宪法法院 / 司法机构重组或权限变更 | 是 |
| G01 选举制度与选举日历 | — | 已登记 | 基线 | 総務省選挙部 | 事件触发 + 年度 | 是 |
| G02 议会与立法程序 | — | 已登记 | 基线 | 衆議院 / 参議院 / Bundestag / parliament.uk | 事件触发 + 年度 | 是 |
| G03 行政区划与地方治理 | — | 已登记 | 基线 | 各国政府官方站 | 事件触发 + 年度 | 是 |
| G04 廉政与透明度 | — | 已登记 | 基线 | Transparency International | 年度 | 是 |
| G05 司法与宪法 | — | 已登记 | 基线 | bundestag.de / 各国法律数据库 | 事件触发 + 年度 | 是 |
| V-Dem Dataset | — | v16（2026-03 发布，531 指标 / 251 指数） | 基线 | https://www.v-dem.net/data/the-v-dem-dataset/ | 版本 + 提取日期 | 是 |

> K01–K08、RL-01–RL-05、G01–G05 的活值与阈值状态在此维护；阈值为 ex-ante 预校准，回测窗口 2027-06。

## 二、已修正事实清单（首期为空，产生修正后逐条补记）

```
【已修正事实清单 — 首期为空，产生修正后逐条补记，格式如下】
- ❌ 不得再称"…"——正确结论为…。[Source: URL, 年份]
```

- 防回退规则：每次运行前必须完整继承本清单；与清单冲突的旧结论不得复活。
- 首期（2026-11）：无修正条目。

## 三、来源清单（持续维护）

| # | 来源 | 层级 | 官方 URL | 状态 |
|---|---|---|---|---|
| 1 | 日本衆議院 | P0 | https://www.shugiin.go.jp/ | 已核验（入口） |
| 2 | 日本参議院 | P0 | https://www.sangiin.go.jp/ | 已核验（入口） |
| 3 | 総務省選挙部 | P0 | https://www.soumu.go.jp/senkyo/ | 已核验（入口） |
| 4 | 德国联邦议院 | P0 | https://www.bundestag.de/en | 已核验（入口） |
| 5 | 英国议会 | P0 | https://www.parliament.uk/ | 已核验（入口） |
| 6 | 美国国会 | P0 | https://www.congress.gov/ | 已核验（入口） |
| 8 | V-Dem Institute / Dataset | P1 | https://www.v-dem.net/data/the-v-dem-dataset/ | 已核验 |
| 9 | Transparency International · CPI | P1 | https://www.transparency.org/en/cpi | 已核验 |
| 10 | UN E-Government Survey | P2 | https://publicadministration.un.org/egovkb/en-us/ | 已核验 |
| 11 | OECD Government at a Glance | P2 | https://www.oecd.org/en/publications/government-at-a-glance.html | 未核验（入口） |
| 12 | World Bank WGI | P2 | https://www.worldbank.org/en/publication/worldwide-governance-indicators | 未核验（入口） |
| 13 | International IDEA | P4 | https://www.idea.int/ | 未核验 |
| 14 | IPU | P4 | https://www.ipu.org/ | 未核验 |
| 15 | Freedom House | 线索 | https://freedomhouse.org/ | 仅作线索，须回官方核验 |
