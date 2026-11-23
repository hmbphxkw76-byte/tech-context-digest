# 多会话 Git 协作协议（MULTI-SESSION-GIT-PROTOCOL v1.7）

> **状态**：现行规范
> **定位**：当多个 Agent 会话与多个 GitHub Actions 共用同一仓库、同一 `main` 时，约定统一的提交与合并方式，保证**各任务独立提交互不覆盖**。
> **单一事实源**：本文件 + `engine/tools/repo_sync.py`（统一提交网关）；分支命名另见
> [branch-naming-and-lifecycle.md](branch-naming-and-lifecycle.md)（BRANCH-NAMING-SPEC v1.0）。
> **最后更新**：2026-11-22

---

## 一、问题根因

- `main` 是唯一共享可变引用；写入者包括多个 Agent 会话与 4 个 CI 工作流（`audit.yml` / `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml`）。
- CI 之间用 `concurrency: auto-commit-main` 串行，但**Agent 推送在该并发组之外**。
- 本地检出在 `fetch` 与 `push` 之间过期 → **non-fast-forward**；仓库为 **public**，服务端分支保护（Require PR）兜底。

---

## 二、三层隔离机制

| 层 | 机制 | 作用 |
|---|---|---|
| 分支隔离 | 任务在 `task/<slug>-<session8>` 分支提交（会话标识内嵌，见 BRANCH-NAMING-SPEC v1.0）；禁止直推 `main` | 任务之间提交 / 文件互不干扰，且分支可回溯到会话 |
| 串行合并 | 经 PR 合并到 `main`（CI 侧：门禁内移 + 立即合并；Agent 侧：`repo_sync pr`） | 基于最新 main、一次一个，杜绝覆盖 |
| 共享检出锁 | `.git/catpaw-sync.lock` 互斥 + 推送前 `fetch --rebase` | 多会话共用工作目录时防并发覆盖 |

> **服务端分支保护（v1.8）**：仓库为 **public**，`main` 已启用服务端分支保护
> （**Require PR** + **enforce_admins** + 评审数 0 + 禁 force-push / 禁删除；
> **不要求必需状态检查**——质量门已内移至工作流，见 §6.1）——直推 `main` 由
> **服务端直接拒绝**。客户端 pre-push 钩子 + `repo_sync.py` 网关为第二道拦截；`ci.yml` 的
> `history-audit` 仍作事后追溯（push 到 main 时运行 `engine/tools/git_history_audit.py`，
> 将「非合并、无 `(#NN)`、非 CI 留痕、不在历史白名单」的首亲提交判为疑似直推并失败告警）。

---

## 三、标准工作流

```bash
# 1) 建任务分支（从最新 main 出发，自动追加会话标识）
python engine/tools/repo_sync.py branch <slug>      # → task/<slug>-<session8>

# 2) 统一网关提交（锁 → 优化流程门禁 --gate → sync → commit → push 当前分支）
python engine/tools/repo_sync.py run --message "feat(x): ..." --paths <files...> --gate

# 3) 开 PR（Agent 任务；--queue 启用服务端自动合并）
python engine/tools/repo_sync.py pr --title "..." --body "..." --queue

# 4) 合并后由 CI / 维护流程同步 main；下次任务从最新 main 重新出发
```

**禁止**：`git push origin main`（除非显式 `--allow-main`，仅用于紧急修复并需人工确认）。

**强制**：任务提交必须带 `--gate`（AGENTS.md「优化流程门禁」硬性约束）；未过门禁（`[E]`）时 `run` 直接拒绝提交，不得绕过。

---

## 四、统一网关命令（`engine/tools/repo_sync.py`）

