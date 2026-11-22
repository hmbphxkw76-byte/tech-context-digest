## 本地等价 CI 运行手册（LOCAL-CI-RUNBOOK v1.0）

**目的**：把「本地优先、远程兜底、结果分享」固化为可复用流程——本地能跑的一律本地跑，
本地环境不具备的才远程跑，且结果保持可追溯分享。

**单一入口**：`engine/tools/local_ci.py`（编排层，不新增门禁项；统一门禁仍为
`optimization_gate` 的 32 项）。

### 一、本地能跑（14 项 · 只读 · 不依赖外网）

| # | id | 检查 | 对应 CI |
|---|---|---|---|
| 1 | `syntax` | 语法编译 | ci.syntax |
| 2 | `unittest` | 单元测试 | ci.test |
| 3 | `gate` | 统一门禁（不含 `--probe`） | ci.validate |
| 4 | `runner` | 端到端编排校验 | ci.validate |
| 5 | `history` | main 首亲历史审计 | ci.history-audit |
| 6 | `hub` | HTML 同步校验 | html-sync.validate |
| 7 | `page_build` | 页面构建门禁 | 门禁.page_build |
| 8 | `fingerprint` | 发布指纹校验 | scheduled-maintenance |
| 9 | `ledger` | 核验台账链校验 | scheduled-maintenance |
| 10 | `audit` | 审计四环节（dry-run） | audit |
| 11 | `audit_status` | 审计登记状态 | scheduled-maintenance |
| 12 | `l3` | L3 SLA 超期检测 | scheduled-maintenance |
| 13 | `compliance` | 报告合规校验 | scheduled-maintenance |
| 14 | `review` | 来源定期复核 | scheduled-maintenance |

### 二、仅远程（本地环境不具备）

| 环节 | 原因 |
|---|---|
| `probe` | 链接可达率探测（`source_check --probe` / 门禁 `--probe`），依赖外网，不稳定 |
| `submit-pr` | 自动开 PR / 自动合并，需 GitHub token 与网络 |
| `webhook-alert` | 外部告警通道，需 webhook 凭据 |
| `runner-env` | GitHub runner 环境 / secrets / 服务端分支保护 |

> **触发现状（仓库 public）**：public 仓库 Actions 免费，`.github/workflows/` 的 `push` / `schedule`
> 自动触发**已恢复**；本地 `local_ci.py` 仍作为常态校验与结果分享入口（本地优先）。

### 三、用法

```bash
python engine/tools/local_ci.py run                             # 人类可读汇总
python engine/tools/local_ci.py run --json                      # JSON 到 stdout
python engine/tools/local_ci.py run --markdown                  # Markdown 摘要
python engine/tools/local_ci.py run --emit engine/audit/records/local-ci-status.json
python engine/tools/local_ci.py run --only syntax,gate,page_build
python engine/tools/local_ci.py run --skip unittest
python engine/tools/local_ci.py list                            # 检查项 + 远程分工
```

**退出码**：0 全部通过；2 仅警告（无错误）；1 存在错误项；3 用法 / 执行错误。

### 四、结果分享

- **落盘**：`--emit engine/audit/records/local-ci-status.json`（确定性 JSON，无时间戳）。
- **提交**：随任务 PR 一并提交（`repo_sync.py run --gate`），或作为独立 chore PR。
- **PR 描述**：`--markdown` 输出可直接贴入 PR 描述。
- **口径**：本地结果**不替代**远程 CI；两者互补——本地快、可复跑、无副作用；
  远程覆盖自动开 PR / 告警 / 真实 runner 环境。

### 五、维护

- 新增检查项 → 在 `local_ci.py` 的 `CHECKS` 登记（id / 名称 / 对应 CI / 命令），
  并同步本表；单测锁定 id 唯一与退出码映射。
- 仅远程环节变化 → 同步 `REMOTE_ONLY` 与第二节。
- 本手册与工具同源；口径冲突时以工具实现为准。
