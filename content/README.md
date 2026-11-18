# 内容层（content/）

研究报告内容按六主题组织；业务线位于 `content/<theme>/<维度段...>/`，维度顺序由 `engine/tools/layout.json` 声明（economy 为 `<region>/<category>`，其余主题为 `<category>/<region>`），以 `prompts/business-config.md` 为单一事实源，报告落 `reports/`。`region` 为可选维度（六个主题均以 `optional_dimensions` 声明），省略 region 的业务线直接以 category 段落位（如 `content/economy/trends`、`content/tech/weekly-roundup`、`content/education/education-system`）。

## economy — 经济

- `content/economy/insight` — 跨研究线决策仪表盘
- `content/economy/trends` — 全球经济趋势周报
- `content/economy/dubai/apartment` — 迪拜公寓住宅市场监测

## tech — 科技

- `content/tech/competitive-intelligence/dubai` — 迪拜 AI 网安竞争格局（竞争情报）
- `content/tech/industry-research/dubai` — 迪拜 AI 网安行业研究
- `content/tech/security/dubai` — AI 安全（红队 / 评估）
- `content/tech/weekly-roundup` — AI 行业趋势周报（安全 × Agent 生态）

## education / international / political / society

四主题均已接入业务线（P1-9，类型 policy-analysis，region 缺省、以 category 段落位）：

- `content/education/education-system` — 教育体系与政策
- `content/international/international-relations` — 国际关系与外交
- `content/political/political-system` — 政治制度与治理
- `content/society/social-structure` — 社会结构与分层

> 四条业务线目前为「已接入、未产出」状态：已有 14 节 `business-config.md`、基线提示词与数据层骨架，报告正文待按各线提示词人工 / Agent 撰写。

## 约定

- 维度顺序：由 `layout.json` 各主题声明（economy 地区优先，其余细分优先）；新增主题 / 业务线须在 `engine/tools/layout.json` 注册。
- 数据不落业务线内：清洗后台账 / 登记 / 量化数据统一入 `data/processed/<theme>/<维度段...>/`（与 content 维度段对齐）。
- 共享机械（模板 / 提示词 / 工具 / 质量 / 审计）一律入 `engine/`，不得复制进业务线。
