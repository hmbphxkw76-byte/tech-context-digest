# 信息质量改进实施方案（INFORMATION-QUALITY-IMPROVEMENT-PLAN v1.2）

> **状态**：现行方案 v1.2（2026-11-19 评估产出；同日追加「就绪与阻塞说明」与批 A 工具收口，并登记 S2 取数阻塞）
> **依据**：[信息分层规范](../templates/information-layering-spec.md)、[决策交付规范](../templates/decision-delivery-spec.md)、[质量 rubric](../quality/rubric.md)、[目标对齐方案 v1.2](goal-alignment-optimization-plan-2026-11-18.md)
> **方法**：以 2026-11-19 实测为基线（`optimization_gate --probe` 0E / 8W、`info_gap_metrics.py`、`info_density_check.py`、`research_kernel_check.py`、盲区台账），逐项给出「动作 / 涉及文件 / 验收标准 / 门禁映射 / 优先级」。
> **读者**：决策者读第 0 节；执行者读第 2、3 节。
> **收口整合**：[优化解决方案与实施清单](optimization-solution-and-implementation-checklist-2026-11-19.md)（2026-11-19；双视角闭环 + 16 项验证对齐清单）。
> **等级标注**：本方案自身按信息分层规范第二节标注——`已核验`（代码 / 工具 / 文件实测）、`部分核验`（抽样推断）、`推断`（机制分析）、`假设`（待验证）。

---

## 0. 决策摘要

**本期判定（三条结论）**：

1. **[已核验] 五项问题均有明确根因与现成工具抓手，P0 三项可在 2026-12 前完成**：IGI-05 已有 R4 块级指针与 `_assertion_stats` 测量（`engine/tools/info_gap_metrics.py:170-204`）；盲区四类已有消号条件与发布日历对应行；逐期序列已有 `update_planner` / `semantic_diff` / `threshold_calibration` 工具链，缺的只是「第二期内容」。
2. **[已核验] 最大风险不是技术，而是「形式化达标」**：IGI-05 可用空指针刷高、摘要可靠删字降密度、盲区可靠代理替代「假消号」——方案为每项配了防刷规则与抽样复核。
3. **[推断] 完成 P0 三项后，IGI-08 预计由 0.8371 升至 ≥0.90**（IGI-05 权重 0.10、IGI-03 权重 0.15，两者达标约贡献 +0.09）。

**决策含义**：

- 顺序上**先做 P0-1（IGI-05）与 P0-2（盲区消号）**：前者是「不确定性消除」的核心熵减，后者直接决定决策者能否做可负担性与供给判断，且两者可并行（一个在报告层、一个在数据采集层）。
- P0-3（逐期序列）是**时间维度的唯一路径**，但依赖内容产出，建议以「第二期最小集」起步，不追求全业务线铺开。
- P1 两项（摘要密度、工程噪声）不阻断目标，但建议在下次审计前收口，避免「门禁全绿」的公信力被稀释。

**本期新增信息**：新增方案 1 份 ｜ 修正既有认知 0 条 ｜ 无变化 3 条（IGI-08 0.8371、门禁 0E、盲区 15 项 open）｜ 假设核验进度 2/4（见 §4）。

---

## 1. 问题与证据基线

| # | 问题 | 实测（2026-11-19） | 根因 | 目标影响 |
|---|---|---|---|---|
| **P-A** | 关键断言核验率偏低 | **IGI-05 = 0.4726**（阈值 ≥0.90，[metrics-dictionary.json:45](../tools/metrics-dictionary.json)） | 报告层大量含数字 `<li>` / `<p>` 断言附近无来源指针；测量块类型仅覆盖 `li` / `p` | 决策者无法区分硬证据与未核验断言 |
| **P-B** | P0 四类盲区未消号 | **I-08 = 0.00（0/15）**（阈值 ≥0.60，[metrics-dictionary.json:38](../tools/metrics-dictionary.json)）；B01 / B02 / B03 / B15 责任周期均 2026-12 | 官方序列缺失或代理未建立；消号条件未走闭环 | 可负担性（月供 / 收入比）、供给兑现不可判 |
| **P-C** | 无逐期序列 | `semantic_diff scan`「有上期可比 0」；**IGI-03 = 0.6364**（阈值 ≥0.80）；**C-05 节拍达成率 = 0.3636**（阈值 =1.0） | 10 份报告全部为首期 / 基线；节拍未运转 | 滚动基线、阈值回测（2027-06）无数据基础 |
| **P-D** | 决策摘要超 1 屏 | **ID-02 5 项 `[W]`**（apartment baseline 1097 字、annual 3335 字、competitive-intelligence 1764 字、industry-research 1522 字、security 1789 字；阈值 ≤900 字 / ≤12 要点） | 摘要承载口径 / 假设 / 局限，未按分层交付下沉 | 决策者认知负载；离决策者最近处信噪比最低 |
| **P-E** | 工程噪声与 FALLBACK | **ruff 97 errors / mypy 45 errors**（门禁 `[W]`）；**A-01 / A-03 / L-03 三项 FALLBACK**（无工具接线） | 静态检查未收口；3 项 P0 指标无实测接线 | 「门禁全绿」公信力被稀释；可自证性不足 |

