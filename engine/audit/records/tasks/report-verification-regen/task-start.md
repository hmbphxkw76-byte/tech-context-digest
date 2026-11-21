# 任务启动 · 全量报告核验：未登记来源补登记 + 等级一致性修正 + 再生成

- slug：`report-verification-regen`
- 起点：`main`；分支：`task/report-verification-regen-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/report-verification-regen/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug report-verification-regen --title ...`

## 任务清单（6 项，详见 tasks.json）

- [pending] T-1 建立 22 份报告的全量核验台账（引用来源 / 核验状态 / 未登记 URL）
- [pending] T-2 补登记未登记外部来源（逐条 web_fetch 复核 tier/lang/verify_status）
- [pending] T-3 修正报告信息等级越标与不可核验内容（更新或文件级删除）
- [pending] T-4 再生成 hub / INDEX / reader 与发布指纹
- [pending] T-5 全量门禁 + 核验台账链校验
- [pending] T-6 repo_sync 提交并开 PR

## 风险登记（3 项，详见 risks.json）

- R-1 补登记来源元数据推断误差（缓解：逐条 web_fetch 复核并记录 evidence）
- R-2 报告改写引入口径漂移（缓解：只改核验标注与来源，不改数值）
- R-3 删除报告导致 hub/索引悬挂（缓解：同步重建 hub/INDEX/指纹）

## 关联报告

- `content/economy/dubai/apartment/reports/2026-11_baseline_report.html`
- `content/economy/dubai/apartment/reports/2026-11_monthly.html`
- `content/economy/dubai/apartment/reports/2026-Q3_quarterly.html`
- `content/economy/dubai/apartment/reports/2026_annual.html`
- `content/economy/insight/reports/2026-11_baseline_report.html`
- `content/economy/trends/reports/2026-11-13_weekly.html`
- `content/economy/trends/reports/2026-11-20_weekly.html`
- `content/economy/trends/reports/2026-11-27_weekly.html`
- `content/education/education-system/reports/2026-11_baseline_report.html`
- `content/education/study-abroad/reports/2026-11_baseline_report.html`
- `content/international/immigration/dubai/reports/2026-11_baseline_report.html`
- `content/international/immigration/reports/2026-11_baseline_report.html`
- `content/international/international-relations/reports/2026-11_baseline_report.html`
- `content/political/political-system/reports/2026-11_baseline_report.html`
- `content/society/social-structure/reports/2026-11_baseline_report.html`
- `content/tech/ai-application/competitive-intelligence/dubai/reports/2026-11_baseline_report.html`
- `content/tech/ai-application/dubai/reports/2026-11_baseline_report.html`
- `content/tech/ai-application/industry-research/dubai/reports/2026-11_baseline_report.html`
- `content/tech/ai-security/competitive-intelligence/dubai/reports/2026-11_baseline_report.html`
- `content/tech/ai-security/competitive-intelligence/dubai/reports/2026-11_monthly.html`
- `content/tech/ai-security/dubai/reports/2026-11_baseline_report.html`
- `content/tech/ai-security/industry-research/dubai/reports/2026-11_baseline_report.html`
