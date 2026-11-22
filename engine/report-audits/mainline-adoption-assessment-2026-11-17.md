# mainline 规范适配性评估（MAINLINE-ADOPTION-ASSESSMENT 2026-11-17）

> **状态**：现行评估
> **评估对象**：`portable-11-stage-mainline-spec-pack.md`（11 阶段 mainline 开发流程规范包） ↔ `tech-context-digest` 现有 CI/CD 全流程。
> **评估方法**：静态通读（`AGENTS.md` / `engine/docs/**` / `engine/tools/**` / `.github/workflows/**` / `.github/actions/**` / `.githooks/**` / `engine/tests/**`）+ 本机实跑回归（单测 / 门禁 / 审计登记 / 性能基线）+ 工具代码核查。
> **基线时点**：2026-11-17（工作树干净，`main` = `5fadf67`）。
> **结论摘要**：**不建议以 mainline 规范为核心做整体融合（替换）**；建议做一次**吸收式融合**——保留现有 N0–N8 体系为主体，选择性接入 mainline 的三项任务级闭环机制（计划工件 / 本地 mainline 编排 / 完成前证据索引）。

---

## 一、现有 CI/CD 全流程梳理

### 1.1 仓库性质判定

本仓库**不是**传统软件发布仓库，而是**「内容生产 + 工具链 + CI 编排」混合仓库**：

- **交付物**：自包含 HTML 报告（CSS/JS 内联，ECharts 走 CDN 白名单）+ 静态枢纽 `index.html` / `reader.html`。
- **引擎层是真实软件代码**：`engine/tools/*.py`（41 个脚本 + `semantic_checks/` 包）+ `engine/tests/`（448 用例），标准库为主，依赖仅 openpyxl / markdown / PyYAML。
- **通信形态**：无网络 RPC / 消息队列 / 数据库；进程间 `subprocess`（门禁调子进程）+ 文件契约（JSON/MD/HTML）+ Git/PR + GitHub API/webhook。

这一双重属性是后文所有适配性判断的前提：**内容线**与 mainline 不适配，**引擎线**与 mainline 高度适配。

### 1.2 主链与门禁（N0–N8 × 五道防线）

事实源：`engine/docs/report-pipeline-system.md`（REPORT-PIPELINE-SYSTEM v1.2）、`engine/tools/pipeline_manifest.json`（声明式 9 节点 / 9 门禁 / 2 闭环）。

| 节点 | 名称 | 就地门禁 | 主要防线 |
|---|---|---|---|
| N0 | 需求与配置 | G0 配置校验 | `validate_layout` / `validate` / 提示词继承 |
| N1 | 信息采集 | G1 来源登记 | `source_check` R1–R5,R7 / `release_calendar` / `metric_registry` |
| N2 | 信息筛选与分级 | G2 分级·双源·死链 | `source_check` R2,R3,R6（`--probe`） |
| N3 | 信息分类 | G3 分类·归位·断链 | `classify` / `validate_layout` / `check_links` |
| N4 | 内容生成 | G4 内容四门禁 + 研究内核 | `research_kernel` / `info_density` / `fact_card` / `decision_hub` / `blind_spot` |
| N5 | 渲染与交付 | G5 页面·合规·性能 | `page_build_check` / `lint` / `compliance` / `perf_monitor` |
| N6 | 质量校验与审计（兜底） | G6 统一门禁 + 审计 | **统一门禁 32 项**（基线 21 项，Phase 3.1 起 32 项）+ 审计四环节（L1/L2/L3 + A1–A8） |
| N7 | 发布 / 索引 / 归档 | G7 产物确定性 | `build_hub --check` / 发布指纹 / 归档 |
| N8 | 运维与监控 | G8 运维·告警 | 6 工作流 + 活跃度 + 告警 |

