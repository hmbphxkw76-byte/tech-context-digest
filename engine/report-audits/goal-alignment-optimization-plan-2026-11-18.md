# tech-context-digest 目标对齐优化解决方案（GOAL-ALIGNMENT-PLAN v1.2）

> **状态**：现行方案（2026-11-18 全量重审产出；v1.2 增「语义弱 / 度量空」专项方案）
> **目标**：以「尽可能消除信息差 / 保持信息质量可靠 / 支持基于信息的决策」为唯一评判尺，给出优化解决方案与可落地、可验收的完整实施清单。
> **方法**：从零重审（不采信既有审计结论），六维并行审计 + 规范逐条比对 + 工具实测复核；证据统一到 `文件:行号`。
> **等级标注**：本方案自身按[信息分层规范](../templates/information-layering-spec.md)第二节标注——`已核验`（代码/文件实测）、`部分核验`（抽样推断）、`推断`（机制分析）、`假设`（待验证）。
> **读者**：决策者读第 0 节即可；执行者读第 4–5 节。

---

## 0. 决策摘要

**本期判定（三条结论）**：

1. **[已核验]** 本仓库在**结构与合规层已高度成熟**：525 项单测全通过、统一门禁 23 项单一入口、`page_build_check` 12/12 页 0E0W、事实卡片 29 张零悬空引用、10 份报告来源标注与 `noopener` 全达标。**「规范 → 门禁 → CI」的骨架已经建立。**
2. **[已核验]** 但在**语义与度量层存在系统性断裂**：规范强制项有多处「门禁不查」（8 类）、内容门禁为**关键词级**判定（可被 CSS 注释与字面命中绕过）、30 项指标**全部 FALLBACK 从未被计算**、来源门禁因 gate-period 后置而**对现有语料零阻断**。结论：**门禁全绿 ≠ 目标达成**。
3. **[推断]** 因此当前对三大目标的支撑度为 **2.7 / 5**（消除信息差 2、质量可靠 3、决策支撑 3）。根因不是「缺规范」，而是**「规范未闭环到可度量、可阻断、可自证」**，以及**「信息差本身从未被定义和计算」**。

**决策含义**：

- 优先做**「度量闭环 + 门禁语义化」**，而不是继续新增规范条文——继续加规范只会扩大「规范有、门禁不查」的缺口。
- 四主题（教育/国际/政治/社会）空转是**信息差的最大来源**，但它属于**内容工程**而非引擎工程，应单独立项、以「接入就绪化」而非「自动生成」推进。
- 本轮落地 P0（引擎侧 6 项，见 §5.1），预计把「可度量性」与「门禁真实性」从`假设`提升到`已核验`；P1/P2 见 §5.2/§5.3。

**本期新增信息**：新增方案 1 份 / 修正既有认知 5 条（门禁盲区、度量断裂、gate-period 固定常量失效、hub 虚构基期、词库 auto_trigger 失效）/ 无变化 3 条（FC 零悬空、来源标注规范、单测全绿）/ 假设核验进度 3/6（见 §6）。

---

## 1. 审计方法与证据基线

| 项 | 内容 |
|---|---|
| 审计范围 | `content/` 7 条业务线 + 10 份报告；`engine/` 全量（docs 13、templates 8、prompts 14 类、tools 60+、vocabulary、tests 32）；`data/` 7 个 source_registry + 台账/卡片 |
| 审计方式 | 6 个只读代理并行（架构/来源事实/词库/提示词/报告/门禁度量）+ 主审逐条复核关键结论 |
| 独立复核 | `optimization_gate --probe`（0 E / 5 WARN）、`page_build_check`（0E0W）、`unittest`（525 OK, 1 skip）、`fact_card_check`（exit 0） |
| 反锚定 | 全程禁止读取 `engine/report-audits/` 既有结论，结论均由代码/文件重新推导 |
| 基准事实 | `layout.json` v4.1（6 主题，economy 维度 region→category，其余 category→region）；报告 10 份（economy 6 / tech 4）；读数时点集中 2026-11-13~15；当前日期 2026-11-18 |

---

## 2. 三维目标诊断

### 2.1 消除信息差 —— 支撑度 **2 / 5**

**定义（本方案口径，新增）**：信息差 = 决策者做决策所需信息 与 体系实际提供的信息 之间的缺口。可分解为四个可计算维度：

| 维度 | 含义 | 当前实测 |
|---|---|---|
| **覆盖差** | 声明范围 vs 实际覆盖 | **[已核验] 2/6 主题有内容**（`content/education|international|political|society` 各仅 1 个 `.gitkeep`）；7 条业务线全部集中在「迪拜 × 公寓/AI 网安」与「全球宏观/AI 趋势」 |
| **时效差** | 读数时点 vs 当前日期的时滞、周期断更 | **[已核验]** 10 份报告读数时点集中 2026-11-13~15，当前 2026-11-18；**全部为各线首期/基线**，无逐期序列；`semantic_diff` 自报「有上期可比 0」 |
| **核验差** | 关键断言中已核验占比 | **[部分核验]** 报告层标注规范（`已核验/部分核验/推断/假设` 齐全），但**决策摘要含「推断」**（见 §2.3），且核验状态无仓库级汇总 |
| **决策差** | 无决策卡 / 无触发条件 / 无反向证据的核心判断占比 | **[已核验]** `content/economy/trends/reports/2026-11-13_weekly.html:339` 的「决策卡」只存在于 CSS 注释中，正文无五字段卡 |

**根因**：

1. **[已核验] 信息差从未被定义与计算**。`metrics-dictionary.json` 定义了 30 项指标，但 `metric_registry.check_all_metrics()` 的 `measured` 默认 `{}`（`engine/tools/metric_registry.py:235`），`audit_tool.py` 调用时也不传实测值 → 30 项**全部 FALLBACK**（`engine/audit/records/pipeline_runs.jsonl` 尾部实证）。**「消除信息差」目前不可度量、不可比较、不可证明。**
2. **[已核验] 无时效监测**。`release_calendar.py` 只校验 P0 六维度覆盖率（`engine/tools/release_calendar.py`），不校验「报告是否按期产出」；10 份报告无一期逾期告警。
3. **[推断]** 四主题空转：`layout.json` 为四主题声明了维度，但无 `business-config.md`、无词库、无发布日历条目 → 架构与内容脱节，形成「有地图无道路」。

