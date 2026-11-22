# 目标对齐批次执行差异报告（b0–b6）

> **时点**：2026-11-18 ｜ **分支**：`task/goal-alignment-batches-67312f84` ｜ **PR**：#58
> **续接**：会话 `2e6777f5`（「消除信息差的全面优化方案与实施清单」）未完成批次。
> **判级**：`已核验`（代码/门禁实测）、`部分核验`（抽样）、`推断`（机制）。

---

## 一、总览

| 批次 | 内容 | 状态 | 证据 |
|---|---|---|---|
| b0 | 「语义弱 / 度量空」专项方案落入方案文档 v1.2 | **已核验·完成** | 方案文档 §4.9 / §4.10；版本记录 v1.2 |
| b1 | 批次 A 语义弱：监测渲染 / 看板台账 / 版本治理 / 命名 | **已核验·完成** | 门禁 24→27；`monitoring_render` / `consistency` / `naming` |
| b2 | 批次 B 度量空：指标实测覆盖 + 覆盖报告 | **已核验·完成** | 26 实测 / 1 探测 / 3 未接线 / 8 LLM |
| b3 | 批次 C P1 内容 / 覆盖 | **部分核验·部分完成** | P1-10 / P1-12 / P1-13 落地；其余 12 项未落地 |
| b4 | 批次 D P2 治理卫生 | **部分核验·部分完成** | P2-2 / 3 / 4 / 8 落地；其余 4 项未落地 |
| b5 | 收尾验收与差异报告 | **已核验·完成** | 本报告；unittest 583 通过；gate 0E / 9W |
| b6 | 续接会话：16 项未落地清单清零（12 P1 + 4 P2） | **已核验·完成** | PR #62/#63/#64/#66/#67/#69/#70/#71/#73/#74；unittest 625 通过；gate 0E / 8W |

**统一门禁**：24 → **29 项**（新增 `monitoring_render`、`consistency`、`naming`、`prompt_consistency`、`model_contract`）。

---

## 二、逐批交付

### b0 专项方案（v1.2）

- 方案文档 `goal-alignment-optimization-plan-2026-11-18.md` 升级 v1.2：
  - §4.9 语义弱专项：8 类「规范有、门禁不查」缺口 → 门禁接线表（S1–S8）。
  - §4.10 度量空专项：38 项指标按 `detected_by` 盘点（TOOL 22 / MIXED 8 / LLM 8）与实测覆盖路径。

### b1 批次 A（语义弱）

| 新增门禁 | 规则 | 级别 |
|---|---|---|
| `monitoring_render` | MON-01 图注齐备 / MON-02 口径并列须注明不可相减 / MON-03 列宽塌缩 / MON-04 noopener / MON-05 原生 title | [W] |
| `consistency` | LC-01 台账结构 / LC-02 看板指标名在最新报告出现 / VG-01 读数时点 / VG-02 语义版本修正留痕 | [W] |
| `naming` | NC-01 目录 kebab-case / NC-02 按位置文件命名规则矩阵 | [W] |

- **附带修复**：`publish_fingerprint` 对 CRLF→LF 归一后再哈希。根因：仓库 `core.autocrlf=true`（Windows 工作区 CRLF、CI LF），按原始字节哈希**平台相关**，恒报漂移。归一后与 CI 登记一致（9/10 立即匹配，1 份为本次修改）。

### b2 批次 B（度量空）

- 新增 `metric_coverage.py`：为 38 项指标产出实测值 / 缺口清单。
- `metric_registry audit --coverage` 输出覆盖报告。
- **实测结果**：26 measured / 1 probe（A-05 需网络探测）/ 3 fallback（A-01、A-03、L-03）/ 8 llm。
- **首次暴露的真实缺口**（此前恒报 FALLBACK 而沉默）：I-08 盲区消号率 0.00、IGI-01 主题覆盖率 0.33、IGI-05 关键断言核验率 0.47、IGI-07 摘要合规率 0.70、IGI-08 信息差指数 0.75。

### b3 批次 C（部分）

