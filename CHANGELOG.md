# 变更记录

本文件记录仓库的结构与规范级变更（报告内容变更见各业务线 `reports/`）。

## 3.8.0 — 2026-11-26：新增投资分析业务线与汇总页类型 chips 动态化

- **结构**：经济主题新增 `content/economy/dubai/apartment-investment`（category=apartment-investment，region=dubai；投资分析与尽调型，基线 + 季度 / 年度复核 + 事件触发专项），标的为迪拜公寓资产类别（市场级）；`data/processed/economy/dubai/apartment-investment/` 同步建立标的档案与来源登记。
- **报告**：产出首期基线《迪拜（阿联酋）公寓住宅市场 · 首期投资覆盖报告》（md + HTML，八节固化锚）；结论为「正利差 + 价格回落 + 供给放量 → 选择性持有（有条件结论）」，估值区间 1,430–1,840 AED/sqft（假设乘积，多方法并列）。
- **hub**：`engine/tools/build_hub.py` 类型 chips 改为仅渲染当前有报告的类型（index.html / reader.html 共用 `visible_types()`）；无报告类型默认不展示，产出首份报告后自动出现；测试 `TestHubTypeChips` 锁定。
- **同步**：`template-registry.md` investment-research「已接入业务线」登记；`layout.json` changelog；INDEX.md / 汇总页重新生成。

## 3.7.0 — 2026-11-23：站点上线、品牌口径统一与自动化闭环

- **发布**：启用 GitHub Pages（`main` 根目录，legacy 构建），站点 `https://hmbphxkw76-byte.github.io/tech-context-digest/`；仓库 homepage 同步；CI 合并后站点自动重建。
- **品牌**：新增 `engine/tools/_common.py::SITE_BRAND` 单一事实源，`build_hub.py`（含 `_reader_script()`）与 `build_index.py` 统一引用；枢纽页标题由旧名改为 `Tech Life Research`；`README.md` 规模口径改为指针（不再硬编码数量）。
- **自动化**：新增两个妙手定时任务——「tech-context-digest 月度内容更新」（每月 1 日 14:30，`FREQ=MONTHLY`）与「审计 L3 深度复核与终审」（每周一 09:00，对齐 `engine/audit/README.md` §三·五），均经 `repo_sync` 网关 + PR。
- **数据治理**：删除 `engine/audit/records/reviews/` 29 条、`semantic/` 49 条迁移孤儿记录与 3 个已删报告快照；`.gitignore` 忽略 `.meituan-catpaw/`。
- **最佳实践对齐**：修正 `architecture-and-pipeline-design.md`（layout.json v5.0 口径）与 `report-classification.md` 漂移；报告外部链接补 `noopener`（MON-04 清零）；`engine/tools/README.md` 补全工具一览；tracker 补齐四个 canonical triage 标签。

## 3.6.0 — 2026-11-21：ai-application 对齐 ai-security 与 immigration/dubai 新增

- **结构**：删除 `content/tech/ai-application/trends/`，新建 `competitive-intelligence/dubai`（竞争情报监测型）、`dubai`（职业就业调研型）、`industry-research/dubai`（行业深度研究型）三条月度业务线，与 `ai-security/` 三类同构；`data/processed/` 同步。
- **结构**：国际主题新增 `content/international/immigration/dubai`（category=immigration，region=dubai；政策法规解读型，基线 + 月度），聚焦黄金签证（Golden Visa）与绿卡签证（Green Visa）。
- **layout.json**：`classification_version` 2026-11-21.3；`changelog` 同步上述两条。

## 3.5.0 — 2026-11-21：科技主题全线月度化与 ai-security/dubai 归位

