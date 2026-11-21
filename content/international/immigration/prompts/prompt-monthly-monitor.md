# 高技能移民政策 · 月度更新（prompt-monthly-monitor）

> **触发**：`schedule.json` 任务 `monthly-monitor`（当前手动，未注册 Schedule）。
> **执行人**：主代理 + 并行子代理。
> **业务配置**：[business-config.md](./business-config.md) 为单一事实源。
> **框架说明（贯穿全程）**：[政策法规解读型月度模板](../../../../engine/templates/policy-analysis/prompt-monthly-monitor-template.md)。
> **交付格式**：纯 HTML 交付（canonical 富样式自包含 HTML）；md 源稿仅存档于 `sources/`。

> **九节固化锚**：本报告结构 = [月度模板](../../../../engine/templates/policy-analysis/prompt-monthly-monitor-template.md) 九节骨架逐字继承（节标题为本业务线固化锚，不得增删节、调整顺序）。字数 6000–12000。

> **🔒 第三节节标题固化锚（业务实例）**
> **一、执行摘要**｜**二、政策台账与监测机制**｜**三、高技能移民框架总览**｜**四、重点国家政策逐条解读**｜**五、影响对象矩阵**｜**六、合规应对建议（建议章）**｜**七、生效时间线**｜**八、数据治理与局限**｜**九、参考来源清单**

## 运行变量（从 business-config 读取）

```
{{REGION}}               = 无（九国横向）
{{TOPIC}}                = 高技能移民政策
{{REPORT_TYPE}}          = policy-analysis
{{BASELINE_DATE}}        = 2026-11-21
{{REGISTRY_PATH}}        = data/processed/international/immigration/immigration_ledger.md
{{REGISTRY_FORMAT}}      = md-table
{{SOURCE_REGISTRY_PATH}} = data/processed/international/immigration/source_registry.json
{{BASELINE_REPORT_PATH}} = sources/2026-11_baseline_report.md
{{FRESHNESS_PRIORITY}}   = 近 12 个月内数据优先；超过 24 个月须标注年份并谨慎使用
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/international/immigration
```

运行后写报告头：版本号、本期读数时点（数据截止月份）、内部台账 / 来源指针。**版本号写入报告内，不进文件名。**

---

## 第零步：继承与读取锚

- 读取基线报告 `{{BASELINE_REPORT_PATH}}` 与上一期月度报告（如有），继承九国框架地图、解读规则与全部已核实结论。
- 读取台账 `{{REGISTRY_PATH}}` 与来源登记 `{{SOURCE_REGISTRY_PATH}}`；逐项填写「是否更新」。
- 继承 business-config 第七节「已修正事实清单」，产生修正后追加；无来源不得入清单。
- 读取 10 项指标「上次值」（见 business-config 第六节）。

---

## 第一步：变更检测（主代理 + 子代理）

按 business-config 第五节触发器，逐国检测本期（自然月）是否有：

- 通道新增 / 关闭 / 改名；薪资门槛或配额调整；职业清单调整；积分 / 抽签规则变化；永居 / 居住年限变化；STEM / AI / IT 定向政策；官方统计更新。

无变更的国家 / 通道在台账标注「截至 {{CURRENT_DATE}} 无更新」，不重新展开解读。

---

## 第二步：增量采集与原文回溯

仅对有变更的国家 / 通道启动采集（2–4 个子代理，仅英文来源）；按 [来源采集规范](../../../../engine/templates/monitoring-common-spec.md) 第 2 / 3 / 5 节执行，政策条款回溯官方原文（公报 / 法规数据库 / 移民局官方页），先登记发布与生效日期、官方 URL 后才进入解读。

---

## 第三步：主代理更新报告

按月度模板生成 `sources/{{YYYY-MM}}_monthly.md`（含 canonical HTML 结构，用于生成 `reports/{{YYYY-MM}}_monthly.html`）。要求：

- **九节结构逐字继承**，九节全模块刷新（不得只写摘要 + 来源）。
- **第一节**：本期结论先行 + 数据变更摘要（本期新增 X / 修正 Y / 无变化 Z / 假设核验进度 k/n）。
- **第三节**：更新九国框架对比矩阵（仅变更格高亮）。
- **第四节**：仅对有变更的国家 / 通道逐条解读；无变更国别注明「本期无更新」。
- **第五节**：影响对象矩阵增量（政策 × 主体 × 方向 / 量级 / 依据条款）。
- **第六节**：建议章与事实分离；行动协议卡三档。
- **第七节**：生效时间线增量（公布 / 生效 / 细则三阶段分列）。
- **第八节**：来源分级 + 未核验清单增量；台账更新编号与来源。
- **第九节**：完整 URL 清单（含本期新增来源），格式 `[Source: URL, 年份]`。
- **阈值校准**：信号 / 红线为预校准（ex-ante），首次中期回测 2027-06；触发阈值时标注并复核。

---

## 第四步：校验与提交

主代理依次执行：`validate.py`、`validate_layout.py`、`check_links.py`、`lint_reports.py`、`classify_reports.py`、`build_hub.py`；全部通过后提交（`engine/tools/repo_sync.py run --gate`，不直推 `main`）。

---

## 完成后回填 business-config

- 追加「已修正事实清单」；
- 追加版本记录（日期 / 变更 / 说明）；
- 同步更新台账「是否更新 / 更新时间」与指标计数。

---

## 质量清单

- [ ] 九节固化锚逐字继承；仅变更项展开，无变更项标注
- [ ] 变更条目附官方原文 URL 与生效日期；数值口径完整
- [ ] 台账增量回写；HTML 通过 lint；阈值触发项已复核
