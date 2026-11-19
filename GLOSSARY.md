# 术语表（GLOSSARY）

> **状态**：现行（随规范演进增补；新增术语须先有事实源，再登记）
> **定位**：tech-context-digest 仓库级术语单一上下文，与 [AGENTS.md](AGENTS.md) 配套。
> **原则**：只给「定义 + 事实源指针」，**不复述**事实源的数值 / 清单（见 [engine/docs/architecture-development-standard.md](engine/docs/architecture-development-standard.md) §1.3）。
> **配套**：受控词库入口 [engine/vocabulary/INDEX.md](engine/vocabulary/INDEX.md)；决策记录见 [engine/docs/adr/](engine/docs/adr/)。

## 架构与分层

| 术语 | 定义 | 事实源 |
|---|---|---|
| 三层架构 | 仓库按内容层 / 引擎层 / 资产层组织，不得跨层存放 | [engine/tools/layout.json](engine/tools/layout.json) |
| 内容层（content/） | 业务专属：报告、业务提示词、`business-config.md`、业务脚本 | [engine/tools/layout.json](engine/tools/layout.json) |
| 引擎层（engine/） | 跨主题复用：模板、提示词、工具、词库、质量、审计、测试、规范 | [engine/tools/layout.json](engine/tools/layout.json) |
| 资产层（data/） | `raw/` 原始抓取、`processed/` 清洗后台账、`assets/` 图片图表 | [engine/tools/layout.json](engine/tools/layout.json) |
| 单一事实源 | 同一事实只在一处定义，其余位置只写指针 | [engine/docs/architecture-development-standard.md](engine/docs/architecture-development-standard.md) |
| 生成物豁免 | 机器生成留痕按生成器模式命名，确定性可重放，不得手工编辑 | [engine/docs/architecture-development-standard.md](engine/docs/architecture-development-standard.md) |

## 主题与维度

| 术语 | 定义 | 事实源 |
|---|---|---|
| 主题（theme） | 六主题：economy / tech / education / international / political / society | [engine/tools/layout.json](engine/tools/layout.json) |
| 维度（dimension） | 业务线的结构段：category（细分）/ region（地区） | [engine/tools/layout.json](engine/tools/layout.json) |
| 维度顺序 | 各主题在 layout.json 自行声明；economy 为 region→category，其余五主题为 category→region | [engine/tools/layout.json](engine/tools/layout.json) |
| 可选维度（optional_dimensions） | region 为可选；缺省时业务线直接以 category 段落位 | [engine/tools/layout.json](engine/tools/layout.json) |
| 地区段（regional_segment） | 独立地区分组段；当前为空串 | [engine/tools/layout.json](engine/tools/layout.json) |
| 业务线 | 位于 `content/<theme>/<维度段...>/` 的报告集合，以 `prompts/business-config.md` 为锚点 | [engine/tools/layout.json](engine/tools/layout.json) |
| 报告类型（type） | 报告的节拍 / 模板分类，由类型登记唯一登记、多处生成 | [engine/templates/template-registry.md](engine/templates/template-registry.md) |

## 报告周期与交付

| 术语 | 定义 | 事实源 |
|---|---|---|
| 周期（cycle） | baseline / monthly / quarterly / annual / weekly | [engine/docs/report-cycle-windows.md](engine/docs/report-cycle-windows.md) |
| 基线（baseline） | 对比锚，常驻展示，不环比、不高亮 | [engine/docs/report-cycle-windows.md](engine/docs/report-cycle-windows.md) |
| 本期更新 | 某周期最新一期的高亮标记（含环比基期） | [engine/docs/report-cycle-windows.md](engine/docs/report-cycle-windows.md) |
| 信息等级 | 已核验 / 部分核验 / 推断 / 假设 | [engine/templates/information-layering-spec.md](engine/templates/information-layering-spec.md) |
| 决策卡 | 核心判断的结论 / 证据强度 / 触发条件 / 反向证据 / 信息充分度 | [engine/templates/decision-delivery-spec.md](engine/templates/decision-delivery-spec.md) |
| 事实卡片（FC） | 事实唯一定义处，正文用「指标编号 + 指针」引用 | [engine/fact_cards/](engine/fact_cards/) |
| 行动协议 | 行动项五要素 + 三档优先级 | [engine/templates/decision-delivery-spec.md](engine/templates/decision-delivery-spec.md) |

## 流程与门禁

| 术语 | 定义 | 事实源 |
|---|---|---|
| 统一门禁 | P0/P1/P2 全部确定性检查的单一入口 `optimization_gate.py` | [engine/tools/optimization_gate.py](engine/tools/optimization_gate.py) |
| 阶段（N0–N8） | 需求 → 采集 → 分级 → 分类 → 生成 → 渲染 → 校验审计 → 发布 → 运维 | [engine/docs/report-pipeline-system.md](engine/docs/report-pipeline-system.md) |
| 防线（G0–G8） | 各阶段就地门禁 | [engine/docs/report-pipeline-system.md](engine/docs/report-pipeline-system.md) |
| 提交网关 | `repo_sync.py`（run / push / pr / branch / branch-rename / branch-audit） | [engine/docs/multi-session-git-protocol.md](engine/docs/multi-session-git-protocol.md) |
| 分支命名 | 受管分支 `task/<slug>-<session8>`，经 PR 合并，禁止直推 `main` | [engine/docs/multi-session-git-protocol.md](engine/docs/multi-session-git-protocol.md) |

## 数据与盲区

| 术语 | 定义 | 事实源 |
|---|---|---|
| 来源分级 | ① 官方一手 > ② 行业机构 > ③ 挂牌门户 > ④ 媒体转述 | [engine/report-audits/data-acquisition-checklist.md](engine/report-audits/data-acquisition-checklist.md) |
| 双源确认 | 进入信号合成的数值须 ≥2 个独立来源方向一致 | [engine/report-audits/data-acquisition-checklist.md](engine/report-audits/data-acquisition-checklist.md) |
| 盲区（blind spot） | 影响结论但缺可核验数据的事项，登记于盲区台账 | [engine/report-audits/blind-spot-ledger.md](engine/report-audits/blind-spot-ledger.md) |
| 消号 | 盲区证据条件满足后关闭；条件：① 官方一手 + 双源 / ② 代理替代 + 校准 / ③ 敏感性证明 | [engine/report-audits/blind-spot-ledger.md](engine/report-audits/blind-spot-ledger.md) |
| 责任周期 | 盲区未消号时的责任窗口（YYYY-MM），逾期须更新 | [engine/report-audits/blind-spot-ledger.md](engine/report-audits/blind-spot-ledger.md) |
| 代理替代 | 以高频代理 + 校准方式替代缺失官方序列（须记录代理与校准） | [engine/report-audits/blind-spot-ledger.md](engine/report-audits/blind-spot-ledger.md) |

## 其他

| 术语 | 定义 | 事实源 |
|---|---|---|
| hub | 汇总页 | [engine/tools/build_hub.py](engine/tools/build_hub.py) |
| reader | 阅读页 | [reader.html](reader.html) |
| canonical 令牌 | 报告样式唯一事实源（`report_style.py` / `build_hub.py`） | [engine/docs/page-build-spec.md](engine/docs/page-build-spec.md) |
| ADR | 架构决策记录，位于 `engine/docs/adr/`，编号 0001 起 | [engine/docs/architecture-development-standard.md](engine/docs/architecture-development-standard.md) |
