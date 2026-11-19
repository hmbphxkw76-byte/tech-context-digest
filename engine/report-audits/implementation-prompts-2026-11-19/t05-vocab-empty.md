# T-05 · 词库空库补录

> 方案条目：[优化解决方案与实施清单 v2.0](../optimization-solution-and-implementation-checklist-2026-11-19.md) §4.6 T-05｜优先级 P2｜性质：内容侧
> 通用协议：见 [index.md](index.md) §2–§3

## 目标
消除 `vocab_drift` VD-02：补录 `education` 与 `international` 两个主题的空词库。

## 背景（已核验）
- 实测：`engine/vocabulary/data/education/terms.md` 与 `engine/vocabulary/data/international/terms.md` 无词条。
- 词库规范：`engine/vocabulary/README.md`（NFKC + 空白折叠 + 大小写归一；词条 + 别名全局唯一）。

## 输入
- `engine/vocabulary/README.md`
- 参照：`engine/vocabulary/data/tech/terms.md`（272 条）、`engine/vocabulary/data/economy/terms.md`（97 条）
- 对应主题的报告与 business-config（`content/education/**`、`content/international/**`）

## 动作
1. 从对应主题的 business-config、提示词与报告中提取术语。
2. 按规范写 `terms.md`：规范形 + 同义词 / 别名；全局唯一。
3. 运行 `python engine/vocabulary/script/vocab_tool.py`（或对应校验）确认合规。

## 输出
两份 `terms.md`。

## 验收标准
- `python engine/tools/optimization_gate.py --only vocab_drift` → 0 `[W]`。
- 词条格式合规、无重复规范形。

## 禁止
- 不编造术语；不引入未在主题内出现的词；不改既有主题词库。

## 完成前证据索引（必填）
1. 变更文件 + 词条数；
2. `--only vocab_drift` 前后输出；
3. 对齐声明：T-05 验收逐条；
4. 回归声明：R-REG-1 / R-REG-9。
