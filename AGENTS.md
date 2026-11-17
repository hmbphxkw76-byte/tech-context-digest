## Agent skills

### Issue tracker

Issues and specs live as GitHub issues (uses the `gh` CLI). See `engine/docs/agents/issue-tracker.md`.

### Triage labels

Five canonical triage roles, label strings equal to role names. See `engine/docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` + `engine/docs/adr/` at the repo root. See `engine/docs/agents/domain.md`.

## 规范分层（硬性约束，适用于任何 Agent 平台）

`AGENTS.md` 只保留**硬性约束 + 指针**；实现细节、清单、阈值与操作手册下沉到专用规范（`engine/docs/`、`engine/templates/`、`engine/audit/`）。新增规范内容遵循「新增即删旧」：每新增一层表述，同步删除等量旧表述，避免复述漂移。

## 仓库三层架构（tech-context-digest）

仓库名 `tech-context-digest`，按三层组织，**不得跨层存放**：

- **`content/` — 内容层**：六主题 `economy`（经济）/ `tech`（科技）/ `education`（教育）/ `international`（国际）/ `political`（政治）/ `society`（社会）。业务线位于 `content/<theme>/<维度段...>/`，维度顺序由 `engine/tools/layout.json` 各主题声明（`economy` 为 `<region>/<category>` 地区优先，其余主题为 `<category>/<region>` 细分优先），以 `prompts/business-config.md` 为锚点；主题级分类目录（如 `content/tech/principles/`）承载非区域 / 全局内容。
- **`engine/` — 引擎层**：跨主题复用的机械与规范——`templates/`、`prompts/`（泛用提示词）、`tools/`、`vocabulary/`、`quality/`、`audit/`、`report-audits/`、`fact_cards/`、`sources/`（通用层源稿，按主题）、`tests/`、`docs/`。
- **`data/` — 资产层**：`raw/`（原始抓取）、`processed/<theme>/<维度段...>/`（清洗后台账 / 登记 / 量化数据，地区分组段不计入）、`assets/`（图片图表）。

## 目录结构硬性规则（适用于任何 Agent 平台）

**维度顺序由 `layout.json` 各主题自行声明，不得在未改 `layout.json` 的情况下倒置。**

- 业务线默认路径为 `content/<theme>/<维度段...>/`；主题注册在 `engine/tools/layout.json`。维度先后按主题声明：`economy` 为 `["region", "category"]`，`tech` / `education` / `international` / `political` / `society` 为 `["category", "region"]`；`regional_segment` 为空串（无独立地区分组段，region 直接作为维度段）。
- 新增主题 / 业务线时，必须在 `engine/tools/layout.json` 的 `themes` 中登记并显式声明 `dimensions`；地区段必须命中 `regions` 白名单（当前 `dubai` / `global`）。
- 任何涉及维度判断、维度排序、维度筛选的逻辑（业务线发现、结构校验、报告归位、索引、汇总页、筛选栏等）都必须符合声明顺序。
- 专项校验：`engine/tools/validate_layout.py` 的 `check_dimension_priority()` 校验维度序列自洽（无重复、无未登记维度名）；`engine/tests/test_tools.py::TestDimensionOrder` 在声明与实例两个层面校验。新增代码须保持该校验，不得绕过或降级。（历史规则「category 必须先于 region」随三层重构回滚取消，见 `engine/docs/architecture-and-pipeline-design.md`。）

## 目录结构与命名规范（硬性约束，适用于任何 Agent 平台）

所有目录与文件命名必须遵循 **`engine/docs/structure-and-naming-spec.md`（STRUCTURE-AND-NAMING-SPEC v1.0）**：

- **模块边界**：业务专属 → `content/`；跨主题复用（模板 / 提示词 / 工具 / 词库 / 质量 / 审计）→ `engine/`；数据资产 → `data/`；机器生成留痕 → `engine/audit/records/`。
- **目录命名**：kebab-case（正则见 `layout.json` 的 `naming.pattern`）；Python 包目录用 snake_case；深度上限 `naming.max_depth=6`；**维度顺序按主题声明**（见上）。
- **文件命名**：报告 `<period>_<cycle>.html`；提示词 `business-config.md` + `prompt-<cycle>.md`；模板 `prompt-<cycle>-template.md`；Python 用 snake_case；数据主体用 snake_case + 可选周期后缀；文档 / 配置 / CI 用 kebab-case。
- **生成物豁免**：`engine/audit/records/**`、`engine/vocabulary/data/**`、`data/raw/**` 按生成器模式命名，必须确定性可重放，不得手工编辑。
- **legacy 冻结**：`engine/fact_cards/`、`engine/tools/institution_tiers.json`、`engine/tools/pipeline_manifest.json`、`engine/quality/manifest.schema.json` 等历史项不强制改名；**新增文件必须合规**。
- **反例清单**：见规范第十节；新增文件提交前按第十二节 Checklist 核对。

