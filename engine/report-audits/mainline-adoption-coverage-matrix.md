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
| P-02 | 「已审计」实际覆盖率≈0（10 份停在 in-review 3/4） | Phase 2.2：L3 批量补审 + SLA；`audit_tool accept` 覆盖率 | `python engine/audit/scripts/audit_tool.py accept` | 已实施 |
| P-03 | strict 审计耗时无阈值 | Phase 0.2：`perf-status.json` 增 `audit_strict_p95_ms`；`perf_monitor.check_thresholds` 增规则 | `python engine/tools/perf_monitor.py check` | 已实施 |
| P-04 | 声明与实现落差（pipeline_runner / repo_sync 工作流零调用） | Phase 0.4 方案 A：`ci.yml` 增 `pipeline_runner validate` | `python engine/tools/pipeline_runner.py validate` | 已实施 |
| P-05 | 任务级闭环工件缺失 | Phase 1.1 / 1.2：`task_plan.py` + `local_mainline.py` | `task_plan.py --check`（置于 `engine/tools/`） | 已实施 |
| P-06 | 门禁清单 / 类型注册多点手工同步 | 未列入 Phase 0–3 | — | 显式延后（需另立「注册结构化」专项，重构 `optimization_gate.CHECKS` / `template-registry.md` / `compliance-rules.json` / `_common.TEMPLATE_TYPE_DIRS` / `build_hub.TYPE_SHORT` 五处对齐；本轮聚焦吸收式融合，避免范围蔓延） |
| P-07 | 规范复述漂移 | Phase 3.3：AGENTS.md 上位-下位收敛，复述点清零；本轮收口门禁数量 21→23 一致性 | `python engine/tools/check_links.py` + `test_pipeline_system_doc` 门禁数量一致性 | 已实施 |
| P-08 | 无静态检查 | Phase 3.1：ruff / mypy 纳入 `optimization_gate` | `python engine/tools/optimization_gate.py --only ruff,mypy` | 已实施 |
| P-09 | 多会话并发写同一工作树 | 未列入 Phase 0–3 | — | 显式延后（文件编辑锁需平台级 / 编辑器级支持；现有「共享检出锁 + PR 串行合并 + 分支隔离」已覆盖 git 层竞态，文件编辑层留待平台能力就绪后实施） |
| P-10 | 审计文档累积无轮转 | Phase 3.2：`report-audits` 轮转归档（保留最近 12 个月） | `python engine/tools/archive_reports.py --audit-docs` | 已实施 |

## 二、吸收项 ① .. ④

| 编号 | 吸收项 | 任务 / 产物 | 验收命令 | 状态 |
|---|---|---|---|---|
| ① | 任务计划工件（plan/tasks/risks + 任务启动文件） | Phase 1.1：`task_plan.py`（置于 `engine/tools/`）→ `engine/audit/records/` 下的 `tasks/<slug>/` 子目录 | `task_plan.py --help`（置于 `engine/tools/`） | 已实施 |
| ② | 本地 mainline 编排脚本 | Phase 1.2：`local_mainline.py`（置于 `engine/tools/`；薄封装，复用 `repo_sync` / `optimization_gate`） | `local_mainline.py --help`（置于 `engine/tools/`） | 已实施 |
| ③ | 完成前审计证据索引 | Phase 2.1：`audit_tool` evidence index + `audit_registry.evidence`；本轮收口 `plan.reports` 关联汇聚（修复 31/31 恒空） | `python engine/audit/scripts/audit_tool.py evidence <report>` | 已实施 |
| ④ | 分支登记册语义对齐 | 既有 `branch_registry.json` + BRANCH-NAMING-SPEC v1.0 | `python engine/tools/repo_sync.py branches` | 已复用 |

## 三、Phase 任务 0.1 .. 3.3

