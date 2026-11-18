# 架构与全流程设计基线（ARCHITECTURE-AND-PIPELINE-DESIGN v1.1）

> **状态**：已批准，实施基线（P1–P4 按此执行）
> **日期**：2026-11-17
> **范围**：tech-context-digest 仓库在「回滚到六主题结构 + 可运行工具链」方向下的架构规划，以及 采集 → 筛选 → 分类 → 生产 → 渲染 → 校验 → 发布 → 运维 全流程落地。
> **上位约束**：本文件是 `report-pipeline-system.md`（REPORT-PIPELINE-SYSTEM v1.2）的**结构适配版**；节点 / 门禁编号（N0–N8 / G0–G8）与退回语义**保持不变**。

---

## 1. 目标与范围

### 1.1 目标

1. **结构统一**：把 `engine/tools/layout.json`（目录结构单一事实源）与磁盘 `content/` 统一为六主题结构，消除「工具发现 0 报告」的错位。
2. **补齐引擎**：补回被删的 `engine/docs`、`engine/audit`、`engine/report-audits`、`engine/fact_cards`、`engine/quality`，并适配新路径。
3. **补齐交付**：补回 `.github/` 工作流与 action、根文档（`AGENTS.md` / `README.md` / `INDEX.md` / `CHANGELOG.md`）、hub（`index.html` / `reader.html`）、状态文件（`automation-status.json` / `perf-status.json`）。
4. **接线全流程**：让 `pipeline_manifest.json`（N0–N8 + G0–G8）→ `pipeline_runner.py` → `optimization_gate.py` 真正可运行，报告风格对齐 `content/economy/dubai/apartment/reports/` 的 canonical 样式。

### 1.2 非目标（本期不做）

- 不恢复三层 `ai-tech` / `current-affairs` 结构（回滚方向保留）。
- 不做真实网络采集自动化与自动生成报告（N1 采集 / N4 生产为 **人工 + Agent 在环**，工具只做登记、校验、渲染、留痕）。
- 不重写业务提示词与报告内容。

---

## 2. 现状诊断（回滚前）

### 2.1 两个 `del` 提交

| 提交 | 内容 |
|---|---|
| `3307bea del` | 删除 `.github/` 全部 6 个工作流 + 3 个 action（9 文件） |
| `e87e082 del` | 删除 229 文件 + 54 纯改名：内容由三层 `ai-tech` / `current-affairs` 回滚为 `tech` / `economy`；删除 `engine/docs`(13)、`engine/audit`、`engine/report-audits`、`engine/fact_cards`、引擎层 sources、`engine/quality`、`engine/vocabulary/data`、根文档、hub、`data/processed` 全部数据 |

### 2.2 回滚前的阻断（实测）

`python engine/tools/optimization_gate.py --probe` → **4 项 ERROR**：`perf-status.json` 缺失、`engine/fact_cards` 不存在、`engine/report-audits/blind-spot-ledger.md` 不存在、审计记录缺失。

更隐蔽的阻断：`semantic_diff` / `research_kernel` / `info_density` / `classify` 均报 **「未发现报告」**——因为 `layout.json` 仍注册三层主题，与磁盘不匹配，`iter_business_dirs()` 发现不到业务线。

---

## 3. 目标架构

### 3.1 三层与主题

```
content/   内容层：<theme>/<维度段...>/  （业务线 = 含 prompts/business-config.md 的目录）
engine/    引擎层：tools / templates / prompts / vocabulary / audit / quality / report-audits / fact_cards / tests / docs
data/      资产层：raw / processed / assets （processed 统一收口于 data/processed/<theme>/<维度段...>）
```

六主题（`layout.json` 注册）：`economy`、`tech`、`education`、`international`、`political`、`society`。

### 3.2 layout.json v4.1（已落地）

业务线深度为「主题 + 维度段」，维度顺序按主题声明；`region` 为可选维度（`optional_dimensions`），缺省时业务线直接以 category 段落位：

