# 遗留任务台账（TECH-DEBT-LEDGER v1.3）

> **状态**：现行台账
> **定位**：集中登记并跟踪**非阻断**遗留项（`[W]` 警告与登记管理件），保证可追溯、可跟进、不阻塞主流程。
> **口径来源**：[page-build-governance.md](../docs/page-build-governance.md) §三（`[W]` 记录不阻断）；`engine/audit/review-workflow.md`（四环节）；`engine/audit/scripts/audit_tool.py`（登记管理）；`monitoring-common-spec.md` §3（列宽两种合法写法）。
> **优先级**：P0 阻断（本台账不含）｜P1 高｜P2 中｜P3 低。
> **状态机**：`open → in_progress → closed`；暂缓用 `deferred`。
> **复核节奏**：每月 content-update 对账；每季度末全面盘点一次。
> **最后更新**：2026-11-16（v1.3 按实跑全量刷新）

---

## 一、总览

| 类别 | 数量 | 优先级 | 状态 | 处置口径 |
|---|---|---|---|---|
| A 类 · lint 表格规范警告 | 86 项 / 4 份报告 | P2 | **closed（已修复）** | 已批量修复（2026-11-15），lint 归零（12/12 合格） |
| B 类 · 登记件（audit-doc 14 + archived 3） | 17 份 | P3 | open / closed（留存·冻结） | 登记管理（设计如此），维护责任已指定 |
| C 类 · 研究内核门禁（历史报告缺内核项） | 0 项 | P2 | **closed（已清零）** | 复跑 `research_kernel_check --gate-period 2026-12` exit 0 |
| D 类 · 来源登记 / 分级（R1 / R2 / R7） | 0 项 | P2 | **closed（已清零）** | 复跑 `source_check --gate-period 2027-01`（无探测）exit 0 |
| E 类 · 来源 R6 探测死链 / 可疑（宽限期） | 7 项 / 7 份报告 | P3 | open（宽限期登记） | `source-gate-period=2027-01` 前不追溯；登记跟踪 |
| **合计（未闭环）** | **24 项** | — | — | **全部非阻断**（B 类为登记管理件、E 类为宽限期探测项） |

---

## 二、A 类明细：lint 表格规范警告（已闭环）

**定性结论（2026-11-15 核验）**：86 项全部为 `[W]` 非阻断警告，均非变更引入（跨提交比对稳定为 86）。性质为两类既有「列宽声明规范」缺口（缺 `class="fixed"` / 多列表头缺列宽）。

**修复执行（2026-11-15）**：`engine/tools/restyle_reports.py --fix-tables` 批量为 4 份报告全部表格补 `class="fixed"`，列宽取 `max(原 px 宽, 表头内容需求宽)`；`lint_reports.py` 由 86 警告转为**全部合格**（12/12）。修复严格限于 `<table>` / `<th>` 标签，正文与 `<style>` 块零改动；4 份报告按「不可回退」要求追加复核留痕并由 CI 重走四环节。

| ID | 报告 | 警告数 | 首现提交 | 状态 |
|---|---|---|---|---|
| A1 | `content/economy/dubai/apartment/reports/2026-Q3_quarterly.html` | 50 | `5256ba9` | closed |
| A2 | `content/economy/dubai/apartment/reports/2026_annual.html` | 23 | `5256ba9` | closed |
| A3 | `content/economy/real-estate/dubai/market-sizing/reports/2026-12_baseline_report.html` | 12 | `fdb3b10` | closed |
| A4 | `content/economy/real-estate/dubai/policy-analysis/reports/2026-12_baseline_report.html` | 1 | `fdb3b10` | closed |

> **为何用 px 而非百分比**：`table-layout:fixed` + 百分比会把宽表锁死在容器宽度，nowrap 表头溢出；px 宽度之和超过容器时表格自动撑开，由 `.tblwrap{overflow-x:auto}` 横向滚动。`monitoring-common-spec.md` §3 已修订为认可两种列宽写法。

---

## 三、B 类明细：登记件（17 份，仅登记管理）

**定性结论**：登记件在 `engine/audit/records/audit_registry.json` 中 `stages` 全为 `false`、`status=draft`；`audit_tool.py` 四环节仅作用于 `category == "report"`，其余登记件按设计为「**登记管理，不适用完整四环节**」。**现状符合设计，无需补走四环节。**

