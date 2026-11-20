# T-08 · 文档级 / 陈述级信源分级

> 方案条目：[优化解决方案与实施清单 v2.0](../optimization-solution-and-implementation-checklist-2026-11-19.md) §4.6 T-08｜优先级 P1｜性质：工具侧
> **依赖**：T-01 合并后再开工（同 `source_check.py`，§4.7 G1 串行）。
> 通用协议：见 [index.md](index.md) §2–§3

## 目标
在机构级 tier 之外，增加**文档级 / 陈述级**分级，消除「机构光环效应」（tier 1 机构的一切产出被默认当一手事实）。

## 背景（已核验）
- `institution_tiers.json` 按机构分级；`source_registry.json` 条目按机构 tier。
- 同一机构的不同产出可信度不同（官方新闻稿 vs 统计年报；Gartner 新闻稿 vs 付费报告）。

## 输入
- `engine/tools/source_check.py`
- `engine/tools/institution_tiers.json`
- 各线 `source_registry.json`
- `engine/templates/monitoring-common-spec.md` §4

## 动作
1. 定义字段：`document_tier`（`primary_data` / `official_release` / `industry_report` / `media` / `opinion`）与 `statement_type`（`fact` / `restatement` / `forecast` / `opinion`）。
2. `check_registry_fields`（或新规则）增加字段存在性与取值校验（`[W]`，不阻断）。
3. 一致性规则：`document_tier` 不得高于机构 tier 允许的上限（如 tier 4 机构不得标 `primary_data`）。
4. 单测：`engine/tests/test_source_check.py` 增用例。

## 输出
schema + 校验 + 单测。

## 验收标准
- 单测全绿；`--only source_check` 0 `[E]`。
- 抽样 3 条来源含 `document_tier`。
- 未改机构 tier 主数据与既有规则。

## 禁止
- 不放宽 R1–R7；不改报告正文；不编造分级。

## 完成前证据索引（必填）
1. 变更文件 + diff 摘要；
2. 单测 + `--only source_check` 输出；
3. 对齐声明：T-08 验收逐条；
4. 回归声明：R-REG-1 / R-REG-2 / R-REG-3。
