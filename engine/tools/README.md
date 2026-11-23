# engine/tools 使用文档

CI 工具链使用说明。所有工具基于仓库根目录相对路径运行（自动定位仓库根），
在仓库根目录执行即可；通用层 + 业务层（`{地区}/{物业类型}/`）结构见
[engine/templates/prompt-generic-base.md](../templates/prompt-generic-base.md) 第 1.1 节。

## 环境准备

```bash
pip install -r requirements.txt   # openpyxl + markdown
python -m unittest discover -s engine/tests -v   # 单元测试（全量）
```

## 退出码约定（校验类工具统一）

| 退出码 | 含义 | CI 行为 |
|---|---|---|
| 0 | 通过（含空清单 / 无可处理项） | 继续 |
| 1 | 存在错误项 | 阻断 |
| 2 | 仅警告项 / 需人工确认 | 不阻断 |

## 工具一览

| 工具 | 类别 | 对应 CI 工作流步骤 |
|---|---|---|
| validate.py | 校验 | ci.yml / scheduled-maintenance「规范校验」 |
| page_build_check.py | 校验 | ci.yml / html-sync / scheduled-maintenance / content-update「页面构建规范门禁（PAGE-BUILD-SPEC）」 |
| validate_layout.py | 校验 | ci.yml / scheduled-maintenance「目录结构校验（layout.json 单一事实源）」 |
| check_links.py | 校验 | ci.yml「路径引用可达性」 |
| lint_reports.py | 校验 | ci.yml / scheduled-maintenance / content-update「报告内容校验」 |
| compliance_check.py | 校验+引导+审计 | ci.yml / content-update「报告模板合规校验」；scheduled-maintenance「报告合规性审计」 |
| source_check.py | 校验 | ci.yml「来源登记前置校验（L0）」：R1 登记覆盖 / R2 分级邻近 / R3 双源 / R4 关键数字 / R5 语言规则 / R6 死链 / R7 机构分级主数据一致性 / R8 登记字段（verify_status / updated） |
| metric_registry.py | 校验+服务 | 指标单一事实源（T3）：字典体检 / 阈值求值 / 归一化存储 / 去重血缘 / 全量准确性兜底；`audit --coverage` 叠加指标实测覆盖报告 |
| metric_coverage.py | 校验+度量 | 指标实测覆盖（批次 B）：TOOL 指标实测接线 + LLM/未接线显式标注 + 覆盖率与缺口报告 |
| release_calendar.py | 采集 | 发布日历结构化采集（P1-2）：解析 release-calendar.md → JSON + 覆盖率 |
| publish_fingerprint.py | 校验+留痕 | 发布指纹（P2-2）：sha256 登记 / 重复检测 / 漂移比对 |
| optimization_gate.py | 校验（统一入口） | ci / html-sync / content-update / scheduled-maintenance / `repo_sync run --gate` 复用；32 项门禁单一入口 |
| pipeline_manifest.json | 配置（声明式图） | 报告全流程 N0–N8 / G0–G8 声明式清单（流程图唯一落地载体） |
| pipeline_runner.py | 编排 | 节点→门禁→路由/退回；复用 `optimization_gate` 单一入口；见 `engine/docs/report-pipeline-implementation-plan.md` |
| local_ci.py | 编排（本地 CI） | 本地等价 CI（本地优先 · 远程兜底 · 结果分享）：复刻 ci / audit / html-sync / maintenance 的本地可读检查；见 `engine/docs/local-ci-runbook.md` |
| pipeline_audit.py | 审计 | 全流程追加式留痕 `engine/audit/records/pipeline_runs.jsonl` |
| research_kernel_check.py | 校验 | ci.yml「研究内核质量门禁（M4）」：新报告四项内核项（周期定位/传导量化/政策入模/盲区列示） |
| info_density_check.py | 校验 | ci.yml「信息密度与分层交付门禁」：分层结构 / 信息等级 / 新增信息模块 / 场景切片（ID-01–ID-08、DC-05） |
| fact_card_check.py | 校验 | ci.yml「事实卡片门禁（FC）」：卡片库结构 + 报告 `[FC-…]` 引用解析 + 共享域覆盖 + 跨层一致性（FC-04，恒 E） |
| report_verification_check.py | 校验 | 报告层信息核验（RV-01..03）：决策摘要纯净 + 未核验来源不得呈现为已核验 / 部分核验 + 来源状态文本一致；接入统一门禁与 G2 / G4 |
| decision_hub_check.py | 校验 | ci.yml「决策交付门禁（DC）」：决策卡字段 / 行动协议五要素 + 三档优先级 / 场景切片 / ex-ante |
| blind_spot_check.py | 校验 | ci.yml「盲区台账门禁（BS）」：字段 / 状态 / 责任周期 / P0 四类 |
| monitoring_render_check.py | 校验 | 监测渲染规范机械项（MON-01–05）：图注齐备 / 口径并列 / 列宽塌缩 / noopener / 原生 title；接入统一门禁 |
| consistency_check.py | 校验 | 看板-台账一致与版本治理（LC-01–02 / VG-01–02）：台账结构 / 指标名在报告出现 / 读数时点 / 语义版本修正留痕 |
| naming_check.py | 校验 | 命名规范全量扫描（NC-01–02）：目录 kebab-case / 按位置文件命名规则矩阵 |
| prompt_consistency_check.py | 校验 | 提示词一致性（PC-01–03）：类型注册表与实际业务线一致 / business-config 不复述规范 / 周期提示词齐备 |
| model_contract_check.py | 校验 | 模型契约（MC-01–05，DC-07）：参数区间 / 假设留痕 / 失败上报；接入统一门禁 |
| cycle_clock.py | 量化模型 | 方案 N1：宏观周期时钟（四阶段 + 过渡带） |
| signal_synth.py | 量化模型 | 方案 N2：K 系三层信号合成 |
| policy_multiplier.py | 量化模型 | 方案 N3：政策乘数表（G01–G05） |
| transmission.py | 量化模型 | 方案 N4：传导弹性（OLS + VAR） |
| valuation.py | 量化模型 | 方案 N5：cap rate / DCF / 相对估值 |
| market_sizing.py | 量化模型 | 方案 N6：TAM/SAM/SOM 规模测算 |
| stress_test.py | 量化模型 | 方案 N7：尾部情景压力测试 |
| monte_carlo.py | 量化模型 | 方案 N8：蒙特卡洛（VaR/ES） |
| threshold_calibration.py | 量化模型 | 方案 4.3：阈值滚动校准 + 状态计数 |
| classify_reports.py | 校验+修复 | scheduled-maintenance / content-update「报告自动归位」 |
| ensure_region_topics.py | 校验+修复 | ci.yml / scheduled-maintenance「结构补全」 |
| verification_vocab.py | 校验（词表） | 核验状态词表单一事实源（INFORMATION-VERIFICATION-SPEC v1.1）：英文枚举 ↔ 中文等级双向映射 |
| verification_ledger.py | 留痕 | 核验台账哈希链（append-only，落 `engine/audit/records/verification_ledger.jsonl`） |
| verification_review.py | 复核 | 来源定期复核与到期告警（落 `pending_verification.json`） |
| source_normalize.py | 校验+归一 | 来源归一化（URL / 机构名 / 主机 / 日期），供登记去重与 R7 匹配复用 |
| vocab_drift_check.py | 校验 | 词库漂移门禁（VOCAB-DRIFT-CHECK v1.0） |
| period_check.py | 校验 | 报告周期校验（落款 period 不得晚于当前自然月） |
| gate_period.py | 规范 | 两级 gate-period 解析（滚动基线，单一事实源） |
| static_check.py | 校验 | ruff / mypy 适配层 → 统一门禁退出码，baseline 只拦新增 |
| task_plan.py | 任务闭环 | 任务计划工件（plan / tasks / risks / task-start）；`repo_sync --gate` 前置 |
| local_mainline.py | 编排 | 本地 mainline 一键闭环（薄封装，只编排不重写校验） |
| indicator_sidecar.py | 生成 | 指标登记册 sidecar（确定性、可重放、无墙钟时间戳） |
| info_gap_metrics.py | 度量 | 信息差指数（IGI）实测计算 |
| proxy_calibration.py | 量化模型 | 代理指标抽样校准（PROXY-CALIBRATION v1.0，方案 T-02） |
| semantic_diff.py | 校验 | 增量语义 diff（T4）：仅对本期相对上期的新增 / 修改块复核 |
| consumer_feedback.py | 反馈台账 | 消费端反馈台账（CONSUMER-FEEDBACK-LEDGER v1.0） |
| finding_rule.py | 反馈台账 | finding→规则回写台账（FINDING-RULE-LEDGER v1.0） |
| remediation_ticket.py | 闭环 | 闭环修正工单（remediation_ticket） |
| a03_truth_check.py | 核验 | A-03 真值核对与计分 |
| perf_bench.py | 性能 | 性能基线压测（T6 / T0 基线） |
| perf_monitor.py | 性能 | 性能监控与结果缓存（T6） |
| `engine/audit/scripts/audit_tool.py` | 审计 | 审计报告标准化管理（AUDIT-MGMT v1.0）：四环节 / 标识 / 抽检 / L3 状态 |
| md2html.py | 生成 | html-sync / scheduled-maintenance「HTML 同步」 |
| report_style.py | 生成 | canonical 报告样式单一事实源（md2html / restyle_reports 共用） |
| restyle_reports.py | 生成 | 既有报告迁移到 canonical 样式 |
| archive_reports.py | 生成 | scheduled-maintenance「归档策略」 |
| build_index.py | 生成 | scheduled-maintenance「生成全局索引」 |
| build_hub.py | 生成 | ci.yml --check / html-sync、scheduled-maintenance「汇总页」 |
| update_planner.py | 编排 | content-update「生成任务清单」 |
| automation_status.py | 编排 | content-update / scheduled-maintenance「状态记录与活跃度」 |
| workspace_cleanup.py | 维护 | ci / html-sync / content-update / scheduled-maintenance / audit 各阶段「预清理 + 收尾清理」；`submit-pr` 提交前清理；`pre-push` 钩子 |
| branch_naming.py | 规范+登记 | 分支命名规范（BRANCH-NAMING-SPEC v1.0）：`task/<slug>-<session8>` 生成与校验、会话标识解析链、`branch_registry.json` 登记册；由 `repo_sync.py` 与 `.githooks/` 复用 |
| git_history_audit.py | 审计 | main 首亲历史直推检测（GIT-HISTORY-AUDIT v1.0）：识别「非合并、无 `(#NN)`、非 CI 留痕、不在白名单」的直接提交；由 `ci.yml::history-audit` 调用 |
| repo_sync.py | 网关 | 多会话统一提交网关：共享检出锁 / sync / push / pr / `run --gate` / 分支建改与审计 / 钩子安装；命名与直推守卫三重拦截 |

