# {{REGION}} · {{TOPIC}} · 项目论证提示词（可行性与市场进入型 · 泛用版 · 项目制）

> **用途**：项目制论证统一入口——新市场进入、新产品线、新设点等一次性项目（当次项目范围由 {{PROJECT_TYPE}} 指定）；另覆盖项目实施后复盘。泛用版业务提示词：建新业务线时复制本文件至 `{REGION}/{PROPERTY}/prompts/`，替换变量与 TODO 后即可运行。
> **产出**：项目论证件 `{{OUTPUT_PATH}}`（`reports/{{YYYY-MM-DD}}-主题.md`）或复盘件 `reports/{{YYYY-MM-DD}}-主题-复盘.md`（+ 同名 html）。命名不在工具链标准正则内，validate 仅 WARN 不阻断，属预期。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../templates/prompt-generic-base.md) × [监测报告通用规范](../../templates/monitoring-common-spec.md) × [项目论证类型模板（可行性与市场进入型）](../../templates/feasibility-study/prompt-study-template.md) × 业务专属配置（实例化后为 `./business-config.md`；泛用版暂缺，业务项以 TODO 标注）。冲突时以业务提示词（即本文件实例化版）为准。

---

## 运行变量（每次运行前填写）

```
{{REGION}} / {{TOPIC}}    = 固定值，见实例化后的 business-config.md
{{CURRENT_DATE}}          = 本次执行日期，格式 YYYY-MM-DD
{{PROJECT_TYPE}}          = 本次类型（新项目论证 / 项目复盘，TODO：项目名称）
{{BASELINE_REPORT_PATH}}  = reports/{{YYYY-MM}}_baseline_report.md
{{REGISTRY_PATH}}         = data/（TODO）
{{OUTPUT_PATH}}           = 由 {{PROJECT_TYPE}} 决定（见用途）
{{REPORT_VERSION}}        = 本次版本号，格式 vYYYY.MM.DD
```

**任务目标**：按[项目论证类型模板](../../templates/feasibility-study/prompt-study-template.md)项目协议执行「框架复核 → 多维论证 → 打分判定 → Go/No-Go」闭环；评估维度与判定标准复用基线（调整须声明理由）；复盘档完成假设回验与判定标准有效性复核；继承已修正事实清单；运行后回写框架档案。

---

## 一、项目协议要点

1. **读取锚**：读取 `{{BASELINE_REPORT_PATH}}`（评估框架锚）与最近同类项目报告（如有）。
2. **判定纪律**：Go / No-Go / 有条件 Go 必须逐项对照判定标准打分；条件清单与验证时点完整。
3. **引用纪律**：引用本仓报告注明来源与口径；缺口项标「本项目专项调研」。

## 二、各模块要点（业务实例化，TODO 按 {{PROJECT_TYPE}} 展开）

- **市场可行性**（TODO：需求容量、目标客群、竞争强度、进入壁垒）。
- **技术与运营**（TODO：资源可得性、关键依赖、运营假设清单）。
- **财务测算**（TODO：投资额、成本收入假设、回收期 / 内部收益率三情景）。
- **法规合规**（TODO：许可与资质清单、合规路径与时点）。
- **判定**（TODO：逐维度打分、结论、条件清单、实施路线图）。

## 三、追踪表（框架档案联动）

运行前从 `{{REGISTRY_PATH}}` 读框架档案 → 复核维度与标准适用性 → 运行后回写（项目结论、假设命中情况、框架修订留痕）。

## 四、执行方式（建议）

1. 输入收集先行：盘点可引用报告与缺口项，专项调研逐点引用。
2. 主代理读取 `{{BASELINE_REPORT_PATH}}` 对齐评估框架；重大未决项存在时结论降级为「有条件 Go」；无法核实项单列「待复核清单」。

## 五、渲染与交付

- 交付包 = 报告（含判定打分表）+ 假设清单附录；结论与风险清单同时呈现。
- 交付格式：md + 同目录自包含 HTML（`python engine/tools/md2html.py`）；HTML 须通过 `python engine/tools/lint_reports.py`。

---
## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-13 | 初始版本 | 从 business-prompt-scaffold.md 拆出独立泛用版项目论证提示词 |
