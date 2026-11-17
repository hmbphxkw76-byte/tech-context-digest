# 经济趋势周报 · 业务线说明

> **类型**：行业趋势周报型（trend-weekly） · **地区**：全球 · **节拍**：周（数据截止日命名）
> **通用指南**：接入与使用见 [类型通用接入指南](../../../../engine/templates/trend-weekly/README.md)；生命周期与校验见 [类型通用运维手册](../../../../engine/templates/trend-weekly/operations-guide.md)。本文件只写本业务线身份与差异。

## 一、业务身份

- **定位**：面向宏观经济研究团队（Macro Research）的全球宏观经济趋势周报。
- **首期锚**：`reports/2026-11-13_weekly.html`（结构与结论锚）。
- **台账**：`data/processed/economy/global/trends/economy_trend_ledger.md`（md-ledger）。
- **主题矩阵**：固定 3 块 —— 主要经济体宏观基本面 / 贸易、供应链与产业政策 / 新兴市场与大宗商品。
- **交付**：富样式自包含 HTML（`reports/{YYYY-MM-DD}_weekly.html`）+ md 源稿（`sources/`）。

## 二、与类型通用模板的差异（本线特有）

| 维度 | 本线规则 |
|---|---|
| 受众 | 宏观经济研究团队 · 跨市场趋势监测（Macro Research） |
| 来源优先级 | 官方一手（IMF / 世界银行 / OECD / 各国统计局与央行）＞ 行业机构 ＞ 挂牌数据库（FRED / e-Stat）＞ 媒体转述 |
| 触发器 | 主要央行议息 → s2；重磅宏观数据（GDP/CPI/就业）→ s2；关税与产业政策 → s3；OPEC+ 与大宗商品异动 → s4；地缘冲突 → s3/s4 |
| 结论边界 | 不给具体买卖价位、汇率点位与仓位建议 |

## 三、快速上手

1. 前置检查（`validate.py` / `classify_reports.py` / `build_hub.py --check`）通过。
2. 打开 `prompts/prompt-weekly-monitor.md` 填写运行变量并执行。
3. 落盘后收尾：`lint_reports.py` → `compliance_check.py` → `classify_reports.py` → `build_index.py` + `build_hub.py` → `archive_reports.py`。

完整执行步骤、变量表与异常排查见 [operations-guide.md](./operations-guide.md) 与 [类型通用运维手册](../../../../engine/templates/trend-weekly/operations-guide.md)。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 重构 | 通用接入指南下沉至类型通用层；本文件只保留业务身份与差异 |