### 2.2 信息质量可靠 —— 支撑度 **3 / 5**

**强项（已核验）**：

- 来源四级分层单一事实源 `engine/tools/institution_tiers.json:5-10`；`source_check.py` R1–R7 实现完整（`engine/tools/source_check.py`）。
- 事实卡片 29 张（SEC 12 / IND 8 / CI 9），schema 8 字段强校验（`engine/tools/fact_card_check.py:30-34`），全仓 29 个 `[FC-…]` 引用**零悬空**（`fact_card_check` exit 0）。
- 报告来源标注实测达标：5 份样本链接全部可点击 + `target="_blank" rel="noopener"`；层级/机构/核验状态齐全（`content/economy/trends/reports/2026-11-13_weekly.html:643-670` 等）。

**短板（已核验）**：

| 编号 | 事实 | 影响 |
|---|---|---|
| Q-1 | **来源门禁实际不阻断**：`optimization_gate.py:51,70` 默认 `--source-gate-period 2027-01`，而现有报告全部为 2026-11/12 → 全部判为历史，R1–R6 降级 `[W]`。实测 `source_check --gate-period 2027-01` = **0 错误 / 28 警告** | 来源质量靠自觉，R1–R6 对存量语料零约束 |
| Q-2 | **gate-period 是固定常量，会随时间失效**：`DEFAULT_GATE_PERIOD = "2026-12"`、`DEFAULT_SOURCE_GATE_PERIOD = "2027-01"`（`optimization_gate.py:69-70`）写死在代码里。到 2027-02，2027-01 的新报告会被判为「历史」而降级放行 | 「新报告强制」的承诺**随时间自动失效**，与「动态滚动基线」的规范要求相悖 |
| Q-3 | **R4 判定过弱**：`source_check.py:556-559` 全文任一处出现「来源/参考/source」或任一 `data-source-id` 即通过。实测全部报告 `data-source-id=0`，`src-inline` 仅出现在 CSS | 关键数字可无逐点指针，R4 形同虚设 |
| Q-4 | **登记粒度不足**：7 个 `source_registry.json`（357 条）字段统一为 `source_id/tier/publisher/title/url/lang/verify_status/in_synthesis/used_in`，`verify_status` 仅 `verified|media_unverified`，**无「无法核实/待核实」取值**，**无 `updated` 时间字段** | 「无法核实」这一重要等级只能降级表达；时效无法追溯 |
| Q-5 | **死链真实存在但放行**：`optimization_gate --probe` 报 `source_check` 37 `[W]`，其中含 5 个 404/410/451 死链（如 `apartment/2026_annual`） | 死链在历史宽限下不阻断，读者可能撞上失效来源 |
| Q-6 | **词库无门禁、无 CI**：`.github/` 全目录 grep 无 vocab 引用；`optimization_gate` 23 项 CHECKS 无词库项；`engine/tests/` 无词库测试。同步失败仅落 `engine/vocabulary/data/sync.log` | 术语→提示词漂移**静默累积**，无兜底 |
| Q-7 | **词库→提示词已漂移**：`engine/vocabulary/prompts/economy/prompt-work-brief.md:13` 称规范形为「消费者价格指数」，而词库 `engine/vocabulary/data/economy/terms.md` ECO-049 词条为 `CPI`；`engine/vocabulary/prompts/tech/prompt-life-brief.md:14` 称规范形「多因素认证」，词库 TEC-155 为 `MFA` | 规范形约束名存实亡，同概念多写法 |

### 2.3 基于信息的决策 —— 支撑度 **3 / 5**

**强项（已核验）**：`content/economy/insight` 决策仪表盘结构完整度为全仓最高——6 张决策卡 + 信息充分度分布、34 条 FC 指针、反向证据与冲突读数并列、触发条件带阈值距离（`content/economy/insight/reports/2026-12_baseline_report.html`）。

**短板**：

| 编号 | 事实 | 影响 |
|---|---|---|
| D-1 | **决策摘要越级（违反 ID-04）**：`content/tech/industry-research/dubai/reports/2026-12_baseline_report.html:432` 核心判断标「推断 [FC-IND-001]」；`competitive-intelligence/dubai/.../2026-12_baseline_report.html:434` 摘要含「传导机制 推断」；`apartment/2026-11_monthly.html:439`、quarterly、annual 同类 | 规范明令「摘要仅许已核验+部分核验」，决策者可能据未核验判断行动 |
| D-2 | **证据强度两套口径冲突**：`content/tech/security/dubai/reports/2026-11_baseline_report.html:450` DC-1 证据强度「中」，而 `data/processed/economy/insight/decision_cards.json:33` DC-AI-SEC-01 为「强」且仪表盘摘要标「已核验」，支撑卡 `engine/fact_cards/security_fact_cards.json:51` FC-SEC-005 实为「部分核验」；DC-AI-TRD-01 标「强」仅凭单源厂商研究 | 同一判断两套强度，决策权重失真、等级拔高 |
| D-3 | **门禁盲区致违规放行**：`info_density_check.py:104-106` 需字数 >900 **且** 要点 >12 才报，而 `_plain` 去标签后无换行 → 要点恒 ≤1，ID-02 实际失效（annual 摘要 3731 字未报）；`:114` ID-04 仅匹配字面「假设乘积」，不匹配 `推断/假设` 等级标记；`decision_hub_check.py:63,69` 为**文档级存在性**，非逐卡逐项（故 trends 报告靠 CSS 注释通过） | 违规报告持续合规放行，规范无法自证 |
| D-4 | **canonical 标签零使用**：「假设乘积」全仓 0 次使用；`apartment/2026_annual.html:780` 三年供给情景标「全部为机制自算」，`:793` 敏感度表同 | 自算测算与已核验读数混排，无法区分确定值与假设积 |
| D-5 | **hub 环比基期为算术虚构**：`index.html:201/207/213` 标「环比基期 2026-10 / 2026-Q2 / 2025」，仓库无对应报告；`build_hub.py:718` 用 `prev_period()` 纯周期减法 | 读者误认存在历史对比基准，直接放大信息差 |
| D-6 | **行动项阈值定性**：insight 多条行动项阈值为「每期周报」「年度刷新」，不符决策交付规范 §2.1「阈值：数值 / 区间」 | 触发条件不可观测，行动协议无法自动判定 |
| D-7 | **无逐期序列**：10 份报告均为首期/基线，`semantic_diff` 0 可比 → 跨期 diff、阈值回测（计划 2027-06）**无数据基础** | 「滚动基线」承诺无法兑现 |