- **结构**：删除 `content/tech/ai-security/weekly-roundup/` 与 `content/tech/ai-application/weekly-roundup/`（含 `data/processed/` 台账与来源登记）；`content/tech/ai-security/security/dubai/` 归位为 `content/tech/ai-security/dubai/`（含 `data/processed/`）；新建 `content/tech/ai-application/trends/`（竞争情报监测型，月度）。
- **节拍**：tech 全线月度化，无季 / 年。`ai-security/dubai`（employment-research）由「季度主更 + 月度核验 + 年度复盘」收敛为「基线 + 月度主更新」，季 / 年提示词停用；`industry-research/dubai` 由「baseline + annual」收敛为「baseline + monthly」。
- **layout.json**：`classification_version` 2026-11-21.1；comment 示例路径更新为 `content/tech/ai-application/trends`。
- **同步**：`template-registry.md`、`compliance-rules.json`、`report-classification.md`、`AGENTS.md`、`README.md`、`content/README.md`、`structure-and-naming-spec.md`、`architecture-and-pipeline-design.md`、`sync.json`、`check_links.py`、`vocabulary/README.md`、`tools/README.md` 与测试同步；hub / INDEX.md / 发布指纹 / 词汇区块重新生成。

## 3.4.0 — 2026-11-20：科技主题 AI 安全 / AI 应用归并与汇总页主题维度改版

- **结构**：`content/tech/` 下四个业务线物理归并为两个分组目录——`ai-security/`（security / competitive-intelligence / industry-research / weekly-roundup）与 `ai-application/`（weekly-roundup）；`data/processed/`、`data/raw/` 同步迁移。
- **layout.json v5.0**：`tech` 维度改为 `["category", "subcategory", "region"]`（region 可选），新增 `category_names`（ai-security → AI安全、ai-application → AI应用）；`classification_version` 2026-11-20.1。`validate_layout.check_theme` 支持不含业务配置的分组目录（深度须小于主题维度数）。
- **周报拆分**：原合并线 `content/tech/weekly-roundup` 拆分为 `ai-security/weekly-roundup`（AI 安全趋势周报，7 节）与 `ai-application/weekly-roundup`（AI 应用趋势周报，8 节）；原合并周报（2026-11-13 / 2026-11-20）移入 `sources/legacy/`；台账与来源登记同步拆分。
- **汇总页**：`build_hub.py` 的「主题」chips 改为一级主题（经济 / 科技 / 教育 / 国际 / 政治 / 社会），正文按一级主题分组、科技下按 AI安全 / AI应用 分组；Hero 统计改为 主题 / 业务线 / 报告 / 类型；`index.html` / `reader.html` / `INDEX.md` 重新生成。
- **同步**：`AGENTS.md`、`README.md`、`content/README.md`、`structure-and-naming-spec.md`、`report-classification.md`、`template-registry.md`、`compliance-rules.json`、`sync.json`、`check_links.py`、`audit_tool.py` 等路径与规则同步；unittest 822 通过，`optimization_gate --probe` 0 错误。

## 3.3.0 — 2026-11-18：engine/sources 迁移至业务线 sources

- **结构**：删除引擎层 `engine/sources/`；5 份 md 源稿按业务归属迁至 `content/economy/trends/sources/` 与 `content/tech/weekly-roundup/sources/`（含 `legacy/` 历史存档）。
- **归档**：`archive_reports.py` 同时轮转 `reports/` 与 `sources/`，源稿与报告共用同一保留策略；`sources/legacy/` 不参与轮转。
- **规范**：`AGENTS.md`、`structure-and-naming-spec.md`、`architecture-and-pipeline-design.md`、`engine/docs/agents/domain.md` 同步移除 `engine/sources` 表述；Markdown 源稿统一放业务线 `sources/`。

## 3.2.0 — 2026-11-17：业务线去 global 段 + region 可选维度

- **结构**：`content/economy/global/trends` → `content/economy/trends`；`content/economy/global/decision-hub` → `content/economy/insight`；`content/tech/trends/global` → `content/tech/weekly-roundup`。`data/processed/` 下对应台账 / 登记同步迁移。删除 `content/tech/{papers,principles,solutions,docs-analysis}` 四个空占位目录。
- **layout.json v4.1**：新增主题级 `optional_dimensions`，`economy` / `tech` 声明 `["region"]`；`regions` 白名单收敛为 `["dubai"]`。业务线可缺省 region 段，直接以 category 段落位。
- **引擎**：`_common.resolve_segments()` 统一维度段映射；`iter_business_dirs()` 改为按 `prompts/business-config.md` 锚点发现（1..维度数深度）；`validate_layout` 同步支持缺省 region；`decision_hub_check` 决策层标记由 `decision-hub` 改为 `insight`；`classify_reports` 过滤空 region 线索。
- **同步**：hub / INDEX.md / 发布指纹重新生成；审计登记册 prune + init；词汇库同步配置与状态刷新。

