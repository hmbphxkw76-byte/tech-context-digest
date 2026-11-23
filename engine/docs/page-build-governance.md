# 页面构建治理：CI/CD 保障与规范落地机制

> **状态**：现行规范
> **配套规范**：[page-build-spec.md](./page-build-spec.md)（PAGE-BUILD-SPEC v1.0）
> **适用范围**：全部 HTML 页面（hub / 报告 / 未来新主题）的构建、校验、发布与迭代。
> **一句话**：规范定义「应该怎么做」，本文件确保「必须做到」——**流程治理是地图，基础设施治理是护栏**。
> **最后更新**：2026-11-16

---

## 一、目标与职责

| 目标 | 机制 |
|---|---|
| 设计一致 | canonical 令牌 / 组件单一事实源 + 漂移色门禁 |
| 结构一致 | 骨架检查（页头 / 导航 / 容器 / 章节） |
| 质量可控 | 性能预算 / A11y / 兼容性 / 确定性检查 |
| 可回溯 | 生成物与生成器一致（`--check`）、审计报告、状态文件 |
| 防漂移 | 每次 push/PR 校验 + 定时维护审计 + 新主题准入清单 |

| 角色 | 职责 |
|---|---|
| 规范所有者（维护者） | 修订 `page-build-spec.md`、令牌与组件事实源、批准破坏性变更 |
| 业务线作者 | 按规范产出报告页；新主题接入前跑校验并全绿 |
| 生成器（`engine/tools/`） | 生成 canonical 页面，保证确定性；不携带时间戳 |
| CI（GitHub Actions） | 强制校验、阻断不合格合并、自动同步与审计 |
| 定时维护 | 结构补全、归档、索引、审计、活跃度心跳 |

---

## 二、CI/CD 保障体系

### 2.1 流水线地图

```
提交 / PR ──► ci.yml ───────────────► 合并到 main
推送 main ──► html-sync.yml ─────────► 重新生成 HTML + hub 并提交
每月/季度 ──► content-update.yml ────► 任务清单 + 维护流水线 + 状态记录
每周一 ─────► scheduled-maintenance ─► 结构/校验/审计/归档/索引/hub/活跃度
报告变更 ───► audit.yml ─────────────► 审计四环节（fail-fast）
异常 ───────► webhook-alert.yml ─────► 告警
```

### 2.2 各环节执行规则

| 环节 | 工作流 | 触发 | 执行内容 | 阻断 |
|---|---|---|---|---|
| 语法检查 | ci.yml `syntax` | push/PR | `py_compile` 全量 Python | 是 |
| 单元测试 | ci.yml `test` | push/PR | `unittest discover -s engine/tests` | 是 |
| 规范校验 | ci.yml `validate` | push/PR | **统一门禁 `optimization_gate.py --probe`** | `[E]` 阻断 |
| HTML 同步 | html-sync.yml | 报告 / 生成器变更 | `md2html` + `build_hub` + 指纹 → 统一门禁 → `submit-pr` | `[E]` 阻断 |
| 内容更新编排 | content-update.yml | 每月 1 日 / 季首月 / dispatch | 归位 → 维护流水线 → 统一门禁 → 任务清单 Issue → `submit-pr` | `[E]` 阻断 |
| 定时维护 | scheduled-maintenance.yml | 每周一 02:30 UTC | 结构补全 → 归位 → 维护流水线 → 统一门禁 → 合规审计 → 单测 → 性能 → 活跃度 → `submit-pr` | `[E]` 阻断 |
| 审计 | audit.yml | 报告变更 / dispatch | `audit_tool run --strict`（四环节 fail-fast）+ `accept` + `submit-pr` | `[E]` 或超 L3 宽限 |
| 失败告警 | webhook-alert.yml | 上述失败 | 建 Issue / 通知 | — |

> 统一门禁的 33 项清单与两级 gate-period 见 [report-pipeline-system.md](./report-pipeline-system.md) §三、§五。

### 2.3 并发与提交纪律

- 四个自动提交工作流（`html-sync` / `content-update` / `scheduled-maintenance` / `audit`）共用并发组 `auto-commit-main`（`cancel-in-progress: false`），串行推送，避免 push 拒绝与 `INDEX.md` 时间戳冲突。
- 提交与推送分离：先 commit 再重试 push，避免重试丢失 commit。
- 无变更时不提交（`git diff --cached --quiet` 判定）。
- 多会话协作见 [multi-session-git-protocol.md](./multi-session-git-protocol.md)。

---

## 三、校验分级与门禁规则

统一约定（与 `lint_reports.py` / `compliance_check.py` 一致）：

| 级别 | 含义 | 退出码 | 处置 |
|---|---|---|---|
| `[E]` | 错误：违反强制项 | 1 | **阻断**合并 / 定时维护提交；必须修复 |
| `[W]` | 警告：建议项 / 既有遗留 | 2 | 记录不阻断；纳入审计报告跟踪 |

**门禁执行细则**：

