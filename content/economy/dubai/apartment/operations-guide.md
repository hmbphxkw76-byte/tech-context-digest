# 迪拜公寓监测 · 四类报告启动操作指引（Agent 可执行版）

> **适用范围**：`content/economy/dubai/apartment` 业务线的基线 / 月度 / 季度 / 年度四类报告。
> **使用方式**：本指引可由人类逐步照做，也可整体交给 AI Agent 执行。Agent 执行时须遵守文末「Agent 执行约定」。
> **单一事实源**：业务参数一律以 [prompts/business-config.md](./prompts/business-config.md) 为准，本指引不复制阈值与来源清单，只给路径。

---

## 0. 通用约定（四类报告共用）

### 0.1 目录速查

| 资产 | 路径 |
|---|---|
| 四份周期提示词（启动入口） | `content/economy/dubai/apartment/prompts/prompt-{baseline-setup|monthly-monitor|quarterly-analysis|annual-review}.md` |
| 业务参数（固定变量、阈值、触发器） | `content/economy/dubai/apartment/prompts/business-config.md` |
| 指标台账 | `data/processed/economy/dubai/apartment/dubai_apartment_indicator_registry_*.xlsx` |
| 报告产物 | `content/economy/dubai/apartment/reports/` |
| 报告归档 | `content/economy/dubai/apartment/reports/archives/` |
| 工具链 | `engine/tools/`（11 个脚本，退出码：0 过 / 1 错 / 2 警告） |
| 通用层（只读，不改） | `engine/templates/` |

### 0.2 两种启动方式

- **手动启动（推荐首次使用）**：打开对应周期提示词 → 填写「运行变量」区块 → 将整份提示词提交给 AI 执行。
- **定时自动启动**：已注册 3 个自动化任务（北京时区）：月度每月 5 日 09:00、季度 1/4/7/10 月 8 日 09:00、年度 1 月 15 日 09:00。自动任务无需人工填变量，由 Agent 自行读取提示词与台账完成。

### 0.3 通用前置检查（每次启动前必做，约 1 分钟）

依次执行，任何一步退出码为 1 即停止并排查（见第 6 节）：

```powershell
# 在仓库根目录 d:\文档\GitHub\tech-context-digest 下执行
python engine/tools/validate.py          # 结构与命名校验，期望：通过
python engine/tools/classify_reports.py  # 报告归位检查，期望：无错位报告
python engine/tools/build_hub.py --check # 汇总页时效，期望：均为最新；过期则先运行 build_hub.py
```

并人工确认三点：

1. 基线报告 `reports/2026-11_baseline_report.html` 存在（月/季/年的对比锚，缺失则**不得启动周期报告**，先走第 6.4 节）。
2. 上期同类型报告存在（首期除外），路径记入运行变量 `{{PREVIOUS_REPORT_PATH}}`。
3. 对应周期提示词存在且版本号 ≥ v1.1（继承声明指向 `engine/templates/`）。

---

## 1. 基线报告（首期机制建立，一次性）

### 1.1 启动入口与前置条件

- 入口：[prompt-baseline-setup.md](./prompts/prompt-baseline-setup.md)
- **重要**：本业务线基线已产出（`reports/2026-11_baseline_report.html` v1.0 + 台账 2026-11）。**正常运行永不重跑基线**。仅以下两种情形允许再次启动：
  - 台账与报告全部丢失（灾难恢复）；
  - 报告 10 节结构发生经维护规范批准的变更（走 prompt-baseline-setup.md 第十一节流程）。
- 前置条件：无上期报告依赖；须完成来源清单与官方发布节奏调研；确认 `{{REGISTRY_PATH}}` 指向的台账不存在或已获准重建。

### 1.2 运行变量（必填）

| 变量 | 填写规则 | 示例 |
|---|---|---|
| `{{CURRENT_DATE}}` | 本次执行日期 | `2026-11-13` |
| `{{CADENCE}}` | 固定填 `月`（基线不区分节拍） | `月` |
| `{{OUTPUT_PATH}}` | 固定 `reports/2026-11_baseline_report.html` | 同左 |
| `{{REPORT_VERSION}}` | 固定 `v1.0`；灾难恢复重建时按业务配置版本记录递增 | `v1.0` |

