# 实施提示词索引（IMPLEMENTATION-PROMPTS v1.0）

> **用途**：把 [优化解决方案与实施清单 v2.0](../optimization-solution-and-implementation-checklist-2026-11-19.md) §4.6 的 T-01…T-10 拆成可**立即投喂 Agent** 的自包含提示词。
> **并发**：每个提示词独立、自包含；多会话 / 多 Agent 可并行执行，隔离方式见 §4.7。
> **判级**：`已核验` / `部分核验` / `推断` / `假设`。

## 1. 分派顺序与并发组

| 组 | 提示词 | 可并行 | 合并顺序 |
|---|---|---|---|
| G1 | `t01-source-evidence.md` → `t08-document-tier.md` | ❌ 串行（同 `source_check.py`） | 1 |
| G2 | `t02-proxy-calibration.md` / `t07-classification-version.md` | ✅ | 2 |
| G3 | `t03-finding-rule-ledger.md` / `t06-consumer-feedback.md` | ✅ | 3 |
| G4 | `t04-research-kernel-backfill.md` / `t05-vocab-empty.md` / `t09-uncertainty-confidence.md` / `t10-impact-tiering.md` | ✅ | 4 |

## 2. 通用执行协议（所有提示词共用）

1. **分支**：`task/<slug>-<session8>`（`session8` = 会话标识 8 位）；用 `python engine/tools/repo_sync.py branch <slug>` 创建。
2. **任务四件套**：`engine/audit/records/tasks/<slug>/{plan.json,tasks.json,risks.json,task-start.md}`（schema 见 `engine/tools/task_plan.py`）。受管 `task/*` 分支无四件套不得 `--gate`。
3. **提交**：`python engine/tools/repo_sync.py run --message "<msg>" --paths <paths> --gate`。
4. **完成前证据索引**：变更文件 + diff 摘要；验证命令与输出；对齐声明（方案 ID ↔ 验收）；回归声明（§5.1）。
5. **禁止**：直推 `main`；改方案外文件；改既有阈值；编造数值；把 `已核验` 与 `推断` 混标。

## 3. 验证对齐（每个任务单元收尾必做）

- **对齐**：`git diff --name-only` 与方案「涉及文件」核对（无越界）；验收标准逐条给证据。
- **不引入新问题**：跑 §5.1 的 R-REG-1/2/3/5（门禁 / 单测 / 指标 / 链接），任一项失败即回滚。
- **抽样复核**：≥3 样本由非执行方复核，一致率 ≥95%。

## 4. 文件清单

| 文件 | 任务 | 性质 |
|---|---|---|
| `t01-source-evidence.md` | 来源核验证据字段 + 内容指纹 | 工具侧 |
| `t02-proxy-calibration.md` | 代理指标抽样校准 | 工具侧 |
| `t03-finding-rule-ledger.md` | finding→规则回写台账 | 工具/流程 |
| `t04-research-kernel-backfill.md` | 研究内核历史警告收口 | 内容侧 |
| `t05-vocab-empty.md` | 词库空库补录 | 内容侧 |
| `t06-consumer-feedback.md` | 消费端反馈机制 | 设计 + 工具 |
| `t07-classification-version.md` | 分类版本号 + 互斥性校验 | 工具侧 |
| `t08-document-tier.md` | 文档级 / 陈述级信源分级 | 工具侧 |
| `t09-uncertainty-confidence.md` | 不确定性置信度字段 | 工具 + 内容 |
| `t10-impact-tiering.md` | 信息影响分级与披露 | 文档 + 内容 |
