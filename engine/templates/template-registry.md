# 报告模板类型注册表（template-registry）

> **定位**：`engine/templates/` 通用层的**类型分类注册表**。记录已注册的报告类型维度、各类型的模板清单与适用业务线，并规定新增类型 / 新增业务线的动态接入步骤。通用基座与跨类型渲染规范常驻本目录根部，类型专属模板按类型 ID 分目录存放——新增类型只加目录、不改既有结构。行业主流类型的**全谱系分类与选型参考**见 [report-classification.md](./report-classification.md)（六族十二类领域口径；本注册表登记已注册类型：十二类对应 12 个类型 ID + 扩展类型，当前总数 13+，含 A4 行业趋势周报型与决策仪表盘型）。

---

## 一、目录分类架构

```
engine/templates/
├── prompt-generic-base.md        # 通用基座（类型中立，全部类型共享）
├── monitoring-common-spec.md     # 渲染/排版/交付通用规范（跨类型共享最低标准）
├── template-registry.md          # 本注册表（类型接入点）
├── report-classification.md      # 行业主流分类体系（六族十二类领域口径，新增类型选型参考）
├── compliance-rules.json         # 合规校验规则（已注册类型结构骨架 × 周期，CI 阻断式校验关卡依据）
├── market-monitoring/            # 类型一：市场指标监测型
│   ├── prompt-baseline-setup-template.md
│   ├── prompt-monthly-monitor-template.md
│   ├── prompt-quarterly-analysis-template.md
│   └── prompt-annual-review-template.md
├── trend-weekly/                 # 类型十三：行业趋势周报型
│   ├── prompt-baseline-setup-template.md
│   ├── prompt-weekly-monitor-template.md
│   ├── operations-guide.md        # 通用运维手册（生命周期/校验/异常/Agent 约定）
│   └── README.md                 # 通用接入与使用指南
├── decision-dashboard/           # 类型十四：决策仪表盘型
│   └── prompt-baseline-setup-template.md
├── employment-research/          # 类型二：职业就业调研型
│   ├── prompt-baseline-setup-template.md
│   ├── prompt-update-template.md
│   ├── operations-guide.md        # 通用运维手册（四档节拍/校验/异常/Agent 约定）
│   └── README.md                 # 通用接入与使用指南
├── competitive-intelligence/     # 类型三：竞争情报监测型
│   ├── prompt-baseline-setup-template.md
│   └── prompt-monthly-update-template.md
├── sentiment-monitoring/         # 类型四：舆情传播监测型
│   ├── prompt-baseline-setup-template.md
│   └── prompt-monthly-update-template.md
├── consumer-research/            # 类型五：消费者·用户调研型
│   ├── prompt-baseline-setup-template.md
│   └── prompt-study-template.md
├── industry-research/            # 类型六：行业深度研究型
│   ├── prompt-baseline-setup-template.md
│   └── prompt-annual-refresh-template.md
├── market-sizing/                # 类型七：市场规模测算与预测型
│   ├── prompt-baseline-setup-template.md
│   └── prompt-annual-refresh-template.md
├── investment-research/          # 类型八：投资分析与尽调型
│   ├── prompt-baseline-setup-template.md
│   └── prompt-target-update-template.md
├── policy-analysis/              # 类型九：政策法规解读型
│   ├── prompt-baseline-setup-template.md
│   ├── prompt-monthly-monitor-template.md
│   └── prompt-policy-review-template.md
├── feasibility-study/            # 类型十：可行性与市场进入型
│   ├── prompt-baseline-setup-template.md
│   └── prompt-study-template.md
├── flash-commentary/             # 类型十一：快评·事件点评型
│   ├── prompt-baseline-setup-template.md
│   └── prompt-flash-note-template.md
└── whitepaper/                   # 类型十二：白皮书·专题深度型
    ├── prompt-baseline-setup-template.md
    └── prompt-topic-study-template.md

engine/prompts/                    # 泛用版业务提示词（每类型一目录，建业务线时整目录复制填值）
├── trend-weekly/                 # prompt-baseline-setup.md · prompt-weekly-monitor.md
├── competitive-intelligence/     # prompt-baseline-setup.md · prompt-monthly-monitor.md · prompt-flash-update.md
├── sentiment-monitoring/         # prompt-baseline-setup.md · prompt-monthly-monitor.md · prompt-flash-warning.md
├── consumer-research/            # prompt-baseline-setup.md · prompt-study.md
├── industry-research/            # prompt-baseline-setup.md · prompt-annual-refresh.md
├── market-sizing/                # prompt-baseline-setup.md · prompt-annual-refresh.md
├── investment-research/          # prompt-baseline-setup.md · prompt-target-review.md
├── policy-analysis/              # prompt-baseline-setup.md · prompt-monthly-monitor.md · prompt-policy-review.md
├── feasibility-study/            # prompt-baseline-setup.md · prompt-project-study.md
├── flash-commentary/             # prompt-baseline-setup.md · prompt-flash-note.md
└── whitepaper/                   # prompt-baseline-setup.md · prompt-topic-study.md
```

