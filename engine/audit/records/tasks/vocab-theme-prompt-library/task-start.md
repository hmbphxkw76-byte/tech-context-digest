# 任务启动 · vocabulary 归并六主题 + 多主题提示词库建设

- slug：`vocab-theme-prompt-library`
- 起点：`main`；分支：`task/vocab-theme-prompt-library-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/vocab-theme-prompt-library/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug vocab-theme-prompt-library --title ...`

## 任务清单（8 项，详见 tasks.json）

- [pending] T-1 六主题分类与归并映射设计（ID 前缀/受控分类/sync 绑定口径）
- [pending] T-2 词汇库归并：economy+financial-markets→economy，ai-agent+ai-security+cybersecurity→tech
- [pending] T-3 新建 education/international/political/society 空主题并建立词库骨架
- [pending] T-4 更新 topics.json/sync.json/INDEX.md/exports，移除旧主题注册与目录
- [pending] T-5 重建 4 个 business-config 的词汇同步区块（按分类过滤）
- [pending] T-6 建立 engine/vocabulary/prompts/<theme>/ 六主题提示词库
- [pending] T-7 更新 structure-and-naming-spec、vocabulary README、AGENTS.md 指针
- [pending] T-8 全量校验（vocab check/topic-check/unittest/optimization_gate/page_build_check）并提交 PR

## 风险登记（4 项，详见 risks.json）

- R-1 归并产生跨主题词条冲突（幻觉/模型上下文协议/SWE-bench）（缓解：保留更完整定义并合并别名后重编号）
- R-2 合并后同步区块语义漂移（AI 安全与 AI Agent 两块并成一块）（缓解：用 categories_include 过滤，digestion 按分类分组保留语义边界）
- R-3 旧主题目录删除不可逆（缓解：先归并校验通过再删除，全程 git 留痕可回滚）
- R-4 空主题无术语支撑导致编造（缓解：仅建分类+提示词骨架+信息缺口清单，词条留空待采集）

## 关联报告

- 无（手工/工具类任务）
