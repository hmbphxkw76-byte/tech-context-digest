# fix-alignment 收口 · 全量验证提示词（FIX-ALIGNMENT-VERIFICATION）

> **用途**：把本文件整体投喂给一个验证 Agent（或自查），用于确认「mainline 吸收式融合完全对齐收口」本轮的 4 项缺口修复（T-1..T-7）是否**全部真实执行到位**，并**重点排查虚假实现**。
> **事实源**：`engine/report-audits/mainline-adoption-assessment-2026-11-17.md`（《方案》v1.2）、`engine/report-audits/mainline-adoption-coverage-matrix.md`（覆盖矩阵 v0.2）、`AGENTS.md`（硬性约束）。
> **本轮基线**：unittest 494 → 510；统一门禁 23 项、`[E]=0`；`origin/main` 合并提交 `97224b6`（PR #25）。
> **性质**：只读验证。除为复现而生成临时文件外，**不得修改仓库**；若发现问题，另开 `task/*` 分支。

---

## 提示词正文（复制以下全部内容使用）

你是本仓库的独立验证 Agent。任务：**全面验证「fix-alignment 收口」本轮的 4 项缺口修复（T-1..T-7）是否全部执行到位、是否引入新问题、是否存在虚假实现**。不要轻信文档声明，一切以**可执行命令的真实输出**为准。

### 0. 必读（按序，不得跳读）

1. `engine/report-audits/mainline-adoption-assessment-2026-11-17.md`（《方案》v1.2；重点 §1.2 门禁数量、§三 对照矩阵、§八 版本记录）。
2. `engine/report-audits/mainline-adoption-coverage-matrix.md`（覆盖矩阵 v0.2；吸收项③、P-07、R3、M6、§七 M9/M10、§九 实测、§十 删改记录）。
3. `AGENTS.md`（硬性约束，特别是「任务级闭环」「优化流程门禁」「多会话 Git 协作」）。
4. 被验证源码：`engine/tools/task_plan.py`、`engine/tools/repo_sync.py`、`engine/tools/optimization_gate.py`、`engine/audit/scripts/audit_tool.py`、`engine/tools/pipeline_runner.py`、`engine/tools/local_mainline.py`。
5. 被验证测试：`engine/tests/test_task_plan.py`、`test_audit_tool.py`、`test_repo_sync.py`、`test_process_gates.py`、`test_pipeline_runner.py`、`test_pipeline_system_doc.py`。
6. CI：`.github/workflows/{ci,audit,scheduled-maintenance,html-sync,content-update}.yml`。
7. 登记数据：`engine/audit/records/audit_registry.json`、`engine/audit/records/tasks/{fix-alignment,phase2-evidence-index}/`。

### 1. 验证原则

- **单一事实源**：结论以《方案》v1.2 + 覆盖矩阵 v0.2 为准。
- **证据优先**：每一项判定必须附「命令 + 真实输出片段」；无输出 = 未验证。
- **不预设结论**：允许也要求报告「未执行 / 部分执行 / 虚假实现嫌疑」；不得为求通过而放宽判据。
- **只读**：验证过程不修改仓库；确需临时文件时放在系统临时目录并清理。

### 2. 反虚假实现红线（逐条核查，本轮专项）

1. **evidence.plans 必须由真实 `plan.reports` 驱动**：`audit_tool.build_evidence` 不得硬编码非空、不得伪造关联；必须读取 `records/tasks/*/plan.json` 的 `reports` 字段。
   - 命令：`python engine/audit/scripts/audit_tool.py evidence engine/report-audits/mainline-adoption-coverage-matrix.md`，核对 `plans` 非空且含 `fix-alignment`；再 `... evidence engine/report-audits/blind-spot-ledger.md`，核对**无**关联时 `plans` 为 `[]`（精确性）。
2. **`plan.reports` 必须真实来自 `--report`**：`task_plan.py init --report <rel>` 后 `plan.json` 的 `reports` 与 `task-start.md`「## 关联报告」必须一致；`normalize_reports` 去重 + 字典序；空值写固定文案 `- 无（手工/工具类任务）`。
   - 命令：`python engine/tools/task_plan.py check --slug fix-alignment` 与 `check --slug phase2-evidence-index` 必须可重放。