## 页面构建规范（硬性约束，适用于任何 Agent 平台）

所有 HTML 页面（hub / 报告 / 新主题）必须遵循 **`engine/docs/page-build-spec.md`（PAGE-BUILD-SPEC v1.0）** 与 **`engine/docs/page-build-governance.md`**：

- **设计系统**：只用 canonical 令牌（事实源 `engine/tools/report_style.py` 与 `build_hub.py`）；漂移色直接判错。
- **结构**：报告统一 `header.report-head`/`.hero` + `nav.report-nav` + `main.wrap` + `h2.sec`；hub 沿用既有骨架；新主题不得另创同义类名。
- **可访问性 / 兼容性 / 性能 / 打印**：`lang`/`viewport`/`.skip-link`/焦点环/`prefers-reduced-motion`/`@media print` 为强制项；预算与断点以下位规范为准。
- **门禁**：`python engine/tools/page_build_check.py` 必须零 `[E]`；新增组件先并入 `report_style.py`；生成物确定性（无时间戳）。
- **CI**：ci.yml / html-sync / scheduled-maintenance / content-update 均含该门禁，[E] 阻断合并与提交。

## 信息分层与决策交付（硬性约束，适用于任何 Agent 平台）

所有报告必须遵循 **`engine/templates/information-layering-spec.md`（INFORMATION-LAYERING-SPEC v1.0）** 与 **`engine/templates/decision-delivery-spec.md`（DECISION-DELIVERY-SPEC v1.0）**：

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层（逻辑）/ 原始层（台账与来源）；共享 boilerplate 上移至通用基座第十节。
- **信息等级**：关键信息标注 `已核验 / 部分核验 / 推断 / 假设`；决策摘要仅允许已核验 + 部分核验；market-sizing 数值标「假设乘积」并区间化。
- **新增信息模块**：报告开头输出「本期新增 X / 修正 Y / 无变化 Z / 假设核验进度 k/n」。
- **单一事实源 + 指针**：事实唯一定义于台账 / 登记册 / 事实卡片（`engine/fact_cards/`，`[FC-…]`），正文用「指标编号 + 指针」。
- **决策卡与行动协议**：核心判断输出决策卡（结论 / 证据强度 / 触发条件 / 反向证据 / 信息充分度）；行动项五要素 + 三档优先级。
- **阈值校准 / 版本治理**：首次中期回测 2027-06；校准前标「预校准（ex-ante）」；核验型运行不升级版本号。
- **门禁**：`info_density_check.py` / `fact_card_check.py` / `decision_hub_check.py` / `blind_spot_check.py` 纳入 `optimization_gate.py` 统一入口；新报告缺项 = [E]，历史 = [W]。

## 优化流程门禁（硬性约束，适用于任何 Agent 平台）

P0/P1/P2 优化清单的全部确定性检查收敛为**单一入口** `engine/tools/optimization_gate.py`（23 项），后续所有阶段必须复用，不得另写一套：

- **本地提交**：`python engine/tools/repo_sync.py run --message ... --paths ... --gate`（统一门禁 [E] 直接拒绝提交）。
- **CI / 自动提交**：`ci.yml` / `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml` 一律只调用该入口（`--probe`），不得分项重复扫描。
- **审计**：`audit.yml` 四环节 fail-fast；`audit_tool.py verify` 内含 `source_check`。
- **一致性校验**：`engine/tests/test_process_gates.py::TestOptimizationGateReuse` 强制各阶段复用；阶段 × 复用映射见 `engine/docs/report-process-reuse.md`。
- **全链路体系**：N0–N8 / G0–G8 / 两级 gate-period / 闭环联动见 `engine/docs/report-pipeline-system.md`；文档与门禁清单数量由 `engine/tests/test_pipeline_system_doc.py` 锁定。
- **端到端编排**：`engine/tools/pipeline_manifest.json` + `engine/tools/pipeline_runner.py` + `engine/tools/pipeline_audit.py`；一致性由 `engine/tests/test_pipeline_runner.py` 锁定。

## 任务级闭环（适配 mainline）（硬性约束，适用于任何 Agent 平台）

**主体保留、增量吸收**：保留现有 N0–N8 体系为主体，选择性接入 mainline 的任务级闭环机制（计划工件 / 本地 mainline 编排 / 完成前证据索引）；**禁止整体替换为 mainline 11 阶段**，禁止引入 `tag` / `changelog` / `RELEASES.md`。依据见 [mainline 规范适配性评估](engine/report-audits/mainline-adoption-assessment-2026-11-17.md) 与 [覆盖矩阵](engine/report-audits/mainline-adoption-coverage-matrix.md)。

