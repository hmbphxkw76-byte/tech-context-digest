# 职业就业调研型（employment-research）· 通用接入与使用指南

> **定位**：`engine/templates/employment-research/` 类型的**通用接入指南**（唯一源）。各业务线的 `README.md` 只保留业务身份与差异。
> **类型继承体系（四层）**：业务提示词 = [通用基座](../prompt-generic-base.md) × [监测报告通用规范](../monitoring-common-spec.md) × [employment-research 类型模板](./) × 业务专属配置（`{业务线}/prompts/business-config.md`）。冲突优先级：业务提示词 ＞ 类型模板 ＞ 通用基座 ＞ 通用规范。

---

## 一、类型能力概览

| 项 | 内容 |
|---|---|
| 节拍 | 季度主节拍 + 事件触发；月度核验轻运行；年度复盘 |
| 报告结构 | 基线九节骨架；周期报告逐字继承（见 business-config 固化锚） |
| 交付 | md 源稿 + 同目录自包含 HTML（`md2html.py` 同步）；双格式交付 |
| 登记载体 | 指标登记册（格式与路径见 business-config `{{REGISTRY_PATH}}`），运行前读 → 核验 → 运行后回写 |
| 合规 | 结构骨架 / 必填字段 / 内容格式由 [compliance-rules.json](../compliance-rules.json) 按类型校验 |

## 二、通用文件清单

| 文件 | 用途 |
|---|---|
| `prompt-baseline-setup-template.md` | 基线报告类型模板（九节骨架 + 基线差异项） |
| `prompt-update-template.md` | 周期更新类型模板（三档节拍 + 更新协议 + 模块要点框架） |
| `operations-guide.md` | **通用运维手册**（生命周期 / 校验 / 异常排查 / Agent 约定） |
| `README.md` | 本文件：通用接入与使用指南 |

## 三、新建同类业务线（复制 → 填值 → 运行）

1. **复制业务提示词**：参考 [engine/prompts/trend-weekly/](../../prompts/trend-weekly/) 泛用版模式，为本类型建立基线 + 三档周期提示词，头部继承声明指向 `./`。
2. **填值**：替换运行变量与 TODO；撰写 `business-config.md`（变量固定值 / 来源优先级实例化 / 触发器 / 指标追踪表 / 已修正事实清单 / 固化锚）。
3. **首期运行**：跑基线提示词建立登记册与基线锚。
4. **登记**：业务线注册到 [template-registry.md](../template-registry.md) 第二节「已接入业务线」。
5. **写业务差异文档**：新业务线的 `README.md` / `operations-guide.md` 只写业务身份与差异，通用流程指向本目录。

## 四、运行入口

| 节拍 | 入口 | 定位 |
|---|---|---|
| 基线 | `prompts/prompt-baseline-setup.md` | 机制建立，一次性，永不重跑 |
| 月度 | `prompts/prompt-monthly-monitor.md` | 核验型轻运行，无触发不启动新报告 |
| 季度 | `prompts/prompt-quarterly-analysis.md` | 主更新节拍，全模块刷新 |
| 年度 | `prompts/prompt-annual-review.md` | 复盘：预测对照 + 清单复审 + 路线图重排 |

通用执行步骤、变量与校验见 [operations-guide.md](./operations-guide.md)。

## 五、质量与校验入口

- 通用运维手册：[operations-guide.md](./operations-guide.md)
- 全局索引：仓库根 `INDEX.md` / `index.html`（`build_index.py` + `build_hub.py` 自动维护）
- CI 关卡：`validate.py` → `lint_reports.py` → `compliance_check.py` → `classify_reports.py`

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 从 employment-research 业务线文档中抽离通用接入指南，作为类型通用层唯一源 |
