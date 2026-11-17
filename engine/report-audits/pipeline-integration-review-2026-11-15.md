# 报告全流程架构与执行逻辑集成审查确认报告（INTEGRATION-REVIEW v1.1）

> **状态**：历史记录（时点审查，留存备查；被审方案见 [report-pipeline-implementation-plan.md](../docs/report-pipeline-implementation-plan.md)）
> **流程事实源**：[report-pipeline-system.md](../docs/report-pipeline-system.md) §1.1 全链路主流程图（N0–N8 + G0–G8 + L1/L2）
> **审查方式**：静态逐项核对 + 单元测试 + 真实全链路运行 + 统一门禁 + 链接校验
> **结论**：**通过**（无阻断性待整改项）

---

## 一、审查范围

| 层 | 设计模块 | 实现载体 |
|---|---|---|
| 编排层 | manifest + runner | `engine/tools/pipeline_manifest.json`、`engine/tools/pipeline_runner.py` |
| 节点层 | N0–N8 | manifest 声明 + 既有工具链（driver = manual/tool/ci） |
| 门禁层 | G0–G8 | `engine/tools/optimization_gate.py`（21 项单一入口） |
| 契约层 | StageResult / GateResult / PipelineRun | `pipeline_runner.py` 数据结构 |
| 审计层 | 追加式留痕 | `engine/tools/pipeline_audit.py` + `engine/audit/records/pipeline_runs.jsonl` |
| 出口审计 | 审计四环节 | `engine/audit/scripts/audit_tool.py run --strict --no-gate`（G6 接线） |

---

## 二、集成完整性（要求 1）

| # | 设计项 | 实现位置 | 状态 |
|---|---|---|---|
| 1.1 | 声明式 N/G 图 | `pipeline_manifest.json` | ✅ `validate` → 9 节点 / 9 门禁 / 2 闭环 |
| 1.2 | 编排器（节点→门禁→路由） | `pipeline_runner.run_pipeline` | ✅ 真实运行 N0→N8 全通 |
| 1.3 | 门禁单一入口复用 | `run_gate` → `optimization_gate.run_checks` | ✅ 子集断言 + 真实结果一致 |
| 1.4–1.6 | 契约 StageResult / GateResult / PipelineRun | `pipeline_runner` | ✅ 字段逐一对应，含 `output` / `rollback_to` / `audit_path` |
| 1.7 | 审计留痕 | `pipeline_audit.append/read_run` | ✅ 可按 run_id 回放 |
| 1.8 | 流程图渲染与清单同源 | `render_flow` | ✅ `plan` 输出与 manifest 一致 |
| 1.9 | 出口审计接线 | manifest G6 `audit.command` | ✅ 真实运行执行审计四环节 |
| 1.10 | 一致性测试 | `test_pipeline_runner.py` | ✅ 16 项通过 |

---

## 三、执行逻辑与集成点一致性（要求 2 & 3）

| 逻辑 | 实现 | 验证 |
|---|---|---|
| 分支判断：通过→下一节点；不通过→按 `on_fail` 退回 | `run_pipeline` 循环 + `blocked` 判定 | `test_full_pass` / `test_g0_block_stops_at_n0` |
| L2：G6 阻断 → 精准退回 N4 | `gate.on_fail = "N4"` + 路由留痕 | `test_g6_block_rolls_back_to_n4` |
| L1：N8 异步触发 N1 | manifest `loops[L1]`；运行到 N8 留痕 `loop` 事件 | `test_loops_exact` |
| 异常处理：门禁抛错 / 审计失败 → 计 error（阻断），不崩溃 | `run_gate` try/except + `_run_command` 容错 | `test_run_gate_exception_blocked` / `test_g6_audit_failure_blocks` |

集成点数据格式：`run_gate` 传 `CHECKS` 名称子集（`*` = 全量 21 项）；审计 JSONL 字段固定（`schema_version/ts/run_id/kind/...`）；G6 传 `audit_tool.py run --strict --no-gate`（退出码 0/1 + 文本，字节容错解码）。

---

## 四、审查发现与处理

### 4.1 已整改项（闭环）

| 发现 | 处理 |
|---|---|
| 门禁工具抛错会向上崩溃 | `run_gate` 加 try/except，异常计 1 error（阻断） |
| G6 未接线审计四环节 | manifest G6 加 `audit.command`；`audit_tool` 加 `--no-gate` |
| Windows `shell=True` 下 `.py` 关联失效 / GBK 解码崩溃 | 命令加 `python` 前缀；字节捕获 + `errors="replace"` |

### 4.2 设计内委托 / 限制（非整改项）

- **节点层执行**：N0/N1/N4 由 Agent / 人完成，N3/N5/N7 由工具链、N8 由 CI 完成；runner 按 `driver` 登记并编排门禁，**不替代内容生产**。
- **L1 异步触发**：runner 声明并留痕；实际触发由 CI 心跳 / 任务清单 / 复审执行。
- **G8 外部门禁**：无自动检查项，由 CI 工作流 + `webhook-alert.yml` 承载。
- **运行副作用**：`run` 追加审计 JSONL，并在 G6 触发审计四环节写审计记录（预期行为）。

---

## 五、验证证据（实测）

| 验证项 | 结果 |
|---|---|
| `unittest discover -s engine/tests` | Ran 405 tests, OK |
| `test_pipeline_runner.py` | 16 项 OK |
| `test_pipeline_system_doc.py` | OK |
| `pipeline_runner.py validate` | 9 节点 / 9 门禁 / 2 闭环 |
| `optimization_gate.py --gate-period 2026-12 --source-gate-period 2027-01` | 0 错误 / 6 警告（不阻断） |
| `check_links.py` | 通过 |
| `pipeline_runner.py run --from N0 --to N8` | `outcome=passed`；9 节点 + 9 门禁；G6 含审计四环节 |

---

## 六、确认结论

1. **要求 1 达成**：设计文档定义的全部模块、组件、接口、数据流已完整集成，无遗漏、无偏差。
2. **要求 2 达成**：分支判断、流程跳转（L2→N4）、异常处理、时序规则（L1 异步 / L2 同步）完全匹配设计规范。
3. **要求 3 达成**：各集成点的依赖关系、调用链路、数据传递格式与架构设计一致，且由测试锁定。
4. **待整改项**：无阻断性待整改项。

### 后续开发约束（硬性）

- 流程图为唯一流程事实源：**N0–N8 串行主链 + G0–G8 就地门禁 + L1（N8→N1 异步）/ L2（G6→N4 同步）**，不得增删节点 / 门禁或改变退回路径。
- 门禁校验一律复用 `optimization_gate` 单一入口，不得另写检查命令。
- 门禁组合 / 周期 / 退回目标只经 `pipeline_manifest.json` 配置，不得硬编码。
- 契约结构与审计字段（`pipeline_runs.jsonl`）不得破坏性变更。
- 任何偏离须先更新设计文档，并同步 `test_pipeline_runner.py` / `test_pipeline_system_doc.py` 断言。

## 版本记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-11-15 | 初始集成审查：逐项核对 + 3 项整改闭环 + 全量验证；结论通过 |
| v1.1 | 2026-11-16 | 精简：合并验证证据表，更新单测计数为 377 |
| v1.2 | 2026-11-16 | 计数刷新 | 单测计数按实跑更新为 405 |
