# 冗余 / 无效代码清理报告（2026-11-14）

> **状态**：历史记录（时点报告，留存备查，不修改）
> **范围**：全仓源代码（Python 工具链 / HTML 页面内联 CSS/JS）
> **方法**：AST 静态分析（未用导入 / 未引用模块级定义 / 终止语句后不可达 / 注释代码 / 跨文件同构函数）+ 逐条人工验证 + 分模块清理并逐批跑测试
> **原则**：只删「确定无用」的代码；保留兼容性代码、占位标记与一次性 / 可复用工具

---

## 一、结论速览

| 指标 | 清理前 | 清理后 | 净变化 |
|---|---|---|---|
| Python 行数 | 7,135 | 7,117 | **−18** |
| Python 字节 | 370,494（361.8 KB） | 369,692（361.0 KB） | **−802** |
| 变更文件 | — | 10 | +15 / −35 行 |

清理后复审：**未使用导入 0、未引用模块级定义 0、不可达代码 0、注释掉的代码 0、未引用依赖 0**。

---

## 二、已移除条目（13 项）

| # | 文件 | 条目 | 类型 |
|---|---|---|---|
| 1 | `content/economy/dubai/apartment/script/build_registry_v2.py` | `import os` | 未使用导入 |
| 2–3 | `content/economy/dubai/apartment/script/build_registry_v1.py` | 常量 `KF` / `DXB` | 未引用定义 |
| 4 | `content/economy/dubai/apartment/script/build_registry_v1.py` | 局部 `d_start` | 未使用局部（改名 `_d_start` 保留解包位） |
| 5 | `engine/tools/_common.py` | 常量 `SKIP_TOP` | 重构遗留，全库无引用 |
| 6 | `engine/tools/check_links.py` | 常量 `WORKFLOW_BASE` | 占位常量，从未使用 |
| 7–8 | `check_links.py` / `rewrite_paths.py` | 本地 `LEGACY_ROOTS` + `known_roots()` | 逐字重复 → 上收 `_common.py` |
| 9 | `engine/tools/validate_layout.py` | 局部 `args` | 未使用局部 |
| 10–12 | `engine/tools/compliance_check.py` | 局部 `errors` / `warnings` / `rel` / `inherited` | 未使用局部 |
| 13 | `engine/tools/build_hub.py`（生成 index / reader） | CSS `.footer .muted` | 死样式（两页面均未使用） |

---

## 三、评估后保留的项（附理由）

| 项 | 保留理由 |
|---|---|
| `err` / `warn` 辅助函数重复（`validate.py` / `validate_layout.py`） | 各自闭包收集本模块错误 / 警告；合并需引入 Reporter 并改动大量调用点，耦合成本高于收益 |
| `setUpClass` 重复（`engine/tests/test_tools.py`） | 测试类独立夹具，惯例写法 |
| canonical CSS「未使用类」（各报告内联） | 刻意的设计系统超集：全部报告内联同一份 `CANONICAL_CSS`，单页只用子集；删除会破坏「单一事实源 + 自包含」 |
| `_STYLE` 中 hub 专属类（`.hero`/`.main`/`.stat`/`.stats`） | index / reader 共享样式表，index 使用；非死代码 |
| `build_registry_v1.py` / `v2.py` | 一次性台账生成脚本，是 `data/*.xlsx` 交付物的生产者，可复用于下一年度重置 |
| `rewrite_paths.py` | 目录迁移工具（含两轮映射），文档化且幂等，可复用于未来迁移 |
| 报告内联 echarts 配置 JS | 数据驱动配置，非静态死代码；由 `.chart-eh` 类名门禁约束 |

---

## 四、验证与遗留

- **分模块验证**：每批清理后执行 `py_compile` + `unittest` + 相关校验器，全部通过后进入下一批。
- **终态**：`unittest` 通过；`page_build_check` 0 错误 0 警告；`validate` / `validate_layout` / `compliance_check --check` / `classify_reports --check` / `check_links` / `build_hub --check` 全绿；`lint_reports` 0 错误。
- **既有遗留**：`lint_reports.py` 既有警告（apartment 季 / 年报表格缺 `class="fixed"` 与列宽）——**已于 2026-11-15 由 `restyle_reports.py --fix-tables` 修复**，见 [tech-debt-ledger.md](tech-debt-ledger.md) A 类。
