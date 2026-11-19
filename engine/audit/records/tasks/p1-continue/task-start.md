# 任务启动 · P1 推荐项推进：2 条新业务线首报 + 周期滚动 + A-05/A-03 收口

- slug：`p1-continue`
- 起点：`main`；分支：`task/p1-continue-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/p1-continue/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug p1-continue --title ...`

## 任务清单（4 项，详见 tasks.json）

- [pending] T-1 SA1 education-system 首份 baseline-setup 报告
- [pending] T-2 SA2 international-relations 首份 baseline-setup 报告
- [pending] T-3 SA3 apartment 2027-01 monthly + trends 2026-11-27 weekly
- [pending] T-4 SA4 A-05 死链复探修复 + A-03 真值核对数据治理

## 风险登记（2 项，详见 risks.json）

- R-1 新业务线内容编造（缓解：来源分级+缺口标未核验）
- R-2 并发写冲突（缓解：文件独占+主会话串行整合）

## 关联报告

- 无（手工/工具类任务）
