# mainline 吸收式融合 · 覆盖矩阵（MAINLINE-ADOPTION-COVERAGE-MATRIX）

> **状态**：现行（随 Phase 推进更新）
> **事实源**：[mainline 规范适配性评估](./mainline-adoption-assessment-2026-11-17.md)（MAINLINE-ADOPTION-ASSESSMENT 2026-11-17）
> **用途**：把《方案》每一项（痛点 / 吸收项 / Phase 任务 / CI 改造 / 治理标准 / 风险 / 量化指标）映射到「任务编号 · 产物 · 验收命令 · 状态」，**不得静默遗漏**。
> **状态取值**：`已实施` / `已复用` / `显式延后（含理由与归属）`。
> **主体声明**：本矩阵确认「**保留现有 N0–N8 体系为主体，选择性接入 mainline 任务级闭环机制**」，不整体替换为 mainline 11 阶段（《方案》§5.1）。

---

## 一、痛点 P-01 .. P-10

| 编号 | 痛点 | 任务 / 产物 | 验收命令 | 状态 |
|---|---|---|---|---|
| P-01 | 审计登记册含失效条目（2 条指向已删除文件） | Phase 0.1：`audit_tool.py` 增 stale 检测 + `prune`；登记 31→29 | `python engine/audit/scripts/audit_tool.py status` | 已实施 |
| P-02 | 「已审计」实际覆盖率≈0（10 份停在 in-review 3/4） | Phase 2.2：L3 批量补审 + SLA；`audit_tool accept` 覆盖率 | `python engine/audit/scripts/audit_tool.py accept` | 待实施 |
| P-03 | strict 审计耗时无阈值 | Phase 0.2：`perf-status.json` 增 `audit_strict_p95_ms`；`perf_monitor.check_thresholds` 增规则 | `python engine/tools/perf_monitor.py check` | 已实施 |
| P-04 | 声明与实现落差（pipeline_runner / repo_sync 工作流零调用） | Phase 0.4 方案 A：`ci.yml` 增 `pipeline_runner validate` | `python engine/tools/pipeline_runner.py validate` | 已实施 |
| P-05 | 任务级闭环工件缺失 | Phase 1.1 / 1.2：`task_plan.py` + `local_mainline.py` | `task_plan.py --check`（置于 `engine/tools/`） | 待实施 |
| P-06 | 门禁清单 / 类型注册多点手工同步 | 未列入 Phase 0–3 | — | 显式延后（需另立「注册结构化」专项，重构 `optimization_gate.CHECKS` / `template-registry.md` / `compliance-rules.json` / `_common.TEMPLATE_TYPE_DIRS` / `build_hub.TYPE_SHORT` 五处对齐；本轮聚焦吸收式融合，避免范围蔓延） |
| P-07 | 规范复述漂移 | Phase 3.3：AGENTS.md 上位-下位收敛，复述点清零 | `python engine/tools/check_links.py` + 人工核查 | 待实施 |
| P-08 | 无静态检查 | Phase 3.1：ruff / mypy 纳入 `optimization_gate` | `python engine/tools/optimization_gate.py --only ruff,mypy` | 待实施 |
| P-09 | 多会话并发写同一工作树 | 未列入 Phase 0–3 | — | 显式延后（文件编辑锁需平台级 / 编辑器级支持；现有「共享检出锁 + PR 串行合并 + 分支隔离」已覆盖 git 层竞态，文件编辑层留待平台能力就绪后实施） |
| P-10 | 审计文档累积无轮转 | Phase 3.2：`report-audits` 轮转归档（保留最近 12 个月） | `python engine/tools/archive_reports.py --audit-docs` | 待实施 |

## 二、吸收项 ① .. ④

