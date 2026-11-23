# Tech Life Research

经济 · 科技 · 教育 · 国际 · 政治 · 社会 研究报告仓库。以三层架构（内容 / 引擎 / 资产）组织可复用、可校验、可自动发布的研究报告体系。

- **内容层 `content/`**：六主题（`economy` / `tech` / `education` / `international` / `political` / `society`），业务线位于 `content/<theme>/<维度段...>/`；维度顺序按主题声明（`economy` 为 `<region>/<category>`，`tech` 为 `<category>/<subcategory>/<region>`，其余主题为 `<category>/<region>`）。`region` 为可选维度（`layout.json` 各主题以 `optional_dimensions` 声明），省略时直接以 category（+subcategory）段落位（如 `content/economy/trends`、`content/tech/ai-application/trends`）。`tech` 下以 `ai-security` / `ai-application` 两个分组目录归并 AI 安全 / AI 应用业务线。
- **引擎层 `engine/`**：跨主题复用的模板、泛用提示词、工具、词库、质量规则、审计与测试。
- **资产层 `data/`**：`raw/` 原始抓取、`processed/<theme>/<维度段...>/` 清洗后数据、`assets/` 图片图表。

> 维度硬性规则：维度先后由 `engine/tools/layout.json` 各主题声明（`economy` 地区优先，`tech` 为 AI 安全 / AI 应用 → 业务线 → 地区，其余主题细分优先），不得在未改 `layout.json` 的情况下倒置；`region` 是否可选由主题 `optional_dimensions` 声明。

## 主题与业务线

六个主题：`economy`（经济）/ `tech`（科技）/ `education`（教育）/ `international`（国际）/ `political`（政治）/ `society`（社会）。

业务线清单（含维度序）、报告类型与最新一期由枢纽页自动汇总，此处不复述，避免手工维护漂移：

- 枢纽页 [index.html](index.html)：主题 / 业务线 / 报告 / 类型四项统计 + 筛选
- 全局索引 [INDEX.md](INDEX.md)：自动生成，逐业务线逐报告

## 快速开始

```bash
# 结构 / 链接 / 页面规范校验
python engine/tools/validate_layout.py
python engine/tools/check_links.py
python engine/tools/page_build_check.py

# 统一优化门禁（P0/P1/P2 全部确定性检查）
python engine/tools/optimization_gate.py --gate-period auto --source-gate-period auto --probe

# 单元测试
python -m unittest discover -s engine/tests -v

# 生成报告枢纽与索引
python engine/tools/build_index.py
python engine/tools/build_hub.py
```

## 文档

- 仓库级硬性约束：[AGENTS.md](AGENTS.md)
- 目录结构与命名规范：[engine/docs/structure-and-naming-spec.md](engine/docs/structure-and-naming-spec.md)
- 体系与规范：[engine/docs/](engine/docs/)
- 通用基座与类型模板：[engine/templates/](engine/templates/)
- 泛用提示词：[engine/prompts/](engine/prompts/)
- 受控词表：[engine/vocabulary/INDEX.md](engine/vocabulary/INDEX.md)
- 审计产出：[engine/report-audits/](engine/report-audits/)

## 自动化

GitHub Actions 工作流（`ci.yml` / `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml` / `audit.yml`）覆盖校验、生成、审计与维护；多会话协作见 [engine/docs/multi-session-git-protocol.md](engine/docs/multi-session-git-protocol.md)。

## 变更记录

见 [CHANGELOG.md](CHANGELOG.md)。
