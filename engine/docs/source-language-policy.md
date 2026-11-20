# 来源语言与来源类型政策（SOURCE-LANGUAGE-POLICY v1.0）

> **定位**：本文件是 tech-context-digest 仓库**来源语言与来源类型**的单一事实源。所有主题、所有业务线的报告生成、来源登记、质量审计与 CI 门禁一律以本文件为准；通用基座、业务配置、类型模板与提示词只得**指针引用**，不得复制或改写口径。
>
> **权威源优先级**：本文件 ＞ 业务配置（`business-config.md`）＞ 通用基座 / 类型模板。业务配置只能**加严**（缩小允许集），不得放宽。

---

## 一、语言规则（默认仅英文）

- **默认规则：仅英文（`official_en`）**。所有业务线的外部来源以英文为准；非英语官方文件须标注原文语言并附官方 URL。
- **唯一例外：中国宏观经济数据**。仅 `content/economy/trends`（全球宏观经济趋势，覆盖中国 GDP / CPI / PPI / 关税等宏观数据）允许使用中文官方来源作**参考**，且**英文资料优先**；中文来源须显式标注「需核实原文」。
- 例外业务线必须在 `business-config.md` 显式声明：
  ```
  {{SOURCE_LANGUAGE_RULE}} = 英文优先；中国宏观数据可用中文官方来源作参考（须标需核实原文）
  {{CHINA_MACRO}}          = true
  ```
- 其他业务线（含 economy 非宏观线、tech / education / international / political / society）**一律严禁中文来源**，不得因「官方 / 权威」身份豁免。

## 二、来源类型白名单（允许的来源形态）

| 允许 | 说明 |
|---|---|
| 英文来源 | 任意英文网页 / PDF / 官方发布 |
| 官方权威一手资料 | 政府 / 央行 / 统计 / 主管部门 / 国际组织；非英语官方文件须标注原文语言 + 官方 URL |
| 主流投资 / 顾问机构 | 如 IMF、World Bank、Bloomberg、Reuters、Gartner、JLL、CBRE、Knight Frank 等 |
| 主流新闻媒体 | 通讯社 / 主流媒体（仅作线索，数值标「需核实原文」） |

**禁止**：中文来源（唯一例外见第一节）；未登记来源；社交媒体 / 个人博客 / 聚合搬运站（除非该机构已登记于 `institution_tiers.json` 且符合语言规则）。

## 三、中文来源白名单（仅中国宏观例外线）

`engine/tools/institution_tiers.json` 的 `lang.zh_macro_whitelist` 为**机器可读白名单**，与本节一致：

| 机构 | 主机 |
|---|---|
| 中国人民银行 | pbc.gov.cn |
| 中国商务部 | mofcom.gov.cn |
| 中国国家统计局（官方微信号） | stats.gov.cn |
| 中国政府网 | gov.cn |

- 例外线内，仅上表机构（或 `lang.zh_macro_hosts` 主机）的中文来源可采；其余中文来源一律 `[E]`。
- 非例外线：任何中文来源一律 `[E]`。
- URL 级判定：命中 `lang.zh_hosts` 的中文主机，若路径含明确英文段（`/eng/`、`/en/`、`/english/`）则按英文来源处理；否则按中文来源处理。

## 四、机器门禁（source_check R9）

- **R9 中文来源校验**（`engine/tools/source_check.py`）：对来源登记逐条判定有效语言（`s.lang` → 机构主数据 `lang` → URL 主机），命中中文即按第一、三节裁决；违规 `[E]`（历史报告按 gate-period 降级为 `[W]`）。
- R9 随 `source_check` 进入统一门禁 `engine/tools/optimization_gate.py`，并被 `ci.yml` / `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml` / `audit.yml` 复用；**不另写一套**。
- R5 语言规则（业务配置 `{{SOURCE_LANGUAGE_RULE}}`）继续生效：非例外线 `official_en` 对 `lang=zh` 直接 `[E]`；例外线 `zh_macro_reference` 放行 `{en, zh}` 后由 R9 做白名单裁决。
- R5 对**非中文**语言不合规（如 ja / ko 官方统计）仅 `[W]`，不阻断——官方权威资料允许非英语，须标注原文语言并附官方 URL；中文违规由 R5 / R9 双重拦截。

## 五、存量与增量

- **存量**：非白名单中文来源引用一律删除（报告正文来源清单 / inline 引用 / 来源登记 / 台账）。
- **增量**：新来源先登记（R1）→ 语言合规（R5 / R9）→ 分级合规（R2 / R7）→ 关键数字（R4）；任一 `[E]` 即阻断，不得采纳。

## 六、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-20 | 初始版本 | 建立来源语言与来源类型政策：默认仅英文、中国宏观例外、来源类型白名单、中文机构白名单、R9 门禁 |
