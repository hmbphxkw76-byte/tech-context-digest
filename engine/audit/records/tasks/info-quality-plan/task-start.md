# 任务启动 · 信息质量改进实施方案 v1.0（5 项问题 / 5 个杠杆）

- slug：`info-quality-plan`
- 起点：`main`；分支：`task/info-quality-plan-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/info-quality-plan/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug info-quality-plan --title ...`

## 任务清单（6 项，详见 tasks.json）

- [done] T-1 生成信息质量改进实施方案文档
- [done] T-2 落盘校验（naming / validate_layout / check_links / optimization_gate）
- [done] T-3 任务分支提交并开 PR
- [done] T-4 批 A 工具改动收口（IGI-05 口径校准 / A-01·A-03·L-03·R-03 接线 / 自链接防刷）
- [done] T-5 IGI 趋势快照接入定时维护（C 轨道）
- [done] T-6 方案文档追加「就绪 + 阻塞说明」（v1.1）

## 风险登记（2 项，详见 risks.json）

- R-1 文档内路径 token 触发断链门禁（缓解：逐条复跑 check_links 并修正）
- R-2 提交夹带无关未跟踪文件（缓解：仅显式 paths 提交本方案与任务计划）

## 关联报告

- `engine/report-audits/information-quality-improvement-plan-2026-11-19.md`