**门禁左移**：G0–G5 为生产阶段出口拦截（短回路退回本阶段）；G6–G8 为兜底/出口守卫。两级 gate-period（内容 2026-12 / 来源 2027-01）实现「历史报告 `[W]` 不追溯、新报告 `[E]` 阻断」。

### 1.3 统一门禁单一入口（`optimization_gate.py`）

- **32 项**（基线 21 项，Phase 3.1 起 32 项）：validate / validate_layout / lint / compliance / classify / period_check / region_topics / links / hub / page_build / source_check / verification_ledger / metric_registry / metric_audit / release_calendar / publish_fingerprint / semantic_diff / perf_monitor / research_kernel / info_density / fact_card / report_verification / decision_hub / blind_spot / ruff / mypy。
- **退出码**：0 通过；1 有 `[E]`（阻断）；2 仅 `[W]`（放行）。`warn_ok` 仅 `links` / `hub` / `metric_registry` 不容忍 exit 2。
- **复用矩阵**：`repo_sync run --gate`（本地提交）、`ci.yml` / `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml`（CI 步骤）、`audit_tool._run_gate()`（审计内部）。
- **一致性强制**：`engine/tests/test_process_gates.py::TestOptimizationGateReuse` 锁定「四门禁必须在 `CHECKS`、四工作流必须调用统一入口且不得分项重复」。

### 1.4 六条工作流与三个复合动作

| 工作流 | 触发 | 关键动作 | 阻断 |
|---|---|---|---|
| `ci.yml` | push(main) / PR | `py_compile` → `unittest` → **统一门禁 `--probe`** → commit status | `[E]` 阻断 |
| `html-sync.yml` | 报告/生成器变更 | `md2html` → `build_hub` → 指纹 → 统一门禁 → `submit-pr` | `[E]` 阻断 |
| `content-update.yml` | 每月 1 日 / dispatch | 归位 → 维护流水线 → 统一门禁 → 任务清单 Issue → `submit-pr` | `[E]` 阻断 |
| `scheduled-maintenance.yml` | 每周一 02:30 UTC | 结构补全 → 归位 → 维护流水线 → 统一门禁 → 合规审计 → 单测 → 性能 → 活跃度 → `submit-pr` | `[E]` 阻断 |
| `audit.yml` | 报告变更 | `audit_tool run --strict`（四环节 fail-fast）+ `accept` + `submit-pr` | `[E]` 或超 L3 宽限 |
| `webhook-alert.yml` | 上述失败 | 建 Issue / webhook | — |

复合动作：`submit-pr`（CI 分支 + PR + auto-merge，固定 SHA `actions/github-script`）、`workspace-cleanup`（只删未跟踪路径，预/收尾双触发）、`remediation-ticket`（幂等建修复 Issue，只通知不提交代码）。

### 1.5 Git 协作治理

- **三层隔离**：分支隔离（`task/<slug>-<session8>`）+ 串行合并（PR + 合并队列 + 分支保护 strict）+ 共享检出锁（`.git/catpaw-sync.lock`，TTL 600s）。
- **统一网关**：`engine/tools/repo_sync.py`（run / push / pr / branch / branch-rename / branch-audit / hook-install / guard）。
- **钩子**：`pre-push` 按 refspec 判定（直推 main、GitLab 远端、命名不符即阻断）；`pre-commit` 校受管分支命名。
- **分支登记册**：`engine/tools/branch_registry.json`（BRANCH-NAMING-SPEC v1.0，合并/删除后保留为历史台账）。
- **CI 也走 PR**：4 个自动提交工作流经 `submit-pr` 开 PR + auto-merge，不直推 main。

### 1.6 实际运行痛点（均含实证）

