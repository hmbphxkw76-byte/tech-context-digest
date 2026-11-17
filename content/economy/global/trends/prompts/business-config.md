# 经济趋势周报 · 业务配置（business-config）

> **定位**：`content/economy/global/trends` 业务线的单一事实源。变量、受众、主题矩阵、来源分级、触发器、交付格式一律以本文件为准；周期提示词不复制这些内容，只给路径。
> **类型继承声明（四层体系）**：业务提示词 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（行业趋势周报型 trend-weekly）](../../../../../engine/templates/trend-weekly/prompt-weekly-monitor-template.md) × 本文件。冲突时以业务提示词为准。

---

## 一、变量区（固定值）

```
{{REGION}}               = 全球
{{TOPIC}}                = 全球宏观经济趋势（主要经济体视角）
{{REPORT_TYPE}}          = trend-weekly
{{CADENCE}}              = 周（weekly，日历节拍）
{{REGISTRY_PATH}}        = data/processed/economy/global/trends/economy_trend_ledger.md
{{REGISTRY_FORMAT}}      = md-ledger
{{SOURCE_REGISTRY_PATH}} = data/processed/economy/global/trends/source_registry.json
{{BASELINE_REPORT_PATH}} = reports/2026-11-13_weekly.html（首期周报，结构与结论锚；本业务线以首期周报为结构锚，机制建立走周报首期，未单独出九节基线文档）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/economy/global/trends
{{FRESHNESS_PRIORITY}}   = 最新官方页 > 上期值 > 预测值
{{SOURCE_LANGUAGE_RULE}} = 官方一手以英文为准；中文媒体仅作线索，数值须回官方页核验
```

## 二、受众定位

- **受众**：宏观经济研究团队 · 跨市场趋势监测（Macro Research）。
- **视角**：从主要经济体宏观基本面、贸易与产业链、新兴市场与大宗商品出发解读全球经济趋势。
- **结论边界**：可执行启示只给「条件 → 判读 → 框架性含义 → 风险提示」，不给具体买卖价位、汇率点位与仓位建议。

## 三、主题矩阵（固定 3 块，对应周报 s2–s4，不得增删）

| 板块 | 周报节 | 覆盖范围 | 不覆盖 |
|---|---|---|---|
| 主要经济体宏观基本面 | s2 | 美国、中国、欧盟、日本、韩国、德国、法国、英国、新加坡、澳大利亚、新西兰等主要经济体的 GDP、通胀、就业、货币政策与财政动态 | 企业微观财报与个股行情 |
| 贸易、供应链与产业政策 | s3 | 跨境贸易、关税与贸易协定、产业补贴、供应链重构与地缘经济措施 | 公司层面并购交易与未落数据的传闻 |
| 新兴市场与大宗商品 | s4 | 越南、马来西亚、沙特、阿联酋、卡塔尔等新兴与资源型经济体；能源与大宗商品价格对宏观的影响 | 加密资产与未公开的市场传闻 |

## 四、来源分级（四层实例化）

| 层级 | 机构清单（示例，持续维护） | 采信规则 |
|---|---|---|
| ① 官方一手 | IMF（WEO）、世界银行、OECD、BLS、BEA、美国财政部、中国国家统计局、中国人民银行、ECB、欧盟统计局、英国 ONS、日本内阁府、韩国 BOK、新加坡 MAS、澳大利亚 ABS、新西兰 Stats NZ / RBNZ、CBUAE、GASTAT、越南 GSO、马来西亚 DOSM / BNM、卡塔尔 PSA / QCB | 唯一可直接采信层，标「已核验」 |
| ② 行业机构 | IMF Blog、OECD Economic Outlook、各国央行研究简报与会议纪要 | 可采信；PDF 记录发布日期；预测分歧并列 |
| ③ 挂牌门户 / 数据库 | FRED、e-Stat、各国官方统计数据库 | 仅作数据快照，须注日期与版本 |
| ④ 媒体转述 | Reuters、Bloomberg、中文财经媒体 | 只作线索；数值标「需核实原文」并回官方页校验 |

## 五、触发器（`事件 → 受影响板块`）

- 主要央行议息会议与利率决议（美联储 / ECB / BOJ / BOK 等）→ s2 当期升级
- 主要经济体重磅宏观数据发布（GDP、CPI、就业）→ s2 当期升级
- 关税、贸易协定与产业政策重大动作 → s3 当期升级
- OPEC+ 产量决议、能源与大宗商品价格异动 → s4 当期升级
- 地缘冲突或突发事件影响供应链与新兴市场 → s3、s4 当期升级

## 六、交付格式与命名

