# 目录结构与文件命名规范（STRUCTURE-AND-NAMING-SPEC v1.0）

> **状态**：现行规范
> **定位**：仓库级**目录分层 + 文件命名**单一规范。与 [layout.json](../tools/layout.json)（目录段单一事实源）配合：layout.json 管「目录段正则 / 主题 / 维度 / 深度」，本规范管「模块边界 / 文件级命名 / 反例 / 迁移」。
> **适用**：全部三层（`content/` / `engine/` / `data/`）、根级文件、`.github/`、`.githooks/`；适用于任何 Agent 平台与协作者。
> **配套**：[PAGE-BUILD-SPEC](./page-build-spec.md)（页面）、[INFORMATION-LAYERING-SPEC](../templates/information-layering-spec.md)（信息分层）、[MULTI-SESSION-GIT-PROTOCOL](./multi-session-git-protocol.md)（Git）。
> **最后更新**：2026-11-16

---

## 一、目的与适用范围

本规范解决三类问题：

1. **目录职责模糊**：什么内容放 `content/`、什么放 `engine/`、什么放 `data/`，子目录拆到多深。
2. **文件命名不统一**：同类文件多种写法（`2026-11_baseline_report.html` vs `2026-11-monthly.html` vs `prompt_baseline.md`）。
3. **扩展时失控**：新增主题 / 业务线 / 报告类型时，目录与文件名各自发明，事后难以检索与校验。

**适用对象**：所有新增文件与目录；历史文件按第十一节「legacy 冻结」处理，不强制改名。

---

## 二、设计原则

| 原则 | 含义 | 落地 |
|---|---|---|
| 单一事实源 | 同一规则只在一处定义 | 目录段正则 / 主题 / 维度 / 深度只在 `layout.json`；文件级规则只在本规范 |
| 三层不跨层 | 内容 / 引擎 / 资产不得混放 | `validate_layout.py` 一级目录白名单 |
| 平台安全 | 只用小写字母、数字与受控分隔符 | 避免大小写、空格、中文、特殊字符导致的 Windows/Linux 差异 |
| 位置驱动 | 命名规则按「目录位置 × 文件类型」确定 | 见第五节规则矩阵，而非全局一刀切 |
| 生成物豁免 | 机器生成的记录按生成器模式命名 | 不强行纳入人工命名规则，但必须确定性、可重放 |
| 渐进迁移 | 新文件强制、历史文件冻结 | 不搞大爆炸重命名；触碰时顺手修正 |

---

## 三、核心模块划分标准

目录的第一层职责必须唯一。判定顺序：**是否业务专属 → 是否跨主题复用 → 是否数据资产 → 是否机器生成**。

| 模块 | 根目录 | 判定标准 | 典型内容 | 禁止放入 |
|---|---|---|---|---|
| 内容层 | `content/` | 业务专属；按主题 / 地区 / 细分组织 | 报告、业务提示词、`business-config.md`、业务脚本 | 跨主题工具、通用模板、清洗后数据 |
| 模板层 | `engine/templates/` | 跨主题复用；类型中立 | 通用基座、类型模板、渲染规范、合规规则 | 任何业务关键词（地区 / 机构 / 专属指标） |
| 提示词层 | `engine/prompts/`、`content/**/prompts/` | 通用母版 vs 业务实例 | `prompt-*.md`、`business-config.md` | 业务提示词放入通用层 |
| 源码 | `engine/tools/`、`engine/audit/scripts/`、`engine/vocabulary/script/`、`content/**/script/` | 可执行逻辑 | `*.py` | 文档、数据、配置 |
| 配置 | `engine/tools/*.json`、`engine/vocabulary/config/`、`.github/`、`layout.json` | 工具 / 流程参数 | JSON、YML | 业务内容、密钥 |
| 资源层 | `data/raw/`、`data/processed/`、`data/assets/` | 原始抓取 / 清洗后台账 / 图片图表 | 原始文件、CSV/XLSX/JSON、图片 | 代码、报告 |
| 测试 | `engine/tests/` | 单元测试，集中管理 | `test_*.py` | 分散到业务线、测试数据混放 |
| 文档 | `engine/docs/`、`engine/report-audits/`、`engine/audit/*.md`、`engine/quality/*.md`、根 `README/AGENTS` | 规范 / 审计 / 说明 | Markdown | 可执行代码、临时草稿 |
| 记录 | `engine/audit/records/` | 机器生成的留痕 | registry、jsonl、reviews、backups | 手工编辑、业务正文 |

