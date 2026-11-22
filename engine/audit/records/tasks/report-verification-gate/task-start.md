# 任务启动 · 报告层未核验信息门禁 + 生成前核验接线 + 历史清理

- slug：`report-verification-gate`
- 起点：`main`；分支：`task/report-verification-gate-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/report-verification-gate/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug report-verification-gate --title ...`

## 任务清单（5 项，详见 tasks.json）

- [pending] T-1 新增 report_verification_check 报告层一致性门禁
- [pending] T-2 接入 optimization_gate 31→32 并同步 CI/文档/测试
- [pending] T-3 生成前核验接线（content-update + pipeline_runner）
- [pending] T-4 更新信息核验/分层规范文档
- [pending] T-5 历史任务工件与残留清理

## 风险登记（2 项，详见 risks.json）

- R-1 新门禁误报历史报告（缓解：缓解=两级 gate-period，历史 [W]）
- R-2 文档门禁数量口径漂移（缓解：缓解=test_pipeline_system_doc 锁定）

## 关联报告

- 无（手工/工具类任务）