## 3.1.0 — 2026-11-17：全维度收口与稳定性加固

在 3.0.0 基础上完成「全维度范围梳理 → 架构对齐 → 自动化验证 → 交付物」收口。

### 收口

- **维度口径统一（F-02）**：`report-pipeline-system.md` / `report-pipeline-implementation-plan.md` / `process-vs-infrastructure-governance.md` / `engine/tools/README.md` / `structure-and-naming-spec.md` 中「category 必须先于 region」残留全部改为「按主题声明顺序」，与 `layout.json` / `AGENTS.md` 一致。
- **计数与基线刷新**：`report-process-reuse.md` / `report-pipeline-system.md` / `page-build-spec.md` / `architecture-development-standard.md` 的测试数（377/405 → 398）、报告数（12 → 10）、页数（17 → 15）、business-config 数（9 → 7）按实跑刷新。
- **发布指纹收敛**：`publish_fingerprint --emit` 重采集 10 份正式报告，`--check` 0 漂移。

### 加固

- **子进程 wall 超时**：`optimization_gate.run_checks`（默认 900s，`--timeout` 可覆盖）与 `pipeline_runner._run_command` / `run_node`（默认 600s）超时按错误（退出码 124）处理，单点挂起不再拖死全链路；新增 `test_gate_timeout_is_bounded` / `test_run_command_timeout` / `test_run_node_command_timeout`。

### 交付

- 新增 `engine/docs/end-to-end-coverage.md`（END-TO-END-COVERAGE v1.0）：六项要求 × 产物映射、N0–N8 覆盖矩阵、交付物清单、验证基线。
- `architecture-and-pipeline-design.md` P3 / P4 标记完成。

### 验证

`pipeline_runner run --from N0 --to N8` `outcome=passed`（run_id `3a0c4033553f`）；unittest 398 通过（1 跳过）；`optimization_gate --probe` 0 错误 / 1 警告；`publish_fingerprint --check` 0 漂移。

## 3.0.0 — 2026-11-17：回滚至六主题结构 + 全流程重建

内容结构由三层主题（`ai-tech` / `current-affairs` / `education`）回滚为**六主题**，补齐被删的引擎配套 / CI / 数据层，并完成 N0–N8 全流程接线。设计基线见 `engine/docs/architecture-and-pipeline-design.md`。

### 结构

- `engine/tools/layout.json` 升版 **v4.0**：六主题 `economy` / `tech` / `education` / `international` / `political` / `society`；维度顺序按主题声明（`economy` = `["region","category"]`，其余主题为 `["category","region"]`）。
- 内容归一化：`content/economy/real-estate/dubai/apartment` → `content/economy/dubai/apartment`；删除 `market-sizing` / `policy-analysis` 两条业务线；`engine/sources/` 子目录改名 `ai-tech` → `tech`、`current-affairs` → `economy`。
- **维度规则调整**：取消「category 必须先于 region」全局硬性规则（三层重构产物），改为按主题声明顺序校验；`validate_layout.py` / `validate.py` / `_common.py` / `structure-and-naming-spec.md` / `AGENTS.md` / `README.md` 同步。
- `pipeline_runner` 审计退出码语义修正：退出码 2 = 警告不阻断（原实现把非零一律当阻断）。

### 补齐

- 从 `1bb607c` 恢复 `engine/docs`(14) / `audit` / `report-audits` / `fact_cards` / `sources` / `quality` / `vocabulary/data` / `.github`(6 工作流 + 3 action) / 根文档 / hub / 状态文件。
- 恢复 27 份真实业务数据至 `data/processed/<业务线>/`；`check_links.py` 增运行期产出前缀白名单。
- 新增设计基线 `engine/docs/architecture-and-pipeline-design.md`（ARCHITECTURE-AND-PIPELINE-DESIGN v1.0）。

### 验证