> **关联指标（不单独立项，并入对应杠杆）**：I-04 事实卡片引用率 = 0.40（阈值 ≥1.0，并入 P-A）；A-05 链接可达率 = probe（并入 P-E）；research_kernel 4 项历史 `[W]`（周期定位 / 传导量化 / 政策入模 / 盲区列示，随 P-C 逐期序列自然收口）。

---

## 2. 解决方案（逐项）

### 2.1 P0-1 · 杠杆一：IGI-05 关键断言核验率（0.47 → ≥0.90）

**现状机制**：IGI-05 = 「含数字断言块中带来源指针的比例」，窗口 = 同表格行或 ±240 字符，指针类型 = `[FC-…]` / `fact-ref` / `data-source-id` / 来源标签 / 外链（`info_gap_metrics.py:163-204`）。R4 块级逐点指针已落地（误报 0/19、非合规召回 4/4，见 [目标对齐批次报告](goal-alignment-batch-progress-2026-11-18.md) b6）。

**动作**：

| 轨道 | 动作 | 涉及文件 |
|---|---|---|
| A · 内容侧（主） | 对 10 份报告做「数字断言逐点指针」补标：含数字的 `<li>` / `<p>` 断言就近补来源标记（优先新报告：`competitive-intelligence/2026-12`、`industry-research/2026-12`、`apartment/2026_annual`） | `content/**/reports/*.html` |
| B · 工具侧 | 扩展 `_assertion_stats` 的块类型覆盖（`div.kpi` / `stat-strip` / `td` 等）与指针类型，并做**测量口径校准**（防止口径放宽导致虚高）；校准说明写入 `metrics-dictionary.json` 的 IGI-05 备注 | `engine/tools/info_gap_metrics.py` |
| C · 门禁侧 | IGI-05 已接入 `metric_audit`；在 `scheduled-maintenance.yml` 输出 IGI 趋势；发布前运行 `info_gap_metrics.py` 留痕 | `engine/tools/metric_registry.py`、`.github/workflows/scheduled-maintenance.yml` |
| D · 防刷 | 指针必须可解析（R4 块级判定）；禁止空指针 / 自链接充数（自链接豁免仅适用于 R1/R6，不适用于 IGI-05） | `engine/tools/source_check.py` |

**验收标准**：IGI-05 ≥ 0.90（3 个月滚动）；10 份报告逐份 `b/a` 明细随审计报表公开；人工抽样复核一致率 ≥ 95%。

**门禁映射**：`metric_audit`（已含 IGI-05 实测）、`source_check` R4、`info_density` ID-06 / ID-07。

**优先级**：**P0**。

### 2.2 P0-2 · 杠杆二：P0 四类盲区消号（0/15 → 2026-12 前 P0 四类闭环）

**现状**：盲区台账 15 项 open、0 closed（[blind-spot-ledger.md](../report-audits/blind-spot-ledger.md) §状态汇总）。P0 四类：B01 空置率、B02 就业、B03 竣工、B15 收入 / 薪资。

**动作（按消号条件三选一）**：

| 盲区 | 消号路径 | 对应发布日历 |
|---|---|---|
| **B02 就业 / 失业率** | ① 官方一手：Dubai LFS（DDSE）调查结果发布后双源入库 | 已有行（`release-calendar.md` §Dubai LFS，季，入库 10 日） |
| **B01 官方空置率** | ② 代理替代：ValuStrat / REIDIN + DLD 单元数据集自建，**须记录代理与校准方式** | 已有 DLD / Dubai Pulse 行 |
| **B03 官方竣工登记** | ② 代理替代：DM 竣工证书 + 机构三口径并列 | 已有 DM 行（季度，入库 10 日） |
| **B15 收入 / 薪资** | ① LFS / 薪酬指南官方英文页双源入库；**在发布日历增补「收入 / 薪酬」行** | 需新增 |

