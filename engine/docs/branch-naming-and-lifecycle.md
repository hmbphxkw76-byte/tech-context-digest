# 分支命名与生命周期规范（BRANCH-NAMING-SPEC v1.0）

> **状态**：现行规范
> **定位**：规定本仓库**分支命名**的统一模板、会话标识嵌入规则、校验拦截点与登记台账，使任
> 何一条开发分支都能回答「属于哪个会话、对应哪件任务」，并与
> [multi-session-git-protocol.md](multi-session-git-protocol.md)（提交与合并方式）配合使用。
> **单一事实源**：本文件 + `engine/tools/branch_naming.py`（纯逻辑）+ `engine/tools/repo_sync.py`
> （CLI 与拦截）+ `engine/tools/branch_registry.json`（登记册）。
> **最后更新**：2026-11-17

---

## 一、为什么要管分支名

多会话 / 多 CI 共用同一 `main` 时，`task/<slug>` 这种名字只能表达「做了什么」，无法表达
「谁在做」。后果：分支删除后无法回溯到任务上下文；多个会话的同名 `task/fix` 互相混淆；出问题
时无法把分支关联到会话记录。因此**受管开发分支必须内嵌会话标识**。

---

## 二、命名规范

### 2.1 受管分支模板

```
task/<slug>-<session8>
```

| 部分 | 说明 | 示例 |
|---|---|---|
| `task/` | 分支种类（kind），当前唯一受管种类 | `task/` |
| `<slug>` | kebab-case 任务名：小写字母 / 数字 / 单连字符，不含首尾连字符 | `ci-permissions-fix` |
| `<session8>` | **会话标识短码**，会话标识归一化后的前 8 位十六进制 | `5f37e90d` |

完整示例：`task/ci-permissions-fix-5f37e90d`

正则（`branch_naming.TASK_BRANCH_RE`）：

```
^task/[a-z0-9]+(?:-[a-z0-9]+)*-[0-9a-f]{8}$
```

### 2.2 会话标识

**归一化**：转小写、去连字符，结果必须为 8–64 位十六进制（`branch_naming.SESSION_RE`）。
标准 UUID 直接可用。

**解析链**（`resolve_session()`，命中即停）：

1. 环境变量 `TECH_CTX_SESSION_ID`（显式覆盖，任意 Agent 平台通用）
2. 环境变量 `CATPAW_CONVERSATION_ID`（妙手会话 ID）
3. 环境变量 `X_AI_SESSIONID`（兼容别名）
4. `git config techctx.sessionId`（本克隆兜底）

**全部缺失 → 拒绝自动建分支**（`BranchNamingError`），不设 `local-xxx` 之类的伪标识，避免产生
不可追溯分支。显式设置的值非法时**直接失败**，不悄悄回退到下一来源。

### 2.3 豁免分支

| 分支 | 理由 |
|---|---|
| `main` | 共享基座，命名不可变 |
| `ci/*` | GitHub Actions 固定分支（`ci/audit`、`ci/html-sync`、`ci/content-update`、`ci/scheduled-maintenance`），由工作流拥有 |

豁免分支**不参与**会话标识校验，钩子与网关对其放行。其它未以 `task/` 开头的自建分支同样放行，
但**不登记**、不享受台账追溯。

### 2.4 会话标识与任务的映射

登记册 `engine/tools/branch_registry.json` 记录每条受管分支的
`session`（完整标识）/ `session_short` / `slug` / `task` / `note`。
从会话反查分支：`branch_naming.session_ledger()`；CLI 见 §3.3。

**条目保留策略**：分支合并 / 删除后其条目**保留**，作为历史台账支撑事后追溯；
`branch-audit` 只检查当前存在的分支，不会因历史条目报错。

---

## 三、标准操作流程

### 3.1 建分支（自动追加会话标识）

```bash
python engine/tools/repo_sync.py branch <slug>
# 例：python engine/tools/repo_sync.py branch ci-permissions-fix
# → 已创建 task/ci-permissions-fix-5f37e90d
```

行为：解析会话标识 → 校验 slug → 从 `origin/main` 建分支 → 写入登记册。
指定其它起点：`--from <ref>`。

查看当前会话标识：

```bash
python engine/tools/repo_sync.py session
```

### 3.2 提交与合并

沿用 [multi-session-git-protocol.md](multi-session-git-protocol.md)：
`repo_sync.py run --message ... --paths ... --gate` → `repo_sync.py pr --queue`。
**禁止直推 `main`**；网关与 pre-push 钩子双重拦截。

