# 「已审计」标识规范（AUDIT-MARK v1.1）

> **定位**：对经完整审计流程（生成→初审→复核→终审）确认通过的报告，在**显著位置**赋予统一、明确的审计状态标识；未通过或未审计的报告不得携带该标识。
>
> **单一事实源**：标识内容由 `engine/audit/records/audit_registry.json` 生成，工具注入，禁止手工另写。
> **版本说明**：v1.1 起标识分为三态（`none / pre / full`），未做 L3 语义复核不得使用「已审计」字样。

---

## 一、标识三态

| 状态 | 触发条件 | 标识文案 | 色彩 |
|---|---|---|---|
| `none` | 未进入流程 | 无标识 | — |
| `pre` | `machine_final` 通过、`semantic_final`（L3）未完成 | 「预审通过（机器）· 语义复核待完成」 | 灰 `#5b6b7c` |
| `full` | 四环节齐备且含 L3（Agent 复核 pass） | 「已审计 · 终审通过」 | canonical navy `#16324f` |

- **不可冒充**：`pre` 与 `full` 视觉与文案必须可区分；禁止以「预审」充当「已审计」。
- `mark_level` 存于 `audit_registry.json`；`accept` 分别统计 full / pre。

---

## 二、标识形态（HTML 报告）

注入于 `<body>` 起始处的顶部横幅（最显著位置），`data-mark-level` 标注状态：

```html
<div class="audit-mark" data-audit-id="AUD-2026-11-14-001" data-mark-level="full"
     style="background:#16324f;color:#fff;font:600 13px/1.6 system-ui,-apple-system,'Segoe UI',sans-serif;
            padding:8px 16px;text-align:center;letter-spacing:.02em">
  <span class="audit-badge">已审计</span>
  <span class="audit-meta">终审通过 · 2026-11-14 · 审查链 4/4 · AUD-2026-11-14-001</span>
</div>
```

`pre` 态示例（灰色）：

```html
<div class="audit-mark" data-audit-id="AUD-2026-11-14-001" data-mark-level="pre"
     style="background:#5b6b7c;color:#fff;...">
  <span class="audit-badge">预审通过（机器）</span>
  <span class="audit-meta">语义复核待完成 · 2026-11-14 · 审查链 3/4 · AUD-2026-11-14-001</span>
</div>
```

- **色彩**：full 仅用 canonical `--navy:#16324f`；pre 用灰；禁止漂移色。

---

## 三、标识形态（Markdown 审计报告）

```markdown
> **【已审计】** 终审通过 · 签发日期 2026-11-14 · 审查链 4/4 · 登记编号 AUD-2026-11-14-001
```

pre 态：

```markdown
> **【预审通过（机器）】** 语义复核待完成 · 2026-11-14 · 审查链 3/4 · 登记编号 AUD-2026-11-14-001
```

---

## 四、注入与撤除（`audit_tool.py`）

| 命令 | 行为 |
|---|---|
| `audit_tool.py mark <report> --level full` | 四环节齐备 → 注入/更新「已审计」；否则拒绝 |
| `audit_tool.py mark <report> --level pre` | 生成 + 初审通过 → 注入「预审通过（机器）」 |
| `audit_tool.py unmark <report>` | 移除标识，`mark_level=none`，状态回 `in-review` |
| `audit_tool.py status [report]` | 输出登记状态、审查链进度与标识分级 |

- 注入前备份 `.bak`；幂等（重复执行不产生副作用）。
- `audit_tool.py run --strict`：final 由 `machine_final + semantic_final` 判定；未做 L3 时只能注入 `pre`。

---

## 五、合规约束

1. 标识 = 审计状态的**唯一权威呈现**；与 registry 不一致时以 registry 为准并告警。
2. 未通过终审的报告携带「已审计」标识即视为**合规违规**（P0）。
3. 标识不改变报告内容本身，仅呈现状态；报告修订后须重新走流程并更新标识。

---

## 六、版本记录

| 版本 | 日期 | 变更 | 说明 |
|---|---|---|---|
| v1.0 | 2026-11-14 | 初始版本 | 标识形态（HTML/MD）、状态区分、注入/撤除与合规约束 |
| v1.1 | 2026-11-15 | 三态分级 | 新增 `pre`（预审通过），`full` 须含 L3；`data-mark-level` 与 `mark --level` |
