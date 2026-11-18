# 任务启动 · 目标对齐批次 b0–b5（语义弱/度量空专项）

- slug：`goal-alignment-batches`
- 起点：`main`；分支：`task/goal-alignment-batches-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/goal-alignment-batches/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug goal-alignment-batches --title ...`

## 任务清单（6 项，详见 tasks.json）

- [pending] T-1 b0 专项方案落入方案文档 v1.2
- [pending] T-2 b1 批次 A 语义弱门禁接线（MON-01..05 / 看板台账 / 版本 / 命名）
- [pending] T-3 b2 批次 B 度量空（38 项指标实测覆盖 + 覆盖报告）
- [pending] T-4 b3 批次 C P1 内容/覆盖
- [pending] T-5 b4 批次 D P2 卫生项
- [pending] T-6 b5 收尾全量验收与差异报告

## 风险登记（3 项，详见 risks.json）

- R-1 存量报告告警噪声稀释门禁信号（缓解：全部 [W] 不阻断并登记 tech-debt）
- R-2 新增门禁改变 CI 口径（缓解：全量单测 + gate 0E 验证）
- R-3 报告正文修改越界（缓解：仅机械合规修正，研究内容不动）

## 关联报告

- 无（手工/工具类任务）
