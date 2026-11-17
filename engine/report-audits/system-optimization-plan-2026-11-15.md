# 报告体系系统优化实施方案（入口可拦 · 出口可信 · 语义可增量 · 指标单一事实源）

> **状态**：已落地（P0/P1/P2 优化事项逐项落地记录见 §七；统一门禁 21 项已收敛）
> **交付定位**：把报告质量管控从「出口后置审核」升级为「入口可拦 + 出口可信 + 语义可增量 + 指标单一事实源」的全链路治理体系。
> **上游依据**：[框架诊断报告](framework-diagnostic-2026-11-14.md)、[量化研究体系优化实施方案](quant-system-optimization-plan-2026-11-14.md)。
> **基准日**：2026-11-15（T0）｜ **适用范围**：全仓库报告生产与审计链路（业务报告 + 审计报告 + hub/reader）。
> **证据边界**：仅基于仓库内已提交文件与既有实跑结果。**标注约定**：【事实】仓库可回溯；【推断】机制分析；【待补】需新增数据或核验。
> **硬性约束**：不得违反通用基座「结论边界」与来源语言规则；不得违反 `AGENTS.md` 页面构建规范、category-first 维度规则与「生成物确定性（无时间戳）」纪律；新增工具一律落地 `engine/tools/`，测试落地 `engine/tests/`。
> **最后更新**：2026-11-16

---

## 一、六项改造任务总表

| # | 改造任务 | 优先级 | 交付物 | 验收口径 |
|---|---|---|---|---|
| **T1** | 入口拦截：来源登记 + L0 前置门禁 | **P0** | `source_registry` 规范 + `source_check.py` + business-config 变量 | 新报告来源登记覆盖 100%；编造 URL / 断头数字 = `[E]` 阻断 |
| **T2** | 出口可信：final 判定收紧 + 标识分级 | **P0** | 改 `audit_tool.py` + `audit-mark.md` 三态标识 | 未做 L3 不得出「终审通过」；标识与 registry 一致率 100% |
| **T3** | 指标单一事实源：字典 + 采集存储 | **P0** | `metrics-dictionary.json` + `metric_registry.py` + 归一化存储 | 重叠指标阈值唯一；新增指标须先登记字典 |
| **T4** | 增量语义扩展：diff 驱动 + 插件协议 | **P1** | `semantic_diff.py` + `semantic_checks/` 插件协议 | 单次复核范围下降 ≥50%；新检查项可插拔接入 |
| **T5** | 发现口径统一：hub / audit / legacy | **P1** | 统一 `iter_reports()` + legacy 治理规则 | 发布面 = 审计面；legacy 不可直链、不发布 |
| **T6** | 效率保障：分层 + 缓存 + 监控 | **P1** | `perf_monitor.py` + 缓存机制 + CI 去重 | CI 时长增幅 ≤10%；门禁 P95 达标 |

---

## 二、分阶段路线图

| 阶段 | 周期 | 目标 | 阶段 gate |
|---|---|---|---|
| **Phase 1 入口与出口** | T0 → 2026-12-12 | 入口可拦、出口可信 | 新报告来源登记 100%；final 不再关键词化；发布面 = 审计面；CI 增幅 ≤10% |
| **Phase 2 事实源与增量** | 2026-12-13 → 2027-01-02 | 指标单一事实源、语义可增量 | 重叠指标阈值唯一；增量复核上线；5/5 矩阵达标 |
| **Phase 3 增强（可选）** | 2027-01-03 起 | 新鲜度 / 发布日历机器化 | A-04 机器判定；漏采告警 |

**责任边界（RACI）**：研究负责人（A，最终责任）；数据采集（R 采集 / C 口径）；平台 / CI（R 工具与门禁）；Agent（R 语义检查项）。

---

## 三、技术实现方案（摘要）

### 3.1 T1 · 入口拦截（L0 前置门禁）

