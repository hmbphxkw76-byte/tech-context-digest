# 优化解决方案与实施清单（OPTIMIZATION-SOLUTION-AND-IMPLEMENTATION-CHECKLIST v2.0）

> **状态**：现行方案（2026-11-19 产出；v2.0 = 整合既有方案 + 双视角闭环 + 验证对齐 + 信息理论补充维度 + 并发执行设计）
> **定位**：`tech-context-digest` 当前阶段的**收口文档**——把「目标对齐方案 v1.2」「信息质量方案 v1.2」「缺口对齐清单」「技术债务台账」「信息理论补充维度」整合为一份可验收、可勾选、可并发执行、可验证对齐的权威清单。
> **执行提示词**：见 [implementation-prompts-2026-11-19/](implementation-prompts-2026-11-19/)（每任务单元一份自包含 prompt，可直接投喂 Agent）。
> **判级口径**：沿用[信息分层规范](../templates/information-layering-spec.md)——`已核验`（命令/文件实测）、`部分核验`（抽样）、`推断`（机制分析）、`假设`（未验证）。
> **单一事实源纪律**：本文件只做**整合与指针**；指标定义归 `engine/tools/metrics-dictionary.json`，门禁规则归 `engine/docs/report-pipeline-system.md`，盲区口径归[决策交付规范](../templates/decision-delivery-spec.md)，本文件不复述其正文。
> **读者**：决策者读第 0 节；执行者读第 4–6 节。

---

## 0. 决策摘要

**三条结论**：

1. **[已核验] 骨架成熟、可复现**：统一门禁 **29 项单一入口**、`0 [E] / 10 [W]`（连续 3 次稳定）、单测 **670 通过 / 1 跳过**、静态检查 **只拦新增**（ruff 69 / mypy 26 baseline，新增 0）、`page_build_check` 0E0W、`compliance_check` 0E。**「规范 → 门禁 → CI」的骨架已经建立并自洽。**
2. **[已核验] 验证未收口，且「全绿」含宽限成分**：当前门禁全绿主要来自**滚动 gate-period 对历史报告的宽限**；真正的缺口集中在 **① p1-continue 批次未提交/未登记（18 份报告仅 10 份登记，8 份无审计链）② 5 项指标不达标 + 7 项 LLM 兜底 ③ 语义层大量为代理口径（A-03 / L-03 / IGI-05 真值核对未计分）**。
3. **[推断] 双视角闭环已可定义、尚未完成**：软件工程视角的「未完成 / 未验证对齐 / 语义与门禁」与信息理论视角的「信息质量 / 决策能力」**共用同一组可测指标**（IGI-08 = 0.9408），但**代理口径与覆盖权重**使该指数存在高估风险；闭环的最后一公里是**盲区消号 + 逐期序列 + 真值核对计分**。

**决策含义**：

- 不再新增规范条文，优先**收口验证对齐**（登记、门禁确定性、指纹漂移）与**语义真实性**（代理 → 真值）。
- 信息质量的最大杠杆是**盲区消号**（I-08 = 0）与**逐期序列**（C-05 = 0.6364），二者直接降低决策条件熵。
- 门禁必须保持「历史不追溯、新报告必阻断、且不随时间失效」的滚动口径。

**本期新增信息**：新增方案 1 份 ｜ 修正 2 条（IGI-02/IGI-03 由不达标转达标；I-04 由 0.40 转 1.00）｜ 无变化 4 条（门禁 0E、单测全绿、IGI-08 达标、盲区 0/15）｜ 假设核验进度 **6/8**（见 §7）。

**v2.0 补充（2026-11-19 信息理论视角评估）**：

- **[已核验] 结构层已成熟，缺口集中在「时间维度 + 度量真实性 + 消费端」**：实测 0 `[E]` / 7 `[W]`、38 项指标全实测、仅 I-08 不达标（盲区 0/15，阻塞 → 2027-03）、IGI-08 = 0.9945。
- **[已核验] 新增 10 个补充实施项（T-01…T-10，见 §4.6）**：来源核验证据字段 / 代理指标抽样校准 / finding→规则回写 / 研究内核历史收口 / 词库空库 / 消费端反馈 / 分类版本号 / 文档级信源分级 / 不确定性置信度 / 信息影响分级。
- **[已核验] 验证对齐协议升级（§5.1）**：双向追溯矩阵 + 「不引入新问题」回归清单（10 项）+ 抽样复核，替代单一自查表。
- **[已核验] 并发执行设计（§4.7）**：worktree 隔离 + `task/<slug>-<session8>` 分支 + 独立性分组 + 合并顺序 + 完成前证据索引。

---

## 1. 评估基线与判级