### 1.3 执行步骤

1. 填写提示词顶部运行变量。
2. 完成发布日历判定（提示词第六节）：核对 CBUAE 公报、FOMC 纪要、EIA STEO、DET 旅游四个官方页面，列出「应发布但未发布」清单及页面依据。
3. 按四维体系（提示词第四节）采集官方英文来源读数；每个数字记录「机构·统计周期·发布日期·核验状态」。
4. 撰写 10 节固定结构报告（顺序、标题逐字固化，不得增删改）。
5. 首建指标台账（7 个工作表：看板 / 指标台账 / 官方来源清单 / 监测日历 / 信号规则 / 首期基线值 / 使用说明）。
6. 回填追踪表 12 项「是否更新」列；空清单补记「已修正事实清单」（首期为空）。
7. 落盘 `{{OUTPUT_PATH}}`，将业务配置第一节 `{{BASELINE_REPORT_PATH}}` 指向新报告。

### 1.4 结果验证

```powershell
python engine/tools/lint_reports.py    # 0 错误（警告不阻断）
node --check 校验报告内联 JS（或由 Agent 完成语法检查）
```

人工核对：10 节标题与既有基线逐字一致（重建场景）；全篇无中文来源；基线导航为简化锚点（非 `.report-nav`）。

---

## 2. 月度报告（主周期，最高频）

### 2.1 启动入口与前置条件

- 入口：[prompt-monthly-monitor.md](./prompts/prompt-monthly-monitor.md)
- 前置条件：通用前置检查通过；确定本期性质（见 2.4）；检查业务配置第七节「月度」触发器是否命中（CBUAE 利率决议 / FOMC / EIA STEO / DLD 月度数据 / CBUAE 公报 / DET 旅游稿件）。**无触发 → 降级为核验/收敛型轻运行，不得虚构变化。**
- 附加检查（仅当命中利率专题）：3M EIBOR 距 K01 红线 ≤25bp 或单月上行 ≥20bp → 本期必须启用第八节专题预警六件套。

### 2.2 运行变量（必填）

| 变量 | 填写规则 | 示例（2026 年 12 月期） |
|---|---|---|
| `{{CURRENT_DATE}}` | 本次执行日期 | `2026-12-05` |
| `{{PREVIOUS_REPORT_PATH}}` | `reports/` 中最近一期月度简报 | `reports/2026-11_monthly.html` |
| `{{OUTPUT_PATH}}` | `reports/{{YYYY-MM}}_monthly.html`，月份＝数据所属月 | `reports/2026-12_monthly.html` |
| `{{REPORT_VERSION}}` | `v` + 执行日期 | `v2026.12.05` |

固定值（不填，读自业务配置第一节）：`{{REGISTRY_PATH}}`、`{{BASELINE_REPORT_PATH}}`、`{{REPO_RAW_URL_BASE}}` 等。

### 2.3 执行步骤

1. 填变量 → 读 `{{PREVIOUS_REPORT_PATH}}` 与基线报告，提取「已修正事实清单」全部条目（防回退）。
2. 发布日历判定（T+0 / T+1 / 空窗）：核对 CBUAE 公报最新期、FOMC Minutes 链接、EIA STEO Release Date、DET 稿件日期。
3. 运行前从台账「指标台账」「信号规则」「首期基线值」表读上次值，填入追踪表。
4. 按五组指标（融资 / 货币信用 / 价格 / 成交租赁 / 宏观外需）采集英文一手数据。
5. 撰写 9 节报告；信号判定执行「连续 2 期同向 + 排除失真信号 + 多指数互证」。
6. 至少 4 张 ECharts（利率路径 / 租金结构 / 价格口径对照 / 利率敏感性）；顶部导航 9 锚点。
7. 运行后将变动回写台账，逐项填写「是否更新」。
8. 落盘 `{{OUTPUT_PATH}}`。