- **来源登记**：业务线 `data/source_registry.json`，字段含 `source_id` / `tier`（1 官方一手 / 2 行业机构 / 3 挂牌门户 / 4 媒体转述）/ `publisher` / `url` / `lang` / `in_synthesis`；business-config 声明 `{{SOURCE_REGISTRY_PATH}}`。
- **规则**：R1 登记覆盖 / R2 分级邻近 / R3 双源 / R4 关键数字来源 / R5 语言规则 / R6 死链 / R7 机构分级主数据一致性；新报告 `[E]`、历史报告 `[W]`。
- **接口**：`source_check.py [--file <报告>] [--gate-period YYYY-MM] [--probe]`，退出码 0/1/2；纯函数 `check_report()` 供单测直接调用。
- **与既有节点关系**：不替代 L1 链接校验与 L3 语义；L3 的「来源可追溯率」改为消费 `source_check` 结果。

### 3.2 T2 · 出口可信（final 判定收紧 + 标识分级）

- **判定拆分**：`machine_final`（A1 / A5 / A6 + L1 全项，CI，真实退出码）与 `semantic_final`（A2 / A3 / A4 / A7 / A8 + L3 四项，Agent，审查记录为证据）。
- **标识三态**：`none`（未进入）/ `pre`（机器终审过、L3 未完成）/ `full`（四环节齐备且含 L3）；`audit_tool.py mark --level pre|full`；registry 增加 `mark_level`；未做 L3 不得使用「已审计」字样。

### 3.3 T3 · 指标单一事实源

- **字典**：`metrics-dictionary.json`（`metric_id` / `name` / `formula` / `threshold` / `severity` / `detected_by` / `owner` / `sources` / `caliber`），合并 audit L3 四项与 quality 21 指标的重叠项；字典变更须同步 `rubric.md` 与 `verification.md`。
- **采集与存储**：`metric_collect.py` → `data/processed/<theme>/<维度段...>/metrics/metrics.csv` → `metric_registry.py`（读 / 写 / 去重 / 口径映射 / 阈值校验）；既有 xlsx / md 台账通过 adapter 导入，原文件保留为展示层。
- **硬约束**：新增指标须先登记字典；未登记指标不得进入合成与报告。

### 3.4 T4 · 增量语义扩展

- **增量逻辑**：复用报告 diff 的 block 级 diff；`semantic_diff.py` 只对新增 / 修改 block 执行语义复核，删除块折叠；事件触发（新报告 push / 变更块数 > 20）+ 周期兜底（每周全量）。
- **插件协议**：`check(blocks, ctx) -> list[Finding]`；内置 `source_trace.py`（来源可追溯）、`consistency.py`（跨章节一致）、`inference.py`（事实 / 推断分离）、`caliber.py`（口径并列）；输出 `records/semantic/<report>.json`。

### 3.5 T5 · 发现口径统一

- `_common.iter_reports(include_archives, include_legacy)` 统一发现；`build_hub.py` 与 `audit_tool.collect_reports()` 改为调用它，禁止各自 `glob` / `rglob`。
- 分类规则：`reports/*.html`（发布 + 四环节 + 可注入标识）/ `reports/archives/`（不发布 + 轻量 L1）/ `reports/legacy/`、`sources/`（不发布 + 不审计）。

### 3.6 T6 · 效率保障

见 §四。

---

## 四、效率保障专项

| 指标 | 目标 | 度量方式 |
|---|---|---|
| L0/L1 全量门禁总时长 | P95 ≤ 60s | `perf_monitor.py` 汇总 |
| 单份报告 L1 | ≤ 2s | 单报告计时 |
| `source_check.py` 单份 | ≤ 1s | 单报告计时 |
| `build_hub.py --check` | ≤ 10s | 命令计时 |
| `audit_tool.py run` | ≤ 30s | 命令计时 |
| CI 全量时长 | 增幅 ≤ 10% | Actions step duration |
| 增量语义单份 | ≤ 30s（Agent 另计） | Agent 任务计时 |

**损耗阈值**：CI 总时长增幅 ≤10%（超限阻塞合并）；单工具增幅 ≤20% 或绝对值 ≤1s（超限建 `performance` Issue）；Agent 语义单次范围下降 ≥50%（未达标回退全量周批）；报告生成不得因门禁增加（门禁全部在落盘后异步执行）。

