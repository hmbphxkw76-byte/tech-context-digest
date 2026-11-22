# 核验收口报告（VERIFICATION-CLOSURE v1.0）

> 日期：2026-11-22｜范围：全仓库报告 + 全部 `.md` 文档 + index / hub 页面
> 判级：`已核验`（命令实测 / 一手来源原文摘录）/ `部分核验`（抽样 / 口径差异）/ `推断` / `假设`
> 分支：`task/verification-closure-8b3dae0b`（独立 worktree 隔离，未触碰并行会话工作区）
> 输入：`engine/docs/information-verification-spec.md`、`optimization_gate.py`（31 项）、`verification_ledger.jsonl`

## 1. 范围与方法

- **对象**：22 份已交付 HTML 报告（16 条业务线）、353 份 `.md` 文档、`index.html` / `reader.html` 及全部 hub 页面。
- **方法**：① 统一门禁 + 审计四环节确定性体检；② 来源登记 ↔ 核验台账 ↔ 事实卡片 ↔ 报告信息等级一致性扫描；③ 对**决策关键指标**逐条 `web_fetch` 回一手来源复核（7 个并行子代理按业务线分组，只读、证据摘录、不得编造）；④ 高置信发现回写报告与登记。
- **并行会话处置**：检出时共享工作区存在活跃会话 `273f7c79`（未提交改动，致门禁 2 项 `[E]`）。依「不影响并行会话」约束，本任务在独立 worktree（`.meituan-catpaw/5833106238/worktrees/verification-closure`）内推进，仅提交本任务文件。

## 2. 基线与收口结果

| 项 | 收口前 | 收口后 | 判定 |
|---|---|---|---|
| 统一门禁 | clean main：0 `[E]` / 5 `[W]`（共享区因并行会话 2 `[E]`） | **0 `[E]` / 5 `[W]`**（exit 2，均为既有基线） | 已核验 |
| 核验台账 | 611 条 / 14 条业务线 | **626 条 / 15 条业务线**；seq 连续、`prev_hash` 链接、hash 重算一致 | 已核验 |
| 来源登记 ↔ 台账 | `immigration/dubai` 11 条来源**未入台账** | **0 缺口**；登记状态与台账末态一致 | 已核验 |
| 来源登记总数 | 622 条 | **626 条**（新增 4 条官方深链） | 已核验 |
| 事实卡片 | 31 张，FC-04 无违规 | 无违规 | 已核验 |
| 发布指纹 | — | 22/22 一致，漂移 0 | 已核验 |
| 页面 / hub / 链接 | — | `page_build` 24 通过 0E0W；`hub` / `links` 通过 | 已核验 |

## 3. 逐条核验发现（决策关键指标）

判定取值：`confirmed` / `partially_confirmed` / `discrepancy` / `unreachable` / `no_source`。

### 3.1 content/economy/dubai/apartment（G01–G04 政策阈值）

| 指标 | 宣称值 | 一手来源 | 判定 | 处置 |
|---|---|---|---|---|
| G01 黄金签证房产门槛 | AED 2,000,000 | u.ae 官方页（Updated 28 Jul 2026） | **confirmed** | 升级为已核验（4 份报告） |
| G02 CBUAE 按揭 LTV | 首套 ≤5m 80%；非居民 50–65% | CBUAE Rulebook | **partially_confirmed** | 修正为：国民首套 85% / 外籍 80%；二套 65%/60%；期房 50% |
| G03 DLD 过户费 | 约 4% | DLD 官方（销售登记页） | **confirmed** | 升级为已核验 |
| G04 期房托管 / Oqood | 2007 年第 8 号法 | DLD 官方 FAQ | **confirmed** | 升级为已核验（2007-06-28 生效，留存 5% 一年） |
| M11 就业 / 失业率 | 调查 10-13 启动 | DDSE 官方页（日期 2026-10-28） | **partially_confirmed** | 日期口径待修；5,000 户一致 |
| M19 迪拜实际 GDP | AED 473bn（H1） | 无官方页 | **no_source** | 量级存疑，已标注「不得作为决策输入」 |

### 3.2 content/economy/trends（2026-11-27 期）

