# 任务启动 · main 首亲历史直推审计（补偿服务端分支保护缺失）

- slug：`git-history-audit`
- 起点：`main`；分支：`task/git-history-audit-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/git-history-audit/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug git-history-audit --title ...`

## 任务清单（5 项，详见 tasks.json）

- [completed] T-1 新增 engine/tools/git_history_audit.py（main 首亲历史直推检测，单一事实源）
- [completed] T-2 新增单测 engine/tests/test_git_history_audit.py（含误报口径用例）
- [completed] T-3 CI 接入 ci.yml（push main 触发 history-audit）并纳入 webhook-alert needs
- [completed] T-4 文档更正 AGENTS.md 与 multi-session-git-protocol.md（服务端保护不可用 + 补偿控制 + 审计口径）
- [completed] T-5 核验（unittest/optimization_gate/check_links）并提交

## 风险登记（2 项，详见 risks.json）

- R-1 审计误报（squash/rebase 合并）（缓解：允许 (#NN) 与历史白名单，测试覆盖）
- R-2 与既有 ci.yml 门禁冲突（缓解：复用 workspace-cleanup，不改动既有 job）

## 关联报告

- 无（手工/工具类任务）
