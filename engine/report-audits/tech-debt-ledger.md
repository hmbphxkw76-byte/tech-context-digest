# 遗留任务台账（TECH-DEBT-LEDGER v1.5）

> **状态**：现行台账
> **定位**：集中登记并跟踪**非阻断**遗留项（`[W]` 警告与登记管理件），保证可追溯、可跟进、不阻塞主流程。
> **口径来源**：[page-build-governance.md](../docs/page-build-governance.md) §三（`[W]` 记录不阻断）；`engine/audit/review-workflow.md`（四环节）；`engine/audit/scripts/audit_tool.py`（登记管理）；`monitoring-common-spec.md` §3（列宽两种合法写法）。
> **优先级**：P0 阻断（本台账不含）｜P1 高｜P2 中｜P3 低。
> **状态机**：`open → in_progress → closed`；暂缓用 `deferred`。
> **复核节奏**：每月 content-update 对账；每季度末全面盘点一次。
> **最后更新**：2026-11-19（v1.6 新增 F 类：静态检查 baseline 债务，只拦新增）

---

## 一、总览

| 类别 | 数量 | 优先级 | 状态 | 处置口径 |
|---|---|---|---|---|
| A 类 · lint 表格规范警告 | 86 项 / 4 份报告 | P2 | **closed（已修复）** | 已批量修复（2026-11-15），lint 归零（12/12 合格） |
| B 类 · 登记件（audit-doc 14 + archived 3） | 17 份 | P3 | open / closed（留存·冻结） | 登记管理（设计如此），维护责任已指定 |
| C 类 · 研究内核门禁（历史报告缺内核项） | 0 项 | P2 | **closed（已清零）** | 复跑 `research_kernel_check --gate-period 2026-12` exit 0 |
| D 类 · 来源登记 / 分级（R1 / R2 / R7） | 0 项 | P2 | **closed（已清零）** | 复跑 `source_check --gate-period 2027-01`（无探测）exit 0 |
| E 类 · 来源 R6 探测死链 / 可疑（宽限期） | 9 项 / 9 份报告（死链 3 / 可疑 72） | P3 | open（宽限期登记） | `source-gate-period=2027-01` 前不追溯；其中 3 处已修复（见 §十一） |
| F 类 · 静态检查 baseline（ruff / mypy） | 95 项（ruff 69 / mypy 26） | P2 | open（baseline 只拦新增） | 已入 `engine/quality/lint-baseline.json`；新增即 `[E]`（见 §十二） |
| **合计（未闭环）** | **119 项** | — | — | **全部非阻断**（B 类为登记管理件、E 类为宽限期探测项、F 类为 baseline 额度内） |

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
| B12 | 历史周报快照（ai-agent 2026-11-13，原 `reports/legacy/ai-agent/2026-11-13_weekly.html`） | archived | 2026-11-17 全量重生成时清理 | closed（已清理） |
| B13 | 历史周报快照（ai-security 2026-11-13，原 `reports/legacy/ai-security/2026-11-13_weekly.html`） | archived | 2026-11-17 全量重生成时清理 | closed（已清理） |
| B14 | 历史周报快照（ai-security 2026-11-14，原 `reports/legacy/ai-security/2026-11-14_weekly.html`） | archived | 2026-11-17 全量重生成时清理 | closed（已清理） |
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
| C3 | `content/economy/trends/reports/2026-11-13_weekly.html` | 2026-11-13 | 传导量化、政策入模、盲区列示 | closed |
| C4 | `content/tech/security/dubai/reports/2026-11_baseline_report.html` | 2026-11 | 周期定位、传导量化、政策入模、盲区列示 | closed |
| C5 | `content/tech/weekly-roundup/reports/2026-11-13_weekly.html` | 2026-11-13 | 传导量化、盲区列示 | closed |

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
| D05 | `content/economy/insight/reports/2026-12_baseline_report.html` | R1 ×1（登记为空） | closed（规则误报，`SOURCE_STRATEGY=synthesis_only` 豁免） |
| D06 | `content/economy/trends/reports/2026-11-13_weekly.html` | R2 ×4 | closed |
| D07 | `content/tech/competitive-intelligence/dubai/reports/2026-12_baseline_report.html` | R2 ×2 | closed |
| D08 | `content/tech/industry-research/dubai/reports/2026-12_baseline_report.html` | R1 ×1 + R7 ×1 | closed |
| D09 | `content/tech/security/dubai/reports/2026-11_baseline_report.html` | R1 ×1（登记为空） | closed |

