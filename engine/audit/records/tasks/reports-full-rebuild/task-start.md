# 任务启动 · 全量报告删除与框架内重生成

- slug：`reports-full-rebuild`
- 起点：`main`；分支：`task/reports-full-rebuild-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/reports-full-rebuild/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug reports-full-rebuild --title ...`

## 任务清单（6 项，详见 tasks.json）

- [pending] T-1 删除 content/**/reports/ 下全部 20 份报告（保留 .gitkeep）
- [pending] T-2 重生成 economy 主题报告（apartment 6 + trends 3 + insight 1）
- [pending] T-3 重生成 tech 主题报告（competitive-intelligence 2 + industry-research 1 + security 1 + weekly-roundup 2）
- [pending] T-4 重生成 education/international/political/society 基线报告（4）
- [pending] T-5 全量门禁（optimization_gate）与问题排查修复
- [pending] T-6 刷新 INDEX/hub/发布指纹并经 repo_sync 提交开 PR

## 风险登记（4 项，详见 risks.json）

- R-1 基线删除后周期报告失去对比锚（缓解：以 git HEAD 版本作为上期/基线参考重新生成）
- R-2 重生成内容与既有事实冲突（缓解：继承各线已修正事实清单防回退）
- R-3 门禁 [E] 阻断（缓解：逐项修复后重跑统一门禁）
- R-4 并行生成一致性（缓解：统一 canonical 样式与类型模板）

## 关联报告

- `content/economy/dubai/apartment/reports/2026-11_baseline_report.html`
- `content/economy/dubai/apartment/reports/2026-11_monthly.html`
- `content/economy/dubai/apartment/reports/2026-12_monthly.html`
- `content/economy/dubai/apartment/reports/2026-Q3_quarterly.html`
- `content/economy/dubai/apartment/reports/2026_annual.html`
- `content/economy/dubai/apartment/reports/2027-01_monthly.html`
- `content/economy/insight/reports/2026-12_baseline_report.html`
- `content/economy/trends/reports/2026-11-13_weekly.html`
- `content/economy/trends/reports/2026-11-20_weekly.html`
- `content/economy/trends/reports/2026-11-27_weekly.html`
- `content/education/education-system/reports/2026-12_baseline_report.html`
- `content/international/international-relations/reports/2026-11_baseline_report.html`
- `content/political/political-system/reports/2026-11_baseline_report.html`
- `content/society/social-structure/reports/2026-11_baseline_report.html`
- `content/tech/competitive-intelligence/dubai/reports/2026-12_baseline_report.html`
- `content/tech/competitive-intelligence/dubai/reports/2026-12_monthly.html`
- `content/tech/industry-research/dubai/reports/2026-12_baseline_report.html`
- `content/tech/security/dubai/reports/2026-11_baseline_report.html`
- `content/tech/weekly-roundup/reports/2026-11-13_weekly.html`
- `content/tech/weekly-roundup/reports/2026-11-20_weekly.html`
