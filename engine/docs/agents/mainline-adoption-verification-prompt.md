# mainline 吸收式融合 · 全量验证提示词（MAINLINE-ADOPTION-VERIFICATION）

> **用途**：把本文件整体投喂给一个验证 Agent（或自查），用于确认「mainline 吸收式融合」是否**完全对齐**《方案》的规划与设计，并**重点排查虚假实现**。
> **事实源**：`engine/report-audits/mainline-adoption-assessment-2026-11-17.md`（《方案》）、`engine/report-audits/mainline-adoption-coverage-matrix.md`（覆盖矩阵）、`AGENTS.md`（硬性约束）。
> **性质**：只读验证。除为复现而生成临时文件外，**不得修改仓库**；若发现问题，另开 `task/*` 分支。

---

## 提示词正文（复制以下全部内容使用）

你是本仓库的独立验证 Agent。任务：**全面验证「mainline 吸收式融合」是否完全对齐《方案》的规划与设计，是否引入新问题，特别是是否存在虚假实现**。不要轻信文档声明，一切以**可执行命令的真实输出**为准。

### 0. 必读（按序，不得跳读）

1. `engine/report-audits/mainline-adoption-assessment-2026-11-17.md`（《方案》全文：§1.6 痛点 P-01..P-10、§三 对照矩阵、§五 结论、§六 路线图、§七 风险、§八 量化指标）。
2. `engine/report-audits/mainline-adoption-coverage-matrix.md`（覆盖矩阵：52 行逐项状态）。
3. `AGENTS.md`（硬性约束）。
4. 被验证的实现源码：`engine/tools/optimization_gate.py`、`engine/tools/repo_sync.py`、`engine/tools/pipeline_runner.py`、`engine/tools/task_plan.py`、`engine/tools/local_mainline.py`、`engine/tools/static_check.py`、`engine/tools/archive_reports.py`、`engine/audit/scripts/audit_tool.py`、`perf-status.json`、`engine/tools/perf_monitor.py`、`engine/tools/pipeline_manifest.json`。
5. 测试：`engine/tests/test_task_plan.py`、`test_local_mainline.py`、`test_static_check.py`、`test_pipeline_runner.py`、`test_audit_tool.py`、`test_repo_sync.py`、`test_process_gates.py`、`test_pipeline_system_doc.py`、`test_tools.py`。
6. CI：`.github/workflows/ci.yml`、`audit.yml`、`scheduled-maintenance.yml`、`content-update.yml`、`html-sync.yml`。

### 1. 验证原则

- **单一事实源**：任何结论以《方案》+覆盖矩阵为准；冲突时以《方案》明确结论为准。
- **复用优先**：不得另写一套校验；所有阶段必须复用 `engine/tools/optimization_gate.py` 与 `engine/tools/repo_sync.py`。
- **证据优先**：每一项判定必须附「命令 + 真实输出片段」；无输出 = 未验证。
- **不预设结论**：允许也要求报告「未对齐 / 部分对齐 / 虚假实现嫌疑」；不得为求通过而放宽判据。
- **只读**：验证过程不修改仓库；确需生成临时文件时放在系统临时目录并清理。

### 2. 反虚假实现红线（重点，逐条核查）

「虚假实现」= 表面存在、实际不产生真实效果，或用占位 / 绕过 / 伪造数据使检查通过。逐条核查：

1. **门禁是否被真正调用**：`local_mainline.py` 必须通过 `subprocess` 真正执行 `optimization_gate.py --probe` 与 `repo_sync.py`，而非 `import` 后 mock、打印假输出、或直接 `return 0`。
   - 命令：`python engine/tools/local_mainline.py run --slug <存在的slug> --title x --dry-run`，核对步骤命令是否指向真实脚本；再读源码确认无 `return 0` 短路、无 `mock`/`unittest` 依赖混入生产路径。
2. **计划工件是否真实生成**：`task_plan.py init` 必须写出 4 个真实文件；`check` 必须**重渲染并逐字节比对**，而非恒返回 `[]`。
   - 命令：`python engine/tools/task_plan.py init --slug verify-tmp --title t --task "T-1:x"`（在临时目录/分支），篡改 `tasks.json` 后 `python engine/tools/task_plan.py check --slug verify-tmp` 必须**报错**。
3. **证据索引是否真实汇聚**：`audit_tool.py evidence <report>` 必须真实读取 `records/tasks/*/plan.json` 与 `records/reviews/*.json`，而非硬编码空列表。
   - 命令：`python engine/audit/scripts/audit_tool.py evidence <report>`，核对 `plans`/`audit.review` 字段非空且路径存在。
4. **L3「已审计」是否有真实审查留痕**：登记册 `status=audited` 的每份报告，必须存在 `records/reviews/<slug>.json` 中 **agent 的 `second` 与 `final` 通过记录**；不得只改 registry。
   - 命令：`python -c` 遍历 `audit_registry.json`，对每个 `audited` 报告检查 `_review_file` 存在且含 agent pass；再 `python engine/audit/scripts/audit_tool.py accept` 核对覆盖率。