- **根部共享**：通用基座定义跨类型质量规则、变量框架、来源分级、锚定与台账协议；渲染规范定义 HTML 报告的最低渲染标准；合规规则文件登记各类型各周期的结构骨架校验规则（节数 / 必填字段 / 内容格式），供 `engine/tools/compliance_check.py` 的 CI 阻断式校验关卡与定期合规审计消费。任何类型的模板与业务提示词均继承根部文件。
- **类型目录**：目录名 = 类型 ID（小写 kebab-case）；每类型必备一份基线类型模板（`prompt-baseline-setup-template.md`），周期模板按类型的节拍设计自定（文件名以 `prompt-` 开头、以 `-template.md` 结尾）。
  - **泛用版业务提示词（`engine/prompts/<类型ID>/`）**：11 个类型各有独立可运行的泛用版业务提示词目录（`prompt-baseline-setup.md` + 各周期提示词 + 可选事件触发专项，共 24 份），位于通用层 `engine/prompts/`，不再存放于类型目录内。泛用版 = 绑定类型的业务提示词母版（变量区 + 类型模板引用 + TODO 业务项）；**修改周期提示词内容时须同步类型模板与 `engine/prompts/` 泛用版两处**。

## 二、已注册类型清单

| 类型 ID | 类型名称 | 基线模板 | 周期模板 | 节拍设计 | 已接入业务线 |
|---|---|---|---|---|---|
| market-monitoring | 市场指标监测型 | prompt-baseline-setup-template.md | monthly / quarterly / annual（三份独立） | 月 / 季 / 年三周期 | content/economy/dubai/apartment |
| trend-weekly | 行业趋势周报型 | prompt-baseline-setup-template.md | prompt-weekly-monitor-template.md | 周报主节拍（数据截止日命名）+ 事件触发板块升级 | content/economy/trends |
| employment-research | 职业就业调研型 | prompt-baseline-setup-template.md | prompt-update-template.md（一份覆盖三档节拍） | 基线 + 月度主更新 + 事件触发 | content/tech/ai-security/dubai；content/tech/ai-application/dubai；content/education/study-abroad |
| competitive-intelligence | 竞争情报监测型 | prompt-baseline-setup-template.md | prompt-monthly-update-template.md（覆盖两档） | 月度主更新（动态矩阵刷新）+ 事件触发升级 | content/tech/ai-security/competitive-intelligence/dubai；content/tech/ai-application/competitive-intelligence/dubai |
| sentiment-monitoring | 舆情传播监测型 | prompt-baseline-setup-template.md | prompt-monthly-update-template.md（覆盖两档） | 月度舆情月报 + 事件触发预警升级 | 暂无 |
| consumer-research | 消费者·用户调研型 | prompt-baseline-setup-template.md | prompt-study-template.md（项目制） | 项目制专题调研 + 年度满意度复测 | 暂无 |
| industry-research | 行业深度研究型 | prompt-baseline-setup-template.md | prompt-annual-refresh-template.md | 一次性深度全景 + 年度刷新（重大事件可插刷） | content/tech/ai-security/industry-research/dubai；content/tech/ai-application/industry-research/dubai |
| market-sizing | 市场规模测算与预测型 | prompt-baseline-setup-template.md | prompt-annual-refresh-template.md | 一次性测算建模 + 年度假设刷新与回测（失效信号可插刷） | 暂无 |
| investment-research | 投资分析与尽调型 | prompt-baseline-setup-template.md | prompt-target-update-template.md | 首次覆盖 + 定期复核 + 事件触发结论修订 | 暂无 |
| policy-analysis | 政策法规解读型 | prompt-baseline-setup-template.md | prompt-monthly-monitor-template.md（月度）；prompt-policy-review-template.md（事件 / 年度） | 月度主更新 + 事件触发单份解读 + 年度台账复盘 | content/education/education-system；content/international/international-relations；content/international/immigration；content/international/immigration/dubai；content/political/political-system；content/society/social-structure |
| feasibility-study | 可行性与市场进入型 | prompt-baseline-setup-template.md | prompt-study-template.md（项目制） | 项目制一次性论证 + 项目复盘 | 暂无 |
| flash-commentary | 快评·事件点评型 | prompt-baseline-setup-template.md（机制文档） | prompt-flash-note-template.md | 事件触发 72h 快评（基线期为机制建立，不出正文） | 暂无 |
| whitepaper | 白皮书·专题深度型 | prompt-baseline-setup-template.md | prompt-topic-study-template.md（选题制） | 新选题白皮书 + 年度系列篇 + 框架修订篇 | 暂无 |
| decision-dashboard | 决策仪表盘型 | prompt-baseline-setup-template.md | 同基线（季度刷新 + 事件触发插刷） | 跨研究线决策层：收敛 / 暴露 / 触发；季度主更新 | content/economy/insight |