| 编号 | 痛点 | 证据 | 影响 |
|---|---|---|---|
| **P-01** | **审计登记册含失效条目**：31 条登记中 2 条指向已删除文件（原 `real-estate` 业务线下的 market-sizing 与 policy-analysis 两份基线报告），却被标 `audited` | `engine/audit/records/audit_registry.json`；`real-estate` 目录已不存在 | 审计留痕可信度受损；重构后未清理登记册 |
| **P-02** | **「已审计」实际覆盖率≈0**：11 份有效正式报告全部停在 `in-review 3/4`（缺 final 终审）；仅有的 2 条 `audited` 是失效路径 | `audit_tool.py status` | G6 审计防线名义存在、实际未收敛；L3 语义终审是瓶颈 |
| **P-03** | **strict 审计耗时无阈值**：`audit_run_strict` p95 ≈ 81.5s，而 `perf_monitor` 阈值只覆盖 `l0_l1_full` / `single_report_l1` / `error_rate` | `perf-status.json`；`engine/tools/perf_monitor.py:71-73` | `audit.yml` 关键路径无性能护栏 |
| **P-04** | **声明与实现落差**：AGENTS.md 把「统一网关 `repo_sync`」「端到端编排 `pipeline_runner`」列为硬性约束，但 CI 侧只调用 `pipeline_audit --rotate` 与钩子 `repo_sync guard`；`pipeline_runner` / `repo_sync run|push|pr` 在 6 条工作流中**零调用** | `grep -rn repo_sync\|pipeline_runner .github` | 规范承诺 > 实际约束；「端到端一键跑通」并未落地 |
| **P-05** | **任务级闭环工件缺失**：无 `plan.json` / `tasks.json` / `risks.json` / 任务启动文件；任务计划靠 `update_planner`（周期维护清单）+ `remediation_ticket`（异常工单），非「每次任务必产出」 | `git ls-files \| grep -iE "plan\|tasks\|risks\|mainline"` 无命中 | 任务上下文散落会话/Issue，多会话协作可追溯性弱 |
| **P-06** | **门禁清单 / 类型注册多点手工同步**：`optimization_gate.CHECKS`、`template-registry.md` 第二节、`compliance-rules.json`、`_common.TEMPLATE_TYPE_DIRS`、`build_hub.TYPE_SHORT` 需手工对齐 | `optimization_gate.py:41-63`；`build_hub.py:42-57` | 扩展易漏改（F-08/17/18/19） |
| **P-07** | **规范复述漂移**：同一事实在 AGENTS.md / structure-and-naming-spec / report-pipeline-system / page-build-spec 多处复述 | F-02/21 遗留 | 改一处漏一处，文档可信度下降 |
| **P-08** | **无静态检查**：无 ruff / mypy 配置与 CI 步骤（`workspace_cleanup` 覆盖其缓存但无检查） | `ci.yml` 仅 `py_compile` | 类型错误 / 未用导入无拦截 |
| **P-09** | **多会话并发写同一工作树**：共享检出锁只覆盖 git 操作，不覆盖文件编辑 | 既有评估 F-09/29 实测 | 并行会话可互相覆盖，基线漂移 |
| **P-10** | **审计文档累积无轮转**：`engine/report-audits/` 19 份文档（含 14 份时点报告），无归档策略（仅 `pipeline_runs.jsonl` 有 `--rotate`） | `ls engine/report-audits` | 时点报告越积越多 |

**实测基线（2026-11-17）**：`unittest` **448 通过 / 1 跳过 / 0 失败**（22.9s）；`validate.py` **0 警告**（F-01 已收口）；统一门禁 **0 错误**；`l0_l1_full` p95 **1416ms**；`page_build_check` 0E/0W；7 业务线 / 13 报告（10 正式 + 3 legacy）。

---

## 二、mainline 11 阶段规范要点

来源：`portable-11-stage-mainline-spec-pack.md`。其核心是**软件交付范式**：以「任务」为单位，强制「计划 → TDD → 本地 mainline → 集成 → 合并 → 发布 → PR 验证 → 清理 → 完成审计」的闭环，并把 `plan.json` / `tasks.json` / `risks.json` / 任务启动文件作为**完成定义（DoD）的强制证据**。