| 项 | 命令 | 实测（2026-11-19） | 判级 |
|---|---|---|---|
| 统一门禁 | `python engine/tools/optimization_gate.py --probe` | **exit 2；0 `[E]` / 7 `[W]`** | 已核验 |
| 单测 | `python -m unittest discover -s engine/tests -p "test_*.py"` | **684 通过 / 1 跳过 / 0 失败** | 已核验 |
| 静态检查 | `python engine/tools/static_check.py ruff\|mypy` | ruff **69/69**、mypy **26/26**，**新增 0** | 已核验 |
| 指标体检 | `python engine/tools/metric_registry.py audit --coverage` | 38 项；**实测 38 / LLM 0 / 不达标 1（I-08）** | 已核验 |
| 信息差指数 | 同上 | **IGI-08 = 0.9945**（≥0.80） | 已核验 |
| 语义 diff | `python engine/tools/semantic_diff.py scan` | 20 份报告；**有上期可比 5**；发现 0 项 | 已核验 |
| 审计登记 | `python engine/audit/scripts/audit_tool.py status` | 登记 45 条；失效 0；**正式报告 20/20** | 已核验 |
| 结构 / 页面 | `validate` / `validate_layout` / `page_build_check` / `compliance_check` / `lint_reports` | 全部通过（lint 20/20） | 已核验 |

**门禁 7 项 `[W]` 构成**：`ruff` / `mypy` baseline、`weekly-roundup` R7 / R6（历史）、`vocab_drift` VD-02（international / education 词库为空，历史）。

---

## 2. 软件工程专家视角

### 2.1 未完成与「未完成验证对齐」的证据

#### A. 未提交批次（p1-continue）

`engine/audit/records/tasks/p1-continue/` 四件套已建，`tasks.json` **4 项全为 `pending`**，产物全部未提交：

- 4 份新报告（未跟踪）：`content/economy/dubai/apartment/reports/2027-01_monthly.html`、`content/economy/trends/reports/2026-11-27_weekly.html`、`content/education/education-system/reports/2026-12_baseline_report.html`、`content/international/international-relations/reports/2026-11_baseline_report.html`。
- 新工具/数据：`engine/tools/indicator_sidecar.py`、`data/processed/economy/dubai/apartment/indicator_latest.json`、`engine/tools/probe-exemptions.json`；`engine/tools/metric_coverage.py` 增 `a03_truth_check` 与 A-05 接线。
- **未验证对齐**：未走 `repo_sync run --gate`；`publish_fingerprint` 报 1 份 CHANGED（education 基线 `22f0614f → 3491be80`）；4 份报告未登记。

#### B. 8 份报告无审计登记（已提交但未验证）

`audit_registry.json` 仅登记 **10 份报告**，磁盘存在 **18 份**。未登记 8 份：

| 报告 | 跟踪状态 |
|---|---|
| `content/economy/dubai/apartment/reports/2026-12_monthly.html` | **已提交** |
| `content/economy/trends/reports/2026-11-20_weekly.html` | **已提交** |
| `content/tech/competitive-intelligence/dubai/reports/2026-12_monthly.html` | **已提交** |
| `content/tech/weekly-roundup/reports/2026-11-20_weekly.html` | **已提交** |
| `content/economy/dubai/apartment/reports/2027-01_monthly.html` | 未提交 |
| `content/economy/trends/reports/2026-11-27_weekly.html` | 未提交 |
| `content/education/education-system/reports/2026-12_baseline_report.html` | 未提交 |
| `content/international/international-relations/reports/2026-11_baseline_report.html` | 未提交 |

> 另有 3 份登记但停在 `in-review 2/4`：`content/economy/insight/reports/2026-12_baseline_report.html`、`content/economy/trends/reports/2026-11-13_weekly.html`、`content/tech/weekly-roundup/reports/2026-11-13_weekly.html`——**L3 终审瓶颈**。

#### C. 度量层：5 项不达标 + 7 项未接线

| 指标 | 实测 | 阈值 | 缺口 | 性质 |
|---|---|---|---|---|
| C-05 节拍达成率 | 0.6364 | =1.00 | -0.36 | 需报告周期滚动 |
| A-05 链接可达率 | 0.9898 | =1.00 | -0.0102 | 2 条死链（分母 196 可判定） |
| L-03 阈值三处一致率 | 0.9412 | =1.00 | -0.059 | **代理口径**（表达式重合） |
| I-05 行动协议合规率 | 0.9444 | ≥1.00 | -0.056 | international 基线行动项缺要素 |
| I-08 盲区消号率 | **0.0000** | ≥0.60 | -0.60 | 0/15 消号，P0 四类阻塞 |

**LLM 兜底（从未计算，仅校验阈值可解析）**：A-02、A-04、L-01、L-02、L-04、L-05、R-05。

#### D. 语义层实施现状（重点）

已接线且 0 警告：`semantic_diff`、`model_contract_check`（MC-01..05）、`consistency_check`（LC/VG）、`prompt_consistency_check`（PC-01..03）、`info_gap_metrics`（IGI-01..08）。

| 项 | 现状 | 风险 |
|---|---|---|
| **A-03 数值一致率** | 实测 1.0000，仅为「同编号显式数值对冲突代理」；`a03_truth_check` 已能读 sidecar 比对，**明确不计分** | 代理 1.0 ≠ 与登记册真值一致；自动判分未实施 |
| **L-03 阈值一致率** | 0.9412，为「报告表达式 ∩ business-config 表达式」重合代理 | 非「config / 登记册 / 报告」三处语义一致 |
| **IGI-05 关键断言核验率** | 0.9736（初测 0.4726） | 提升主要来自**口径校准**（块类型扩展至 `div.kpi`/`stat-strip`，`td` 因误报 164 处剔除）；需区分真实改进与口径放宽 |
| **S6 / S7 / S8**（语义弱专项） | S6→L-03 代理、S7→R-03 代理（0.0297）、S8→改接 I-01（1.0） | S8 口径已修正；S6/S7 仍为代理 |

