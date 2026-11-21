# 高技能移民政策 · 首期基线采集（prompt-baseline-setup）

> **触发**：`schedule.json` 任务 `baseline-setup` 一次运行（当前手动，未注册 Schedule）。
> **执行人**：主代理 + 3–5 个并行子代理。
> **业务配置**：[business-config.md](./business-config.md) 为单一事实源。
> **框架说明（贯穿全程）**：[政策法规解读型基线模板](../../../../engine/templates/policy-analysis/prompt-baseline-setup-template.md)。
> **交付格式**：纯 HTML 交付（canonical 富样式自包含 HTML）；md 源稿仅存档于 `sources/`。

> **九节固化锚**：本报告结构 = [基线模板](<../../../../engine/templates/policy-analysis/prompt-baseline-setup-template.md>) 九节骨架逐字继承（节标题为本业务线固化锚，不得增删节、调整顺序）。字数 8000–15000。

> **🔒 第三节节标题固化锚（业务实例）**
> **一、执行摘要**｜**二、政策台账与监测机制**｜**三、高技能移民框架总览**｜**四、重点国家政策逐条解读**｜**五、影响对象矩阵**｜**六、合规应对建议（建议章）**｜**七、生效时间线**｜**八、数据治理与局限**｜**九、参考来源清单**

## 运行变量（从 business-config 读取）

