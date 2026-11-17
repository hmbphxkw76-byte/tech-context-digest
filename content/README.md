# 内容层（content/）

研究报告内容按六主题组织；业务线位于 `content/<theme>/<维度段...>/`，维度顺序由 `engine/tools/layout.json` 声明（economy 为 `<region>/<category>`，其余主题为 `<category>/<region>`），以 `prompts/business-config.md` 为单一事实源，报告落 `reports/`。

## economy — 经济

- `content/economy/global/decision-hub` — 跨研究线决策仪表盘
- `content/economy/global/trends` — 全球经济趋势周报
- `content/economy/dubai/apartment` — 迪拜公寓住宅市场监测

## tech — 科技

- `content/tech/competitive-intelligence/dubai` — 迪拜 AI 网安竞争格局（竞争情报）
- `content/tech/industry-research/dubai` — 迪拜 AI 网安行业研究
- `content/tech/security/dubai` — AI 安全（红队 / 评估）
- `content/tech/trends/global` — AI 行业趋势周报（安全 × Agent 生态）

## education / international / political / society

- 主题已注册，暂未建立子目录（保留扩展位）。

## 约定

- 维度顺序：由 `layout.json` 各主题声明（economy 地区优先，其余细分优先）；新增主题 / 业务线须在 `engine/tools/layout.json` 注册。
- 数据不落业务线内：清洗后台账 / 登记 / 量化数据统一入 `data/processed/<theme>/<维度段...>/`（与 content 维度段对齐）。
- 共享机械（模板 / 提示词 / 工具 / 质量 / 审计）一律入 `engine/`，不得复制进业务线。
