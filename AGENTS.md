## Agent skills

### Issue tracker

Issues and specs live as GitHub issues (uses the `gh` CLI). See `engine/docs/agents/issue-tracker.md`.

### Triage labels

Five canonical triage roles, label strings equal to role names. See `engine/docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` + `engine/docs/adr/` at the repo root. See `engine/docs/agents/domain.md`.

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

- **设计系统**：只用 canonical 令牌（`--navy:#16324f` 等，事实源 `engine/tools/report_style.py` 与 `build_hub.py`）；禁止私建主色 / 私有样式分支（漂移色 `#1f3d63` / `#123a5c` / `#1a1a2e` / `#16213e` 直接判错）。
- **结构**：报告统一 `header.report-head`/`.hero` + `nav.report-nav`（`.nav-url` + `.nav-tabs`）+ `main.wrap` + `h2.sec`；hub 沿用既有骨架；新主题不得另创同义类名。
- **可访问性 / 兼容性**：`lang`/`viewport`/`.skip-link`/焦点环/`prefers-reduced-motion`/`@media print` 为强制项。
- **门禁**：`python engine/tools/page_build_check.py` 必须零 `[E]`；新增组件先并入 `report_style.py`；生成物必须确定性（无时间戳）。
- **CI**：ci.yml / html-sync / scheduled-maintenance / content-update 均含该门禁，[E] 阻断合并与提交。

## 信息分层与决策交付（硬性约束，适用于任何 Agent 平台）

所有报告必须遵循 **`engine/templates/information-layering-spec.md`（INFORMATION-LAYERING-SPEC v1.0）** 与 **`engine/templates/decision-delivery-spec.md`（DECISION-DELIVERY-SPEC v1.0）**：

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层（逻辑）/ 原始层（台账与来源）；共享 boilerplate（来源分级规则、口径声明模板、研究局限模板）上移至通用基座第十节，报告正文只写专属口径与前提假设。
- **信息等级**：关键信息标注 `已核验 / 部分核验 / 推断 / 假设`；决策摘要仅允许已核验 + 部分核验；market-sizing 数值必须标「假设乘积」并区间化。
- **新增信息模块**：报告开头输出「本期新增 X / 修正 Y / 无变化 Z / 假设核验进度 k/n」。
- **单一事实源 + 指针**：事实唯一定义于台账 / 登记册 / 事实卡片（`engine/fact_cards/`，`[FC-…]` 引用），正文用「指标编号 + 指针」，删除同义复述。
- **决策卡与行动协议**：核心判断输出决策卡（结论 / 证据强度 / 触发条件 / 反向证据 / 信息充分度）；行动项按「触发条件 + 阈值 + 责任角色 + 时限 + 验证指标」并分三档优先级（立即行动 / 持续观察 / 仅记录存档）。
- **阈值校准**：首次中期回测 2027-06；校准完成前信号灯标注「预校准（ex-ante）」。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」；仅核心事实修正才升级版本号。
- **门禁**：`info_density_check.py` / `fact_card_check.py` / `decision_hub_check.py` / `blind_spot_check.py` 纳入 `optimization_gate.py` 统一入口；新报告缺项 = [E] 阻断，历史报告 = [W]。
- **阶段复用（硬性）**：四门禁与全部 P0/P1/P2 确定性检查必须由 `optimization_gate.py` 统一承载（P1-2 去重）；`ci.yml` / `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml` 一律只调用该入口（`--probe`），不得分项重复扫描；阶段 × 复用映射见 `engine/docs/report-process-reuse.md`；一致性由 `engine/tests/test_process_gates.py` 强制（缺一阶段即失败）。

## 优化流程门禁（硬性约束，适用于任何 Agent 平台）

P0/P1/P2 优化清单（邻近判定 / 机构分级主数据 / 指标字典 / gate-period / 分类口径 / R5 token 化 / URL 探测 / 发布日历 / 去重血缘 / 类型双校验 / 全量准确性兜底 / 覆盖率 / 发布指纹 / 分类边界）的全部确定性检查收敛为**单一入口** `engine/tools/optimization_gate.py`，后续所有阶段必须复用，不得另写一套：