#### E. 质量门禁实施现状（重点）

**已落地**：29 项单一入口；滚动 gate-period（`auto` = 当前月 + 1；`C-05` / `A-05` 均改锚点，不再取墙钟）；复用一致性由 `test_process_gates` 锁定；CI 四工作流统一调用；`ruff` / `mypy` 入 baseline 只拦新增；`publish_fingerprint` CRLF 归一；新增 `monitoring_render` / `consistency` / `naming` / `prompt_consistency` / `model_contract` 五项门禁。

**薄弱 / 未完成**：

1. **新报告强制力受限**：gate-period `auto` = 2026-12，故 2026-11 及更早报告即使缺内核项 / 行动项也判 `[W]` 放行；仅当月报告为 `[E]`。
2. **门禁确定性未定位**（gap-checklist E1）：与 `unittest` **并行**运行时曾出现 1 次 `1 [E] / exit 1`；干净重跑 3 次均 `0 [E] / exit 2`。推断为 records 写入竞态或网络抖动，**未复现定位**。
3. **指纹漂移未收口**：`content/education/education-system/reports/2026-12_baseline_report.html` 需 `publish_fingerprint.py --emit`。
4. **历史警告积压**：`monitoring_render` 86 `[W]`、`source_check` 76 `[W]`（含 3 处死链待人工复核）。
5. **词库空库**：political / society `terms.md` 无词条（VD-02 `[W]`）。

#### F. 显式延后 / 登记管理（非待办，需知情）

- **P-06** 门禁清单 / 类型注册五点手工同步（`optimization_gate.CHECKS` / `template-registry.md` / `compliance-rules.json` / `_common.TEMPLATE_TYPE_DIRS` / `build_hub.TYPE_SHORT`）——显式延后。
- **P-09** 多会话并发写同一工作树——仅 git 层有共享检出锁，**文件编辑层无锁**。
- **B 类**审计文档为登记管理件；**E 类** R6 宽限期（2027-01 转强制）；**F 类** ruff 69 / mypy 26 baseline。

### 2.2 实施计划情况

| 计划 | 规模 | 状态 | 收口判断 |
|---|---|---|---|
| 目标对齐 P0 | 6 项 | **已闭环** | IGI 接线、ID-02/04 语义化、决策卡逐卡、滚动 gate-period、hub 基期、词库门禁 |
| 目标对齐 P1 | 15 项 | **大部分闭环** | 残留：P1-8 死链（A-05 0.9898）、P1-9 四主题（political 与 society 无报告）、P1-6 字段需复核 |
| 目标对齐 P2 | 8 项 | **已闭环** | 死代码处置、文档漂移、PCE 指针、注册表同步、术语策略、审计报表、结构加固 |
| 信息质量 P0-1（IGI-05） | 工具侧 | **已闭环**（0.9736 达标） | 内容侧补标持续 |
| 信息质量 P0-2（盲区） | 内容/数据 | **阻塞**（→2027-03） | 0/15，P0 四类取数未获官方一手 |
| 信息质量 P0-3（逐期序列） | 内容 | **进行中** | 已产 4 份第二期；semantic_diff 5 可比 |
| 信息质量 P1-4（摘要密度） | 内容 | **部分** | 1 项历史 `[W]`；ID-02 仍 `WARN_ONLY` |
| 信息质量 P1-5（工程噪声） | 引擎 | **部分** | baseline 已建；7 项 LLM 未接线 |
| 第二期最小集 | 3 线 | **工具就绪、内容进行中** | 定义 + 派发就绪 |

---

## 3. 信息理论专家视角

### 3.1 框架

把体系视为一个信息信道：

```
信源(机构/官方) → 采集·登记(source_registry) → 过滤·分级(tier1-4)
  → 编码(报告/决策卡/FC) → 信道(链接可达性/时效) → 解码(读者) → 决策
```

信息质量 = **信源可靠性 × 覆盖 × 时效 × 可核验性 × 一致性 × 低冗余**；决策能力取决于**可观测变量的完备性**与**反馈闭环（回测 / 校准）**。

### 3.2 信息质量水平评估

| 维度 | 指标（实测） | 判断 |
|---|---|---|
| **覆盖** | IGI-01 = 1.0000（6/6 主题就绪）；IGI-02 = 0.8182（9/11 业务线）；**有报告的主题仅 4/6** | 结构覆盖高、**实质内容覆盖低** |
| **时效** | IGI-03 = 0.8182；C-05 = 0.6364 | 读数时点集中 2026-11，逐期序列刚起步（5 可比） |
| **可核验 / 溯源** | IGI-04 = 0.9868；IGI-05 = 0.9736；A-01 = 0.9736 | **强项**：登记与断言指针覆盖高 |
| **一致性** | A-03 = 1.0000（代理）；L-03 = 0.9412；R-03 = 0.0297 | 代理一致率高，但**真值一致性未验证**；跨主题冗余低（好） |
| **信道可靠性** | A-05 = 0.9898（2 死链 / 196 可判定） | 高，但 135 条 `unreachable` 为环境性不可判（**信道噪声未消除**） |
| **决策变量完备性** | I-08 = **0.0000**；盲区 15 项（P0 四类） | **最大短板**：关键变量未观测 → 条件熵高 |
| **综合** | **IGI-08 = 0.9408** | 数值高，含代理口径与权重折算，**需打折看待** |

