# 任务启动 · 告警治理：R7 补录 + R2 分级标注 + MON 渲染（新增报告）

- slug：`warnings-cleanup`
- 起点：`main`；分支：`task/warnings-cleanup-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/warnings-cleanup/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug warnings-cleanup --title ...`

## 任务清单（5 项，详见 tasks.json）

- [done] T-1 补录 40 家新增机构至 institution_tiers.json（纯追加）
- [done] T-2 修正 business-config 来源优先级引用（Robert Half）
- [done] T-3 ai-application/dubai 报告补 R2 分级标注（9 处）
- [done] T-4 immigration 报告补 MON-04 外链属性（59 处）+ MON-03 列宽
- [done] T-5 刷新指纹/索引并全量回归

## 风险登记（1 项，详见 risks.json）

- R-1 仅做追加与结构性修复，不改既有内容数据

## 关联报告

- 无（手工/工具类任务）