## 校验类

### page_build_check.py — 页面构建规范门禁（PAGE-BUILD-SPEC）

```bash
python engine/tools/page_build_check.py [--quiet]
```

按 `engine/docs/page-build-spec.md` §8 校验全部 hub 页与报告页：文档基础（lang /
viewport / charset）、canonical 主色与漂移色、`.skip-link` / 焦点 / 减少动态 /
打印、表格配平、报告骨架（页头 / 导航 / 容器）、`h2.sec` 与锚点、echarts 容器
`.chart-eh`、生成物确定性、体积预算。退出码 0/1/2（通过 / 有 `[E]` / 仅 `[W]`），
[E] 在 ci.yml、html-sync、scheduled-maintenance、content-update 中阻断。

### validate.py — 结构与规范校验

```bash
python engine/tools/validate.py
```

检查项：通用层根部 3 份共享文件齐全（`prompt-generic-base.md` / `monitoring-common-spec.md` /
`template-registry.md`）；各类型模板目录必备文件齐全（`market-monitoring/`、
`employment-research/`，清单见 `_common.TEMPLATE_TYPE_DIRS`，与
[engine/templates/template-registry.md](../templates/template-registry.md) 第二节登记一致）；
通用层全目录（含类型子目录）无业务关键词
（迪拜/公寓/Dubai/UAE/DLD/CBUAE/EIBOR 等，清单见 `_common.BUSINESS_KEYWORDS`）；
业务线目录结构（`prompts/business-config.md` 及其 `{{REGION}}/{{TOPIC}}/{{REGISTRY_PATH}}`
变量区）；`reports/` 内文件命名符合约定。