**判断（推断）**：信息质量呈「**结构层高、内容层低**」的哑铃形——溯源与合规接近成熟（≈0.97），但覆盖、时效、关键变量完备性拉低有效信息量。

### 3.3 基于信息的决策能力评估

| 能力 | 证据 | 判断 |
|---|---|---|
| 决策载体完备 | IGI-06 = 1.0；IGI-07 = 1.0 | **结构完备** |
| 行动可执行 | I-05 = 0.9444 | 轻微缺口 |
| 结论可靠性 | I-07 = 1.0；DC-08 已接线 | 结构合规，**缺回测校准** |
| 经验闭环 | 无：semantic_diff 5 可比、0 发现；阈值回测需 2027-06 | **决策未经反馈校准** |
| 关键变量可观测 | I-08 = 0；P0 四类阻塞 | **可负担性 / 供给判断不可判** |

**判断（推断）**：决策支持系统属「**高结构、低经验校准**」——仪表盘完整，但传感器（盲区 / 序列 / 回测）尚未校准；可类比为「读数精确但量程未标定」。

### 3.4 关键风险

1. **度量伪影（Goodhart）**：IGI-05 由 0.4726 → 0.9736 主要来自口径校准；A-03 = 1.0 为代理；L-03 为表达式重合。**代理与真实语义之间存在互信息损失**。
2. **形式化达标**：空指针可刷高 IGI-05、删字可降摘要密度、代理可「假消号」盲区；当前防刷机制尚未覆盖全量。
3. **信道不确定性**：135 条 `unreachable` 与 3 条待复核死链说明信源可达性判定本身有噪声；A-05 只能视为「可判定子集上的高可达率」。

---

## 4. 完整实施清单

> 状态取值：`已闭环` / `进行中` / `部分` / `未开始` / `阻塞` / `显式延后`。
> 验收标准均可映射到命令或文件；「门禁映射」指向统一门禁项或规范条。

### 4.1 目标对齐 P0（6 项 · 已闭环）

| ID | 动作 | 涉及文件 | 验收标准 | 门禁映射 | 状态 |
|---|---|---|---|---|---|
| P0-1 | IGI 指标组接线实测 | `metrics-dictionary.json` / `info_gap_metrics.py` / `metric_registry.py` | 8 项定义齐全；`audit` 输出 FALLBACK = 0（有数据时） | `metric_audit` | 已闭环 |
| P0-2 | ID-02 / ID-04 语义化 + 剥离注释 | `info_density_check.py` | 「字符>900 或 要点>12」；摘要节检出推断/假设 | `info_density` | 已闭环 |
| P0-3 | 决策卡逐卡 / 逐条行动项校验 | `decision_hub_check.py` | 剥离注释后逐卡五字段、逐条五要素 + 三档 | `decision_hub` | 已闭环 |
| P0-4 | 滚动 gate-period（`auto`） | `optimization_gate.py` / `gate_period.py` / 各门禁 | `auto` = 当前月 + 1；默认 auto；单测锁定 | 全部内容门禁 | 已闭环 |
| P0-5 | hub 环比基期只标真实上期 | `build_hub.py` / `index.html` / `reader.html` | 无上期时标「首期」；`hub --check` 通过 | `hub` | 已闭环 |
| P0-6 | 词库同步修复 + 漂移门禁 | `vocab_tool.py` / `vocab_drift_check.py` | `auto_trigger=false` 不触发；`vocab_drift` 接入 | 统一门禁 | 已闭环 |

### 4.2 目标对齐 P1（15 项）

| ID | 动作 | 验收标准 | 门禁映射 | 状态 |
|---|---|---|---|---|
| P1-1 | 摘要越级修正 | 摘要节零推断/假设；ID-04 全绿 | `info_density` ID-04 | 已闭环（历史） |
| P1-2 | 证据强度一致性 + DC-08 | 决策卡强度由支撑卡 `level` 唯一推导 | `decision_hub` DC-08 | 已闭环 |
| P1-3 | 「假设乘积」标注治理 | 自算测算标「假设乘积 + 区间」 | `info_density` ID-04 | 已闭环 |
| P1-4 | 行动项阈值数值化 | 阈值为数值/区间/日期 | `decision_hub` DC-02 | 已闭环 |
| P1-5 | trends 决策卡补全 | 五字段齐全 | `decision_hub` DC-01 | 已闭环 |
| P1-6 | 来源登记字段扩展 | `unverifiable` + `updated` | `source_check` R8 | 已闭环（需复核存量） |
| P1-7 | R4 关键数字逐点指针 | 块级判定；误报 < 5% | `source_check` R4 | 已闭环 |
| P1-8 | 死链真实修复 | `--probe` 死链 `[E]` 归零 | `source_check` R6 | **部分**（A-05 0.9898；3 条待复核） |
| P1-9 | 四主题接入就绪化 | 四主题可发现；IGI-01 ≥ 0.5 | `vocab_drift` / IGI-01 | **部分**（political 与 society 无报告） |
| P1-10 | 提示词单一事实源 + 一致性门禁 | 泛用版/实例一致或指针；去复述 | `prompt_consistency` | 已闭环 |
| P1-11 | 词库规范形统一 + 缺口补录 | 提示词规范形与词库一致 | `vocab_drift` | **部分**（political 与 society 空库） |
| P1-12 | N0–N8 接线 | CI 调 `pipeline_runner`；G8 `checks` 非空 | `pipeline_audit` | **部分**（G8 = `["perf_monitor"]`） |
| P1-13 | 模型契约门禁 | DC-07 从单测提升为 gate | `model_contract` | 已闭环 |
| P1-14 | 数据层补薄 + raw 落仓 | 两线有台账 + 量化数据；官方快照落 raw | IGI-05 | 已闭环 |
| P1-15 | hub 卡片信息区分度 | 同周期多报告可区分 | `hub` | 已闭环 |

