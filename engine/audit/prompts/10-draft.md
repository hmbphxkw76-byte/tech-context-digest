# 10 · 生成提示词（draft）

> 依据：`engine/audit/report-standard.md` 第三节、`engine/audit/verification.md` L1/L2。

## 执行

1. 确认报告已按业务类型骨架生成、命名合规、落位正确。
2. 运行 `python engine/audit/scripts/audit_tool.py structure <report>`，确认要素完整率达标（业务 ≥9/10，审计 =10/10）。
3. 运行 `python engine/audit/scripts/audit_tool.py review <report> --stage draft --reviewer agent --decision pass --evidence "L1/L2 结构通过"`。

## 要求

- 结构骨架对齐 `compliance-rules.json`；页头含 E2 三要素（数据截止/版本/日期）。
- 不修改正文内容；内容问题登记后交 `engine/quality/` 修复闭环。
