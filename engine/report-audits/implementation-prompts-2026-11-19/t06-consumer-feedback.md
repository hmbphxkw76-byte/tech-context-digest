# T-06 · 消费端反馈机制

> 方案条目：[优化解决方案与实施清单 v2.0](../optimization-solution-and-implementation-checklist-2026-11-19.md) §4.6 T-06｜优先级 P2｜性质：设计 + 工具
> 通用协议：见 [index.md](index.md) §2–§3

## 目标
接通情报周期的最后一环：为报告与 hub 增加**消费端反馈入口**，并把消费侧指标纳入 IGI 设计。

## 背景（已核验）
- 现有质量指标全部是**生产侧**（`acceptance.md`：登记覆盖率 / 流程完备率 / 标识一致率）。
- 无读者侧度量：谁读、读哪节、是否用于决策、是否发现错误。

## 输入
- `engine/tools/build_hub.py`（hub / reader 生成）
- `engine/tools/report_style.py`（canonical 令牌与页脚组件）
- `engine/docs/page-build-spec.md`
- `engine/tools/metrics-dictionary.json`

## 动作
1. 设计反馈入口：报告页脚加「反馈 / 纠错」入口（静态链接或 `data-` 属性占位，避免外部依赖）。
2. 在 `build_hub.py` / 模板中落地，保持 canonical 令牌与设计系统。
3. 定义消费侧指标草案（如「决策卡被引用次数」「纠错条目数」），写入 `metrics-dictionary.json` 备注（**先不接线**，标 `probe`）。
4. 单测：若改动生成逻辑，加 `test_hub`/`test_process_gates` 相关用例。

## 输出
生成逻辑改动 + 设计说明 + 字典备注。

## 验收标准
- `python engine/tools/build_hub.py --check` 通过（产物确定性）。
- 反馈入口在 hub 与报告页脚可见。
- 消费侧指标定义入库（标 `probe`）。

## 禁止
- 不引入外部服务 / 不合规脚本；不改 canonical 令牌；不破坏无 JS 可用性。

## 完成前证据索引（必填）
1. 变更文件 + diff 摘要；
2. `build_hub.py --check` 输出；
3. 对齐声明：T-06 验收逐条；
4. 回归声明：R-REG-1 / R-REG-7 / R-REG-9。
