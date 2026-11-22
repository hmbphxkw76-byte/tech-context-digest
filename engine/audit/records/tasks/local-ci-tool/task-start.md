# 任务启动 · 本地等价 CI 工具与运行手册（本地优先·远程兜底·结果分享）

- slug：`local-ci-tool`
- 起点：`main`；分支：`task/local-ci-tool-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/local-ci-tool/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug local-ci-tool --title ...`

## 任务清单（4 项，详见 tasks.json）

- [done] T-1 新增 local_ci.py（14 项只读检查编排 + JSON/Markdown 输出 + 结果落盘）
- [done] T-2 新增 engine/docs/local-ci-runbook.md（分工/用法/分享/维护）
- [done] T-3 check_links 跳过 .meituan-catpaw（并行 worktree 非仓库内容）+ 单测
- [done] T-4 文档同步（tools/README、AGENTS.md）+ 结果落盘 local-ci-status.json + 门禁/单测复跑

## 风险登记（2 项，详见 risks.json）

- R-1 本地与远程 CI 口径差异（网络探测归远程）（缓解：runbook 明确分工）
- R-2 并行会话 worktree 触发断链/拖慢扫描（缓解：check_links 跳过 .meituan-catpaw）

## 关联报告

- 无（手工/工具类任务）
