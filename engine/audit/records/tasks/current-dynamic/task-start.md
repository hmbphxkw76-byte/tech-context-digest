# 任务启动 · brief-current 动态化（移出仓库+/report 服务端渲染）与 soak 口径补充

- slug：`current-dynamic`
- 起点：`main`；分支：`task/current-dynamic-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/current-dynamic/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug current-dynamic --title ...`

## 任务清单（4 项，详见 tasks.json）

- [pending] T-1 git rm brief-current.html+.gitignore+server /report 动态渲染
- [pending] T-2 README/soak 补充 6h 周期下 --interval 覆盖口径
- [pending] T-3 单测(动态路由)/静态检查/build_hub --check/浏览器实测
- [pending] T-4 统一门禁+PR+合并+清理

## 风险登记（3 项，详见 risks.json）

- R-1 /report 依赖快照（缓解：无快照时服务端即时刷新,失败返回明确提示）
- R-2 Pages 无动态页（缓解：hub 只链静态样板专题,current 仅本地(已声明)）
- R-3 rebuild_all 磁盘副本保留供调试但被 ignore,需防止误提交

## 关联报告

- 无（手工/工具类任务）