### validate_layout.py — 目录结构校验（layout.json 单一事实源）

```bash
python engine/tools/validate_layout.py
```

校验一级根目录合规（无未注册目录）、主题注册完整、业务线层级深度与主题维度数一致、
命名符合 kebab-case、地域段命中 `layout.regions` 白名单，以及**维度顺序按主题声明**
（`check_dimension_priority()` 校验维度序列自洽：无重复、无未登记维度名；与主题声明不符即判错）。
单一事实源为 [engine/tools/layout.json](../tools/layout.json)；新增主题 / 业务线只改该文件，
工具与 CI 自动适配。

### check_links.py — 路径引用可达性校验

```bash
python engine/tools/check_links.py            # 全量扫描
python engine/tools/check_links.py --verbose  # 同时列出已校验通过的引用数
```

扫描文本文件中的仓库相对路径、`./` 与 `../` 相对链接、GitHub `blob/main` URL，
逐条校验目标存在（含大小写敏感校验，避免 Linux CI 断链误报）。退出码 0 = 无断链。

### lint_reports.py — 报告内容校验

```bash
python engine/tools/lint_reports.py
```

扫描全部业务线 `reports/*.html`。**错误项（退出码 1）**：thead/tbody/table 标签不配对、
重复 `</tbody>`、畸形 `<th scope="col"ead>`。**警告项（退出码 2）**：
≥6 列表格 `<th>` 未声明百分比列宽、表格缺 `class="fixed"`、`<img>` 缺 alt。
纯函数 `lint_html(text)` 可被测试直接调用。