> **边界速判**：一份文件如果只服务一条业务线 → `content/`；如果服务多条业务线 → `engine/`；如果可被程序读写且属于研究数据 → `data/`；如果是运行产物 → `engine/audit/records/`。

---

## 四、目录命名规则

### 4.1 全局规则

- **正则**：`^[a-z0-9]+(?:-[a-z0-9]+)*$`（与 `layout.json` 的 `naming.pattern` 一致）。
- **格式**：kebab-case（小写字母 + 数字 + 连字符），禁止大写、下划线、空格、中文、连续连字符、首尾连字符。
- **单复数**：统一复数（`reports/`、`prompts/`、`templates/`、`tests/`、`docs/`）。
- **语义**：用完整词，不用歧义缩写（`docs/` 而非 `doc/`；`scripts/` 而非 `scr/`）。

### 4.2 例外（白名单）

| 例外 | 规则 | 示例 |
|---|---|---|
| Python 包目录 | snake_case，且含 `__init__.py` | `engine/tools/semantic_checks/` |
| 点目录 | 平台约定，不受本规范约束 | `.github/`、`.githooks/`、`.meituan-catpaw/` |
| 生成目录 | 由工具创建，随生成器命名 | `engine/vocabulary/data/<topic>/{imports,exports}/`、`engine/audit/records/{reviews,semantic,backups}/` |
| legacy 冻结 | 非包但为 snake_case 的历史目录 | `engine/fact_cards/`（新增同类目录必须 kebab） |

### 4.3 层级深度与维度优先级

- **深度上限**：`layout.json` 的 `naming.max_depth = 6`。业务线全路径 `content/<theme>/<维度段...>/`（多数主题为 2 维、`region` 可缺省时为 1 维；`tech` 为 3 维：`category→subcategory→region`），提示词 / 报告文件位于业务线之下。
- **engine 域内深度**：`engine/<域>/<子域>/<文件>`，建议 ≤ 4 层（如 `engine/tools/semantic_checks/base.py`）。
- **data 深度**：`data/processed/<theme>/<维度段...>/<文件>` 与 content 维度段对齐（≤ 6）；`data/raw/<source>/<文件>` ≤ 3；`data/assets/<文件>` ≤ 2。
- **维度顺序（硬性）**：维度先后由 `layout.json` 各主题自行声明——`economy` 为 `["region", "category"]`（地区优先），`tech` 为 `["category", "subcategory", "region"]`（AI 安全 / AI 应用两大类 → 业务线 → 地区），`education` / `international` / `political` / `society` 为 `["category", "region"]`（细分优先）；不得在未改 `layout.json` 的情况下倒置。地区段必须命中 `regions` 白名单（当前 `dubai`）。
- **region 可选（硬性）**：主题可在 `layout.json` 以 `optional_dimensions` 声明某维度可缺省；当前**六个主题均声明** `["region"]`。缺省 region 时业务线直接以 category（+subcategory）段落位（如 `content/economy/trends`、`content/tech/ai-application/weekly-roundup`、`content/education/education-system`），剩余段按声明顺序剔除 region 后逐位映射。
- **分组目录（硬性）**：theme 下允许存在不含 `prompts/business-config.md` 的**分组目录**（如 `content/tech/ai-security`），仅作业务线祖先；其层级深度须**小于**该主题维度数，不参与地域白名单与业务线深度校验（校验见 `validate_layout.check_theme`）。
- **禁止过深**：不得在业务线内继续发明 `prompts/{layer1}/{layer2}/` 之类的中间层；需要分类时用文件前缀或台账字段表达。

### 4.4 目录树示例（目标结构）

