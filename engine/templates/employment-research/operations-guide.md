# 职业就业调研型（employment-research）· 通用运维手册

> **适用范围**：`engine/templates/employment-research/` 类型下**全部业务线**的基线 / 月度 / 季度 / 年度四类报告全生命周期。
> **定位**：本文件是 employment-research 类型的**通用流程唯一源**。各业务线的 `operations-guide.md` 只保留业务差异（变量、来源优先级、触发器、固化锚、特殊规则），不再复制通用流程。
> **单一事实源**：业务参数一律以各业务线 `prompts/business-config.md` 为准；本手册不复制阈值与来源清单，只给路径。
> **类型与方法论**：见 [基线类型模板](./prompt-baseline-setup-template.md) 与 [周期更新类型模板](./prompt-update-template.md)（三档节拍：月核验 / 季主更 / 年复盘）。

---

## 0. 通用约定

### 0.1 目录速查

| 资产 | 路径 |
|---|---|
| 四份周期提示词（启动入口） | `prompts/prompt-{baseline-setup\|monthly-monitor\|quarterly-analysis\|annual-review}.md` |
| 业务参数（固定变量、来源优先级、触发器、已修正事实清单） | `prompts/business-config.md` |
| 指标登记册 | `data/{{REGISTRY_FILE}}`（路径与格式见 business-config `{{REGISTRY_PATH}}`） |
| 报告产物 | `reports/` |
| 报告归档 | `reports/archives/` |
| 工具链 | `engine/tools/`（退出码：0 过 / 1 错 / 2 警告） |
| 类型通用层（只读，不改） | `engine/templates/employment-research/` |
| 业务差异操作手册 | `<业务线>/operations-guide.md` |

### 0.2 两种启动方式

- **手动启动**：打开对应周期提示词 → 填写「运行变量」区块 → 将整份提示词提交给 AI 执行。
- **定时自动启动**：按业务线节拍注册 Schedule 任务；注册后须同步业务线 operations-guide 与 `automation-status.json`。

### 0.3 通用前置检查（每次启动前必做）

依次执行，任何一步退出码为 1 即停止并排查（见第 6 节）：

```powershell
# 在仓库根目录下执行
python engine/tools/validate.py            # 结构与命名校验，期望：通过
python engine/tools/classify_reports.py    # 报告归位检查，期望：无错位报告
python engine/tools/build_hub.py --check   # 汇总页时效，期望：均为最新
```

并人工确认：基线报告存在（季/年的对比锚，缺失则**不得启动周期报告**）；指标登记册存在且齐全；对应周期提示词继承声明指向 `engine/templates/`（四层体系完整）。

---

## 1. 基线报告（首期机制建立，一次性）

- 入口：`prompts/prompt-baseline-setup.md`。基线已产出的业务线**正常运行永不重跑**；仅灾难恢复或经批准的结构变更允许重建。
- 运行变量：`{{CURRENT_DATE}}`、`{{OUTPUT_PATH}}`、`{{REPORT_VERSION}}`（固定 v1.0）。
- 执行：采集一手来源读数（每个数字附 `[Source: URL, 年份]`）→ 撰写固定结构报告 → 首建指标登记册 → 落盘并同步 HTML。
- 验证：`md2html.py` → `lint_reports.py`（0 错误）。

## 2. 月度报告（核验型轻运行，不产出新报告文件）

- 入口：`prompts/prompt-monthly-monitor.md`。
- **核验轻运行**：全部未变动时**不启动新报告**，仅在登记册标注「截至 {{CURRENT_DATE}} 无更新」；命中任一触发器才升级为季度重点更新。不得为制造变化而虚构变化。
- 执行：读登记册与基线 → 逐项核验 → 回写留痕（先备份再增量修订，不覆盖历史值）。
- 与上期同日或仅隔 1 日时，在登记册更新记录中明确写「T+1 刷新，官方发布窗口未开，价值在于核验与口径澄清」。

## 3. 季度报告（主更新节拍，全模块刷新）