```json
{
  "version": "4.1",
  "updated": "2026-11-17",
  "comment": "仓库目录结构单一事实源（content、engine、data 三层）。六主题：economy / tech / education / international / political / society。维度顺序按主题声明（economy 为 region→category，其余为 category→region）。region 为可选维度。",
  "root_reserved": ["content","engine","data",".github",".gitignore","AGENTS.md","README.md","CHANGELOG.md","requirements.txt","index.html","reader.html","INDEX.md","automation-status.json","perf-status.json"],
  "content_root": "content",
  "regional_segment": "",
  "themes": {
    "economy": { "name": "经济", "dimensions": ["region", "category"], "optional_dimensions": ["region"] },
    "tech": { "name": "科技", "dimensions": ["category", "region"], "optional_dimensions": ["region"] },
    "education": { "name": "教育", "dimensions": ["category", "region"] },
    "international": { "name": "国际", "dimensions": ["category", "region"] },
    "political": { "name": "政治", "dimensions": ["category", "region"] },
    "society": { "name": "社会", "dimensions": ["category", "region"] }
  },
  "regions": ["dubai"],
  "naming": { "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$", "max_depth": 6 }
}
```

**落地要点**：
- 原 `content/economy/real-estate/dubai/apartment` 归一化为 `content/economy/dubai/apartment`（`real-estate` 语义由 business-config 的 `{{TOPIC}}` 承载）；样式参照目录相应变为 `content/economy/dubai/apartment/reports/`。
- `validate_layout.py` 的「category 必须先于 region」全局硬性规则取消，改为**按主题声明顺序**校验（维度序列自洽：无重复、无未登记维度名）。理由：旧维度中 economy 本就是地区优先、tech 是细分优先，该统一规则是三层重构的产物。

### 3.3 目标目录结构

```
content/
  economy/
    <category>/              # region 缺省：insight（决策仪表盘）、trends（全球经济趋势周报）
    <region>/<category>/     # region=dubai：apartment（原 real-estate 板块）
  tech/
    <category>/              # region 缺省：weekly-roundup（AI 行业趋势周报）
    <category>/<region>/     # 如 security 与 dubai 的组合
  education/  international/  political/  society/     # 空占位（.gitkeep）
```

每个业务线目录内：`prompts/`（business-config + 周期提示词）、`reports/`（canonical HTML）、`sources/`（可选 md 源稿）、`script/`（可选）。

### 3.4 命名规范

沿用 STRUCTURE-AND-NAMING-SPEC 口径：目录 kebab-case；报告 `<period>_<cycle>.html`（基线 `_baseline_report.html`）；提示词 `business-config.md` + `prompt-<cycle>.md`；模板 `prompt-<cycle>-template.md`；数据主体 snake_case + 可选周期后缀。

### 3.5 部署架构（静态交付 + CI 编排）

本仓库不是运行态服务，部署架构由「静态交付物 + 工具链 + CI 编排」构成：

| 层 | 载体 | 说明 |
|---|---|---|
| 交付物 | 自包含 HTML（报告 + `index.html` / `reader.html` / `INDEX.md`） | CSS/JS 内联，ECharts 走 CDN 白名单；无服务端渲染 |
| 发布源 | GitHub `main` 分支（仓库根 + `content/**/reports/`） | 分支保护（必需检查 + strict）；不直推，经 PR 合并 |
| 构建 | `engine/tools/{md2html,build_hub,build_index,publish_fingerprint,archive_reports}.py` | 本地或 CI 生成，确定性（无时间戳） |
| 托管 | 静态站点托管（GitHub Pages / 任意静态服务器），入口 `index.html` | 无数据库 / 无运行态进程 / 无外部服务依赖 |
| CI 编排 | `.github/workflows/{ci,html-sync,content-update,scheduled-maintenance,audit,webhook-alert}.yml` + `.github/actions/{submit-pr,workspace-cleanup,remediation-ticket}` | 提交 → 门禁 → PR → 合并 → 自动发布 |
| 环境 | 本地 Windows（Python 3.12）+ CI `ubuntu-latest`（Python 3.12） | 依赖仅 `requirements.txt`；发布用 `gh`（GitHub 托管） |
| 数据流 | `data/raw/` → `data/processed/<theme>/<维度段>/` → `content/<theme>/<维度段>/reports/` → hub / INDEX | 地区分组段不计入 processed |
| 回滚 / 留痕 | Git 历史 + `engine/audit/records/publish_fingerprints.json` + `archive_reports` 归档 + `pipeline_runs.jsonl` | 任一发布可经指纹比对与 Git 回退 |