```
<repo>/
├── content/                                  # 内容层
│   ├── <theme>/                              # economy / tech / education / international / political / society
│   │   ├── <region>/<category>/               # economy：地区优先（dubai）
│   │   ├── <category>/                        # region 缺省：直接以 category 落位（如 content/economy/trends）
│   │   ├── <category>/<region>/               # education 等：细分优先（dubai）
│   │   └── <category>/<subcategory>/<region>/ # tech：AI 安全 / AI 应用 → 业务线 → 地区
│   │       └── <category>/<subcategory>/      # tech region 缺省（如 content/tech/ai-application/weekly-roundup）
│   │       ├── prompts/                       # business-config.md + prompt-*.md
│   │       ├── reports/                       # 正式报告 *.html
│   │       │   ├── archives/                  # 归档（保留策略）
│   │       │   └── legacy/                    # 存档（不发布不审计）
│   │       ├── sources/                       # md 源稿（与报告同名）
│   │       │   └── archives/                  # 源稿归档（与报告同保留策略）
│   │       ├── script/                        # 业务脚本（可选）
│   │       ├── operations-guide.md
│   │       └── README.md
├── engine/                                   # 引擎层
│   ├── templates/                            # 通用基座 + <type>/ 类型模板
│   ├── prompts/                              # 泛用版业务提示词 <type>/
│   ├── tools/                                # 工具 + layout.json + 配置 JSON
│   │   └── semantic_checks/                  # Python 包（snake_case）
│   ├── fact_cards/                           # 事实卡片库（legacy snake；新库目录用 kebab、JSON 沿用 snake）
│   ├── vocabulary/                           # 受控词表（config/ script/ data/）
│   ├── quality/                              # 质量规则 + prompts/
│   ├── audit/                                # 审计规范 + scripts/ + prompts/ + records/
│   ├── report-audits/                        # 审计产出
│   ├── docs/                                 # 仓库级规范文档
│   └── tests/                                # 单元测试（集中）
├── data/                                     # 资产层
│   ├── raw/                                  # 原始抓取
│   ├── processed/<theme>/<维度段...>/          # 清洗后台账 / 登记 / 量化数据（与 content 维度段对齐）
│   └── assets/                               # 图片图表
├── .github/
│   ├── actions/<action>/action.yml
│   └── workflows/<slug>.yml
├── .githooks/<hook>
├── AGENTS.md / README.md / CHANGELOG.md / INDEX.md
├── requirements.txt
├── index.html / reader.html
└── automation-status.json / perf-status.json
```

---

## 五、文件命名规则矩阵

### 5.1 总表（按位置）

