# 内容质量评估与自动修复提示词体系（QUALITY-AUDIT）

> **定位**：对 tech-context-digest 全项目所有主题内容做**全量、可周期复跑**的质量评估，自动识别「信息混乱」并闭环修复。覆盖范围包括：全部业务线的**报告 / 提示词 / 登记册 / 词汇**，以及 `engine/templates/` 通用层与 `engine/vocabulary/` 词库；未来新增业务线 / 报告 / 词条由动态发现自动纳入，无需修改本提示词体系。
>
> **双视角**：信息获取者（该有的有没有、可不可信）× 信息接收者（读起来通不通、关联对不对）。
>
> **执行者**：AI Agent。读取 `prompts/00-orchestrator.md` 后按阶段执行；**确定性判定复用仓库既有工具链**（`engine/tools/`、`engine/vocabulary/script/`），**语义判定由 Agent 完成**。两者互补，不另起炉灶。

---

## 一、四维度与双视角映射

| 视角 | 维度 | 核心问题 | 指标数 | 主要检测层 |
|---|---|---|---|---|
| 信息获取者 | 主题完整性 | 该有的有没有 | 6 | 工具 |
| 信息获取者 | 信息准确性 | 数据 / 来源可不可信 | 5 | 混合 |
| 信息接收者 | 逻辑一致性 | 读起来通不通 | 5 | LLM |
| 信息接收者 | 内容关联性 | 关联 / 归属对不对 | 5 | 工具 + LLM |

量化指标单一事实源见 [rubric.md](./rubric.md)；混乱场景分类见 [chaos-taxonomy.md](./chaos-taxonomy.md)；修复规范见 [repair-sop.md](./repair-sop.md)。

---

## 二、闭环流程

```mermaid
flowchart LR
  A["0 备份"] --> B["1 全量盘点"]
  B --> C["2 机器判定"]
  C --> D["3 语义判定"]
  D --> E["4 定级排序"]
  E --> F["5 自动修复"]
  F --> G["6 复验回归"]
  G --> H["7 确定性报告"]
  G -->|"存在未清 P0"| F
```

- **阶段 0 备份**：所有写盘前快照（git 未提交改动 / `.bak`），保证可回滚。
- **阶段 1 盘点**：动态发现全部对象，产出 `inventory`。
- **阶段 2 机器判定**：运行既有工具，收集 `[E]` / `[W]`。
- **阶段 3 语义判定**：Agent 按 15 类场景逐项检查，产出 `findings`。
- **阶段 4 定级排序**：P0 → P1 → P2，同级别按「影响面 × 修复成本」排序。
- **阶段 5 自动修复**：按 SOP 执行，低风险直接改，高风险「备份 + 改 + 标记待复核」。
- **阶段 6 复验回归**：重跑机器判定 + 语义复评，确认无新增问题（回归）。
- **阶段 7 报告**：产出确定性 `quality-audit-<date>.md` 与结构化 manifest。

---

## 三、文件清单

| 文件 | 职责 |
|---|---|
| `README.md` | 本文件：总览、闭环、快速开始 |
| `rubric.md` | 四维 × 21 项量化指标（公式 / 阈值 / 检测层 / 数据来源） |
| `chaos-taxonomy.md` | 15 类信息混乱场景判定表 |
| `repair-sop.md` | 标准化自动修复操作规范（触发 → 动作 → 验证 → 回滚） |
| `manifest.schema.json` | 评估 / 修复 / 复验结果的结构化 schema |
| `ops-guide.md` | 周期复跑 runbook（触发方式、频率、CI 接入、告警） |
| `prompts/00-orchestrator.md` | **主控提示词**：编排全流程，可直接投喂 Agent |
| `prompts/01-inventory.md` | 阶段 1：全量动态盘点 |
| `prompts/02-evaluate.md` | 阶段 2–3：四维量化评估 |
| `prompts/03-classify.md` | 阶段 4：混乱场景分类判定 |
| `prompts/04-repair.md` | 阶段 5：自动修复执行 |
| `prompts/05-verify.md` | 阶段 6–7：复验与报告 |

---

## 四、权威源优先级（修复与冲突裁决的唯一依据）

**层内优先级**（同主题内冲突时）：

```
业务提示词 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范
```

**跨对象优先级**（跨主题 / 跨报告冲突时）：

```
官方一手 > 行业机构 > 挂牌门户 > 媒体转述
登记册 / 词汇库（结构化单一事实源）> 报告正文
business-config（业务单一事实源）> 报告正文
```

- 低权威源与高权威源冲突：**以高权威源为准**，低权威源对齐或标注「需核实原文」，不得静默择一。
- 无法裁决时：**并列呈现并标注**，列入「待复核清单」，不擅自删改。

---

## 五、覆盖范围与动态发现

| 对象 | 发现方式 | 单一事实源 |
|---|---|---|
| 业务线 | 遍历 `content/<theme>/<category>/<region>/` 下的业务目录 | `engine/tools/layout.json` |
| 报告 | 各业务线 `reports/*.html`（含 `archives/`、`sources/`、`legacy/`） | 各 `prompts/business-config.md` 落盘规则 |
| 提示词 | 各业务线 `prompts/*.md` | 各 `business-config.md` 继承声明 |
| 登记册 | 集中数据目录 `data/processed/<theme>/<维度段...>/` 下台账（xlsx / md） | `{{REGISTRY_PATH}}` |
| 通用层模板 | `engine/templates/` 根部 + 类型子目录 | `template-registry.md` |
| 词汇 | `engine/vocabulary/data/<topic>/terms.md` | `config/topics.json` |
| 类型 / 周期 | `compliance-rules.json` | `template-registry.md` 第二节 |

> **可扩展**：新增业务线只需在 `layout.json` 登记主题与维度，并在 `template-registry.md` 登记类型；本体系自动纳入，无需改动提示词。

---

## 六、快速开始（Agent 执行）

```
1. 读取 engine/quality/prompts/00-orchestrator.md
2. 按其指引依次读取 01 → 05 并执行
3. 产物：engine/report-audits/quality-audit-<YYYY-MM-DD>.md + quality-manifest.json
```

**门禁判定**：

- 通过：P0 问题数 = 0 且总体健康度 ≥ 90%。
- 不通过：存在未清 P0 → 回到阶段 5 继续修复；连续两轮无法清零 → 输出「待人工复核清单」并停止自动修复。

---

## 七、周期复跑

见 [ops-guide.md](./ops-guide.md)。要点：

- **语义层**由 Agent 周期执行（建议接入妙手 automation 或手动触发），**确定性子集**可接 `scheduled-maintenance.yml`。
- 每次运行产出确定性报告（无时间戳漂移），便于跨轮 diff 与趋势追踪。
- 新增业务线 / 报告 / 词条自动纳入。

---

## 八、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 建立双视角四维提示词体系：21 项量化指标、15 类混乱场景、自动修复 SOP、闭环流程与周期复跑 runbook |
