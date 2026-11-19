# 任务启动 · A-03 登记册真值核对 + 其余不达标项 P0（A-05/L-03/R-03）

- slug：`a03-truth`
- 起点：`main`；分支：`task/a03-truth-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/a03-truth/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug a03-truth --title ...`

## 任务清单（5 项，详见 tasks.json）

- [pending] T-1 A-03 真值核对（apartment 登记册同周期比对）
- [pending] T-2 A-05 死链修复与 unreachable 复查
- [pending] T-3 L-03 报告阈值与 business-config 对齐
- [pending] T-4 R-03 跨主题重复段落去重/指针化
- [pending] T-5 P1 滚动/阻塞登记（IGI-02/C-05/IGI-03/I-08）

## 风险登记（2 项，详见 risks.json）

- R-1 真值核对跨期误判（缓解：仅同周期纳入分母,跨期标不可比）
- R-2 链接不可达（缓解：不放宽明确可达定义,无法解决登记豁免）

## 关联报告

- 无（手工/工具类任务）