### 2.4 时间范围与数据范围规则

- **报告月份 = 数据所属月**（非执行月）。文件名 `2026-12_monthly.html` 覆盖 2026 年 12 月发布窗口内可取得的最新数据。
- T+1 判定：本期与上期发布窗口同日或仅隔 1 日 → 报告明确标注「T+1 刷新」，价值在核验、口径澄清与阈值距离，不制造变化。
- 时效取舍：最新官方页 ＞ 上期值 ＞ 预测值；同一指标多版本并存以官方最新发布为准。

### 2.5 结果验证

```powershell
python engine/tools/lint_reports.py       # 表格列宽、URL 规范
python engine/tools/classify_reports.py   # 文件名可识别归位
python engine/tools/build_index.py && python engine/tools/build_hub.py  # 刷新索引与汇总页
```

人工核对：9 锚点全部跳转准确；表格内无「完整 URL」列（链接在弹层/行内）；8 张数字卡与第 3 节数值一致。

---

## 3. 季度报告（四维全景研判）

### 3.1 启动入口与前置条件

- 入口：[prompt-quarterly-analysis.md](./prompts/prompt-quarterly-analysis.md)
- 前置条件：通用前置检查通过；确认季度触发器（CBRE / JLL / Knight Frank 季报、CBUAE 季度经济评论、DLD 季度数据等，见业务配置第七节「季度」）；核对机构报告可获取性——CBRE `cbre.ae/insights`、JLL `jll.com/en-ae/insights`、Knight Frank `knightfrank.ae/newsroom/press-release`。
- **若三大家当季报告均未发布**：改用季度最小可替代集（DLD 官方锚 / Savills / C&W Core / Cavendish Maxwell / ValuStrat / PropertyIndex / DXBinteract），结论置信度降为「方向高、幅度中、时点低」并在报告中标注；滞后一期须标「滞后一期」，不得外推。

### 3.2 运行变量（必填）

| 变量 | 填写规则 | 示例 |
|---|---|---|
| `{{CURRENT_DATE}}` | 本次执行日期 | `2027-01-08` |
| `{{QUARTER}}` | 被分析季度，自然季 | `2026-Q4` |
| `{{PREVIOUS_REPORT_PATH}}` | 最近一期季度报告 | `reports/2026-Q3_quarterly.html` |
| `{{OUTPUT_PATH}}` | `reports/{{YYYY-Qn}}_quarterly.html`，季度＝被分析季度 | `reports/2026-Q4_quarterly.html` |
| `{{REPORT_VERSION}}` | `v` + 执行日期 | `v2027.01.08` |

### 3.3 执行步骤

1. 填变量 → 读上期季度报告与基线，继承「已修正事实清单」。
2. 四维必查（价格成交 / 供需管道 / 租赁收益 / 宏观先行），逐机构交叉核验，口径并列（表观均价 ≠ 同质化 ≠ 混合调整 ≠ 中位价，豪宅注明门槛）。
3. 用 DLD 登记做方向校验；能下载则重算，不能则明写「未重算」。
4. 重算先行信号矩阵（8 项）与结构红线 RL-01–RL-09（红线归一化距离）；触发硬红线须启动升级复核并重算情景。
5. 重算供给情景与次年交付区间；更新条件化决策情景。
6. 撰写报告（10–13 张数字卡，至少 7 张图）；落盘。

### 3.4 时间范围与数据范围规则

- **分析对象 = 自然季度**（Q1=1–3 月，Q2=4–6 月，Q3=7–9 月，Q4=10–12 月）。启动时点通常在季末后 1–2 个月，以机构季报发布为准。
- 机构数据滞后于自然季时标「滞后一期」；UAE-wide 口径不得与 Dubai-only 合并；不同豪宅门槛禁止直接比较。
- 年度复核触发：第 4 季度报告须评估是否与年度复盘合并节奏（1 月年度任务承接全年复盘，季度报告只做季度研判）。