| 编号 | 吸收项 | 任务 / 产物 | 验收命令 | 状态 |
|---|---|---|---|---|
| ① | 任务计划工件（plan/tasks/risks + 任务启动文件） | Phase 1.1：`task_plan.py`（置于 `engine/tools/`）→ `engine/audit/records/` 下的 `tasks/<slug>/` 子目录 | `task_plan.py --help`（置于 `engine/tools/`） | 待实施 |
| ② | 本地 mainline 编排脚本 | Phase 1.2：`local_mainline.py`（置于 `engine/tools/`；薄封装，复用 `repo_sync` / `optimization_gate`） | `local_mainline.py --help`（置于 `engine/tools/`） | 待实施 |
| ③ | 完成前审计证据索引 | Phase 2.1：`audit_tool` evidence index + `audit_registry.evidence` | `python engine/audit/scripts/audit_tool.py evidence <report>` | 待实施 |
| ④ | 分支登记册语义对齐 | 既有 `branch_registry.json` + BRANCH-NAMING-SPEC v1.0 | `python engine/tools/repo_sync.py branches` | 已复用 |

## 三、Phase 任务 0.1 .. 3.3

| 编号 | 任务 | 产物 | 验收命令 | 状态 |
|---|---|---|---|---|
| 0.1 | 审计登记册失效清理 + stale 检测 | `audit_tool.py`（`stale_paths` / `cmd_prune` / `status`） | `python engine/audit/scripts/audit_tool.py status` | 已实施 |
| 0.2 | strict 审计性能阈值 | `perf-status.json` / `perf_monitor.py` | `python engine/tools/perf_monitor.py check` | 已实施 |
| 0.3 | 修 `pipeline_runner` probe 语义 | `pipeline_runner.py`（CLI `--probe/--no-probe` 默认尊重清单） | `python engine/tools/pipeline_runner.py validate` | 已实施 |
| 0.4 | 收口「声明-实现」落差（方案 A） | `ci.yml` 增 `pipeline_runner validate` 步骤 | `grep pipeline_runner .github/workflows/ci.yml` | 已实施 |
| 1.1 | 新增 `task_plan.py` | `task_plan.py` + `test_task_plan.py`（均置于 `engine/tools/` 与 `engine/tests/`） | `python -m unittest engine.tests.test_task_plan` | 待实施 |
| 1.2 | 新增 `local_mainline.py` | `local_mainline.py` + `test_local_mainline.py`（均置于 `engine/tools/` 与 `engine/tests/`） | `python -m unittest engine.tests.test_local_mainline` | 待实施 |
| 1.3 | AGENTS.md 增「任务级闭环」硬性约束节 | `AGENTS.md` / `report-pipeline-system.md` N0.5 | `python engine/tools/check_links.py` | 待实施 |
| 2.1 | `audit_tool` 增 evidence index | `audit_tool.py` + `audit_registry.json` `evidence` 字段 | `python engine/audit/scripts/audit_tool.py evidence` | 待实施 |
| 2.2 | L3 瓶颈专项 | 10 份 `in-review` 批量补 L3 + SLA 写入规范 | `python engine/audit/scripts/audit_tool.py accept` | 待实施 |
| 2.3 | 登记册清理纳入维护流水线 | `scheduled-maintenance.yml` stale 检测步骤 | `grep audit_tool .github/workflows/scheduled-maintenance.yml` | 待实施 |
| 3.1 | ruff / mypy 纳入统一门禁 | `optimization_gate.CHECKS` + `static_check.py` + 配置 | `python engine/tools/optimization_gate.py --only ruff,mypy` | 待实施 |
| 3.2 | `report-audits` 轮转归档 | `archive_reports.py --audit-docs` | `python engine/tools/archive_reports.py --audit-docs` | 待实施 |
| 3.3 | 规范上位-下位收敛 | `AGENTS.md` 精简 + 专用规范下沉 | `python engine/tools/check_links.py` | 待实施 |

## 四、配套 CI/CD 改造点

| 工作流 | 改造 | 状态 |
|---|---|---|
| `ci.yml` | 增 `pipeline_runner validate`（0.4 方案 A）；增 ruff/mypy 步骤（3.1，经统一门禁承载） | 待实施 |
| `scheduled-maintenance.yml` | 增 stale 检测（2.3）；增 `archive_reports --audit-docs`（3.2）；保留 `pipeline_audit --rotate` | 待实施 |
| `audit.yml` | 接入 evidence index（2.1）；strict 性能阈值护栏（0.2，经 `perf_monitor` 统一门禁承载） | 待实施 |
| `submit-pr` | **不改动**：已对齐（CI 分支 + PR + auto-merge，固定 SHA） | 已复用 |
| `workspace-cleanup` | **不改动**：已对齐（只删未跟踪路径，预/收尾双触发） | 已复用 |
| `remediation-ticket` | **不改动**：已对齐（幂等建 Issue，只通知不提交代码） | 已复用 |

