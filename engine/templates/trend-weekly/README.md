# 行业趋势周报型（trend-weekly）· 通用接入与使用指南

> **定位**：`engine/templates/trend-weekly/` 类型的**通用接入指南**（唯一源）。各业务线的 `README.md` 只保留业务身份与差异，不再复制本指南。
> **类型继承体系（四层）**：业务提示词 = [通用基座](../prompt-generic-base.md) × [监测报告通用规范](../monitoring-common-spec.md) × [trend-weekly 类型模板](./) × 业务专属配置（`{业务线}/prompts/business-config.md`）。冲突优先级：业务提示词 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、类型能力概览

| 项 | 内容 |
|---|---|
| 节拍 | 周报主节拍（数据截止日命名）+ 事件触发板块升级 |
| 报告结构 | 由 business-config 主题矩阵定义板块数与顺序；通用骨架见 [周期类型模板](./prompt-weekly-monitor-template.md) |
| 交付 | 富样式自包含 HTML 为主交付物（`reports/{YYYY-MM-DD}_weekly.html`）；md 源稿存 `sources/`，不参与 md2html 自动转换 |
| 登记载体 | 指标台账（`data/{{REGISTRY_FILE}}`），运行前读 → 核验 → 运行后回写 |
| 合规 | 结构骨架 / 必填字段 / 内容格式由 [compliance-rules.json](../compliance-rules.json) 按类型校验 |

## 二、通用文件清单

| 文件 | 用途 |
|---|---|
| `prompt-baseline-setup-template.md` | 基线期机制文档类型模板 |
| `prompt-weekly-monitor-template.md` | 运行期周报类型模板（更新协议 / 模块要点 / 质量自检） |
| `operations-guide.md` | **通用运维手册**（生命周期 / 校验 / 异常排查 / Agent 约定） |
| `README.md` | 本文件：通用接入与使用指南 |

泛用版业务提示词（建业务线时整目录复制填值）见 [engine/prompts/trend-weekly/](../../prompts/trend-weekly/)：`prompt-baseline-setup.md` + `prompt-weekly-monitor.md`。

## 三、新建同类业务线（复制 → 填值 → 运行）

1. **复制泛用提示词**：把 [prompts/](../../prompts/trend-weekly/) 整目录复制到新业务线 `prompts/`（含 `prompt-baseline-setup.md` + `prompt-weekly-monitor.md`）。
2. **填值**：替换 `{{REGION}}` / `{{TOPIC}}` 与全部 TODO；撰写 `business-config.md`（变量固定值 / 来源优先级实例化 / 触发器 / 指标追踪表 / 已修正事实清单 / 固化锚）。
3. **首期运行**：以首期周报为结构锚（或跑基线提示词建台账与机制文档）；随后每周跑周报提示词。
4. **登记**：业务线注册到 [template-registry.md](../template-registry.md) 第二节「已接入业务线」。
5. **写业务差异文档**：新业务线的 `README.md` / `operations-guide.md` 只写业务身份与差异，通用流程指向本目录。

## 四、生成一期新周报

**方式 A：手动（推荐首次）**

1. 打开业务线 `prompts/prompt-weekly-monitor.md`，填写顶部运行变量（`{{CURRENT_DATE}}` / `{{DATA_CUTOFF}}` / `{{PREVIOUS_REPORT_PATH}}` / `{{REPORT_VERSION}}`）。
2. 整份提示词提交给 AI 执行；产出落盘 `reports/{{DATA_CUTOFF}}_weekly.html`。

**方式 B：交给 Agent 整体执行**

将业务线 `operations-guide.md` 全文交给 Agent，并附加一句：「按 operations-guide.md 执行 YYYY-MM-DD 期周报，数据截止 YYYY-MM-DD」。

**方式 C：定时自动**

以 `repository_dispatch: content-update-requested`（payload：`project=<业务线路径>`）或 Schedule 周任务触发。

**本期产物三件套**：周报 HTML（`reports/`）+ md 源稿（`sources/`）+ 台账增量（`data/`）。

## 五、质量与校验入口

- 通用运维手册：[operations-guide.md](./operations-guide.md)
- 全局索引：仓库根 `INDEX.md` / `index.html`（`build_index.py` + `build_hub.py` 自动维护）
- CI 关卡：`validate.py` → `lint_reports.py` → `compliance_check.py` → `classify_reports.py`（全类型同一条流水线，无业务线特例）

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 从三条 trend-weekly 业务线的 README 中抽离通用接入指南，作为类型通用层唯一源 |
