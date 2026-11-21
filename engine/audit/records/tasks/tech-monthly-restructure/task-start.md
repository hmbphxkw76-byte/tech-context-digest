# 任务启动 · 科技主题全线月度化与 ai-security/dubai 归位

- slug：`tech-monthly-restructure`
- 起点：`main`；分支：`task/tech-monthly-restructure-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/tech-monthly-restructure/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug tech-monthly-restructure --title ...`

## 任务清单（6 项，详见 tasks.json）

- [pending] T-1 删除 tech 下两处 weekly-roundup（content + data/processed）
- [pending] T-2 迁移 ai-security/security/dubai → ai-security/dubai（content + data/processed）
- [pending] T-3 新建 ai-application/trends 月度业务线（competitive-intelligence）
- [pending] T-4 现有 tech 线节拍改月度（business-config + 周期提示词模板）
- [pending] T-5 同步引用与生成物（template-registry / layout.json / 文档 / build_hub）
- [pending] T-6 定向门禁校验与提交

## 风险登记（3 项，详见 risks.json）

- R-1 路径迁移导致历史引用失效（缓解：缓解）
- R-2 ai-security/dubai 维度语义变化影响工具链（缓解：缓解）
- R-3 工作区存在 report-period 任务未提交改动（缓解：缓解）

## 关联报告

- `content/tech/ai-application/trends`
- `content/tech/ai-security/competitive-intelligence/dubai`
- `content/tech/ai-security/dubai`
- `content/tech/ai-security/industry-research/dubai`