### 3.5 结果验证

```powershell
python engine/tools/lint_reports.py && python engine/tools/classify_reports.py
python engine/tools/build_index.py && python engine/tools/build_hub.py
```

人工核对：红线归一化表与 RL 登记簿一致；数字卡 10–13 张；口径并列表齐全；触发升级复核的项有重算记录。

---

## 4. 年度报告（复盘 + 台账换代）

### 4.1 启动入口与前置条件

- 入口：[prompt-annual-review.md](./prompts/prompt-annual-review.md)
- 前置条件：通用前置检查通过；年度触发器确认（CBRE/JLL/KF/Savills 年报、CBUAE 年度评论、UNCTAD WIR、IMF WEO、DET 年度旅游数据、政策变更，见业务配置第七节「年度」）；确认上期最新月度/季度报告路径；确认台账新版年份。
- 政策复核：G01–G05（黄金签证 / LTV / 过户费 / Oqood / RERA 租金规则）逐项打开官方英文条款页；未取得官方页的标「未核验」。

### 4.2 运行变量（必填）

| 变量 | 填写规则 | 示例（复盘 2026 年） |
|---|---|---|
| `{{CURRENT_DATE}}` | 本次执行日期 | `2027-01-15` |
| `{{YEAR}}` | **被复盘的年份** | `2026` |
| `{{NEXT_YEAR}}` | 台账新版生效年份 | `2027` |
| `{{DATA_CUTOFF}}` | 数据截止日；未发布写最近已发布周期 | `2026-12-31` |
| `{{OUTPUT_REGISTRY}}` | `data/processed/economy/dubai/apartment/dubai_apartment_indicator_registry_{{NEXT_YEAR}}-01.xlsx` | `data/processed/economy/dubai/apartment/dubai_apartment_indicator_registry_2027-01.xlsx` |
| `{{PREVIOUS_REPORT_PATH}}` | 最近一期月度或季度报告 | `reports/2026-12_monthly.html` |
| `{{OUTPUT_PATH}}` | `reports/{{YEAR}}_annual.html` | `reports/2026_annual.html` |
| `{{REPORT_VERSION}}` | `v` + 执行日期 | `v2027.01.15` |

**命名铁律**：报告用被复盘年份，台账用生效年份（2026 复盘 → `2026_annual.html` + `registry_2027-01.xlsx`）。

### 4.3 执行步骤

1. 填变量 → 读上期报告与基线，继承「已修正事实清单」。
2. 全年复盘七项（价格 / 成交量金额 / 期房现房结构 / 交付兑现率 / 新推盘 / 租金收益率 / 分区表现）。
3. 预测 vs 实际偏离检验：偏离度 =（实际 ÷ 对照）− 1，**绝对值 >30% 必须重设假设并列出重设的三项假设**，不做事后拟合。
4. 重置长期基线（人口 / FDI / GDP-CPI / 利率 / 兑现率）；校准 K01–K15（回测 15 条规则，阈值变更同步 business-config 第五节并记版本）。
5. 政策复核 G01–G05；任一变更 → 立即重算需求情景。
6. 生成新版台账（9 个工作表，较基线版新增：预警红线 / 年度基线{{NEXT_YEAR}}）；说明全部变更。
7. 撰写报告（8 张数字卡、2–3 张配套图、未核验清单 ≥8 项）；落盘报告 + 新版台账。

### 4.4 时间范围与数据范围规则

- **复盘对象 = `{{YEAR}}` 全年**；数据截止 `{{DATA_CUTOFF}}`，未发布的年度值写最近已发布周期并标注。
- 台账切换：新版台账生效后，月/季报告的 `{{REGISTRY_PATH}}` 语义切换到新版（业务配置第一节更新），旧版台账保留不删。
- 年度阈值校准结果必须回写 business-config.md 第五节并在版本记录表登记，硬红线变更不得事后改写。

### 4.5 结果验证

