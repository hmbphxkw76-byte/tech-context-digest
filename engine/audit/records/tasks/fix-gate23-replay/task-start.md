# 任务启动 · 门禁数量 21→23 收口 + 任务工件可重放性回归

- slug：`fix-gate23-replay`
- 起点：`main`；分支：`task/fix-gate23-replay-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/fix-gate23-replay/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug fix-gate23-replay --title ...`

## 任务清单（5 项，详见 tasks.json）

- [pending] T-1 修复 A：方案 v1.3 门禁数量 21→23 收口（§1.3/§四/§五 + 版本记录）
- [pending] T-2 修复 A：强化 test_pipeline_system_doc FORBIDDEN 并显式放行合法基线表述
- [pending] T-3 修复 B：5 个旧任务工件纯渲染重写回归（final-self-audit/fix-matrix-status/phase1-task-loop/phase3-static-linting/verification-prompt）
- [pending] T-4 文档回写：覆盖矩阵 v0.3（§九/§十 记录本次收口）
- [pending] T-5 验收：9 条命令逐项记录退出码与输出，提交经 --gate

## 风险登记（3 项，详见 risks.json）

- R-1 重写任务工件时误改 tasks/risks 实质内容（缓解：只经 load_artifacts→write_artifacts 纯渲染，事后 git diff 核对 id/title/description/mitigation 不变）
- R-2 强化 FORBIDDEN 误伤合法基线/更正表述（缓解：显式 ALLOWED 放行「基线 21 项」「由 21 项更正为 23 项」，断言 offenders=={} 真实成立）
- R-3 提交绕过门禁或直推 main（缓解：统一走 repo_sync run --gate，经 PR 合并）

## 关联报告

- `engine/report-audits/mainline-adoption-assessment-2026-11-17.md`
- `engine/report-audits/mainline-adoption-coverage-matrix.md`