### optimization_gate.py — 优化流程统一门禁（单一入口）

```bash
python engine/tools/optimization_gate.py                      # 全部门禁（32 项）
python engine/tools/optimization_gate.py --only source_check,metric_registry
python engine/tools/optimization_gate.py --gate-period auto --source-gate-period auto --json
python engine/tools/optimization_gate.py --list
```

把 P0/P1/P2 全部确定性检查收敛为单一入口，供所有后续阶段复用（阶段 × 复用映射见
`engine/docs/report-process-reuse.md` 第三节）；退出码 0/1/2。**任何阶段不得另写一套检查命令**；
本地提交用 `repo_sync.py run ... --gate` 强制调用。

两级 gate-period（显式、可分别覆盖）：内容四门禁 + 研究内核用 `--gate-period`（默认 `auto` = 当前自然月）；
来源登记 `source_check` 用 `--source-gate-period`（默认 `auto` = 当前自然月）。全链路节点 × 防线 × 闭环见
`engine/docs/report-pipeline-system.md`。

### pipeline_runner.py — 报告全流程编排器（严格对齐 §1.1 流程图）

```bash
python engine/tools/pipeline_runner.py plan       # 由清单渲染流程图
python engine/tools/pipeline_runner.py validate   # 校验清单结构（9 节点 / 9 门禁 / 2 闭环）
python engine/tools/pipeline_runner.py gate G4    # 执行单个门禁
python engine/tools/pipeline_runner.py run --from N0 --to N8
python engine/tools/pipeline_runner.py audit --run <run_id>
```

按 `pipeline_manifest.json` 串行驱动 N0→G0→…→N8→G8，门禁**复用 `optimization_gate`**
（单一入口、同口径）；E 阻断按 `gate.on_fail` 精准退回（G6 → N4）。端到端方案与任务清单见
`engine/docs/report-pipeline-implementation-plan.md`；审计留痕见 `pipeline_audit.py`
（`engine/audit/records/pipeline_runs.jsonl`，只追加、可回放）。

### source_check.py — 来源登记前置校验（L0 入口拦截，T1）

```bash
python engine/tools/source_check.py                          # 全量（业务线正式报告）
python engine/tools/source_check.py --file <报告路径>         # 单份
python engine/tools/source_check.py --gate-period 2027-01    # 早于该周期降级为警告
python engine/tools/source_check.py --probe                  # 自动探测外部 URL 可达性（接入 R6）
python engine/tools/source_check.py --coverage               # 输出来源登记覆盖率
python engine/tools/source_check.py --self-test              # 内置合成用例自检
```

规则 R1–R8；退出码 0/1/2。**gate-period 前置**：历史报告由 `check_report` 内部把
R1–R6 的 `[E]` 前置降级为 `[W]`；**R7 结构性冲突（M3 重复 source_id / M4 同机构同登记多分级）任何周期都阻断**；
**R8 登记字段**（`verify_status` ∈ verified / media_unverified / unverifiable，`updated` = YYYY-MM-DD）仅 `[W]`，数据卫生不阻断。
R2 采用**邻近判定**（标注须出现在来源链接后 `PROXIMITY_WINDOW` 字符内）；
R5 为 **token 化分级**（`official_en`=`[E]`，`en_or_zh` 集外语言=`[W]`）；
R7 消费机构级分级主数据 `engine/tools/institution_tiers.json`（机构 → tier，
与 source_registry / business-config 来源优先级一致性校验）。

### metric_registry.py — 指标单一事实源（T3）