- **R1 登记覆盖**：原 5 项已清零——4 项随 `35a5f9f` 重生成补齐登记；decision-hub 为无外部来源的综合层，属规则误报，已按 `SOURCE_STRATEGY=synthesis_only` 豁免。
- **R2 分级合规**：tier=3 / tier=4 来源的邻近标注缺失（原 15 项），已随 `35a5f9f` 重生成修复。
- **R7 机构分级**：原 1 项 business-config 来源优先级与 `institution_tiers.json` 主数据不一致，已随 `35a5f9f` 修复。

---

## 六、E 类明细：来源 R6 探测死链 / 可疑（宽限期登记）

**来源**：`engine/tools/source_check.py --probe --probe-lenient --gate-period 2027-01`（实时 URL 探测）。

**定性**：R6 为**来源可达性探测**（404/410/451 判死链；超时 / 反爬判可疑需人工复核）。所有命中报告均早于 `source-gate-period=2027-01`，属**宽限期**内既有缺口，按设计**历史报告不追溯改写**（保持已审计产物冻结）。**不阻断**（`source_check` 退出码 2 → 统一门禁 `[W]`）。

**本环境探测局限（重要）**：本机对多数海外主域不可达（`sec.gov`、`openai.com`、`g42.ai`、`nvlpubs.nist.gov` 整站等报不可达，而同主域可达），故**「可疑」不等于链接腐烂**；仅「死链」（明确 HTTP 错误）可作为修复依据，且需主域交叉验证。

### 2026-11-18 复测（续接会话）

| 报告 | 死链 | 可疑 | 处置 |
|---|---|---|---|
| `content/economy/dubai/apartment/reports/2026-11_baseline_report.html` | 0 | 5 | 保留登记（环境不可达） |
| `content/economy/dubai/apartment/reports/2026-11_monthly.html` | 0 | 7 | 保留登记 |
| `content/economy/dubai/apartment/reports/2026-Q3_quarterly.html` | 0 | 2 | 保留登记 |
| `content/economy/dubai/apartment/reports/2026_annual.html` | 0 | 10 | 保留登记 |
| `content/economy/trends/reports/2026-11-13_weekly.html` | 0 | 11 | 保留登记 |
| `content/tech/competitive-intelligence/dubai/reports/2026-12_baseline_report.html` | 0（原 2） | 20 | **已修复**：`gitex.com` → `gitexglobal.com`（已验证可达） |
| `content/tech/industry-research/dubai/reports/2026-12_baseline_report.html` | 0（原 3） | 16 | **已修复**：同上（2 处）；`gisec.ae` 转可疑 |
| `content/tech/security/dubai/reports/2026-11_baseline_report.html` | 2 | 0 | 待人工复核（见下） |
| `content/tech/weekly-roundup/reports/2026-11-13_weekly.html` | 1 | 11 | 待人工复核（见下） |

**待人工复核死链（3 个 URL）**：

| URL | 证据 | 结论 |
|---|---|---|
| `https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf` | 主域 `nist.gov` 可达，`nvlpubs.nist.gov` 整站报死链；大小写两种写法与 `csrc.nist.gov/pubs/ai/100/1/final` 变体均不可达 | **疑环境干扰，非链接腐烂**；保留登记，待网络正常时复核 |
| `https://u.ae/en/information-and-services/jobs/employment-in-the-private-sector/emiratis-employment-in-private-sector` | 主域 `u.ae` 可达，具体路径报死链；缩短路径亦不可达 | 页面可能已迁移；保留登记，待复核 |
| `https://www.163.com/dy/article/LBEFH3E00556ENJI.html` | 主域 `www.163.com` 可达，文章页报死链（大小写两种写法均不可达） | 文章页确已失效；保留登记，不删除来源条目 |

**稳定性复验（同日多轮）**：同一 URL 在连续多轮探测中会在「可达 / 死链」间摆动 —— 实例 `https://genai.owasp.org/agentic-top-10/` 首轮判可达、随后两轮判死链。故本环境下「死链」判定**不足以作为删除或替换依据**；上表 3 项均**保留登记**，待网络条件稳定时复核。

**处置**：登记跟踪；随下一期报告按来源登记机制使用可归档 URL（优先官方统计 / 机构一手页），并在宽限期结束（2027-01）后纳入强制校验。

---

## 七、优先级标准

