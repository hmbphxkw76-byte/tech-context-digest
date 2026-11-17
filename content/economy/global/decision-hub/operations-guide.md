# 决策仪表盘运维手册（decision-hub）

> **类型**：decision-dashboard ｜ **节拍**：季度主更新 + 事件触发插刷 ｜ **读数时点**：2026-11-15 ｜ **版本**：v1.0

## 一、生命周期

1. **收敛**：读取各研究线最新报告与 `engine/fact_cards/`，把核心判断收敛为决策卡（`data/processed/economy/global/decision-hub/decision_cards.json`）。
2. **暴露**：标记缺失事实与冲突读数（信息充分度 = 需补充 X 类信息才可决策）。
3. **触发**：按阈值与缺失清单启动补缺 / 专题任务（行动协议五要素 + 三档优先级）。
4. **产出**：更新 `reports/` 季度报告；核验 / 收敛型运行不新增版本号，只更新「本期读数时点」。

## 二、数据源

- 决策卡台账：`data/processed/economy/global/decision-hub/decision_cards.json`
- 场景切片：`data/processed/economy/global/decision-hub/scenario_slices.md`
- 事实卡片库：`engine/fact_cards/`（三域共享）
- 盲区台账：`engine/report-audits/blind-spot-ledger.md`
- 来源登记：各研究线 `data/processed/<theme>/<维度段...>/source_registry.json`

## 三、校验清单

```bash
python engine/tools/info_density_check.py --file content/economy/global/decision-hub/reports/2026-12_baseline_report.html
python engine/tools/fact_card_check.py
python engine/tools/decision_hub_check.py --file content/economy/global/decision-hub/reports/2026-12_baseline_report.html
python engine/tools/blind_spot_check.py
python engine/tools/compliance_check.py --file content/economy/global/decision-hub/reports/2026-12_baseline_report.html
python engine/tools/page_build_check.py
```

## 四、异常处理

- 决策卡字段缺失 → 不发布，补齐五要素。
- 行动协议缺要素 → 降级为「仅记录存档」或补齐。
- 事实卡片引用不存在 → `fact_card_check` 阻断，先登记卡片。
- 阈值校准未完成（至 2027-06）→ 信号灯一律标「预校准（ex-ante）」。

## 五、版本规则

- 核验 / 收敛型运行：不升级版本号，只更新「本期读数时点」。
- 核心事实修正：升级版本号并在决策卡与来源登记留痕。
