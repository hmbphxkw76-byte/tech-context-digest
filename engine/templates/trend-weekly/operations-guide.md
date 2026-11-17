# 行业趋势周报型（trend-weekly）· 通用运维手册

> **适用范围**：`engine/templates/trend-weekly/` 类型下**全部业务线**的周报（weekly）全生命周期：启动 → 执行 → 校验 → 归档 → 版本管理。
> **定位**：本文件是 trend-weekly 类型的**通用流程唯一源**。各业务线的 `operations-guide.md` 只保留业务差异（变量、主题矩阵、来源分级、触发器、特殊规则），不再复制通用流程；通用流程改动只改本文件。
> **单一事实源**：变量、受众、主题矩阵、来源分级、触发器一律以各业务线 `prompts/business-config.md` 为准；本手册不复制其内容，只给路径。
> **类型与方法论**：行业趋势周报型（trend-weekly），见 [周期更新类型模板](./prompt-weekly-monitor-template.md) 与 [基线类型模板](./prompt-baseline-setup-template.md)。

---

## 0. 目录结构速查（通用）

| 资产 | 路径 |
|---|---|
| 周报提示词（启动入口） | `prompts/prompt-weekly-monitor.md` |
| 基线机制建立提示词（占位，正常永不重跑） | `prompts/prompt-baseline-setup.md` |
| 业务参数（变量、主题矩阵、来源分级、触发器） | `prompts/business-config.md` |
| 指标台账 | `data/{{REGISTRY_FILE}}`（文件名见 business-config `{{REGISTRY_PATH}}`） |
| 报告产物 | `reports/`（命名 `{YYYY-MM-DD}_weekly.html`，日期 = 数据截止日） |
| 报告归档 | `reports/archives/`（weekly 保留 12 期，超限自动移入） |
| md 源稿存档 | `sources/`（同名 `.md`，不参与 md2html 自动转换） |
| 类型通用层（只读，不改） | `engine/templates/trend-weekly/` |
| 业务差异操作手册 | `<业务线>/operations-guide.md`（本文件的业务实例） |

## 1. 启动方式

- **手动启动（推荐）**：打开 `prompts/prompt-weekly-monitor.md` → 填写「运行变量」区块 → 将整份提示词提交给 AI 执行。
- **交给 Agent 整体执行**：将本手册与业务线 `operations-guide.md` 全文交给 Agent，并附加一句：「按 operations-guide.md 执行 YYYY-MM-DD 期周报，数据截止 YYYY-MM-DD」。
- **定时启动（可选）**：以 `repository_dispatch: content-update-requested`（payload 带 `project=<业务线路径>`）或 Schedule 周任务触发；Agent 自行读取提示词与台账完成，无需人工填变量。

## 2. 通用前置检查（每次启动前必做）

在仓库根目录下执行，任何一步退出码为 1 即停止排查（见第 7 节）：

```powershell
python engine/tools/validate.py                        # 结构与命名校验，期望：无 ERROR
python engine/tools/classify_reports.py --check --unknown-warn   # 报告归位，期望：无错位
```

并确认两点：

1. 上期周报存在（首期除外），路径记入运行变量 `{{PREVIOUS_REPORT_PATH}}`；被归档则到 `reports/archives/` 找。
2. 台账存在且「已修正事实清单」可读（缺失 = 灾难恢复，先走第 7 节）。

## 3. 运行变量（必填）

| 变量 | 填写规则 | 示例（首期后第 2 期） |
|---|---|---|
| `{{CURRENT_DATE}}` | 本次执行日期 | `2026-11-20` |
| `{{DATA_CUTOFF}}` | 数据截止日（报告命名与标题锚定此日期） | `2026-11-20` |
| `{{PREVIOUS_REPORT_PATH}}` | 最近一期周报 | `reports/{上期文件名}.html` |
| `{{OUTPUT_PATH}}` | `reports/{{DATA_CUTOFF}}_weekly.html` | `reports/2026-11-20_weekly.html` |
| `{{REPORT_VERSION}}` | `v` + 执行日期 | `v2026.11.20` |

固定值（不填，读自 business-config 第一节）：`{{REGION}}`、`{{TOPIC}}`、`{{CADENCE}}`、`{{BASELINE_REPORT_PATH}}`（首期周报，结构与结论锚）、`{{REGISTRY_PATH}}`、`{{REPO_RAW_URL_BASE}}`、`{{FRESHNESS_PRIORITY}}`、`{{SOURCE_LANGUAGE_RULE}}`。

## 4. 执行步骤（顺序不可跳）

1. 填变量 → 读 `{{PREVIOUS_REPORT_PATH}}` 与 `{{BASELINE_REPORT_PATH}}`（首期周报，结构与结论锚），提取台账「已修正事实清单」全部条目（防回退）。
2. 按 business-config 来源分级采集本周新事实；逐点记录「机构 · 统计周期 · 发布日期 · 核验状态」。
3. 核对 business-config 触发器：命中 → 对应板块当期升级；**无触发且无实质变化 → 降级为核验轻运行，不得虚构变化**；与上期数据截止日仅隔 1 日 → 报告头部标注「T+1 刷新」。
4. 逐块更新主题板块（板块数量与顺序由 business-config 主题矩阵定义，不得增删节、调整顺序）。
5. 数据看板逐行核对：运行前从台账读上次值 → 运行后回写台账，逐项填「是否更新」，未变动项注明「截至 {{CURRENT_DATE}} 无更新」。
6. 撰写周报（顶部导航锚点与节标题逐字一致；`.nav-url` = `{{REPO_RAW_URL_BASE}}` + `/reports/{本期文件名}.html` 并显示完整 URL；表格 `class="fixed"` + 百分比列宽），落盘 `{{OUTPUT_PATH}}`；md 源稿同步存 `sources/`。
7. 回写台账全部工作表（看板追踪表 / 已修正事实清单 / 来源清单 / 触发器登记 / 版本记录）。

