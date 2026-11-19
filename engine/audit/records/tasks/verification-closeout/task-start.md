# 任务启动 · 验证对齐收口（N 类 + 语义真实性 + 内容覆盖）

- slug：`verification-closeout`
- 起点：`main`；分支：`task/verification-closeout-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/verification-closeout/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug verification-closeout --title ...`

## 任务清单（15 项，详见 tasks.json）

- [pending] T-1 N-8 指纹漂移 --emit（4 份→0）
- [pending] T-2 N-3 11 份 in-review 补 L3 终审（4/4）
- [pending] T-3 N-7 门禁确定性 E1 排查 + 台账登记
- [pending] T-4 N-1 p1-continue 工件收尾
- [pending] T-5 I-05→1.0 international 行动卡五要素+三档
- [pending] T-6 N-6 7 项 LLM 指标接线（measured≥35）
- [pending] T-7 L-03→1.0 三处语义一致升级
- [pending] T-8 N-5 A-03 真值核对转计分
- [pending] T-9 P1-4 ID-02 摘要密度治理
- [pending] T-10 P1-11 political/society 词库骨架非空
- [pending] T-11 P1-9 political/society 首报
- [pending] T-12 N-4 A-05 死链收口
- [pending] T-13 P0-2 盲区 P0 四类登记
- [pending] T-14 文档同步（台账/总方案/上游版本记录）
- [pending] T-15 全量门禁复跑 + 提交/PR

## 风险登记（3 项，详见 risks.json）

- R-1 并发 Agent 写同一工作树冲突（缓解：按文件归属分区，禁止跑全量 unittest/gate）
- R-2 内容产出编造来源（缓解：不虚构 URL/数值，无法核实标未核验）
- R-3 代理口径误当语义达标（缓解：字典 detected_by + 备注显式标注）

## 关联报告

- 无（手工/工具类任务）
