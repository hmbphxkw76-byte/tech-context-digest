# 任务启动 · 全量报告核验收口：关键指标一手来源复核 + 台账/覆盖完整性补齐

- slug：`verification-closure`
- 起点：`main`；分支：`task/verification-closure-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/verification-closure/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug verification-closure --title ...`

## 任务清单（6 项，详见 tasks.json）

- [pending] T-1 基线门禁与核验对象清点（22 报告 / 353 md / index+hub）
- [pending] T-2 台账覆盖缺口修复（immigration/dubai 11 条来源补登哈希链）
- [pending] T-3 并行深度核验各业务线决策关键指标（web_fetch 一手来源）
- [pending] T-4 核验结果回写（source_registry 状态/evidence、事实卡片、报告核验统计）
- [pending] T-5 文档与 hub/index 页面一致性收口
- [pending] T-6 门禁/审计收口 + workspace_cleanup + PR

## 风险登记（3 项，详见 risks.json）

- R-1 并行会话共用工作区（缓解：独立 worktree 隔离，仅提交本任务文件）
- R-2 一手来源不可达/反爬（缓解：如实标注 unreachable，不虚报覆盖率）
- R-3 台账 append-only 并发写冲突（缓解：由主会话串行追加）

## 关联报告

- 无（手工/工具类任务）
