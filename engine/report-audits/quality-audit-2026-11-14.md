# 内容质量审计报告 @ 2026-11-14

> **状态**：历史记录（时点审计，留存备查；四维 21 指标的事实源为 `engine/quality/rubric.md`）
> **执行体系**：`engine/quality/`（QUALITY-AUDIT v1.0）· 主控 `engine/quality/prompts/00-orchestrator.md`
> **范围**：全部业务线 / 报告 / 业务线提示词 / 登记册 / 词汇 + `engine/templates/` 通用层 + `engine/vocabulary/` 词库
> **本轮性质**：优化后工具链的复跑（含条件节拍识别、年度别名、基线守卫）
> **计数口径**：8 条业务线 / 14 份报告 / 137 单测（2026-11-14 时点）

---

## 一、结论

- **门禁：pass** —— P0 = 0，P1 = 0，P2 = 0。
- **总体健康度：100%**（完整性 / 准确性 / 一致性 / 关联性 四维均达标）。
- 两轮累计修复 **8 项**（F-01…F-05 + N1…N3）全部闭环，本轮**无新增 finding**。

---

## 二、盘点摘要

| 对象 | 数量 |
|---|---|
| 业务线 | 8 |
| 报告 | 14（11 主 + 3 legacy） |
| 业务线提示词 | 27 |
| 通用层类型 | 13 |
| 词汇主题 | 5（372 条） |

业务线明细：apartment(4 报告/5 提示词) · market-sizing(1/3) · policy-analysis(1/3) · economy-trends(1/3) · competitive-intelligence(1/4) · industry-research(1/3) · security(1/5) · ai-trends(1/3)。

---

## 三、机器判定结果

| 工具 | 退出码 | 结果 |
|---|---|---|
| `validate.py` / `validate_layout.py` | 0 | 通过 |
| `compliance_check.py --check` | 0 | 全部报告符合类型骨架 |
| `page_build_check.py` | 0 | 16 页 0E / 0W |
| `lint_reports.py` | 2 | 0 错误 / 86 警告（既有历史项） |
| `check_links.py` | 0 | 0 断链 |
| `classify_reports.py --check` | 0 | 无错位报告 |
| `update_planner.py --pending-only` | 0 | 空清单 |
| `vocab_tool check ×5` / `sync_vocab.py verify` | 0 | 0 错 0 警 / 5 绑定全通过 |
| `unittest`（`engine/tests`） | 0 | **137 通过** |

---

## 四、语义判定结果（四维 21 项）

| 维度 | 指标数 | 实测 | 判定 |
|---|---|---|---|
| 完整性 | 6（C-01…C-06） | 结构 / 字段 / 目录 100%；登记册覆盖 apartment 94.7%、security 100%；节拍 0 pending；词汇 5/5 | 全达标 |
| 准确性 | 5（A-01…A-05） | 来源可追溯 ≥95%（抽样）；分级合规 100%；数值一致 100%；新鲜度 ≥90%；链接可达 100% | 全达标 |
| 一致性 | 5（L-01…L-05） | 跨章节数值 100%；口径 100%（S12→S11 已统一）；阈值三处一致 0 处不一致；结论-证据 ≥95%；时间线 100% | 全达标 |
| 关联性 | 5（R-01…R-05） | 归属 100%；维度优先级 100%；跨主题重复 0%；断头锚点 0%；主题-内容匹配 ≥95% | 全达标 |

> 完整 21 指标定义与阈值见 `engine/quality/rubric.md`；A-01 / A-04 / L-04 为抽样判定，其余为全量工具或逐项核验。

**关键不变量复核（证据）**：登记册阈值逐行比对 0 处不一致；ai-trends 周报单位矛盾已修；季报活跃指标编号已统一为 S11 子项；industry-research 报告含 6 条 ❌ 修正锚；market-sizing 登记册正确指向公寓台账；security 月度提示词含 `report-output: none`（条件节拍，规划器不派任务）；新线基线守卫生效（不再派基线前任务）。

---

## 五、修复记录

| ID | 场景 | 级别 | 目标 | 状态 |
|---|---|---|---|---|
| F-01 | C10/L-03 阈值口径 | P0 | apartment 登记册 xlsx | fixed |
| F-02 | C06/A-03 单位矛盾 | P0 | ai-trends 周报 | fixed |
| F-03 | C08/L-02 S12/S11 | P1 | apartment 季报 | fixed |
| F-04 | C-05 条件节拍 | P2 | `update_planner` + security 提示词 | fixed |
| F-05 | C13 时效标注 | P2 | apartment 年报 | fixed |
| N1 | C05/C07 登记载体 / 路径 | P1 | 4 条新线配置 | fixed / 设计如此 |
| N2 | C05 周期提示词缺失 | P1 | 4 条新线 `prompts/` | fixed（补建 9 份） |
| N3 | C06 修正未继承 | P1 | industry-research 报告 | fixed |

无「待人工复核」项。

---

## 六、回归检查与既有遗留

- **回归**：重跑全部机器门禁，错误项只减不增；语义复评 21 项全达标；15 类混乱场景命中 0；本轮新增问题数 = 0。
- **既有遗留（不计入健康度）**：`lint_reports.py` 86 项警告（公寓季 / 年报表格缺 `class="fixed"` 与列宽）——**已于 2026-11-15 修复**，见 [tech-debt-ledger.md](tech-debt-ledger.md) A 类；历史报告缺免责声明节为既有项。

---

## 七、附录

- 结构化清单：`quality-manifest-2026-11-14.json`（同目录）
- 体系文件：`engine/quality/`（README / rubric / chaos-taxonomy / repair-sop / ops-guide / prompts 00–05）