- **P1-10**：新增 `prompt_consistency_check.py`（PC-01 注册表一致 / PC-02 去复述 / PC-03 周期模板齐备）；`template-registry.md` 补登 `competitive-intelligence/dubai`、`industry-research/dubai`（修 C-11）；7 份 business-config 复述段改为指针。
- **P1-12**：`pipeline_manifest.json` G8 `checks` 由 `[]` 改为 `["perf_monitor"]`（运维 / 告警校验不再空转）。
- **P1-13**：新增 `model_contract_check.py`（MC-01..05，DC-07）；`valuation` 结果补 `assumptions` 字段（契约完整）。

### b4 批次 D（部分）

- **P2-3**：`prompt-generic-base.md` 第八节补「执行xx报告」触发词与 PCE 指针。
- **P2-4**：类型注册表同步（由 PC-01 承载）。
- **P2-8**：`engine/vocabulary/README.md` 新增「七·补 术语策略」。
- **P2-2**：核实无漂移（`reports/legacy/`、`sources/legacy/` 均存在，`check_links` 通过）。
  > **b6 纠正**：该结论有误——`reports/legacy/` 自 2026-11-17（57d1728）起即为空缺，仅 `sources/legacy/` 存在；文档漂移已于 b6 修正（见下）。

### b6 续接会话：未落地清单清零（12 P1 + 4 P2）

> 续接会话 `67312f84`（「继续执行未完成全部任务」）；分支 `task/p1-remaining-67312f84`；任务计划四件套（slug `p1-remaining`，工件已于 2026-11-23 清理）。

| 项 | 交付 | PR | 关键证据 |
|---|---|---|---|
| P1-1 | 摘要越级修正 | #61（启动批次） | apartment monthly / quarterly 共 2 处历史 `[W]` 消除 |
| P1-2 | 证据强度一致性 + DC-08 | #63 | `decision_hub_check.dc08_strength`；台账 ↔ 正文强度一致 |
| P1-3 | 「假设乘积」标注治理 | #67 | ID-04 扩展「自算须标假设乘积+区间」 |
| P1-4 | 行动项阈值数值化 | #67 | DC-02 扩展「阈值须为数值/区间/日期」 |
| P1-5 | trends 决策卡补全 | #67 | `DC-ECO-TRD-W1` 五字段齐全 |
| P1-6 | 来源登记字段扩展 | #66 | R8：`verify_status=unverifiable` + `updated` |
| P1-7 | R4 关键数字逐点指针（重设计） | #74 | 块级判定；误报 **0/19**，非合规召回 4/4，语料 0 命中 |
| P1-8 | 死链真实修复 | #64 | 17 行处置台账；12 修复 / 5 误报复核 |
| P1-9 | 四主题接入就绪化 | #62 | IGI-01 由 0.33 → 1.00（6/6） |
| P1-11 | 词库规范形统一 + 缺口补录 | #69 | VD-03 清零；高频概念补录 |
| P1-14 | 数据层补薄 + raw 落仓 | #70 | 两线台账 + 3 份量化台账 + raw 官方快照（CI 10/19、IR 7/20） |
| P1-15 | hub 卡片信息区分度 | #70 | 卡片常驻类型标签 + 标题兜底 + `data-region`/`data-type` |
| P2-1 | 死代码与规范外结构处置 | #71 | 保留 2（有据）/ 迁移 1 / 修正漂移 3；**未删除任何文件**（详见 tech-debt-ledger §十） |
| P2-5 | 主题 README 治理 | #69 | 与 business-config 一致 |
| P2-6 | 审计报表增强 | #73 | `audit_tool status` 输出 IGI 八度趋势表；`igi-snapshot` + `records/igi_history.json` |
| P2-7 | 报告结构加固（核实） | #73 | 四份公寓报告 `nav-tabs` 各 7 处；`compliance_check` 0E（无代码改动） |

**新增测试**：`TestHubCardDistinguishability`、`TestTechDataLayerThin`、`TestDeadCodeCleanup`、`TestIgiTrend`、`TestR4KeyNumber`（13 项）。

**b6 续：变更收口与历史债务清理**（同日，续接会话第二轮）：

