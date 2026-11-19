# T-07 · 分类版本号 + 互斥性校验

> 方案条目：[优化解决方案与实施清单 v2.0](../optimization-solution-and-implementation-checklist-2026-11-19.md) §4.6 T-07｜优先级 P2｜性质：工具侧
> 通用协议：见 [index.md](index.md) §2–§3

## 目标
给分类体系加**版本号**与**变更影响评估**，并增加**跨主题互斥性**检查，防止分类漂移导致跨期信息不可比。

## 背景（已核验）
- `engine/tools/layout.json` 历史上多次重构（regional/global 反复、维度倒置回滚）。
- 六主题间存在天然重叠（如 economy 主题的 trends 业务线、tech 主题的 trends 业务线、economy 主题的 insight 业务线）。
- 现无分类版本号，变更影响不可追溯。

## 输入
- `engine/tools/layout.json`
- `engine/tools/validate_layout.py`
- `engine/tools/_common.py`
- `engine/tests/test_tools.py::TestDimensionOrder`

## 动作
1. 在 `layout.json` 增加 `classification_version`（如 `2026-11-19.1`）与 `changelog`。
2. `validate_layout.py` 增加版本号存在性 + 格式校验。
3. 增加互斥性检查：任一同质内容块归属唯一主题；命中多个主题即告警（先 `[W]`）。
4. 变更影响评估：分类变更时输出受影响报告清单（可只提供工具 `--impact`）。
5. 单测：`engine/tests/test_tools.py` 增用例。

## 输出
schema 扩展 + 校验扩展 + 单测 + 影响评估工具。

## 验收标准
- 单测全绿；`python engine/tools/validate_layout.py` 通过。
- `layout.json` 含 `classification_version`。
- 互斥性检查可跑（先 `[W]`，不阻断）。

## 禁止
- 不新增 / 删除主题；不改维度顺序（除 `layout.json` 显式声明）；不放宽既有校验。

## 完成前证据索引（必填）
1. 变更文件 + diff 摘要；
2. 单测 + `validate_layout` 输出；
3. 对齐声明：T-07 验收逐条；
4. 回归声明：R-REG-1 / R-REG-2 / R-REG-7。