| 命令 | 行为 |
|---|---|
| `status` | 分支、与 `origin/main` 偏离、锁状态 |
| `lock` / `unlock` | 显式获取 / 释放共享检出锁 |
| `sync [base]` | `fetch + rebase`；冲突则 `rebase --abort` 并报告 |
| `push [--allow-main]` | 默认拒绝推 `main`；推当前分支前自动 `sync`；受管分支命名不符同样拒绝 |
| `pr [--queue]` | 创建 PR；`--queue` 请求进入合并队列 |
| `run --message M --paths ... [--gate] [--checks ...]` | 锁 →（`--gate`）优化流程统一门禁 → 校验（可选）→ commit → push；门禁 [E] 拒绝提交 |
| `session` | 解析并打印当前会话标识（含来源），供建分支与排查 |
| `branch <slug> [--from <ref>]` | 按 BRANCH-NAMING-SPEC 自动追加会话标识建分支，并登记台账 |
| `branches` | 列出手头分支 + 登记信息 + 合规标记 |
| `branch-audit` | 扫描存量分支，列出受管但命名违规项（有违规退出码 1） |
| `branch-rename <旧> <新> [--remote]` | 改名并同步登记册；`--remote` 连同远端旧分支迁移 |
| `hook-install` / `hook-uninstall` | 安装 / 卸载 `.githooks`（`core.hooksPath`） |
| `guard [--stage push\|commit]` | 钩子调用：按 refspec（push）或当前分支（commit）判定；直推 `main`、GitLab 远端、受管分支命名不符时返回 1 |

---

## 五、pre-push / pre-commit 钩子（本克隆强制）

```bash
python engine/tools/repo_sync.py hook-install   # 内部即 git config core.hooksPath .githooks
python engine/tools/repo_sync.py hook-uninstall  # 即 git config --unset core.hooksPath
```

**pre-push** 在门禁前调用 `workspace_cleanup.py`（容错），随后判定基于 **pre-push stdin 的
refspec**（`<local ref> <local sha> <remote ref> <remote sha>`），而非当前分支：

- 任一 remote ref 为 `refs/heads/main` 且非删除 → 阻断（**站在 `task/*` 上显式 `git push origin main` 也会被阻断**）；
- 受管分支（`task/*`）命名不符合 BRANCH-NAMING-SPEC（缺 `-<session8>` 等）→ 阻断，提示用
  `repo_sync.py branch-rename` 整改；
- 删除 `main`（`(delete)`）或推送 `ci/*` 等豁免分支 → 放行（因此可在 `main` 上清理远端已合并分支）；
- 无 stdin（手动执行 `repo_sync.py guard`）→ 回退为当前分支判定。

**pre-commit**（`repo_sync.py guard --stage commit`）：当前检出为受管分支且命名不合规 → 阻断提交，
避免「先提交、后改名」留下不可追溯的历史；`main` / `ci/*` 豁免。

统一网关（`repo_sync.py push` / `run` / `pr`）复用同一套命名判定，**钩子未安装时同样拦截**。

### 5.1 远端约束：仅 GitHub，禁用 GitLab

本仓库**只允许 GitHub 远端**（用户硬性约束）。`guard` 在判定 `main` 之前先扫描 `git remote -v`：

- 任一远端 URL 含 `gitlab`（大小写不敏感）→ **阻断推送**，提示改用 GitHub 或移除该远端；
- `repo_sync` 统一网关与 `.githooks/pre-push` 均调用 `gitlab_remote_blocked()`，`engine/tests/test_repo_sync.py` 强制校验当前仓库无 GitLab 远端。

---

## 六、CI 侧约定（CI 也走 PR · 门禁内移自动合并）

- 4 个自动提交工作流（`audit.yml` / `html-sync.yml` / `content-update.yml` / `scheduled-maintenance.yml`）**不直推 `main`**，统一复用 `.github/actions/submit-pr`：提交到固定 CI 分支（`ci/audit`、`ci/html-sync`、`ci/content-update`、`ci/scheduled-maintenance`）→ **先在工作流内跑门禁**（统一入口 `optimization_gate.py`；`audit.yml` 为四环节审计）→ 开 / 复用 PR → **门禁通过即 `gh pr merge --merge` 立即合并**。
- `main` 分支保护：**Require a pull request before merging** + **enforce_admins** + 评审数 0；**不再要求必需状态检查**（原因见 §6.1）。
- Agent 侧仍经 `repo_sync`（推送前 `sync`），与 CI 分支互不冲突（分支不同、目标不同）。

