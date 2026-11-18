# 任务启动 · 报告周期与展示窗口规范落地（月18/6+更多、季24、年60月5份、环比高亮、周报例外）

- slug：`report-cycle-windows`
- 起点：`main`；分支：`task/report-cycle-windows-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/report-cycle-windows/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug report-cycle-windows --title ...`

## 任务清单（4 项，详见 tasks.json）

- [pending] T-1 定义周期窗口单一事实源（CYCLE_WINDOWS/HIGHLIGHT_CYCLES/period_months/prev_period）
- [pending] T-2 build_hub 窗口切分、更多折叠、本期更新高亮与环比基期标注（index/reader）
- [pending] T-3 归档 KEEP 与窗口同源（月18/季8/年5/基线3/周报12）
- [pending] T-4 规范文档与测试对齐（REPORT-CYCLE-WINDOWS-SPEC、AGENTS 指针、TestReportCycleWindows）

## 风险登记（2 项，详见 risks.json）

- R-1 窗口锚点若取墙钟会导致生成物漂移（缓解：锚点取报告 period，禁用时间戳/mtime）
- R-2 展示窗口与归档口径漂移（缓解：KEEP 由 CYCLE_WINDOWS 派生，单一事实源）

## 关联报告

- 无（手工/工具类任务）
