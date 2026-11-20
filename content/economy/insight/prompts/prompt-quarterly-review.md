# 决策仪表盘 · 季度提示词（insight）

> **继承声明**：本提示词 = [通用基座](../../../../engine/templates/prompt-generic-base.md) × [监测报告通用规范](../../../../engine/templates/monitoring-common-spec.md) × [信息分层规范](../../../../engine/templates/information-layering-spec.md) × [决策交付规范](../../../../engine/templates/decision-delivery-spec.md) × [决策仪表盘型模板](../../../../engine/templates/decision-dashboard/prompt-baseline-setup-template.md) × [业务配置](business-config.md)。冲突时以本提示词 ＞ 业务配置 ＞ 类型模板 ＞ 决策交付规范 ＞ 信息分层规范 ＞ 通用基座 ＞ 通用规范。

## 一、任务

按季度（事件触发可插刷）产出跨研究线决策仪表盘：读取各研究线最新报告与 `{{DECISION_CARDS_PATH}}`，收敛决策卡、暴露缺失、触发行动。

## 二、运行变量

```
{{REGION}}               = 跨研究线（全球 / 迪拜）
{{TOPIC}}                = 决策仪表盘
{{CURRENT_DATE}}         = 本次执行日期
{{CADENCE}}              = 季
{{REGISTRY_PATH}}        = data/processed/economy/insight/decision_cards.json
{{DECISION_CARDS_PATH}}  = data/processed/economy/insight/decision_cards.json
{{SLICES_PATH}}          = data/processed/economy/insight/scenario_slices.md
{{PREVIOUS_REPORT_PATH}} = reports/ 最近一期决策仪表盘
{{OUTPUT_PATH}}          = reports/{{YYYY-Qn}}_quarterly.html
{{READING_TIME}}         = 本期读数时点
{{REPORT_VERSION}}       = 仅核心事实修正时升级
{{SOURCE_LANGUAGE_RULE}} = 仅英文（本业务线为综合层，无外部来源）
```

## 三、执行步骤

1. 读取 `{{PREVIOUS_REPORT_PATH}}` 与 `{{DECISION_CARDS_PATH}}`，继承决策卡与口径裁决。
2. 读取各研究线最新报告与 `engine/fact_cards/`，收敛核心判断为决策卡（结论 / 证据强度 / 触发条件 / 反向证据 / 信息充分度）。
3. 暴露缺失事实（信息充分度 = 需补充 X 类信息才可决策），指向盲区台账。
4. 输出 9 节报告（见类型模板第二节）；开头输出新增信息统计模块与读数时点。
5. 行动项按五要素 + 三档优先级；信号灯标注「预校准（ex-ante）」。
6. 回写 `{{DECISION_CARDS_PATH}}` 与 `{{SLICES_PATH}}`。

## 四、自检

- [ ] 9 节齐全；决策卡 / 行动协议 / 场景切片 / ex-ante / 新增信息统计非空
- [ ] 决策摘要仅含已核验 + 部分核验，无「假设乘积」点值
- [ ] 行动协议五要素 + 三档优先级
- [ ] 读数时点与版本处理符合版本治理
- [ ] 渲染符合监测报告通用规范与页面构建规范
