# 端到端全流程覆盖清单（END-TO-END-COVERAGE v1.0）

> **状态**：现行说明
> **用途**：把「信息收集 → 报告输出」全生命周期各维度，映射到本仓库的**具体产物 / 门禁 / 测试 / CI 配置**，作为全维度覆盖的**单一切入**。本文件只作指针与矩阵，不复制规则正文（事实源见各专用规范）。
> **上位**：[AGENTS.md](../../AGENTS.md)；**体系**：[report-pipeline-system.md](./report-pipeline-system.md)；**设计**：[architecture-and-pipeline-design.md](./architecture-and-pipeline-design.md)；**编排**：[report-pipeline-implementation-plan.md](./report-pipeline-implementation-plan.md)。
> **最后更新**：2026-11-17

---

## 一、六项要求 × 覆盖产物

| # | 要求 | 覆盖产物（事实源 / 机制） | 强制手段 | 验证入口 |
|---|---|---|---|---|
| 1 | 全维度范围梳理 | 本文件 + [软件架构全面评估](../report-audits/architecture-assessment-2026-11-16.md) + [报告全链路体系](./report-pipeline-system.md)（N0–N8 / 五道防线） | — | 本文件 §四 |
| 2 | 系统性架构规划与优化 | [架构与全流程设计基线](./architecture-and-pipeline-design.md) + [架构开发规范](./architecture-development-standard.md) + [目录结构与命名规范](./structure-and-naming-spec.md) + [页面构建规范](./page-build-spec.md) | `validate_layout` / `validate` / `page_build_check` | unittest + 统一门禁 |
| 3 | 分阶段落地实施 | 设计基线 §6 的 P1–P4 + [架构开发规范](./architecture-development-standard.md) §三（流程与评审节点） | 阶段出口就地门禁 G0–G5 | `pipeline_runner run` |
| 4 | 全链路自动化与稳定性保障 | `pipeline_runner` + `pipeline_manifest.json` + `automation_status` / `perf_monitor` / `remediation_ticket` / `workspace_cleanup` | 子进程 wall 超时 / 共享检出锁 / 退出码 0-1-2 / 幂等 | `test_pipeline_runner` / `test_perf_monitor` |
| 5 | 标准化交付物输出 | 见 §三交付物清单 | 命名规范 + 生成物确定性 | `check_links` / `validate` |
| 6 | 基础设施保障机制 | `optimization_gate`（21 项单一入口）+ `repo_sync` + `pre-push` + 分支保护 + CI 六工作流 | `[E]` 阻断合并 / 提交 | `test_process_gates` / `test_repo_sync` / `test_workflow_isolation` |

---

## 二、生命周期 N0–N8 × 产物 × 门禁 × 测试

| 节点 | 名称 | driver | 主要产物 | 门禁 | 锁定测试 |
|---|---|---|---|---|---|
| N0 | 需求与配置 | manual | `business-config.md` / `layout.json` 维度注册 | G0 | `test_tools` / `test_prompt_inheritance` |
| N1 | 信息采集 | manual | `source_registry.json` / 台账 / `release-calendar.json` | G1 | `test_source_check` / `test_release_calendar` |
| N2 | 信息筛选与分级 | semi | 四层分级标注 / 死链清单 | G2 | `test_source_check` |
| N3 | 信息分类 | tool | 归位结果 / 类型·维度标签 | G3 | `test_classification_mapping` / `test_classify_boundary` |
| N4 | 内容生成 | manual | 报告 md·HTML / `[FC-…]` 引用 | G4 | `test_info_density` / `test_fact_cards` / `test_decision_hub` / `test_blind_spot` |
| N5 | 渲染与交付 | tool | 自包含 canonical HTML | G5 | `test_tools`（page_build） |
| N6 | 质量校验与审计 | tool | 审计记录 / 终审标识（none·pre·full） | G6 | `test_audit_tool` / `test_audit_strict` / `test_process_gates` |
| N7 | 发布 / 索引 / 归档 | tool | `index.html` / `reader.html` / `INDEX.md` / 指纹 / 归档 | G7 | `test_publish_fingerprint` |
| N8 | 运维与监控 | ci | 告警 / 任务清单 / 状态留痕 | G8 | `test_automation_status` / `test_remediation_ticket` / `test_workflow_isolation` |

