# 信息核验机制规范（INFORMATION-VERIFICATION-SPEC v1.0）

> 目标：在既有「来源登记 + R1–R9 门禁」之上，补齐**跨层词表统一、核验留痕哈希链、
> 来源级定期复核、来源归一化**四项机制，使信息质量「可核验、可追溯、可重放」，
> 而不仅是一次性登记。
>
> 单一事实源：本文件。工具实现见 `engine/tools/verification_*.py` 与
> `engine/tools/source_normalize.py`；门禁接入见 `optimization_gate.py`
> 的 `verification_ledger` 项；定期复核接入 `scheduled-maintenance.yml`。

## 一、范围与非目标

**范围内**
1. 核验状态词表映射（数据层英文枚举 ↔ 卡片 / 报告层中文等级）；
2. 核验台账哈希链（append-only，防篡改 / 防删减）；
3. 来源定期复核与到期告警（按机构 tier 重核周期）；
4. 来源归一化原语（URL / 机构名 / 主机 / 日期）。

**非目标（本期不做）**
- 不改动存量 `source_registry.json` 的取值（英文枚举仍为数据层 canonical）；
- 不引入报告层信息等级与来源状态的逐条 proximity 一致性（留待二期）；
- 不引入分层抽检 / 已审计徽章 / 阶段闸左移（与本仓库结构无耦合，避免过度工程）。

## 二、核验状态词表（单一事实源）

单一事实源：`engine/tools/verification_vocab.py`。两套词形语义等价，**不得**再各自定义：

| 语义 | 数据层 canonical（英文） | 卡片 / 报告层 canonical（中文） | 允许的最高信息等级 |
|---|---|---|---|
| 已核实 | `verified` | `已核验` | 已核验 |
| 部分核实 | `media_unverified` | `部分核验` | 部分核验 |
| 无法核实 | `unverifiable` | `未核验` | 假设 |

- 信息等级：`已核验 / 部分核验 / 推断 / 假设`（INFORMATION-LAYERING-SPEC 第四节）。
- 决策摘要仅允许 `已核验 / 部分核验`（`is_decision_safe`）。
- 一致性判定：`is_consistent(level, status, kind)` —— 信息等级强度不得高于核验状态上限。
- 门禁行为：
  - `source_check` R8 接受两套词形，非 canonical 词形给 `[W]`（数据卫生，不阻断）；
  - `fact_card_check` 接受两套词形，非法即 `[E]`。

## 三、核验台账哈希链

单一事实源：`engine/tools/verification_ledger.py`；落盘
`engine/audit/records/verification_ledger.jsonl`（生成物豁免路径）。

- 事件结构：`{seq, prev_hash, hash, ts, actor, event, payload}`；
- 哈希：`sha256(prev_hash + canonical_json(payload))`，首条 `prev_hash = "0"*64`；
- 事件类型：`source_verified` / `source_reviewed` / `source_status_changed`；
- **append-only**：只追加，禁止重写既有行；合并冲突须重基追加，不得改写
  `seq / prev_hash / hash`；
- `verify` 三项校验：seq 从 1 连续、`prev_hash` 链接、`hash` 重算；
- `backfill` 从现有登记回填初始事件，台账非空时幂等跳过（`--force` 才重填）；
- 门禁：`optimization_gate` 的 `verification_ledger` 项调用 `verify`，链断裂 = `[E]` 阻断。

## 四、来源定期复核

单一事实源：`engine/tools/verification_review.py`；落盘
`engine/audit/records/pending_verification.json`。

- 重核周期（按机构 tier）：tier 1 = 180 天，tier 2 = 120 天，tier 3 = 90 天，
  tier 4 = 60 天；tier 缺失 / 非法按最严 60 天。
- 基准日：`evidence.snapshot_date` 优先，其次 `updated`；均缺记 `unknown`。
- 临期阈值：达到周期 80% 记 `due_soon`，超过记 `overdue`。
- 周期锚定：`--period` 缺省 `auto`（当前自然月），基准日取该月最后一日；
  **不取墙钟**，保证同周期可重放。
- 退出码：0 无到期 / 临期；2 存在到期或临期（告警，不阻断提交）。

## 五、来源归一化

单一事实源：`engine/tools/source_normalize.py`。

- `normalize_url`：NFKC、小写 scheme/host、去 fragment、去跟踪参数；路径保持原样；
- `normalize_publisher`：NFKC、全角空格→半角、压缩空白、去首尾噪声标点；
- `host_key`：注册域（去 `www.`），用于跨登记归并；
- `normalize_date`：`YYYY-MM-DD` / `YYYY/MM/DD` / `YYYY年M月D日` / 英文月日年 → ISO。

**分工**：`source_check.py` 内部的 `normalize_url` 服务 R1/R6 的**可达性**比对，
刻意保守；本模块服务**登记去重 / 归并 / 复核**。两者不得互相替换。

## 六、接入矩阵

| 机制 | 工具 | 门禁 / CI | 级别 |
|---|---|---|---|
| 词表归一 | `verification_vocab.py` | `source_check` R8 / `fact_card_check` | W / E |
| 核验台账链 | `verification_ledger.py verify` | `optimization_gate` → `verification_ledger` | E（链断裂） |
| 台账回填 | `verification_ledger.py backfill` | `scheduled-maintenance.yml`（幂等） | E（执行失败） |
| 来源定期复核 | `verification_review.py` / `audit_tool verify-review` | `scheduled-maintenance.yml` | 告警（2 不阻断） |
| 来源归一化 | `source_normalize.py` | `source_check` R7（匹配用） | — |

## 七、确定性

- 台账与复核产物不含墙钟时间戳；复核基准日取 `--period` 锚定的周期末日；
- 台账 `ts` 为元数据，不入哈希，便于确定性重放；
- 回填 / 复核输出均按 `(business_line, source_id)` 排序。

## 八、版本迭代

- 版本号 / 变更流程同 PAGE-BUILD-SPEC 的治理约定；
- 破坏性变更须并行期 + 迁移说明；新增事件类型 / 词表值须同步本文件与测试。