- **N0.5 任务计划子节点**：任务计划作为 N0 之后的子节点，映射与流程图见 [report-pipeline-system.md](engine/docs/report-pipeline-system.md) §N0.5；其余 N0–N8 与 G0–G8 不变。
- **工件位置与 schema**：`engine/audit/records/` 下的 `tasks/<slug>/`，含 `plan.json` / `tasks.json` / `risks.json` / `task-start.md`；schema 由 `engine/tools/task_plan.py` 单一事实源定义，其余位置只指针。
- **复用入口（不得另写一套）**：统一门禁 `engine/tools/optimization_gate.py`；提交网关 `engine/tools/repo_sync.py`；端到端编排 `engine/tools/pipeline_runner.py`；一键闭环 `engine/tools/local_mainline.py`（薄封装，只编排）；审计 `engine/audit/scripts/audit_tool.py`。
- **工件即门禁输入**：受管 `task/*` 分支无 `plan.json` 不得执行 `repo_sync run --gate`（应急需显式 `--allow-no-plan` 并人工确认）。
- **确定性**：任务工件不得嵌入时间戳 / mtime；`task_plan.py check --slug <slug>` 必须可重放。
- **内容线不强制 TDD**：TDD 仅建议引擎线遵循；报告内容生成不强制红-绿-重构。

## 报告生成规则（硬性约束，适用于任何 Agent 平台）

1. **触发词「执行xx报告」**：用户说「执行xx报告」（如「执行 AI 安全周报」）时，视为完整下达报告生成指令，须严格遵循对应模板/提示词的全部规范执行，无需用户重复说明：①先定位并读取该报告对应类型模板与业务提示词（含 business-config 单一事实源）作为唯一规范依据；②内容结构、章节层级、格式排版、数据呈现方式、术语标准、输出格式全维度对齐模板，不得出现结构偏差、格式错乱、内容遗漏或任何不符合规范的自定义调整；③生成完成后逐项对照模板交叉校验，确认所有规范要求满足，保证规范性、一致性与合规性后才交付。

2. **触发词「执行报告」（简短形式，与规则 1 等效）**：用户只说「执行报告」而未指明具体报告时，同样视为完整报告生成指令，按规则 1 的全流程执行；报告对象按上下文最近提及的报告/当前打开的业务线确定，无法确定时向用户确认一次后立即执行，不做任何超出模板规范的自定义调整。

## 多会话 Git 协作（硬性约束，适用于任何 Agent 平台）

多个 Agent 会话与多个 CI 工作流共用同一 `main`，必须遵守 **`engine/docs/multi-session-git-protocol.md`（MULTI-SESSION-GIT-PROTOCOL v1.5）** 与 **`engine/docs/branch-naming-and-lifecycle.md`（BRANCH-NAMING-SPEC v1.0）**：

- **禁止直推 `main`**：任务一律在 `task/<slug>-<session8>` 分支提交，经 PR 合并。
- **统一网关**：提交/推送使用 `python engine/tools/repo_sync.py`（run / push / pr / branch / branch-rename / branch-audit）。
- **分支命名**：受管分支 `task/*` 必须内嵌会话标识；建分支用 `repo_sync.py branch <slug>`；`main` 与 `ci/*` 豁免。
- **钩子**：`core.hooksPath=.githooks`（安装：`repo_sync.py hook-install`）；pre-push 按 refspec 判定，pre-commit 在违规受管分支上阻断。
- **CI 也走 PR**：audit.yml / html-sync.yml / content-update.yml / scheduled-maintenance.yml 经 `.github/actions/submit-pr` 开 PR + 自动合并；`main` 启用分支保护。

## 工作区清理（硬性约束，适用于任何 Agent 平台）

**单一入口** `engine/tools/workspace_cleanup.py`（复合动作 `.github/actions/workspace-cleanup`）负责缓存 / 临时 / 构建产物清理，各阶段一律复用：

- **只删未被 git 跟踪的路径**：跟踪集合取自 `git ls-files`；删除前必须确认目标未跟踪。
- **覆盖范围 / 豁免**：见工具 `--help` 与 `engine/docs/structure-and-naming-spec.md`；生成物豁免路径不清理。
- **CI 全流程自动触发**：各工作流预清理 + 收尾清理（`if: always()`）；`submit-pr` 在 `git add` 前清理。
- **确定性 / 门禁归属**：输出排序、无时间戳、幂等；不得并入 `optimization_gate` 门禁清单。