```
{{REGION}}               = 无（九国横向：新西兰 / 荷兰 / 澳大利亚 / 爱尔兰 / 加拿大 / 美国 / 新加坡 / 德国 / 法国）
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

运行后写报告头：版本号 `v1.0`、本期读数时点（数据截止月份）、内部台账 / 来源指针。

---

## 第一步：建立台账结构（主代理）

在 `data/processed/international/immigration/immigration_ledger.md` 写入字段定义与待采集清单；在 `source_registry.json` 写入来源分级、分级规则、核验状态枚举与「政策原文回溯规则」（六项强制字段：发布机构、文号 / 页面标题、发布日期、生效日期、官方 URL、文本完整性核验）。

台账最小字段集：

- 通道编号（C01–Cxx，按国别分组）；国家；通道英文名 + 中文译名；通道类别（雇主担保 / 积分制 / 人才类 / 留学生过渡）
- 适用人群；核心资格条件（学历 / 技能 / 语言 / 工作经验）
- 薪资门槛（数值 + 币种 + 年 / 月 / 小时口径 + 适用年份）
- 雇主担保 / 认证要求；有效期；转永居 / 长期居留路径与居住年限
- 官方 URL；核验状态（verified / snippet / unverified）；是否更新；更新时间

同步定义信号阈值与红线：

- **信号阈值（K01–K08，ex-ante）**：① 通道新增 / 关闭 / 改名；② 薪资门槛调整；③ 配额 / 抽签规则变化；④ 职业清单调整；⑤ 积分计分规则变化；⑥ 永居 / 居住年限变化；⑦ STEM / AI / IT 定向政策；⑧ 官方统计年度更新。
- **结构红线（RL-01–RL-05，ex-ante）**：① 主要通道关闭或暂停；② 永居路径中断；③ 配额耗尽致通道实际关闭；④ 薪资门槛大幅上调（>30%）；⑤ 排期 / 积压超阈值。

---

## 第二步：并行采集（3–5 个子代理，仅英文来源）

建议分组（每组 2–3 国）：① 新西兰 + 荷兰 + 澳大利亚；② 爱尔兰 + 加拿大 + 美国；③ 新加坡 + 德国 + 法国。

**采集内容**：按 [来源采集规范](../../../../engine/templates/monitoring-common-spec.md) 第 2 / 3 / 5 节执行：
- 第 2 节：逐条证据块附「官方原文 / 数值表」URL；**政策条款须回溯官方原文**（公报 / 法规数据库 / 移民局官方页），先登记发布与生效日期、官方 URL 后才进入解读。
- 第 3 节：每条证据 = 官方来源 URL + 版本 / 发布日期 + 完整引用段 + 原文核验状态 + 口径说明；数值口径（年 / 月 / 小时、毛 / 净）逐条标注。
- 第 5 节：仅采信官方 / 原始来源；英文媒体转述仅作线索，标「需核实原文」。

**语言限制**：严禁中文来源（只作发现线索，不作证据引用）。政策原文为非英语时（德 / 法），优先英文官方页；无英文页则标注原文语言并附官方 URL，列入待复核。

**产出**：主代理写入 `{{REGISTRY_PATH}}`（台账）与 `{{SOURCE_REGISTRY_PATH}}`（来源登记）。

---

## 第三步：官方原文回溯（主代理，采集后立即执行）

逐条核对子代理登记的官方 URL 是否可访问、是否为条款 / 细则页；优先官方公报 / 法规数据库 / 移民局官方页。未获原文的条目标注「未核验」并保留线索来源（媒体 / 搜索摘要），**列入待复核清单**，不得作为事实直引。

---

## 第四步：主代理解读与报告生成

按基线模板生成 `sources/2026-11_baseline_report.md`（含 canonical HTML 结构，用于生成 `reports/2026-11_baseline_report.html`）。要求：

- **九节结构逐字继承**：按 [基线模板](<../../../../engine/templates/policy-analysis/prompt-baseline-setup-template.md>) 与上方「九节固化锚」，九节全模块（不得只写摘要 + 来源）；第一节决策摘要 ≤1 屏。
- **第一节**：`结论先行`（核心判断 3–6 条）+ 一句话定位 + 场景切片（主：赴外就业 / 定居决策；次：政策研究 / 比较）。
- **第三节**：九国框架总览（层级地图 + 国别对比矩阵 + 术语口径区分）。
- **第四节**：逐国逐通道解读（条款摘编 / 解读 / 官方答问），每国附 2024–2026 变化与来源。
- **第五节**：影响对象矩阵（通道 / 条款 × 主体 × 方向 / 量级 / 依据）。
- **第六节**：建议章与事实分离（合规要点 + 待明确事项清单，标「建议」）；行动协议卡三档。
- **第七节**：生效时间线（公布 / 生效 / 细则三阶段分列）+ 待生效清单。
- **第八节**：来源分级表 + 文本时效与版本治理 + 未核验清单（U-xx 表）。
- **第九节**：完整 URL 清单，优先官方 / 原始来源，格式 `[Source: URL, 年份]`。
- **决策摘要**：标注核心判断的信息等级（`已核验` / `部分核验` / `推断` / `假设`）+ 证据指针；仅允许「已核验 + 部分核验」进摘要。
- **开头**：新增信息统计（本期新增 X / 修正 Y / 无变化 Z / 假设核验进度 k/n）；基线首期「本期新增 = 全部基线项」。
- **指针引用**：台账 / 来源登记指针（`{{REGISTRY_PATH}}` / `{{SOURCE_REGISTRY_PATH}}`）。
- **阈值校准**：阈值 / 信号 / 红线为预校准（ex-ante），首次中期回测 2027-06。
- **信息分层 boilerplate**：共享部分不复制正文，只引用通用基座第十节规范；强制项见 business-config 第九节。

---

## 第五步：校验与提交

主代理依次执行：`validate.py`、`validate_layout.py`、`check_links.py`、`lint_reports.py`、`classify_reports.py`、`build_hub.py`；全部通过后提交（`engine/tools/repo_sync.py run --gate`，不直推 `main`）。

> 纯 HTML 交付：报告 HTML 由 md 源稿经 `md2html.py` 渲染后人工核对 canonical 样式；md 源稿存 `sources/`，不参与自动转换。

---

## 完成后回填 business-config

- 更新 `{{BASELINE_DATE}}`；
- 追加「已修正事实清单」；
- 追加版本记录（日期 / 变更 / 说明）；
- 同步更新 `{{REGISTRY_PATH}}` 的台账计数（已登记通道数 / 待采集数）。

---

## 质量清单

- [ ] 九节固化锚逐字继承；无媒体直引；核心判断有证据与等级标注
- [ ] 九国通道逐条附官方 URL 与核验状态；数值口径（年 / 月 / 小时、币种、年份）完整；冲突口径并列
- [ ] 台账 / 来源登记字段完整，政策原文回溯规则执行；HTML 通过 lint
