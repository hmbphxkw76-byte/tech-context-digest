# 跨研究线决策仪表盘 · 业务专属配置（business-config）

> **定位**：`content/economy/insight` 业务线的**单一业务事实源**：决策卡协议、场景切片、盲区优先级、读数时点与版本规则集中于此。本业务线为**跨研究线统一决策层**（不占研究编号、不落研究正文），做三件事：收敛（各研究线结论 → 标准化决策卡）、暴露（缺失事实与冲突读数）、触发（按阈值启动补缺 / 专题）。
>
> **继承声明（四层体系）**：业务提示词 = [通用基座](../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../engine/templates/monitoring-common-spec.md) × [信息分层规范](../../../../engine/templates/information-layering-spec.md) × [决策交付规范](../../../../engine/templates/decision-delivery-spec.md) × [决策仪表盘型模板](../../../../engine/templates/decision-dashboard/prompt-baseline-setup-template.md) × 本文件。冲突时以业务提示词 ＞ 本文件 ＞ 类型模板 ＞ 决策交付规范 ＞ 信息分层规范 ＞ 通用基座 ＞ 通用规范。

---

## 一、运行变量固定值

```
{{REGION}}               = 跨研究线（全球 / 迪拜）
{{TOPIC}}                = 决策仪表盘
{{REPORT_TYPE}}         = decision-dashboard
{{CADENCE}}              = 季（事件触发可插刷）
{{REGISTRY_PATH}}        = data/processed/economy/insight/decision_cards.json
{{REGISTRY_FORMAT}}      = json-decision-ledger
{{DECISION_CARDS_PATH}}  = data/processed/economy/insight/decision_cards.json
{{SLICES_PATH}}          = data/processed/economy/insight/scenario_slices.md
{{BASELINE_REPORT_PATH}} = reports/2026-12_baseline_report.html
{{READING_TIME}}         = 2026-11-15（本期读数时点）
{{REPORT_VERSION}}       = v1.0（仅核心事实修正时升级）
{{FRESHNESS_PRIORITY}}   = 最新官方页 > 上期值 > 预测值
{{SOURCE_LANGUAGE_RULE}} = 仅英文（决策卡引用事实卡片与来源登记，均英文来源）
{{SOURCE_STRATEGY}}       = synthesis_only（无外部来源的综合层；不新采数据，只收敛仓库内已文档化事实，引用走事实卡片 / 来源登记指针）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/economy/insight
```

**落盘规则**：

| 周期 | 输出路径 | 版本号 | 上期报告 |
|---|---|---|---|
| 基线 | `reports/2026-12_baseline_report.html` | v1.0（首期固定） | 无 |
| 季度 | `reports/{{YYYY-Qn}}_quarterly.html` | 仅核心事实修正时升级 | `reports/` 最近一期 |
| 事件触发 | 并入当期季度报告 | 不升级 | — |

**输出格式**：自包含 HTML（canonical 样式）。

---

## 二、受众与场景切片

| 场景 | 决策问题 | 切片内容 | 优先级 |
|---|---|---|---|
| 投资决策 | 值不值得进 / 投 / 持 | 估值区间、收益安全垫、触发条件、尾部损失 | 主场景 |
| 就业决策 | 能不能去 / 怎么去 | 供需缺口、薪酬区间、技能要求、路径与时限 | 主场景 |
| 政策制定 | 政策含义与合规应对 | 政策台账、乘数区间、影响对象矩阵、时间线 | 主场景 |

- **取消单份报告服务所有受众**：每类场景输出独立切片（报告第七节 + `data/processed/economy/insight/scenario_slices.md`），只输出该场景所需信息。
- 跨切片共享事实走事实卡片（`engine/fact_cards/`）与来源登记指针，不复述。

---

## 三、决策卡协议（结论 + 证据强度 + 触发条件 + 反向证据 + 信息充分度）

