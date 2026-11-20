# T-01 · 来源核验证据字段 + 内容指纹

> 方案条目：[优化解决方案与实施清单 v2.0](../optimization-solution-and-implementation-checklist-2026-11-19.md) §4.6 T-01｜优先级 P1｜性质：工具侧
> 通用协议：见 [index.md](index.md) §2–§3

## 目标
让每条来源登记**可自证**（核验证据），并对关键来源做**内容指纹**，使「URL 可达但内容漂移」可探测。

## 背景（已核验）
- `source_check.py` 的 R8（`check_registry_fields`，约 488 行）仅校验 `verify_status ∈ {verified, media_unverified, unverifiable}` 与 `updated`（YYYY-MM-DD）。
- 登记条目（例：`data/processed/tech/security/dubai/source_registry.json`）无「核验方式 / 快照日 / 存档哈希」字段。
- 死链台账（`engine/report-audits/dead-link-ledger.md`）有人工留痕，但**来源登记本身不可自证**。

## 输入
- `engine/tools/source_check.py`
- 抽样登记：`data/processed/tech/security/dubai/source_registry.json`
- 规范：`engine/templates/monitoring-common-spec.md` §4；单一事实源：字段定义归 `metrics-dictionary.json` 备注，工具只做校验。

## 动作
1. 定义 `evidence` 可选字段：`method`（`web_fetch` / `manual` / `pdf`）、`snapshot_date`、`archive_hash`（可选）、`note`。
2. `check_registry_fields` 增加统计与 `[W]` 提示：含 `evidence` 的条目占比；缺失**不阻断**（数据卫生）。
3. 新增内容指纹能力：对 `tier ∈ {1,2}` 且 `in_synthesis=true` 的来源记录正文 sha256；提供 `--fingerprint` 输出与「变更检测」（与上次快照比对）。
4. 单测：`engine/tests/test_source_check.py` 增用例（字段合法 / 缺失提示 / 指纹变更）。

## 输出
代码 + 单测 + `metrics-dictionary.json` 备注（新增字段说明，不改阈值）。

## 验收标准
- 单测全绿；`python engine/tools/optimization_gate.py --only source_check` → 0 `[E]`。
- 抽样 3 条来源含 `evidence` 字段（可新增示例或补登记）。
- 未改 `verify_status` 取值集合、未改 R1–R7 规则。

## 禁止
- 不改 `optimization_gate.py` 的 `CHECKS` 清单（如需新增门禁项，先按 §4.7 合并顺序协调）。
- 不改报告正文；不放宽既有规则；不编造哈希。

## 完成前证据索引（必填）
1. 变更文件清单 + 关键 diff 摘要；
2. 命令与输出（单测 / `--only source_check`）；
3. 对齐声明：T-01 验收逐条 → 证据；
4. 回归声明：§5.1 的 R-REG-1 / R-REG-2 / R-REG-3 / R-REG-5 通过。