- **纯 HTML 交付**（业务配置声明，走 monitoring-common-spec 第 1 节例外条款）：富样式手写自包含 HTML 为主交付物，落盘 `reports/{{YYYY-MM-DD}}_weekly.html`（日期 = 数据截止日）；md 源稿存 `sources/` 同名存档，**不参与 `md2html.py` 自动转换**（防止覆盖手工渲染）。
- 周报按归档保留策略滚动（weekly 保留 12 期，超限移入 `reports/archives/`）。

<!-- VOCAB-SYNC:BEGIN topic=economy do-not-edit -->
## 词汇速览（词汇库自动同步）

> 由 `engine/vocabulary/script/sync_vocab.py` 自动维护：词汇库 economy v1.3，共 48 条（同步于 2026-11-14T15:24:27）。标记区间内请勿手工编辑；词条变更走词汇库导入流程（engine/vocabulary/README.md 第三节），同步机制见第九节。

- **经济体与国家**（22）：美国（United States、USA、U.S.）；中国（China、中华人民共和国）；新加坡（Singapore）；日本（Japan）；韩国（South Korea、Korea）；德国（Germany）；法国（France）；英国（United Kingdom、UK）；新西兰（New Zealand）；澳大利亚（Australia）；阿联酋（United Arab Emirates、UAE）；沙特（Saudi Arabia、沙特阿拉伯、KSA）；越南（Vietnam、Viet Nam）；马来西亚（Malaysia）；卡塔尔（Qatar）；欧元区（Eurozone、欧元经济区）；新兴市场（Emerging Markets、EM）；发达经济体（Advanced Economies）；前沿市场（Frontier Markets）；科威特（Kuwait）；巴林（Bahrain）；阿曼（Oman）
- **区域经济组织**（10）：欧盟（European Union、EU）；G7（七国集团、Group of Seven）；G20（二十国集团、Group of Twenty）；金砖国家（BRICS、金砖机制）；海湾合作委员会（GCC、Gulf Cooperation Council、海湾六国）；OPEC（石油输出国组织、欧佩克）；东盟（ASEAN、东南亚国家联盟）；APEC（亚太经合组织、Asia-Pacific Economic Cooperation）；WTO（世界贸易组织、World Trade Organization）；IEA（国际能源署、International Energy Agency）
- **经济概念**（16）：全球主要经济体（全球主要经济体国家、Major Economies）；购买力平价（PPP、Purchasing Power Parity）；经济周期（Business Cycle、繁荣衰退周期）；滞胀（Stagflation）；软着陆与硬着陆（Soft Landing、Hard Landing）；人口红利（Demographic Dividend）；城镇化率（Urbanization Rate）；全要素生产率（TFP、Total Factor Productivity）；贸易顺差与逆差（Trade Surplus、Trade Deficit）；外汇储备（Foreign Exchange Reserves）；主权债务（Sovereign Debt、公共债务）；基尼系数（Gini Coefficient）；中等收入陷阱（Middle-Income Trap）；石油美元（Petrodollar）；产业转移（Manufacturing Relocation、供应链转移）；海湾国家（Gulf States、Gulf Countries、海湾地区国家）
<!-- VOCAB-SYNC:END -->

## 七、信息分层与决策交付（强制项）

- **分层交付**：决策摘要（≤1 屏，仅结论）/ 证据层 / 原始层；共享 boilerplate 上移通用基座第十节，不复制（规范：`engine/templates/information-layering-spec.md`）。
- **信息等级**：已核验 / 部分核验 / 推断 / 假设；决策摘要仅引用已核验 + 部分核验；新增信息模块「本期新增 X / 修正 Y / 无变化 Z / 假设核验进度 k/n」。
- **指针引用**：事实唯一定义于台账 / 事实卡片（`[FC-…]`），正文用「指标编号 + 指针」。
- **决策卡与行动协议**：核心判断输出决策卡；行动项按「触发条件 + 阈值 + 责任角色 + 时限 + 验证指标」并分三档优先级（规范：`engine/templates/decision-delivery-spec.md`）。
- **阈值校准**：首次中期回测 2027-06；校准完成前信号灯标注「预校准（ex-ante）」。
- **场景切片**：主场景 **政策制定**；次场景 **投资决策**。
- **版本治理**：核验 / 收敛型运行不升级版本号，标注「本期读数时点」。
- **盲区**：P0 四类（就业 / 收入 / 空置 / 竣工）优先消号。

---

## 八、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 业务线建立：按 trend-weekly 类型接入目录规范、提示词与校验链；台账骨架首建（v1.0）；词汇库 economy 主题（17 条）绑定接入「词汇速览」标记区间 |