### 6.1 为什么移除必需状态检查（对齐 jp-life-work）

GitHub 官方规则：**当使用 `GITHUB_TOKEN` 的工作流创建 / 更新 PR 时，生成的 `pull_request`（`opened` / `synchronize` / `reopened`）工作流运行一律处于「需要批准」状态**——这是防递归的硬规则，**没有任何设置可关**。因此：

- bot 创建的 CI PR，其 `pull_request` 工作流要么被门禁、要么不触发 → 若把它们设为**必需检查**，`gh pr merge --auto` 会**永久 `BLOCKED`**；
- 故本仓库**把门禁内移到工作流**（提交前执行，失败即中止 job），并在 `submit-pr` 中**门禁通过后立即 `gh pr merge --merge`**；分支保护**移除必需状态检查**（保留 Require PR + enforce_admins + 评审数 0），使被门禁的 `pull_request` 运行不再阻塞合并。
- 这些被门禁的空跑运行（`action_required`）由 `submit-pr` 在合并后**自动删除**（限 `head_branch` 为 `ci/*`，需 `actions: write`），避免 Actions 列表累积「待批准」噪音。

**取舍**：服务端不再强制必需检查；质量门由「工作流内门禁 + 本地 `repo_sync run --gate`」保证（与 jp-life-work v1.3 同口径）。

**无凭据**：`submit-pr` 的 `token` 输入留空即回退 `GITHUB_TOKEN`。如将来设 PAT / GitHub App 安装令牌，PR 作者变更、`pull_request` 工作流亦可正常触发——属**可选增强**，非必需。

---

## 七、冲突与回滚

- `sync` 冲突：工具 `rebase --abort` 并打印冲突文件；人工解决后重试。
- 锁残留：`.git/catpaw-sync.lock` 带 PID + 时间戳，超过 TTL（600s）或进程不存在时自动回收。
- 误推：`git reset --soft HEAD~1` 或 `git revert <sha>`。

---

## 八、版本记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-11-15 | 初始版本：三层隔离、repo_sync 网关、pre-push 钩子 |
| v1.1 | 2026-11-15 | CI 也改为开 PR + 自动合并；main 启用分支保护（必需检查 + strict） |
| v1.2 | 2026-11-15 | `guard` 改为按 pre-push refspec 判定：堵住「站在 task 分支显式推 main」的绕过，同时不再误拦远端分支删除 |
| v1.3 | 2026-11-15 | `run --gate`：提交前强制复用优化流程统一门禁 `optimization_gate.py`（[E] 拒绝提交）；新增 `--checks` 自定义校验 |
| v1.4 | 2026-11-16 | 新增远端约束：`guard` 扫描 `git remote -v`，任一远端含 `gitlab` 即阻断推送（本仓库仅允许 GitHub）；单测强制校验 |
| v1.5 | 2026-11-17 | 分支命名纳入协议：任务分支统一 `task/<slug>-<session8>`（BRANCH-NAMING-SPEC v1.0）；新增 pre-commit 钩子与 `hook-install` / `branch` / `branch-rename` / `branch-audit` 子命令；网关复用命名校验 |
| v1.6 | 2026-11-18 | 更正「main 启用分支保护」表述：private 免费方案服务端保护不可用；新增 CI 首亲历史直推审计（`git_history_audit.py` + `ci.yml::history-audit`）作为补偿检测 |
| v1.7 | 2026-11-22 | 仓库转为 **public**，服务端分支保护正式启用（Require PR + status checks + strict + enforce_admins）+ auto-merge；CI 触发恢复自动（public 免费额度）；新增 `LICENSE`（MIT） |
| v1.8 | 2026-11-23 | 对齐 jp-life-work：**门禁内移 + 立即合并**——`submit-pr` 改为建 PR 后 `gh pr merge --merge`（不再 `--auto`）；分支保护**移除必需状态检查**（保留 Require PR + enforce_admins + 评审数 0）；删除 `CI_PR_TOKEN`（无凭据、零审批、零 review） |