| 阶段 | 核心动作 | 强制工件 / 门禁 |
|---|---|---|
| 1 问题定义 | 明确问题 / 验收标准 / 复现 | Issue + 验收标准 |
| 2 计划与准备 | 生成计划与任务分解、风险登记 | `plan.json` / `tasks.json` / `risks.json` / 任务启动文件；每步前跑 `verify_plan_step.sh` |
| 3 分支与配置 | 从 main 建任务分支、登记 | 分支登记册 + 命名规范 |
| 4 TDD 循环 | 红-绿-重构，测试先行 | 失败测试 → 实现 → 通过；测试证据 |
| 5 本地 mainline | 本地跑完整验证后推分支 | `plan→tdd→integration→push→verify` 一键脚本 |
| 6 集成与验证 | CI 集成、跨模块验证 | `integrate` + `verify_mainline.sh` |
| 7 合并到 mainline | 合并并确认 main 健康 | 合并队列 / 手动 merge |
| 8 发布与确认 | 打 tag / changelog / 发布说明 | `changelog` / `tag` / `alias` / `RELEASES.md` |
| 9 PR 验证 | PR 检查与评审 | 必需检查 + 评审 |
| 10 清理 | 清理分支 / 临时产物 | 分支删除 + 登记册维护 |
| 11 完成定义与审计 | 完成前审计与证据索引 | 证据索引 + pending review |

---

## 三、逐阶段对照矩阵

| mainline 阶段 | 本仓库对应实现 | 覆盖度 | 差距判定 |
|---|---|---|---|
| 1 问题定义 | `remediation_ticket`（异常工单）+ Issue + `update_planner`（周期清单） | 中 | 无「每次任务必产出的计划工件」 |
| 2 计划与准备 | `update_planner`（仅周期维护） | **低** | **缺 `plan/tasks/risks` 三件套与任务启动文件** |
| 3 分支与配置 | `repo_sync branch` + `branch_registry.json` + 钩子三重拦截 | **高** | 已对齐，语义等价（甚至多一层钩子） |
| 4 TDD 循环 | `unittest`（448 项，事后执行） | 中 | 无「红-绿-重构」强制与任务级测试证据；引擎线适配、内容线不适配 |
| 5 本地 mainline | `optimization_gate --probe` + `repo_sync run/push` | 中 | 无「一键串联」入口，命令散落 6 条 |
| 6 集成与验证 | `ci.yml`（syntax/test/gate）+ `audit.yml`（strict） | **高** | 已对齐；缺任务级「集成验证脚本」封装 |
| 7 合并到 mainline | `submit-pr` + 合并队列 + 分支保护 strict | **高** | 已对齐（merge queue 优于手动 merge） |
| 8 发布与确认 | `publish_fingerprint` + `build_hub` + `build_index` + 归档 | 中 | 缺 `tag/changelog/RELEASES.md`；**内容仓库无版本发布需求** |
| 9 PR 验证 | `ci.yml` 三作业 + commit status | **高** | 已对齐 |
| 10 清理 | `workspace_cleanup` + 分支删除 + 登记册保留策略 | **高** | 已对齐（登记册保留策略已明确） |
| 11 完成定义与审计 | `audit_tool` 四环节 + `audit_registry` 三态标识 | 中 | 缺「完成前证据索引」；且 **L3 终审阻塞**（P-02） |

**结论**：约 **60% 阶段已对齐或更强**（3/6/7/9/10 + 统一门禁），**40% 不适配或缺失**（2/4/5/8/11）。

---

## 四、五维评估