---

## 3. 核心问题清单（按对决策的有效贡献排序）

| # | 问题 | 证据 | 目标影响 | 级别 |
|---|---|---|---|---|
| **C-1** | 信息差从未被定义与计算，30 项指标全 FALLBACK | `metric_registry.py:235`；`pipeline_runs.jsonl` | 信息差 | **P0** |
| **C-2** | 门禁关键词化 + 盲区，[E] 规则可被系统性绕过 | `info_density_check.py:104-106,114`；`decision_hub_check.py:63,69` | 质量可靠 + 决策 | **P0** |
| **C-3** | gate-period 固定常量，随时间自动失效 | `optimization_gate.py:69-70` | 质量可靠 | **P0** |
| **C-4** | hub 环比基期虚构，向读者传递不存在的对比 | `build_hub.py:718`；`index.html:201/207/213` | 信息差 | **P0** |
| **C-5** | 词库无门禁且 auto_trigger 失效，漂移静默 | `vocab_tool.py:273-293`；`.github/` 无 vocab | 信息差 | **P0** |
| **C-6** | 摘要越级（含推断）违反 ID-04 | `industry-research/.../2026-12_baseline_report.html:432` 等 5 处 | 决策 | **P1** |
| **C-7** | 证据强度跨载体不一致（报告 vs 决策卡台账） | `security/.../2026-11_baseline_report.html:450` vs `decision_cards.json:33` | 决策 | **P1** |
| **C-8** | 来源登记缺「无法核实」取值与 `updated` 字段 | 7 个 registry 字段实测 | 质量可靠 | **P1** |
| **C-9** | 四主题空转，覆盖差最大来源 | `content/` 下 `education` / `international` / `political` / `society` 四主题各仅 1 个 `.gitkeep` | 信息差 | **P1** |
| **C-10** | 提示词三处复述漂移（泛用版过时 + 同名跨类型） | `engine/prompts/trend-weekly/prompt-weekly-monitor.md` vs `content/tech/weekly-roundup/prompts/prompt-weekly-monitor.md`；`prompt-monthly-monitor` 跨 market-monitoring / employment-research 复用 | 信息差 | **P1** |
| **C-11** | 类型注册表与实际脱节 | `template-registry.md` 第二节仅登记 5 条，遗漏 `content/tech/industry-research/dubai`、`content/tech/competitive-intelligence/dubai` | 质量可靠 | **P1** |
| **C-12** | N0–N8 编排未接线，CI 只 validate | `.github/workflows/ci.yml:239-240`；`pipeline_manifest.json:168` G8 `checks=[]` 恒 skipped | 决策 | **P1** |
| **C-13** | R4 关键数字判定过弱 | `source_check.py:556-559` | 质量可靠 | **P1** |
| **C-14** | 数据层两条 tech 业务线过薄（仅 source_registry） | `data/processed/tech/{competitive-intelligence,industry-research}/dubai/` | 决策 | **P2** |
| **C-15** | 死代码与规范外结构 | `content/economy/dubai/apartment/script/build_registry_v1.py`（保留：tracked xlsx 生产者，见 tech-debt-ledger §十）；`content/economy/trends/sources/archives/`（原 `followup/`，已迁移）；`content/tech/weekly-roundup/sources/legacy/`（保留：存档）；`weekly-roundup/README.md` 指向不存在的 `reports/legacy/`（已修正） | 质量可靠 | **P2** |

---

## 4. 优化方案

### 4.0 设计原则（新增，贯穿全案）

1. **闭环优先于条文**：任何新增规范必须同时给出「工具 + 门禁 + 验收标准」三件套，否则不批。
2. **度量先于优化**：先把「信息差」变成可计算指标，再谈改善——否则无法证明改善。
3. **门禁必须语义化**：禁止用「关键词命中」代替「结构判定」；判定单元下沉到**决策摘要节 / 决策卡 / 行动项 / 来源指针**级别。
4. **历史不追溯、新报告必阻断**：所有加强项通过**滚动 gate-period** 生效，不制造即时阻断，但绝不随时间失效。
5. **单一事实源 + 指针**：同一规则只在一处定义，其余位置引用；禁止在泛用版/模板/business-config 三处复述。

### 4.1 信息差度量体系（IGI，新增，最高优先）

**新增指标组**（写入 `engine/tools/metrics-dictionary.json`， severity=P0，detected_by=TOOL）：

| 指标 ID | 名称 | 公式 | 阈值 | 数据源 |
|---|---|---|---|---|
| **IGI-01** | 主题覆盖率 | 有 `business-config.md` 的主题数 / `layout.json` 注册主题数 | ≥ 0.50 | `_common.iter_business_dirs()` + `layout.json` |
| **IGI-02** | 业务线覆盖率 | 有 ≥1 份正式报告的业务线数 / 已声明业务线数 | ≥ 0.80 | `iter_reports()` |
| **IGI-03** | 时效健康度 | 距当前 ≤1 个周期的正式报告数 / 应有周期数（按 `TYPE_CADENCE` 推算） | ≥ 0.80 | 报告期次 + `release_calendar` |
| **IGI-04** | 来源登记覆盖率 | 报告内外部 URL 可匹配 registry 的比例（R1 的量化版） | ≥ 0.95 | `source_check.coverage_report()` |
| **IGI-05** | 关键断言核验率 | 带来源指针的含数字断言数 / 含数字断言总数 | ≥ 0.90 | 新增 `assertion_source_check` |
| **IGI-06** | 决策卡完备率 | 五字段齐全决策卡数 / 决策卡总数 | ≥ 0.95 | `decision_hub_check` 逐卡结果 |
| **IGI-07** | 摘要合规率 | 无越级（无推断/假设）摘要数 / 摘要总数 | ≥ 1.00 | `info_density_check` ID-04 |
| **IGI-08** | 信息差指数（合成） | `1 - 加权(IGI-01..07 归一化缺口)`，权重 0.25/0.15/0.15/0.15/0.10/0.10/0.10 | ≥ 0.80 | 上述汇总 |

