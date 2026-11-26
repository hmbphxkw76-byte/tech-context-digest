# 任务启动 · 汇总页类型 chips 动态化 + 迪拜公寓投资分析业务线首期基线

- slug：`hub-chips-investment-line`
- 起点：`main`；分支：`task/hub-chips-investment-line-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/hub-chips-investment-line/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug hub-chips-investment-line --title ...`

## 任务清单（4 项，详见 tasks.json）

- [pending] T-1 build_hub 类型 chips 仅展示有报告类型并补测试
- [pending] T-2 新建 apartment-investment 业务线（business-config + 提示词实例化）
- [pending] T-3 执行首期基线八节报告与标的档案
- [pending] T-4 注册表/文档同步与门禁全绿

## 风险登记（2 项，详见 risks.json）

- R-1 新增阈值触发 metric_coverage L03 一致性校验（缓解：逐条对齐配置与报告措辞）
- R-2 来源 URL 未登记触发 source_check R1（缓解：以登记册 URL 为准回改链接）

## 关联报告

- `content/economy/dubai/apartment-investment/reports/2026-11_baseline_report.html`
