# 40 · 终审提示词（final）

> 依据：`engine/audit/acceptance.md` 第一节。

## 终审核对

| # | 标准 | 阈值 |
|---|---|---|
| A1 | L1 机器校验 | 0 错误（LEGACY 除外） |
| A2 | L2 要素完整率 | 审计 10/10；业务 ≥9/10 |
| A3 | 来源可追溯率 | ≥95% |
| A4 | 数据一致率 | ≥99% |
| A5 | 结论-证据一致率 | ≥95% |
| A6 | 表述硬性项 | 无绝对化、无裸单位 |
| A7 | 签发链 | 四环节记录齐备 |
| A8 | 标识一致 | 与 registry 一致 |

## 执行

1. 核对上述标准，全部满足 → `review <report> --stage final --reviewer agent --decision pass --evidence "终审通过"`。
2. 任一不满足 → `--decision fix` 或 `--decision reject`，说明原因。
3. 终审通过后：`python engine/audit/scripts/audit_tool.py mark <report>` 注入「已审计」标识。

## 签发

终审记录即签发记录，含：签发人（reviewer）、日期（timestamp）、登记编号（audit_id）。