| 维度 | 评分 | 判断 |
|---|---|---|
| **流程适配性** | 中 | mainline 是软件交付范式（TDD / release tag / changelog / 11 阶段硬编码）；本仓库是内容生产 + 工具链。内容线 40% 不适配（报告不是代码，TDD 不适用；无版本发布需求）。引擎线高度适配。 |
| **落地成本** | 高 | 需重写规范体系（AGENTS.md + 6 份 docs + manifest）、改造 6 工作流、新增三件套生成器与本地 mainline 脚本、重训团队习惯；而现有体系已 448 单测 + 24 门禁（基线 21）+ 6 工作流稳定运行。 |
| **团队协作效率** | 中（有明确增量） | mainline 的任务级工件（plan/tasks/risks）正是当前缺口（P-05），能提升多会话可追溯性；但可用更轻量方式吸收，无需整体替换。 |
| **质量保障能力** | 现有**更强** | 现有 5 防线 + 24 门禁 + 审计四环节 + 两级 gate-period，显著强于 mainline 的「单测 + 本地脚本」。以 mainline 为核心替换等于**降级**。 |
| **长期可维护性** | 中偏负 | 规范已过剩（P-07/21），再叠加 11 阶段 + 三件套会加剧复杂度与漂移；但「分支登记册 + 完成前证据索引」对长期审计有利，值得吸收。 |

---

## 五、结论

### 5.1 核心结论

**不需要以 mainline 规范为核心做整体融合（替换）。** 三条核心原因：

1. **质量保障会降级**：现有 5 道防线 / 32 项统一门禁 / 审计四环节 / 两级 gate-period 在「内容生产」维度上**强于** mainline 的质量门（单测 + 本地脚本）。以 mainline 为核心替换，等于用简化门禁替换成熟门禁。
2. **40% 阶段与仓库性质不适配**：TDD 不适用于报告内容生成；`tag/changelog/RELEASES.md` 对静态 HTML 交付物无意义。强行套用会制造形式主义工件，反而增加负担。
3. **落地成本 > 收益，且规范已过载**：现有体系已稳定运行且经 448 单测锁定；再引入 11 阶段 + 三件套会加剧「规范复述漂移」（P-07），与长期可维护性目标冲突。

### 5.2 但需要做「吸收式融合」（selective adoption）

保留现有 N0–N8 体系为**主体**，把 mainline 的三项**增量机制**作为「任务级闭环层」接入：

| 吸收项 | 来源阶段 | 接入位置 | 价值 |
|---|---|---|---|
| ① 任务计划工件（`plan/tasks/risks` + 任务启动文件） | 阶段 2 | 新增 N0.5「任务计划」子节点（新增 `task_plan.py`，置于 `engine/tools/`） | 补 P-05，任务上下文可回溯 |
| ② 本地 mainline 编排脚本（`plan→unittest→gate→push→pr→verify` 一键） | 阶段 5 | 新增 `local_mainline.py`（置于 `engine/tools/`；薄封装，复用 `repo_sync` / `optimization_gate`） | 补 P-04/P-05，命令收敛为一条 |
| ③ 完成前审计证据索引（evidence index） | 阶段 11 | 扩展 `audit_tool` / `audit_registry` | 补 P-01/P-02，审计可信、可追溯 |
| ④ 分支登记册语义对齐 | 阶段 3 | 复用既有 `branch_registry.json` | 已对齐，补文档映射即可 |

**明确不吸收**：阶段 4 的「TDD 强制」不用于内容线（仅建议引擎线遵循）；阶段 8 的 `tag/changelog/alias/RELEASES.md` 不引入（无版本发布需求）；11 阶段硬编码不替换 9 节点 + 5 防线。

---

## 六、优化路线图（分阶段落地）

### Phase 0 — 治理收口（P0，1 周内，零架构改动）

