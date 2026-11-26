# 任务启动 · 构建热点新闻实时追踪报告系统 hot-news-monitor

- slug：`hot-news-monitor`
- 起点：`main`；分支：`task/hot-news-monitor-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/hot-news-monitor/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug hot-news-monitor --title ...`

## 任务清单（6 项，详见 tasks.json）

- [pending] T-1 layout.json 注册顶层目录 hot-news-monitor 并递增分类版本留痕
- [pending] T-2 实现英文权威信源白名单 + RSS/HTTP 抓取器 + 聚合去重聚类与热度计算 + JSONL 存储
- [pending] T-3 实现 5 分钟周期调度与本地 API 服务(无感知刷新接口+运行日志)
- [pending] T-4 实现四大核心模块前端看板(三维排序筛选/三级信息层级/响应式/加载动画)
- [pending] T-5 实现三项等价验证(30-60分钟长跑+断点恢复/100条抽样准确性/全模块交互流畅性)
- [pending] T-6 统一门禁 optimization_gate 零 E,提交并创建 PR

## 风险登记（3 项，详见 risks.json）

- R-1 部分权威源网络不可达导致抓取失败（缓解：多源冗余+离线种子兜底+可达性降级告警）
- R-2 新增顶层目录触发结构/命名/门禁校验失败（缓解：预先在 layout.json 注册并复用统一门禁修复）
- R-3 新增文件导致 hub/指纹/发布日历等生成物漂移（缓解：不改动既有生成源,提交前重放校验）

## 关联报告

- 无（手工/工具类任务）
