# 50 · 周期深度复核与终审提示词（L3 + 终审）

> **执行者**：妙手定时任务（Agent）· **依据**：`engine/audit/verification.md` 第四节、`engine/audit/acceptance.md` 第一节。
> **触发**：每周定期（见 `engine/audit/README.md` 第三节的 CI/定期任务表）。

## 一、目标

对全部 `category=report` 的正式报告完成 **L3 语义深度复核** 与 **终审签发**，补齐 CI 确定性四环节未覆盖的语义部分。

## 二、执行步骤

1. `python engine/audit/scripts/audit_tool.py init`（刷新登记）。
2. **L3 语义深度复核**（逐项写下证据）：
   - 信息准确性：关键数字与登记册/台账/官方来源核对，一致率 ≥ 99%；
   - 来源可追溯：关键数字来源率 ≥ 95%；死链 = 0；
   - 数据一致性：跨章节/跨报告同指标 ≥ 99%；阈值三处一致率 100%；
   - 表述逻辑：结论-证据一致率 ≥ 95%；事实与推断分离；口径并列不合并。
3. **记录复核**：`review <report> --stage second --reviewer agent --decision pass|fix --evidence "<证据>"`。
4. **终审**：按 A1–A8 核对；通过者 `review <report> --stage final --reviewer agent --decision pass --evidence "终审通过"`，随后 `mark <report>`。
5. **验收与抽检**：`accept` + `sample --ratio 0.3 --seed <date>`。
6. **提交留痕**：`git add -A && git commit -m "chore(audit): 周期 L3 深度复核与终审（YYYY-MM-DD）" && git push`；网络不可达时保留本地提交并说明。

## 三、纪律

- 不得跳级；四环节记录齐备方可 `mark`。
- 每条 finding 必须可回溯到报告位置与证据；禁止「感觉不一致」。
- 不编造数据、日期、URL、机构名；不修改报告正文（标识除外）。
- 内容质量问题登记后交 `engine/quality/` 修复闭环。

## 四、输出

本轮复核报告：通过/待修清单 + 关键指标 + 是否需人工介入。
