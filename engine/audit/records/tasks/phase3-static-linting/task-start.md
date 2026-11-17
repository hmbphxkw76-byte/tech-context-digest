# 任务启动 · Phase 3 静态检查与规范分层（ruff/mypy 门禁 / 文档轮转 / 上位-下位收敛）

- slug：`phase3-static-linting`
- 起点：`main`；分支：`task/phase3-static-linting-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/phase3-static-linting/`
  - `plan.json`（计划与 N0–N8 映射）
  - `tasks.json`（任务分解）
  - `risks.json`（风险登记）
  - `task-start.md`（本文件）

## 体系映射（主体保留，增量吸收）

| 节点 | 名称 | 说明 |
|---|---|---|
| N0 | 需求与配置 | business-config / layout.json 维度注册 |
| N0.5 | 任务计划（mainline 阶段 2 吸收） | plan.json / tasks.json / risks.json / task-start.md |
| N1 | 信息采集 | source_registry / 台账 / 发布日历 |
| N2 | 信息筛选与分级 | 四层分级 + 双源 + 死链 |
| N3 | 信息分类 | 类型 / 维度 / 归位 |
| N4 | 内容生成 | 四层提示词继承 + 量化模型 |
| N5 | 渲染与交付 | canonical 样式 + 自包含 HTML |
| N6 | 质量校验与审计 | 统一门禁 + 审计四环节 |
| N7 | 发布 / 索引 / 归档 | hub / INDEX / 指纹 / 归档 |
| N8 | 运维与监控 | CI 工作流 + 告警 |

## 复用入口（不得另写一套校验）

- 统一门禁：`python engine/tools/optimization_gate.py --gate-period 2026-12 --source-gate-period 2027-01 --probe`
- 提交网关：`python engine/tools/repo_sync.py run --message ... --paths ... --gate`
- 端到端编排：`python engine/tools/pipeline_runner.py validate`
- 一键闭环：`python engine/tools/local_mainline.py run --slug phase3-static-linting --title ...`

## 任务清单（4 项，详见 tasks.json）

- [pending] T-01 ruff / mypy 纳入统一门禁（static_check 适配 + pyproject + requirements）
- [pending] T-02 report-audits 轮转归档（archive_reports --audit-docs，维护流水线执行）
- [pending] T-03 规范上位-下位收敛（AGENTS.md 精简 + 新增即删旧）
- [pending] T-04 门禁计数与文档同步（21→23）+ 单测全量回归

## 风险登记（3 项，详见 risks.json）

- R-01 静态检查噪声阻断门禁（缓解：默认 [W]，工具缺失/发现均告警不阻断）
- R-02 规范删改误删硬约束（缓解：保留四门禁脚本名与硬性约束，单测锁定）
- R-03 轮转误删在用文档（缓解：只轮转带日期且超 12 个月，无日期账本型不轮转）

## 关联报告

- 无（手工/工具类任务）