| ID | 登记件 | 类别 | 维护责任 / 处置 | 状态 |
|---|---|---|---|---|
| B01 | `blind-spot-ledger.md` | audit-doc | 研究负责人；KPI-5 机制月度复盘 | open |
| B02 | `compliance-audit.md` | audit-doc | CI 每周定时维护自动重跑（`compliance_check --audit`） | open |
| B03 | `data-acquisition-checklist.md` | audit-doc | 数据采集；随采集流程维护 | open |
| B04 | `dead-code-cleanup-2026-11-14.md` | audit-doc | 时点报告；留存备查，不修改 | closed（留存） |
| B05 | `framework-diagnostic-2026-11-14.md` | audit-doc | 时点诊断；留存备查，不修改 | closed（留存） |
| B06 | `quality-audit-2026-11-14.md` | audit-doc | 下一轮质量巡检（`engine/quality/`）对照 | open |
| B07 | `quant-implementation-completion-report-2026-11-14.md` | audit-doc | 时点报告；留存备查，不修改 | closed（留存） |
| B08 | `quant-system-optimization-plan-2026-11-14.md` | audit-doc | 量化体系迭代维护 | open |
| B09 | `release-calendar.md` | audit-doc | 研究负责人；每季度复核「下次预期窗口」 | open |
| B10 | `system-optimization-plan-2026-11-15.md` | audit-doc | 质量管控体系迭代维护 | open |
| B11 | `pipeline-integration-review-2026-11-15.md` | audit-doc | 时点审查；留存备查 | closed（留存） |
| B12 | `content/tech/trends/global/reports/legacy/ai-agent/2026-11-13_weekly.html` | archived | 冻结保管，不修改 | closed（冻结） |
| B13 | `content/tech/trends/global/reports/legacy/ai-security/2026-11-13_weekly.html` | archived | 冻结保管，不修改 | closed（冻结） |
| B14 | `content/tech/trends/global/reports/legacy/ai-security/2026-11-14_weekly.html` | archived | 冻结保管，不修改 | closed（冻结） |
| B15 | `tech-debt-ledger.md`（本台账） | audit-doc | 规范所有者；季度盘点 | open |
| B16 | `l3-deep-review-2026-11-16.md` | audit-doc | 时点深度复核；留存备查 | closed（留存） |
| B17 | `cicd-alignment-audit-2026-11-16.md` | audit-doc | 时点对齐校验；留存备查 | closed（留存） |

---

## 四、C 类明细：研究内核门禁（已清零）

**来源**：`engine/tools/research_kernel_check.py --gate-period 2026-12`（CI「研究内核质量门禁」）。

**复跑结论（2026-11-16）**：`研究内核门禁通过：全部新报告四项内核项齐全`（exit 0）。原 5 项历史报告缺口（周期定位 / 传导量化 / 政策入模 / 盲区列示）已随 `35a5f9f` 全面重生成补齐，**C 类清零**。

| ID | 报告 | 周期 | 原缺失内核项 | 状态 |
|---|---|---|---|---|
| C1 | `content/economy/dubai/apartment/reports/2026-11_baseline_report.html` | 2026-11 | 周期定位、传导量化、政策入模 | closed |
| C2 | `content/economy/dubai/apartment/reports/2026-Q3_quarterly.html` | 2026-Q3 | 周期定位、传导量化、政策入模 | closed |
| C3 | `content/economy/global/trends/reports/2026-11-13_weekly.html` | 2026-11-13 | 传导量化、政策入模、盲区列示 | closed |
| C4 | `content/tech/security/dubai/reports/2026-11_baseline_report.html` | 2026-11 | 周期定位、传导量化、政策入模、盲区列示 | closed |
| C5 | `content/tech/trends/global/reports/2026-11-13_weekly.html` | 2026-11-13 | 传导量化、盲区列示 | closed |

---

## 五、D 类明细：来源登记 / 分级（已清零）

**来源**：`engine/tools/source_check.py --gate-period 2027-01`（无探测模式，CI「来源登记前置校验」）。