```bash
python engine/tools/metric_registry.py list      # 全部指标
python engine/tools/metric_registry.py check     # 字典体检（别名唯一 / 字段 / 阈值 / 级别）
python engine/tools/metric_registry.py audit     # 全量准确性检查（无实测值走兼底结构校验）
python engine/tools/metric_registry.py eval A-01 0.97
python engine/tools/metric_registry.py export --xlsx <path> --out <csv> --dedupe --lineage <json>
```

别名为跨指标唯一事实源（`dictionary_conflicts` / `dedupe_aliases` / `resolve_alias`）；
`--dedupe` 按 `(date, indicator_id, caliber)` 去重，默认**大小写敏感**，
`--lineage` 输出去重血缘与冲突明细；`check_all_metrics` 对字典全量指标给出结论
（有实测值求值，无实测值兜底结构校验，不静默跳过）。

### release_calendar.py — 发布日历结构化采集（P1-2）

```bash
python engine/tools/release_calendar.py --emit engine/report-audits/release-calendar.json
python engine/tools/release_calendar.py --check    # 字段完整率 + P0 维度覆盖
python engine/tools/release_calendar.py --list
```

### publish_fingerprint.py — 发布指纹（P2-2）

```bash
python engine/tools/publish_fingerprint.py --emit    # 采集正式报告 sha256 入库
python engine/tools/publish_fingerprint.py --check   # 漂移 / 重复内容检测
```

### compliance_check.py — 报告模板合规校验 / 模板引导 / 合规审计

校验规则与已注册类型模板骨架一一对应，规则文件为
[engine/templates/compliance-rules.json](../templates/compliance-rules.json)
（与 [template-registry.md](../templates/template-registry.md) 第二节登记一致；
周期未单独登记的类型按「结构逐字继承基线」回落校验）。报告类型自动识别：读取业务线
`prompts/business-config.md` 继承声明中的 `engine/templates/<类型ID>/` 引用。

```bash
python engine/tools/compliance_check.py --check        # 全量校验（CI 阻断式关卡）
python engine/tools/compliance_check.py --file <路径>   # 校验单份报告（开发自查）
python engine/tools/compliance_check.py --list-types   # 列出已注册类型与模板引用入口
python engine/tools/compliance_check.py --scaffold market-monitoring monthly   # 模板自动填充引导
python engine/tools/compliance_check.py --audit        # 历史报告合规审计（写审计报告，不阻断）
```

**校验口径**（结构完整性 / 必填字段 / 内容格式三类）：

- **错误项（阻断合并）**：h2 节数少于类型模板骨架（结构缺失）、章节编号 `id="sN"`
  不连续或不有序、缺 `<title>`、月/季/年周期报告缺顶部导航、
  锚点 `href="#x"` 无对应 id（断头锚点）。
- **警告项（不阻断）**：h2 节数超出骨架（如为业务固化锚需人工确认）、基线报告缺简化
  锚点导航、文件名不符合命名约定（无法识别周期）、业务线未注册类型。
- `--audit` 对全部历史报告执行同口径校验，匹配度汇总与逐项明细写入
  `engine/report-audits/compliance-audit.md`（定时维护提交留痕），发现不符合项退出码 2 并转
  预警 Issue，不阻断维护流水线。
- 纯函数 `check_report(text, rule, common)` / `detect_type(config_text)` /
  `cycle_rule(rules, type_id, cycle)` 可被测试直接调用。

### classify_reports.py — 报告自动归位

```bash
python engine/tools/classify_reports.py --check --unknown-warn   # 只检查
python engine/tools/classify_reports.py --apply --unknown-warn   # 执行移动
```

扫描散落在业务目录之外（仓库根、`engine/templates/` 全目录含类型子目录）的报告文件，
按文件名中地区/业务类型词判定归属并移入对应业务线 `reports/`；无法判定归属的报警告警
（`--unknown-warn` 时退出码 2）。

### ensure_region_topics.py — 结构补全（幂等）

```bash
python engine/tools/ensure_region_topics.py --check   # 只报告缺失
python engine/tools/ensure_region_topics.py           # 创建缺失子目录
```

为每条业务线补齐 `prompts/`、`reports/`、`data/` 三个子目录；缺
business-config.md 时告警。重复执行无副作用。

### validate_layout.py — 目录结构校验（layout.json 单一事实源）

```bash
python engine/tools/validate_layout.py            # 校验
python engine/tools/validate_layout.py --check    # 同上（显式声明）
```

