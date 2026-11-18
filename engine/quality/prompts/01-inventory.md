# 01 · 全量动态盘点（inventory）

> **阶段**：1。**上游**：无。**下游**：`02-evaluate.md`。
>
> **目标**：发现全项目所有评估对象，产出结构化 `inventory`，作为后续所有指标的「分母」。

---

## 一、发现规则

### 1.1 业务线

- 遍历一级主题目录（`layout.json` 的 `themes` 键：`economy` / `political` / `law` / `culture` / `education` / `technology`）下的所有业务目录。
- 业务目录判定：包含 `prompts/` 或 `reports/` 或 `data/` 的叶子目录。
- 校验：目录层级深度与维度数一致；含 `region` 维度的主题 `category` 段先于 `region`（`validate_layout.py` 口径）。
- 记录 `business_lines[]`：相对路径 + 主题名 + 地区 + 类型 ID（从 `business-config.md` 继承声明解析）。

### 1.2 报告

- 各业务线 `reports/` 下全部 `*.html`（含 `archives/`、`legacy/`）；`sources/` 下 `*.md` 作为源稿关联记录。
- 记录 `reports[]`：路径、业务线、周期（baseline / weekly / monthly / quarterly / annual / study / flash_note / target_update / review / topic_study，从文件名或 business-config 解析）。

### 1.3 提示词

- 各业务线 `prompts/*.md`：`business-config.md` + 周期提示词。
- 记录 `prompts[]`：路径、业务线、角色（config / baseline / cycle）。

### 1.4 登记册

- 各业务线 `data/` 下台账文件（xlsx / md / pdf），以 `business-config` 的 `{{REGISTRY_PATH}}` 为准。
- 记录 `registries[]`：路径、格式（xlsx-ledger / md-ledger）。

### 1.5 通用层模板

- `engine/templates/` 根部 3 份共享文件 + 类型子目录（类型 ID 清单见 `template-registry.md` 第二节，须与 `compliance-rules.json` 的 `types` 键一致）。
- 记录 `templates[]`：类型 ID、名称、模板文件清单。

### 1.6 词汇

- `engine/vocabulary/data/<topic>/terms.md`，主题清单见 `config/topics.json`。
- 记录 `vocab_terms[]`：主题 ID、词条数、版本。

---

## 二、产出格式

写入 `quality-manifest.json` 的 `inventory` 段，字段见 `../manifest.schema.json`。

```json
{
  "inventory": {
    "reports": [
      { "path": "content/economy/dubai/apartment/reports/2026-11_monthly.html", "type": "report", "cycle": "monthly", "business_line": "content/economy/dubai/apartment" }
    ],
    "prompts": [
      { "path": "content/economy/dubai/apartment/prompts/business-config.md", "type": "prompt", "business_line": "content/economy/dubai/apartment" }
    ],
    "registries": [
      { "path": "data/processed/economy/dubai/apartment/dubai_apartment_indicator_registry_2027-01.xlsx", "type": "registry", "business_line": "content/economy/dubai/apartment" }
    ],
    "vocab_terms": [
      { "path": "engine/vocabulary/data/economy/terms.md", "type": "vocab", "business_line": "engine/vocabulary" }
    ]
  }
}
```

---

## 三、校验

- 盘点完成后，立即核对：
  - `layout.json` 的 `themes` 均有对应目录（缺失报 INFO，不阻断）；
  - 每个业务线具备 `prompts/business-config.md`（缺失计入 C-03）；
  - 类型 ID 清单与 `template-registry.md` 第二节一致（不一致计入 C11）。
- 输出对象计数汇总（业务线 / 报告 / 提示词 / 登记册 / 模板 / 词汇词条）。

---

## 四、注意

- 盘点**只读**，不修改任何文件。
- 新增业务线 / 报告 / 词条由本阶段自动发现，无需改动本提示词。