| 指标 | 宣称值 | 一手来源 | 判定 | 处置 |
|---|---|---|---|---|
| K05 能源 / 食品分项 | 19.1% / 0.8% | Eurostat | **discrepancy** | 更正为 **21.0% / 1.5%** |
| 欧元区 Q3 GDP / 9 月失业率 | +0.5% / 6.2% | Eurostat | **discrepancy** | 更正为 **+0.4% / 6.5%**（EU 口径 0.5% / 6.2%） |
| K03 美国 Q3 GDP | +3.4% | BEA | confirmed | 维持 |
| K06 / K07 中国 GDP / CPI / PPI | +4.5% / +0.7% / +5.7% | 国家统计局 | confirmed | 维持 |

### 3.3 content/education/study-abroad

| 指标 | 宣称值 | 一手来源 | 判定 | 处置 |
|---|---|---|---|---|
| 丹麦求职居留 | 3 年 → 6 个月或 1 年 | nyidanmark.dk | **discrepancy** | 更正为 **3 年 → 1 年**（博士仍 3 年），无「6 个月」档 |
| 美国 SEVP 固定居留期 | 2026-07-17 final rule | ice.gov / 联邦法院 | **discrepancy** | 已标注 **2026-11-16 被实体判决撤销（vacatur）**，未生效 |
| 全球公约缔约方 | 未给值 | UNESCO | confirmed | 可回填 **43**（2026-11） |
| 里斯本公约 | 生效日待核 | UNESCO | confirmed | **1999-02-01 生效，57 缔约方（2024-11）** |

### 3.4 content/international/immigration(+dubai)

| 指标 | 宣称值 | 一手来源 | 判定 | 处置 |
|---|---|---|---|---|
| 美国 H-1B 配额 | 65,000 / 20,000 | USCIS | **confirmed** | U-03 可消号 |
| 黄金 / 绿卡门槛 | AED 2,000,000 / 30,000 / 15,000 / 360,000 等 | ICP 官方 | **confirmed** | 维持 |
| 黄金签证年限 | u.ae 5 年 vs ICP 10 年 | u.ae / ICP | **discrepancy（坐实）** | 房地产 / 企业家 / 优秀高中生三类均冲突，维持并列 |
| 处理时长 / 费用 | 待核 | ICP / GDRFA 服务卡 | **confirmed** | ICP 2 天 / GDRFA 48 小时；费用按年 100 AED |
| 境外停留上限 | 具体月数待核 | u.ae / ICP | **partially_confirmed** | 口径为「通常 6 个月基准 + 超限许可」，无固定月数 |

### 3.5 content/political / content/society

| 指标 | 宣称值 | 一手来源 | 判定 | 处置 |
|---|---|---|---|---|
| 德国联邦议院议席 | 基本 598 | bundestag.de | **discrepancy** | 区分「法定 598（2017/2021）」与「第 21 届实际 **630**（2025-02 后）」 |
| CPI 2025 丹麦 | 90 分 | transparency.org（官方页拦截，二手一致） | **discrepancy** | CPI 2024 = 90；**CPI 2025 = 89** |
| 世界 65+ 占比 | 约 8% | World Bank WDI（源自 UN WPP） | **discrepancy** | 更正为 **约 10%（10.20%，2024）** |
| 日本 65+ | 约 3625 万 / 29.3% | stat.go.jp | **partially_confirmed** | 官方 36,243 千人（3624.3 万），29.3% 确认 |
| 中国 2024 65+ / 60+ | 2.20 亿 / 15.6%；22.0% | 国家统计局 | confirmed | 维持 |

### 3.6 content/tech/ai-security（含 insight 综合层）

| 指标 | 宣称值 | 一手来源 | 判定 | 处置 |
|---|---|---|---|---|
| 微软–G42 152 亿美元计划 | 报告称「未获证实」并剔除 | news.microsoft.com（微软官方） | **discrepancy** | 官方确认存在；已恢复并注明为**公告 / 计划口径** |
| 微软–G42 股权 + 基金 | 15 亿 + 10 亿美元 | blogs.microsoft.com | confirmed | 维持 |
| ISC2 技能缺口 | AI 41% / 88% | isc2.org | confirmed | 维持 |
| Mordor 市场规模 | 8.2 亿 → 15.1 亿美元，CAGR 10.66% | mordorintelligence.com | confirmed | 维持 |
| Gartner / GMI / Hub71 / CPX / G42 官网 | — | Cloudflare / 反爬 | **unreachable** | 维持待复核，未升级 |
| insight DC-AI-SEC-01 证据强度 | 摘要标「强」、明细标「中」 | 内部不一致（FC-SEC-005/006 为部分核验） | **discrepancy** | 统一为 **中** |