校验一级根目录合规（无未注册目录）、主题注册完整、业务线层级深度与维度数一致、
目录段命名符合 `naming.pattern`、region 维度段命中 `regions` 白名单。
已注册未创建的主题报 INFO（不阻断）。退出码同「退出码约定」。

### check_links.py — 路径引用可达性校验

```bash
python engine/tools/check_links.py             # 全量扫描
python engine/tools/check_links.py --verbose   # 附带扫描文件数
```

扫描文本文件中的仓库相对路径、`./` 与 `../` 相对链接、GitHub `blob/main` URL，
逐条校验目标存在。特性：逐段**大小写校验**（防 Windows/Linux 差异）、业务目录
相对引用回退（如 `prompts/business-config.md`）、`.../` URL 截断标记豁免、
`data-search` 小写索引豁免、冻结文档/夹具/派生状态跳过。

## 生成类

### md2html.py — md → HTML 同步

```bash
python engine/tools/md2html.py
```

将业务线 `reports/*.md` 转换为同名自包含 HTML，输出 **canonical 报告样式**
（`report_style.CANONICAL_CSS`）：页头 `<header class="report-head">`（h1 + 副标题）、
顶部固定导航 `<nav class="report-nav">` + `.nav-tabs` 锚点、`<main class="wrap">`
正文（h2 重编号 `id="sN"` 且加 `class="sec"`）、表格 `class="fixed"` + 百分比列宽。
纯图表型简报（只出 HTML 的业务线）无 md 源时自动跳过。依赖 markdown 包。

### report_style.py — canonical 报告样式（单一事实源）

全部报告与 hub 共用的设计系统：设计令牌（`--navy:#16324f` 等，与
`build_hub.py` 的 `_STYLE` 同值）+ 基础排版 + 组件（页头 / 导航 / KPI 卡 /
图表 / 时间线 / 来源弹层 / 标签 / 声明）。`md2html.py` 与 `restyle_reports.py`
均从这里取样式，保证跨业务线、跨页面一致。

### restyle_reports.py — 既有报告迁移到 canonical

```bash
python engine/tools/restyle_reports.py --files <报告.html> [--rename-chart] [--fix-colors] [--dry]
```

替换 `<style>` 块为 canonical CSS；`--rename-chart` 把 echarts 容器
`class="chart"` 改名为 `class="chart-eh"`（canonical 中 `.chart` 是 trends 的
图表卡片）；`--fix-colors` 把旧令牌 `#1f3d63` 替换为 `#16324f`。

### archive_reports.py — 滚动归档（幂等）

```bash
python engine/tools/archive_reports.py
```

每类报告保留最新 N 期（monthly 12 / quarterly 8 / annual 5 / baseline 3），
超出部分移入业务目录内 `reports/archives/`。保留策略为纯函数
`select_archives(items, keep_map)`。

### build_index.py — 全局索引

```bash
python engine/tools/build_index.py
```

按业务线汇总全部报告，生成根目录 `INDEX.md`（含「最近生成」时间戳，作为
content-update 工作流的活跃度心跳）。

### build_hub.py — 汇总页

```bash
python engine/tools/build_hub.py          # 生成 index.html + reader.html
python engine/tools/build_hub.py --check  # 校验是否为最新
```

`index.html` 为按业务线分组的报告枢纽；`reader.html` 为在线阅读器（navy 渐变头部 +
sticky 筛选栏 + 侧栏报告列表 + iframe 阅读区，与主页共用设计令牌与公共组件，移动端
为抽屉式侧栏，`?report=<路径>` 直达）。`--check`：过期退出码 1；文件缺失（全新克隆）
退出码 0 并提示，由定时维护首建。比对前对两侧做归一化——抹平「最近生成」生成时刻
时间戳（分钟级心跳，不参与最新性判定），报告清单部分逐字节比对。

## 编排类

### update_planner.py — 内容更新任务清单

```bash
# porcelain JSON（content-update 工作流用于判断清单是否为空）
python engine/tools/update_planner.py --porcelain --pending-only > tasks.json
# 人读 md 清单
python engine/tools/update_planner.py --pending-only > tasks.md
# 限定项目 / 周期
python engine/tools/update_planner.py --project content/economy/dubai/apartment --period 2026-Q4
```

- `--period` 接受 `YYYY-MM` / `YYYY-Qn` / `YYYY`；缺省按当前 UTC 日期推导
  （季首月用季度标识，与工作流逻辑一致）。