| 位置 | 规则 | 正确示例 | 备注 |
|---|---|---|---|
| 仓库根 | 约定固定名（大写或 kebab） | `README.md`、`AGENTS.md`、`CHANGELOG.md`、`INDEX.md`、`requirements.txt`、`index.html`、`reader.html`、`automation-status.json`、`perf-status.json` | 新根级文件须先评估是否应迁入 `engine/` |
| `.github/workflows/` | kebab-case + `.yml` | `ci.yml`、`html-sync.yml`、`scheduled-maintenance.yml` | 统一 `.yml`，不用 `.yaml` |
| `.github/actions/<action>/` | 目录 kebab；入口固定 `action.yml` | `submit-pr/action.yml`、`workspace-cleanup/action.yml` | — |
| `.githooks/` | kebab-case，无扩展名 | `pre-push` | — |
| `engine/tools/*.py` | snake_case | `validate_layout.py`、`report_style.py` | 私有共享模块加 `_` 前缀：`_common.py`、`_quant.py` |
| `engine/tests/*.py` | `test_<对象>.py`（snake） | `test_tools.py`、`test_pipeline_runner.py` | 测试集中于此，不按业务线分散 |
| `engine/tools/*.json` | kebab-case | `layout.json`、`metrics-dictionary.json` | legacy 冻结：`institution_tiers.json`、`pipeline_manifest.json` |
| `engine/templates/`（根） | kebab-case | `prompt-generic-base.md`、`monitoring-common-spec.md`、`template-registry.md`、`compliance-rules.json` | 类型中立 |
| `engine/templates/<type>/` | `prompt-<cycle>-template.md`；固定 `operations-guide.md` / `README.md` | `prompt-baseline-setup-template.md` | 目录名 = 类型 ID（kebab） |
| `engine/prompts/<type>/` | `prompt-<cycle>.md` | `prompt-weekly-monitor.md` | 与类型模板一一对应 |
| `engine/docs/*.md` | kebab-case | `page-build-spec.md`、`report-pipeline-system.md` | — |
| `engine/docs/adr/` | `NNNN-slug.md` | `0001-dimension-order.md` | 四位序号 + kebab |
| `engine/audit/*.md`、`engine/quality/*.md` | kebab-case | `report-standard.md`、`repair-sop.md` | — |
| `engine/{audit,quality}/prompts/` | `NN-slug.md`（两位序号） | `00-orchestrator.md`、`10-draft.md` | 同目录内唯一、连续 |
| `engine/report-audits/*.md` | `<slug>[-YYYY-MM-DD].md` | `cicd-alignment-audit-2026-11-16.md`、`tech-debt-ledger.md` | 台账类不加日期；一次性审计带日期 |
| `engine/report-audits/*.json` | kebab，可带日期 | `release-calendar.json`、`quality-manifest-2026-11-14.json` | — |
| `content/**/prompts/*.md` | `business-config.md` + `prompt-<cycle>.md` | `business-config.md`、`prompt-monthly-monitor.md` | 见第七节 |
| `content/**/reports/*.html` | `<period>_<cycle>[_report].html` | `2026-11_monthly.html`、`2026-11_baseline_report.html` | 见第六节 |
| `content/**/sources/*.md` | 与对应报告同名（`.md`） | `2026-11_baseline_report.md` | 纯 HTML 业务线可无；归档入 `sources/archives/` |
| `content/**/operations-guide.md`、`README.md` | 固定名 | — | — |
| `data/processed/{theme}/{维度段...}/` | snake_case 主体 + 可选 `_period` 后缀 | `ai_trend_ledger.md`、`source_registry.json`、`dubai_apartment_indicator_registry_2026-11.xlsx` | 见第八节 |
| `data/raw/**` | 来源原名（豁免），建议 `<source>_<period>.<ext>` | `cbuae_statistical_bulletin_2026-08_official.xlsx` | 不清洗、不改名原始抓取 |
| `data/assets/**` | kebab-case | `dubai-price-index.png` | — |
| `engine/vocabulary/config/*.json` | kebab / 单词 | `topics.json`、`sync.json` | — |
| `engine/vocabulary/data/<topic>/` | `terms.md`；`imports/YYYY-MM-DD_<slug>.md`；`exports/<topic>_YYYY-MM-DD_export.{json,csv,jsonl}` | `terms.md`、`2026-11-13_seed-ai-security.md`、`ai-security_2026-11-13_export.csv` | 生成物，模式固定 |
| `engine/vocabulary/data/*-backups/` | `*.YYYYMMDD_HHMMSS.{json,md,bak}` | `topics.20261113_170458.json` | 时间戳紧凑无分隔 |
| `engine/audit/records/**` | 机器生成，文件名 = 报告路径派生 | `content-...-reports-2026-11-monthly-html.json` | 豁免大小写；顶层 `audit_registry.json` / `publish_fingerprints.json` 为 snake |
| `engine/fact_cards/*.json` | snake_case | `security_fact_cards.json` | legacy；新增卡片 JSON 沿用 snake_case，目录名建议后续改为 `fact-cards/` |

### 5.2 全局字符集约束

- 允许字符：`a-z`、`0-9`、连字符 `-`、下划线 `_`、点 `.`。
- 连字符用于：目录、文档、配置、CI、提示词、报告周期前的部分。
- 下划线用于：Python 标识符、数据主体、报告 `<period>_<cycle>` 分隔、日期前缀 `<date>_<slug>` 分隔。
- 点仅用于扩展名与版本/模式（`manifest.schema.json`、`topics.20261113_170458.json`）。
- 禁止：大写字母（固定名与生成物派生除外）、空格、中文、`@#!$%` 等特殊字符、连续分隔符、首尾分隔符。

---

## 六、报告命名细则

### 6.1 周期标识

| 周期 | period 格式 | 示例 |
|---|---|---|
| 月度 monthly | `YYYY-MM` | `2026-11` |
| 季度 quarterly | `YYYY-Qn` | `2026-Q3` |
| 年度 annual | `YYYY` | `2026` |
| 周报 weekly | `YYYY-MM-DD`（数据截止日） | `2026-11-13` |
| 基线 baseline | `YYYY-MM` | `2026-11` |

### 6.2 文件名

```
<period>_<cycle>.html
<period>_<cycle>_report.html        # 仅 baseline 兼容旧写法
<period>_baseline_<slug>.html        # 框架专项（基线家族，纳入基线组）
```

