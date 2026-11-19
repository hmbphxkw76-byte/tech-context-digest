# 第二期最小集（SECOND-ISSUE-MINIMAL-SET v1.0）

> **状态**：定义 + 工具就绪（2026-11-19）
> **依据**：[信息质量改进实施方案 v1.2](information-quality-improvement-plan-2026-11-19.md) §2.3（P0-3）/ [报告周期窗口](../docs/report-cycle-windows.md)
> **目标**：以最小内容成本让「逐期序列」从零到可比较，满足 P0-3 验收（≥3 条业务线有第二期 + `semantic_diff` 有上期可比 ≥1）。
> **边界**：本文件只到「定义 + 工具就绪」；**报告正文属内容产出**，须按各业务线 `prompts/` 流程人工或 Agent 撰写，不自动生成。

---

## 1. 最小集定义（3 条业务线 / 3 份报告）

| # | 业务线 | 周期 | 提示词（业务线相对） | 输出（业务线相对） | 上期（环比基期） |
|---|---|---|---|---|---|
| 1 | `content/economy/dubai/apartment` | monthly 2026-12 | `prompts/prompt-monthly-monitor.md` | `reports/2026-12_monthly.html` | `reports/2026-11_monthly.html` |
| 2 | `content/economy/trends` | weekly 2026-11-20 | `prompts/prompt-weekly-monitor.md` | `reports/2026-11-20_weekly.html` | `reports/2026-11-13_weekly.html` |
| 3 | `content/tech/weekly-roundup` | weekly 2026-11-20 | `prompts/prompt-weekly-monitor.md` | `reports/2026-11-20_weekly.html` | `reports/2026-11-13_weekly.html` |

**可选第 4 份**：`content/tech/competitive-intelligence/dubai` · monthly 2026-12（规划器已派发；无同周期上期，不参与 `semantic_diff` 可比）。

> 路径均相对各业务线目录书写;绝对落盘位置为 `<业务线>/reports/<文件名>`。

---

## 2. 工具覆盖（就绪）

| 工具 | 作用 | 状态 |
|---|---|---|
| `engine/tools/update_planner.py --period 2026-12` | 派发月度任务（apartment、competitive-intelligence） | **[已核验] 就绪** |
| `engine/tools/update_planner.py --period 2026-11-20` | 派发周报任务（`content/economy/trends`、`content/tech/weekly-roundup`） | **[已核验] 就绪（周周期派发为本次新增）** |
| `engine/tools/semantic_diff.py scan` | 产出后可比（当前「有上期可比 0」） | **[已核验] 就绪** |
| `_common.CYCLE_WINDOWS` + hub | 滚动基线「本期更新 + 环比基期」 | **[已核验] 就绪** |
| `update_planner.py` 盲区阻塞跟踪段 | S2 未消号项与责任周期（过期显式标注） | **[已核验] 就绪** |

---

## 3. 验收口径（方案 §2.3）

- ≥ 3 条业务线有第二期报告；
- `semantic_diff` 有上期可比 ≥ 1；
- IGI-03 ≥ 0.80；C-05 提升；
- 滚动基线（本期更新 + 环比基期）在 hub 生效。

---

## 4. 依赖与阻塞

- **内容撰写**：需单独确认后执行（内容产出，不自动生成）。
- **数据侧**：B01 / B02 / B03 / B15 阻塞未解（见[盲区台账](blind-spot-ledger.md)），第二期内容在数据缺口处须显式标注，不得编造。

---

## 5. 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-19 | 初始版本 | 3 条业务线最小集 + 工具覆盖说明（月 / 周派发均就绪） |
