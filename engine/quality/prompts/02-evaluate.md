# 02 · 四维量化评估（evaluate）

> **阶段**：2–3。**上游**：`01-inventory.md`。**下游**：`03-classify.md`。
>
> **目标**：先跑机器判定，再逐项计算 21 项指标，产出带证据的 `findings`。

---

## 一、阶段 2 · 机器判定汇总

依次运行下述命令，记录退出码（0/1/2）与 `[E]`/`[W]` 计数，填入 `verification.tools[]`：

```
python engine/tools/validate.py
python engine/tools/validate_layout.py
python engine/tools/compliance_check.py --check
python engine/tools/page_build_check.py
python engine/tools/lint_reports.py
python engine/tools/check_links.py --verbose
python engine/tools/classify_reports.py --check --unknown-warn
python engine/tools/update_planner.py --porcelain --pending-only
python engine/vocabulary/script/vocab_tool.py check
python engine/vocabulary/script/vocab_tool.py topic-check
python engine/vocabulary/script/sync_vocab.py verify
```

**映射**：退出码 1 → P0；退出码 2 → P1；每条 `[E]`/`[W]` 生成一条 finding（场景见 `../chaos-taxonomy.md`）。

---

## 二、阶段 3 · 四维指标计算

逐项按下表计算。每项须记录：实测值、阈值、是否达标、证据、检测层。

### 维度一 · 主题完整性

| # | 指标 | 计算 | 阈值 |
|---|---|---|---|
| C-01 | 结构完整率 | 实际 `h2.sec` 节数 / 骨架节数 | ≥100% |
| C-02 | 必填字段完整率 | 已填 / 应填 | 100% |
| C-03 | 目录完整率 | 合规业务线 / 业务线总数 | 100% |
| C-04 | 登记册指标覆盖率 | 报告引用指标 / 登记册指标 | ≥90% |
| C-05 | 节拍达成率 | 实际报告 / 应产出报告 | 100% |
| C-06 | 词汇同步覆盖率 | 已绑定主题 / 已注册主题 | 100% |

### 维度二 · 信息准确性

| # | 指标 | 计算 | 阈值 |
|---|---|---|---|
| A-01 | 来源可追溯率 | 有来源关键数字 / 关键数字总数 | ≥95% |
| A-02 | 来源分级合规率 | 合规来源条目 / 来源条目总数 | 100% |
| A-03 | 数值一致率 | 与登记册一致数值 / 可核对数值 | ≥99% |
| A-04 | 新鲜度合规率 | 时效内数据条目 / 数据条目总数 | ≥90% |
| A-05 | 链接可达率 | 可达链接 / 链接总数 | 100% |

### 维度三 · 逻辑一致性

| # | 指标 | 计算 | 阈值 |
|---|---|---|---|
| L-01 | 跨章节数值一致率 | （1 − 冲突数 / 指标总数） | ≥99% |
| L-02 | 口径一致率 | 遵守口径表条目 / 应遵守条目 | 100% |
| L-03 | 阈值三处一致率 | 三处一致阈值 / 阈值总数 | 100% |
| L-04 | 结论-证据一致率 | 有证据结论 / 结论总数 | ≥95% |
| L-05 | 时间线一致率 | 无矛盾事件 / 事件总数 | 100% |

### 维度四 · 内容关联性

| # | 指标 | 计算 | 阈值 |
|---|---|---|---|
| R-01 | 归属正确率 | 正确归属报告 / 报告总数 | 100% |
| R-02 | 维度优先级合规率 | 无倒置业务线 / 业务线总数 | 100% |
| R-03 | 跨主题重复率 | 重复段落 / 段落总数 | ≤5% |
| R-04 | 断头锚点率 | 断头锚点 / 锚点总数 | 0% |
| R-05 | 主题-内容匹配率 | 匹配报告 / 报告总数 | ≥95% |

> 完整口径（含「关键数字」「口径映射」「并列豁免」定义）见 `../rubric.md`。

---

## 三、finding 产出格式

每条 finding 必须含以下字段（写入 `findings[]`）：

| 字段 | 要求 |
|---|---|
| `id` | `F-<日期>-<序号>` |
| `scenario` | C01–C15（见 `../chaos-taxonomy.md`） |
| `severity` | P0 / P1 / P2 |
| `dimension` | completeness / accuracy / consistency / relevance |
| `target` | 文件相对路径（或对象标识） |
| `description` | 一句话问题陈述 |
| `evidence` | 可复述证据（文件 + 位置 + 具体值） |
| `metric` | 触发的指标编号（如 L-01） |
| `threshold` | 阈值与实测值 |
| `detected_by` | TOOL / LLM / MIXED |

---

## 四、纪律

- 不输出无证据的「正常」结论；每个维度给出实测计数。
- LLM 判定必须写下依据（引用原文），不得只给结论。
- 机器判定与语义判定冲突时，以证据更强的一方为准，并在报告中说明。
- 本阶段**只读**，不修改文件。
