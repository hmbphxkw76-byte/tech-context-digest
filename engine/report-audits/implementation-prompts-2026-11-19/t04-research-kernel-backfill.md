# T-04 · 研究内核历史警告收口

> 方案条目：[优化解决方案与实施清单 v2.0](../optimization-solution-and-implementation-checklist-2026-11-19.md) §4.6 T-04｜优先级 P1｜性质：内容侧
> 通用协议：见 [index.md](index.md) §2–§3

## 目标
消除 `research_kernel` 的 10 项历史 `[W]`：为历史周报补齐「周期定位 / 传导量化 / 政策入模 / 盲区列示」四项内核。

## 背景（已核验）
- `optimization_gate` 实测：`research_kernel` 10 项历史警告，集中在 `content/tech/weekly-roundup/reports/2026-11-13_weekly.html` 与 `2026-11-20_weekly.html`。
- 四项内核定义见 `engine/tools/research_kernel_check.py` 与 `engine/docs/report-pipeline-system.md`。

## 输入
- 上述 2 份周报（+ 其余触发警告的历史报告，以 `--only research_kernel` 输出为准）
- `engine/tools/research_kernel_check.py`（判定规则）
- 各线 `prompts/business-config.md`

## 动作
1. 先跑 `python engine/tools/optimization_gate.py --only research_kernel` 取全量警告清单。
2. 逐份按规则补齐四项内核；**内容须有来源**，不得编造；无法核验处标 `未核验` 或列入盲区。
3. 保持 canonical 结构与信息分层规范（摘要 / 证据 / 原始）。
4. 若某报告确实无法补齐（如数据缺失），显式登记原因，不伪造。

## 输出
更新后的历史周报 + 变更说明。

## 验收标准
- `python engine/tools/optimization_gate.py --only research_kernel` → 0 `[W]`（或剩余项均有书面免责）。
- 补齐内容含来源指针；无编造数值。
- 报告仍过 `page_build_check` / `compliance_check`。

## 禁止
- 不删除既有内容来「消警告」；不改门禁规则；不编造。

## 完成前证据索引（必填）
1. 变更文件 + diff 摘要；
2. `--only research_kernel` 前后输出；
3. 对齐声明：T-04 验收逐条；
4. 回归声明：R-REG-1 / R-REG-7。