**接线方式（关键）**：新增 `engine/tools/info_gap_metrics.py` 计算 IGI-01..07；`metric_registry.py audit` 子命令在无 `--measured` 时自动调用它填充实测值（`metric_registry.py:366-375`），使 `check_all_metrics` 不再恒 FALLBACK。**无数据时必须显式报「实测数据缺失」为 `[W]`，不得静默通过。**

**产出**：`engine/audit/records/pipeline_runs.jsonl` 尾部从 30 项 FALLBACK 变为真实达标/不达标；`scheduled-maintenance.yml` 每周输出 IGI 趋势。

### 4.2 门禁语义化改造

| 门禁 | 现状 | 改造 |
|---|---|---|
| `info_density_check` ID-02 | 需字数>900 **且** 要点>12，要点计数因 `_plain` 无换行恒 ≤1 | 按「决策摘要节」独立单元：字符数 >900 **或** 要点数 >12（取更严）即报；要点计数改为按块级元素（`li`/`p`/`br`）统计 |
| `info_density_check` ID-04 | 仅匹配字面「假设乘积」 | 摘要节内出现 `lvl-inferred` / `lvl-assumption` 标记或「推断」「假设」字样即报；剥离 HTML 注释后判定 |
| `decision_hub_check` DC-01/02 | 全文包含即通过（被 CSS 注释欺骗） | 剥离 `<!-- -->` 注释；解析每张决策卡（`conclusion/evidence_strength/trigger/counter_evidence/sufficiency`）与每条行动项（五要素 + 三档）逐项校验 |
| `source_check` R4 | 全文有来源词即豁免 | 含数字的块级断言（`p/li/td`）附近 `PROXIMITY_WINDOW` 内须有来源标记（`[FC-`/`[K\d`/`[Source:`/`data-source-id`/registry 编号） |
| 全部内容门禁 | 全文匹配 | 判定前先剥离 HTML 注释与 `<style>`/`<script>` 块，避免注释误判 |

### 4.3 滚动 gate-period（修 C-3）

- `optimization_gate.py` 新增 `--gate-period auto`（**默认 auto`）`：解析为「当前自然月 + 1」；`--source-gate-period auto` 同理。
- 各门禁脚本（`info_density_check` / `decision_hub_check` / `research_kernel_check` / `source_check`）接受 `auto` 并同样解析。
- 效果：新报告**永远**被强制，历史报告**永远**只警告；不再随时间失效。
- 兼容：显式传 `YYYY-MM` 仍可用（CI 可固定口径复现）；`test_process_gates.py` 增加 auto 接线断言。

### 4.4 报告质量治理（P1）

- **摘要越级修正**：把 5 处「推断/假设」结论移出决策摘要，摘要只留已核验+部分核验，推断内容下沉证据层并以「见证据层」指针引用（ID-04）。
- **证据强度一致性**：以 `engine/fact_cards/*.json` 的 `level` 为唯一依据重算 `decision_cards.json` 的 `evidence_strength`（强=关键事实全部已核验且双源；中=主体已核验；弱=含推断/假设），并加门禁 `DC-08 证据强度与支撑卡等级一致`。
- **「假设乘积」标注**：`apartment/2026_annual.html:780,793` 等自算情景改为「假设乘积 + 区间」。
- **行动项阈值数值化**：insight 行动项阈值改数值/区间。
- **trends 决策卡**：补五字段决策卡（或明确声明该线为「核验型轻运行」并豁免，二者取一，不得含糊）。

### 4.5 提示词单一事实源收敛（P1）

- 以业务线实例为准回写泛用版：`engine/prompts/trend-weekly/prompt-weekly-monitor.md`（八节/3 板块）与 `content/tech/weekly-roundup/prompts/prompt-weekly-monitor.md`（v1.9 的 10 节/5 板块）二选一，保留后者、前者改为指针。
- 解决 `prompt-monthly-monitor` 跨类型复用：按类型拆分命名（`prompt-monthly-update` vs `prompt-monthly-monitor`），或明确「同名不同构」并在注册表登记差异。
- **新增 `prompt_consistency_check.py`**：校验 ① 泛用版/类型模板/business-config 三者对同一强制项的表述一致；② business-config 不得复述规范正文（`information-layering-spec.md` §1.3 要求「只实例化」）；③ 类型注册表登记的业务线与实际 `content/` 一致（修 C-11）。接入 `optimization_gate` 与 CI。
- `business-config` 七份复述段（信息等级/决策卡/ex-ante 规则句）改为指针引用。

### 4.6 词库对齐（P1）

- 修 `vocab_tool.py:273-293`：`auto_sync_hook` 读取 `sync.json` 的 `auto_trigger`，false 时跳过。
- 修 `sync_vocab.py:403` verify 日志用 `tpath.name` 导致两个 tech 目标不可区分 → 改用 `topic=>relpath`。
- **新增 `vocab_drift_check.py`** 接入 `optimization_gate`：① 六主题词库非空（空库 `[W]`，新主题 `[E]`）；② 同步区区块完整（`VOCAB-SYNC:BEGIN/END` 成对）；③ 提示词声称的规范形与词库词条一致（修 Q-7）。
- 统一规范形策略（缩写 vs 中文），并补录高频缺口概念（口径/成交/阈值/监测/台账/预校准/盲区/决策卡等 top 10）。
- 四主题建词库骨架（`prompt-skeleton.md` 已存在，扩展为可用骨架）。