| # | 任务 | 改造点 | 验收 |
|---|---|---|---|
| 0.1 | 清理审计登记册失效条目 | `engine/audit/records/audit_registry.json` 移除 2 条 `real-estate` 失效记录；`audit_tool` 增加 **stale 检测**（登记路径不存在 → `[W]`/`[E]`） | 登记 31→29，全部路径存在；stale 检测纳入 `audit_tool status` |
| 0.2 | 补 strict 审计性能阈值 | `perf-status.json` 增 `audit_strict_p95_ms`（建议 ≤180000）；`perf_monitor.check_thresholds` 增对应规则 | 阈值校验生效；`audit.yml` 有护栏 |
| 0.3 | 修 `pipeline_runner` probe 语义 | `gate` 子命令默认 `probe=False` 覆盖了 manifest 的 `probe:true`（`pipeline_runner.py:226,361`）；改为尊重清单 | `pipeline_runner validate` 通过且 probe 语义一致 |
| 0.4 | 收口「声明-实现」落差 | 二选一：① 在 `ci.yml` 增 `pipeline_runner validate` 步骤（低成本，落地端到端编排）；② 在 AGENTS.md 标注「`pipeline_runner` 为可选演练入口，CI 直连统一门禁」 | 文档口径与 CI 实际一致 |

### Phase 1 — 任务级闭环层（P1，2 周内）

| # | 任务 | 改造点 | 验收 |
|---|---|---|---|
| 1.1 | 新增 `task_plan.py`（置于 `engine/tools/`） | 生成 `plan.json` / `tasks.json` / `risks.json` 与任务启动文件（落 `engine/audit/records/` 下的 `tasks/<slug>/`） | 测试 `test_task_plan.py`；工件 schema 固定 |
| 1.2 | 新增 `local_mainline.py`（置于 `engine/tools/`） | 薄封装：`plan → unittest → optimization_gate --probe → repo_sync push → repo_sync pr`；**不重写任何校验逻辑** | 测试 `test_local_mainline.py`；一键闭环可跑通 |
| 1.3 | AGENTS.md 增「任务级闭环（适配 mainline）」硬性约束节 | 声明与 N0–N8 的映射、工件位置、复用入口 | `check_links` 通过；`test_process_gates.py` 增补复用断言 |

### Phase 2 — 完成前审计证据索引（P2，2–3 周）

| # | 任务 | 改造点 | 验收 |
|---|---|---|---|
| 2.1 | `audit_tool` 增 evidence index | 每份报告/每次任务关联 `plan/tasks/risks` + 门禁输出 + 审计记录链接 | `audit_registry` 增 `evidence` 字段；`status` 可打印 |
| 2.2 | L3 瓶颈专项 | 对 10 份 `in-review` 批量补 L3 语义终审；或明确「L3 由 Agent 定期执行」SLA（建议每两周） | 有效报告 `audited` 覆盖率 ≥90% |
| 2.3 | 审计登记册清理纳入维护流水线 | `scheduled-maintenance` 增 stale 检测步骤（复用 `audit_tool`） | 登记册无失效条目 |

### Phase 3 — 静态检查与规范分层（P3，持续）

| # | 任务 | 改造点 | 验收 |
|---|---|---|---|
| 3.1 | ruff / mypy 纳入统一门禁 | `optimization_gate.CHECKS` 增两项（默认 `[W]`，稳定后升 `[E]`） | 测试锁定门禁数量 |
| 3.2 | `report-audits` 轮转归档 | 扩展 `archive_reports.py` 或新增轮转；保留最近 12 个月在根 | 归档幂等 |
| 3.3 | 规范上位-下位收敛 | AGENTS.md 只留硬性约束 + 指针；细节下沉专用规范 | 复述点清零 |

### 配套 CI/CD 改造点汇总

| 工作流 | 改造 |
|---|---|
| `ci.yml` | 增 `pipeline_runner validate`（0.4 选①时）；增 `ruff`/`mypy` 步骤（3.1） |
| `scheduled-maintenance.yml` | 增 stale 检测（2.3）；`pipeline_audit --rotate` 保留 |
| `audit.yml` | 接入 evidence index（2.1）；strict 性能阈值护栏（0.2） |
| `submit-pr` / `workspace-cleanup` / `remediation-ticket` | 不改动（已对齐） |

### 配套流程治理标准

