# 经济趋势周报 · 操作手册（业务差异）

> **定位**：本文件是 [类型通用运维手册](../../../../engine/templates/trend-weekly/operations-guide.md) 的**业务实例**，只写本线差异；通用执行步骤、变量表、校验关卡、异常排查与 Agent 约定以通用手册为准。
> **单一事实源**：业务参数以 [prompts/business-config.md](./prompts/business-config.md) 为准。

---

## 0. 本线目录速查

| 资产 | 路径 |
|---|---|
| 周报提示词（启动入口） | `prompts/prompt-weekly-monitor.md` |
| 基线机制建立提示词（占位） | `prompts/prompt-baseline-setup.md` |
| 业务参数 | `prompts/business-config.md` |
| 指标台账 | `data/processed/economy/global/trends/economy_trend_ledger.md` |
| 报告产物 / 归档 / md 源稿 | `reports/` / `reports/archives/` / `sources/` |
| 通用层（只读） | `engine/templates/trend-weekly/` |

## 1. 本线要点

- **主题矩阵**：固定 3 块（s2 主要经济体宏观基本面 / s3 贸易、供应链与产业政策 / s4 新兴市场与大宗商品），周报共 8 节（含 Top5、数据看板、风险、启示、来源）。
- **来源语言**：官方一手以英文为准；中文媒体仅作线索，数值须回官方页核验。
- **交付**：纯 HTML（business-config 第六节声明）；md 源稿存 `sources/`，不参与 md2html 自动转换。
- **触发器**：见 business-config 第五节（央行议息 / 宏观数据 → s2；关税与产业政策 → s3；OPEC+ 与大宗商品 → s4；地缘冲突 → s3/s4）。

## 2. 本线特有排查项

| 现象 | 处置 |
|---|---|
| 官方统计修订历史值 | 以最新发布为准，并在台账「已修正事实清单」留痕，不覆盖历史 |
| 多国数据发布窗口错位（T+1 / 空窗） | 报告头部标注「T+1 刷新」；无变化时降级核验轻运行 |
| 汇率/大宗口径冲突 | 并列呈现，不静默择一；交叉核对官方口径 |

其余通用异常（validate/lint/compliance/classify/build_hub 退出码、上期报告缺失、词汇速览误编辑等）见 [类型通用运维手册第 7 节](../../../../engine/templates/trend-weekly/operations-guide.md)。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 重构 | 通用流程下沉至类型通用层；本文件瘦身为业务差异 |