### 3.7 content/tech/ai-application

| 指标 | 宣称值 | 一手来源 | 判定 | 处置 |
|---|---|---|---|---|
| UAE AI 市场（IMARC） | 7.057 亿 → 43.873 亿美元，CAGR 21.84% | imarcgroup.com（索引快照） | confirmed | 维持（单源） |
| 四家薪酬指南「均 gated」 | Michael Page / Hays / Cooper Fitch / Charterhouse | 各官网 | **discrepancy** | Charterhouse 为**直接 PDF 直链**（未 gated） |
| LLM API 份额括注 | 「合计 86%」 | menlovc.com | **partially_confirmed** | 86% 仅 Anthropic+OpenAI，三者相加 95% |
| 黄金签证 30,000 AED | u.ae 未列，需 ICP 确认 | u.ae / ICP / WAM 2022 | **partially_confirmed** | 官方措辞为**月薪**（非基本工资），源自 2022 执行条例 |

## 4. 已回写修正清单

**报告层（10 份）**：apartment 4 份（G01–G04 政策阈值 + 未核验清单 + 场景切片）、trends 11-27 期（K05 分项 / 欧元区口径）、study-abroad（丹麦 / SEVP）、society（世界 65+）、political（德国议席 / CPI）、ai-security/dubai（152 亿）、insight（证据强度 强→中）。

**登记 / 台账层**：
- `immigration/dubai` 11 条来源补登台账（seq 612–622）；
- apartment 新增 4 条官方深链（S-082 u.ae 黄金签 / S-083 DLD 销售登记 / S-084 DLD FAQ 托管 / S-085 CBUAE Rulebook LTV），各含 `web_fetch` 证据与快照日；
- 台账 `source_verified` 事件同步追加，链校验通过。

## 5. 未决 / 不可核验清单（不虚报）

- **反爬 / gated**：澳大利亚 homeaffairs（Akamai）、美国 travel.state.gov / ICC / ICJ（Cloudflare）、Gartner / GMI / Hub71 / CPX / G42 官网、OECD 主站、Khaleej Times、hiredeveloper.ae（含提示注入内容）。维持 `unreachable`。
- **非英语原文**：中国全国人大口径、日 / 德 / 韩法律原文条款对照——受来源语言政策约束，标 `no_source`。
- **口径待对齐**：u.ae 与 ICP 黄金签证年限（5 年 vs 10 年）；EAG 与 UIS 的 GER/NER 定义映射；韩国居民登记 ↔ KOSIS 口径映射。
- **系统性治理提示（不属本 PR 范围）**：622 条登记中 **493 条** `evidence.note` 为「登记信息人工核对（未抓取正文，故无 archive_hash）」却标 `verified`，与 SPEC 第二节「已核实 = 内容级」语义存在口径差。建议单独立项按业务线分批补快照 / 降级，不在本收口 PR 内大面积改动。

## 6. 回归验证

| 项 | 结果 |
|---|---|
| 统一门禁 | **0 `[E]` / 5 `[W]`**（source_check 49 警告、metric_audit、ruff、mypy、monitoring_render，均基线内） |
| 核验台账 | 626 条，链校验通过 |
| 页面 / hub / 链接 | `page_build` 24 通过；`hub` / `links` / `validate_layout` 通过 |
| 发布指纹 | 22/22 一致，漂移 0 |
| 报告归位 / 周期 / 结构 | 通过 |
| 事实卡片 FC-01–FC-04 | 无违规 |

## 7. 判定摘要

| 维度 | 结论 |
|---|---|
| 台账覆盖完整性 | **已闭环**（0 缺口，15 条业务线全覆盖） |
| 决策关键指标一手核验 | **部分闭环**：apartment G01/G03/G04、H-1B 配额、黄金/绿卡门槛、处理时长等**已核验**；其余受反爬 / 非英语 / 口径冲突阻塞，已如实标注 |
| 报告信息质量 | 8 类 discrepancy 已回写修正；未决项显式列出，无虚报 |
| 仓库清洁 | 本任务 worktree 内提交，共享工作区未被本任务改动 |
