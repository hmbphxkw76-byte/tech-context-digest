# 任务启动 · Phase 1 任务级闭环层（task_plan / local_mainline / 计划门禁）

- slug：`phase1-task-loop`
- 起点：`main`；分支：`task/phase1-task-loop-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/phase1-task-loop/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug phase1-task-loop --title ...`

## 任务清单（5 项，详见 tasks.json）

- [pending] T-01 新增 task_plan.py 任务计划工件生成器（plan/tasks/risks + 启动文件）
- [pending] T-02 新增 local_mainline.py 一键闭环编排（只编排不重写校验）
- [pending] T-03 repo_sync 增「工件即门禁输入」计划校验与 --allow-no-plan 应急
- [pending] T-04 AGENTS.md / report-pipeline-system.md 增任务级闭环与 N0.5 映射
- [pending] T-05 配套单测与全量门禁回归

## 风险登记（3 项，详见 risks.json）

- R-01 任务工件形式主义（缓解：工件即门禁输入 + check 可重放）
- R-02 双入口漂移（缓解：local_mainline 只编排，测试锁定复用 optimization_gate/repo_sync）
- R-03 计划强制影响既有会话（缓解：仅受管 task/* 生效，保留 --allow-no-plan 应急）

## 关联报告

- 无（手工/工具类任务）
