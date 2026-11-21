# 全球 AI 应用竞争格局 · 基线报告提示词（竞争情报监测型）

> **用途**：建立《全球 AI 应用竞争格局》监测机制与首份基线报告。可直接复制，替换顶部变量后提交给 AI 执行。
> **产出**：中文九节基线报告（canonical 富样式自包含 HTML），落盘 `{{OUTPUT_PATH}}`（`reports/2026-11_baseline_report.html`）+ 竞品动态登记册（`data/processed/tech/ai-application/trends/ai_application_competition_registry.md`）。
>
> **继承声明（四层体系）**：本文件 = [通用基座](../../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../../engine/templates/monitoring-common-spec.md) × [基线报告类型模板（竞争情报监测型）](../../../../../engine/templates/competitive-intelligence/prompt-baseline-setup-template.md) × [业务专属配置](./business-config.md)。质量规则见通用基座与通用规范；竞争情报监测型骨架见类型模板；业务变量、来源优先级、竞品清单、信号规则见业务配置；冲突时以本文件为准。

---

## 运行变量（运行前填写）

```
{{CURRENT_DATE}}         = 本次运行日期，格式 YYYY-MM-DD
{{OUTPUT_PATH}}          = reports/2026-11_baseline_report.html
{{REGISTRY_PATH}}        = data/processed/tech/ai-application/trends/ai_application_competition_registry.md
{{SOURCE_REGISTRY_PATH}} = data/processed/tech/ai-application/trends/source_registry.json
```

**任务目标**：建立「全球 AI 应用竞争格局」监测机制与首份基线报告。以英文一手 / 权威来源为依据，完成「监测机制设计 → 格局总览 → 竞品档案首建 → 动态矩阵与信号规则 → 来源与核验治理 → 风险与盲区 → 交付与运行方式 → 来源清单」闭环，产出可直接用于后续月度对比的基线。

---

## 一、项目专属硬性约束

通用约束自动继承[通用基座第三节](../../../../../engine/templates/prompt-generic-base.md)；来源语言规则、受众定位、术语口径见[业务配置](./business-config.md)第二、三节。本项目额外强制：

1. **来源语言规则**：仅英文（{{SOURCE_LANGUAGE_RULE}}），严禁中文来源；仅中文源数据标注「未找到英文权威来源，已剔除」。
2. **口径并列不合并**：模型能力 / 活跃用户 / 支出份额 / 应用收入分别登记，不互换。
3. **结论边界**：竞品动作只做事实记录与影响提示，不做「必然成功 / 失败」断言；影响提示标「判断 / 推断」。

## 二、来源优先级

见[业务配置](./business-config.md)第四节（① 官方一手 ＞ ② 行业机构 / 第三方研究 ＞ ③ 基准与评测 ＞ ④ 媒体转述）；关键动作须至少 2 家独立来源确认。

## 三、监测机制设计

- 玩家分层与入选标准见[业务配置](./business-config.md)第五节（模型层 / 应用层 / 云与基础设施 / 开源生态）。
- 追踪表（玩家 × 优先信息渠道 × 更新频率）见[业务配置](./business-config.md)第六节。
- 信号触发器与 R1–R6 阈值见[业务配置](./business-config.md)第七、八节。

## 四、九节结构

九节固定骨架见[基线类型模板第三节](../../../../../engine/templates/competitive-intelligence/prompt-baseline-setup-template.md)；本项目节标题固化锚见[业务配置第十节](./business-config.md)：

1. 执行摘要｜2. 监测机制设计｜3. 竞争格局总览｜4. 竞品档案首建｜5. 动态矩阵与信号规则｜6. 来源与核验治理｜7. 风险与盲区｜8. 交付物与后续运行方式｜9. 参考来源清单

## 五、执行方式（建议）

1. 启动 4–6 个并行研究子代理：① 模型层；② 应用层（编码 / 生产力 / 搜索 / 图像）；③ 云与基础设施 + 开源生态；④ 基准与评测。全部限定英文源、逐点引用。
2. 子代理返回后由主代理合并为九节结构，建立竞品档案卡与动态矩阵。
3. 冲突数据保留双份引用；无法核实项单列「待复核清单」。
4. 产出后执行 `python engine/tools/lint_reports.py` 验证。

## 六、输出格式要求

- 中文报告，九节结构；引用与版本规则遵循通用规范。
- 文末标注：`本报告为基线首建版，数据基准 {{CURRENT_DATE}}，来源要求见项目提示词。`

## 七、质量自检

通用自检见[通用基座第九节](../../../../../engine/templates/prompt-generic-base.md)与[基线类型模板第六节](../../../../../engine/templates/competitive-intelligence/prompt-baseline-setup-template.md)。本项目额外确认：

- [ ] 九节结构完整，无缺节
- [ ] 全篇零中文来源，URL 均为英文站
- [ ] 竞品档案卡字段完整（分层 / 产品 / 动作 / 来源）
- [ ] 动态矩阵含编号 + 玩家 + 动作 + 日期 + 来源 URL
- [ ] 影响提示均标「判断 / 推断」
- [ ] HTML 通过 lint

## 八、Agent 执行约定

通用约定见[通用基座第八节](../../../../../engine/templates/prompt-generic-base.md)。本项目额外：

- 登记载体 `{{REGISTRY_PATH}}` 运行期创建；不得编造缺失数据。
- 不修改用户上传的只读附件；如需引用，先复制到可编辑目录。
- 所有结论可回溯到具体来源行与 URL。

---

## 版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-21 | 初始版本 | 新建 `content/tech/ai-application/trends` 基线提示词；四层继承体系指向 `engine/templates/competitive-intelligence/` |