### 4.3 目标对齐 P2（8 项 · 已闭环）

| ID | 动作 | 状态 |
|---|---|---|
| P2-1 | 死代码与规范外结构处置 | 已闭环（保留 2 / 迁移 1 / 修正 3，未删除任何文件） |
| P2-2 | 文档漂移修正 | 已闭环 |
| P2-3 | 提示词引用 AGENTS / PCE | 已闭环 |
| P2-4 | 类型注册表同步 | 已闭环 |
| P2-5 | 主题 README 治理 | 已闭环 |
| P2-6 | 审计报表增强（IGI 趋势） | 已闭环 |
| P2-7 | 报告结构加固 | 已闭环（核实已满足） |
| P2-8 | 术语策略文档 | 已闭环 |

### 4.4 信息质量方案（P0-1 … P1-5）

| ID | 动作 | 验收标准 | 门禁映射 | 状态 |
|---|---|---|---|---|
| P0-1 | IGI-05 关键断言核验率 | ≥0.90（3 个月滚动）；抽样一致率 ≥95% | `metric_audit` / `source_check` R4 | 工具侧已闭环（0.9736）；内容侧持续 |
| P0-2 | P0 四类盲区消号 | 四类 `closed`；I-08 ≥0.60 | `blind_spot` / `metric_audit` | **阻塞**（→2027-03） |
| P0-3 | 建立逐期序列（最小集） | ≥3 线有第二期；可比 ≥1；IGI-03 ≥0.80 | `semantic_diff` / `hub` | **进行中** |
| P1-4 | 摘要密度治理 | ID-02 警告清零；≤900 字 / ≤12 要点 | `info_density` ID-02 | **部分**（仍 `WARN_ONLY`） |
| P1-5 | 工程噪声与 FALLBACK 收口 | measured ≥35；ruff/mypy 0 或 baseline；无沉默项 | `metric_audit` / `ruff` / `mypy` | **部分**（7 LLM 未接线） |

### 4.5 本次新增识别项（N 类）

| ID | 动作 | 涉及文件 | 验收标准 | 状态 |
|---|---|---|---|---|
| N-1 | p1-continue 批次提交 + 门禁 + 登记 | 4 报告 + `indicator_sidecar.py` + `probe-exemptions.json` + `metric_coverage.py` | `repo_sync run --gate` 通过；登记入册 | **已闭环**（PR #88 `7290e98`；工件 `tasks.json` done） |
| N-2 | 8 份报告补审计登记 | `audit_registry.json` | 登记报告数 = 18 | **已闭环**（20/20） |
| N-3 | in-review 补 L3 终审 | 13 份（含 insight / trends / weekly-roundup + political / society 首报） | 4/4 审查链 | **已闭环**（13 份补 `second`；`final` 由 CI `run --strict` 收口） |
| N-4 | A-05 死链收口 | 3 条待复核 URL | 死链 `[E]` 归零（2027-01 强制） | **已闭环**（探测 dead=0） |
| N-5 | A-03 真值核对转计分 | `indicator-truth-registry.json` + `metric_coverage` | 自动判分纳入 A-03 | **已闭环**（A-03 = 1.0000） |
| N-6 | 7 项 LLM 指标接线 / 人工判定 | `metric_coverage.py` / 字典 | measured ≥35 | **已闭环**（measured 38/38） |
| N-7 | 门禁确定性 E1 排查 | `optimization_gate` / records 写入 | 单跑 vs 并行各 3 次一致 | **已定位**（无 records 竞态；差异为 hub 重生成时点） |
| N-8 | `publish_fingerprint --emit` | `publish_fingerprints.json` | 指纹漂移 0 | **已闭环**（20/20 一致） |

### 4.6 信息理论补充实施项（v2.0 新增）

> 来源：2026-11-19 信息理论视角评估中「信息质量改进方案 v1.2 未覆盖」的维度。判级同第二节。
> **执行性质**：`工具侧`（可立即执行）/ `内容侧`（需研究或撰写）/ `阻塞`（外部依赖）。
> 既有 P0/P1 项（盲区消号、逐期序列、摘要密度、工程噪声）见 §4.4，本表不重复。

