# 报告流程复用清单（PROCESS-REUSE-MANIFEST v1.3）

> **状态**：现行规范
> **用途**：确认「信息分层与决策交付」优化后的流程被**后续每一个阶段**一致复用，杜绝某阶段绕过新规范。
> **事实源**：[信息分层规范](../templates/information-layering-spec.md)、[决策交付规范](../templates/decision-delivery-spec.md)、[通用基座](../templates/prompt-generic-base.md) 第十/十一节。
> **校验**：`engine/tests/test_process_gates.py`（阶段复用一致性测试，接入 unittest / ci.yml）。
> **最后更新**：2026-11-17

---

## 一、阶段 × 复用映射

| 阶段 | 载体 | 复用的优化流程 | 强制确认 |
|---|---|---|---|
| 采集 | 人工 / Agent + `source_check.py` | 来源分级（通用基座 §4）、R5 语言规则、来源登记 | 新报告来源分级与语言规则由 `source_check` 把关 |
| 生成 | 类型模板 + business-config + 两份新规范 | 分层交付 / 信息等级四级 / 新增信息模块 / 事实卡片 / 决策卡 / 行动协议 / 场景切片 / ex-ante | 7 份 business-config + 16+ 份类型模板均声明强制项 |
| 本地校验 | unittest + 四门禁 + validate / compliance / page_build / research_kernel | ID-01–08、FC、DC-01–04、BS | 398 单测；新报告 0E |
| CI 门禁 | `ci.yml` → `optimization_gate.py --probe` | 四门禁 + 全部 P0/P1/P2 检查 | 新报告缺项 `[E]` 阻断 |
| 自动提交 | `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml` → 同一统一入口 | 四门禁（与 ci.yml 同规则同口径） | 三阶段均调用统一入口，不得分项重复 |
| 审计 | `audit.yml` 四环节 | 新报告须先过新门禁（前置） | 审计对象 = 已合规报告 |
| 发布 / 索引 | `build_hub.py` / `build_index.py` → hub / reader | 决策仪表盘作为业务线可发现；决策卡 / 场景切片可导航 | `build_hub --check` 通过 |
| 监控 / 告警 | `automation_status.py` / `webhook-alert.yml` | 门禁失败 → `automation-failure` | 失败告警链路不变 |

---

## 二、单一事实源与指针

- 门禁工具：`info_density_check.py`（ID-01–08、DC-05）、`fact_card_check.py`（FC-01–04）、`decision_hub_check.py`（DC-01–04）、`blind_spot_check.py`（BS-01–05）。
- 规范事实源：`information-layering-spec.md`、`decision-delivery-spec.md`；业务配置只实例化，不复述规则正文。
- 决策卡事实源：`data/processed/economy/insight/decision_cards.json`。
- 事实卡片事实源：`engine/fact_cards/*.json`。
- 盲区事实源：`engine/report-audits/blind-spot-ledger.md`。
- 指标事实源：`engine/tools/metrics-dictionary.json`。

---

## 三、统一门禁入口（optimization_gate，P0/P1/P2 复用）

P0/P1/P2 优化清单的全部确定性检查收敛为单一入口 **`engine/tools/optimization_gate.py`**，后续任何阶段均须复用该入口（不得另写一套检查命令），保证口径一致：

| 阶段 | 载体 | 复用方式 | 强制确认 |
|---|---|---|---|
| 本地提交 | `repo_sync.py run --gate` | 提交前调用统一门禁，[E] 拒绝提交 | `repo_sync.py` 含 `--gate` |
| PR / 推送 | `ci.yml` | 「优化流程一致性门禁（统一入口）」步骤 | 存在该步骤 |
| 自动同步 | `html-sync.yml` | 同上 | 存在该步骤 |
| 内容更新 | `content-update.yml` | 同上 | 存在该步骤 |
| 定时维护 | `scheduled-maintenance.yml` | 同上 | 存在该步骤 |
| 审计 | `audit.yml`（fail-fast）+ `audit_tool verify`（内含 source_check） | [E] 即阻断，不再告警后放行 | `::error::审计四环节未通过` |

- 门禁清单（32 项）：validate / validate_layout / lint / compliance / classify / period_check / region_topics / links / hub / page_build / source_check / verification_ledger / metric_registry / metric_audit / release_calendar / publish_fingerprint / semantic_diff / perf_monitor / research_kernel / info_density / fact_card / report_verification / decision_hub / blind_spot / vocab_drift / ruff / mypy / monitoring_render / consistency / naming / prompt_consistency / model_contract（以 `optimization_gate.py --list` 为准）。
- 两级 gate-period：内容四门禁 + 研究内核用 `--gate-period`；来源登记 `source_check` 用 `--source-gate-period`；**两级默认均为 `auto`（滚动基线 = 当前自然月）**，见 [report-pipeline-system.md](./report-pipeline-system.md) §5.2。
- 退出码：0 通过；1 存在错误项（阻断）；2 仅警告（不阻断）。
- 一致性由 `engine/tests/test_process_gates.py::TestOptimizationGateReuse` 强制：任一阶段未复用即失败。

---

## 四、版本治理（阶段复用）

- 核验 / 收敛型运行不升级版本号，只更新「本期读数时点」。
- 仅核心事实修正才升级版本号；历史版本保留不删。
- 阈值校准完成前（至 2027-06）所有信号灯标「预校准（ex-ante）」。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-15 | 初始版本 | 阶段 × 复用映射；四门禁接入 ci / html-sync / content-update / scheduled-maintenance；一致性测试 |
| v1.1 | 2026-11-15 | 统一门禁入口 | 新增第三节：P0/P1/P2 检查收敛为 `optimization_gate.py`，五阶段复用矩阵；`repo_sync run --gate`；一致性测试扩展 |
| v1.2 | 2026-11-16 | 计数刷新 | 生成阶段强制确认更新为 9 份 business-config / 16+ 类型模板 / 377 单测 |
| v1.3 | 2026-11-17 | 计数与口径刷新 | 生成阶段强制确认更新为 7 份 business-config / 16+ 类型模板 / 398 单测；维度口径对齐 `layout.json`（按主题声明） |
