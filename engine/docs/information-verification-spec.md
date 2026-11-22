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
4. 来源归一化原语（URL / 机构名 / 主机 / 日期）；
5. 报告层信息等级 ↔ 来源核验状态一致性（RV-01..03，见 §二·补）。

**非目标（本期不做）**
- 不改动存量 `source_registry.json` 的取值（英文枚举仍为数据层 canonical）；
- 不引入分层抽检 / 已审计徽章 / 阶段闸左移（与本仓库结构无耦合，避免过度工程）。

## 二、核验状态词表（单一事实源）

单一事实源：`engine/tools/verification_vocab.py`。两套词形语义等价，**不得**再各自定义：

| 语义 | 数据层 canonical（英文） | 卡片 / 报告层 canonical（中文） | 允许的最高信息等级 |
|---|---|---|---|
| 已核实 | `verified` | `已核验` | 已核验事实 |
| 部分核实 | `media_unverified` | `部分核验` | 部分核验 |
| 无法核实 | `unverifiable` | `未核验` | 假设 |

- 信息等级：`已核验事实 / 部分核验 / 推断 / 假设`（INFORMATION-LAYERING-SPEC 第四节）。
  canonical 为「已核验事实」；「已核验」是报告 inline 标记 / 历史用词别名，
  由 `normalize_info_level` 归一，不另立强度。
- 决策摘要仅允许 `已核验事实 / 部分核验`（`is_decision_safe`）。
- 一致性判定：`is_consistent(level, status, kind)` —— 信息等级强度不得高于核验状态上限。
- 门禁行为：
  - `source_check` R8 接受两套词形，非 canonical 词形给 `[W]`（数据卫生，不阻断）；
  - `fact_card_check` 接受两套词形，非法即 `[E]`；
  - `fact_card_check` FC-04 执行卡片 `level ≤ verify_status` 上限（恒 `[E]`，结构性，与 FC-01/02 同档）；
  - `report_verification_check` 执行报告层一致性 RV-01..03（新报告 `[E]` / 历史报告 `[W]`，
    两级 gate-period，与内容四门禁同档）。

### 二·补、报告层信息一致性（RV-01..03）

单一事实源：`engine/tools/report_verification_check.py`。来源状态取自各业务线
`data/processed/**/source_registry.json`（R8 约定），链接按归一化 URL 精确匹配，
避免机构名缩写导致的模糊误判；陈述单元取非嵌套的 `tr / li / p`（不用通用 `div`，
否则整表 / 时间线会把多个陈述并成一个单元而漏判）。

| 项 | 规则 | 判定依据 |
|---|---|---|
| RV-01 | 决策摘要纯净：`decision-summary` 内不得出现 `lvl-inferred` / `lvl-assumption`，不得链接 `unverifiable` 来源，不得出现「未核验」状态文本 | 决策摘要仅允许已核验 + 部分核验 |
| RV-02 | 未核验来源呈现：`lvl-verified` / `lvl-partial` 单元若仅链接 `unverifiable` 来源，或 `lvl-verified` 仅链接 `media_unverified` 来源，判不一致 | 信息等级不得高于来源上限（`is_consistent` 同口径） |
| RV-03 | 来源状态文本一致：单元内显式状态文本（`· 未核验` / `· 部分核验`）与 `lvl-*` 标记冲突时判不一致 | 报告自洽 |

- 单元内同时存在已核验 / 部分核验来源支撑时，不判 RV-02（避免误报）；
- 接线：统一门禁 `optimization_gate` 的 `report_verification` 项；
  `pipeline_manifest.json` 的 G2（生成前）与 G4（生成后）就地门禁；
  `content-update.yml` 在创建生成任务 Issue 前执行统一门禁，构成「生成前核验」。

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
| 跨层一致性 | `verification_vocab.is_consistent` | `fact_card_check` FC-04 | E（结构性） |
| 报告层一致性 | `report_verification_check.py` RV-01..03 | `optimization_gate` → `report_verification`；G2 / G4 | E（新）/ W（历史） |
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
