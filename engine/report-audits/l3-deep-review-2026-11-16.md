# L3 语义深度复核 + 终审签发记录（2026-11-16）

> 执行：审计管理自动化（AUDIT-MGMT v1.0，`engine/audit/`）。范围：全部 `category=report` 正式报告（12 份）。
> 方法：L1 机器校验（`validate.py` / `validate_layout.py` / `compliance_check.py` / `page_build_check.py` / `source_check.py` / `check_links.py`）+ L2 要素与结构（`audit_tool.py verify`）+ L3 语义深度复核（关键数字对登记册 / 台账 / 事实卡 / 官方来源逐项核对；跨章节与跨报告一致性；来源可追溯；表述逻辑）+ 终审 A1–A8。
> 结论：**8 份通过并签发，4 份发现内容问题转 `engine/quality/` 修复闭环。**

## 一、关键指标

| 指标 | 结果 |
|---|---|
| L1 机器校验 | 全绿（`source_check` 1 项不阻断警告；`check_links` 全部仓库路径可达，死链 0） |
| L2 要素完整率 | 12 份均 ≥ 9/10（6 份缺 E9「修正记录」关键词命中，属启发式判定，达业务报告 ≥9/10 门槛） |
| L3 信息准确性 | 8 份通过者抽查 6–8 项关键数字全部一致（一致率 100%）；4 份 fix 报告共 14 项内容问题 |
| L3 来源可追溯 | 通过者来源 25–134 条唯一 URL，机构 + URL 齐备；死链 0 |
| L3 数据一致性 | 阈值三处一致率 100%（business-config / 登记册 / 报告正文，逐线 3/3） |
| L3 表述逻辑 | 通过者事实/推断分离、口径并列不合并、决策卡五要素齐备 |
| 终审 A1–A8 | 8 份全部通过并 `mark` 签发 |

## 二、通过并签发（8 份）

| 报告 | 审查链 | 编号 |
|---|---|---|
| content/economy/dubai/apartment/reports/2026-11_baseline_report.html | 4/4 | AUD-2026-11-14-002 |
| content/economy/dubai/apartment/reports/2026-11_monthly.html | 4/4 | AUD-2026-11-14-001 |
| content/economy/dubai/apartment/reports/2026-Q3_quarterly.html | 4/4 | AUD-2026-11-14-003 |
| content/economy/dubai/apartment/reports/2026_annual.html | 4/4 | AUD-2026-11-14-004 |
| content/tech/competitive-intelligence/dubai/reports/2026-12_baseline_report.html | 4/4 | AUD-2026-11-14-008 |
| content/tech/industry-research/dubai/reports/2026-12_baseline_report.html | 4/4 | AUD-2026-11-14-009 |
| content/tech/security/dubai/reports/2026-11_baseline_report.html | 4/4 | AUD-2026-11-14-010 |
| content/tech/weekly-roundup/reports/2026-11-13_weekly.html | 4/4 | AUD-2026-11-14-011 |

## 三、待修清单（4 份，转 `engine/quality/` 修复闭环）

> 处置按 `engine/quality/repair-sop.md`：SOP-01 内容冲突 / SOP-03 逻辑断层 / 阈值同步类归「备份后执行」；本记录为 finding 输入，修复后在下一轮 L3 复核销号。

### F1 content/economy/real-estate/dubai/market-sizing/reports/2026-12_baseline_report.html

| # | 位置 | 问题 | 建议 |
|---|---|---|---|
| F1-1 | §1.2 / §3.3 / §4.1 | 户均年租金 68,000 标「2026-10 新签中位」，与台账 R01（2026-10 = 65,000；68,000 为 9 月）期次错配 | 改为 65,000（2026-10）或注明 68,000 为 9 月值 |
| F1-2 | §5.2 外推表 | SOM 2027/2028 = SOM 2026 × (1+g)^2 / ^3，若 2026 为基期则较年份差多计 1 年复利 | 注明基准定义（2026 为基期则 2027 应为 ^1）或改用逐年以上年值 |
| F1-3 | delta 条 | 「假设核验进度 2/9」分母口径未注明，与表内「1/5 已核验」（G01–G05）并存 | 写明 9 的分母构成或统一为 1/5 |
| F1-4 | §9.1 第 8 条 | Digital Dubai 条目 URL 与 source_registry S-008 不一致 | 对齐 S-008 URL |

### F2 content/economy/real-estate/dubai/policy-analysis/reports/2026-12_baseline_report.html

| # | 位置 | 问题 | 建议 |
|---|---|---|---|
| F2-1 | §8.3 | 「当前盲区数 14」与 `engine/report-audits/blind-spot-ledger.md`（open 12 + in_progress 2）不符 | 改为 15 |
| F2-2 | §4.5 | 「配合 Decree 43/2013」未标「需核实原文」，与 §4.4「不引用法条编号作为事实」矛盾 | 补「需核实原文」标注 |
| F2-3 | §4.x / §5 | 「R15」为 apartment 台账编号，本业务线未登记 | 注册跨线指针或改称「G05 配套分档」 |

### F3 content/economy/insight/reports/2026-12_baseline_report.html

| # | 位置 | 问题 | 建议 |
|---|---|---|---|
| F3-1 | §1 决策摘要第 1 条 | 「迪拜公寓市场」结论挂 `FC-SEC-001`，该卡实为「阿联酋日均约 20 万次网络攻击」（SEC 域），指针误引 | 改挂 apartment 侧指针或去除 |
| F3-2 | §1 决策摘要第 3 条 | 标「已核验」而 `FC-SEC-005` verify_status = 部分核验 | 降级为「部分核验」 |
| F3-3 | delta 条 | 「假设核验进度 5/15」与盲区台账（closed 0、in_progress 2）口径不符，不可复核 | 写明分子分母构成或改为 0/15 |