- 台账：`data/processed/economy/insight/decision_cards.json`；字段与格式见类型模板第四节。
- 证据强度：**强** = 关键事实全部已核验且双源；**中** = 主体已核验、个别部分核验；**弱** = 含推断 / 假设支撑。
- 信息充分度：**可直接决策** / **需补充 X 类信息才可决策**；缺失项指向盲区台账（`engine/report-audits/blind-spot-ledger.md`）。
- 每条决策卡至少 1 条反向证据；无则写「未发现」并说明检索范围。

---

## 四、行动协议

- 五要素缺一不可；优先级三档：**立即行动 / 持续观察 / 仅记录存档**。
- 责任角色：研究负责人 / 数据采集 / 模型负责人 / 平台 CI。
- 时限：YYYY-MM-DD 或 T+N 日；验证指标：指标编号 + 期望方向。
- 边界：不给买卖价位 / 杠杆 / 仓位建议。

---

## 五、信息分层与决策交付（强制项实例化）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制。
- **信息等级**：四级标注与摘要引用约束见 `engine/templates/information-layering-spec.md` 第二 / 四节；market-sizing 数值按同规范标「假设乘积」并区间化。
- **新增信息模块**：四要素模板见 `engine/templates/information-layering-spec.md` 第四节。
- **指针引用**：决策卡以 `DC-<研究线>-<序号>` 引用；事实以 `[FC-…]` 引用。

---

## 六、阈值校准与 ex-ante

- 首次回测时间点 **2027-06**（中期），2027-12 全期；校准前标注口径见 `engine/templates/decision-delivery-spec.md` 第六节。
- 校准对象：K01–K15 + RL-01–RL-09；输出 95% CI 与分位依据；工具 `engine/tools/threshold_calibration.py`。
- 已登记触发阈值（决策卡触发条件与行动协议引用）：K01 3M EIBOR 距硬红线 **≤25bp**（融资成本专题，口径同 `content/economy/dubai/apartment` 业务线台账）。

---

## 七、盲区与消号

- 台账：`engine/report-audits/blind-spot-ledger.md`；P0 四类（就业 / 收入 / 空置 / 竣工）优先消号。
- 消号条件与责任周期以台账为准；本业务线每季公布状态。
- 盲区总数目标 **≤6**（KPI-5，Phase 3 末；当前值与消号进度以台账为准）。

---

## 八、版本治理

- 核验 / 收敛型运行**不新增版本号**，统一标注「**本期读数时点 YYYY-MM-DD**」。
- 仅当核心事实修正时升级版本号，并在决策卡与来源登记留痕。

---

## 九、来源与核验

- 来源分级遵循通用基座第四节；本业务线不新采数据，只收敛仓库内已文档化事实（各研究线报告 + 事实卡片库 + 来源登记）。
- 来源登记：`{{SOURCE_REGISTRY_PATH}}`（默认 `data/processed/economy/insight/source_registry.json`，首期可缺，引用走事实卡片 source 字段）。
- **来源策略**：`{{SOURCE_STRATEGY}} = synthesis_only`——本业务线为**无外部来源的综合层**，报告不出现外部 URL，来源追溯经事实卡片 `[FC-…]` / 各研究线来源登记指针完成。`source_check` R1 据此豁免「登记为空」告警；若未来报告引入外部 URL，仍须先登记来源（R1 不受豁免影响）。

---

## 十、渲染差异（相对通用规范的实例化）

- **决策卡**：用 `.decision-card` 组件；证据强度 `ev-strong / ev-mid / ev-weak`；信息充分度 `suff ok / suff need`。
- **行动协议**：用 `.action-card` + `.prio immediate / watch / archive`。
- **场景切片**：用 `.slice`。
- **新增信息统计**：用 `.delta-strip`。
- **信息等级**：用 `.lvl lvl-verified / lvl-partial / lvl-inferred / lvl-assumption`。

---

## 十一、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-15 | 初始版本 | 决策仪表盘业务配置：决策卡协议、三场景切片、ex-ante、盲区消号、版本治理、渲染差异 |
| v1.1 | 2026-11-16 | 来源策略声明 | 新增 `{{SOURCE_STRATEGY}} = synthesis_only`，供 R1 区分「无外部来源的综合层」与「登记缺失」，消除误报 |