- CI 步骤用 `set +e` 取值后判定：`1 → ::error:: + exit 1`；`2 → ::warning:: + exit 0`。
- `page_build_check.py` 同规则；检查项与级别见规范 §九。
- 新增检查项默认为 `[W]`；升级为 `[E]` 需规范所有者批准并同步本文与规范。

---

## 四、规范落地机制

### 4.1 单一事实源

| 内容 | 事实源 | 消费方 |
|---|---|---|
| 报告样式 | `engine/tools/report_style.py::CANONICAL_CSS` | `md2html.py`、`restyle_reports.py` |
| hub 样式 | `engine/tools/build_hub.py::_STYLE` | `build_hub.py`（生成 index/reader） |
| 目录维度 | `engine/tools/layout.json` | `validate_layout.py`、发现/归位/索引 |
| 报告类型 | `engine/templates/template-registry.md`、`compliance-rules.json` | `compliance_check.py` |

**约束**：禁止在页面内维护与事实源平行的样式副本；新增组件先并入 canonical。

### 4.2 迁移机制

- 既有报告：`python engine/tools/restyle_reports.py --files <报告.html> [--rename-chart] [--fix-colors]`。
- md → HTML：`python engine/tools/md2html.py`（输出 canonical 结构）。
- 令牌 / 组件变更：先改事实源 → 迁移存量 → 全量校验 → 更新规范文档。

### 4.3 漂移检测

- **每次 push/PR**：统一门禁中的 `page_build` 检查检测漂移色、私建结构、A11y 缺失。
- **每周定时维护**：`validate` / `lint` / `compliance --audit` / 归档 / 索引 / hub 全量复跑；审计写入 `engine/report-audits/`。
- **生成物一致性**：`build_hub.py --check` 保证 index/reader 与生成器一致，防止手工改动产物。

---

## 五、版本迭代约束

### 5.1 版本号

`PAGE-BUILD-SPEC vX.Y`：

- **补丁（x.Z）**：文案、示例、非强制建议修正——维护者直接改。
- **次版本（X.Y）**：新增检查项 / 组件 / 推荐项——维护者批准，同步事实源与测试。
- **主版本（X.0）**：令牌 / 类名 / 结构等破坏性变更——须走 §5.2 流程。

### 5.2 变更流程

```
提案（Issue / ADR）→ 影响面评估（存量页面 / 生成器 / 校验器）
  → 事实源变更（report_style.py / build_hub.py）→ 同步文档
  → 迁移存量（restyle_reports.py）→ 全量校验（unittest + 各校验器）
  → CI 观察 → 发布
```

### 5.3 破坏性变更的并行期

- 主版本变更提供**迁移工具**与**并行期**（默认一个迭代周期）。
- 并行期内 CI 允许新旧两套（白名单），到期后移除白名单并转 `[E]`。
- 回滚：保留上一版事实源常量（如 `CANONICAL_CSS_V1`）直到并行期结束。

### 5.4 新主题 / 新页面准入

1. 复用 canonical 样式与结构（不得私建）。
2. 本地跑 `page_build_check.py` + `unittest`，全绿。
3. 提交 PR，CI 全绿（含门禁项）。
4. 维护者合并；定时维护首跑生成索引 / hub 条目。

---

## 六、度量、审计与告警

| 机制 | 位置 | 说明 |
|---|---|---|
| 合规审计 | `engine/report-audits/compliance-audit.md` | 历史报告 × 模板匹配度，每周刷新 |
| 状态记录 | `automation-status.json` | 各 phase 结果与运行链接 |
| 性能基线 | `perf-status.json` | 门禁耗时，P95 阈值 |
| 活跃度 | `automation_status.py activity` | >45 天预警，防 60 天停摆 |
| 失败告警 | `webhook-alert.yml` / Issue 标签 | `automation-failure` / `report-compliance` / `automation-warning` |
| 索引心跳 | `INDEX.md`「最近生成」 | 定时维护刷新 |

---

## 七、流程速查表

| 我要做什么 | 执行 |
|---|---|
| 新增报告页 | 复用 canonical → `page_build_check.py` → 提交 PR |
| 迁移旧报告 | `restyle_reports.py --files ... [--rename-chart] [--fix-colors]` |
| md 转 HTML | `md2html.py` |
| 改设计令牌 | 改 `report_style.py` + `build_hub.py` → 迁移 → 更新规范 → 全量校验 |
| 改 hub 页面 | 改 `build_hub.py` → `build_hub.py --check` → 重新生成 |
| 本地全量自检 | `py_compile`（编译）→ `unittest`（测试）→ `python engine/tools/optimization_gate.py --probe`（**全部确定性校验统一入口**，33 项；不再分项调用 `validate.py` / `page_build_check.py` / `lint_reports.py` / `compliance_check.py` / `check_links.py` / `build_hub.py --check`） |
| 排查规范问题 | 先读 `page-build-spec.md` §九 检查项，再定位事实源 |
