# 20 · 初审提示词（initial）

> 依据：`engine/audit/report-standard.md` 第十节、`engine/audit/verification.md` L2。

## 逐项核对（任一不满足即 `--decision fix` 并记录 finding）

| 项 | 核对 |
|---|---|
| E1–E10 | 十大要素齐备（见 `structure` 输出） |
| E2 | 页头含数据截止/版本/日期 |
| E6 | 关键数字有来源；媒体转述标「需核实原文」 |
| E7 | 多口径并列；无裸单位数字 |
| E9 | 已修正事实清单存在（或注明本期无修正） |
| 归属 | `classify_reports.py --check` 无错位 |
| 页面 | `page_build_check.py` 无 [E] |

## 执行

**通过**：`review <report> --stage initial --reviewer agent --decision pass --evidence "..."`，状态转 `in-review`。
