# 社会结构与分层 · 指标台账（md-ledger）

> **定位**：`content/society/social-structure` 业务线的活值登记载体（业务配置 `{{REGISTRY_PATH}}`）。运行前读 → 核验 → 运行后回写；prompt 模板内严禁预填活值。
> **格式**：md-ledger。台账修改采用增量方式：报告层补充与台账更新严格区分。
> **状态**：首期基线已播种（2026-11 基线运行）。

---

## 一、数据看板追踪表（年报 / 事件解读联动）

| 指标 | 上期值 | 本期值 | 变化 | 来源 | 口径 | 是否更新 |
| --- | --- | --- | --- | --- | --- | --- |
| K01 人口自然增长 | — | 未触发（世界 82 亿；63 国已达峰） | 基线 | UN WPP 2024 https://population.un.org/wpp/ | 出生 / 死亡 / 迁移口径并列 | 是 |
| K02 家庭户数与结构 | — | 未触发（韩国单人家庭 42.27%） | 基线 | 韓国行政安全部 https://www.mois.go.kr/ | 家庭户 ≠ 人口；常住 / 户籍分列 | 是 |
| K03 收入不平等（基尼） | — | 未触发 | 基线 | OECD https://data.oecd.org/inequality/income-inequality.htm | 可支配收入口径；基尼 ≠ 五等分比 | 是 |
| K04 老龄化率 | — | 未触发（中国 15.6%；日本约 29.3%；韩国 21.21%） | 基线 | stats.gov.cn / stat.go.jp / mois.go.kr | 65+ 占比 ≠ 总抚养比 | 是 |
| K05 城镇化率 | — | 未触发（世界城市人口约 45%） | 基线 | UN WUP 2025 https://population.un.org/wup/ | 城乡定义须注明 | 是 |
| K06 社会保障覆盖率 | — | 未触发 | 基线 | ILO https://ilostat.ilo.org/ | 覆盖率 ≠ 支出占比；分险种并列 | 是 |
| K07 失业率 / 劳动参与 | — | 未触发 | 基线 | ILOSTAT https://ilostat.ilo.org/ | ILO 口径 ≠ 自报口径 | 是 |
| K08 教育获得与流动 | — | 未触发 | 基线 | UNESCO / OECD | 测量方法须注明 | 是 |
| RL-01 人口结构 | — | 未触发 | 基线 | UN WPP 2024 | 人口连续 2 年负增长 | 是 |
| RL-02 收入分配 | — | 未触发 | 基线 | OECD | 基尼 >0.45 连续 2 年 | 是 |
| RL-03 老龄化 | — | 未触发 | 基线 | 国家统计 / UN WPP | 65+ 占比 >28% 或总抚养比 >60% | 是 |
| RL-04 社会保障 | — | 未触发 | 基线 | ILO / 各国主管机关 | 主要险种覆盖率 <50% | 是 |
| RL-05 就业 | — | 未触发 | 基线 | ILOSTAT / 自报口径 | 失业率高企且参与率持续下降 | 是 |
| G01 人口与家庭政策 | — | 已登记 | 基线 | stats.gov.cn / stat.go.jp / KOSIS | 事件触发 + 年度 | 是 |
| G02 收入分配与税收 | — | 已登记 | 基线 | OECD / 各国统计局 | 年度 | 是 |
| G03 社会保障与福利 | — | 已登记 | 基线 | ILO / 各国主管机关 | 事件触发 + 年度 | 是 |
| G04 城市化与社区 | — | 已登记 | 基线 | UN-Habitat / UN WUP | 年度 | 是 |
| G05 风险与公共危机 | — | 已登记 | 基线 | WHO / 各国应急主管机关 | 事件触发 + 年度 | 是 |
| UN WPP 2024 | — | 世界人口 82 亿（2024），2080s 中期达峰约 103 亿 | 基线 | https://population.un.org/wpp/ | 第 28 版；中位估计 | 是 |

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
| 1 | 中国国家统计局 | P0 | https://www.stats.gov.cn/ | 已核验（入口） |
| 2 | 日本総務省統計局 | P0 | https://www.stat.go.jp/ | 已核验（入口） |
| 3 | 韓国 統計庁 KOSIS | P0 | https://kosis.kr/ | 已核验（入口） |
| 4 | 韓国 行政安全部 | P0 | https://www.mois.go.kr/ | 已核验（入口） |
| 5 | UN World Population Prospects 2024 | P1 | https://population.un.org/wpp/ | 已核验 |
| 6 | UN World Urbanization Prospects 2025 | P1 | https://population.un.org/wup/ | 已核验 |
| 7 | OECD Income Distribution Database | P2 | https://data.oecd.org/inequality/income-inequality.htm | 已核验（入口） |
| 8 | OECD Data | P2 | https://data.oecd.org/ | 已核验（入口） |
| 9 | World Bank WDI | P2 | https://data.worldbank.org/ | 未核验（入口） |
| 10 | ILOSTAT | P2 | https://ilostat.ilo.org/ | 已核验（入口） |
| 11 | UN Data | P2 | http://data.un.org/ | 未核验 |
| 12 | 国立社会保障・人口問題研究所 | P2 | https://www.ipss.go.jp/ | 未核验 |
| 13 | UN DESA | P4 | https://www.un.org/en/desa/ | 未核验 |
| 14 | WHO | P4 | https://www.who.int/ | 未核验 |
| 15 | UN-Habitat | P4 | https://unhabitat.org/ | 未核验 |