| 编号 | 任务 | 产物 | 验收命令 | 状态 |
|---|---|---|---|---|
| 0.1 | 审计登记册失效清理 + stale 检测 | `audit_tool.py`（`stale_paths` / `cmd_prune` / `status`） | `python engine/audit/scripts/audit_tool.py status` | 已实施 |
| 0.2 | strict 审计性能阈值 | `perf-status.json` / `perf_monitor.py` | `python engine/tools/perf_monitor.py check` | 已实施 |
| 0.3 | 修 `pipeline_runner` probe 语义 | `pipeline_runner.py`（CLI `--probe/--no-probe` 默认尊重清单） | `python engine/tools/pipeline_runner.py validate` | 已实施 |
| 0.4 | 收口「声明-实现」落差（方案 A） | `ci.yml` 增 `pipeline_runner validate` 步骤 | `grep pipeline_runner .github/workflows/ci.yml` | 已实施 |
| 1.1 | 新增 `task_plan.py` | `task_plan.py` + `test_task_plan.py`（均置于 `engine/tools/` 与 `engine/tests/`） | `python -m unittest engine.tests.test_task_plan` | 已实施 |
| 1.2 | 新增 `local_mainline.py` | `local_mainline.py` + `test_local_mainline.py`（均置于 `engine/tools/` 与 `engine/tests/`） | `python -m unittest engine.tests.test_local_mainline` | 已实施 |
| 1.3 | AGENTS.md 增「任务级闭环」硬性约束节 | `AGENTS.md` / `report-pipeline-system.md` N0.5 | `python engine/tools/check_links.py` | 已实施 |
| 2.1 | `audit_tool` 增 evidence index | `audit_tool.py` + `audit_registry.json` `evidence` 字段 | `python engine/audit/scripts/audit_tool.py evidence` | 已实施 |
| 2.2 | L3 瓶颈专项 | 10 份 `in-review` 批量补 L3 + SLA 写入规范 | `python engine/audit/scripts/audit_tool.py accept` | 已实施 |
| 2.3 | 登记册清理纳入维护流水线 | `scheduled-maintenance.yml` stale 检测步骤 | `grep audit_tool .github/workflows/scheduled-maintenance.yml` | 已实施 |
| 3.1 | ruff / mypy 纳入统一门禁 | `optimization_gate.CHECKS` + `static_check.py` + `pyproject.toml` | `python engine/tools/optimization_gate.py --only ruff,mypy` | 已实施 |
| 3.2 | `report-audits` 轮转归档 | `archive_reports.py --audit-docs` | `python engine/tools/archive_reports.py --audit-docs` | 已实施 |
| 3.3 | 规范上位-下位收敛 | `AGENTS.md` 精简 + 专用规范下沉 | `python engine/tools/check_links.py` | 已实施 |

## 四、配套 CI/CD 改造点

| 工作流 | 改造 | 状态 |
|---|---|---|
| `ci.yml` | 增 `pipeline_runner validate`（0.4 方案 A）；增 ruff/mypy 步骤（3.1，经统一门禁承载） | 已实施 |
| `scheduled-maintenance.yml` | 增 stale 检测（2.3）；增 `archive_reports --audit-docs`（3.2）；保留 `pipeline_audit --rotate` | 已实施 |
| `audit.yml` | 接入 evidence index（2.1）；strict 性能阈值护栏（0.2，经 `perf_monitor` 统一门禁承载） | 已实施 |
| `submit-pr` | **不改动**：已对齐（CI 分支 + PR + auto-merge，固定 SHA） | 已复用 |
| `workspace-cleanup` | **不改动**：已对齐（只删未跟踪路径，预/收尾双触发） | 已复用 |
| `remediation-ticket` | **不改动**：已对齐（幂等建 Issue，只通知不提交代码） | 已复用 |

## 五、配套流程治理标准 1 .. 5