### 4.7 内容覆盖与数据层（P1）

- **四主题接入就绪化**（不自动生成内容）：为 `content/` 下四个空主题（`education` / `international` / `political` / `society`）各建 `business-config.md`（14 节）+ 基线提示词 + 发布日历条目 + 词库骨架，使 `iter_business_dirs()` 可发现、IGI-01 可提升。**报告正文仍按 AGENTS.md 由人工/Agent 依提示词撰写。**
- 补 `data/processed/tech/{competitive-intelligence,industry-research}/dubai` 的台账与量化数据（当前仅 `source_registry.json`）。
- `data/raw/` 落原始抓取（至少保留官方来源快照/导出），使报告可溯源到一手文件（修「报告不可溯源」）。

### 4.8 架构与编排（P1）

- **修 C-4**：`build_hub.py` 仅在仓库真实存在上一期报告时才输出「本期更新 · 环比基期」徽章；否则不标（或标「首期基线」）。
- **接线 N0–N8**：`ci.yml` 在 validate 之外调用 `pipeline_runner.py run`（或至少在 `scheduled-maintenance.yml` 试跑并留痕），G8 `checks=[]` 补实际检查项。
- **模型契约门禁**：把 `transmission/valuation/stress_test` 的「参数区间 + 假设 + 失败上报」从单测提升为 `optimization_gate` 检查项（DC-07）。
- 清理死代码与规范外结构（C-15），文档漂移修正（`weekly-roundup/README.md`）。

### 4.9 语义弱专项方案（批次 A）

**根因**：规范条文只约束「新报告撰写时的人工照做」，没有机械门禁在生成 / 提交时校验；存量报告与生成器可绕开。**解法**：把规范中**机械可判定**的条款逐条接入门禁，并修掉存量违规；语义判断类条款不伪造自动化，显式标注为 LLM / 人工项。

**8 类「规范有、门禁不查」缺口 → 接线**：

| # | 缺口 | 规范出处 | 门禁接线 | 级别 |
|---|---|---|---|---|
| S1 | 监测渲染机械项：图表图注单位 / 来源、口径并列、列宽塌缩、noopener、断头数字、hover tooltip | monitoring-common-spec §2 / §3 / §4 / §6 | 新增 `engine/tools/monitoring_render_check.py`（MON-01..），接入统一门禁 | [W] |
| S2 | 看板-台账一致：阈值 / 口径 / 基期在 hub 与 `data/processed` 台账一致 | information-layering §3.2 | `consistency_check.py`（LC-01 台账结构 / LC-02 看板指标名在最新报告出现） | [W] |
| S3 | 版本治理：仅核心事实修正才升版本号，核验型运行不升版本 | decision-delivery §7 | `consistency_check.py`（VG-01 读数时点 / VG-02 语义版本修正留痕） | [W] |
| S4 | 文件命名与维度顺序：kebab-case、`layout.json` 声明顺序 | structure-and-naming §8 | `validate_layout.py`（维度顺序）+ `naming_check.py`（NC-01/02 全量命名扫描） | [E] / [W] |
| S5 | 假设不得进入决策摘要点值 | information-layering §2.3-3 | 已由 P0-2（ID-04 点值检查）落地 | [E] |
| S6 | 模型契约：指标定义 / 阈值 / 口径三处一致 | decision-delivery §4 | 新增契约门禁，接 `L-03` 阈值三处一致 | [W] |
| S7 | 不得复制决策卡全文 / 卡片同义复述 | information-layering §5.3 | 重复率代理校验，接 `R-03` | [W] |
| S8 | 共享 boilerplate 上移后报告残留 | prompt-generic-base §10 | 残留率代理校验，接 `R-02` | [W] |

**执行顺序**：S1（新增渲染门禁）→ S2 / S3（一致性 / 版本）→ S4（命名收口）→ S6–S8（契约与重复率，随批次 C / D 收口）。

### 4.10 度量空专项方案（批次 B）

**根因**：`metrics-dictionary.json` 的 38 项指标注册了公式与阈值，但只有 IGI-01..08 接了实测；其余 30 项走结构兜底（FALLBACK），`metric_registry audit` 恒报「30 项无实测值」——**看起来像达标、实际没度量**。

**38 项盘点**（`detected_by`）：

| 类别 | 数量 | 指标 | 处置 |
|---|---|---|---|
| TOOL | 22 | C-01/02/03/05/06、A-05、R-01/02/04、I-01/03/04/07/08/09、IGI-01/02/03/04/06/07/08 | 复用既有工具产出实测值 |
| MIXED | 8 | C-04、A-01、A-03、L-03、I-02、I-05、I-06、IGI-05 | 工具可测部分接线，语义部分标 LLM |
| LLM | 8 | A-02、A-04、L-01、L-02、L-04、L-05、R-03、R-05 | 显式标注「LLM / 人工判定」，不伪造实测值 |

**解法**：

1. 新增 `engine/tools/metric_coverage.py`（**已落地**）：汇总 22 项 TOOL 指标的实测值（复用 `validate_layout` / `check_links` / `page_build_check` / `info_density` / `fact_card` / `decision_hub` / `source_check` / `metric_registry` / `info_gap_metrics`），产出覆盖率与缺口清单。当前实测 **26 项**（TOOL 22 项中 21 项 measured、A-05 需网络探测；MIXED 代理 4 项），LLM 8 项显式标注，未接线 3 项（A-01 / A-03 / L-03）入 gap。
2. 8 项 MIXED 指标中工具可测子集（I-02 标注率、I-06 决策卡覆盖、L-03 阈值三处一致、IGI-05 来源指针率）接线实测。
3. `metric_registry audit --coverage` 输出「指标覆盖报告」：measured / fallback / LLM 三类计数与逐项缺口，替代恒报 FALLBACK 的沉默。
4. 覆盖率为 0 的指标视为**未度量**，进入 `tech-debt-ledger` 并给出接线计划（不静默跳过）。