| ID | 动作 | 涉及文件 | 验收标准 | 门禁映射 | 优先级 | 执行性质 |
|---|---|---|---|---|---|---|
| **T-01** | 来源核验证据字段 + 内容指纹 | `source_check.py`（R8 扩展）、各线 `source_registry.json`、`metrics-dictionary.json` | 每条来源含 `evidence`（存档哈希 / 快照日 / 核验方式）；关键来源内容指纹变更可探测；单测覆盖 | `source_check` R8 | P1 | 工具侧 |
| **T-02** | 代理指标抽样校准 | 在 `engine/tools/` 下新增 `proxy_calibration.py`；`metrics-dictionary.json` | 每季度 ≥200 断言人工核验；输出代理 precision / recall 与口径版本；「代理达标 ≠ 真值达标」说明入库 | `metric_audit` | P0 | 工具侧 |
| **T-03** | finding→规则回写台账 | `engine/audit/`（新 schema + 工具）、`review-workflow.md` | 每个 L3 / 质量 finding 映射预防规则；规则命中次数可跟踪；重复 finding 自动提示 | `audit_tool` | P1 | 工具/流程 |
| **T-04** | 研究内核历史警告收口 | 10 份历史周报 | 周期定位 / 传导量化 / 政策入模 / 盲区列示四项补齐；`research_kernel` 0 `[W]` | `research_kernel` | P1 | 内容侧 |
| **T-05** | 词库空库补录 | `engine/vocabulary/data/{education,international}/terms.md` | VD-02 清零；词条 + 别名合规 | `vocab_drift` | P2 | 内容侧 |
| **T-06** | 消费端反馈机制 | `build_hub.py` / 报告模板、设计文档 | 报告页脚反馈入口；读者回访流程；消费侧指标纳入 IGI | `hub` | P2 | 设计 + 工具 |
| **T-07** | 分类版本号 + 互斥性校验 | `engine/tools/validate_layout.py` / `layout.json` | 分类体系带版本号；跨主题归属唯一性检查；变更影响评估留痕 | `validate_layout` | P2 | 工具侧 |
| **T-08** | 文档级 / 陈述级信源分级 | `source_check.py`、各线 `source_registry.json` | `document_tier` / `statement_type` 字段与校验；机构 tier 仅作先验 | `source_check` | P1 | 工具侧 |
| **T-09** | 不确定性置信度字段 | `metrics-dictionary.json`、`decision_hub_check.py`、报告模板 | 关键推断带区间 / 置信度；决策卡含置信度；四级标签配操作性判定规则 | `decision_hub` | P1 | 工具 + 内容 |
| **T-10** | 信息影响分级与披露 | `information-layering-spec.md` / 报告模板 | 高影响主题（就业 / 签证 / 投资）强制置信区间与披露强度 | `info_density` | P2 | 文档 + 内容 |

### 4.7 并发执行设计（多 Agent / 多会话）

**隔离方式**：每个任务单元在独立 git worktree 中执行，分支 `task/<slug>-<session8>`（`session8` = 会话标识 8 位）；禁止直推 `main`；经 `python engine/tools/repo_sync.py run --gate` 提交，CI 走 PR。

**独立性分组**（同组文件交集最小，可并行）：

| 组 | 任务单元 | 文件交集 | 可并行 |
|---|---|---|---|
| G1 | T-01 → T-08 | 均涉 `source_check.py` + registry schema | ❌ 串行（同一工具，T-08 排队） |
| G2 | T-02 / T-07 | `metrics-dictionary.json`（只加备注）/ `validate_layout.py` | ✅ |
| G3 | T-03 / T-06 | `engine/audit/` / `build_hub.py` | ✅ |
| G4 | T-04 / T-05 / T-09 / T-10 | 内容 / 词库 / 模板（不同业务线） | ✅ |

**合并顺序**：G1 → G2 → G3 → G4。每组合并前跑 `--only` 相关门禁 + 单测；合并后跑全量门禁。

**冲突规避**：
- 同一工具文件（`source_check.py`）只允许一个任务单元修改，另一个排队；
- `metrics-dictionary.json` 只允许「新增字段 / 备注」，不得改既有阈值；
- 内容侧任务按业务线目录隔离，禁止跨线改文件。

**完成前证据索引**（每个任务单元必须产出）：
1. 变更文件清单 + 关键 diff 摘要；
2. 验证命令与输出（单测 / 门禁 `--only`）；
3. 对齐声明：本任务对应方案条目 ID + 验收标准逐条映射；
4. 回归声明：未引入新问题的证据（见 §5.1）。

---

## 5. 验证对齐清单（确保对齐优化方案的验证清单）

> 事实源：[目标对齐优化方案 · 剩余缺口对齐清单](goal-alignment-gap-checklist-2026-11-19.md) §八「对齐验收自查表」。本节按 2026-11-19 复测刷新。

