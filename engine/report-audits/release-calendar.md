# 发布日历（RELEASE-CALENDAR）

> **状态**：现行台账（每季度复核一次「下次预期窗口」）
> **依据**：[量化研究体系优化实施方案](quant-system-optimization-plan-2026-11-14.md) 第三节 M2
> **机制**：各来源发布时点、滞后、复审日集中管理；接入 `update_planner.py` 生成待办；发布后 T+N 日内入库，漏采触发告警。
> **结构化**：`python engine/tools/release_calendar.py --check` 校验；`--emit` 输出 `release-calendar.json`（由定时维护 / 内容更新写入）。
> **注**：下表「下次预期」为按历史发布规律推算的窗口，非官方公告，须以官方实际发布为准。
> **最后更新**：2026-11-19（E1/F1 定向取数留痕）

| 来源 | 指标 | 频率 | 滞后 | 下次预期窗口 | 入库期限 | 责任人 |
|---|---|---|---|---|---|---|
| CBUAE | 基准利率 / 货币与信贷统计 | 月度 | 5–6 周 | 次月第 4 周 | 发布后 5 日 | 数据采集 |
| CBUAE | 季度经济评论（QER）/ 信贷景气调查 | 季度 | 季末前后 | 季末后 2 周 | 发布后 5 日 | 数据采集 |
| CBUAE / 定盘行 | EIBOR 3M/6M/1Y | 日 | 当日 | 每日 | 每周汇总 | 数据采集 |
| Federal Reserve | FOMC / H.15 / SEP | 事件 | 当日 | 会议日程 | 发布后 2 日 | 数据采集 |
| Dubai LFS（DDSE） | 就业 / 失业率 | 季 | 不定 | 结果发布后 30 日（LFS 2026 于 2026-10-28 启动，结果待发布） | 发布后 10 日 | 数据采集 |
| Dubai LFS（DDSE）/ 薪酬指南（Michael Page / Hays / Robert Half） | 收入 / 薪资中位数 / 行业薪资 | 半年 / 年 | 不定 | 发布后 30 日（LFS 2026 结果待发布；薪酬指南未见 UAE 2026 版） | 发布后 10 日 | 数据采集 |
| DDSE | 人口 / 家庭户数 | 年度 | 约 9 月 | 2027-09 | 发布后 10 日 | 数据采集 |
| Dubai Municipality / DMO | 建筑许可 / 许可面积 / 竣工证书 | 季度（不定期） | 季内 | 季度末后 4 周 | 发布后 10 日 | 数据采集 |
| DLD / Dubai Pulse | 成交 / 租赁 / 单元数据集 | 周 / 月 | 周 / 次月 | 每周 | 发布后 5 日 | 数据采集 |
| CBRE / JLL / Knight Frank | 季度市场报告 | 季度 | 季后 4–6 周 | 季后第 6 周 | 发布后 5 日 | 数据采集 |
| UNCTAD | World Investment Report | 年度 | 次年 6–7 月 | 2027-06/07 | 发布后 15 日 | 数据采集 |
| IMF | WEO / Article IV | 半年 | 不定 | 2027-04/10 | 发布后 15 日 | 数据采集 |
| DET / Media Office | 旅游月度 / 年度数据 | 月 / 年 | 次月 | 次月第 2 周 | 发布后 5 日 | 数据采集 |
| EIA | STEO 月报 | 月 | 当月上旬 | 次月上旬 | 发布后 3 日 | 数据采集 |
| 政策发布方（u.ae / centralbank.ae / dubailand.gov.ae / RERA） | LTV / 黄金签证 / 过户费 / 托管 / 租金规则 | 事件 | 当日 | 持续监测 | 变更后 3 日 | 研究负责人 |
| UNESCO UIS | 教育统计（GER / NER / 教育支出） | 年度 | 不定 | 次年 Q1 | 发布后 15 日 | 数据采集 |
| OECD | Education at a Glance | 年度 | 当年 Q4 | 次年 1 月 | 发布后 15 日 | 数据采集 |
| 各国教育部 / 主管机关 | 教育政策 / 学制 / 互认协议 | 事件 | 当日 | 持续监测 | 变更后 3 日 | 数据采集 |
| UN Treaty Collection | 多边条约签署 / 批准 / 生效状态 | 事件 | 当日 | 持续监测 | 变更后 5 日 | 数据采集 |
| 各国外交部 / 政府 | 外交声明 / 制裁 / 条约 | 事件 | 当日 | 持续监测 | 变更后 3 日 | 数据采集 |
| V-Dem Institute | 治理与民主数据集 | 年度 | 次年 Q1 | 次年 4 月 | 发布后 15 日 | 数据采集 |
| 各国选举委员会 / 议会 | 选举公告 / 议席 / 修法 | 事件 | 当日 | 持续监测 | 变更后 3 日 | 数据采集 |
| UN DESA | World Population Prospects | 两年 | 不定 | 2027 | 发布后 15 日 | 数据采集 |
| ILO / OECD | 劳动与社会保障统计 | 年度 | 不定 | 次年 Q2 | 发布后 15 日 | 数据采集 |

## 校验规则

- P0 来源日历覆盖率 100%（Phase 1 末验收）。
- 每次发布后核对入库状态；漏采写入触发登记。
- 日历每季度复核一次并更新「下次预期窗口」。

## 取数留痕（2026-11-19，E1/F1）

- **Dubai LFS（DDSE）**：DDSE 官方公告 LFS 2026 已启动（2026-10-28，样本 5,000 户），**结果未发布**；「下次预期窗口」与入库期限不变。[Source: https://www.digitaldubai.ae/newsroom/news/digital-dubai-launches-the-labour-force-survey-2026-to-strengthen-data-driven-labour-market-planning-and-decision-making, 2026]
- **Dubai Municipality / DMO（竣工）**：DM 官方仅见法规页，无竣工统计；WAM 转述 DLD 2025 竣工 124 个项目 / AED27.5bn，待 DLD 官方页核验后并入。
- **DLD / Dubai Pulse（空置 / 成交）**：DLD 官网服务入口可达，但未获 2025 年度统计页；ValuStrat / REIDIN 官方正文被反爬拦截，空置序列仍缺。