**验收**：22 项 TOOL 指标全部有实测值（非 FALLBACK）；MIXED 工具部分接线；LLM 项显式标注；`audit` 输出覆盖率与缺口清单。**实际**：26 measured / 1 probe（A-05）/ 3 fallback（A-01、A-03、L-03）/ 8 llm；`metric_registry audit --coverage` 已输出覆盖与缺口。

---

## 5. 完整实施清单

> **字段**：ID｜优先级｜动作｜涉及文件｜验收标准｜门禁映射｜依赖
> **优先级口径**：三维并重，按「对决策的有效贡献」排序——P0 = 不修则目标不可度量/门禁不可信；P1 = 不修则质量与覆盖有实质缺口；P2 = 治理与卫生。
> **本轮落地**：§5.1 全部 6 项。

### 5.1 P0 —— 本轮落地（度量闭环 + 门禁真实性）

| ID | 动作 | 涉及文件 | 验收标准 | 门禁映射 |
|---|---|---|---|---|
| **P0-1** | 新增 IGI 指标组并接线实测值 | `engine/tools/metrics-dictionary.json`、**新增** `engine/tools/info_gap_metrics.py`、`engine/tools/metric_registry.py:226-265,366-375`、`engine/audit/scripts/audit_tool.py` | 8 项指标定义齐全；`metric_registry.py audit` 输出中 FALLBACK 项数 = 0（有数据时）；无数据时输出「实测数据缺失」`[W]`；`pipeline_runs.jsonl` 尾部含真实 status | `metric_audit`（新增 IGI 判定）；`optimization_gate` |
| **P0-2** | `info_density_check` ID-02/ID-04 语义化 + 剥离注释 | `engine/tools/info_density_check.py:89-139` | ID-02 改为「字符>900 或 要点>12」并正确计数块级要点；ID-04 在摘要节内检出 `lvl-inferred/lvl-assumption` 与「推断/假设」；剥离 `<!-- -->` 后判定；新增单测覆盖 | `info_density` |
| **P0-3** | `decision_hub_check` 逐卡/逐项校验 | `engine/tools/decision_hub_check.py:57-88` | 剥离注释后逐卡解析五字段、逐条解析行动项五要素 + 三档；`trends` 报告不再因注释误判通过；新增单测（含注释陷阱用例） | `decision_hub` |
| **P0-4** | 滚动 gate-period（`auto`） | `engine/tools/optimization_gate.py:69-70,139-143`、`info_density_check.py:32,198`、`decision_hub_check.py:26,134`、`source_check.py:131-136,742`、`research_kernel_check.py`、`engine/tests/test_process_gates.py` | `--gate-period auto` / `--source-gate-period auto` 解析为「当前月+1」；默认 auto；显式 `YYYY-MM` 仍可用；单测断言 auto 接线与「历史/W、新/E」判定 | `test_process_gates::TestOptimizationGateReuse`；全部内容门禁 |
| **P0-5** | hub 环比基期只标真实上期 | `engine/tools/build_hub.py`（`has_previous_period` / `_render_card` / `global_base_period`）、`index.html`、`reader.html`、`engine/tests/test_tools.py`、`engine/tests/test_goal_alignment.py` | 无同周期上一期报告时输出「首期」徽章而非虚构基期；Hero 改标「最新月报 X」；`build_hub --check` 通过；单测覆盖有/无上期与跨周期三分支 | `hub` |
| **P0-6** | 词库同步修复 + 漂移门禁接入统一入口 | `engine/vocabulary/script/vocab_tool.py:273-293`、**新增** `engine/tools/vocab_drift_check.py`、`engine/tools/optimization_gate.py` | `auto_trigger=false` 时钩子不触发（单测）；`vocab_drift` 已接入统一门禁（第 24 项） | `optimization_gate`（第 24 项） |

**P0-6 接线说明**：`vocab_drift_check` 已接入 `optimization_gate`（第 24 项），门禁清单 23 → 24 已同步全部声明文件——包括 `AGENTS.md`、报告全链路体系说明与流程复用清单、架构与开发规范/端到端覆盖/页面构建治理/流程治理四份文档、报告流水线实施方案、audit 目录的 verification 文件、tools 目录的 README 与 pipeline_runner 及其测试、以及 mainline 适配评估（2026-11-17）。

### 5.2 P1 —— 质量与覆盖实质缺口（下一轮）

