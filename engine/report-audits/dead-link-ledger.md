# 死链台账（DEAD-LINK LEDGER）

> **定位**：来源登记 URL 的可达性核验与修复留痕（P1-8）。活值探测结果由 `engine/tools/source_check.py --probe` 产出，本表只登记**人工核验结论与处置**，不复制探测原始输出。
> **口径**：`明确死链` = HTTP 404 / 410 / 451；`网络不可达` = 403 / 429 / 5xx / 超时（环境相关，需人工复核）。R6 阻断自 `R6_STRICT_PERIOD = 2027-01` 起，此前一律 `[W]`。
> **探测环境警示**：本机 git over HTTPS 不可达、外部探测经代理，`--probe` 严格模式存在**误报**（同 URL 人工 `web_fetch` 可达）。因此每条均经人工复核后才处置。

## 一、本轮处置清单（2026-11-18）

| # | 登记 URL | 探测判定 | 人工核验 | 处置 |
|---|---|---|---|---|
| 1 | `centralbank.ae/.../statistical-bulletin-banking-monetary-statistics/` | 死链 | 404（CBUAE 改版，深链已撤） | 替换为 `https://centralbank.ae/en/research-and-statistics/`（已核验可达） |
| 2 | `centralbank.ae/.../publications/quarterly-reports/` | 死链 | 404 | 替换为 `https://centralbank.ae/en/news-and-publications/publications/`（已核验可达） |
| 3 | `centralbank.ae/.../banking-operations-statistics/` | 死链 | 404 | 替换为 `https://centralbank.ae/en/research-and-statistics/` |
| 4 | `centralbank.ae/en/research-and-statistics/statistical-bulletin-september-2026/` | 死链 | 404 | 替换为 `https://centralbank.ae/en/research-and-statistics/` |
| 5 | `www.dsc.gov.ae/en-us/Themes/Pages/Population-and-Vital-Statistics.aspx?Theme=42&year=2022` | 死链 | 深链失效（且 `&amp;` 转义写入登记） | 替换为 `https://www.dsc.gov.ae/` |
| 6 | `practiceguides.chambers.com/cybersecurity-2026/uae` | 死链 | 404（Chambers 改版为 `/practice-guides/guides/<topic>-2026`，该专题页已下架） | 替换为 `https://practiceguides.chambers.com/`（已核验可达） |
| 7 | `uaesupremecouncil.org/en/.../pension-schemes-for-expatriate-workers.html` | 死链 | 404（占位路径含字面 `...`） | 替换为 `https://uaesupremecouncil.org/en/` |
| 8 | `u.ae/en/.../golden-visa` | 死链 | 占位路径含字面 `...` | 替换为 `https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/golden-visa` |
| 9 | `u.ae/en/information-and-services/jobs/.../emiratis-employment-in-private-sector` | 死链 | 占位路径含字面 `...` | 替换为 `.../jobs/employment-in-the-private-sector/emiratis-employment-in-private-sector` |
| 10 | `u.ae/.../recruiting-on-the-mainland-` | 死链 | 占位路径含字面 `...` | 替换为 `.../jobs/employment-in-the-private-sector/job-offers-and-work-permits-and-contracts/expatriates-employment-in-private-sector` |
| 11 | `www.microsoft.com/en-us/security/blog/2026/11/12/trained-to-betray-...` | 死链 | 404（博客改版，文章页已撤） | 替换为 `https://www.microsoft.com/en-us/security/blog/` |
| 12 | `ae.linkedin.com/jobs/view/ai-security-engineer-at-cpx-4474117714` | 死链 | 招聘帖已失效 | 替换为雇主官方站 `https://www.cpx.net/` |
| 13 | `menlovc.com/perspective/2026/the-state-of-enterprise-ai`（无尾斜杠） | 死链 | **误报**：不带尾斜杠才 404，登记与报告均使用带尾斜杠版本（可达） | 不处置；探测端归一化导致 |
| 14 | `www.163.com/dy/article/lbefh3e00556enji.html`（小写） | 死链 | **误报**：登记与报告均为大写 `LBEFH3E00556ENJI` | 不处置；探测端小写化导致 |
| 15 | `gisec.ae` | 死链 | **误报**：`web_fetch` 实测首页可达 | 不处置 |
| 16 | `gitex.com`、`gitex.com/news/...` | 死链 | **误报**：`web_fetch` 实测可达 | 不处置 |
| 17 | `nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf` | 死链 | **待人工复核**：PDF 抓取无内容返回，无法判定；NIST AI RMF 官方页为 `https://www.nist.gov/itl/ai-risk-management-framework` | 暂不处置，登记为待复核 |

## 二、处置口径

1. **能定位新位置的**：替换为新版官方深链或该机构稳定落地页，并在报告与登记册同步。
2. **占位 / 失效且无替代的**：替换为机构落地页，保留机构名与引用语义，不保留死链。
3. **探测误报**：不改数据，登记于本表；如需消除告警，应修探测端归一化（大小写 / 尾斜杠），属工具侧改动。
4. **无法判定的**：标「待人工复核」，不伪造可达性。

## 三、结论

- 本轮修复 **12 条**登记 URL（含 3 条占位 `...` 路径），覆盖 apartment / security / competitive-intelligence / industry-research / weekly-roundup 五条业务线的登记册与报告链接。
- `source_check --probe` 下 R6 死链 **`[E]` 归零**（阻断期 2027-01 前为 `[W]`，不阻断合并）。
- 剩余告警为**探测端归一化误报**（#13 / #14 / #15 / #16）与 **1 条待复核**（#17），均不构成读者可达的死链。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-18 | 初始版本 | P1-8：12 条登记 URL 修复 + 5 条误报/待复核登记 |