### 3.3 查看与梳理

```bash
python engine/tools/repo_sync.py branches        # 分支 + 登记信息 + 合规标记
python engine/tools/repo_sync.py branch-audit    # 受管但命名违规清单（有违规退出码 1）
```

### 3.4 存量分支整改

```bash
python engine/tools/repo_sync.py branch-rename <旧名> <新名>            # 本地改名 + 登记册
python engine/tools/repo_sync.py branch-rename <旧名> <新名> --remote   # 连同远端一起迁移
python engine/tools/repo_sync.py branch-delete <分支> [--allow-unmerged]  # 删本地 + 远端；登记条目保留
```

新名必须符合 §2.1；旧名未登记时会用当前会话标识补齐。
`branch-delete` 仅删 `task/*`，默认要求已合并进 `main`；**登记册条目按 §2.4 保留**
（历史台账），不随分支删除而注销。

### 3.5 钩子安装（每个克隆一次）

```bash
python engine/tools/repo_sync.py hook-install     # git config core.hooksPath .githooks
python engine/tools/repo_sync.py hook-uninstall
```

---

## 四、校验与拦截点

同一套判定逻辑（`branch_naming.validate_managed`）被三个入口复用，口径一致：

| 入口 | 触发 | 行为 |
|---|---|---|
| `.githooks/pre-push` | `git push` | 直推 `main` / GitLab 远端 / 受管分支命名不合规 → **阻断** |
| `.githooks/pre-commit` | `git commit` | 当前检出为受管分支且命名不合规 → **阻断** |
| `repo_sync.py` 网关（`push` / `run` / `pr`） | 提交推送 | 同上（**不依赖钩子是否安装**，钩子未装时仍拦截） |

说明：

- 判定基于 pre-push stdin 的 **refspec**，站在 `task/*` 上显式 `git push origin main` 同样被阻断；
- 删除远端分支（`(delete)`）始终放行，便于清理已合并分支；
- `pre-push` 在门禁前调用 `workspace_cleanup.py`（容错，失败不阻断），沿用工作区清理单一入口。

---

## 五、角色与执行标准

| 角色 | 必须做 | 禁止 |
|---|---|---|
| Agent 会话 | 用 `repo_sync.py branch <slug>` 建分支；提交走 `run --gate`；合并走 `pr` | 手打 `task/<slug>` 分支名；直推 `main`；绕过网关 |
| 协作者 / 人工 | 同左；首次克隆执行 `hook-install` | 在未装钩子的克隆上直推 `main`（网关仍会拦） |
| CI 工作流 | 使用固定 `ci/*` 分支，经 `.github/actions/submit-pr` 开 PR | 直推 `main`；新建 `task/*` 分支 |
| 维护者 | 定期 `branch-audit`；合并后清理已合并分支 | 手工编辑登记册（用 `branch-rename`） |

---

## 六、异常处理

| 现象 | 根因 | 处置 |
|---|---|---|
| `[拒绝] 推送被阻断 … 命名不合规` | 分支名缺 `-<session8>` 或格式错 | `branch-rename` 改成 `task/<slug>-<session8>` |
| `[FAIL] 未解析到会话标识` | 四类来源全空 | 设 `TECH_CTX_SESSION_ID` 或 `git config techctx.sessionId` |
| `[FAIL] … 取值非法` | 标识含非十六进制或长度不足 | 用标准 UUID（或 8–64 位 hex） |
| `[拒绝] 禁止直接推送 main` | 直推基座 | 改用 `task/<slug>-<session8>` + PR；确需紧急直推用 `--allow-main` 并人工确认 |
| `pre-commit` 阻断提交 | 在违规受管分支上提交 | 先 `branch-rename`，再提交 |
| 钩子未生效 | 新克隆未装 | `hook-install`；`git config --get core.hooksPath` 应为 `.githooks` |
| 误删远端分支 | `--remote` 迁移出错 | 用 `git push origin <新名>` 恢复；登记册用 `branch-rename` 回滚 |

**紧急直推**：`repo_sync.py run --allow-main` / `push --allow-main` 仍保留（仅紧急修复并需人工
确认），但**不受命名规范豁免**——`main` 本身即豁免分支。

---

## 七、版本记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-11-17 | 初始版本：`task/<slug>-<session8>` 模板、会话标识解析链、登记册、pre-push / pre-commit 钩子与网关三重拦截 |
