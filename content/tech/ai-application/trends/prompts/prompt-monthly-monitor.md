# 全球 AI 应用竞争格局 · 月度更新提示词（竞争情报监测型 · 主更新节拍）

> **用途**：周期性（每月）刷新《全球 AI 应用竞争格局》，动态获取英文权威数据；重大竞品动作触发器命中时亦走本提示词做对应模块重点更新。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：中文九节报告（canonical 富样式自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM}}_monthly.html`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（竞争情报监测型）](../../../../../engine/templates/competitive-intelligence/prompt-monthly-update-template.md) × [业务专属配置](./business-config.md)。质量规则见通用基座与通用规范；更新协议与模块更新要点框架见周期类型模板；业务变量、来源优先级、竞品清单、信号规则见业务配置；冲突时以本文件为准。

---

## 运行变量（每次运行前填写）

```
{{CURRENT_DATE}}         = 本次执行日期，格式 YYYY-MM-DD
{{PREVIOUS_REPORT_PATH}} = 最近一期月度报告路径（首期更新时为空，仅锚定基线）
{{BASELINE_REPORT_PATH}} = reports/2026-11_baseline_report.html
{{REPORT_VERSION}}       = 本次版本号，格式 vYYYY.MM.DD（写入报告文首/文末，不进入文件名）
{{OUTPUT_PATH}}          = reports/{{YYYY-MM}}_monthly.html
{{REGISTRY_PATH}}        = data/processed/tech/ai-application/trends/ai_application_competition_registry.md
```

**任务目标**：执行「全球 AI 应用竞争格局」的月度更新任务。以英文一手 / 权威来源为依据、以上一期报告与基线为对比锚，完成「核验 → 更新 → 影响提示 → 可靠性」闭环；九节结构与基线逐字一致（见[业务配置第十节](./business-config.md)），产出可直接用于下期对比的报告。

---

## 一、项目专属硬性约束

通用约束自动继承[通用基座第三节](../../../../../engine/templates/prompt-generic-base.md)；来源语言规则、受众定位、术语口径见[业务配置](./business-config.md)第二、三节。本项目额外强制：

1. **来源语言规则**：仅英文（{{SOURCE_LANGUAGE_RULE}}），严禁中文来源；仅中文源数据标注「未找到英文权威来源，已剔除」。
2. **口径并列不合并**：模型能力 / 活跃用户 / 支出份额 / 应用收入分别登记，不互换。
3. **结论边界**：竞品动作只做事实记录与影响提示，不做「必然成功 / 失败」断言；影响提示标「判断 / 推断」。

## 二、来源优先级

见[业务配置](./business-config.md)第四节（① 官方一手 ＞ ② 行业机构 / 第三方研究 ＞ ③ 基准与评测 ＞ ④ 媒体转述）；关键动作须至少 2 家独立来源确认。

## 三、基线锚定

更新时必须**读取 `{{PREVIOUS_REPORT_PATH}}`**（首期更新除外）与 `{{BASELINE_REPORT_PATH}}`，继承九节结构与全部已核实结论，严禁重新引入[业务配置第九节](./business-config.md)已修正事实（产生新修正后逐条追加，每条附 `[Source: URL, 年份]`）。

## 四、各模块更新要点（对应九节）

- **第 3 节 · 竞争格局总览**：更新模型层 / 应用层 / 云与基础设施 / 开源生态分层与格局变化。
- **第 4 节 · 竞品档案**：增量修订受影响玩家档案卡（产品 / 定价 / 动作 / 来源）。
- **第 5 节 · 动态矩阵**：全量刷新动作登记（编号 + 玩家 + 动作 + 日期 + 来源 URL），应用 R1–R6 阈值。
- **第 6 节 · 来源与核验治理**：更新来源时效、冲突登记与待复核清单。
- **第 7 节 · 风险与盲区**：更新风险与盲区，标注「推断」。

## 五、执行方式（建议）

1. 启动 4–6 个并行研究子代理：① 模型层；② 应用层；③ 云与基础设施 + 开源生态；④ 基准与评测。全部限定英文源、逐点引用。
2. 子代理返回后由主代理读取 `{{PREVIOUS_REPORT_PATH}}` 与基线做差异合并。
3. 冲突数据保留双份引用；无法核实项单列「待复核清单」。
4. 产出后执行 `python engine/tools/lint_reports.py` 验证。

## 六、输出格式要求

- 中文报告，九节结构与基线逐字一致；版本号 `{{REPORT_VERSION}}` 写入报告文首/文末。
- 文末标注：`本报告为 {{REPORT_VERSION}} 动态更新版，数据基准 {{CURRENT_DATE}}，来源要求见项目提示词。`

## 七、质量自检

通用自检见[通用基座第九节](../../../../../engine/templates/prompt-generic-base.md)与[周期类型模板第六节](../../../../../engine/templates/competitive-intelligence/prompt-monthly-update-template.md)。本项目额外确认：

- [ ] 九节结构与基线逐字一致，无增删节
- [ ] 全篇零中文来源，URL 均为英文站
- [ ] 动态矩阵全量刷新，动作字段完整
- [ ] 影响提示均标「判断 / 推断」
- [ ] 追踪表逐项核对并回写登记册
- [ ] HTML 通过 lint

## 八、Agent 执行约定

通用约定见[通用基座第八节](../../../../../engine/templates/prompt-generic-base.md)。本项目额外：

- 登记载体 `{{REGISTRY_PATH}}` 默认不改写；若需更新，先备份再增量修订，不得覆盖历史值。
- 不修改用户上传的只读附件；如需引用，先复制到可编辑目录。
- 不得编造任何缺失数据；所有结论可回溯到具体来源行与 URL。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-21 | 初始版本 | 新建 `content/tech/ai-application/trends` 月度更新提示词；四层继承体系指向 `engine/templates/competitive-intelligence/` |
