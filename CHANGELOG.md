# 变更记录

本文件记录仓库的结构与规范级变更（报告内容变更见各业务线 `reports/`）。

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