- 周期推导规则：月度期 → 月度任务；季首月追加季度任务；1 月追加上一自然年年度任务。
- 任务状态：期望输出（如 `reports/2026-12_monthly.html`）已存在 → done，否则 pending；
  `--pending-only` 只留 pending。参数错误退出码 2。
- **条件节拍**：提示词正文含 `<!-- report-output: none -->` 时，该周期不产出报告文件，规划器不派任务
  （用于「核验型轻运行 / 无触发不启动新报告」的业务；tech 全线月度化后暂无此类业务线，示例保留机制说明）。
  判定见 `_common.prompt_produces_report()`。

### automation_status.py — 自动化状态与活跃度

```bash
# 记录一次执行（工作流 always 步骤调用）
python engine/tools/automation_status.py record --phase content-update \
    --result success --run-url "<运行链接>"

# 活跃度检查（scheduled-maintenance 用于 >45 天预警）
python engine/tools/automation_status.py activity --threshold 45 --porcelain   # 输出天数或 unknown
python engine/tools/automation_status.py activity --threshold 45               # 人读说明
```

状态写入根目录 `automation-status.json`（追加式，工作流提交）。

## 信息分层与决策交付（INFORMATION-LAYERING-SPEC v1.0 / DECISION-DELIVERY-SPEC v1.0）

```bash
# 信息密度与分层交付（新报告 [E] / 历史 [W]）
python engine/tools/info_density_check.py --gate-period 2026-12
# 事实卡片库（engine/fact_cards/）与报告引用
python engine/tools/fact_card_check.py --gate-period 2026-12
# 决策卡 / 行动协议 / 场景切片 / ex-ante
python engine/tools/decision_hub_check.py --gate-period 2026-12
# 盲区台账（P0 四类：就业 / 收入 / 空置 / 竣工）
python engine/tools/blind_spot_check.py
```

规范：`engine/templates/information-layering-spec.md`、`engine/templates/decision-delivery-spec.md`；
决策层业务线：`content/economy/insight`（类型 `decision-dashboard`）；
指标：`engine/tools/metrics-dictionary.json` 的 I-01–I-09。

## 量化研究模型链（方案 N1–N8）

纯标准库实现（`_quant.py` 提供 OLS/VAR/线性代数），零新增依赖；退出码 0/1/2。

```bash
# N1 周期时钟
python engine/tools/cycle_clock.py --snapshot data/processed/economy/dubai/apartment/quant_macro_snapshot.csv
# N2 信号合成（可带 cycle_clock 阶段交叉校验）
python engine/tools/signal_synth.py --input data/processed/economy/dubai/apartment/quant_signal_status.csv --phase 过渡带
# N3 政策乘数
python engine/tools/policy_multiplier.py --coverage
# N4 传导弹性（OLS + VAR）
python engine/tools/transmission.py --input data/processed/economy/dubai/apartment/quant_transmission_series_synthetic.csv --chain all
# N5 估值
python engine/tools/valuation.py --demo
# N6 规模测算
python engine/tools/market_sizing.py --demo
# N7 压力测试 / N8 蒙特卡洛
python engine/tools/stress_test.py --run
python engine/tools/monte_carlo.py --demo
# 阈值滚动校准
python engine/tools/threshold_calibration.py --input <csv> --column value --window 36
```

> 数据口径与状态见 `engine/report-audits/data-acquisition-checklist.md`；
> 盲区见 `engine/report-audits/blind-spot-ledger.md`；发布日历见 `engine/report-audits/release-calendar.md`。

## 工作区清理（CI 全流程自动触发）

`workspace_cleanup.py` 是**单一入口**的标准化工作区清理（缓存 / 临时 / 构建产物），
供本地钩子、提交网关与全部工作流各阶段复用，避免各处各写一套：

```bash
python engine/tools/workspace_cleanup.py            # 清理
python engine/tools/workspace_cleanup.py --mode dry-run   # 只报告
python engine/tools/workspace_cleanup.py --mode verify    # 有残留即 exit 1
python engine/tools/workspace_cleanup.py --deep           # 连同 .venv/venv/env
```

- **覆盖**：`__pycache__/`、`*.pyc/pyo/pyd`、`.pytest_cache/`、`.ruff_cache/`、`.mypy_cache/`、
  `.coverage`、`htmlcov/`、`*.egg-info/`、`.eggs/`、`build/`、`dist/`、
  `.automation-tmp/`、`.screenshots/`、`.trae-html-share-packages/`、`*.html.tmp`、`*.tmp`。