> **命名兼容性说明**：节拍为月度 / 季度 / 年度 / 周度的类型，产出命名与 `engine/tools` 标准正则（monthly / quarterly / annual / baseline / weekly）兼容；项目制与事件触发类型（consumer-research、feasibility-study、flash-commentary、policy-analysis、investment-research、whitepaper 的一次性件）使用 `{{YYYY-MM-DD}}-主题.md` 通用命名，`validate.py` 仅提示 WARN 不阻断，属预期行为。

## 三、动态接入步骤

### 3.1 新增报告类型（不改动既有结构）

0. 先查 [report-classification.md](./report-classification.md)：确认目标报告类型在六族十二类中的归属与边界（避免与既有类型交叉重叠），并参考第四节选型优先级决定是否模板化。
1. 在 `engine/templates/` 下新建类型目录（类型 ID，小写 kebab-case），撰写该类型的基线类型模板与周期类型模板（头部继承声明指向根部通用基座与渲染规范）。
2. 模板内**严禁**出现任何业务关键词（地区 / 机构 / 专属指标，校验见 `engine/tools/validate.py`）。
3. 在本注册表第二节清单登记：类型 ID、名称、模板文件、节拍设计。
4. 在 `engine/tools/_common.py` 的 `TEMPLATE_TYPE_DIRS` 中登记类型 ID 与必备文件清单（供 validate.py 校验）。
5. 在 `engine/templates/compliance-rules.json` 登记该类型各周期结构骨架规则（节数 / 节名参考 / 模板文件），供合规校验关卡与审计消费（未登记的类型其报告按警告处理）。

### 3.2 已有类型下新增业务线

1. 按[通用基座第 1.2 节](./prompt-generic-base.md)执行：建立 `content/<theme>/<category>/<region>/` 目录（`prompts/` / `reports/`），撰写 `business-config.md`（业务单一事实源），数据落 `data/processed/<theme>/<维度段...>/`。
2. 按类型节拍设计建立业务周期提示词，头部继承声明指向 `./<类型ID>/` 下对应类型模板。
3. 首期运行基线提示词，建立登记册与基线锚；业务线注册到本注册表第二节「已接入业务线」列。

### 3.3 类型退役 / 合并

1. 业务线迁移完成后，从第二节清单移除并在「变更记录」留痕；类型目录归档前须确认无业务线引用（全仓 grep 类型 ID）。
2. 不物理删除历史类型目录，除非版本记录中明确批准。