**验收标准**：P0 四类全部 `closed`（或明确转 P1 并更新责任周期）；I-08 盲区消号率 ≥ 0.60；台账逐项留证据链接与校准说明；`blind_spot_check.py` 通过。

**门禁映射**：`blind_spot`、`metric_audit`（I-08）、`release_calendar`。

**优先级**：**P0（2026-12 硬约束）**。

### 2.3 P0-3 · 杠杆三：建立逐期序列（无序列 → 第二期最小集）

**现状**：10 份报告均为首期 / 基线，读数时点集中 2026-11-13~15；`semantic_diff scan` 可比 0；IGI-03 = 0.6364、C-05 = 0.3636。

**动作**：

| 步骤 | 动作 | 涉及文件 |
|---|---|---|
| A · 定义最小集 | 按 `_common.TYPE_CADENCE` 与发布日历，先补：apartment 2026-12 monthly（月度节拍）、weekly-roundup 与 `content/economy/trends` 下一周 weekly、security 下一期 monthly | `_common.py`、`release-calendar.md` |
| B · 内容产出 | 走既有周期提示词（`prompt-monthly-monitor` / `prompt-weekly-monitor` 等）+ 人工 / Agent 撰写，**不自动生成内容** | `content/**/prompts/` |
| C · 工具侧 | `update_planner.py --pending-only` 输出任务清单（`content-update.yml` 已接线）；`semantic_diff scan` 产生可比对；`report-cycle-windows` 滚动基线生效 | `engine/tools/update_planner.py`、`semantic_diff.py` |
| D · 回测准备 | 序列 ≥ 3 期后启动 `threshold_calibration.py` 滚动分位数阈值；**2027-06 首次中期回测**不变 | `engine/tools/threshold_calibration.py` |
| E · 时效告警 | 报告 period 与读数时点纳入 IGI-03；连续 2 期未产出触发告警 | `.github/workflows/scheduled-maintenance.yml` |

**验收标准**：≥ 3 条业务线有第二期报告；`semantic_diff` 有上期可比 ≥ 1；IGI-03 ≥ 0.80；C-05 提升；滚动基线（本期更新 + 环比基期）在 hub 生效。

**门禁映射**：`semantic_diff`、`release_calendar`、`metric_audit`（IGI-03 / C-05）、`hub`。

**优先级**：**P0**。

### 2.4 P1-4 · 杠杆四：摘要密度治理（ID-02 5 项 `[W]` → 0）

**现状**：5 份报告摘要超 1 屏（见 §1 P-D）；ID-02 为 `WARN_ONLY`（`info_density_check.py:199`），**永不阻断**。

**动作**：

| 轨道 | 动作 | 涉及文件 |
|---|---|---|
| A · 内容重构 | 摘要只留「本期判定 + 关键变化 + 决策含义」结论性要点（≤12 条 / ≤900 字）；口径 / 假设 / 局限下沉证据层并以指针引用（与 ID-04 越级约束同步） | 5 份报告 |
| B · 工具侧（政策变更，二选一） | ① 将 ID-02 从 `WARN_ONLY` 调整为「新报告 `[E]` / 历史 `[W]`」；或 ② 保留 `[W]` 但新增「摘要密度趋势」纳入 IGI 报告。**建议 ①**（与 ID-04 已阻断的口径一致） | `info_density_check.py`、`information-layering-spec.md` 第七节 |
| C · 验收 | 5 份全部 ≤900 字 / ≤12 要点；若选 B-① 则新报告 0E | — |

**验收标准**：ID-02 警告清零；摘要合规率（IGI-07）保持 1.00；读者实测认知负载下降（抽样）。

**门禁映射**：`info_density` ID-02。

**优先级**：**P1**。

### 2.5 P1-5 · 杠杆五：工程噪声与 FALLBACK 收口（可自证性）

**现状**：ruff 97 errors / mypy 45 errors（门禁 `[W]`，[tech-debt-ledger](../report-audits/tech-debt-ledger.md) 未登记）；A-01 / A-03 / L-03 三项 P0 指标 FALLBACK；A-05 为 probe。

