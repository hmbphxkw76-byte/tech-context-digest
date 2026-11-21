# 任务启动 · 统一框架对齐：全部报告对齐新优化框架

- slug：`framework-align`
- 起点：`main`；分支：`task/framework-align-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/framework-align/`
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

- 统一门禁：`python engine/tools/optimization_gate.py --gate-period auto --source-gate-period auto --probe`
- 提交网关：`python engine/tools/repo_sync.py run --message ... --paths ... --gate`
- 端到端编排：`python engine/tools/pipeline_runner.py validate`
- 一键闭环：`python engine/tools/local_mainline.py run --slug framework-align --title ...`

## 任务清单（7 项，详见 tasks.json）

- [pending] T-1 决策卡补齐置信度（DC-09，15 份）
- [pending] T-2 高影响报告补齐强制披露块（ID-09，9 份）
- [pending] T-3 修复监测渲染规范告警（MON-02/03，4 份）
- [pending] T-4 补录机构分级主数据（R7，54 家）
- [pending] T-5 来源登记补 document_tier/evidence/statement_type（R8，10 线）
- [pending] T-6 补 ai-application/trends 数据目录并刷新 hub/INDEX/指纹
- [pending] T-7 全量回归（门禁 0[E]/单测/页面/指纹）并提交

## 风险登记（2 项，详见 risks.json）

- R-1 置信度由证据强度映射可能与个别卡片语义有偏差（缓解：保留反向证据说明并统一映射口径）
- R-2 批量改动引入门禁回退（缓解：逐阶段跑门禁与单测并回归）

## 关联报告

- 无（手工/工具类任务）