| # | 验证项 | 目标 | 当前实测 | 判定 | 证据 / 动作 |
|---|---|---|---|---|---|
| V-1 | L-03 / R-03 / A-01 / A-03 均为 `measured` | 非 FALLBACK | 四项均 `measured` | **已达成** | audit 输出各实测值 |
| V-2 | `tech-debt-ledger.md` 含 A-01/A-03/L-03 登记节 | 有登记 | §十三「度量接线登记」 | **已达成** | `tech-debt-ledger.md` §十三 |
| V-3 | 方案 §4.9 S8 口径修正（不再指向 R-02） | 口径一致 | 已改接 I-01 | **已达成** | 方案 §4.9 S8 行 |
| V-4 | R-04 公式 / 阈值 / 实现一致 | 无误报 | 实测 0.0000 = 0.0000 | **已达成** | audit `[OK] R-04` |
| V-5 | C-05 不依赖墙钟 | 确定性 | 锚点改 `GATE_PERIOD` / `resolve_gate_period` | **已达成** | `metric_coverage.py::c05_cadence` |
| V-6 | IGI-05 ≥0.90 | ≥0.90 | **0.9768** | **已达成** | `metric_registry audit` |
| V-7 | I-04 ≥1.00 | ≥1.00 | **1.0000** | **已达成** | 口径对齐 + apartment 卡片库 |
| V-8 | IGI-02 / IGI-03 ≥0.80 | ≥0.80 | **1.0000 / 1.0000** | **已达成** | 新增 political / society 首报 + 周期滚动 |
| V-9 | I-08 ≥0.60 | ≥0.60 | **0.0000** | **未达成** | 盲区 0/15，取数阻塞 → 2027-03 |
| V-10 | C-05 = 1.00 | =1.00 | **1.0000** | **已达成** | 周报周期解析修正 + 周期滚动 |
| V-11 | 门禁连续 3 次结果一致 | 可重放 | 单跑 3 次 0 `[E]`；并行 3 次 0 `[E]`（无 records 竞态） | **已达成** | N-7 排查 |
| V-12 | unittest 全绿且数量不减 | 全绿 | **684 通过 / 1 跳过** | **已达成** | `unittest discover` |
| V-13 | 报告登记率 = 100% | 20/20 | **20/20** | **已达成** | N-2 |
| V-14 | 指标不达标项 | 0 | **1（I-08）** | **部分** | I-08 阻塞；其余全部达标 |
| V-15 | 语义层真值核对计分 | A-03 计分 | A-03 = **1.0000**（真值 1/1 + 代理） | **已达成** | N-5 |
| V-16 | 指纹漂移 | 0 | **0** | **已达成** | N-8 `--emit` |

**验证对齐结论**：**15 项已达成 / 1 项未达成（V-9 I-08，阻塞 → 2027-03）**；V-14 因 I-08 记「部分」。原未达成项（V-9 除外）均由 N 类动作收口。

### 5.1 验证对齐协议（双向追溯 + 不引入新问题）

**A. 双向追溯矩阵**（方案条目 ↔ 实施工件 ↔ 验收证据）：

| 方案条目 | 实施工件（文件 / 提交） | 验收证据（命令 / 值） | 对齐判定 |
|---|---|---|---|
| T-01 | `source_check.py` / registry | `optimization_gate --only source_check`；抽样 3 条来源含 `evidence` | 待执行 |
| T-02 | `proxy_calibration.py` / 字典 | 单测；试跑输出 precision / recall | 待执行 |
| T-03 | `engine/audit/` schema + 工具 | 单测；finding 映射率 100% | 待执行 |
| T-04 | 10 份历史周报 | `optimization_gate --only research_kernel` 0 `[W]` | 待执行 |
| T-05 | `terms.md` × 2 | `optimization_gate --only vocab_drift` 0 `[W]` | 待执行 |
| T-06 | `build_hub.py` / 模板 | `hub --check`；反馈入口存在 | 待执行 |
| T-07 | `validate_layout.py` | 单测；分类版本号存在 | 待执行 |
| T-08 | `source_check.py` / registry | 单测；`document_tier` 校验 | 待执行 |
| T-09 | 字典 / `decision_hub_check.py` | 单测；置信度字段 | 待执行 |
| T-10 | 规范 / 模板 | 规范条款 + 模板字段 | 待执行 |

**B. 对齐判定规则**：
- **全覆盖**：方案每条都有对应工件与证据；
- **无越界**：工件不修改方案外文件（`git diff --name-only` 核对）；
- **验收达标**：证据值满足方案验收标准；
- **判级**：`已核验`（命令实测）/ `部分核验`（抽样）。

**C. 「不引入新问题」回归清单**（任一项失败即回滚）：

| # | 回归项 | 命令 | 通过判据 |
|---|---|---|---|
| R-REG-1 | 统一门禁 | `python engine/tools/optimization_gate.py` | 0 `[E]`；新增 `[W]` 已登记 |
| R-REG-2 | 单元测试 | `python -m unittest discover -s engine/tests -p "test_*.py"` | 全绿；数量 ≥ 684 |
| R-REG-3 | 指标体检 | `python engine/tools/metric_registry.py audit --coverage` | measured = 38；不达标 ≤ 1（仅 I-08） |
| R-REG-4 | 审计登记 | `python engine/audit/scripts/audit_tool.py status` | 登记报告率 100% |
| R-REG-5 | 链接 / 死链 | `python engine/tools/check_links.py`；`source_check --probe` | 死链 0 |
| R-REG-6 | 发布指纹 | `python engine/tools/publish_fingerprint.py --check` | 漂移 0 |
| R-REG-7 | 结构 / 页面 | `validate.py` / `validate_layout.py` / `page_build_check.py` | 0E |
| R-REG-8 | 信息差指数 | `metric_registry.py audit` | IGI-08 ≥ 0.9945（不退化） |
| R-REG-9 | 文档一致性 | `prompt_consistency` / `naming` / `model_contract` | 无新增警告 |
| R-REG-10 | 可回滚 | 分支 / 补丁 | 每个任务单元可独立回滚 |