- **闭环 L1**：N8 → N1（异步：心跳 / 任务清单 / 复审）。
- **闭环 L2**：G6 → N4（同步：`[E]` 阻断，携上下文退回生成）。
- **统一门禁**：G6 = `*`（全量 21 项，`--probe`），两级 gate-period（内容 2026-12 / 来源 2027-01）。

---

## 三、标准化交付物清单（可复用 / 可维护 / 可扩展）

| 类别 | 交付物 |
|---|---|
| 全流程操作文档 | [engine/tools/README.md](../tools/README.md)（工具）、[report-pipeline-system.md](./report-pipeline-system.md)（体系）、[architecture-development-standard.md](./architecture-development-standard.md)（流程与验收） |
| 架构设计说明 | [architecture-and-pipeline-design.md](./architecture-and-pipeline-design.md)、[architecture-development-standard.md](./architecture-development-standard.md) |
| 治理规范手册 | [process-vs-infrastructure-governance.md](./process-vs-infrastructure-governance.md)、[page-build-governance.md](./page-build-governance.md)、[multi-session-git-protocol.md](./multi-session-git-protocol.md)、[report-process-reuse.md](./report-process-reuse.md) |
| CI/CD 流水线配置 | `.github/workflows/{ci,html-sync,content-update,scheduled-maintenance,audit,webhook-alert}.yml` + `.github/actions/{submit-pr,workspace-cleanup,remediation-ticket}/action.yml` |
| 自动化报告生成脚本 | `engine/tools/{md2html,report_style,build_hub,build_index,publish_fingerprint,archive_reports}.py` |
| 全流程编排 | `engine/tools/pipeline_manifest.json` + `pipeline_runner.py` + `pipeline_audit.py` + `optimization_gate.py` |
| 全链路验证测试用例 | `engine/tests/`（27 文件 / 398 用例） |

---

## 四、验证命令与当前基线（2026-11-17）

| 命令 | 结果 |
|---|---|
| `python -m unittest discover -s engine/tests` | 398 通过（1 跳过） |
| `python engine/tools/optimization_gate.py --gate-period 2026-12 --source-gate-period 2027-01 --probe` | 0 错误 / 1 警告（`source_check` R6 历史死链，宽限期内不追溯） |
| `python engine/tools/pipeline_runner.py run --from N0 --to N8` | `outcome=passed`（G0–G8 全过；G2/G6/G7 仅宽限期警告） |
| `python engine/tools/pipeline_runner.py validate` | 9 节点 / 9 门禁 / 2 闭环 |
| `validate_layout` / `validate` / `check_links` / `page_build_check` / `build_hub --check` | 全部 0 |
| `python engine/tools/publish_fingerprint.py --check` | 10/10 一致，0 漂移 |

---

## 五、覆盖边界与已知缺口

- **在环边界**：N1 采集 / N4 生产为「人工 + Agent 在环」，工具只做登记、校验、渲染、留痕（设计见 [architecture-and-pipeline-design.md](./architecture-and-pipeline-design.md) §1.2 非目标）。自动化覆盖 N2 / N3 / N5 / N6 / N7 与 N8 监控。
- **已知缺口**：完整问题清单与优化方向见 [软件架构全面评估](../report-audits/architecture-assessment-2026-11-16.md)（F-01…F-35）；本文件不复制其结论。
- **历史告警**：`source_check` R6 宽限期探测项登记于 [tech-debt-ledger.md](../report-audits/tech-debt-ledger.md)，不阻断。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-17 | 初始版本 | 六项要求 × 产物映射、N0–N8 覆盖矩阵、交付物清单、验证基线、覆盖边界 |