- **安全硬性**：只删**未被 git 跟踪**的路径（跟踪集合取自 `git ls-files`），
  被跟踪文件 / 目录一律跳过；默认跳过 `.git`。
- **确定性**：输出排序、无时间戳，重复执行结果一致（幂等）。
- **CI 接线**：`.github/actions/workspace-cleanup` 复合动作；五个工作流（ci / html-sync /
  content-update / scheduled-maintenance / audit）的每个作业均在**阶段开始前**与
  **阶段结束后（`if: always()`）**调用；`submit-pr` 在 `git add` 前清理；
  `scheduled-maintenance` 另执行 `pipeline_audit.py --rotate` 归档审计流水。
- **说明**：`webhook-alert` 无工作区检出、不产生构建产物，不接入清理。

## 分支命名与多会话网关（BRANCH-NAMING-SPEC v1.0）

规范全文见 [engine/docs/branch-naming-and-lifecycle.md](../docs/branch-naming-and-lifecycle.md)，
提交与合并协议见 [engine/docs/multi-session-git-protocol.md](../docs/multi-session-git-protocol.md)。

```bash
# 会话标识（建分支 / 排查用）
python engine/tools/repo_sync.py session

# 建任务分支（自动追加会话标识，从 origin/main 出发）
python engine/tools/repo_sync.py branch <slug>          # → task/<slug>-<session8>

# 存量梳理与整改
python engine/tools/repo_sync.py branches               # 分支 + 登记 + 合规标记
python engine/tools/repo_sync.py branch-audit           # 违规清单（有违规退出码 1）
python engine/tools/repo_sync.py branch-rename <旧> <新> [--remote]
python engine/tools/repo_sync.py branch-delete <branch> [--allow-unmerged]   # 删本地+远端；登记条目保留

# 钩子安装（每个克隆一次）
python engine/tools/repo_sync.py hook-install
python engine/tools/repo_sync.py hook-uninstall
```

- 受管分支仅 `task/*`，模板 `task/<slug>-<session8>`（8 位十六进制会话短码）；`main` 与 `ci/*` 豁免。
- 会话标识解析链：`TECH_CTX_SESSION_ID` → `CATPAW_CONVERSATION_ID` → `X_AI_SESSIONID`
  → `git config techctx.sessionId`；全部缺失即拒绝自动建分支。
- 拦截三重：`.githooks/pre-push`、`.githooks/pre-commit`、`repo_sync` 网关（钩子未装也拦）。
- 登记册 `engine/tools/branch_registry.json` 为分支 → 会话 / 任务的映射台账（工具读写，勿手改）。

## 常见场景速查

| 场景 | 命令 |
|---|---|
| 提交前本地自查 | `validate.py && lint_reports.py && compliance_check.py --check && build_hub.py --check` |
| CI 报「汇总页已过期」 | 运行 `build_hub.py` 重新生成后提交 |
| CI 报 lint 错误 | 按 `[E] 文件: 原因` 修复报告 HTML（多为标签不配对） |
| CI 报模板合规错误 | 按 `[E] 文件: [类型/周期] 不符合项` 对照类型模板补齐（结构缺失 / 必填字段 / 断头锚点） |
| 新报告开写前取骨架 | `compliance_check.py --scaffold <类型ID> [周期]` 输出骨架与自检要点 |
| 查历史报告合规匹配度 | `compliance_check.py --audit` 后看 `engine/report-audits/compliance-audit.md` |
| 新增业务线后首跑 | `ensure_region_topics.py` → 补 business-config.md → 首期基线报告 |
| 手动补跑月度任务清单 | `update_planner.py --project content/economy/dubai/apartment --period 2026-12` |
| 清理本地缓存/临时/构建残留 | `workspace_cleanup.py`（`--mode verify` 可先体检） |
| 新建任务分支 | `repo_sync.py branch <slug>`（自动追加会话标识并登记） |
| 分支名被钩子拦下 | `repo_sync.py branch-rename <旧> <新>`（见命名规范§六） |
| 查分支属于哪个会话 | `repo_sync.py branches` 或读 `branch_registry.json` |

## 注意事项

- 所有路径均为仓库内相对路径，业务线整体迁移（改目录名）不影响工具运行。
- `archive_reports.py` 会移动历史报告到 `reports/archives/`——基线是对比锚，
  保留策略已含 baseline 3 份；如需永久保留请自行调整 `_common` 之外的 KEEP 表。
