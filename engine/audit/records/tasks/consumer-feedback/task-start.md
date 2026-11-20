# 任务启动 · 消费端反馈机制

- slug：`consumer-feedback`
- 起点：`main`；分支：`task/consumer-feedback-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/consumer-feedback/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug consumer-feedback --title ...`

## 任务清单（5 项，详见 tasks.json）

- [done] T-06 报告/hub 反馈入口 + 消费侧指标草案
- [done] T-07 补全报告页脚反馈入口（闭合 T-06 自身验收 + 监控通用规范 §5）
- [done] T-08 消费端反馈台账 engine/audit/records/consumer-feedback.json
- [done] T-09 CF-01/02/03 接线 + 字典草案转正
- [done] T-10 回归收口：hub/指纹/门禁/单测 + 提交 PR

## 风险登记（4 项，详见 risks.json）

- R-1 破坏无 JS 可用性（缓解：保持渐进增强：反馈入口为纯静态链接，无 JS / 外部服务依赖）
- R-2 报告字节变更引发发布指纹漂移（缓解：同批 publish_fingerprint --emit 重采，check 归零；audit.yml 已加指纹采集根治）
- R-3 报告页脚自引用 URL 拉低 IGI-04 来源登记覆盖率（缓解：IGI-04 排除本仓库自引用（与 source_check R6 同口径），IGI-04 回升至 0.9946）
- R-4 CF-02 / CF-03 读数为 0 被误读为体系退化（缓解：字典 note 显式注明为「消费闭环尚未启动」的真实信号，不伪造、不标 probe）

## 关联报告

- 无（手工/工具类任务）
