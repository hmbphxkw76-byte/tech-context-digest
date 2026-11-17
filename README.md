# Tech Life Research

经济 · 科技 · 教育 · 国际 · 政治 · 社会 研究报告仓库。以三层架构（内容 / 引擎 / 资产）组织可复用、可校验、可自动发布的研究报告体系。

- **内容层 `content/`**：六主题（`economy` / `tech` / `education` / `international` / `political` / `society`），业务线位于 `content/<theme>/<维度段...>/`；维度顺序按主题声明（`economy` 为 `<region>/<category>`，其余主题为 `<category>/<region>`）。
- **引擎层 `engine/`**：跨主题复用的模板、泛用提示词、工具、词库、质量规则、审计与测试。
- **资产层 `data/`**：`raw/` 原始抓取、`processed/<theme>/<维度段...>/` 清洗后数据、`assets/` 图片图表。

> 维度硬性规则：维度先后由 `engine/tools/layout.json` 各主题声明（`economy` 地区优先，其余主题细分优先），不得在未改 `layout.json` 的情况下倒置。

## 主题与业务线

| 主题 | 说明 | 业务线（维度序） |
|---|---|---|
| `economy` | 经济 | global · decision-hub、global · trends、dubai · apartment |
| `tech` | 科技 | dubai · competitive-intelligence、dubai · industry-research、dubai · security、global · trends |
| `education` | 教育 | （已注册，待扩展） |
| `international` | 国际 | （已注册，待扩展） |
| `political` | 政治 | （已注册，待扩展） |
| `society` | 社会 | （已注册，待扩展） |

当前 7 条业务线、10 份正式报告、14 个已注册报告类型。

## 快速开始

```bash
# 结构 / 链接 / 页面规范校验
python engine/tools/validate_layout.py
python engine/tools/check_links.py
python engine/tools/page_build_check.py

# 统一优化门禁（P0/P1/P2 全部确定性检查）
python engine/tools/optimization_gate.py --gate-period 2026-12 --source-gate-period 2027-01 --probe

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
