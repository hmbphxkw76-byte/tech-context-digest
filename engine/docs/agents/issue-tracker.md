# Issue Tracker：GitHub

> **状态**：现行约定
> **用途**：本仓库的 issue 与 spec 托管在 GitHub，所有操作使用 `gh` CLI。

## 常用命令

- **创建**：`gh issue create --title "..." --body "..."`（多行正文用 heredoc）。
- **读取**：`gh issue view <number> --json number,title,body,labels,comments`。
- **列表**：`gh issue list --state open --json number,title,labels --jq '[.[] | {number, title, labels: [.labels[].name]}]'`（可加 `--label` / `--state` 过滤）。
- **评论**：`gh issue comment <number> --body "..."`。
- **标签**：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`。
- **关闭**：先 `gh issue comment <number> --body "..."` 说明，再 `gh issue close <number>`。

仓库从 `git remote -v` 推断；`gh` 在克隆内会自动识别。

## 子任务与阻塞关系

- **设为子 issue**：`gh issue create --parent <parent> ...`，或 `gh issue edit <parent> --add-sub-issue <child>`（`gh` 2.94+）。旧版 `gh` 用 `gh api --method POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<child-db-id>`。不支持子 issue 时，在子 issue 正文顶部写 `Part of #<parent>`。
- **阻塞关系**：使用 GitHub **原生 issue 依赖**（UI 可见）。`gh issue create --blocked-by <n>,<n> ...` 或 `gh issue edit <child> --add-blocked-by <blocker>`（`gh` 2.94+）。旧版 `gh` 用 `.../dependencies/blocked_by -F issue_id=<blocker-db-id>`，其中 id 为 **database id**（`gh api repos/<owner>/<repo>/issues/<n> --jq .id`），不是 `#number` / `node_id`。无依赖功能时回退为正文顶部 `Blocked by: #<n>, #<n>`；阻塞项全部关闭即解除。
- **统计未关闭阻塞**：`gh api repos/<owner>/<repo>/issues/<n> --jq .issue_dependencies_summary.blocked_by`（0 = 可开工）。`gh issue view <n> --json blockedBy` 会含已关闭项，需过滤 `--jq '[.blockedBy.nodes[] | select(.state == "OPEN")] | length'`。

## PR 作为 triage 面

默认**不**将外部 PR 当作需求面。若确需启用，PR 与 issue 共用同一标签与状态机，使用 `gh pr` 等价命令（`gh pr view` / `gh pr diff` / `gh pr comment` / `gh pr edit --add-label` / `gh pr close`）。GitHub 的 issue 与 PR 共用编号空间，裸 `#42` 可能指任一：先 `gh pr view 42`，失败再 `gh issue view 42`。

## 远端确认

只在用户自己的仓库建 issue，**不要**提到 skill 的来源仓库。fork 场景下 `gh` 可能默认指向上游；会话首次 `gh issue create` 前用 `gh repo view --json nameWithOwner` 确认目标，非本人仓库时与用户确认。

## Wayfinding 操作

`/wayfinder` 使用：**map** 是单个带 `wayfinder:map` 标签的 issue，正文含 Notes / Decisions-so-far / Fog；**子 ticket** 为 map 的子 issue（或正文任务列表项 + `Part of #<map>`），标签 `wayfinder:<type>`（`research` / `prototype` / `grilling` / `task`）。认领用 `gh issue edit <n> --add-assignee @me`；解决后用评论写答案并关闭，再把上下文指针（gist + 链接）追加到 map 的 Decisions-so-far。
