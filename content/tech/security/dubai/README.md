# 迪拜 AI 网络安全调研 · 业务线说明

> **类型**：职业就业调研型（employment-research） · **地区**：UAE · 迪拜 · **节拍**：季度主更 + 月度核验 + 年度复盘
> **通用指南**：接入与使用见 [类型通用接入指南](../../../../engine/templates/employment-research/README.md)；生命周期与校验见 [类型通用运维手册](../../../../engine/templates/employment-research/operations-guide.md)。本文件只写本业务线身份与差异。

## 一、业务身份

- **定位**：面向 AI 方向的 AI 网络安全/信息安全从业者，提供迪拜（UAE）就业与落地的英文源决策监测。
- **基线锚**：`reports/2026-11_baseline_report.html`（v1.0，2026-11-11 完稿；md 源稿存 `sources/`）；正常运行永不重跑。
- **登记册**：`data/processed/tech/security/dubai/ai_cybersecurity_indicator_registry.md`（md-table，14 项指标，每格附 `[来源, 年份]`）。
- **报告命名**：`reports/{YYYY-MM}_monthly.html` / `{YYYY-Qn}_quarterly.html` / `{YEAR}_annual.html`（纯 HTML 交付，canonical 富样式；md 源稿存 `sources/`）。
- **工具链**：`engine/tools/`（报告为纯 HTML 交付，canonical 富样式；本线登记册为 md-table，无 `script/` 目录）。

## 二、与类型通用模板的差异（本线特有）

| 维度 | 本线规则 |
|---|---|
| 来源语言 | **全篇仅英文来源**；仅中文源数据标「未找到英文权威来源，已剔除」并列入待复核清单 |
| 来源优先级 | ① 政府官方 ＞ ② 国际权威组织 ＞ ③ 薪酬指南 ＞ ④ 招聘平台抽样 ＞ ⑤ 英文媒体 |
| 月度定位 | 核验型轻运行：全部未变动时**不启动新报告**，仅在登记册标注「截至 {{CURRENT_DATE}} 无更新」 |
| 触发器（7 条） | GITEX / GISEC 新届次、ISC2 人力研究新版、Gartner MENA 支出更新、新法规生效、薪酬指南新年版、签证 / 阿化规则变更、新 AI 安全证书 / SANS 日程 |
| 季度特有 | 4–6 个并行研究子代理（市场政策+企业生态 / 人才供需+薪酬交叉验证 / 岗位技能 / 证书路线+本地考点 / 落地签证）；薪酬至少 3 家指南交叉验证，冲突双引用不静默择一 |
| 年度特有 | 预测对照（偏离 >30% 必须重设三项假设）；清单年度复审；登记册「复制 → 修订 → 另存」换代（报告用复盘年、登记册用生效年） |
| 口径警示 | MENA 信息安全终端支出（Gartner）≠ 阿联酋市场含服务总收入（Mordor / GMI），并列呈现不相加 |

## 三、快速上手

1. 前置检查（`validate.py` / `classify_reports.py` / `build_hub.py --check`）通过。
2. 按节拍打开对应提示词（`prompts/prompt-{baseline-setup|monthly-monitor|quarterly-analysis|annual-review}.md`）填写运行变量并执行。
3. 落盘后收尾：`lint_reports.py` → `classify_reports.py` → `build_index.py` + `build_hub.py` → `archive_reports.py`。

完整执行步骤、变量表与异常排查见 [operations-guide.md](./operations-guide.md) 与 [类型通用运维手册](../../../../engine/templates/employment-research/operations-guide.md)。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 新增 | 业务线说明（通用接入指南下沉至类型通用层，本文件只保留业务身份与差异） |
