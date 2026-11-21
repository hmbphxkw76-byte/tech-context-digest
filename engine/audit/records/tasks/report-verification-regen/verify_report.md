# 全量报告核验台账（2026-11-22）

口径：报告内引用（含行内链接与纯文本 URL）→ `source_registry.json` 登记与 `verify_status`；
信息等级（已核验/部分核验/推断/假设）不得高于来源核验状态上限（`verification_vocab.is_consistent`）。

## 结论

- 22 份报告全部通过 `optimization_gate`（5 项警告，均为既有非阻断项）。
- 块级「信息等级 vs 来源核验状态」一致性检查：**0 处越标**。
- **无需删除的报告**：无报告的核心结论依赖无法核验的来源。
- 处置：补登记 `content/education/study-abroad` 40 个官方来源（web_fetch 逐条核验，3 条抓取失败标 `unverifiable`）；
  补录 26 个机构分级主数据；核验台账追加 40 条事件（527 verified / 84 status_changed，链校验通过）。

## 逐报告

| 报告 | 业务线 | 引用来源 | 已核验 | 部分核验 | 未核验 | 未登记 | 处置 |
|---|---|---|---|---|---|---|---|
| `content/economy/dubai/apartment/reports/2026-11_baseline_report.html` | content/economy/dubai/apartment | 26 | 22 | 2 | 0 | 0 | 保留 |
| `content/economy/dubai/apartment/reports/2026-11_monthly.html` | content/economy/dubai/apartment | 27 | 24 | 0 | 0 | 0 | 保留 |
| `content/economy/dubai/apartment/reports/2026-Q3_quarterly.html` | content/economy/dubai/apartment | 14 | 11 | 0 | 0 | 0 | 保留 |
| `content/economy/dubai/apartment/reports/2026_annual.html` | content/economy/dubai/apartment | 30 | 27 | 0 | 0 | 0 | 保留 |
| `content/economy/insight/reports/2026-11_baseline_report.html` | content/economy/insight | 2 | 0 | 0 | 0 | 0 | 保留 |
| `content/economy/trends/reports/2026-11-13_weekly.html` | content/economy/trends | 32 | 23 | 6 | 0 | 0 | 保留 |
| `content/economy/trends/reports/2026-11-20_weekly.html` | content/economy/trends | 32 | 23 | 6 | 0 | 0 | 保留 |
| `content/economy/trends/reports/2026-11-27_weekly.html` | content/economy/trends | 33 | 24 | 6 | 0 | 0 | 保留 |
| `content/education/education-system/reports/2026-11_baseline_report.html` | content/education/education-system | 27 | 25 | 0 | 0 | 0 | 保留 |
| `content/education/study-abroad/reports/2026-11_baseline_report.html` | content/education/study-abroad | 68 | 62 | 2 | 3 | 0 | 保留 |
| `content/international/immigration/dubai/reports/2026-11_baseline_report.html` | content/international/immigration/dubai | 12 | 9 | 1 | 1 | 0 | 保留 |
| `content/international/immigration/reports/2026-11_baseline_report.html` | content/international/immigration | 52 | 37 | 14 | 0 | 0 | 保留 |
| `content/international/international-relations/reports/2026-11_baseline_report.html` | content/international/international-relations | 31 | 29 | 0 | 0 | 0 | 保留 |
| `content/political/political-system/reports/2026-11_baseline_report.html` | content/political/political-system | 19 | 12 | 0 | 5 | 0 | 保留 |
| `content/society/social-structure/reports/2026-11_baseline_report.html` | content/society/social-structure | 18 | 10 | 0 | 6 | 0 | 保留 |
| `content/tech/ai-application/competitive-intelligence/dubai/reports/2026-11_baseline_report.html` | content/tech/ai-application/competitive-intelligence/dubai | 32 | 24 | 6 | 0 | 0 | 保留 |
| `content/tech/ai-application/dubai/reports/2026-11_baseline_report.html` | content/tech/ai-application/dubai | 34 | 32 | 0 | 0 | 0 | 保留 |
| `content/tech/ai-application/industry-research/dubai/reports/2026-11_baseline_report.html` | content/tech/ai-application/industry-research/dubai | 23 | 20 | 1 | 0 | 0 | 保留 |
| `content/tech/ai-security/competitive-intelligence/dubai/reports/2026-11_baseline_report.html` | content/tech/ai-security/competitive-intelligence/dubai | 47 | 34 | 11 | 0 | 0 | 保留 |
| `content/tech/ai-security/competitive-intelligence/dubai/reports/2026-11_monthly.html` | content/tech/ai-security/competitive-intelligence/dubai | 48 | 34 | 11 | 0 | 0 | 保留 |
| `content/tech/ai-security/dubai/reports/2026-11_baseline_report.html` | content/tech/ai-security/dubai | 44 | 36 | 5 | 1 | 0 | 保留 |
| `content/tech/ai-security/industry-research/dubai/reports/2026-11_baseline_report.html` | content/tech/ai-security/industry-research/dubai | 39 | 32 | 4 | 1 | 0 | 保留 |

> 注：`content/economy/insight` 为 `synthesis_only` 跨线仪表盘，按设计不引用外部 URL（来源追溯走 `[FC-…]` 事实卡片）。
> 全量 22 份报告的引用来源登记覆盖率 = 100%（0 条未登记）。