**埋点**：每工具输出 `duration_ms` / `files_scanned` / `cache_hit` / `exit_code`，汇总写入 `perf-status.json`；连续两次超阈值 → 自动建 Issue。**去重**：CI 负责全量 L1，`scheduled-maintenance` 只跑「变更相关 + 归档 / 索引 / hub」。

---

## 五、核心目标校验矩阵

| 核心目标 | 改造项 | 验收指标 | 目标 |
|---|---|---|---|
| 入口可拦 | T1 | 新报告来源登记覆盖率 | 100% |
| 入口可拦 | T1 | 编造 URL / 断头数字拦截 | `[E]` 阻断 |
| 出口可信 | T2 | final 关键词误判 | 判 `[E]` |
| 出口可信 | T2 | 标识与 registry 一致率 | 100%（含 L3 区分） |
| 语义可增量 | T4 | 单次复核范围 | 下降 ≥50% |
| 语义可增量 | T4 | 新检查项接入成本 | ≤0.5 人日 |
| 指标单一事实源 | T3 | 重叠指标阈值唯一性 | 单一 |
| 指标单一事实源 | T3 | 未登记指标拦截 | `[E]` |
| 发现口径一致 | T5 | 发布面 = 审计面 | 一致 |
| 效率无显著下降 | T6 | CI 时长增幅 | ≤10% |
| 效率无显著下降 | T6 | 门禁 P95 | ≤60s |
| 效率无显著下降 | T6 | 报告生成时长 | 不增加 |

---

## 六、风险与边界

1. **来源登记维护成本**：纳入数据采集 SOP，漏登触发 `[E]` 倒逼流程。
2. **历史报告兼容**：无登记、无 L3 的历史报告统一按 `[W]` / `pre` 处理，不追溯阻断。
3. **指标字典迁移风险**：adapter 导入须逐值比对，防止口径漂移。
4. **语义插件质量**：必须有单测与证据要求，禁止「感觉不一致」。
5. **效率风险**：须以基线对比判定，禁止无基线宣称「无影响」。
6. **标识权威性**：`pre` 与 `full` 必须视觉可区分，禁止以「预审」冒充「已审计」。

---

## 七、优化事项落地状态（2026-11-16 核验）

> 统一复用入口（硬性）：全部确定性检查收敛为 `engine/tools/optimization_gate.py`（21 项，退出码 0/1/2）。本地 `repo_sync run --gate` → `ci.yml` / `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml` → `audit.yml`（fail-fast，`audit_tool verify` 内含 `source_check`）。阶段 × 复用映射见 [report-process-reuse.md](../docs/report-process-reuse.md) §三；一致性由 `test_process_gates.py::TestOptimizationGateReuse` 强制。