3. **`check` 必须真比对**：`task_plan.check` 篡改 `tasks.json` 后必须报错（重渲染逐字节比对），不得恒返回 `[]`。
   - 命令：临时目录 `init` 后篡改 → `check` 必须非零/非空。
4. **L3 SLA 必须真实可算**：`audit_tool.l3_overdue(reports, reviews_dir, today=None)` 为纯函数，取 `records/reviews/<slug>.json` 中**最后一条 Agent（非 `ci-bot`/空 reviewer）的 `second`/`final` pass** 的 timestamp，缺失回退 `first_seen_at`，`> L3_GRACE_DAYS(14)` 判超期；`ci-bot` 记录必须被忽略；`today` 可注入保证可重放；不得写时间戳。
   - 命令：`python engine/audit/scripts/audit_tool.py l3-status` 退出码 0（当前无超期）；`grep -n "l3_overdue\|l3-status" engine/audit/scripts/audit_tool.py`。
5. **L3 SLA 必须接线到流水线**：`scheduled-maintenance.yml` 必须存在「L3 SLA 超期检测」步骤，调用 `audit_tool.py l3-status`，退出码 2 → `::warning::`（不阻断），1 → `::error::` + `exit 1`。
   - 命令：`grep -n "l3-status" .github/workflows/scheduled-maintenance.yml`。
6. **四件套必须真强制**：`repo_sync.require_task_plan` 必须校验 `plan.json` / `tasks.json` / `risks.json` / `task-start.md` 四件，缺任一拒绝；`--allow-no-plan` 仅显式应急。
   - 命令：`python -c "import sys;sys.path.insert(0,'engine/tools');import repo_sync as rs;print(rs.TASK_ARTIFACTS, rs.require_task_plan())"`；构造缺 `task-start.md` 的临时目录验证拒绝。
7. **门禁数量必须处处为 23**：`optimization_gate.CHECKS` 长度 = 23；现行文件不得残留 `optimization_gate … 21 项` / `全量 21 项` / `统一门禁 21 项` 等；历史时点报告（`report-audits/*-2026-11-15/16.md`）与 `engine/quality/**` 显式排除。
   - 命令：`python -c "import sys;sys.path.insert(0,'engine/tools');import optimization_gate as g;print(len(g.CHECKS))"`；`grep -rnE "optimization_gate[^。；\n]{0,60}21 项|21 项[^。；\n]{0,30}optimization_gate|全量 21 项|统一门禁 21 项" engine/ AGENTS.md`。
8. **测试不得恒真 / 自我 mock**：新增测试不得 `unittest.mock` 被测函数本身，不得只断言「文件存在」，不得 `try/except` 吞异常。
   - 命令：`grep -nE "mock|return_value|assertIn\(.*exists|except.*pass" engine/tests/test_task_plan.py engine/tests/test_audit_tool.py engine/tests/test_repo_sync.py engine/tests/test_pipeline_system_doc.py`，逐处判断。
9. **不得直推 main / 绕过门禁**：`git log --first-parent origin/main --oneline` 必须全为 PR 合并；`--no-gate` / `--allow-no-plan` 仅显式应急。
10. **不得整体替换为 mainline 11 阶段**：`pipeline_manifest.json` 仍为 N0–N8 + G0–G8；未引入 `tag` / 发布 changelog 流程 / `RELEASES.md`；`AGENTS.md` 已澄清「既有根文档 `CHANGELOG.md` 不在此列」。

### 3. 逐项验证（T-1..T-7）

