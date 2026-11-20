# T-03 · finding→规则回写台账

> 方案条目：[优化解决方案与实施清单 v2.0](../optimization-solution-and-implementation-checklist-2026-11-19.md) §4.6 T-03｜优先级 P1｜性质：工具/流程
> 通用协议：见 [index.md](index.md) §2–§3

## 目标
把「纠错闭环」升级为「学习闭环」：每个 L3 / 质量 finding 必须映射到**预防规则**，并跟踪规则命中，防止同类错误复发。

## 背景（已核验）
- 现有：审计四环节 + `engine/quality/repair-sop.md` + `engine/report-audits/l3-deep-review-2026-11-16.md`（14 项内容问题）。
- 缺口：finding 被修复，但「规范 / 提示词 / 校验规则」是否因新错误而演进，不可见；同类错误可能反复出现。

## 输入
- `engine/audit/`（结构见 `engine/audit/README.md`）
- `engine/quality/repair-sop.md` / `review-workflow.md`
- `engine/report-audits/l3-deep-review-2026-11-16.md`（finding 样例）

## 动作
1. 在 `engine/audit/records/` 下定义 schema `finding-rules.json`（或目录），字段：`finding_id` / `来源` / `根因` / `预防规则`（新增校验项 / 提示词条款 / 模板修订）/ `规则位置` / `命中次数` / `状态`。
2. 在 `engine/tools/` 下新增工具 `finding_rule.py`：`register` / `match`（新 finding 与已有规则相似即提示）/ `stats`。
3. 回填历史：把 `l3-deep-review` 的 14 项 finding 映射到既有规则（无规则则新建）。
4. 单测：在 `engine/tests/` 下新增 `test_finding_rule.py`。

## 输出
schema + 工具 + 回填记录 + 单测。

## 验收标准
- 单测全绿；历史 14 项 finding 映射率 100%。
- `finding_rule.py match` 能对测试 finding 命中至少 1 条规则。
- schema 字段完整、可重放（无时间戳）。

## 禁止
- 不改报告正文；不把未验证的映射标 `已核验`；不重复 `repair-sop` 内容（只指针）。

## 完成前证据索引（必填）
1. 变更文件 + diff 摘要；
2. 单测输出 + `stats` 输出；
3. 对齐声明：T-03 验收逐条；
4. 回归声明：R-REG-1 / R-REG-2 / R-REG-9。
