# 任务启动 · 英伟达最新事件专题追踪报告（近7天+本地链接）

- slug：`nvidia-tracking`
- 起点：`main`；分支：`task/nvidia-tracking-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/nvidia-tracking/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug nvidia-tracking --title ...`

## 任务清单（5 项，详见 tasks.json）

- [pending] T-1 采集并核验近7天英文权威信源的英伟达相关报道(NVIDIA Newsroom/IR/SEC/主流权威媒体)
- [pending] T-2 实现专题报告生成器与数据落盘(runtime/nvidia_brief.json)
- [pending] T-3 前端增加深链(#event/id、?q=预设)并生成 dashboard/report-nvidia.html
- [pending] T-4 浏览器实测+截图证据+机器核验清单
- [pending] T-5 统一门禁零E,提交并创建PR

## 风险登记（3 项，详见 risks.json）

- R-1 部分权威站点网络不可达（缓解：多通道检索(web_search/web_fetch)+官方一手源优先,核实失败标注待核实）
- R-2 检索结果时效与真实性无法完全保证（缓解：每条留原文URL与抓取时间,数值与日期以官方一手源为准）
- R-3 新页面触发既有生成物校验漂移（缓解：仅新增独立文件,提交前重放统一门禁）

## 关联报告

- 无（手工/工具类任务）