**部署约束**：不引入运行态服务 / 容器 / 数据库；所有发布产物必须确定性可重放（`build_hub --check` / `publish_fingerprint --check` 门禁）；发布动作统一经 `repo_sync` / `submit-pr`，禁止直推 `main`。

---

## 4. 全流程设计（N0–N8 + G0–G8）

节点 / 门禁编号、退回语义**完全沿用** `pipeline_manifest.json` 与 `report-pipeline-system.md` v1.2，本节只补充「在本仓库如何落地」。

### 4.1 节点 - 门禁总表

| 节点 | 名称 | driver | 落地载体（本仓库） | 门禁 | 门禁检查项 |
|---|---|---|---|---|---|
| N0 | 需求与配置 | manual | business-config + `layout.json` | G0 | validate_layout, validate, region_topics |
| N1 | 信息采集 | manual | `source_check.py`（源注册表 / 死链 / 覆盖）+ `release_calendar.py` + `metric_registry.py` | G1 | source_check, release_calendar, metric_registry |
| N2 | 信息筛选与分级 | semi | `source_check.py --probe`（双源 / 分级 / 死链） | G2 | source_check(--probe) |
| N3 | 信息分类 | tool | `classify_reports.py` + `layout.json` + `check_links.py` | G3 | validate_layout, classify, links |
| N4 | 内容生成 | manual | 四层提示词体系（通用基座 × 通用规范 × 类型模板 × business-config） | G4 | research_kernel, info_density, fact_card, decision_hub, blind_spot |
| N5 | 渲染与交付 | tool | `md2html.py` + `report_style.py`（canonical 样式）+ `page_build_check.py` | G5 | page_build, lint, compliance, perf_monitor |
| N6 | 质量校验与审计 | tool | `optimization_gate.py`（全量 28 项）+ `audit_tool.py`（审计四环节） | G6 | `*` + 审计 |
| N7 | 发布 / 索引 / 归档 | tool | `publish_fingerprint.py` + `build_hub.py` + `archive_reports.py` | G7 | hub, publish_fingerprint |
| N8 | 运维与监控 | ci | `.github/workflows/` 下的维护 / 内容 / 审计流水线 | G8 | （外部 CI） |

### 4.2 关键节点细化

**N1 信息采集（manual）**
- 输入：业务线 `prompts/business-config.md` 的 `{{SOURCE_REGISTRY_PATH}}`。
- 动作：Agent / 人按来源分级（Tier1–Tier5）检索 → 登记到 `data/processed/<theme>/<维度段...>/source_registry.json` 与指标登记册（xlsx / md-table / md-ledger）。
- 工具：`source_check.py`（源覆盖 / 死链 / 分级校验）、`release_calendar.py`（未来发布计划）、`metric_registry.py`（指标口径登记）。
- 留痕：`engine/audit/records/pipeline_runs.jsonl`（由 runner 写）。

**N2 信息筛选与分级（semi）**：`source_check.py --probe` 对登记来源做双源核验、死链、分级合规；不通过回 N2。

**N3 信息分类（tool）**：`classify_reports.py` 按 `layout.json` 维度归位、校验报告类型 / 节拍；`check_links.py` 验链。

**N4 内容生成（manual）**：按四层提示词体系撰写；`research_kernel` / `info_density` / `fact_card` / `decision_hub` / `blind_spot` 五门禁左移校验。

**N5 渲染与交付（tool）**：`md2html.py` 输出 canonical 结构；`report_style.py` 提供 canonical CSS（navy `#16324f` 等）；`page_build_check.py` 15 项 P0/P1 校验。报告风格**完全参照** `content/economy/dubai/apartment/reports/` 现有 4 份：`report-head`/`hero` 页头、`nav-tabs`、`h2.sec`、`table.fixed` + `scope`、`src-head`/`src-pop` 引用弹层，结尾为 `<footer>` 免责 / 版本段（`.refs`/`.disc` 属 canonical 组件库，定义在 `report_style.py`，供其它报告使用；apartment 4 份未使用这两个类）。

