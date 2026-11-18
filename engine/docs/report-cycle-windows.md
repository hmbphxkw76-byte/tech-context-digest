# 报告周期与展示窗口规范（REPORT-CYCLE-WINDOWS-SPEC v1.0）

> **状态**：现行规范
> **文档定位**：月 / 季 / 年 / 周报的**保留窗口、hub 展示窗口与环比高亮**唯一事实源；生成器（`build_hub.py`）、归档器（`archive_reports.py`）与页面组件均以此为准。
> **配套**：页面组件标准见 [page-build-spec.md](page-build-spec.md)；归档与发布链路见 [report-pipeline-system.md](report-pipeline-system.md) §N7。
> **最后更新**：2026-11-18

---

## 一、周期窗口

| 周期 | 保留（月） | hub 直接展示 | 「更多」折叠 | 环比高亮 |
|---|---|---|---|---|
| 月度 `monthly` | 近 **18** 个月 | 最近 **6** 个月 | 6–18 个月部分，点开完整展示 | 最新一期 |
| 季度 `quarterly` | 近 **24** 个月 | 全部（8 期） | 无 | 最新一期 |
| 年度 `annual` | 近 **60** 个月 | 最近 **5** 份 | 无 | 最新一期 |
| 基线 `baseline` | 常驻 | 全部 | 无 | 不参与（对比锚） |
| 周报 `weekly` | 近 12 期 | 全部（按周单独展示） | 无 | 不参与 |

- **保留**：`reports/` / `sources/` 内保留的时长，超出由 `archive_reports.py` 滚动归档（`KEEP` 由本表派生：月 18 / 季 8 / 年 5 / 基线 3 / 周报 12）。
- **「更多」**：仅月度使用；折叠块为原生 `<details>/<summary>`，无 JS 也可完整展开，打印前自动展开。

## 二、环比与高亮

- **环比口径**：报告更新一律在**环比**基础上进行；hub 对每个主题、每个参与周期（月 / 季 / 年）的**最新一期**加「本期更新」高亮，hover 显示其环比基期（上一期）。
- **基期滚动**：全局「环比基期」取仓库内**最新一期月报**的 period（当前 `2026-11`）；2027-01 起随 `2026-12` 月报自动滚动为 `2026-12`。其它周期同理（季 / 年取各自最新一期）。
- **无更新保持不变**：非最新一期的报告按普通样式展示，不加高亮。
- **周报例外**：单独按周展示，不环比、不高亮、不折叠。

## 三、窗口锚点与确定性

- 窗口锚点 = **该主题该周期的最新一期 period**（如 `2026-11`），**不取墙钟 / 文件 mtime**，保证 `build_hub.py --check` 确定性（无时间戳）。
- 超出保留窗口的报告由 `archive_reports.py` 归档，hub 不再展示；INDEX.md 作为全量台账索引不受窗口限制。

## 四、单一事实源与落地

| 位置 | 职责 |
|---|---|
| `engine/tools/_common.py` | `CYCLE_WINDOWS` / `HIGHLIGHT_CYCLES` / `CYCLE_ORDER` / `period_months()` / `prev_period()` |
| `engine/tools/build_hub.py` | `group_topic_reports()` 窗口切分；`更多` 折叠；`本期更新` badge；`环比基期` 标注 |
| `engine/tools/archive_reports.py` | `KEEP` 由 `CYCLE_WINDOWS` 派生，滚动归档 |
| `engine/tests/test_tools.py::TestReportCycleWindows` | 窗口 / 高亮 / 归档口径回归 |

## 五、验收

- `python -m unittest engine.tests.test_tools`（含 `TestReportCycleWindows`）通过。
- `python engine/tools/page_build_check.py` 零 `[E]`。
- `python engine/tools/build_hub.py --check` 通过（生成物确定性）。
