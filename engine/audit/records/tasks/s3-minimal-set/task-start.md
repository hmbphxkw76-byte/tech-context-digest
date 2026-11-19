# 任务启动 · A 档：S2 盲区阻塞跟踪闭环 + S3 第二期最小集定义与工具侧

- slug：`s3-minimal-set`
- 起点：`main`；分支：`task/s3-minimal-set-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/s3-minimal-set/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug s3-minimal-set --title ...`

## 任务清单（4 项，详见 tasks.json）

- [done] T-1 update_planner 增盲区阻塞跟踪段（S2 闭环）
- [done] T-2 update_planner 支持周周期派发（S3 工具侧）
- [done] T-3 产出「第二期最小集」清单文档
- [done] T-4 方案 §3 指针 + 测试 + 门禁 + PR

## 风险登记（2 项，详见 risks.json）

- R-1 周周期派发属新口径，可能与非周业务线任务混淆（缓解：仅对有 weekly 提示词的業務线派发 + 单测锁定）
- R-2 最小集依赖内容产出，本次只到「定义 + 工具就绪」（缓解：不擅自撰写报告正文）

## 关联报告

- 无（手工/工具类任务）
