# 共享事实卡片库（FACT-CARD LIBRARY）

> **定位**：`security`（AI 网安就业）、`industry-research`（AI 网安行业深度）、`competitive-intelligence`（竞争情报）、`apartment`（迪拜公寓监测）四类报告的**共享事实底座**。所有事实在此唯一一次定义，报告正文以 `[FC-<域>-<序号>]` 指针引用，避免多份报告内容同质化。
>
> **规范**：字段与引用规则见 [信息分层规范](../templates/information-layering-spec.md) 第五节。
>
> **纪律**：新增事实必须先登记卡片；卡片变更须记录来源与更新内容；禁止无来源新增。

## 文件

| 文件 | 域 | 说明 |
|---|---|---|
| `security_fact_cards.json` | SEC | 就业 / 人才 / 薪资 / 证书 / 签证 |
| `industry_research_fact_cards.json` | IND | 行业规模 / 产业链 / 玩家 |
| `competitive_intelligence_fact_cards.json` | CI | 竞争格局 / 份额 / 动作 |
| `apartment_fact_cards.json` | APT | 价格 / 供需 / 租赁 / 宏观（迪拜公寓） |

## 字段

| 字段 | 说明 |
|---|---|
| `card_id` | `FC-<域>-<三位序号>`，全域唯一 |
| `fact` | 事实陈述（唯一一次定义） |
| `source` | 来源机构 + URL + 年份 |
| `tier` | 1 官方一手 / 2 行业机构 / 3 挂牌门户 / 4 媒体转述 |
| `verify_status` | 已核验 / 部分核验 / 未核验 |
| `level` | 已核验事实 / 部分核验 / 推断 / 假设 |
| `updated` | 最近更新日期（YYYY-MM-DD）与更新内容摘要 |
| `indicators` | 关联指标编号（指针） |
| `used_by` | 引用该卡片的业务线标识（可多个；`fact_card_check` 据此动态派生共享事实域） |

## 校验

```bash
python engine/tools/fact_card_check.py            # 卡片库结构 + 引用可解析 + 共享域覆盖 + FC-04 一致性
python engine/tools/fact_card_check.py --json
```

退出码 0/1/2（通过 / 有 `[E]` / 仅 `[W]`）。

- FC-01–03：结构 / 引用可解析 / 共享域覆盖（新报告 `[E]`，历史 `[W]`）；
- FC-04：卡片 `level` 不得高于 `verify_status` 允许上限（`verification_vocab.is_consistent`，
  恒 `[E]`，结构性，与 FC-01/02 同档）。
