# 迪拜（阿联酋） · AI 网安竞争格局 · 月度更新提示词（竞争情报监测型 · 主更新节拍）

> **用途**：周期性（每月）刷新竞争动态矩阵与竞品档案；重大动作触发器命中时亦走本提示词做对应模块重点更新。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：中文九节更新版报告（canonical 富样式自包含 HTML），落盘 `reports/{{YYYY-MM}}_monthly.html`。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../../engine/templates/monitoring-common-spec.md) × [周期更新类型模板（竞争情报监测型）](../../../../../../engine/templates/competitive-intelligence/prompt-monthly-update-template.md) × [业务专属配置](./business-config.md)。冲突时以本文件为准。

---

## 运行变量（每次运行前填写）

固定值（见[业务配置第一节](./business-config.md)）：

```
{{REGION}}               = 迪拜（阿联酋）
{{TOPIC}}                = AI 网安竞争格局
{{REGISTRY_PATH}}        = data/processed/tech/ai-security/competitive-intelligence/dubai/ai_cyber_competition_registry.md
{{REGISTRY_FORMAT}}      = md-table
{{BASELINE_REPORT_PATH}} = reports/2026-12_baseline_report.html
{{FRESHNESS_PRIORITY}}   = 最新官方 / 一手发布 > 上期值 > 第三方研究 > 媒体转述
{{SOURCE_LANGUAGE_RULE}} = 仅英文（严禁中文来源）
{{REPO_RAW_URL_BASE}}    = https://github.com/hmbphxkw76-byte/tech-context-digest/blob/main/content/tech/ai-security/competitive-intelligence/dubai
```

运行时变量：

```
{{CURRENT_DATE}}         = 本次执行日期，格式 YYYY-MM-DD
{{PREVIOUS_REPORT_PATH}} = 最近一期月度报告路径（首期更新时为空，仅锚定基线）
{{OUTPUT_PATH}}          = reports/{{YYYY-MM}}_monthly.html
{{REPORT_VERSION}}       = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：以公开来源为依据、以上一期报告与首期基线为对比锚，完成「采集 → 核验 → 矩阵刷新 → 影响提示」闭环；九节结构与基线逐字一致（逐字继承 `reports/2026-12_baseline_report.html` 的九节固化锚）；继承已修正事实清单；无触发器命中且无新动作时降级为核验轻运行（登记册标注「截至 {{CURRENT_DATE}} 无更新」），不得虚构变化。

---

## 一、各模块更新要点（业务实例化）

- **竞争格局**：份额口径更新（全球企业 LLM API 支出 / 企业 AI 部署支出 / 阿联酋网安市场规模 / MENA 信息安全终端支出 / 全球 AI in cybersecurity 市场规模，五口径并列不合并）、新进入者 / 退出者、格局演变判断复核（标「推断」）。
- **竞品档案**：产品矩阵与版本、定价与促销、渠道与生态合作、组织与关键人事、招聘动向（间接情报）；逐家档案卡增量修订，每格附 `[来源, 日期]`。
- **动态矩阵**：本期动作逐条登记（编号 + 玩家 + 动作 + 日期 + 来源 URL）；信号规则 R1–R6 命中状态。
- **影响提示**：对自身定位的威胁 / 机会，标「判断 / 推断」，与事实分离。

## 二、九节固化锚（逐字继承）

九节结构与[基线提示词](./prompt-baseline-setup.md)逐字一致，节标题逐字继承 `reports/2026-12_baseline_report.html` 的 h2 固化锚：一、执行摘要 ｜ 二、监测机制设计 ｜ 三、竞争格局总览 ｜ 四、竞品档案首建 ｜ 五、动态矩阵与信号规则 ｜ 六、来源与核验治理 ｜ 七、风险与盲区 ｜ 八、交付物与后续运行方式 ｜ 九、参考来源清单。

## 三、更新协议与追踪表回写

更新协议与命名见[周期类型模板第二、四节](../../../../../../engine/templates/competitive-intelligence/prompt-monthly-update-template.md)；追踪表（[业务配置第六节](./business-config.md)）逐项核对回写 `{{REGISTRY_PATH}}`（md-table），未变动项注明「截至 {{CURRENT_DATE}} 无更新」；继承已修正事实清单（[业务配置第九节](./business-config.md)），无来源不得入清单、严禁回退；信号触发器（[业务配置第七节](./business-config.md)）命中即对应模块重点更新，无触发不得虚构变化。

## 四、渲染与交付

渲染交付同[基线提示词](./prompt-baseline-setup.md)第六节：纯 HTML 交付（canonical 富样式自包含），md 源稿可选存档、不参与 `md2html.py` 自动转换；遵循 `engine/docs/page-build-spec.md` 与 `engine/docs/page-build-governance.md`；`python engine/tools/lint_reports.py` 与 `python engine/tools/page_build_check.py` 必须零 `[E]`；命名 `reports/{{YYYY-MM}}_monthly.html`。

## 五、质量自检

通用自检见[通用基座第九节](../../../../../../engine/templates/prompt-generic-base.md)与[周期类型模板第六节](../../../../../../engine/templates/competitive-intelligence/prompt-monthly-update-template.md)。本项目额外确认：

- [ ] 九节结构与基线逐字一致（顺序、编号不变）
- [ ] 已修正事实清单已继承并续写，无回退
- [ ] 档案库逐家核对并回写登记册；prompt 模板无硬编码活值
- [ ] 关键动作多源确认；单源项已标注
- [ ] 数据变更摘要 + 待复核清单已产出
- [ ] HTML 通过 lint 与 page_build_check（零 [E]）

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 依竞争情报监测型脚手架第四节实例化：填入业务配置固定值、模块更新要点、追踪表回写与九节固化锚；纯 HTML 交付 |