`pipeline_runner run --from N0 --to N8` 全流程通过；`optimization_gate --probe` 0 阻断；unittest 395 通过；`validate_layout` / `validate` / `classify` / `page_build` / `check_links` / `build_hub --check` / `publish_fingerprint --check` 全 0。

### 提交

`c5056e9`（初始化 tech-context-digest：完整迁移核心代码与内容，已推送 `main`）。过程提交 `1f12b3e`（压平回滚）→ `0fd12b4`(P1) → `ca0ff0c`(P2+P3) → `355943f`(P4) 已压平。

## 2.0.0 — 2026-11-16：三层架构重构与仓库独立化

仓库迁移独立化为 **`tech-context-digest`**，并按「内容 / 引擎 / 资产」三层重构目录。

### 新增层

- **`content/`（内容层）**：三大主题 `ai-tech`（AI 科技）、`current-affairs`（时事）、`education`（教育，新建）。业务线统一 `content/<theme>/regional/<region>/<category>/`；主题级分类目录（`principles/`、`solutions/`、`macro/`、`finance/`、`real-estate/`、`weekly-brief/`、`deep-dives/`、`universities/` 等）承载全局 / 非区域内容。
- **`engine/`（引擎层）**：由原 `src/` 迁移并拆分——`templates/`（原 `report_templates/`）、`prompts/`（泛用提示词，自类型模板 `*/prompts/` 收口）、`sources/`（原 global/trends/sources）、`fact_cards/`、`vocabulary/`、`tools/`、`quality/`、`audit/`、`report-audits/`、`tests/`、`docs/`。
- **`data/`（资产层）**：`raw/`、`processed/<theme>/<region>/<category>/`（原各业务线 `data/` 与 global/trends/data 上移）、`assets/`。

### 业务线迁移（region-first）

| 旧路径 | 新路径 |
|---|---|
| `economy/dubai/apartment` | `content/economy/real-estate/apartment` |
| `economy/dubai/market-sizing` | `content/economy/real-estate/market-sizing` |
| `economy/dubai/policy-analysis` | `content/economy/real-estate/policy-analysis` |
| `economy/insight` | `content/economy/insight` |
| `economy/trends` | `content/economy/trends` |
| `technology/ai/dubai/competitive-intelligence` | `content/tech/regional/dubai/competitive-intelligence` |
| `technology/ai/dubai/industry-research` | `content/tech/regional/dubai/industry-research` |
| `technology/ai/dubai/security` | `content/tech/security/dubai` |
| `technology/ai/global/trends` | `content/tech/weekly-roundup` |

### 配套变更

- `engine/tools/layout.json` 升版 v2.0：主题改为 `ai-tech` / `current-affairs` / `education`，维度 `["region","category"]`，新增 `content_root` / `regional_segment`。
- `_common.py`：`iter_business_dirs` / `iter_theme_dirs` 改用内容层根；新增 `processed_data_dir()`。
- 工具链（`validate_layout` / `ensure_region_topics` / `source_check` / `metric_registry` / `build_hub` / `build_index` / `check_links` / `page_build_check` / `optimization_gate`）与 6 个 workflow 全部改为新路径。
- 业务线 `data/` 全部上移 `data/processed/<theme>/<region>/<category>/`；报告、提示词、模板、审计文档中的路径引用同步更新。
- 品牌引用 `MacroPulse` → `Tech Life Research`。
- 新增根 `README.md` 与本 `CHANGELOG.md`。
- 历史文档清理：删除 11 份 `business-prompt-scaffold.md`（内容并入 `engine/prompts/<类型ID>/` 泛用版）、4 份重构历史记录（两轮迁移方案 / 业务线整合说明 / 重构前基线快照）、一次性迁移工具 `engine/tools/rewrite_paths.py`；审计记录 `reviews/` 按当前报告路径重命名（保留证据），`semantic/` 旧路径重复副本清除；`template-registry.md` 目录树与类型 README 同步修正。

### 兼容性

- 旧路径迁移映射已在重构中完成，不再保留独立迁移工具。
- 历史审计记录为冻结留痕，不参与断链判定；迁移方案文档已清理。