| ID | 动作 | 涉及文件 | 验收标准 | 门禁映射 |
|---|---|---|---|---|
| P1-1 | 摘要越级修正（5 处） | `content/tech/industry-research/dubai/reports/2026-12_baseline_report.html:432`、`content/tech/competitive-intelligence/dubai/reports/2026-12_baseline_report.html:434`、`content/economy/dubai/apartment/reports/{2026-11_monthly,2026-Q3_quarterly,2026_annual}.html` | 摘要节内零「推断/假设」；推断内容下沉并以指针引用；ID-04 全绿 | `info_density` ID-04 |
| P1-2 | 证据强度一致性 + DC-08 门禁 | `data/processed/economy/insight/decision_cards.json`、`engine/fact_cards/*.json`、`decision_hub_check.py` | 决策卡 `evidence_strength` 由支撑卡 `level` 唯一推导；DC-08 校验跨载体一致 | `decision_hub` DC-08（新增） |
| P1-3 | 「假设乘积」标注治理 | `content/economy/dubai/apartment/reports/2026_annual.html:780,793`、`content/economy/insight/reports/2026-12_baseline_report.html` | 自算测算全部标「假设乘积 + 区间」；ID-04 扩展匹配 | `info_density` ID-04 |
| P1-4 | 行动项阈值数值化 | `content/economy/insight/reports/2026-12_baseline_report.html` 等 | 阈值字段为数值/区间；DC-02 校验阈值可解析 | `decision_hub` DC-02 |
| P1-5 | trends 决策卡补全或显式豁免 | `content/economy/trends/reports/2026-11-13_weekly.html` | 有二选一的明确处置，门禁判定一致 | `decision_hub` DC-01 |
| P1-6 | 来源登记字段扩展 | 7 个 `data/processed/**/source_registry.json`、`source_check.py` | `verify_status` 增加 `unverifiable`（无法核实）；新增 `updated` 字段；存量数据补字段 | `source_check` R1/R7 |
| P1-7 | R4 关键数字逐点指针 | `source_check.py:556-559` | 含数字块级断言附近窗口内须有来源标记；抽样误报率 < 5% | `source_check` R4 |
| P1-8 | 死链真实修复 | `content/economy/dubai/apartment/reports/2026_annual.html` 等 5 处死链 | `--probe` 下死链 `[E]` 归零 | `source_check` R6 |
| P1-9 | 四主题接入就绪化 | `content/{education,international,political,society}/prompts/business-config.md` 等 | 四主题 `iter_business_dirs()` 可发现；IGI-01 ≥ 0.5；词库骨架非空 | `vocab_drift_check`、`IGI-01` |
| P1-10 | 提示词单一事实源收敛 + 一致性门禁 | `engine/prompts/trend-weekly/prompt-weekly-monitor.md`、`engine/prompts/` 下各周期提示词、**新增** `prompt_consistency_check.py`（置于 `engine/tools/`） | 泛用版与业务线实例一致或前者改为指针；business-config 去复述；注册表与实际业务线一致（C-11） | `optimization_gate`（**已接入 `prompt_consistency`**） |
| P1-11 | 词库规范形统一 + 缺口补录 | `engine/vocabulary/data/*/terms.md`、`engine/vocabulary/prompts/*` | 提示词声称的规范形与词库一致；top 10 高频概念入库 | `vocab_drift_check` |
| P1-12 | N0–N8 接线 | `.github/workflows/ci.yml:239-240`、`engine/tools/pipeline_manifest.json:168`、`pipeline_runner.py` | CI 调用 `pipeline_runner run` 并留痕；G8 `checks` 非空 | `pipeline_audit` |
| P1-13 | 模型契约门禁 | `engine/tools/` 下 `transmission/` 弹性模型、`optimization_gate.py` | DC-07 从单测提升为 gate 检查项 | `optimization_gate` |
| P1-14 | 数据层补薄 + raw 落仓 | `data/processed/tech/{competitive-intelligence,industry-research}/dubai/`、`data/raw/` | 两条 tech 业务线有台账 + 量化数据；官方来源快照落 raw | `IGI-05` |
| P1-15 | hub 卡片信息区分度 | `build_hub.py` | 同周期多报告可区分（标题/类型/地区） | `hub` |

> **批次 C 进度（2026-11-18）**：P1-10 已落地——新增 `prompt_consistency_check.py`（PC-01 注册表一致 / PC-02 去复述 / PC-03 周期模板齐备）并接入统一门禁（第 28 项）；`template-registry.md` 补登 `competitive-intelligence/dubai`、`industry-research/dubai`（修 C-11）；7 份 business-config 复述段改为指针。P1-1/3/4/5/6/7/8/9/11/12/13/14/15 未落地（见 §5.2）。

### 5.3 P2 —— 治理与卫生

| ID | 动作 | 涉及文件 | 验收标准 |
|---|---|---|---|
| P2-1 | 死代码清理 | `content/economy/dubai/apartment/script/build_registry_v1.py`（保留）、`content/economy/trends/sources/archives/`（原 `followup/`，已迁移）、`content/tech/weekly-roundup/sources/legacy/`（保留） | 删除或迁入 `sources/archives/`；`validate_layout` 通过（**已落地，处置见 tech-debt-ledger §十**） |
| P2-2 | 文档漂移修正 | `content/tech/weekly-roundup/README.md`（指向不存在的 `reports/legacy/`） | 文档与实际目录一致；`check_links` 通过（**已落地**：仅 `sources/legacy/` 存在；`reports/legacy/` 系 2026-11-17 有意清理（tech-debt-ledger B12–B14 closed），README / operations-guide / 台账三处指向已修正） |
| P2-3 | 提示词引用 AGENTS/PCE | `engine/templates/prompt-generic-base.md`、`engine/prompts/*` | 提示词层感知「执行xx报告」触发与润色-确认门禁（**已落地**：通用基座第八节新增指针） |
| P2-4 | 类型注册表同步 | `engine/templates/template-registry.md` 第二节 | 登记全部 7 条业务线；新增业务线自动校验（**已落地**：PC-01 补登 + 门禁） |
| P2-5 | 主题 README 治理 | 各主题 README | 与 `business-config.md` 一致 |
| P2-6 | 审计报表增强 | `engine/audit/`、`audit_tool.py` | IGI 趋势纳入审计报表现（**已落地**：`audit_tool.py status` 固定输出 IGI 八度趋势表；`igi-snapshot` 按 gate-period 落盘 `records/igi_history.json`，月末基准、同周期覆盖幂等） |
| P2-7 | 报告结构加固 | `apartment/monthly|baseline|annual` 缺 `nav-tabs` | `compliance_check` 0E（**核实已满足**：四份公寓报告 `nav-tabs` 各 7 处；`compliance_check` 通过，0 错误） |
| P2-8 | 术语策略文档 | `engine/vocabulary/README.md` | 明确缩写/中文规范形策略（**已落地**：新增「七·补 术语策略」） |

> **批次 D 进度（2026-11-18）**：P2-2 已核实无漂移；P2-3 / P2-4 / P2-8 已落地；P2-1（死代码删除 / 迁移，需授权）、P2-5（主题 README 治理）、P2-6（审计报表增强）、P2-7（核实已基本满足：baseline 属规范豁免，compliance_check 0E）未落地。

---

## 6. 风险与反向证据

