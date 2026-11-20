# T-10 · 信息影响分级与披露

> 方案条目：[优化解决方案与实施清单 v2.0](../optimization-solution-and-implementation-checklist-2026-11-19.md) §4.6 T-10｜优先级 P2｜性质：文档 + 内容
> 通用协议：见 [index.md](index.md) §2–§3

## 目标
为**高影响主题**（就业 / 签证 / 投资等）建立信息影响分级与强制披露强度，降低「高影响低可逆」信息的误用风险。

## 背景（已核验）
- 现有「公开信息边界」标签与「结论边界」（不给买卖价位 / 杠杆 / 仓位）。
- 无显式信息分级（公开 / 内部 / 敏感）与滥用风险评估。

## 输入
- `engine/templates/information-layering-spec.md`
- `engine/templates/decision-delivery-spec.md`
- `engine/templates/monitoring-common-spec.md`
- 高影响主题 business-config（employment / 签证 / 投资类）

## 动作
1. 定义信息影响分级（如 `high` / `medium` / `low`）与披露强度矩阵。
2. 在规范中增加条款：高影响主题强制置信区间、时效声明、免责与「非专业建议」披露。
3. 在报告模板 / business-config 中落地字段（如 `impact_tier`）。
4. 单测或校验：`info_density` 增 `impact` 检查（`[W]`）。

## 输出
规范条款 + 模板字段 + 校验（可选）。

## 验收标准
- 规范含分级与披露矩阵；高影响主题模板含 `impact_tier`。
- `--only info_density` 0 `[E]`。
- 不新增主题、不改既有阈值。

## 禁止
- 不写具体投资 / 法律建议；不编造分级；不改报告正文结论。

## 完成前证据索引（必填）
1. 变更文件 + diff 摘要；
2. 校验输出；
3. 对齐声明：T-10 验收逐条；
4. 回归声明：R-REG-1 / R-REG-2 / R-REG-9。