## 5. 结果验证与收尾（每次落盘后必做）

```powershell
python engine/tools/lint_reports.py                                # 0 错误（警告不阻断）
python engine/tools/compliance_check.py --file <本期报告路径>        # 结构骨架 + 导航
python engine/tools/classify_reports.py --check --unknown-warn     # 无错位
python engine/tools/build_index.py                                 # 刷新 INDEX.md
python engine/tools/build_hub.py                                   # 刷新 index.html / reader.html
python engine/tools/archive_reports.py                             # weekly 12 期滚动归档
```

人工抽查：打开 HTML 确认导航锚点跳转、表格无竖排塌缩、数据看板数值与台账一致。最后 git 提交。

## 6. 版本管理与质量校验规则

### 6.1 版本管理

| 对象 | 版本规则 |
|---|---|
| 周报 | 文件名即版本（数据截止日唯一标识）；报告内 `{{REPORT_VERSION}}` = v + 执行日期；历史报告不覆盖、不删除 |
| 台账 | 增量修订（追加行 + 版本记录表登记），不覆盖历史值 |
| business-config | 变更须在版本记录登记；主题矩阵与来源分级变更属结构性变更，须同步评估周期提示词 |
| 词汇速览区块 | 由 `engine/vocabulary/script/sync_vocab.py` 自动维护，禁止手工编辑；词条变更走词汇库导入流程 |
| 类型通用层 | `engine/templates/trend-weekly/` 为只读通用层；修改须走 [template-registry.md](../template-registry.md) 变更记录 |

### 6.2 质量校验规则（CI 同口径）

| 关卡 | 工具 | 阻断条件 |
|---|---|---|
| 结构与命名 | `validate.py` | ERROR：通用层缺失、命名违规 |
| 内容 lint | `lint_reports.py` | ERROR：表格标签不配对 |
| 模板合规 | `compliance_check.py` | ERROR：h2 节数 < 骨架、编号不连续、缺顶部导航、缺 title、断头锚点 |
| 归位检查 | `classify_reports.py` | 可自动归位的错位报告 |
| 索引时效 | `build_hub.py --check` | 汇总页过期 |

警告项（不阻断但须在维护窗口清理）：表格缺 `class="fixed"`、≥6 列表未声明列宽、h2 超额（业务固化锚需人工确认）。

## 7. 常见异常排查

| 现象 | 原因 | 处置 |
|---|---|---|
| `validate.py` 退出码 1 | 通用层缺文件 / 命名违规 | 按 error 行补齐；不得为过检删通用层内容 |
| `compliance_check.py` 报「结构不完整」 | 节数少于骨架 | 对照首期周报逐字恢复结构 |
| 报「编号不连续」 | h2 id="sN" 断号或乱序 | 重排 id 为连续序号 |
| 找不到 `{{PREVIOUS_REPORT_PATH}}` | 上期报告被归档 | 到 `reports/archives/` 找；确实没有按「首期」处理并标注 |
| 官方页面无新数据 | 发布窗口未开（T+1/空窗） | 按核验轻运行写报告；禁止虚构变化 |
| md2html 覆盖了手写 HTML | md 源稿误放入 `reports/` | md 源稿只存 `sources/`；被覆盖时从 git 恢复 HTML |
| 「词汇速览」区间被误编辑 | 手工改动标记区间 | 重跑 `python engine/vocabulary/script/sync_vocab.py sync --topic <主题>` 自动整块重写 |
| 定时任务未产出 | Schedule 停摆 | 查 `automation-status.json`；手动按本手册补跑 |

## 8. Agent 执行约定

1. **顺序不可跳**：前置检查 → 填变量 → 触发器判定 → 读上期报告 → 采集 → 写报告 → 回写台账 → 校验 → 收尾。任何前置步骤失败即停，不得带病运行。
2. **单一事实源**：变量、来源清单、主题矩阵从 business-config.md 与台账读取，不得凭记忆填写；模板内严禁预填活值。
3. **防回退**：每次运行必须完整继承「已修正事实清单」；与清单冲突的旧结论不得复活。
4. **不虚构**：无触发且无新数据时降级轻运行；「没有数据」写成可核验陈述。
5. **留痕**：所有修正逐条补记台账清单；报告层补充与台账更新严格区分。
6. **边界**：可执行启示只给「条件 → 判读 → 框架性含义 → 风险提示」，不给选型背书、买卖价位与仓位建议；来源语言规则按 business-config 第一节执行。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 从三条 trend-weekly 业务线的 operations-guide 中抽离通用流程，作为类型通用层唯一源；业务线文档瘦身为业务差异 |
