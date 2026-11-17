# 周期复跑 runbook（ops-guide）

> **用途**：规定 QUALITY-AUDIT 的触发方式、频率、执行步骤、产物与告警，保证「周期复跑」可落地、可追溯、不干扰既有流水线。

---

## 一、两层分工

| 层 | 内容 | 执行者 | 接入点 |
|---|---|---|---|
| **确定性子集** | 既有工具链（11 项命令）的 `[E]`/`[W]` 扫描 | Python 脚本 | `scheduled-maintenance.yml`（已存在） |
| **语义层** | 15 类场景判定、冲突裁决、修复、复验 | Agent | 本提示词体系（周期触发） |

- 确定性子集已接入 CI，无需新增步骤即可持续产出机器结果。
- 语义层需要 LLM，**不能**放进纯脚本 CI；由 Agent 周期执行，消费 CI 产出的机器结果。

---

## 二、触发方式（三选一或组合）

### 方式 A：妙手 automation（推荐）

用妙手定时任务周期执行 `prompts/00-orchestrator.md`。建议频率：

| 频率 | 适用 |
|---|---|
| 每周一次 | 与 `scheduled-maintenance` 同步，复用其机器结果 |
| 每月一次 | 仅语义巡检，不修复 |
| 事件触发 | 新业务线接入 / 大规模重构后立即跑一次 |

> 创建定时任务需用户显式授权；本文件只提供配置口径。

### 方式 B：手动触发

用户说「执行质量评估」/「跑质量巡检」时，Agent 读取 `engine/quality/prompts/00-orchestrator.md` 执行。

### 方式 C：CI 确定性子集增强（可选）

在 `scheduled-maintenance.yml` 增加一步，将机器结果汇总为 `machine-quality-report.json`（落位 `engine/report-audits/`），供语义层消费。**不引入 LLM 调用**，仅做结果落盘，风险低。

---

## 三、执行步骤（Agent）

```
阶段 0  备份：确认 git 工作区干净；对将改文件建 .bak
阶段 1  盘点：动态发现业务线 / 报告 / 提示词 / 登记册 / 模板 / 词汇 → inventory
阶段 2  机器判定：运行既有工具，收集 [E]/[W]
阶段 3  语义判定：按 15 类场景逐项检查 → findings
阶段 4  定级排序：P0 → P1 → P2
阶段 5  自动修复：按 repair-sop.md 执行
阶段 6  复验回归：重跑工具 + 语义复评，确认无新增
阶段 7  报告：写 quality-audit-<date>.md + quality-manifest.json
```

各阶段提示词见 `engine/quality/prompts/` 下的 `01-inventory.md` ~ `05-verify.md`。

---

## 四、产物与落位

| 产物 | 路径 | 说明 |
|---|---|---|
| 审计报告 | `engine/report-audits/quality-audit-<YYYY-MM-DD>.md` | 人读，含健康度、findings、repairs、待复核清单 |
| 结构化清单 | `engine/report-audits/quality-manifest-<YYYY-MM-DD>.json` | 机读，符合 `manifest.schema.json` |
| 机器结果（可选） | `machine-quality-report.json`（落位 `engine/report-audits/`） | CI 确定性子集汇总 |

**确定性要求**：报告正文不写生成时刻（或在跨轮比对时归一化剔除），保证同内容同产物。

---

## 五、告警与升级

| 情况 | 处置 |
|---|---|
| P0 未清零且自动修复无效 | 输出「待人工复核清单」，创建 issue（label: `quality-audit`） |
| 连续两轮总体健康度下降 | 标记趋势异常，提示人工介入 |
| 修复引入新增问题（回归 fail） | 立即回滚，记录原因 |
| 权威源不明确的冲突 | 并列呈现 + 标「口径待核实」，不擅改 |

---

## 六、新增对象自动纳入

- 新增业务线：在 `engine/tools/layout.json` 登记主题与维度，即被阶段 1 发现。
- 新增报告：落入业务线 `reports/` 即被纳入。
- 新增类型：在 `template-registry.md` + `compliance-rules.json` 登记即被纳入。
- 新增词汇主题：`vocab_tool.py topic-add` 后即被纳入。

> **无需修改本提示词体系**。

---

## 七、与既有规范的关系

- 本体系**不替代** `page-build-spec.md` / `page-build-governance.md`，而是复用其门禁工具。
- 本体系**不替代** `compliance_check.py` / `validate.py`，而是消费其结果并补齐语义层。
- 本体系新增的量化口径集中在 [rubric.md](./rubric.md)，不与既有规范各写一套。

---

## 八、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 两层分工、三种触发方式、执行步骤、产物落位、告警升级与自动纳入 |