| 风险 | 说明 | 缓解 |
|---|---|---|
| **R-1 门禁加强立即暴露存量违规** | P0-2/P0-3 加强后，现有 10 份报告（含 2026-12）会产生大量 `[E]` | 通过 P0-4 滚动 gate-period，强制期从「当前月+1」起算；存量报告为历史 `[W]`，不制造即时阻断 |
| **R-2 IGI 指标可能诱发「刷指标」** | 覆盖率类指标可通过建空壳 business-config 注水 | IGI-01 要求 `business-config` **14 节齐全**且 `iter_reports()` 有产出；IGI-08 合成指数含核验率与摘要合规率，空壳无法提升 |
| **R-3 逐卡门禁误报** | 决策卡结构多样，解析器可能误判 | P0-3 先覆盖 canonical 五字段结构；误报以单测校准；误报率高则降级为 `[W]` 并保留人工审计 L3 权威 |
| **R-4 与既有规范冲突** | 本方案新增 IGI 指标组与 DC-08，需回写规范 | 按「新增即删旧」：IGI 定义只入 `metrics-dictionary.json`，方案文档只指针；DC-08 入 `decision-delivery-spec.md` 第八节表格 |
| **R-5 度量接线改变审计语义** | `metric_audit` 由「恒 FALLBACK」变为真实判定，可能首次出现不达标 | 这是**预期且必要**的——不达标即暴露真实缺口；建议首次以 `[W]` 发布，下一周期转 `[E]` |
| **反向证据** | 有观点认为「525 单测 + 23 门禁已足够，无需再加度量层」 | 反驳：全绿门禁下仍实测出摘要越级、证据强度冲突、虚构基期、指标全 FALLBACK——**门禁绿不等于目标达**；度量层正是把「目标达」变成可证明的唯一路径 |

**假设核验进度**：6 项关键假设中 3 项已核验（C-1 度量断裂、C-2 门禁盲区、C-4 虚构基期，均代码/文件实测）；3 项待验证（IGI 权重合理性、R-3 误报率、四主题接入成本）。

---

## 7. 与既有规范的关系（单一事实源纪律）

| 本方案内容 | 落点 | 不得复述于 |
|---|---|---|
| IGI 指标定义 | `engine/tools/metrics-dictionary.json` | 本方案（只指针）、各 business-config |
| DC-08 规则 | `engine/templates/decision-delivery-spec.md` 第八节 | 本方案（只指针） |
| 滚动 gate-period 规则 | `engine/docs/report-pipeline-system.md` §5.2 | 本方案（只指针） |
| 提示词一致性规则 | `engine/docs/structure-and-naming-spec.md` 或新专文 | 本方案（只指针） |

---

## 附录 A：本轮落地记录（2026-11-18，P0）

**已落地并验证**（`unittest` 553 通过；`optimization_gate --probe` 0 错误 / 7 警告）：

| 项 | 落地内容 | 验证 |
|---|---|---|
| P0-1 | 新增 `engine/tools/info_gap_metrics.py`（IGI-01..08 实测）+ `metrics-dictionary.json` 增补 8 项 + `metric_registry audit` 接线实测值（此前 30 项全 FALLBACK） | 实测 IGI-08 = 0.746（阈值 0.80，不达标项显式上报） |
| P0-2 | `info_density_check` 剥离注释/样式、ID-02 改「或」判定、ID-04 增「摘要结论性要点不得带推断/假设等级标记」（排除提示块与信号灯误报） | 新报告 2 处违规已修正；门禁 0E |
| P0-3 | `decision_hub_check` 剥离注释/样式 + 逐卡（结论/证据强度/反向证据）与逐条行动项（五要素）校验 | `trends` 报告不再因 CSS 注释误判通过 |
| P0-4 | `gate_period.py` 滚动基线（`auto` = 当前月 + 1）；两级默认改 `auto`；`local_mainline` / 各门禁 / 规范同步 | 新报告判定不再随时间失效 |
| P0-6 | `vocab_tool.auto_sync_hook` 尊重 `auto_trigger`；新增 `vocab_drift_check.py`（VD-01..03）并接入统一门禁（第 24 项） | 门禁清单 23 → 24，声明文件全部同步；gate 0E |
| P0-5 | `build_hub` 仅在同周期上一期报告真实存在时才标「本期更新 · 环比基期」，否则标「首期」；Hero 改标「最新月报」 | hub 中不再出现虚构基期；`hub --check` / `page_build_check` 通过 |
| 报告修正 | `industry-research/2026-12` 移除摘要推断项；`competitive-intelligence/2026-12` 推断下沉证据层（FC 指针保留）；`apartment/2026_annual` 补 tier-4 标注 | ID-04 新报告 0E |
| 来源治理 | 补登 6 条缺失来源（CI menlovc URL 修正 + apartment 5 条官方/媒体源）；CI tier-4 11 条补「需核实原文」；`source_check` 增自链接豁免（内部指针） | source_check 0E / 36W |

**本轮新增政策（已写入代码与规范）**：

- **R6 死链规则级期限**：死链阻断自 `R6_STRICT_PERIOD = "2027-01"` 起，此前仅告警。理由：链接腐烂修复属内容维护（P1-8），实测 13 处死链（含 centralbank.ae / u.ae / dsc.gov.ae 等官方页迁移），集中清理完成前不阻断合并；到期后自动转 `[E]`，滚动基线下不失效。
- **自链接豁免**：指向本仓库自身的 GitHub 链接为内部指针，不计入 R1 登记覆盖与 R6 死链判定（私有仓库下外部探测必然 404）。

**未落地（顺延）**：

- **P1 全部 15 项 / P2 全部 8 项**：按优先级分批推进。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-18 | 初始版本 | 六维全量重审；三维诊断（2/5、3/5、3/5）；15 项核心问题；八面优化方案；52 条实施清单（P0 6 / P1 15 / P2 8） |
| v1.1 | 2026-11-18 | 落地记录 | 附录 A：P0 落地与验证、R6 规则级期限与自链接豁免两项新政策、受阻项说明 |
| v1.2 | 2026-11-18 | 专项方案 | 新增 §4.9「语义弱专项方案」（8 类门禁缺口逐条接线）与 §4.10「度量空专项方案」（38 项指标盘点与实测覆盖路径）；批次 b0 产出 |
