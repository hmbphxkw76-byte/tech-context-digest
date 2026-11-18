# 领域文档（Domain Docs）

> **状态**：现行约定
> **用途**：说明工程类 skill 在探索本仓库前应如何消费领域文档。

## 探索前先读这些

按优先级：

1. **`AGENTS.md`**（仓库根）：仓库级硬性约束（目录维度优先级、页面构建规范、信息分层与决策交付、统一门禁、多会话 Git 协议、报告生成规则）。
2. **`engine/docs/`**：体系与规范正文——全链路体系、页面构建规范与治理、流程复用清单、分类体系、Git 协议。
3. **`engine/templates/`**：通用基座、监测报告通用规范、信息分层 / 决策交付规范、类型注册表。
4. **`engine/vocabulary/INDEX.md`**：受控词表索引。
5. **`GLOSSARY.md` / `GLOSSARY-MAP.md` / `engine/docs/adr/`**（仓库根）：若存在则读；**不存在时 proceed silently**，不要提示缺失、不要建议预先创建。

## 术语与决策

- 输出中命名领域概念时，使用 `engine/vocabulary/` 与类型注册表定义的术语，不要漂移到同义词。
- 若需要的概念尚未登记，说明这是缺口（留给 `/domain-modeling`），不要自造项目不用的语言。
- 若输出与既有 ADR 冲突，显式指出而不是静默覆盖：

  > _与 ADR-0007（事件溯源订单）冲突，但值得重开讨论，因为……_

## 目录结构速查

```
/
├── AGENTS.md                     # 仓库级 Agent 硬性约束
├── content/                      # 内容层：六主题
│   ├── economy/                  # 经济（<region>/<category>/）
│   ├── tech/                     # 科技（<category>/<region>/）
│   ├── education/                # 教育（<category>/<region>/）
│   ├── international/            # 国际（<category>/<region>/）
│   ├── political/                # 政治（<category>/<region>/）
│   └── society/                  # 社会（<category>/<region>/）
├── engine/                       # 引擎层（跨主题复用）
│   ├── docs/                     # 体系 / 规范 / 协议 / 治理
│   ├── templates/                # 通用基座 + 通用规范 + 类型模板
│   ├── prompts/                  # 泛用提示词（按类型）
│   ├── vocabulary/               # 受控词表（INDEX.md 为入口）
│   ├── fact_cards/               # 事实卡片
│   ├── tools/                    # 生成器与校验器
│   ├── quality/                  # 内容质量评估与修复
│   ├── audit/                    # 审计管理体系
│   ├── report-audits/            # 审计产出记录
│   └── tests/                    # 单元测试
└── data/                         # 资产层
    ├── raw/                      # 原始抓取
    ├── processed/                # 清洗后数据（<theme>/<维度段...>/）
    └── assets/                   # 图片 / 图表
```