## 四、变更记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 建立双类型分类架构（market-monitoring / employment-research）与动态接入规程 |
| v1.1 | 2026-11-13 | 新增 report-classification.md | 通用层补充行业主流分类体系（六族十二类）作为新增类型选型参考；3.1 接入流程前置选型步骤 |
| v1.2 | 2026-11-13 | 全类型模板骨架接入 | 依 report-classification.md 将其余 10 个主流类型全部模板化并注册（competitive-intelligence / sentiment-monitoring / consumer-research / industry-research / market-sizing / investment-research / policy-analysis / feasibility-study / flash-commentary / whitepaper），每类型基线 + 周期模板各一份；_common.py TEMPLATE_TYPE_DIRS 同步登记；新增命名兼容性说明 |
| v1.3 | 2026-11-13 | 业务提示词脚手架 | 其余 10 个类型各新增 business-prompt-scaffold.md（复制式业务提示词脚手架：实例化步骤 + business-config 清单 + 各周期提示词全文脚手架），对接通用基座 1.2 节新增业务线流程 |
| v1.4 | 2026-11-13 | 合规校验规则接入 | 新增根部共享文件 compliance-rules.json（12 类 × 周期结构骨架校验规则）；engine/tools/compliance_check.py 提供 CI 阻断式模板合规校验关卡、--scaffold 模板自动填充引导与 --audit 历史报告合规审计；3.1 接入流程追加第 5 步（合规规则登记） |
| v1.5 | 2026-11-13 | 泛用版业务提示词 | 其余 10 个类型各新增 prompts/ 子目录（共 23 份独立泛用版业务提示词：基线 + 主周期 + 竞争情报 / 舆情事件触发专项），由 business-prompt-scaffold.md 拆分；建新业务线时整目录复制填值即用 |
| v1.6 | 2026-11-13 | 新增类型十三：行业趋势周报型（trend-weekly） | 注册周节拍类型（基线机制文档 + 八节周报模板 + scaffold + 泛用 prompts ×2）；_common.py TEMPLATE_TYPE_DIRS 登记；compliance-rules.json 登记八节骨架；周报命名 `{YYYY-MM-DD}_weekly`（日期 = 数据截止日）纳入标准正则；首条业务线 content/tech/weekly-roundup 接入 |
| v1.7 | 2026-11-13 | 第二条 trend-weekly 业务线接入 | content/economy/trends（经济趋势周报）按类型标准流程接入：目录 + business-config + 周期/基线提示词 + 台账骨架；词汇库 economy 主题（44 条）绑定至「词汇速览」区块；首期周报待运行（以首期周报为结构锚） |
| v1.8 | 2026-11-13 | 第三条 trend-weekly 业务线接入 | content/tech/weekly-roundup（AI Agent 与大模型趋势周报）按类型标准流程接入：目录 + business-config + 周期/基线提示词 + 台账骨架；词汇库 ai-agent 主题（73 条，5 分类）绑定至「词汇速览」区块；首期周报待运行（以首期周报为结构锚） |
| v1.9 | 2026-11-14 | 通用层补全 + 业务线合并 | ① trend-weekly / employment-research 各新增 `operations-guide.md`（通用运维手册）与 `README.md`（通用接入指南），作为类型通用流程唯一源，业务线文档瘦身为业务差异；② trends/ai-security 与 trends/ai-agent 合并为 content/tech/weekly-roundup（五主题板块，共用台账与词汇）；已接入业务线更新为 content/tech/weekly-roundup；content/economy/trends |
| v1.10 | 2026-11-15 | 口径修正 | 明确「六族十二类（领域口径）≠ 注册类型总数」；注册类型 = 12 个对应类型 + 扩展类型（A4 行业趋势周报型、决策仪表盘型），当前 13+；compliance-rules.json 措辞同步 |
| v1.11 | 2026-11-16 | 目录树修正 | 泛用版业务提示词已上移至 `engine/prompts/<类型ID>/`（类型目录内 `prompts/` 子目录不再存在）；`business-prompt-scaffold.md` 全 11 份已删除（内容并入泛用版）；目录树与文件清单同步修正 |
| v1.12 | 2026-11-16 | 计数更正 | 泛用版业务提示词实际 24 份（11 目录：2+3+3+2×8）；第一节当前描述由「23 份」更正为「24 份」，v1.5 历史行的「23 份」为初版计数口径，保留不改 |
| v1.13 | 2026-11-16 | 同步纪律恢复 | 恢复泛用版「母版定义 + 修改周期提示词须同步类型模板与 engine/prompts/ 泛用版两处」维护纪律（该表述为全仓唯一，此前目录树修正时被精简掉） |
| v1.14 | 2026-11-18 | 四主题业务线接入 | policy-analysis 类型下新增四条业务线：`content/education/education-system`、`content/international/international-relations`、`content/political/political-system`、`content/society/social-structure`（P1-9 四主题接入就绪化；region 可选，业务线以 category 段落位） |
| v1.15 | 2026-11-21 | 科技主题月度化 | trend-weekly 仅保留 `content/economy/trends`（tech 两条周报线停用）；employment-research 接入业务线更新为 `content/tech/ai-security/dubai`；competitive-intelligence 新增 `content/tech/ai-application/trends` |
| v1.16 | 2026-11-21 | policy-analysis 月度节拍扩展 | 新增 `prompt-monthly-monitor-template.md`（类型模板）与 `engine/prompts/policy-analysis/prompt-monthly-monitor.md`（泛用版）；compliance-rules.json 登记 monthly 骨架；`_common.py` TYPE_CADENCE 注册 monthly；首条接入业务线 `content/international/immigration` |
| v1.17 | 2026-11-21 | ai-application 对齐 ai-security | ai-application 删除 `trends`，新建 `competitive-intelligence/dubai`、`dubai`、`industry-research/dubai` 三条月度业务线；employment-research / competitive-intelligence / industry-research 三个类型的「已接入业务线」列同步登记 |
| v1.18 | 2026-11-21 | 长期居留签证业务线接入 | policy-analysis 类型下新增业务线 `content/international/immigration/dubai`（黄金签证 / 绿卡签证；基线 + 月度 + 事件触发）；机构分级主数据补录 u.ae / ICP / GDRFA / Arab News |