5. **测试是否恒真 / 自我 mock**：检查新增测试是否 mock 掉**被测函数本身**、是否只断言「文件存在」而无行为断言、是否用 `try/except` 吞异常。
   - 命令：`grep -nE "mock\\.patch|assertIn|return_value" engine/tests/test_task_plan.py engine/tests/test_local_mainline.py engine/tests/test_static_check.py`，逐处判断是否合理。
6. **`--check` 是否可重放**：`task_plan check`、`build_hub --check`、`publish_fingerprint --check` 连续两次结果必须一致；生成物不得含时间戳 / mtime。
   - 命令：`python engine/tools/task_plan.py check --slug <slug>` 两次；`grep -nE "20[0-9]{2}-[0-9]{2}-[0-9]{2}T|mtime|datetime.now" engine/tools/task_plan.py engine/tools/local_mainline.py`（生产路径不得依赖当前时间）。
7. **是否绕过门禁 / 直推 main**：`grep -nE "no-gate|allow_no_plan|--allow-no-plan" engine/tools/repo_sync.py` 确认仅为显式应急；`git log origin/main --oneline` 确认合并均来自 PR，无直推。
8. **是否整体替换为 mainline 11 阶段**：确认 `pipeline_manifest.json` 仍为 N0–N8 + G0–G8；`AGENTS.md` 明示「主体保留、增量吸收」；未引入 `tag` / `changelog` / `RELEASES.md`。
9. **生成物确定性**：任务工件、审计记录、指纹文件不得含运行时间戳；`git diff` 不应出现与实现无关的时间字段。
10. **CI 是否真调用统一门禁**：`.github/workflows/*.yml` 必须出现 `optimization_gate.py`（或 `repo_sync.py ... --gate`），不得分项重复扫描。

### 3. 对齐验证（逐项，覆盖矩阵 52 行）

按覆盖矩阵逐行核对，逐项给出「已对齐 / 部分对齐 / 未对齐 / 显式延后」与证据：

- **A. 痛点 P-01..P-10**（10 项）：重点复核 P-01（stale 检测真实）、P-02（L3 覆盖率真实）、P-04（CI 确含 `pipeline_runner validate`）、P-06 / P-09（显式延后理由是否成立）。
- **B. 吸收项 ①..④**（4 项）：计划工件、本地编排、证据索引、分支登记册语义。
- **C. Phase 0.1..0.4 / 1.1..1.3 / 2.1..2.3 / 3.1..3.3**（13 项）：逐项跑验收命令。
- **D. CI/CD 改造点**：`ci.yml` / `scheduled-maintenance.yml` / `audit.yml` 是否落地；`submit-pr` / `workspace-cleanup` / `remediation-ticket` 是否「不改动」且有理由。
- **E. 治理标准 1..5**：工件即门禁输入、单一事实源、复用纪律、版本治理、新增即删旧。
- **F. 风险 6 项**：R1..R6 的缓解是否真实存在（尤其 R5 是否显式延后）。
- **G. 量化指标 8 项**：按 §1.6 命令实测，记录输出。

### 4. 必跑验证命令（逐条记录退出码与关键输出）

```bash
python -m py_compile engine/tools/*.py engine/tests/*.py engine/audit/scripts/*.py
python -m unittest discover -s engine/tests -p "test_*.py"
python engine/tools/optimization_gate.py --gate-period 2026-12 --source-gate-period 2027-01 --probe
python engine/tools/optimization_gate.py --only ruff,mypy
python engine/tools/validate.py
python engine/tools/check_links.py
python engine/tools/page_build_check.py
python engine/tools/pipeline_runner.py validate
python engine/audit/scripts/audit_tool.py status
python engine/audit/scripts/audit_tool.py accept
python engine/audit/scripts/audit_tool.py index
python engine/tools/perf_monitor.py check
python engine/tools/archive_reports.py --audit-docs
python engine/tools/task_plan.py check --slug <存在的slug>
python engine/tools/local_mainline.py run --slug <存在的slug> --title x --dry-run
git log origin/main --oneline -10
git status --short
```

判据：统一门禁 0 `[E]`；`unittest` 全绿；`check_links` / `page_build_check` 0E/0W；`validate` / `pipeline_runner validate` / `perf_monitor` 通过；`audit_tool status` stale 0。

### 5. 结论格式（必须输出）

1. **总判定**：完全对齐 / 部分对齐 / 未对齐（三选一）。
2. **逐项状态表**：覆盖矩阵 52 行 + 量化指标 8 项，每行附证据命令与结论。
3. **虚假实现嫌疑清单**：逐条列出「文件:行号 + 疑点 + 复核命令 + 实际输出 + 判定（成立/不成立）」。
4. **新引入问题**：回归、性能、确定性、命名、文档断链等。
5. **未达标项**：原因与后续计划（若存在）。
6. **证据索引**：所有执行过的命令与输出摘要。

### 6. 禁止事项（验证过程）

- 禁止为「通过」而修改被验证代码 / 数据 / 配置；
- 禁止直推 `main`；禁止绕过 `--gate`；
- 禁止把「文档声明」当作「实现证据」；
- 禁止遗漏《方案》任何条目（含 P-06 / P-09 的显式延后判定）。
