# 任务启动 · 迪拜长期居留签证业务线（黄金 / 绿卡）首期基线

- slug：`immigration-dubai-visa`
- 起点：`main`；分支：`task/immigration-dubai-visa-<session8>`（见 `branch_registry.json`）
- 计划工件目录：`engine/audit/records/` 下的 `tasks/immigration-dubai-visa/`
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
- 一键闭环：`python engine/tools/local_mainline.py run --slug immigration-dubai-visa --title ...`

## 任务清单（7 项，详见 tasks.json）

- [pending] T-1 新建 dubai 业务线骨架（business-config + 基线/月度提示词）
- [pending] T-2 采集英文官方来源并登记台账 / source_registry
- [pending] T-3 生成首期基线报告（md + canonical HTML）
- [pending] T-4 更新类型注册表 / 机构分级主数据 / layout.json / 测试断言
- [pending] T-5 重新生成 hub（index.html / reader.html）
- [pending] T-6 跑全量门禁与测试
- [pending] T-7 提交并开 PR

## 风险登记（4 项，详见 risks.json）

- R-1 u.ae 与 ICP 对房地产/企业家年限口径冲突（缓解：并列呈现并列入未核验清单 U-01）
- R-2 部分官方页抓取失败（WAM 公告）（缓解：标未核验，不直引，列入 U-02）
- R-3 新增业务线破坏既有测试断言（缓解：同步更新 test_tools 集合断言与类型注册表）
- R-4 并发会话共享工作区互相影响（缓解：仅提交本任务路径，走 PR 串行合并）

## 关联报告

- `content/international/immigration/dubai/reports/2026-11_baseline_report.html`