| 级别 | 含义 | 判据 | 本台账适用 |
|---|---|---|---|
| P0 | 阻断 | `[E]`，CI exit 1，必须立即修复 | 无 |
| P1 | 高 | 影响主流程 / 合规，需本迭代处理 | 无 |
| P2 | 中 | 非阻断但有规模、影响可读性 / 可追溯，宜在既有自动化窗口批量处理 | 无（A/C/D 均已闭环） |
| P3 | 低 | 非阻断，按既有机制维护或仅确认留存 | B01–B17、E 类（9 项） |

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
| 2026-11-18 | 新增 §十 | P2-1（C-15）逐条人工核验处置：保留 2 处 / 迁移 1 处 / 修正文档漂移 3 处；**未删除任何文件**（候选均存在保留或迁移依据） |
| 2026-11-18 | 升版 v1.5 + 新增 §十一 | 续接会话历史债务清理：变更全量收口；R1/R2/R7 清零；R6 修复 3 处死链（gitex.com → gitexglobal.com、menlovc URL 拼写）；E 类按 2026-11-18 实跑复测刷新 |
| 2026-11-19 | 升版 v1.6 + 新增 §十二 | F 类静态检查 baseline：ruff 97→69、mypy 45→26，剩余入 baseline（只拦新增）；A-05 探测接入定时维护 |

---

## 十、C-15 死代码与规范外结构处置（P2-1，2026-11-18）

**来源**：`goal-alignment-optimization-plan-2026-11-18.md` C-15 / P2-1 / P2-2。逐条人工核验后处置如下——**未删除任何文件**：三处候选中两处有明确保留依据，一处迁入规范归档位。

| 候选 | 核验结论 | 处置 | 状态 |
|---|---|---|---|
| `content/economy/dubai/apartment/script/build_registry_v1.py` | **保留**。该脚本是 tracked 交付物 `dubai_apartment_indicator_registry_2026-11.xlsx` 的生产者，`build_registry_v2.py` 以其输出为输入；`dead-code-cleanup-2026-11-14.md` §三亦明示保留（「可复用于下一年度重置」）。删除将破坏「生成物确定性可重放」 | 关闭 C-15「无引用」判定（误报） | closed |
| 原 `followup/`（现 `content/economy/trends/sources/archives/`） | `followup/` 不在 `structure-and-naming-spec.md` §4.4 目标结构内，属规范外；文档无引用 | **迁移**至 `content/economy/trends/sources/archives/2026-11-13_followup-execution.md`，撤销 `followup/` | closed |
| `content/tech/weekly-roundup/sources/legacy/` | **保留**。`operations-guide.md` §0、`archive_reports.py` 头注释、`business-config.md` 版本记录均明示为存档（不参与轮转） | 关闭 C-15「规范外结构」判定（误报） | closed |
| `weekly-roundup/README.md` 指向不存在的 `reports/legacy/` | **真实漂移**。`reports/legacy/` 已由 57d1728 清理（B12–B14 closed），仅 md 源稿留存 | 修正 README / `operations-guide.md` / `ai_trend_ledger.md` 三处指向为实际状态 | closed |

**验证**：`validate_layout` / `validate` / `check_links` 均通过；`followup/` 已不存在，`sources/archives/` 入册；`optimization_gate --probe` 0 错误。

**附带纠正**：b5（`goal-alignment-batch-progress-2026-11-18.md`）§四称 P2-2「两 legacy 目录均存在」与事实不符——`reports/legacy/` 自 2026-11-17 起即为空缺，已在规划文档 P2-2 行更正。

---

## 十一、续接会话历史债务清理（2026-11-18）

**触发**：续接会话要求「所有会话修改完全合并 / 提交 / 推送，无历史债务；数据完整无缺前提下执行清理」。

### 11.1 变更收口（全量核查）

| 项 | 结果 |
|---|---|
| 远端分支（main / ci/audit / ci/html-sync / task×3） | **全部已并入 `origin/main`**（`git merge-base --is-ancestor` 逐条验证） |
| open PR | **0** |
| stash | **0** |
| 工作树 | clean |
| 本地分支与远端一致性 | `main`、`task/p1-remaining-67312f84` 均已同步（后者补推 1 个本地合并提交） |

### 11.2 来源类债务（D 类 R1/R2/R7 + E 类 R6）

| 项 | 清理前 | 清理后 | 处置 |
|---|---|---|---|
| R1 未登记 URL | 1 | **0** | 定位到 weekly-roundup 报告正文 URL 拼写与登记不一致，修正为登记形态 |
| R2 媒体转述缺『需核实原文』 | 14 | **0** | weekly-roundup ⑷ 媒体转述清单 12 条逐条补标；apartment baseline 4 处补标 |
| R7 机构未录入分级主数据 | 12 | **0** | `institution_tiers.json` 补 `Digital Dubai`、`Dubai Pulse / DLD` 别名（不新增重复机构） |
| R6 死链 | 4 份报告 / 9 个 URL | **2 份报告 / 3 个 URL** | 修复 6 个：全仓 24 处 `gitex.com` 引用统一为 `gitexglobal.com`（已验证可达）、menlovc 路径拼写 3 处；余 3 个待人工复核 |
| R6 可疑（网络不可达） | 5 份报告 / 35 个 URL | 7 份报告 / 72 个 URL | **未处理**：本环境对多数海外主域不可达，探测数受网络波动影响（死链转可疑属正常涨落）；已登记为环境局限，不作链接腐烂认定 |

