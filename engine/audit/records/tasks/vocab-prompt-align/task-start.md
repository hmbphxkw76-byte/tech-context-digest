# 任务启动 · 补齐多主题提示词库术语对齐覆盖（分类全覆盖 + 规范形漂移修正）

- slug：`vocab-prompt-align`
- 起点：`main`；分支：`task/vocab-prompt-align-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/vocab-prompt-align/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug vocab-prompt-align --title ...`

## 任务清单（3 项，详见 tasks.json）

- [completed] T-1 economy README §2.2 补分类列、覆盖经济体与国家/区域经济组织并修正 IMF/巴塞尔协议III/LIBOR 别名
- [completed] T-2 tech README §2.2 补分类列、覆盖 9 个缺失分类并修正密码与身份认证/多因素认证规范形
- [completed] T-3 核验（vocab check/topic-check/optimization_gate/unittest）并提交

## 风险登记（2 项，详见 risks.json）

- R-1 新增核心术语行与词库别名不一致（缓解：逐条比对 terms.md 并以门禁校验）
- R-2 并发会话改写同一文件（缓解：提交前检查 git status 与 rebase）

## 关联报告

- 无（手工/工具类任务）
