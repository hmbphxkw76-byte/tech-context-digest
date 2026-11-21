# 任务启动 · ai-application 目录对齐 ai-security 并生成首期基线

- slug：`ai-application-align`
- 起点：`main`；分支：`task/ai-application-align-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/ai-application-align/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug ai-application-align --title ...`

## 任务清单（7 项，详见 tasks.json）

- [pending] T-1 删除 trends 业务线（content + data）
- [pending] T-2 新建三条 ai-application 业务线骨架（business-config + 提示词）
- [pending] T-3 生成三条线首期基线报告
- [pending] T-4 同步 layout.json / 测试 / check_links / 词汇配置
- [pending] T-5 重新生成 hub（index.html / reader.html）
- [pending] T-6 跑全部门禁与测试
- [pending] T-7 提交并开 PR

## 风险登记（3 项，详见 risks.json）

- R-1 基线报告内容来源不足导致门禁失败（缓解：以 ai-security 基线为结构参照，仅英文来源，缺数据处标假设/待核实）
- R-2 删除 trends 破坏既有测试断言（缓解：同步更新 test_tools 业务线集合断言）
- R-3 维度/命名校验失败（缓解：遵循 layout.json 声明并跑 validate_layout）

## 关联报告

- 无（手工/工具类任务）