- **变更收口**：远端 6 个分支（`main` / `ci/audit` / `ci/html-sync` / `task×3`）逐条验证**全部已并入 `origin/main`**；open PR 0、stash 0、工作树 clean；本地 `main` 与任务分支均已与远端一致。
- **来源类债务清零**：R1 未登记 URL 1→0、R2 媒体转述标注 14→0、R7 机构分级 12→0、R6 死链 9→3（修复 `gitex.com` → `gitexglobal.com` 共 24 处引用、menlovc 拼写 3 处）。
- **探测口径修复**：`normalize_url` 不再小写 path（原会误判 `LBEFH3E00556ENJI` 类路径）；R6 探测集排除自引用。
- **未闭环项**：B 类 17 份为设计如此的登记管理件、E 类 9 项为宽限期登记 —— 均已逐条登记定性，无未登记债务。详见 [tech-debt-ledger.md](tech-debt-ledger.md) v1.5 §十一。

---

## 三、验收证据

- `python -m unittest discover -s engine/tests` → **583 通过 / 1 跳过 / 0 失败**（b5 时点）。
- `python engine/tools/optimization_gate.py --probe` → **0 错误 / 9 警告**（警告全部 `warn_ok` 容忍，不阻断）。
- `check_links` / `build_hub --check` / `page_build_check` / `compliance_check` / `pipeline_runner validate` 全部通过。
- 新增测试：`TestMonitoringRender`、`TestConsistency`、`TestNaming`、`TestPromptConsistency`、`TestModelContract`、`TestCoverage`。

**b6 终态（2026-11-18）**：

- `python -m unittest discover -s engine/tests` → **625 通过 / 1 跳过 / 0 失败**。
- `python engine/tools/optimization_gate.py --probe` → **0 错误 / 8 警告**。
- 专项门禁全绿：`validate` / `validate_layout` / `check_links` / `page_build_check`（12 页 0E0W）/ `compliance_check` / `classify_reports` / `lint_reports`（10/10）/ `build_hub --check` / `pipeline_runner validate`（9 节点 / 9 门禁 / 2 闭环）。
- `audit_tool.py status` 输出 IGI 八度趋势表（基线 gate-period 2026-12：IGI-08 = 0.8366）。

---

## 四、未落地清单（诚实登记）

> **b6 状态：以下 16 项已全部落地**（逐项证据见 §二·b6）。

**P1（12 项）**：P1-1 摘要越级修正（apartment monthly / quarterly 共 2 处历史 `[W]`）、P1-2 证据强度一致性 + DC-08、P1-3 「假设乘积」标注治理、P1-4 行动项阈值数值化、P1-5 trends 决策卡补全 / 豁免、P1-6 来源登记字段扩展（`unverifiable` / `updated`）、P1-7 R4 逐点指针（块级抽样误报率远高于 5%，需重新设计）、P1-8 死链真实修复、P1-9 四主题就绪化、P1-11 词库规范形统一 + 缺口补录、P1-14 数据层补薄 + raw 落仓、P1-15 hub 卡片信息区分度。

**P2（4 项）**：P2-1 死代码清理（删除 / 迁移，需授权）、P2-5 主题 README 治理、P2-6 审计报表增强、P2-7 报告结构加固（核实已基本满足：baseline 属规范豁免，`compliance_check` 0E）。

**两项处置与字面不同，需登记**：

- **P2-1 未删除任何文件**——三处候选中两处有明确保留依据（`build_registry_v1.py` 是 tracked xlsx 生产者；`sources/legacy/` 为文档化存档），一处迁入 `sources/archives/`；仅修正真实文档漂移 3 处。详见 `tech-debt-ledger.md` §十。
- **P2-2 原结论「两 legacy 目录均存在」有误**——`reports/legacy/` 自 2026-11-17 起空缺（有意清理，tech-debt-ledger B12–B14 closed），仅 `sources/legacy/` 存在；已在 b6 修正文档指向。

---

## 五、风险与后续

- **R-1 度量接线首曝不达标**：`metric_audit` 由「恒 FALLBACK」变为真实判定，首次出现 9 项不达标——**预期且必要**（不达标即暴露真实缺口）。建议下一周期评估是否将结构性项转 `[E]`。
- **R-2 A-05 需网络探测**：链接可达率依赖 `source_check --probe`，未探测时显式标 `probe`，不伪造。
- **R-3 后续优先级建议**：P1-9（四主题就绪化，直接提升 IGI-01）→ P1-2（DC-08，质量可靠）→ P1-8（死链）→ P1-6（登记字段）。
