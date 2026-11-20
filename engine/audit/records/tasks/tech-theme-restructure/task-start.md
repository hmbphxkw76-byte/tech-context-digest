# 任务启动 · 科技主题 AI 安全/AI 应用归并与汇总页主题维度改版

- slug：`tech-theme-restructure`
- 起点：`main`；分支：`task/tech-theme-restructure-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/tech-theme-restructure/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug tech-theme-restructure --title ...`

## 任务清单（4 项，详见 tasks.json）

- [pending] T-1 布局与内容层结构归并(ai-security/ai-application)
- [pending] T-2 Weekly Roundup 拆分为 AI 安全/AI 应用两条周报并拆分数据资产
- [pending] T-3 build_hub 主题维度改版与 index/reader/INDEX 重生成
- [pending] T-4 文档/配置/测试同步与门禁验证

## 风险登记（2 项，详见 risks.json）

- R-1 路径迁移导致历史引用失效（缓解：check_links 白名单放行历史审计记录、活跃链接全量校验）
- R-2 维度模型变更影响工具链（缓解：全量 unittest 与 optimization_gate 验证）

## 关联报告

- `content/tech/ai-application/weekly-roundup`
- `content/tech/ai-security/weekly-roundup`