**动作**：

| 轨道 | 动作 | 涉及文件 |
|---|---|---|
| A · 静态检查 | 分「修缺陷」与「加 baseline 例外」两轨；目标 ruff / mypy 0 error，或显式 baseline 文件 + 只拦新增；登记入 tech-debt-ledger | `engine/tools/static_check.py`、`pyproject.toml`、`tech-debt-ledger.md` |
| B · FALLBACK 接线 | **A-01**：复用 IGI-05 断言级测量（同一数据源）接线工具部分；**A-03**：扩展 `consistency_check.py` 做「报告数值 vs 台账」逐值比对；**L-03**：扩展 `consistency_check.py` / `model_contract_check.py` 比对 business-config / 登记册 / 报告三处阈值 | `info_gap_metrics.py`、`consistency_check.py`、`model_contract_check.py` |
| C · 探测收口 | A-05 在 `scheduled-maintenance.yml` 定期 `--probe`，结果落审计记录 | `source_check.py` |

**验收标准**：38 项指标 measured ≥ 35（fallback = 0）；ruff / mypy 0 error 或 baseline 只拦新增；`metric_audit` 无「实测数据缺失」沉默项。

**门禁映射**：`metric_audit`、`ruff`、`mypy`、`consistency`、`model_contract`。

**优先级**：**P1**。

---

## 3. 实施顺序与依赖

| 阶段 | 时间锚 | 交付 | 依赖 |
|---|---|---|---|
| **S1** | 2026-11 内 | P0-1 工具侧（B/ C/ D 轨道）+ P0-2 发布日历增补 | 无 |
| **S2** | 2026-12 前 | P0-1 内容侧补标；P0-2 P0 四类消号 | S1 |
| **S3** | 2026-12 起 | P0-3 第二期最小集产出（[最小集定义](second-issue-minimal-set-2026-11-19.md)） | 提示词与内容流程（既有） |
| **S4** | 2026-12 起 | P1-4 摘要重构（结合 S3 的第二期重写） | S3 |
| **S5** | 独立 | P1-5 工程噪声与 FALLBACK 收口 | 无 |
| **S6** | 2027-06 | 阈值首次中期回测（`threshold_calibration.py`） | S3 序列 ≥ 3 期 |

> **硬约束**：2026-12（盲区责任周期）；2027-06（阈值回测）。滚动 gate-period（`auto` = 当前月 + 1）保证「新报告必阻断」不随时间失效。

---

## 4. 风险与反向证据

| 风险 | 说明 | 缓解 |
|---|---|---|
| **R-1 形式化补指针** | 补标时可能用空指针 / 自链接刷高 IGI-05 | 指针可解析 + R4 块级判定 + 人工抽样复核（一致率 ≥ 95%） |
| **R-2 测量口径虚高** | 扩展块类型可能让 IGI-05 「看起来达标」 | 校准说明写入 metrics-dictionary；口径变更留版本记录 |
| **R-3 代理替代假消号** | 盲区走②代理替代时口径漂移 | 消号条件②要求「记录代理与校准方式」；台账字段校验 |
| **R-4 序列内容成本高** | 第二期最小集仍需人工 / Agent 撰写 | 最小集先行（≥3 条业务线），不追求全业务线铺开 |
| **R-5 静态检查修复引入回归** | ruff / mypy 修复可能改动行为 | 单测 + 滚动 gate-period；baseline 例外只拦新增 |
| **反向证据** | 有观点认为「结构层已足够，无需再投入」 | 反驳：IGI-05 = 0.47、盲区 0/15、无逐期序列——三维目标（消除信息差 / 质量可靠 / 决策支撑）均未闭环；本方案是把「目标达」变成可证明的路径 |

**假设核验进度**：4 项关键假设中 2 项已核验（P0 三项工具抓手存在、ID-02 为 WARN_ONLY）；2 项待验证（IGI-08 提升幅度、静态检查修复成本）。

---

## 5. 就绪与阻塞说明

> 本节为 2026-11-19 会话中断后的收口状态（v1.1 追加）。等级标注同第二节。

**就绪（无外部依赖，可立即执行）**：