**D. 抽样复核**：每个任务单元抽 ≥3 个样本，由非执行方（另一 Agent / 人工）按验收标准复核，一致率 ≥ 95%。

**E. 验证报告**：执行后产出 `verification-report-<date>.md`，含追溯矩阵填充、回归结果、抽样结论、遗留项。

---

## 6. 闭环机制（DoD / 门禁 / 审计 / 防刷）

| 层级 | 机制 | 现状 |
|---|---|---|
| **完成定义 DoD** | 任务四件套（`plan.json` / `tasks.json` / `risks.json` / `task-start.md`）为 `repo_sync run --gate` 强制输入 | 已实施（`task/*` 分支 + `--allow-no-plan` 应急） |
| **门禁** | 单一入口 `optimization_gate.py`（29 项）；两级 gate-period（内容 / 来源）；滚动 `auto` 不失效 | 已实施；确定性已排查（N-7：无 records 竞态） |
| **审计** | 四环节（draft → initial → second → final）+ L3 SLA + evidence index | 已实施；13 份补 `second`，`final` 由 CI 收口 |
| **度量** | `metric_registry audit --coverage`；LLM 项显式标注不伪造 | 已实施；38/38 实测，0 项 LLM 兜底 |
| **防刷** | 指针可解析；自链接豁免仅限 R1/R6；盲区消号须留证据；代理口径写备注 | 已实施（A-03 真值核对已计分；代理口径均写备注） |
| **归档** | `report-audits` 保留最近 12 个月 + `archive_reports --audit-docs` | 已实施 |

**闭环判定**：**骨架与内容闭环均已达成**（DoD / 门禁 / 审计 / 度量 / 归档机制齐备；V-1…V-8、V-10…V-13、V-15、V-16 达成）；**唯一未闭环项为 V-9（I-08 盲区消号率）**，属取数阻塞，责任周期 2027-03，已登记 [盲区台账](blind-spot-ledger.md)。

---

## 7. 风险与反向证据

| 风险 | 说明 | 缓解 |
|---|---|---|
| R-1 | 门禁加强立即暴露存量违规 | 滚动 gate-period；存量 `[W]`，新报告 `[E]` |
| R-2 | IGI / 度量诱发「刷指标」 | 覆盖率类要求结构齐全 + 有产出；IGI-08 含核验率与摘要合规率 |
| R-3 | 逐卡 / 逐条门禁误报 | 先覆盖 canonical 结构；单测校准；误报高则降级 `[W]` |
| R-4 | 代理口径被误读为语义 | 字典 `detected_by` + 备注；A-03 真值核对转计分（N-5） |
| R-5 | 度量接线改变审计语义 | 首次以 `[W]` 发布，下一周期转 `[E]` |
| **反向证据** | 「525 单测 + 29 门禁已足够」 | 反驳：全绿下仍实测出盲区 0/15、8 报告未登记、A-03 代理 1.0——**门禁绿不等于目标达**；度量层正是把「目标达」变成可证明的唯一路径 |

**假设核验进度**：8 项关键假设中 **6 项已核验**（骨架成熟、验证未收口、门禁全绿含宽限、代理口径存在、盲区阻塞、逐期序列工具就绪）；**2 项待验证**（IGI-08 提升幅度、门禁确定性竞态根因）。

---

## 8. 与既有规范的关系（单一事实源）

| 本文件内容 | 事实源 | 不得复述于 |
|---|---|---|
| 指标定义 / 阈值 | `engine/tools/metrics-dictionary.json` | 本文件（只指针） |
| 门禁规则 / 清单 | `engine/docs/report-pipeline-system.md` | 本文件（只指针） |
| 盲区消号条件 | [决策交付规范](../templates/decision-delivery-spec.md) 第六节 | 本文件（只指针） |
| 信息分层 / 决策交付 | [信息分层规范](../templates/information-layering-spec.md) / [决策交付规范](../templates/decision-delivery-spec.md) | 本文件（只指针） |
| 上游方案 | [目标对齐方案](goal-alignment-optimization-plan-2026-11-18.md) / [信息质量方案](information-quality-improvement-plan-2026-11-19.md) / [缺口清单](goal-alignment-gap-checklist-2026-11-19.md) / [技术债务台账](tech-debt-ledger.md) | 本文件为整合层，不替代上游 |

---

## 9. 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-19 | 初始版本 | 整合目标对齐 / 信息质量 / 缺口 / 台账；双视角（软件工程 + 信息理论）闭环；16 项验证对齐清单；N 类新增项；闭环机制 |
| v1.1 | 2026-11-19 | 验证对齐收口 | N-1…N-8 全部闭环；§1 基线刷新（0E/7W、684 单测、不达标 1、IGI-08 0.9945、登记 20/20）；§4.5 / §5 / §6 状态更新；唯一未闭环 V-9（I-08 阻塞 2027-03）。合并 PR #93（`47ed028`）；CI 审计回填 PR #94（`1b80992`，20/20 `audited` 4/4） |
| v2.0 | 2026-11-19 | 信息理论补充 + 并发执行 | 实测基线刷新；新增 §4.6（T-01…T-10）/ §4.7（并发设计）/ §5.1（验证对齐协议）；执行提示词目录 `implementation-prompts-2026-11-19/` |