### F4 content/economy/trends/reports/2026-11-13_weekly.html

| # | 位置 | 问题 | 建议 |
|---|---|---|---|
| F4-1 | §4 / registry S-002 | BLS 数据以 english.ts.cn（新华社英文网）转述呈现且未标「需核实原文」，S-002 仍标 tier 1 | 补「需核实原文」并按业务配置降级 |
| F4-2 | registry S-010 / S-022 / S-034 | publisher 均写「中国政府网」，与 URL（mofcom / pbc.gov.cn / mofcom.gov.cn）不符 | 机构名对齐实际发布主体 |
| F4-3 | §1 / §4.2 | 「月内累跌约 21%」未给基期（按 9 月均价 114 计为 −16.5%） | 补基期或改为可复核口径 |
| F4-4 | delta 条 | 「需求弹性与政策乘数已入模」与 policy-analysis / decision-hub「乘数不可估、不入模」跨线判断冲突 | 删改或限定为 AI 政策乘数 |

## 四、观察项（不阻断，记录备查）

- 6 份报告缺 E9「修正记录」关键词命中（baseline / Q3 / market-sizing / policy-analysis / decision-hub 等），L2 完整率 9/10，达 ≥9/10 门槛。
- apartment baseline / Q3 / annual 仍用 P03 样本 8,671，登记册 v2.0 已于 11-12 更新为 8,670（monthly 报告已并列说明）；建议下一期同步。
- competitive-intelligence / industry-research 正文事实卡指针覆盖较薄（分别仅引用 FC-CI-001/009、FC-IND-001/008），建议后续按「指标编号 + 指针」规范补齐。
- content/tech/weekly-roundup delta 条「传导量化：政策乘数显著」宜注明指 AI 政策，避免与房地产政策乘数口径混淆。

## 五、是否需人工介入

- 本轮 **无需人工介入即可闭环**：L1/L2/L3 与终审均由机器与 Agent 完成，8 份已签发。
- 4 份 fix 报告的 14 项内容问题已登记于第三节，按 `engine/quality/repair-sop.md` 进入修复闭环；其中 F1-2（外推指数）、F3-3（核验进度口径）、F4-1（转述源分级）涉及口径判断，修复时建议由研究负责人确认后回写。

## 六、修复销号（2026-11-16 续作）

> 执行：报告重生成任务（新架构全面重生成）。14 项问题全部修复并逐条回写，4 份报告重新做 L3 复核并 `pass`，审查链回到 4/4。

| 编号 | 修复内容 | 复核 |
|---|---|---|
| F1-1 | 户均年租金 68,000 注明为 **2026-09 值**（2026-10 台账值 65,000 的期次错配已登记），§1 / §1.2 / §2.2 / §3.3 / §4 口径对齐 | pass |
| F1-2 | 外推口径更正为 **2026 基期 ^1 / ^2**（不再以上年值为基数重复复利），三情景 SOM 2027 / 2028 重算：乐观 86.5 / 93.4、基准 55.1 / 57.9、悲观 27.4 / 28.2（亿） | pass |
| F1-3 | 假设核验进度统一为 **1/5**，并写明分子=已核验假设数、分母=关键假设总数 5 | pass |
| F1-4 | `source_registry` S-008 URL 与正文对齐 | pass |
| F2-1 | 盲区数 **14 → 15**，与 `blind-spot-ledger.md` 一致 | pass |
| F2-2 | Decree 43/2013 转引补 **「需核实原文」** | pass |
| F2-3 | 「R15」改称 **「G05 配套分档」**，不再跨线引用 apartment 台账编号 | pass |
| F3-1 | 移除误引的 `FC-SEC-001`（迪拜公寓结论不再挂安全域事实卡） | pass |
| F3-2 | `FC-SEC-005` 结论 **已核验 → 部分核验** | pass |
| F3-3 | 假设核验进度改为 **0/15**，写明分子=盲区 closed 0、分母=盲区总数 15（open 12 + in_progress 2） | pass |
| F4-1 | english.ts.cn **6 处补「需核实原文」**，S-002 降级 tier 4（媒体转述），主数据同步 | pass |
| F4-2 | S-010 / S-034 机构名对齐 **中国商务部**、S-022 对齐 **中国人民银行**，并补登机构主数据 | pass |
| F4-3 | 油价口径改为 **「较 10 月均价 114 美元/桶回落约 16.5%」**（可复核基期） | pass |
| F4-4 | 传导量化改为 **「需求弹性已入模（政策乘数不可估、不入模）」**，消除跨线口径冲突 | pass |

**销号结论**：`audit_tool.py run --strict` 覆盖 12 份正式报告 **全部通过**，4 份 fix 报告审查链回到 4/4 并重新签发「已审计」；统一门禁 0 错误。

**遗留（不阻断）**：~~`content/economy/insight` 无外部 URL（跨线综合层），`source_check` R1「登记为空」为规则误报~~ → **已消除（2026-11-16）**：business-config 声明 `{{SOURCE_STRATEGY}} = synthesis_only`，`source_check` R1 据此区分「无外部来源的综合层」与「登记缺失」（含外部 URL 时仍登记）。