| 项 | 状态 | 证据 |
|---|---|---|
| 批 A 工具改动（IGI-05 口径校准 / A-01·A-03·L-03·R-03 接线 / 自链接防刷） | **[已核验] 已完成，待合并 PR #77** | IGI-05 = 0.9299（≥0.90）；L-03 = 0.4375（21/48，非退化）；R-03 转 TOOL 实测 0.1479；unittest 627 通过；门禁 0E / 8W |
| IGI 趋势快照接入定时维护（C 轨道） | **[已核验] 已完成** | `scheduled-maintenance.yml` 增 `audit_tool.py igi-snapshot` 步骤，`igi_history.json` 纳入提交路径 |
| 方案文档「就绪 + 阻塞说明」 | **[已核验] 本节** | — |

**口径决策（D4 调整，已核验）**：IGI-05 块类型扩展至 `div.kpi` / `stat-strip`；**`td` 不纳入**——与 R4 同口径（P1-7 实测表格逐单元格判定误报 164 处）。实测：纳入 `td` 后 IGI-05 降至 0.3881（2989 块中 1829 块无指针），不满足 ≥0.90 验收；剔除后 0.9299。

**阻塞（依赖外部 / 内容产出，本次不执行）**：

| 阶段 | 阻塞条件 | 责任周期 |
|---|---|---|
| S2 · P0-2 盲区消号 | 依赖 Dubai LFS 调查发布 / 代理数据自建（ValuStrat / REIDIN / DM 竣工） | **2027-03**（原 2026-12，取数阻塞顺延；I-08 仍 0/15） |
| S2 · P0-1 内容侧补标 | 依赖 10 份报告人工 / Agent 逐点补标 | 2026-12 前 |
| S3 · P0-3 第二期最小集 | 依赖内容产出（不自动生成） | 2026-12 起 |
| S4 · P1-4 摘要重构 | 依赖 S3 第二期重写 | 2026-12 起 |
| S5 · P1-5 工程噪声 | 依赖 ruff / mypy 安装与 baseline 策略（当前 ruff 97 / mypy 45，未收口） | 独立 |
| S6 · 阈值回测 | 依赖 S3 序列 ≥ 3 期 | 2027-06 |

**S2 取数进展（2026-11-19）**：P0 四类（B01 空置 / B02 就业 / B03 竣工 / B15 收入）取数尝试**未获可核验官方一手来源**（检索未命中 DDSE / DLD / DM / ValuStrat / REIDIN 官方页）。按「不虚报消号」原则不消号，责任周期由 2026-12 顺延至 **2027-03** 并逐类登记阻塞（见[盲区台账](blind-spot-ledger.md)「阻塞与取数记录」节）；`release-calendar.md` 已增补「收入 / 薪酬」行；`data-acquisition-checklist.md` 四项转 `blocked`。

**本节新增信息**：新增就绪/阻塞清单 1 组 ｜ 修正 0 条 ｜ 无变化 3 条 ｜ 假设核验进度 2/4。

---

## 6. 与既有规范的关系（单一事实源）

| 本方案内容 | 落点 | 不得复述于 |
|---|---|---|
| IGI-05 / I-08 / ID-02 规则 | `metrics-dictionary.json` / `info_density_check.py` | 本方案（只指针） |
| 盲区消号条件 | [决策交付规范](../templates/decision-delivery-spec.md) 第六节 | 本方案（只指针） |
| 摘要密度阈值 | [信息分层规范](../templates/information-layering-spec.md) 第七节 | 本方案（只指针） |
| 实施清单口径 | 本方案 §2 / §3 | 各 business-config |

---

## 7. 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-19 | 初始版本 | 5 项问题（P-A…P-E）+ 5 个杠杆（P0-1…P1-5）+ 实施顺序（S1–S6）+ 风险与反向证据 |
| v1.1 | 2026-11-19 | 追加 §5 就绪与阻塞说明；批 A 工具收口 | IGI-05 口径校准（块类型 + 指针 + 防刷，0.9338→0.9299）；A-01/A-03/L-03/R-03 接线；L-03 阈值正则重写（0/0 → 21/48）；R-03 字典 LLM→TOOL；scheduled-maintenance 接入 IGI 快照 |
| v1.2 | 2026-11-19 | S2 取数阻塞登记 | P0 四类取数未获官方一手来源；责任周期 2026-12 → 2027-03；发布日历增补收入/薪酬行；采集清单四项转 blocked |
| v1.3 | 2026-11-19 | 收口整合 | 新增整合文档 [优化解决方案与实施清单](optimization-solution-and-implementation-checklist-2026-11-19.md)；双视角闭环 + 16 项验证对齐清单 |
