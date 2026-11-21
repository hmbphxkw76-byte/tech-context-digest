# 任务启动 · 数据卫生治理：R7 机构分级一致性 + R8 登记字段回填

- slug：`data-hygiene-r7r8`
- 起点：`main`；分支：`task/data-hygiene-r7r8-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/data-hygiene-r7r8/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug data-hygiene-r7r8 --title ...`

## 任务清单（5 项，详见 tasks.json）

- [done] T-1 补录 57 家缺失机构至 institution_tiers.json
- [done] T-2 统一登记册分级（9 条偏离项）
- [done] T-3 修正 business-config 来源优先级引用（Eurostat / UN Digital Library）
- [done] T-4 R8 回填 document_tier / statement_type / evidence（410 条）
- [done] T-5 全量回归与提交

## 风险登记（2 项，详见 risks.json）

- R-1 官方数据库分级口径歧义（缓解：统一按 master 定义（官方/多边=1）并对齐 business-config）
- R-2 evidence 批量回填的合规性（缓解：仅结构化既有登记信息（method=manual + snapshot_date=updated），note 透明标注未留存 archive_hash）

## 关联报告

- 无（手工/工具类任务）
