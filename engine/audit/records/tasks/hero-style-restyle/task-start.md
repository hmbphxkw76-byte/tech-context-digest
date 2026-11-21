# 任务启动 · 报告页头统一 hero 风格并全量重出报告

- slug：`hero-style-restyle`
- 起点：`main`；分支：`task/hero-style-restyle-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/hero-style-restyle/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug hero-style-restyle --title ...`

## 任务清单（4 项，详见 tasks.json）

- [pending] T-1 幂等校验并补齐 18 份正式报告 hero 题头（legacy 存档不动）
- [pending] T-2 收口 restyle_reports.py 工具缺陷（--help 崩溃、docstring 列宽口径）
- [pending] T-3 过统一门禁/页面门禁/hub 校验/单测
- [pending] T-4 repo_sync 提交推送并 PR 合并到 main

## 风险登记（2 项，详见 risks.json）

- R-1 幂等复跑误改已迁移报告（缓解：缓解=先 --dry 预览再实跑，git diff 复核）
- R-2 受管分支缺计划工件被门禁拒绝（缓解：缓解=先补四件套再提交）

## 关联报告

- `content/economy/dubai/apartment/reports/2026-11_baseline_report.html`
- `content/economy/trends/reports/2026-11-13_weekly.html`
- `content/tech/ai-security/security/dubai/reports/2026-11_baseline_report.html`