- 入口：`prompts/prompt-quarterly-analysis.md`。
- 运行变量：`{{CURRENT_DATE}}`、`{{PREVIOUS_REPORT_PATH}}`、`{{OUTPUT_PATH}} = reports/{{YYYY-Qn}}_quarterly.md`、`{{REPORT_VERSION}}`（写入报告内，不进入文件名）。
- 执行：读上期与基线 → 按调研维度启动并行研究子代理（限定来源语言、逐点引用）→ 核心指标交叉验证（冲突并列，不静默择一）→ 逐项回写登记册 → 产出数据变更摘要与待复核清单 → 撰写固定结构报告。
- 分析对象 = 自然季度（Q1=1–3 月 … Q4=10–12 月）。

## 4. 年度报告（复盘 + 登记册换代）

- 入口：`prompts/prompt-annual-review.md`。
- 运行变量：`{{YEAR}}`（被复盘年份，进入报告文件名）、`{{NEXT_YEAR}}`（登记册新版生效年份）、`{{OUTPUT_REGISTRY}}`。
- **命名铁律**：报告用被复盘年份，登记册用生效年份。
- 执行：预测对照（偏离 >30% 必须重设假设并列出三项假设）→ 清单复审 → 路线图重排 → 登记册年度版**复制 → 修订 → 另存**（严禁覆盖历史值）→ 撰写年度报告。

## 5. 全类型通用收尾（每次报告落盘后必做）

1. **HTML 同步**：`python engine/tools/md2html.py`。
2. **校验**：`lint_reports.py`（0 错误）→ `classify_reports.py`（无错位）。
3. **索引刷新**：`build_index.py` → `build_hub.py`。
4. **归档**：`archive_reports.py`（保留策略：monthly 18 / quarterly 8 / annual 5 / baseline 3；基线常驻顶层不归档）。
5. **提交**：git 提交报告 + 登记册 + 索引产物。
6. **浏览器抽查**：打开 HTML，确认锚点目录、表格渲染与正文数值一致。

## 6. 常见异常排查

| 现象 | 原因 | 处置 |
|---|---|---|
| `validate.py` 退出码 1 | 通用层缺文件 / 业务目录结构缺项 / 提示词命名不合规 | 按 error 行补齐；不得为过检删通用层内容 |
| `lint_reports.py` 退出码 1 | 报告月份非法、表格标签未配对 | 按行修复 HTML |
| `build_hub.py --check` 报「汇总页已过期」 | 生成报告后未刷新索引 | 运行 `build_index.py` + `build_hub.py` |
| `classify_reports.py` 报错位 | 报告文件名不符合命名约定 | 改名后再跑；版本号不得写入文件名 |
| 找不到 `{{PREVIOUS_REPORT_PATH}}` | 上期报告被归档或首期 | 到 `reports/archives/` 找；否则按「首期更新」处理并标注 |
| 官方页面无新数据 | 发布窗口未开（T+1 / 空窗） | 月度降级为登记册核验留痕；禁止虚构变化 |
| 基线报告缺失 | 误删或未恢复 | **停止周期报告**，先走基线灾难恢复 |
| 登记册被整档覆盖 | 运行未遵守「先备份再增量修订」 | 从 git 历史恢复；此后回写一律增量修订 |

## 7. Agent 执行约定

1. **顺序不可跳**：前置检查 → 填变量 → 触发器判定 → 读上期/基线 → 采集（并行子代理）→ 写报告 → 回写登记册 → 校验 → 收尾。
2. **单一事实源**：来源优先级、触发器、口径、已修正事实清单从 business-config.md 与登记册读取，不得凭记忆填写；提示词内严禁预填活值。
3. **防回退**：每次运行必须完整继承「已修正事实清单」；新修正逐条追加且每条附 `[Source: URL, 年份]`，无来源不得入清单。
4. **不虚构**：月度无触发器命中时保持核验轻运行，不产出新报告；「没有数据」写成可核验陈述。
5. **来源语言规则**：按 business-config 第一节执行（如仅英文来源）。
6. **边界**：结论允许框架性建议（标「建议 / 推断」），不承诺结果；所有结论可回溯到具体来源行与 URL。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 从 employment-research 业务线 operations-guide 中抽离通用流程，作为类型通用层唯一源；业务线文档瘦身为业务差异 |
