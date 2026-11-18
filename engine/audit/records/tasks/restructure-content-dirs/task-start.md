# 任务启动 · 业务线目录去 global 段 + region 可选维度

- slug：`restructure-content-dirs`
- 起点：`main`；分支：`task/restructure-content-dirs-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/restructure-content-dirs/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug restructure-content-dirs --title ...`

## 任务清单（4 项，详见 tasks.json）

- [pending] T-1 layout.json v4.1 可选 region 模型与引擎改造
- [pending] T-2 content/data 业务线目录迁移与占位删除
- [pending] T-3 全仓引用同步与文档/模板/测试更新
- [pending] T-4 派生登记重生成与全门禁验证

## 风险登记（3 项，详见 risks.json）

- R-1 迁移后相对链接深度变化导致断链（缓解：逐文件校正 ../ 层级并跑 check_links）
- R-2 维度模型变更影响既有发现/归位逻辑（缓解：补 optional region 用例并全量 unittest）
- R-3 派生登记（hub/指纹/审计）与磁盘漂移（缓解：重生成后跑 publish_fingerprint --check 与 audit_tool）

## 关联报告

- `content/economy/insight/reports/2026-12_baseline_report.html`
- `content/economy/trends/reports/2026-11-13_weekly.html`
- `content/tech/weekly-roundup/reports/2026-11-13_weekly.html`
