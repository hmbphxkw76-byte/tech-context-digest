# 任务启动 · 英伟达专题报告最佳实践补齐（分层/核验/引用/缺口/决策卡/公开链接）

- slug：`report-polish`
- 起点：`main`；分支：`task/report-polish-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/report-polish/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug report-polish --title ...`

## 任务清单（5 项，详见 tasks.json）

- [pending] T-1 brief 数据扩展(信息等级/摘要/缺口/决策卡/复核周期)与模板升级
- [pending] T-2 专题核验脚本 app/verify_brief.py(结构/白名单/可达性)+单测
- [pending] T-3 看板热度联动链接+来源层级筛选+时间线折叠
- [pending] T-4 GitHub Pages 部署并验证公开链接可达
- [pending] T-5 unittest/ruff/mypy/浏览器截图/门禁/PR

## 风险登记（3 项，详见 risks.json）

- R-1 Pages 部署属共享状态操作（缓解：仅在仓库已 public 前提下启用 root 源,失败则回退本地链接并说明）
- R-2 可达性探测受网络限制（缓解：不可达只标注不阻断,报告口径不受影响）
- R-3 数据字段扩展破坏既有渲染（缓解：保留旧字段兼容,单测锁定）

## 关联报告

- 无（手工/工具类任务）
