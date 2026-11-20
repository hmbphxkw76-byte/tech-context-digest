# T-02 · 代理指标抽样校准

> 方案条目：[优化解决方案与实施清单 v2.0](../optimization-solution-and-implementation-checklist-2026-11-19.md) §4.6 T-02｜优先级 P0｜性质：工具侧
> 通用协议：见 [index.md](index.md) §2–§3

## 目标
为「代理口径」指标建立**代理 → 真值**的抽样校准，量化代理的 precision / recall，防止「指标达标 ≠ 信息质量达标」（Goodhart 风险）。

## 背景（已核验）
- `metrics-dictionary.json` 中 A-03 / L-03 / IGI-05 等备注为「代理口径，非语义达标」。
- IGI-05 曾由 0.4726 → 0.9736，提升部分来自口径校准（块类型扩展、`td` 剔除）。
- 现状：无系统性抽样校准，无法知道代理达标时真实质量。

## 输入
- `engine/tools/metric_coverage.py`（A-03 / L-03 / IGI-05 计算）
- `engine/tools/info_gap_metrics.py`（IGI-05）
- `engine/tools/metrics-dictionary.json`
- 报告抽样：`content/**/reports/*.html`

## 动作
1. 在 `engine/tools/` 下新增 `proxy_calibration.py`：
   - 输入：指标 ID + 报告抽样数（默认 200 断言）；
   - 输出：代理判定 vs 人工判定混淆矩阵（TP/FP/FN/TN）、precision / recall / F1、口径版本号；
   - 支持 `--emit` 落校准记录到 `engine/audit/records/` 下的 `proxy-calibration/` 目录。
2. 定义抽样方法：分层抽样（按主题 / 业务线 / 断言类型），保证覆盖。
3. `metrics-dictionary.json` 为代理指标增加 `calibration` 备注字段（不改阈值）。
4. 单测：在 `engine/tests/` 下新增 `test_proxy_calibration.py`。

## 输出
新工具 + 单测 + 校准记录样例 + 字典备注。

## 验收标准
- 单测全绿；工具可对至少 1 个代理指标产出 precision / recall。
- 字典中代理指标均带 `calibration` 备注。
- 校准记录含口径版本 + 样本数 + 日期。

## 禁止
- 不得为提升代理值而放宽分母 / 块类型（口径变更须留版本与理由）。
- 不改既有阈值；不编造校准数值（无人工核验则标 `假设`）。

## 完成前证据索引（必填）
1. 变更文件 + diff 摘要；
2. 单测输出 + 一次试跑输出；
3. 对齐声明：T-02 验收逐条；
4. 回归声明：R-REG-1 / R-REG-2 / R-REG-3。