```powershell
python engine/tools/lint_reports.py && python engine/tools/classify_reports.py
python engine/tools/build_index.py && python engine/tools/build_hub.py
python -c "import openpyxl; wb=openpyxl.load_workbook(r'data/processed/economy/dubai/apartment/<新版台账>.xlsx', read_only=True); print([ws.title for ws in wb.worksheets])"
```

人工核对：新版台账 9 表齐全；偏离 >30% 的项均有假设重设记录；未核验清单 ≥8 项；报告 + 台账命名符合「复盘年 / 生效年」铁律。

---

## 5. 全类型通用收尾（每次报告落盘后必做）

1. **校验**：`lint_reports.py`（0 错误）→ `classify_reports.py`（无错位）。
2. **索引刷新**：`python engine/tools/build_index.py` → `python engine/tools/build_hub.py`（否则汇总页过期告警）。
3. **归档**：`python engine/tools/archive_reports.py`（保留策略：月度 12 / 季度 8 / 年度 5 / 基线 3，超限移入 `reports/archives/`）。
4. **提交**：git 提交报告 + 台账 + 索引产物（建议提交信息：`report: {YYYY-MM} 月度监测简报` 等格式）。
5. **浏览器抽查**：打开 HTML，确认导航锚点、图表渲染、数字卡数值与正文一致。

---

## 6. 常见异常排查

| 现象 | 原因 | 处置 |
|---|---|---|
| `validate.py` 退出码 1 | 通用层缺文件 / 业务目录结构缺项 / 提示词命名不合规 | 按 error 行补齐文件或改命名；不得为过检删除通用层内容 |
| `lint_reports.py` 退出码 1 | 报告月份非法、表格规范错误 | 按行修复 HTML |
| lint 大量 `[W]` 警告 | 既有报告表格缺 `class="fixed"` 或 `<th>` 百分比列宽 | 警告不阻断；留待维护窗口统一修复 |
| `build_hub.py --check` 报「汇总页已过期」 | 生成报告后未刷新索引 | 运行 `build_index.py` + `build_hub.py` |
| `classify_reports.py` 报错位 | 报告文件名不符合 `{YYYY-MM}_monthly` 等约定 | 改名后再跑；不要手改工具 |
| 找不到 `{{PREVIOUS_REPORT_PATH}}` | 上期报告被归档或首期 | 到 `reports/archives/` 找；确实没有则按「首期」处理并在报告标注 |
| 官方页面无新数据 | 发布窗口未开（T+1/空窗） | 正常情形：按轻运行写核验型报告；禁止虚构变化 |
| 机构季报未发布 | CBRE/JLL/KF 当季未出 | 用季度最小可替代集，标注置信度降级 |
| 基线报告缺失 | 误删或未恢复 | **停止周期报告**，先走 1.2 基线灾难恢复 |
| 内联 JS 报错 | ECharts 语法错误 | `node --check` 定位；修复后重新落盘 |
| 定时任务未产出 | Schedule 停摆或工作流失败 | 查 automation-status.json 与 GitHub Actions 日志；手动按本指引补跑 |

---

## 7. Agent 执行约定

1. **顺序不可跳**：前置检查 → 填变量 → 日历判定 → 读上期/基线 → 采集 → 写报告 → 回写台账 → 校验 → 收尾。任何前置步骤失败即停，不得带病运行。
2. **单一事实源**：阈值、来源清单、口径从 business-config.md 与台账读取，不得凭记忆填写；模板内严禁预填活值。
3. **防回退**：每次运行必须完整继承「已修正事实清单」；与清单冲突的旧结论不得复活。
4. **不虚构**：无触发器命中时降级轻运行；「没有数据」写成可核验陈述（如「核对公报目录共 38 张表，无该分项」）。
5. **留痕**：所有修正逐条补记清单；台账更新按五类分组（实质修订 / 新增口径记录 / 复核确认 / 未取得维持上期值 / 结论不变）。
6. **边界**：只输出「条件 → 周期判读 → 框架性含义 → 风险提示」，不给买卖价位、杠杆比例、仓位建议；全篇仅英文来源。
