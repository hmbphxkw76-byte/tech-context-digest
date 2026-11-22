# 任务启动 · 本地补跑审计四环节（strict + accept + index + 指纹采集）

- slug：`audit-strict-local`
- 起点：`main`；分支：`task/audit-strict-local-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/audit-strict-local/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug audit-strict-local --title ...`

## 任务清单（4 项，详见 tasks.json）

- [done] T-1 audit_tool run --strict 写入登记并注入审计标识
- [done] T-2 audit_tool accept + index 收敛登记与索引
- [done] T-3 publish_fingerprint --emit 重采发布指纹
- [done] T-4 门禁复跑 + 提交与 PR

## 风险登记（2 项，详见 risks.json）

- R-1 CI 计费阻断，合并无 CI 检查，靠本地门禁 + unittest 兜底
- R-2 审计标识注入报告 HTML（内容层字节变更），经 page_build_check 与门禁校验

## 关联报告

- 无（手工/工具类任务）
