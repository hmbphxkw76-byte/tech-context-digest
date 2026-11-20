# 验证报告（VERIFICATION-REPORT v1.0）

> 日期：2026-11-19｜范围：优化解决方案 v2.0 第一波并发实施（T-01 / T-02 / T-03）
> 判级：`已核验`（命令实测）/ `部分核验`（抽样）/ `推断` / `假设`
> 对齐协议：[优化解决方案与实施清单 v2.0](optimization-solution-and-implementation-checklist-2026-11-19.md) §5.1

## 1. 双向追溯

| 方案条目 | 实施工件 | 验收证据 | 判定 |
|---|---|---|---|
| T-01 | `task/source-evidence-a1e5c9f2` @ `7d43984` | `unittest engine.tests.test_source_check` 82 OK；`optimization_gate --only source_check` 0 `[E]`；登记样本含 `evidence` | 已闭环 |
| T-02 | `task/proxy-calibration-b2f6d0a3` @ `c6508ec` | `test_proxy_calibration` 29 OK；IGI-05 试跑 precision 0.802 / recall 0.9875 / F1 0.8851（合成真值演示，非校准值） | 已闭环 |
| T-03 | `task/finding-rule-c3a7e1b4` @ `356ec38` | `test_finding_rule` 18 OK；14 项 finding 映射率 100%；`match` 命中 13 条 | 已闭环 |

## 2. 不引入新问题 · 回归结果

| # | 回归项 | 结果 | 判级 |
|---|---|---|---|
| R-REG-1 | 统一门禁 | 0 `[E]` / 8 `[W]`（新增 1 项 evidence 覆盖 `[W]`，已登记） | 已核验 |
| R-REG-2 | 单元测试 | `Ran 748 tests … OK (skipped=1)`（≥684） | 已核验 |
| R-REG-3 | 指标体检 | measured 38；不达标 1（I-08）；IGI-08 = 0.9945 | 已核验 |
| R-REG-4 | 审计登记 | 未逐项复跑（本波无新增报告） | 假设 |
| R-REG-5 | 链接 / 死链 | `check_links` 通过 | 已核验 |
| R-REG-6 | 发布指纹 | 漂移 5 份，`git diff origin/main` 为空 → **既有问题**（`c44174e`），非本次引入 | 已核验 |
| R-REG-7 | 结构 / 页面 | 未逐项复跑（本波无页面改动） | 假设 |
| R-REG-8 | 信息差指数 | IGI-08 = 0.9945（未退化） | 已核验 |
| R-REG-9 | 文档一致性 | naming / prompt_consistency / model_contract 均 0 警告 | 已核验 |
| R-REG-10 | 可回滚 | 三分支独立、已 `--no-ff` 合并，可 `git revert` | 已核验 |

## 3. 并发执行方式

- 三个 Agent 各自独立 git worktree + 独立分支，文件集互不重叠（`source_check.py` / `proxy_calibration.py`+字典 / `finding_rule.py`+audit）。
- 冲突：`metrics-dictionary.json`（T-01 `note` × T-02 `calibration`）→ 人工并集消解，保留双方字段。
- 合并顺序 T-01 → T-02 → T-03，`--no-ff` 保留合并记录。

## 4. 遗留 / 后续

- T-04…T-10 待后续波次（内容侧为主）。
- I-08 盲区消号仍阻塞（→ 2027-03）。
- 既有指纹漂移建议单独立项修复（`publish_fingerprint --emit` 重采 + CI 接线）。

## 5. 第二波（T-04 / T-05 / T-06 / T-07）验证

### 5.1 双向追溯