1. **工件即门禁输入**：无 `plan.json` 不得执行 `repo_sync run --gate`（防形式主义）。
2. **单一事实源**：任务工件 schema 由 `task_plan.py` 定义，其余位置只指针。
3. **复用纪律**：`local_mainline.py` 只做编排，禁止重写校验；测试锁定「门禁仍走 `optimization_gate`」。
4. **版本治理**：核验/收敛不升级版本号；仅核心事实修正才升级。
5. **新增即删旧**：每新增一层规范，必须同步删除等量旧表述（控复杂度）。

---

## 七、风险点

| 风险 | 说明 | 缓解 |
|---|---|---|
| 任务工件沦为形式主义 | 为建而建、与实际任务脱节 | 「工件即门禁输入」+ 任务启动文件强制 |
| 双入口漂移 | `local_mainline.py` 与 `repo_sync` 各写一套 | 脚本只做编排；测试锁定复用关系 |
| L3 瓶颈不解决 | 审计覆盖率难提升，P-02 延续 | 设 SLA + 批量复核；明确 Agent 定期执行 |
| 规范复杂度再增 | 与 P-07 冲突 | 严格「新增即删旧」；版本治理 |
| 多会话并发写 | 锁不覆盖文件编辑（P-09） | 建议引入文件编辑锁或会话协调（既有评估方向 B） |
| 吸收式融合被误读为全量替换 | 团队按 mainline 11 阶段重建 | 本评估 + AGENTS.md 明确「主体保留、增量吸收」 |

---

## 八、预期收益量化指标

| 指标 | 现状（2026-11-17） | 目标 | 验证方式 |
|---|---|---|---|
| 审计登记册失效条目 | 2 | **0** | `audit_tool status` stale 检测 |
| 有效报告「已审计」覆盖率 | 0/11（≈0%） | **≥90%** | `audit_tool status` 4/4 计数 |
| 本地一次任务闭环操作数 | ~6 条命令 | **1 条** | `local_mainline.py` 一键 |
| strict 审计性能护栏 | 无阈值 | **p95 ≤180s 有阈值** | `perf_monitor` |
| 门禁噪声（validate 警告） | 0（已收口） | 保持 0 | `validate.py` |
| 规范复述点 | 多处残留 | **0** | `check_links` + 人工核查 |
| 统一门禁错误项 | 0 | 保持 0 | `optimization_gate --probe` |
| 单测 | 448 通过 | 保持全绿 | `unittest` |

---

## 版本记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-11-17 | 初始评估：现有流程梳理、11 阶段对照、五维评估、结论（不整体融合 + 吸收式融合）、四阶段路线图、风险与量化收益 |
| v1.1 | 2026-11-17 | 实施回写：Phase 0–3 全部落地（吸收式融合，**主体 N0–N8 保留**）。Phase 0.4 选**方案 A**（`ci.yml` 增 `pipeline_runner validate`）；Phase 2.2 L3 采用「依据 2026-11-16 L3 记录批量补审 + 每两周 SLA」；P-06（注册结构化）/ P-09（并发写）**显式延后**（理由与归属见覆盖矩阵）。逐项状态与实测见 [覆盖矩阵](./mainline-adoption-coverage-matrix.md)。 |
| v1.2 | 2026-11-17 | 核心事实修正：§1.2 统一门禁数量由 21 项更正为 **29 项**（基线 21 项，Phase 3.1 起 29 项）；收口轮修复证据索引 `plan.reports` 关联、L3 SLA 接线、任务启动文件四件套强制与门禁数量复述漂移，见 [覆盖矩阵](./mainline-adoption-coverage-matrix.md) v0.2。 |
| v1.3 | 2026-11-17 | 门禁数量复述收口：§1.3 / §四 / §五 由 21 更正为 23，与 §1.2、`optimization_gate.CHECKS` 全量对齐（§1.3 清单补齐 ruff / mypy 两项）。 |