| # | 标准 | 落地 | 状态 |
|---|---|---|---|
| 1 | 工件即门禁输入：无 `plan.json` 不得 `repo_sync run --gate` | `repo_sync.run` 增计划校验（`task/*` 分支 + `--gate`），`local_mainline` 强制计划 | 已实施 |
| 2 | 单一事实源：任务工件 schema 由 `task_plan.py` 定义 | `task_plan.py` schema + 其余位置只指针 | 已实施 |
| 3 | 复用纪律：`local_mainline.py` 只编排，禁止重写校验 | 单测锁定「门禁仍走 `optimization_gate`」 | 已实施 |
| 4 | 版本治理：核验 / 收敛不升级版本号 | 既有 `report-pipeline-system.md` §六 | 已复用 |
| 5 | 新增即删旧：每新增一层规范，同步删除等量旧表述 | Phase 3.3 执行并记录删改点（见 §十） | 已实施 |

## 六、风险 6 项

| # | 风险 | 缓解 | 状态 |
|---|---|---|---|
| R1 | 任务工件沦为形式主义 | 「工件即门禁输入」+ 任务启动文件强制 | 已实施 |
| R2 | 双入口漂移 | `local_mainline.py` 只编排；测试锁定复用关系 | 已实施 |
| R3 | L3 瓶颈不解决 | SLA（每两周）+ 批量复核 + `audit_tool l3-status` 接线维护流水线 | 已实施 |
| R4 | 规范复杂度再增 | 「新增即删旧」；版本治理 | 已实施 |
| R5 | 多会话并发写 | 文件编辑锁 / 会话协调 | 显式延后（见 P-09） |
| R6 | 吸收式融合被误读为全量替换 | 本矩阵 + AGENTS.md 明确「主体保留、增量吸收」 | 已实施 |

## 七、量化指标 10 项（实测结果见§九）

| # | 指标 | 现状 | 目标 | 验证方式 | 状态 |
|---|---|---|---|---|---|
| M1 | 审计登记册失效条目 | 2 | 0 | `audit_tool status` | 已实施 |
| M2 | 有效报告「已审计」覆盖率 | 0/10 | ≥90% | `audit_tool accept` | 已实施 |
| M3 | 本地一次任务闭环操作数 | ~6 条 | 1 条 | `local_mainline.py` | 已实施 |
| M4 | strict 审计性能护栏 | 无阈值 | p95 ≤180s 有阈值 | `perf_monitor check` | 已实施 |
| M5 | 门禁噪声（validate 警告） | 0 | 保持 0 | `validate.py` | 已复用 |
| M6 | 规范复述点 | 多处残留 | 0 | `check_links` + `test_pipeline_system_doc` 门禁数量一致性 | 已实施 |
| M7 | 统一门禁错误项 | 0 | 保持 0 | `optimization_gate --probe` | 已复用 |
| M8 | 单测 | 494 通过 | 保持全绿 | `unittest` | 已复用 |
| M9 | evidence.plans 关联 | 31/31 恒空 | 关联报告非空 | `audit_tool.py evidence <report>` | 已实施 |
| M10 | L3 SLA 接线 | 未接线 | 维护流水线告警 | `audit_tool.py l3-status` | 已实施 |

## 八、Phase 门禁记录

| Phase | 统一门禁 `[E]` | unittest | check_links | page_build | 备注 |
|---|---|---|---|---|---|
| 基线（2026-11-17） | 0 | 448 OK（1 skip） | 通过 | 0E/0W | 见《方案》§1.6 |
| Phase 0 | 0 | 459 OK（1 skip） | 通过 | 0E/0W | — |
| Phase 1 | 0 | 478 OK（1 skip） | 通过 | 0E/0W | — |
| Phase 2 | 0 | 482 OK（1 skip） | 通过 | 0E/0W | — |
| Phase 3 | 0 | 493 OK（1 skip） | 通过 | 0E/0W | — |

## 九、量化指标实测结果

> 实测时点：2026-11-17（Phase 0–3 全部合并后，mainline 吸收式融合收口轮）。
> 实测分支：`task/fix-alignment-b30cfd92`。