| 方案条目 | 实施工件 | 验收证据 | 判定 |
|---|---|---|---|
| T-04 | `task/research-kernel-d4b8f2c5` @ `8806632` | `--only research_kernel` 0 `[W]`；`page_build_check` 22/0E0W；`compliance_check` 通过 | 已闭环 |
| T-05 | `task/vocab-empty-e5c9a3d6` @ `b601c80` | `--only vocab_drift` 0 `[W]`；词条 113（45+68）；`vocab_tool check` 0 警告 | 已闭环 |
| T-06 | `task/consumer-feedback-f6d0b4e7` @ `861108b` | `build_hub --check` 通过；报告/hub 页脚反馈入口；消费指标草案 `probe` 入库 | 已闭环 |
| T-07 | `task/classification-version-a7e1c5f8` @ `99ca0f4` | `test_tools` 120 OK；`validate_layout` 通过；`classification_version=2026-11-19.1` | 已闭环 |

### 5.2 不引入新问题 · 回归结果

| # | 回归项 | 结果 |
|---|---|---|
| R-REG-1 | 统一门禁 | 0 `[E]` / 6 `[W]`（较第一波 8 `[W]` 降 2：`research_kernel`、`vocab_drift` 清零） |
| R-REG-2 | 单元测试 | `Ran 763 tests … OK (skipped=1)` |
| R-REG-3 | 指标体检 | measured 38；不达标仅 I-08 |
| R-REG-5 | 链接 | `check_links` 通过 |
| R-REG-7 | 结构 / 页面 | `validate_layout` 通过；`page_build_check` 22/0E0W；`build_hub --check` 通过 |
| R-REG-9 | 文档一致性 | naming / prompt_consistency / model_contract 0 警告 |

### 5.3 越界改动核对

- T-05 两处配套修正：`engine/vocabulary/prompts/education/prompt-skeleton.md` 去掉被 VD-03 误判的占位直角引号；`engine/tests/test_goal_alignment.py::test_empty_theme_detected` 改为合成用例（六主题现已全非空）。**核对结论**：均为达成验收所必需，未削弱检测逻辑。
- T-04 修改 10 份历史报告 → `publish_fingerprint` 漂移属**预期**（内容变更），不构成「新问题」。

## 6. 第三波（T-08 / T-09 / T-10）验证

### 6.1 双向追溯

| 方案条目 | 实施工件 | 验收证据 | 判定 |
|---|---|---|---|
| T-08 | `task/document-tier-b8f2d6a9` @ `09340df` | `test_source_check` 95 OK；`--only source_check` 0 `[E]`；抽样含 `document_tier` | 已闭环 |
| T-09 | `task/uncertainty-confidence-c9a3e7b0` @ `940ab6c` | `test_decision_hub` 22 OK；规范 §2.4/§2.5；dubai 报告含 `confidence`；`--only decision_hub` 0 `[E]` | 已闭环 |
| T-10 | `task/impact-tiering-d0b4f8c1` @ `7c6788b` | 规范 §七；5 条 business-config `impact_tier`；`test_info_density` 24 OK；`--only info_density` 0 `[E]` | 已闭环 |

### 6.2 不引入新问题 · 回归结果

| # | 回归项 | 结果 |
|---|---|---|
| R-REG-1 | 统一门禁 | 0 `[E]` / 8 `[W]`（新增 `[W]` 为可选字段覆盖率 / 历史项，已登记） |
| R-REG-2 | 单元测试 | `Ran 789 tests … OK (skipped=1)` |
| R-REG-3 | 指标体检 | measured 38；不达标仅 I-08；IGI-08 = 0.9946 |
| R-REG-5 | 链接 | `check_links` 通过 |
| R-REG-7 | 结构 / 页面 | `validate_layout` 通过；`page_build_check` 22/0E0W；`build_hub --check` 通过 |
| R-REG-9 | 文档一致性 | naming / prompt_consistency / model_contract 0 警告 |

### 6.3 执行方式说明

第三波首派被中断，改用**续做**：新 Agent 进入原 worktree，先审查未提交的 partial 改动（T-08 核心代码 / T-09 近完整 / T-10 仅规范），再补全、验证、提交。合并冲突仅 `information-layering-spec.md` 版本记录一处，已合并为单行。