- **canonical**：`YYYY-MM_monthly.html`、`YYYY-Qn_quarterly.html`、`YYYY_annual.html`、`YYYY-MM-DD_weekly.html`、`YYYY-MM_baseline_report.html`。
- **框架专项件**：`<period>_baseline_<slug>.html`（如 PRIME 对齐件），按基线周期管理，常驻展示不参与归档计数；与 `_common.detect_report()` / `naming_check.REPORT_RE` 同步。
- `YYYY-MM_baseline.html` 为兼容别名，仅历史文件保留；新文件统一 `_baseline_report.html`（与 `_common.expected_output()` 一致）。
- **交付物只放 `.html`**；Markdown 源稿放业务线 `sources/`，不得放入 `reports/`。
- 归档：`reports/archives/` 与 `sources/archives/`（保留策略内）；存档：`reports/legacy/`（不发布不审计）。
- 项目制 / 事件触发类型的一次性件使用 `YYYY-MM-DD_<slug>.html`（如快评、专项），须在类型模板注册表中登记命名兼容性。

### 6.3 反例

| 反例 | 问题 | 正确 |
|---|---|---|
| `2026-11-monthly.html` | 周期与文件名用连字符 | `2026-11_monthly.html` |
| `2026_11_monthly.html` | 周期内用下划线 | `2026-11_monthly.html` |
| `monthly_2026-11.html` | 周期前置 | `2026-11_monthly.html` |
| `2026-11_baselineReport.html` | 驼峰 | `2026-11_baseline_report.html` |
| `2026-11_baseline.html`（新文件） | 非 canonical | `2026-11_baseline_report.html` |
| `2026-11_monthly_report.html` | 多余 `_report` | `2026-11_monthly.html` |
| `2026-11-13_weekly_report.html` | 周报多余 `_report` | `2026-11-13_weekly.html` |
| `2026年11月报告.html` | 中文 | `2026-11_monthly.html` |
| `monthly report final v2.html` | 空格 / 版本词 | `2026-11_monthly.html` |

---

## 七、提示词命名细则

### 7.1 业务提示词（`content/**/prompts/`）

- **单一事实源**：`business-config.md`（业务配置、变量区、来源优先级、类型声明）。
- **周期提示词**：`prompt-<cycle>.md`。
- **cycle 白名单**（标准名）：`baseline-setup`、`monthly-monitor`、`quarterly-analysis`、`annual-review`、`weekly-monitor`。
- **类型别名**（须在 `engine/templates/template-registry.md` 登记）：`annual-refresh`、`update`、`study`、`flash-note`、`flash-update`、`flash-warning`、`policy-review`、`target-review`、`project-study`、`topic-study`、`quarterly-review`、`monthly-update`。
- 条件节拍（不产出报告）须在正文含 `<!-- report-output: none -->`。

### 7.2 通用提示词与模板

| 位置 | 规则 | 示例 |
|---|---|---|
| `engine/prompts/<type>/` | `prompt-<cycle>.md`（与类型模板对应） | `prompt-flash-note.md` |
| `engine/templates/<type>/` | `prompt-<cycle>-template.md` | `prompt-monthly-monitor-template.md` |
| `engine/audit/prompts/`、`engine/quality/prompts/` | `NN-slug.md` | `20-initial-review.md` |

### 7.3 反例

| 反例 | 问题 | 正确 |
|---|---|---|
| `prompt_baseline.md` | 下划线 | `prompt-baseline-setup.md` |
| `baseline.md` | 缺 `prompt-` 前缀 | `prompt-baseline-setup.md` |
| `promptBaseline.md` | 驼峰 | `prompt-baseline-setup.md` |
| `提示词-月度.md` | 中文 | `prompt-monthly-monitor.md` |
| `prompt-monthly-monitor-template.md` 放在业务 `prompts/` | 模板与实例混淆 | 业务用 `prompt-monthly-monitor.md`，模板放 `engine/templates/<type>/` |
| `business_config.md` | 下划线 | `business-config.md` |

---

## 八、数据资产命名细则

### 8.1 清洗后数据（`data/processed/<theme>/<维度段...>/`）

```
<subject>[_<period>][_<qualifier>].<ext>
```