| # | 指标 | 命令 | 实测输出 | 判定 |
|---|---|---|---|---|
| M1 | 审计登记册失效条目 | `python engine/audit/scripts/audit_tool.py status` | `登记 31 条；失效条目（stale）：0；含证据索引：31` | 达标（0） |
| M2 | 有效报告「已审计」覆盖率 | `python engine/audit/scripts/audit_tool.py accept` | 正式报告已审计率 `10/10 = 100.0%`；登记覆盖率 `31/31 = 100.0%`；标识一致率 `10/10` | 达标（≥90%） |
| M3 | 本地一次任务闭环操作数 | `python engine/tools/local_mainline.py run --slug <slug> --title ... --dry-run` | 1 条命令编排 5 步（plan → unittest → gate → push → pr） | 达标（1 条） |
| M4 | strict 审计性能护栏 | `python engine/tools/perf_monitor.py check` | `性能阈值校验通过：全部达标`（`audit_strict_p95_ms=180000`，实测 P95 81521ms） | 达标 |
| M5 | 门禁噪声（validate 警告） | `python engine/tools/validate.py` | `结构与规范校验通过`（0 警告） | 达标（保持 0） |
| M6 | 规范复述点 | `python engine/tools/check_links.py` + `grep -c "validate、validate_layout、lint、compliance" AGENTS.md` | 链接校验通过；复述计数 `0` | 达标（0） |
| M7 | 统一门禁错误项 | `python engine/tools/optimization_gate.py --gate-period 2026-12 --source-gate-period 2027-01 --probe` | `优化流程门禁：3 项警告（不阻断）`，退出码 2，`[E]` 计数 0 | 达标（保持 0） |
| M8 | 单测 | `python -m unittest discover -s engine/tests -p "test_*.py"` | `Ran 510 tests ... OK (skipped=1)` | 达标（全绿） |
| M9 | evidence.plans 关联 | `python engine/audit/scripts/audit_tool.py evidence engine/report-audits/mainline-adoption-coverage-matrix.md` | `plans` 非空，含 `fix-alignment`（`plan.reports` 真实关联） | 达标 |
| M10 | L3 SLA 接线 | `python engine/audit/scripts/audit_tool.py l3-status` | 退出码 0（10/10 已审，无超期）；步骤已接入 `scheduled-maintenance.yml` | 达标 |

**未达标项**：无。10/10 达标。

> 注：上表 M9 实测引用的任务工件（`fix-alignment` / `phase2-evidence-index` 等）已于 2026-11-23 全部清理，`engine/audit/records/tasks/` 仅存 `.gitkeep`。`audit_tool.py evidence` 的关联机制不变（由真实 `plan.reports` 驱动），M9 结论为清理前状态。

**透明说明**：
- M2 的「已审计」为**依据既有 2026-11-16 L3 记录的回溯补录**（非本轮重新全文复核），已在 Phase 2 PR 与覆盖矩阵登记；后续按 L3 SLA（每两周）由 Agent 定期复核。
- M7 的 3 项警告为：来源登记历史死链（宽限期内）+ ruff（88）+ mypy（40），均默认 `[W]` 不阻断。

**收口轮实测（fix-gate23-replay，2026-11-17）**：

| 项 | 命令 | 实测输出 | 判定 |
|---|---|---|---|
| 门禁数量 | `python -c "import sys;sys.path.insert(0,'engine/tools');import optimization_gate as g;print(len(g.CHECKS))"` | `23` | 达标 |
| 门禁数量一致性 | `python -m unittest engine.tests.test_pipeline_system_doc -v` | `Ran 13 tests ... OK`（`offenders == {}`，含反恒真 / 放行用例） | 达标 |
| 任务工件可重放 | `python engine/tools/task_plan.py check --slug <slug>`（7 存量 + fix-gate23-replay） | 8/8 退出码 0 | 达标 |

本次收口修复两点：①《方案》§1.3 / §四 / §五 门禁数量由 21 更正为 23，与 §1.2、`optimization_gate.CHECKS` 全量对齐（§1.3 清单补齐 ruff / mypy）；② `task_plan.render_start_md` 新增「## 关联报告」段后，5 个旧任务工件（final-self-audit / fix-matrix-status / phase1-task-loop / phase3-static-linting / verification-prompt）纯渲染重写恢复可重放（tasks/risks 实质内容不变）。

