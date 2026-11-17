# 任务启动 · 收尾自审计：8 项量化指标实测 + 回写《方案》v1.1

- slug：`final-self-audit`
- 起点：`main`；分支：`task/final-self-audit-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/final-self-audit/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug final-self-audit --title ...`

## 任务清单（4 项，详见 tasks.json）

- [pending] T-01 实测《方案》§八 8 项量化指标并记录到覆盖矩阵
- [pending] T-02 回写《方案》v1.1 版本行（Phase 0.4 方案 A / L3 批量补审 / P-06 P-09 延后）
- [pending] T-03 修复 local_mainline CLI（add_subparsers）并补回归测试
- [pending] T-04 登记 2 份审计文档（audit_tool init）使登记覆盖率 100%

## 风险登记（2 项，详见 risks.json）

- R-01 指标实测口径漂移（缓解：全部按《方案》§八 命令原样执行）
- R-02 回写引入偏差（缓解：仅追加版本行，不改结论）

## 关联报告

- 无（手工/工具类任务）