- `<subject>`：snake_case，表达指标 / 台账 / 登记册（`macro_snapshot`、`signal_status`、`transmission_series`）。
- `<period>`：可选，`YYYY-MM` / `YYYY-MM-DD` / `YYYY-Qn` / `YYYY`。
- `<qualifier>`：可选，来源或版本限定（`official`、`synthetic`）。
- `<ext>`：小写（`.csv` / `.json` / `.xlsx` / `.md` / `.pdf`）。
- 台账 / 登记册：`<subject>_ledger.md`、`<subject>_registry.json` 或 `<subject>_registry.md`。

**正确示例**：`quant_macro_snapshot.csv`、`quant_signal_status.csv`、`quant_transmission_series_synthetic.csv`、`source_registry.json`、`ai_trend_ledger.md`、`dubai_apartment_indicator_registry_2026-11.xlsx`。

### 8.2 原始抓取（`data/raw/`）

- 保留来源原始文件名，**不强制** case；但禁止空格与中文，必要时改写为 `<source>_<period>.<ext>`。
- 原始文件不清洗、不覆盖；处理结果写入 `data/processed/`。

### 8.3 资产（`data/assets/`）

- kebab-case，与报告内引用路径一致；图片必须有可检索的语义名。

### 8.4 反例

| 反例 | 问题 | 正确 |
|---|---|---|
| `Data.xlsx` / `DATA.csv` | 大写 | `quant_macro_snapshot.csv` |
| `2026-11数据.csv` | 中文 | `quant_macro_snapshot_2026-11.csv` |
| `my report final v2.xlsx` | 空格 / 版本词 | `dubai_apartment_indicator_registry_2026-11.xlsx` |
| `dump_20261113_final_FINAL.csv` | 冗余修饰 | `quant_signal_status.csv` |
| `snapshot.csv` | 主体过泛、无口径 | `quant_macro_snapshot.csv` |

---

## 九、配置 / CI / 脚本命名细则

| 类型 | 规则 | 示例 |
|---|---|---|
| GitHub Actions 工作流 | `.github/workflows/<slug>.yml`，kebab | `content-update.yml` |
| 复合动作 | `.github/actions/<slug>/action.yml` | `submit-pr/action.yml` |
| Git 钩子 | `.githooks/<slug>`，无扩展名 | `pre-push` |
| Python 工具 | `engine/tools/<snake>.py` | `validate_layout.py` |
| Python 包 | 目录 snake_case + `__init__.py` | `engine/tools/semantic_checks/` |
| 工具配置 JSON | kebab（legacy 冻结除外） | `layout.json`、`metrics-dictionary.json` |
| 测试 | `engine/tests/test_<对象>.py` | `test_validate_layout.py` |
| 环境依赖 | 固定 `requirements.txt` | — |
| 状态文件 | 根级 kebab | `automation-status.json`、`perf-status.json` |

**禁止**：工作流用 `.yaml`；钩子加 `.sh`；测试文件放入业务目录；工具配置用中文或大写。

---

## 十、反例清单（速查）

| 类别 | 反例 | 正确 |
|---|---|---|
| 目录 | `Content/`、`currentAffairs/`、`regional_data/` | `content/`、`economy/`、`data/processed/<theme>/<维度段...>/` |
| 目录 | `content/<theme>/regional/<region>/<category>/`（已撤销的 regional 分组段） | `content/economy/dubai/apartment/`（region→category）或 `content/tech/ai-security/competitive-intelligence/dubai/`（category→subcategory→region）；区域缺省业务线为 `content/economy/trends/`、`content/tech/ai-application/trends/` |
| 目录 | `engine/tools/{subdir}/common.py`（过深且职责模糊） | `engine/tools/_common.py` |
| 文件 | `Report_Final.md` | `report-final.md` 或报告规范名 |
| 文件 | `2026-11_monthly.html` 放入 `reports/archived/` | `reports/archives/` |
| 文件 | `prompt-monthly-monitor.html` | `prompt-monthly-monitor.md` |
| 文件 | `business-config.yaml` | `business-config.md` |
| 文件 | `release calendar.json` | `release-calendar.json` |
| 文件 | `test-tools.py`（连字符） | `test_tools.py` |
| 生成物 | 手工改 `engine/audit/records/**` | 由 `audit_tool.py` / `pipeline_audit.py` 生成 |
| 临时 | `*.tmp`、`*.bak`（非备份目录）入仓 | `.gitignore` + `workspace_cleanup.py` |

---

## 十一、适配性验证

