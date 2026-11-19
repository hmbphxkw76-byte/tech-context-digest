# T-09 · 不确定性置信度字段

> 方案条目：[优化解决方案与实施清单 v2.0](../optimization-solution-and-implementation-checklist-2026-11-19.md) §4.6 T-09｜优先级 P1｜性质：工具 + 内容
> 通用协议：见 [index.md](index.md) §2–§3

## 目标
把四级信息标签（已核验 / 部分核验 / 推断 / 假设）升级为**可操作判定规则 + 置信度**，并让不确定性传播到决策卡。

## 背景（已核验）
- `information-layering-spec.md` §二定义四级标签，但无判定细则与数值置信度。
- `decision-delivery-spec.md` 决策卡有「证据强度」字段，但未与置信度绑定。

## 输入
- `engine/templates/information-layering-spec.md`
- `engine/templates/decision-delivery-spec.md`
- `engine/tools/decision_hub_check.py`
- `engine/tools/metrics-dictionary.json`
- 抽样报告决策卡

## 动作
1. 为四级标签写**操作性判定规则**（含边界案例），写入规范（单一事实源）。
2. 定义置信度字段（如 `confidence` ∈ `[0,1]` 或 Kent 词表），决策卡增加该字段。
3. `decision_hub_check.py` 增加校验（`[W]`，不阻断；新报告可 `[E]`）。
4. 字典增加对应指标备注（不改阈值）。
5. 单测：`engine/tests/test_decision_hub.py` 增用例。

## 输出
规范条款 + 工具校验 + 单测 + 字典备注。

## 验收标准
- 单测全绿；规范含四级判定规则。
- 抽样 1 份报告决策卡含 `confidence`。
- `--only decision_hub` 0 `[E]`。

## 禁止
- 不改动四级标签名称（保持兼容）；不编造置信度；不改既有阈值。

## 完成前证据索引（必填）
1. 变更文件 + diff 摘要；
2. 单测 + `--only decision_hub` 输出；
3. 对齐声明：T-09 验收逐条；
4. 回归声明：R-REG-1 / R-REG-2 / R-REG-9。