### 4.3 数据层流转

```
data/raw/<theme>/...          原始采集（PDF / JSON / md）
data/processed/<theme>/...   登记册 + source_registry.json + 清洗数据
data/assets/<theme>/...       图片 / 图表资源
```

`data/processed` 由 `layout.processed_data_dir(business_rel)` 统一推导，业务线内不再存数据。运行期产出（登记册 / 来源注册表 / 快照）在 `check_links.py` 中以白名单前缀声明为「基线可缺」。

### 4.4 闭环

- **L1（异步）**：N8 → 心跳 / 任务清单 → N1。
- **L2（同步）**：G6 阻断 → 携上下文退回 N4。

---

## 5. 补齐与对齐清单

| 类别 | 处理方式 |
|---|---|
| `engine/docs/` | 恢复 13 份并适配路径；本文件为结构适配设计基线 |
| `engine/audit/` | 恢复结构（README / prompts / records）；历史记录文件名保留 |
| `engine/report-audits/` | 恢复；路径引用改六主题 |
| `engine/fact_cards/` | 恢复 |
| `engine/quality/` | 恢复（含 rubric / chaos-taxonomy / repair-sop / ops-guide / manifest.schema.json / prompts） |
| `engine/vocabulary/data/` | 恢复主题词库（economy / tech / education / international / political / society + imports/exports；economy、tech 为归并后词库） |
| `.github/` | 恢复 6 工作流 + 3 action；按新结构校准路径 |
| 根文档 / hub / 状态文件 | 恢复并重新生成（`build_hub.py` / `automation_status.py` / `perf_monitor.py`） |
| `data/processed/` | 运行期产出，基线可缺（白名单前缀）；业务线首次采集时落盘 |
| 7 份 `business-config.md` | 改写旧路径引用（内容路径、数据路径、相对深度） |

---

## 6. 分阶段实施计划

| 阶段 | 内容 | 出口标准 |
|---|---|---|
| **P1 结构对齐** ✅ | layout.json v4.0；apartment 归一化；全量旧路径改写；维度校验放宽 | `validate_layout` / `validate` / `classify_reports` 通过；工具发现 7 条业务线 / 10 份报告 |
| **P2 补齐引擎** ✅ | 恢复 docs / audit / report-audits / fact_cards / quality / vocabulary 并适配 | `optimization_gate --probe` 的错误清零（仅剩运行期数据 / 交付物） |
| **P3 数据与交付** ✅ | 恢复 `.github`；重建 hub 与根文档；data 层骨架 | `build_hub --check` 通过；CI 工作流可跑 |
| **P4 接线验证** ✅ | `pipeline_runner` N0–N8 全流程试跑；`engine/tests` 回归 | unittest 全绿；`optimization_gate` 0 阻断；`run --from N0 --to N8` `outcome=passed` |

---

## 7. 决策记录

- **D1 维度方案**：方案 A（归一化目录，apartment 迁至 `content/economy/dubai/apartment`）。
- **D2 空主题**：保留注册（`education` / `international` / `political` / `society`），便于扩展。
- **D3 数据层**：运行期产出，基线只建骨架 + 白名单；不编造数值。
- **D4 旧审计记录**：`engine/audit/records/**` 为冻结留痕，保留历史文件名，不参与断链判定。
- **D5 提交策略**：压平本地未推送的 `del` 提交，从 `1bb607c` 起干净提交。

---

## 8. 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-17 | 初始版本 | 六主题三层结构、layout.json v4.0、N0–N8 / G0–G8 落地、P1–P4 计划 |
| v1.1 | 2026-11-17 | 补齐部署架构 | 新增 §3.5 部署架构（静态交付 + CI 编排）；P3 / P4 标记完成；交叉引用 REPORT-PIPELINE-SYSTEM v1.2 |

---
*按 P1→P4 执行；每阶段结束跑对应校验并汇报。全维度覆盖映射见 [end-to-end-coverage.md](./end-to-end-coverage.md)。*