- **本地提交**：`python engine/tools/repo_sync.py run --message ... --paths ... --gate`（统一门禁 [E] 直接拒绝提交）。
- **CI / 自动提交**：`ci.yml` / `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml` 均含「优化流程一致性门禁（统一入口）」步骤。
- **审计**：`audit.yml` 四环节 fail-fast（[E] 即阻断，不再告警后放行）；`audit_tool.py verify` 内含 `source_check`。
- **一致性校验**：`engine/tests/test_process_gates.py::TestOptimizationGateReuse` 强制各阶段复用；阶段 × 复用映射见 `engine/docs/report-process-reuse.md` 第三节。
- **全链路体系**：信息录入 → 校验 → 更新 → 生成 → 发布的全链路节点、五道防线、两级 gate-period 与闭环联动见 `engine/docs/report-pipeline-system.md`（REPORT-PIPELINE-SYSTEM v1.2，门禁左移：N0–N5 各阶段就地门禁 G0–G5，N6 统一门禁 + 审计兜底）；文档与门禁清单数量由 `engine/tests/test_pipeline_system_doc.py` 锁定。
- **端到端编排（硬性约束）**：流程图落地为 `engine/tools/pipeline_manifest.json`（声明式 N0–N8 / G0–G8 图 + L1/L2 闭环）+ `engine/tools/pipeline_runner.py`（节点→门禁→路由/退回，复用统一门禁单一入口）+ `engine/tools/pipeline_audit.py`（追加式留痕）；方案与任务清单见 `engine/docs/report-pipeline-implementation-plan.md`；一致性由 `engine/tests/test_pipeline_runner.py` 锁定（9 节点 / 9 门禁 / G6→N4 / N8→N1）。

## 报告生成规则（硬性约束，适用于任何 Agent 平台）

1. **触发词「执行xx报告」**：用户说「执行xx报告」（如「执行 AI 安全周报」）时，视为完整下达报告生成指令，须严格遵循对应模板/提示词的全部规范执行，无需用户重复说明：①先定位并读取该报告对应类型模板与业务提示词（含 business-config 单一事实源）作为唯一规范依据；②内容结构、章节层级、格式排版、数据呈现方式、术语标准、输出格式全维度对齐模板，不得出现结构偏差、格式错乱、内容遗漏或任何不符合规范的自定义调整；③生成完成后逐项对照模板交叉校验，确认所有规范要求满足，保证规范性、一致性与合规性后才交付。

2. **触发词「执行报告」（简短形式，与规则 1 等效）**：用户只说「执行报告」而未指明具体报告时，同样视为完整报告生成指令，按规则 1 的全流程执行；报告对象按上下文最近提及的报告/当前打开的业务线确定，无法确定时向用户确认一次后立即执行，不做任何超出模板规范的自定义调整。

## 多会话 Git 协作（硬性约束，适用于任何 Agent 平台）

多个 Agent 会话与多个 CI 工作流共用同一 `main`，必须遵守 **`engine/docs/multi-session-git-protocol.md`（MULTI-SESSION-GIT-PROTOCOL v1.4）**：

- **禁止直推 `main`**：任务一律在 `task/<slug>` 分支提交，经 PR 合并；直推 `main` 会与其他会话/CI 竞争并触发 non-fast-forward。
- **统一网关**：提交/推送使用 `python engine/tools/repo_sync.py`（`run` / `push` / `pr`），它提供共享检出锁、推送前 `fetch --rebase`、直推 `main` 守卫。
- **钩子**：本克隆启用 `core.hooksPath=.githooks`，pre-push 直推 `main` 会被阻断（v1.2 起按 refspec 判定：即使站在 `task/*` 显式 `git push origin main` 也阻断）。
- **CI 也走 PR**：`audit.yml` / `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml` 不再直推 `main`，统一经 `.github/actions/submit-pr` 开 PR + 自动合并；`main` 启用分支保护（必需检查 + strict）。

## 工作区清理（硬性约束，适用于任何 Agent 平台）

**单一入口** `engine/tools/workspace_cleanup.py`（复合动作 `.github/actions/workspace-cleanup`）负责缓存 / 临时 / 构建产物清理，各阶段一律复用，不得另写一套：

- **只删未被 git 跟踪的路径**：跟踪集合取自 `git ls-files`；被跟踪文件 / 目录（含其内部）一律跳过，绝不删版本控制内容；默认跳过 `.git`。删除操作前必须确认目标未跟踪。
- **覆盖范围**：`__pycache__/`、`*.pyc/pyo/pyd`、`.pytest_cache/`、`.ruff_cache/`、`.mypy_cache/`、`.coverage`、`htmlcov/`、`*.egg-info/`、`.eggs/`、`build/`、`dist/`、`.automation-tmp/`、`.screenshots/`、`.trae-html-share-packages/`、`*.html.tmp`、`*.tmp`（`--deep` 才含虚拟环境）。
- **CI 全流程自动触发**：`ci.yml` / `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml` / `audit.yml` 每个作业在**阶段开始前（预清理）**与**阶段结束后（收尾清理，`if: always()`）**调用；`submit-pr` 在 `git add` 前清理；`pre-push` 钩子在推送网关前清理。新增工作流 / 作业须沿用同一复合动作，不得省略。
- **确定性**：输出排序、无时间戳，重复执行结果一致（幂等）；清理失败逐项容错，不掩盖。
- **审计流水轮转**：`pipeline_audit.py --rotate`（超量归档 + 只保留最近 5 份）由 `scheduled-maintenance` 每周执行，防止 `pipeline_runs.jsonl` 无限增长。
- **门禁归属**：清理属工作区维护，**不得**并入 `optimization_gate` 门禁清单（其 21 项数量由 `engine/tests/test_pipeline_system_doc.py` 锁定）。
