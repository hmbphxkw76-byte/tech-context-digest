# 04 · 自动修复执行（repair）

> **阶段**：5。**上游**：`03-classify.md`。**下游**：`05-verify.md`。
>
> **目标**：按 `../repair-sop.md` 逐条执行修复，无需人工触发；产物可回溯、可回滚。

---

## 一、执行前置

1. 确认阶段 0 备份存在（每个待改文件有 `.bak`，或 git 工作区干净）。
2. 读取 `../repair-sop.md`，确认每条 finding 的 SOP 条款与分级。
3. 按修复队列顺序执行。

---

## 二、分级执行

| 分级 | 处置 | 是否需人工触发 |
|---|---|---|
| 自动执行 | 直接修改 | 否 |
| 备份后执行 + 标记待复核 | 修改并标 `pending-human-review` | 否 |
| 仅标记 | 不修改，写入待复核清单 | 否（但产物标记） |

> 任何分级都**不阻塞**流程；无法执行的写入待复核清单。

---

## 三、逐条执行流程

对队列中每条 finding：

```
1. 读取目标文件与上下文（business-config / 登记册 / 词汇库）。
2. 按 SOP 条款判定权威源，确定修复方案。
3. 写修复记录草稿（finding / sop / action / backup）。
4. 执行修改（工具命令或编辑）。
5. 即时验证（该 SOP 的「修复后验证」）。
6. 通过 → status = fixed；不通过 → 回滚并标 skipped / pending-human-review。
7. 写入 repairs[]。
```

---

## 四、SOP 执行入口

| SOP | 场景 | 执行入口 |
|---|---|---|
| SOP-01 | C01 | 编辑低权威源 + 回写登记册 |
| SOP-02 | C02 | 保留权威源，其余改引用 / 删除 |
| SOP-03 | C03 | 补桥接 / 补证据，或降级「待核实」 |
| SOP-04 | C04 | `python engine/tools/classify_reports.py --apply --unknown-warn` + 手动移动 + 重生成索引 |
| SOP-05 | C05 | 补采补写；不能补则标「未核验」 |
| SOP-06 | C06 | 复核来源 + 续写「已修正事实清单」 |
| SOP-07 | C07 | 补来源 / 标「需核实原文」/ 删数值 |
| SOP-08 | C08 | 按口径表统一 + 并列呈现 |
| SOP-09 | C09 | 修路径 / 锚点；批量迁移用专用改写脚本 |
| SOP-10 | C10 | 以登记册为准同步 business-config + 报告 |
| SOP-11 | C11 | `compliance_check.py --scaffold <类型ID> [周期]` 后按骨架补节 |
| SOP-12 | C12 | `vocab_tool.py import` 补词条，统一写法 |
| SOP-13 | C13 | 更新数据或标「滞后 N 期」 |
| SOP-14 | C14 | `restyle_reports.py --files <报告.html> --rename-chart --fix-colors` + 补 a11y |
| SOP-15 | C15 | 修 `layout.json` + 目录重构 + 批量改写引用 |

---

## 五、批量操作命令

```bash
# 结构类
python engine/tools/compliance_check.py --scaffold <类型ID> [周期]

# 格式类
python engine/tools/restyle_reports.py --files <报告.html> --rename-chart --fix-colors

# 归位类
python engine/tools/classify_reports.py --apply --unknown-warn

# 词汇类
python engine/vocabulary/script/vocab_tool.py import --topic <主题> --file <导入文件>
python engine/vocabulary/script/sync_vocab.py sync --topic <主题>
```

---

## 六、修复记录

每条写入 `repairs[]`，格式见 `../repair-sop.md` 第六节；字段：`id / scenario / sop / severity / target / finding / action / backup / verification / status / timestamp`。

---

## 七、回滚

- 单文件回滚：用 `.bak` 覆盖。
- 批量回滚：`git checkout -- <路径>`（仅限未提交改动）。
- 回滚后该 finding 标 `skipped`，计入待复核清单。

---

## 八、纪律

- 不删除历史报告 / 基线。
- 不编造数据、日期、URL、机构名。
- 不修改只读附件。
- `LEGACY` 组不自动修复。
- 每次修复后立即验证，不攒到最后。
- 连续两轮 P0 不下降 → 停止修复，输出待复核清单。