**复跑结论（2026-11-16）**：`来源校验通过：全部报告来源登记合规`（exit 0）。原 R1 / R2 / R7 缺口已全部消除，**D 类清零**。

| ID | 报告 | 警告构成 | 状态 |
|---|---|---|---|
| D01 | `content/economy/dubai/apartment/reports/2026-11_baseline_report.html` | R2 ×1 | closed |
| D02 | `content/economy/dubai/apartment/reports/2026-Q3_quarterly.html` | R2 ×3 | closed |
| D03 | `content/economy/dubai/apartment/reports/2026_annual.html` | R2 ×5 | closed |
| D04 | `content/economy/real-estate/dubai/market-sizing/reports/2026-12_baseline_report.html` | R1 ×1（登记为空） | closed |
| D05 | `content/economy/global/decision-hub/reports/2026-12_baseline_report.html` | R1 ×1（登记为空） | closed（规则误报，`SOURCE_STRATEGY=synthesis_only` 豁免） |
| D06 | `content/economy/global/trends/reports/2026-11-13_weekly.html` | R2 ×4 | closed |
| D07 | `content/tech/competitive-intelligence/dubai/reports/2026-12_baseline_report.html` | R2 ×2 | closed |
| D08 | `content/tech/industry-research/dubai/reports/2026-12_baseline_report.html` | R1 ×1 + R7 ×1 | closed |
| D09 | `content/tech/security/dubai/reports/2026-11_baseline_report.html` | R1 ×1（登记为空） | closed |

- **R1 登记覆盖**：原 5 项已清零——4 项随 `35a5f9f` 重生成补齐登记；decision-hub 为无外部来源的综合层，属规则误报，已按 `SOURCE_STRATEGY=synthesis_only` 豁免。
- **R2 分级合规**：tier=3 / tier=4 来源的邻近标注缺失（原 15 项），已随 `35a5f9f` 重生成修复。
- **R7 机构分级**：原 1 项 business-config 来源优先级与 `institution_tiers.json` 主数据不一致，已随 `35a5f9f` 修复。

---

## 六、E 类明细：来源 R6 探测死链 / 可疑（宽限期登记）

**来源**：`engine/tools/source_check.py --probe --probe-lenient --gate-period 2027-01`（实时 URL 探测）。

**定性**：R6 为**来源可达性探测**（404/410/451 判死链；超时/反爬判可疑需人工复核）。所有命中报告均早于 `source-gate-period=2027-01`，属**宽限期**内既有缺口，按设计**历史报告不追溯改写**（保持已审计产物冻结）。**不阻断**（`source_check` 退出码 2 → 统一门禁 `[W]`）。

| ID | 报告 | 警告 | 示例 |
|---|---|---|---|
| E1 | `content/economy/dubai/apartment/reports/2026-11_baseline_report.html` | 死链 ×3 | centralbank.ae 统计公报 |
| E2 | `content/economy/dubai/apartment/reports/2026-11_monthly.html` | 可疑 ×1 | cavendishmaxwell.com |
| E3 | `content/economy/dubai/apartment/reports/2026-Q3_quarterly.html` | 死链 ×3 | centralbank.ae 统计公报 |
| E4 | `content/economy/dubai/apartment/reports/2026_annual.html` | 死链 ×4 | centralbank.ae 统计公报 |
| E5 | `content/economy/global/trends/reports/2026-11-13_weekly.html` | 可疑 ×12 | gov.cn 联播 |
| E6 | `content/tech/competitive-intelligence/dubai/reports/2026-12_baseline_report.html` | 死链 ×2 | practiceguides.chambers.com |
| E7 | `content/tech/trends/global/reports/2026-11-13_weekly.html` | 死链 ×2 | microsoft.com/security/blog |

**处置**：登记跟踪；随下一期报告按来源登记机制使用可归档 URL（优先官方统计/机构一手页），并在宽限期结束（2027-01）后纳入强制校验。

---

## 七、优先级标准

| 级别 | 含义 | 判据 | 本台账适用 |
|---|---|---|---|
| P0 | 阻断 | `[E]`，CI exit 1，必须立即修复 | 无 |
| P1 | 高 | 影响主流程 / 合规，需本迭代处理 | 无 |
| P2 | 中 | 非阻断但有规模、影响可读性 / 可追溯，宜在既有自动化窗口批量处理 | 无（A/C/D 均已闭环） |
| P3 | 低 | 非阻断，按既有机制维护或仅确认留存 | B01–B17、E1–E7 |

