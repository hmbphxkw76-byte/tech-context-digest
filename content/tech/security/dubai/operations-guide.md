# 迪拜 AI 网络安全调研 · 操作手册（业务差异）

> **定位**：本文件是 [类型通用运维手册](../../../../engine/templates/employment-research/operations-guide.md) 的**业务实例**，只写本线差异；通用执行步骤、变量表、校验关卡、Agent 约定以通用手册为准。
> **单一事实源**：业务参数以 [prompts/business-config.md](./prompts/business-config.md) 为准。

---

## 0. 本线目录速查

| 资产 | 路径 |
|---|---|
| 四份周期提示词 | `prompts/prompt-{baseline-setup\|monthly-monitor\|quarterly-analysis\|annual-review}.md` |
| 业务参数 | `prompts/business-config.md` |
| 指标登记册（md-table，14 项） | `data/processed/tech/security/dubai/ai_cybersecurity_indicator_registry.md` |
| 报告产物 / 归档 | `reports/` / `reports/archives/` |
| 通用层（只读） | `engine/templates/employment-research/` |

> 与 `content/economy/dubai/apartment` 的结构差异：本线登记册为 **md-table**（非 xlsx），无 `script/` 目录；报告为纯 HTML 交付（canonical 富样式），md 源稿存 `sources/`。

## 1. 启动方式

- **手动启动（当前唯一方式）**：打开对应周期提示词 → 填运行变量 → 提交 AI 执行。
- **定时自动启动（未注册）**：本线尚未注册 Schedule；如需注册参考 `content/economy/dubai/apartment` 三任务节拍（北京时区），注册后同步本手册与 `automation-status.json`。

## 2. 各节拍本线要点

### 2.1 基线（一次性，永不重跑）

- 已产出：`sources/2026-11_baseline_report.md` v1.0 + 登记册（2026-11-11）。
- 仅灾难恢复或经批准的九节结构变更允许重建。
- 采集全英文一手来源；每个数字附 `[Source: URL, 年份]`；九节固定结构逐字固化于 business-config 第八节。

### 2.2 月度（核验型轻运行）

- 读登记册与基线，继承 business-config 第七节已修正事实清单（当前 6 条）。
- 按 14 项追踪表逐项核验；变动项回写「当前值 / 最近核实」，未变动项注明「截至 {{CURRENT_DATE}} 无更新」。
- 对照 7 条触发器（见 business-config 第五节）；命中即升级季度更新，未命中即结束。
- 与上期同日或仅隔 1 日：登记册写明「T+1 刷新，官方发布窗口未开，价值在于核验与口径澄清」。

### 2.3 季度（主更新，九节全模块刷新）

- 启动 4–6 个并行研究子代理（市场政策+企业生态 / 人才供需+薪酬交叉验证 / 岗位技能 / 证书路线+本地考点 / 落地签证），全部限定英文源、逐点引用。
- 薪酬交叉验证：≥3 家薪酬指南最新年版网安分表 + 招聘平台抽样；冲突数据保留双份引用，不静默择一。
- 运行前读 14 项「上次值」，运行后逐项回写「是否更新」；产出数据变更摘要（覆盖 14 项）+ 待复核清单。
- 分析对象 = 自然季度；版本号写入报告内，**不进文件名**。

### 2.4 年度（复盘 + 登记册换代）

- 预测对照：偏离度 =（实际 ÷ 对照）− 1；**|偏离| > 30% 必须重设假设并列出三项假设**，不做事后拟合。
- 清单年度复审；证书路线图与落地路径重排。
- 登记册「复制 → 修订 → 另存」（严禁覆盖历史值）；**命名铁律：报告用复盘年、登记册用生效年**。

## 3. 本线特有排查项

| 现象 | 处置 |
|---|---|
| 薪酬指南新年版未发布（Hays / Robert Half / Cooper Fitch） | 用招聘平台抽样并标注「抽样」；已有年版仍有效时不重复引用旧数字 |
| 仅中文源可得的数值 | 标「未找到英文权威来源，已剔除」，列入待复核清单 |
| MENA 支出与阿联酋市场收入口径冲突 | 并列呈现，不直接比较（Gartner 终端支出 ≠ Mordor/GMI 含服务总收入） |

其余通用异常（validate/lint/classify/build_hub 退出码、基线缺失、登记册被覆盖等）见 [类型通用运维手册第 6 节](../../../../engine/templates/employment-research/operations-guide.md)。

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 重构 | 通用流程下沉至类型通用层；本文件瘦身为业务差异（节拍要点 + 特有排查项） |