## 十、规范分层删改记录（Phase 3.3，「新增即删旧」）

| 上位（AGENTS.md）删改点 | 下沉事实源 | 理由 |
|---|---|---|
| 删除完整 21→23 项门禁清单逐项罗列 | `engine/docs/report-pipeline-system.md` §3.3、`engine/docs/report-process-reuse.md` | 清单单点维护，AGENTS.md 只留入口与数量 |
| 删除 P0/P1/P2 逐项明细与复用矩阵细节 | `engine/docs/report-process-reuse.md` 第三节 | 复用映射已由专用规范承载 |
| 删除页面构建的漂移色 hex / 性能预算 / 断点细节 | `engine/docs/page-build-spec.md`、`page-build-governance.md` | 设计系统细节单点维护 |
| 删除信息分层的决策卡五字段 / 行动协议五要素全文 | `engine/templates/information-layering-spec.md`、`decision-delivery-spec.md` | 规范正文为准，AGENTS.md 留约束 |
| 删除多会话 Git 的 v1.5 钩子细节 / 分支命名细则 | `engine/docs/multi-session-git-protocol.md`、`branch-naming-and-lifecycle.md` | 协议文档为准 |
| 删除工作区清理覆盖范围逐项列表 | `engine/tools/workspace_cleanup.py --help`、`engine/docs/structure-and-naming-spec.md` | 工具与规范为准 |
| 澄清「禁止 changelog」为 mainline 阶段 8 的 tag / 发布 changelog 流程 / `RELEASES.md` | 既有根文档 `CHANGELOG.md` 不在此列（见 AGENTS.md） | 消除与仓库既有 `CHANGELOG.md` 的字面冲突 |
| 强化 `TestGateCountConsistency`：FORBIDDEN 覆盖旧门禁口径 21（项 / 门禁写法），显式放行「基线 21 项」「由 21 项更正为 23 项」，新增反恒真与放行用例；《方案》§1.3/§四/§五 由 21 更正为 23 | `engine/tests/test_pipeline_system_doc.py`、`engine/report-audits/mainline-adoption-assessment-2026-11-17.md` v1.3 | 门禁数量口径单一事实源（`optimization_gate.CHECKS` = 23），消除复述漂移且避免测试恒真 |

**保留**：四门禁脚本名（`info_density_check.py` / `fact_card_check.py` / `decision_hub_check.py` / `blind_spot_check.py`）、「信息分层与决策交付（硬性约束」、全部硬性约束与指针；由 `test_process_gates.py::test_spec_layering_declared` 锁定。

## 版本记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v0.1 | 2026-11-17 | 初始覆盖矩阵：P-01..P-10 / 吸收项①..④ / Phase 0.1..3.3 / CI 改造 / 治理标准 / 风险 / 量化指标全量映射 |
| v0.2 | 2026-11-17 | 收口轮：吸收项③ `plan.reports` 关联汇聚（修 31/31 恒空）；P-07 / M6 门禁数量 21→23 一致性（新增 `test_pipeline_system_doc` 扫描）；R3 / M10 `l3-status` 接线维护流水线；§九 实测更新（unittest 510、evidence.plans 非空、L3 SLA 接线）；§十 增记 AGENTS.md「禁止 changelog」措辞澄清 |
| v0.3 | 2026-11-17 | 收口轮（fix-gate23-replay）：《方案》升 v1.3，§1.3 / §四 / §五 门禁数量 21→23 全量对齐；强化 `TestGateCountConsistency`（FORBIDDEN 覆盖旧门禁口径 21 的项 / 门禁写法 + 显式放行基线 / 更正表述 + 反恒真用例）；5 个旧任务工件纯渲染重写恢复可重放；§九 增收口轮实测、§十 增收改记录 |