---

## 八、时间节点与责任归属

| 节点 | 时间 | 内容 | 责任归属 |
|---|---|---|---|
| 每周自动 | 周一 02:30 UTC | lint / 合规 / 内核 / 来源登记复跑，警告数对账 | CI（`scheduled-maintenance.yml`） |
| 每周自动 | 周一 09:00（Asia/Shanghai） | L3 深度复核顺带核对遗留状态 | Agent 周期复核 |
| 每月 | 1 日 03:17 UTC | 对账 B / E 类状态 | CI + 规范所有者（`content-update.yml`） |
| 2026-12 季度盘点 | 季度末 | 确认 B 类维护责任与冻结状态 | 规范所有者（研究负责人） |
| 2027-01（宽限期结束） | gate-period 生效 | E 类 R6 转强制校验，新报告不得带死链 | 业务线作者 + CI |

**责任角色**（对齐 `page-build-governance.md` §一）：规范所有者批准 `[W]→[E]` 升级与口径裁定；业务线作者执行修复与新报告补齐；生成器（`engine/tools/`）提供批量修复能力；CI 自动重走四环节与标识注入；定时维护负责结构 / 校验 / 归档 / 索引 / hub / 活跃度。

---

## 九、复核与变更记录

| 日期 | 变更 | 说明 |
|---|---|---|
| 2026-11-15 | 建立台账（v1.0） | 核验 86 项 lint 警告 + 登记件口径确认；定性全部非阻断 |
| 2026-11-15 | A 类修复完成 | `--fix-tables` 批量修复 86 项；lint 归零；4 份报告追加复核留痕 |
| 2026-11-15 | 口径修正 | 列宽由百分比改为 `max(原 px, 表头需求宽)` px 口径，消除宽表表头溢出 |
| 2026-11-15 | 升版 v1.1 | 新增 C 类（研究内核）、D 类（来源登记）；B 类补维护责任 |
| 2026-11-16 | 升版 v1.2 | 按实跑刷新：C 类 6→5 项；D 类由 R1 11 项扩为 R1/R2/R7 20 项 / 9 份报告；B 类补 `system-optimization-plan`、`pipeline-integration-review` 与本台账 |
| 2026-11-16 | D05 销号 | decision-hub 为无外部来源的综合层，R1「登记为空」系规则误报；business-config 声明 `SOURCE_STRATEGY=synthesis_only`，`source_check` 据此豁免 |
| 2026-11-16 | 升版 v1.3 | **全量复跑刷新**：C 类 5→0（closed）；D 类 20→0（closed）；B 类 15→17（补 `l3-deep-review`、`cicd-alignment-audit`）；新增 E 类（R6 宽限期探测 7 项）；总览由 40 项修正为 24 项 |

---

## 附录：核验证据（2026-11-16）

**1. lint 警告数**：`lint 通过：12 份报告全部合格`（exit 0）。

**2. 登记件状态**（`python engine/audit/scripts/audit_tool.py status`）：正式报告 12/12 `audited`（4/4 审查链）；audit-doc 14 份、archived 3 份为 `draft`（登记管理，不适用完整四环节）。

**3. C 类证据**（`python engine/tools/research_kernel_check.py --gate-period 2026-12`）：`研究内核门禁通过：全部新报告四项内核项齐全`（exit 0）。

**4. D 类证据**（`python engine/tools/source_check.py --gate-period 2027-01`）：`来源校验通过：全部报告来源登记合规`（exit 0）。

**5. E 类证据**（`python engine/tools/source_check.py --probe --probe-lenient --gate-period 2027-01`）：`来源校验存在 7 项警告（无错误，不阻断）`（exit 2）。

**6. 工具口径**：`audit_tool.py::cmd_run` 仅处理 `category == "report"`；`cmd_accept` 输出「其他登记（归档 / 审计文档）：登记管理，不适用完整四环节」；ci.yml 中研究内核 / 来源登记前置校验按退出码 2 → `::warning::`、exit 0（不阻断）。
