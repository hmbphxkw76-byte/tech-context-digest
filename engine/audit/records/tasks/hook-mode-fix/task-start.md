# 任务启动 · 修复 .githooks 文件模式（644→755）以消除 CI 变基失败

- slug：`hook-mode-fix`
- 起点：`main`；分支：`task/hook-mode-fix-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/hook-mode-fix/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug hook-mode-fix --title ...`

## 任务清单（2 项，详见 tasks.json）

- [pending] T-1 将 .githooks/pre-commit 与 pre-push 的 git 索引模式改为 755（钩子须可执行）
- [pending] T-2 复跑触发维护流水线验证 submit-pr 变基不再失败

## 风险登记（1 项，详见 risks.json）

- R-1 模式变更影响本地（缓解：缓解=Windows core.filemode=false 无感；Linux 钩子本须可执行）

## 关联报告

- 无（手工/工具类任务）
