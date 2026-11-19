# 任务启动 · 待实施清单 5 工作流并发执行（方案/验证对齐 + 信息质量收口）

- slug：`ws-batch`
- 起点：`main`；分支：`task/ws-batch-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/ws-batch/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug ws-batch --title ...`

## 任务清单（5 项，详见 tasks.json）

- [pending] T-1 WS1 方案与验证对齐收口（S8 口径/台账登记/版本漂移/gap checklist 提交）
- [pending] T-2 WS2 度量接线与门禁确定性（A-05 接线/并行竞态/baseline 策略）
- [pending] T-3 WS3 内容质量补标与摘要重构（A-01/A-03/I-04/ID-02）
- [pending] T-4 WS4 第二期最小集产出（3+1 份，数据缺口显式标注）
- [pending] T-5 WS5 盲区消号与数据采集 + GLOSSARY/ADR

## 风险登记（3 项，详见 risks.json）

- R-1 并发写冲突（缓解：文件独占+主会话串行合并）
- R-2 内容编造（缓解：来源分级+不核实不写+数据缺口显式标注）
- R-3 取数阻塞（缓解：仅产出阻塞登记与检索留痕,不虚报消号）

## 关联报告

- 无（手工/工具类任务）