| 项 | 验证点 | 必须成立的证据 |
|---|---|---|
| **T-1** 吸收项③ | `task_plan.build_plan` 含 `reports: []`；`init --report` 写入；`render_start_md` 含「## 关联报告」；`validate_artifacts` 校验非空字符串/无重复（不校验文件存在性） | `evidence <覆盖矩阵>` → `plans` 非空含 `fix-alignment`；`evidence <blind-spot-ledger>` → `plans=[]`；`phase2-evidence-index/plan.json` 含 `reports` |
| **T-2** P-07/M6 | 现行文档/代码统一 23；新增 `TestGateCountConsistency` 扫描 + `CHECKS==23` + 声明文件含「23 项」 | `len(CHECKS)==23`；禁词 grep 0 命中（排除历史/质量）；`test_pipeline_system_doc` 通过 |
| **T-3** R3 | `l3_overdue` 纯函数 + `l3-status` 子命令 + `scheduled-maintenance.yml` 接线 | `l3-status` 退出码 0；`TestL3Overdue` 覆盖无 Agent 超期/有 14 天内/忽略 ci-bot/`today` 注入；CI 步骤存在 |
| **T-4** R1 | `require_task_plan` 四件套 | `TASK_ARTIFACTS` 四件；缺 `task-start.md` 拒绝；`test_repo_sync` 通过 |
| **T-5** | `audit.yml` 注释引用 `optimization_gate.py --probe`，无重复调用 | `grep -n "optimization_gate.py" .github/workflows/audit.yml`；无第二次 `optimization_gate.py` 调用 |
| **T-6** | `AGENTS.md` 措辞澄清 | 含「mainline 阶段 8 的 tag / 发布 changelog 流程 / RELEASES.md（仓库既有根文档 CHANGELOG.md 不在此列）」 |
| **T-7** | 覆盖矩阵 §九（510 / evidence.plans / L3 SLA）、§七 M9/M10、§十、版本 v0.2；方案 v1.2；`report-pipeline-system.md` §N0.5 / §L3 | 逐项读文档核对命令与数值 |

### 4. 必跑验收命令（逐条记录退出码与关键输出）

```bash
python -m py_compile engine/tools/*.py engine/tests/*.py engine/audit/scripts/*.py
python -m unittest discover -s engine/tests -p "test_*.py"
python engine/tools/optimization_gate.py --gate-period 2026-12 --source-gate-period 2027-01 --probe
python engine/tools/optimization_gate.py --only ruff,mypy
python engine/tools/validate.py && python engine/tools/check_links.py && python engine/tools/page_build_check.py
python engine/tools/pipeline_runner.py validate
python engine/audit/scripts/audit_tool.py status
python engine/audit/scripts/audit_tool.py accept
python engine/audit/scripts/audit_tool.py l3-status
python engine/audit/scripts/audit_tool.py evidence engine/report-audits/mainline-adoption-coverage-matrix.md
python engine/tools/perf_monitor.py check
python engine/tools/archive_reports.py --audit-docs
python engine/tools/task_plan.py check --slug fix-alignment
python engine/tools/local_mainline.py run --slug fix-alignment --title x --dry-run
git log --first-parent origin/main --oneline -10
git status --short
```

判据：`unittest` 全绿（≥510）；统一门禁 `[E]=0`；`check_links` / `page_build_check` 0E/0W；`validate` / `pipeline_runner validate` / `perf_monitor` 通过；`audit status` stale 0；`accept` ≥90%；`l3-status` 无超期；`evidence.plans` 非空；`task_plan check` 可重放；`git status` 干净且 `origin/main` 无直推。

### 5. 结论格式（必须输出）

1. **总判定**：全部执行到位 / 部分执行到位 / 未执行到位（三选一）。
2. **逐项状态表**：T-1..T-7 每行附「验证命令 + 真实输出 + 结论（到位/部分/未到位/虚假嫌疑）」。
3. **虚假实现嫌疑清单**：逐条列出「文件:行号 + 疑点 + 复核命令 + 实际输出 + 判定（成立/不成立）」。
4. **新引入问题**：回归、确定性、命名、文档断链、登记数据一致性等。
5. **未达标项**：原因与后续计划（若存在）。
6. **证据索引**：所有执行过的命令与输出摘要。

### 6. 禁止事项（验证过程）

- 禁止为「通过」而修改被验证代码 / 数据 / 配置；
- 禁止直推 `main`；禁止绕过 `--gate`；
- 禁止把「文档声明」当作「实现证据」；
- 禁止篡改历史时点报告（`report-audits/*-2026-11-15/16.md`）与 `engine/quality/**` 的 21 项口径；
- 禁止把 `evidence.plans` 硬编码为非空或伪造关联。
