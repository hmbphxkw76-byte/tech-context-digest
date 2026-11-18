# 任务启动 · P1/P2 剩余项收口（16 项）

- slug：`p1-remaining`
- 起点：`main`；分支：`task/p1-remaining-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/p1-remaining/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug p1-remaining --title ...`

## 任务清单（17 项，详见 tasks.json）

- [pending] P1-1 摘要越级修正（5 处）
- [pending] P1-2 证据强度一致性 + DC-08 门禁
- [pending] P1-3 「假设乘积」标注治理
- [pending] P1-4 行动项阈值数值化
- [pending] P1-5 trends 决策卡补全或显式豁免
- [pending] P1-6 来源登记字段扩展（unverifiable / updated）
- [pending] P1-7 R4 关键数字逐点指针（重新设计）
- [pending] P1-8 死链真实修复
- [pending] P1-9 四主题接入就绪化
- [pending] P1-11 词库规范形统一 + 缺口补录
- [pending] P1-14 数据层补薄 + raw 落仓
- [pending] P1-15 hub 卡片信息区分度
- [pending] P2-1 死代码清理（需授权）
- [pending] P2-5 主题 README 治理
- [pending] P2-6 审计报表增强（IGI 趋势）
- [pending] P2-7 报告结构加固
- [pending] V 终验 unittest + optimization_gate --probe + 专项门禁

## 风险登记（4 项，详见 risks.json）

- R-1 门禁加强暴露存量违规（缓解：滚动 gate-period 延迟强制期）
- R-2 R4 逐点指针误报率偏高（缓解：先离线抽样校准，误报率高则降级 W）
- R-3 四主题就绪化被空壳注水（缓解：IGI-01 要求 14 节齐全 + 有产出）
- R-4 死链修复涉及官方页迁移（缓解：逐条核实，无法修复则登记豁免）

## 关联报告

- `engine/report-audits/goal-alignment-batch-progress-2026-11-18.md`