## 五、配套流程治理标准 1 .. 5

| # | 标准 | 落地 | 状态 |
|---|---|---|---|
| 1 | 工件即门禁输入：无 `plan.json` 不得 `repo_sync run --gate` | `repo_sync.run` 增计划校验（`task/*` 分支 + `--gate`），`local_mainline` 强制计划 | 待实施 |
| 2 | 单一事实源：任务工件 schema 由 `task_plan.py` 定义 | `task_plan.py` schema + 其余位置只指针 | 待实施 |
| 3 | 复用纪律：`local_mainline.py` 只编排，禁止重写校验 | 单测锁定「门禁仍走 `optimization_gate`」 | 待实施 |
| 4 | 版本治理：核验 / 收敛不升级版本号 | 既有 `report-pipeline-system.md` §六 | 已复用 |
| 5 | 新增即删旧：每新增一层规范，同步删除等量旧表述 | Phase 3.3 执行并记录删改点 | 待实施 |

## 六、风险 6 项

| # | 风险 | 缓解 | 状态 |
|---|---|---|---|
| R1 | 任务工件沦为形式主义 | 「工件即门禁输入」+ 任务启动文件强制 | 待实施 |
| R2 | 双入口漂移 | `local_mainline.py` 只编排；测试锁定复用关系 | 待实施 |
| R3 | L3 瓶颈不解决 | SLA（每两周）+ 批量复核 | 待实施 |
| R4 | 规范复杂度再增 | 「新增即删旧」；版本治理 | 待实施 |
| R5 | 多会话并发写 | 文件编辑锁 / 会话协调 | 显式延后（见 P-09） |
| R6 | 吸收式融合被误读为全量替换 | 本矩阵 + AGENTS.md 明确「主体保留、增量吸收」 | 待实施 |

## 七、量化指标 8 项（实测结果见§九）

| # | 指标 | 现状 | 目标 | 验证方式 | 状态 |
|---|---|---|---|---|---|
| M1 | 审计登记册失效条目 | 2 | 0 | `audit_tool status` | 已实施 |
| M2 | 有效报告「已审计」覆盖率 | 0/10 | ≥90% | `audit_tool accept` | 待实施 |
| M3 | 本地一次任务闭环操作数 | ~6 条 | 1 条 | `local_mainline.py` | 待实施 |
| M4 | strict 审计性能护栏 | 无阈值 | p95 ≤180s 有阈值 | `perf_monitor check` | 已实施 |
| M5 | 门禁噪声（validate 警告） | 0 | 保持 0 | `validate.py` | 已复用 |
| M6 | 规范复述点 | 多处残留 | 0 | `check_links` + 人工核查 | 待实施 |
| M7 | 统一门禁错误项 | 0 | 保持 0 | `optimization_gate --probe` | 已复用 |
| M8 | 单测 | 448 通过 | 保持全绿 | `unittest` | 已复用 |

## 八、Phase 门禁记录

| Phase | 统一门禁 `[E]` | unittest | check_links | page_build | 备注 |
|---|---|---|---|---|---|
| 基线（2026-11-17） | 0 | 448 OK（1 skip） | 通过 | 0E/0W | 见《方案》§1.6 |
| Phase 0 | 0 | 459 OK（1 skip） | 通过 | 0E/0W | — |
| Phase 1 | 待测 | 待测 | 待测 | 待测 | — |
| Phase 2 | 待测 | 待测 | 待测 | 待测 | — |
| Phase 3 | 待测 | 待测 | 待测 | 待测 | — |

## 九、量化指标实测结果

> 收尾自审计时填写：命令 + 输出 + 达标判定；未达标项给出原因与后续计划。

（待收尾填写）

## 版本记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1 | 2026-11-17 | 初始覆盖矩阵：P-01..P-10 / 吸收项①..④ / Phase 0.1..3.3 / CI 改造 / 治理标准 / 风险 / 量化指标全量映射 |
