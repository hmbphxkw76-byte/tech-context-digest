# 任务启动 · S5 工程噪声收口：静态检查 baseline + 高价值修复

- slug：`lint-baseline`
- 起点：`main`；分支：`task/lint-baseline-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/lint-baseline/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug lint-baseline --title ...`

## 任务清单（6 项，详见 tasks.json）

- [done] T-1 ruff 安全自动修复（I001/F401）+ 高价值项手工修（E741/F841）
- [done] T-2 mypy 高价值项修复（类型注解 / None 守卫）
- [done] T-3 baseline 机制（lint-baseline.json + static_check 只拦新增）
- [done] T-4 tech-debt-ledger 登记静态检查债务
- [done] T-5 A-05 probe 接入 scheduled-maintenance
- [done] T-6 测试 + 门禁 + 提交 + PR

## 风险登记（2 项，详见 risks.json）

- R-1 自动修复改动导入顺序 / 未用导入可能影响行为（缓解：仅安全修复 + 全量单测 + 门禁复跑）
- R-2 baseline 若按行号会漂移（缓解：按 path×code 计数，不看行号）

## 关联报告

- 无（手工/工具类任务）