| 优先级 | 优化事项 | 落地载体 | 状态 |
|---|---|---|---|
| P0 | 邻近判定逻辑 | `source_check.proximity_ok()`（`PROXIMITY_WINDOW`） | ✅ |
| P0 | 机构分级主数据与一致性（R7：M1–M5） | `institution_tiers.json` + `check_institution_consistency()` | ✅ |
| P0 | metrics-dictionary 别名唯一 / 冲突去重 | `metrics-dictionary.json` + `metric_registry` | ✅ |
| P0 | gate-period 前置 + L0 真阻断 | `check_report` 前置降级；`BLOCKING_RULES={R6}` | ✅ |
| P0 | 十二类 ↔ 注册类型映射 | `engine/docs/report-classification.md` / `engine/templates/*` 口径修正 | ✅ |
| P0 | R5 语言规则 token 化分级 | `parse_language_rule` / `check_language` | ✅ |
| P0 | 审计不卡死（宽限期 / 语义权威） | `audit_tool.agent_stage_pass()` / `in_grace()`（`L3_GRACE_DAYS=14`） | ✅ |
| P0 | machine_final 接统一门禁 | `audit_tool._run_gate()` → `optimization_gate.run_checks(probe=True)` | ✅ |
| P0 | R6 死链分级 + 真阻断 | `source_check.probe_urls_detail()` + `--probe --probe-lenient` | ✅ |
| P0 | 提交前默认门禁 | `repo_sync run` 默认 `--gate` | ✅ |
| P1 | 外部 URL 自动探测接入 R6 | `source_check.probe_urls()` + `--probe` | ✅ |
| P1 | 发布日历结构化采集 | `release_calendar.py` + `release-calendar.json` | ✅ |
| P1 | 去重血缘与冲突明细 | `metric_registry.dedupe_rows()` + `export --dedupe --lineage` | ✅ |
| P1 | 类型声明结构化 + classify 双校验 | `_common.parse_report_type` / `TYPE_CADENCE`；`classify_reports.owner_signals` | ✅ |
| P1 | 指标字典全量准确性兜底 | `metric_registry.check_all_metrics()` + CLI `audit` | ✅ |
| P1 | 阶段去重 | 四工作流一律仅调 `optimization_gate --probe` | ✅ |
| P1 | 增量语义 scan | `semantic_diff.py scan` 纳入统一门禁 | ✅ |
| P1 | 性能接入 | `perf_bench.py` + `perf_monitor.py check` 入定时维护 | ✅ |
| P1 | 字典消费方 | `audit_tool.cmd_accept` 调 `metric_registry.check_all_metrics()` | ✅ |
| P1 | 发布日历 / 指纹接入 | `release_calendar --emit`；`publish_fingerprint --emit` | ✅ |
| P2 | 采集覆盖率度量 | `source_check.coverage_report()` + `--coverage` | ✅ |
| P2 | 发布指纹 | `publish_fingerprint.py` + `records/publish_fingerprints.json` | ✅ |
| P2 | 分类边界单测 | `engine/tests/test_classify_boundary.py` | ✅ |
| P2 | 发现口径统一 | `build_index.py` / `source_check.py` 改用 `iter_business_reports()` | ✅ |
| P2 | 告警补齐 | ci / html-sync / audit 增加失败 Issue 或 webhook 告警 | ✅ |

**工具生产引用核对**：上述全部工具均被统一门禁或工作流引用，无「已实现未接入」孤儿模块。

### 7.1 集成完整性（阶段 × 门禁 × 工作流）

| 阶段 | 门禁接入点 | 关键工具 |
|---|---|---|
| 采集 | `source_check`（统一门禁内，`--probe`） | `source_check.py`、`institution_tiers.json`、`release_calendar.py` |
| 分类 / 归位 | 统一门禁 `classify`；维护 / 内容更新 `--apply` | `classify_reports.py`、`_common.parse_report_type` |
| 生成 | 生成后由统一门禁校验（`hub` / `page_build`） | `md2html.py`、`build_hub.py` |
| 本地校验 | `repo_sync run` 默认 `--gate` | `repo_sync.py`、`optimization_gate.py` |
| CI 门禁 | `ci.yml` → `optimization_gate --probe`（唯一入口） | 21 项确定性检查 |
| 自动提交 | `html-sync` / `content-update` / `scheduled-maintenance` | `archive_reports` / `build_index` / `release_calendar --emit` / `publish_fingerprint --emit` |
| 审计 | `audit.yml` → `audit_tool run --strict` | `audit_tool._run_gate()`、`metric_registry` |
| 发布 / 索引 | 统一口径 `iter_business_reports` | `build_hub.py`、`build_index.py` |
| 监控 / 告警 | 失败 Issue 或 `webhook-alert` | `automation_status.py`、`webhook-alert.yml` |
| 增量语义 / 效率 | 统一门禁 `semantic_diff`（warn）/ `perf_monitor`（warn） | `semantic_diff.py scan`、`perf_bench.py`、`perf_monitor.py` |

**统一门禁 21 项**：validate / validate_layout / lint / compliance / classify / region_topics / links / hub / page_build / source_check / metric_registry / metric_audit / release_calendar / publish_fingerprint / semantic_diff / perf_monitor / research_kernel / info_density / fact_card / decision_hub / blind_spot。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-15 | 初始版本 | 六项改造任务、技术设计、效率专项、checklist 与校验矩阵 |
| v1.1 | 2026-11-15 | 落地状态 | 新增 §七：P0/P1/P2 优化事项 → 代码 / 测试 / 门禁映射 |
| v1.2 | 2026-11-16 | 精简与核验 | 合并重复章节；落地状态按 2026-11-16 实跑核验刷新 |