### 11.1 当前规模

- 6 主题、2 地区、7 条业务线、14 个注册报告类型。
- 技术栈：Python 标准库工具链 + Markdown/HTML 交付 + GitHub Actions + 机器生成记录。

### 11.2 全量命名审计结果（2026-11-16）

按本规范「位置 × 文件类型」规则对 431 个跟踪文件做全量比对：

- **人工编写文件**：文档 / 提示词 / 模板 / 配置 / 脚本 / 报告 —— **0 项违规**。
- **生成物**：`engine/audit/records/**`、`engine/vocabulary/data/**`、`data/raw/**` —— 按生成器模式豁免，均确定性可重放。
- **legacy 冻结项**（不改名，触碰时顺手修正）：
  - 目录 `engine/fact_cards/`（snake，非包）；
  - `engine/tools/institution_tiers.json`、`engine/tools/pipeline_manifest.json`（snake，工具直接加载）；
  - `engine/quality/manifest.schema.json`（点号模式）；
  - `engine/vocabulary/data/{sync-backups,topic-backups,imports,exports}/**`（时间戳生成物）。
- 报告源稿镜像：`content/**/sources/` 下与报告同名的 `.md`（如 `2026-11_baseline_report.md`）按报告周期命名豁免。
- 报告命名：`validate.py` 已对 `reports/` 做正则校验；`validate_layout.py` 已对目录段与维度声明做校验。

### 11.3 扩展路径验证

| 扩展动作 | 需要改动 | 命名是否需新规则 |
|---|---|---|
| 新增主题 | `layout.json` 注册主题 + 建 `content/<theme>/` | 否 |
| 新增业务线 | 建 `content/<theme>/<维度段...>/`（economy 为 `<region>/<category>`，其余主题为 `<category>/<region>`；region 缺省时仅 `<category>/`）+ `business-config.md` | 否 |
| 新增报告类型 | `engine/templates/<type>/` + 注册表 + `compliance-rules.json` + `_common.TEMPLATE_TYPE_DIRS` | 否 |
| 新增周期报告 | 按 `<period>_<cycle>.html` 落盘 | 否 |
| 新增数据资产 | 按 `data/processed/{theme}/{维度段...}/<subject>[_period].<ext>` 落盘 | 否 |
| 新增工具 | `engine/tools/<snake>.py` + `engine/tests/test_<对象>.py` | 否 |

结论：规则是**机械可执行**的，扩展不需要发明新命名，也不需要新增校验工具（避免过度设计）。

### 11.4 与既有门禁的关系

| 规范条目 | 现有强制 |
|---|---|
| 目录段 kebab / 一级目录白名单 / 维度顺序（按主题声明） / 深度 | `engine/tools/validate_layout.py` |
| 报告文件名周期 | `engine/tools/validate.py`、`_common.REPORT_RES` |
| 模板 / 提示词必备文件 | `engine/tools/validate.py` |
| 路径引用可达 | `engine/tools/check_links.py` |
| 页面结构 / 设计令牌 | `engine/tools/page_build_check.py` |
| 文件级命名（本规范新增部分） | 人工 review + 本规范反例清单；后续如需可增量加 `naming_check.py`，当前不建 |

---

## 十二、落地与校验

### 12.1 执行口径

- **新增文件 / 目录**：必须符合本规范；PR review 时按第十节反例清单逐项核对。
- **历史文件**：冻结。若因功能变更必须触碰，则顺手改为规范名，并在 PR 描述中注明。
- **生成物**：不得手工编辑；如需改命名，改生成器而非产物。

### 12.2 人工 Checklist（新文件提交前）

1. 目录是否是 kebab-case？是否在最浅的必要层？
2. 业务内容是否在 `content/`、跨主题复用是否在 `engine/`、数据是否在 `data/`？
3. 报告是否是 `<period>_<cycle>.html` 且只含必要部分？
4. 提示词是否有 `prompt-` 前缀且 cycle 在白名单？
5. Python 是否 snake_case、测试是否 `test_` 前缀？
6. 数据主体是否 snake_case、周期后缀是否规范？
7. 是否误把生成物 / 临时文件纳入版本控制？

### 12.3 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-16 | 初始版本 | 建立三层模块划分、目录 / 文件命名矩阵、报告 / 提示词 / 数据细则、反例清单与全量审计验证 |
