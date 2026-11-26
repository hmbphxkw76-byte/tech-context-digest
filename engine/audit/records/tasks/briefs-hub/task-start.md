# 任务启动 · 热点专题机制泛化(自动轮换current)与首页集成

- slug：`briefs-hub`
- 起点：`main`；分支：`task/briefs-hub-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/briefs-hub/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug briefs-hub --title ...`

## 任务清单（5 项，详见 tasks.json）

- [pending] T-1 专题数据迁移 briefs/ + manifest index.json
- [pending] T-2 brief.py 支持 manifest 重建与 current 页(按快照Top1自动替换标题)
- [pending] T-3 server 路由 /report 与 report-nvidia 重定向;refresh 后自动重建
- [pending] T-4 build_hub.py 热点区块(确定性读 manifest)+看板导航条
- [pending] T-5 测试/截图/门禁/PR

## 风险登记（3 项，详见 risks.json）

- R-1 hub 生成物漂移破坏 CI --check（缓解：仅读入库确定性数据,提交后跑 html-sync 复核）
- R-2 旧分享链接失效（缓解：report-nvidia.html 保留 302 重定向）
- R-3 current 页依赖 runtime/state.json（缓解：缺失时回退最近专题并在页面标注）

## 关联报告

- 无（手工/工具类任务）
