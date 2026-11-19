# 任务启动 · A-03 数值一致率代理口径改写 + apartment 事实卡片新建与 I-04 口径对齐

- slug：`a03-fc`
- 起点：`main`；分支：`task/a03-fc-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/a03-fc/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug a03-fc --title ...`

## 任务清单（5 项，详见 tasks.json）

- [pending] T-1 A-03 改写为相邻显式数值对一致性代理并同步字典 note
- [pending] T-2 i04_fact_card 口径对齐（分母=有卡片库业务线报告数）
- [pending] T-3 新建 apartment_fact_cards.json（域 APT）并补报告指针
- [pending] T-4 fact_card_check FC-03 共享域动态派生 + README
- [pending] T-5 测试更新与台账登记

## 风险登记（2 项，详见 risks.json）

- R-1 代理分母偏小（缓解：显式呈现分母与局限,不掩盖）
- R-2 卡片编造（缓解：仅收录已核验/部分核验且有来源的事实）

## 关联报告

- 无（手工/工具类任务）