**同时修复的探测口径缺陷**（避免后续误判）：

- `normalize_url` 不再小写 **path**（原整串小写会把 `LBEFH3E00556ENJI` 一类区分大小写的路径误判为死链）。
- R6 探测集**排除自引用**（本仓库自身 GitHub 链接不是外部来源）。

### 11.3 未闭环项的最终定性

| 类 | 数量 | 定性 |
|---|---|---|
| B 类登记件 | 17 份（8 open / 9 closed） | **设计如此**，非待办：登记管理件（审计报告 / 规划 / 日历 / 本台账），维护责任已指定；**不得为「清零」而关闭**（B15 即本台账自身） |
| E 类 | 9 项（死链 3 / 可疑 72） | **宽限期登记**（`source-gate-period=2027-01` 前不追溯、不阻断）；3 个死链已逐条给出核验证据 |
| A/C/D 类 | 0 | 已闭环 |

**结论**：本 repo **不存在未登记的历史债务**——所有残留均已在本台账逐条登记并给出定性、证据与责任归属；其中可在「数据完整无缺」前提下安全闭环的部分（R1/R2/R7 与 6 处死链）已全部闭环。

---

## 十二、F 类：静态检查 baseline 债务（2026-11-19）

**来源**：`engine/tools/static_check.py`（ruff / mypy 适配层）+ 统一门禁 `ruff` / `mypy` 项。

**定性**：均为**代码风格与类型注解**类非阻断发现，非变更引入、跨提交稳定。处置策略（11-19 方案 P1-5）：**修高价值 + 其余入 baseline，只拦新增**。

| 工具 | 初始 | 已修 | baseline | 剩余构成 |
|---|---|---|---|---|
| ruff | 97 | 28 | 69 | E702 分号多语句 69（风格，逐行拆分收益低） |
| mypy | 45 | 19 | 26 | `semantic_diff` 7 / `perf_bench` 11 / `transmission` 4 / `pipeline_runner` 2 / `stress_test` 1 / 其他 1（涉及重构，风险高） |

**已修明细（高价值）**：ruff 安全自动修复（导入排序 / 未用导入 13）+ 手工（歧义变量名 `l` 11、未用局部 2）；mypy 类型注解 / None 守卫 / 变量遮蔽 19（含 `metric_coverage`、`model_contract_check`、`task_plan`、`validate_layout`、`repo_sync`、`branch_naming`）。

**baseline 机制**：`engine/quality/lint-baseline.json` 按 `(path, code)` **计数**（不看行号，避免漂移）；`static_check.py` 比对当前与 baseline：额度内 → `[W]`（exit 2，不阻断），超额度 → `[E]`（exit 1，阻断）。更新 baseline 需显式 `static_check.py <tool> --update-baseline` 并随 PR 审核。

**A-05 探测收口**：`scheduled-maintenance.yml` 新增「A-05 链接可达率探测」步骤，`source_check.py --probe --emit engine/audit/records/link-probe.json` 定期落盘（`{probed, dead, unreachable, ok}`，无时间戳）。

**证据**：`python engine/tools/static_check.py ruff` / `mypy` 均输出「新增 0 项」，exit 2；unittest 627 通过。

---

## 附录：核验证据（2026-11-16）

**1. lint 警告数**：`lint 通过：12 份报告全部合格`（exit 0）。

**2. 登记件状态**（`python engine/audit/scripts/audit_tool.py status`）：正式报告 12/12 `audited`（4/4 审查链）；audit-doc 14 份、archived 3 份为 `draft`（登记管理，不适用完整四环节）。

**3. C 类证据**（`python engine/tools/research_kernel_check.py --gate-period 2026-12`）：`研究内核门禁通过：全部新报告四项内核项齐全`（exit 0）。

**4. D 类证据**（`python engine/tools/source_check.py --gate-period 2027-01`）：`来源校验通过：全部报告来源登记合规`（exit 0）。

**5. E 类证据**（`python engine/tools/source_check.py --probe --probe-lenient --gate-period 2027-01`）：`来源校验存在 7 项警告（无错误，不阻断）`（exit 2）。

**6. 工具口径**：`audit_tool.py::cmd_run` 仅处理 `category == "report"`；`cmd_accept` 输出「其他登记（归档 / 审计文档）：登记管理，不适用完整四环节」；ci.yml 中研究内核 / 来源登记前置校验按退出码 2 → `::warning::`、exit 0（不阻断）。
