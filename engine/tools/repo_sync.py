#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""多会话统一提交网关（repo_sync）。

解决的问题：多个 Agent 会话与多个 GitHub Actions 同时向 main 直推，
本地检出过期导致 non-fast-forward、相互覆盖。

机制（三层隔离）：
  1) 分支隔离：任务在 task/<slug> 分支提交，默认禁止直推 main；
  2) 串行合并：经 PR（可选 merge queue）合并到 main；
  3) 共享检出锁：多会话共用工作目录时互斥，并在推送前 fetch + rebase。

命令：
  status                 查看分支、与 main 的偏离、锁状态
  lock / unlock          显式获取/释放锁
  sync [base]            fetch + rebase 到 origin/<base>（冲突则中止）
  push [--allow-main]    推送当前分支（默认拒绝 main）
  pr [--queue]           创建 PR（--queue 启用自动合并，合并队列入队）
  run --message MSG --paths a b ...  锁 → 校验 → 提交 → sync → 推送
                                        （默认先跑优化流程统一门禁 optimization_gate，含 source_check；
                                          --no-gate 可显式跳过；--checks 追加自定义校验）

退出码：0 成功；1 用法/冲突/被拒；2 检测到风险需人工确认。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT  # noqa: E402
import branch_naming  # noqa: E402

BASE_BRANCH = "main"
MAIN_REF = f"refs/heads/{BASE_BRANCH}"
LOCK_PATH = ROOT / ".git" / "catpaw-sync.lock"
LOCK_TTL_SEC = 600
GATE_SCRIPT = "engine/tools/optimization_gate.py"
GATE_PERIOD = "2026-12"          # 内容门禁（研究内核/信息分层/事实卡片/决策交付）
SOURCE_GATE_PERIOD = "2027-01"   # 来源登记门禁（source_check）


class SyncError(Exception):
    pass


# ---------------------------------------------------------------- git 基础

def _git(*args: str, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=check)


def current_branch() -> str:
    r = _git("rev-parse", "--abbrev-ref", "HEAD")
    if r.returncode != 0:
        raise SyncError(f"无法获取当前分支：{r.stderr.strip()}")
    return r.stdout.strip()


def divergence(base: str = BASE_BRANCH) -> tuple[int, int]:
    """返回 (远端领先, 本地领先)。"""
    r = _git("rev-list", "--left-right", "--count", f"origin/{base}...HEAD")
    if r.returncode != 0:
        return (0, 0)
    a, b = r.stdout.split()
    return int(a), int(b)


def require_task_plan(branch: str | None = None, root: Path | None = None) -> tuple[bool, str]:
    """治理标准 1「工件即门禁输入」：受管 task/* 分支 `run --gate` 前必须存在计划。

    非受管分支（main / ci/* / 其它）不强制；计划路径为
    `engine/audit/records/tasks/<slug>/plan.json`（由 task_plan.py 生成）。
    """
    root = ROOT if root is None else root
    br = current_branch() if branch is None else branch
    parsed = branch_naming.parse_branch(br)
    if parsed is None:
        return True, f"非受管分支 {br}，不强制任务计划"
    slug = parsed["slug"]
    plan = root / "engine" / "audit" / "records" / "tasks" / slug / "plan.json"
    if not plan.exists():
        return False, (f"受管分支 {br} 缺任务计划 {plan.relative_to(root)}；"
                       f"先执行 `python engine/tools/task_plan.py init --slug {slug} --title ...`"
                       f"（或显式 --allow-no-plan 跳过）")
    return True, f"任务计划就绪：{plan.relative_to(root)}"


# ---------------------------------------------------------------- 锁

def _read_lock() -> dict | None:
    if not LOCK_PATH.exists():
        return None
    try:
        return json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"pid": 0, "ts": 0, "holder": "unknown"}


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        try:
            r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True)
        except OSError:
            return False
        out = (r.stdout or b"").decode("gbk", errors="replace")
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def acquire_lock(holder: str = "", timeout: int = 30) -> str:
    """获取共享检出锁；被占用时等待至超时。返回 token。"""
    deadline = time.time() + timeout
    while True:
        try:
            fd = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            token = f"{holder or 'session'}-{os.getpid()}"
            os.write(fd, json.dumps({"pid": os.getpid(), "ts": time.time(), "holder": token}).encode("utf-8"))
            os.close(fd)
            return token
        except FileExistsError:
            rec = _read_lock()
            stale = (rec is None or (time.time() - float(rec.get("ts", 0)) > LOCK_TTL_SEC)
                     or not _pid_alive(int(rec.get("pid", 0))))
            if stale:
                try:
                    LOCK_PATH.unlink()
                except OSError:
                    pass
                continue
            if time.time() >= deadline:
                who = (rec or {}).get("holder", "unknown")
                raise SyncError(f"共享检出锁被 {who} 占用（超时 {timeout}s）")
            time.sleep(2)


def release_lock() -> None:
    try:
        LOCK_PATH.unlink()
    except OSError:
        pass


@contextmanager
def locked(holder: str = ""):
    token = acquire_lock(holder)
    try:
        yield token
    finally:
        release_lock()


# ---------------------------------------------------------------- 同步

def sync(base: str = BASE_BRANCH) -> tuple[bool, str]:
    """fetch + rebase 到 origin/<base>；冲突则 abort 并报告。"""
    r = _git("fetch", "origin", base)
    if r.returncode != 0:
        return False, f"fetch 失败：{r.stderr.strip()}"
    r = _git("rebase", f"origin/{base}")
    if r.returncode != 0:
        _git("rebase", "--abort")
        return False, (f"rebase 到 origin/{base} 冲突，已回退；请人工解决后重试：\n{r.stdout}\n{r.stderr}")
    return True, f"已同步到 origin/{base}"


# ---------------------------------------------------------------- 推送 / PR

def _push(allow_main: bool = False, branch: str | None = None,
          acquire: bool = False) -> tuple[bool, str]:
    br = branch or current_branch()
    if br == BASE_BRANCH and not allow_main:
        return False, (f"拒绝直接推送 {BASE_BRANCH}（会与其他会话/CI 竞争）。"
                       f"请改用 task 分支 + PR；如确需直推，显式加 --allow-main。")
    ok, why = branch_naming.validate_managed(br)
    if not ok:
        return False, (f"分支命名不符合 {branch_naming.SPEC_ID}：{why}\n"
                       f"        改名：python engine/tools/repo_sync.py branch-rename {br} <新名>")
    if acquire:
        with locked(holder=f"push:{br}"):
            return _push(allow_main=allow_main, branch=br, acquire=False)
    ok, msg = sync()
    if not ok:
        return False, msg
    r = _git("push", "-u", "origin", br)
    if r.returncode != 0:
        return False, f"push 失败：{r.stderr.strip()}"
    return True, f"已推送 {br}"


def push(allow_main: bool = False, branch: str | None = None) -> tuple[bool, str]:
    return _push(allow_main=allow_main, branch=branch, acquire=True)


def create_pr(title: str, body: str, queue: bool = False,
              base: str = BASE_BRANCH) -> tuple[bool, str]:
    br = current_branch()
    if br == base:
        return False, "当前在 base 分支，无法对其创建 PR；请先切到 task 分支"
    with locked(holder=f"pr:{br}"):
        ok, msg = _push(allow_main=False, acquire=False)
        if not ok:
            return False, msg
        r = subprocess.run(["gh", "pr", "create", "--base", base, "--head", br,
                             "--title", title, "--body", body],
                            cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            return False, f"创建 PR 失败：{r.stderr.strip()}"
        out = r.stdout.strip()
        if queue:
            # 与 .github/actions/submit-pr 口径一致：启用 auto-merge（仓库开启合并队列时自动入队）。
            # 注意：gh 2.103 无 `--queue` 标志，需显式给合并策略。
            q = subprocess.run(["gh", "pr", "merge", "--auto", "--merge"], cwd=ROOT,
                               capture_output=True, text=True)
            if q.returncode != 0:
                return True, f"PR 已创建，但启用自动合并失败：{q.stderr.strip()}"
        return True, out or f"PR 已创建（{br} → {base}）"


def run(paths: list[str], message: str, allow_main: bool = False,
        checks: list[list[str]] | None = None, gate: bool = True,
        allow_no_plan: bool = False) -> tuple[bool, str]:
    """锁 → 校验 → 提交 → sync → 推送的组合流程。

    先提交再 sync：`git rebase` 要求干净工作区，若先 sync 则带未提交改动时必然失败
    （与协议文档的标准用法矛盾）。sync 失败时提交已保留在本地，修复后可重试 push。
    `gate` 默认 True：先运行优化流程统一门禁（optimization_gate.py，含 source_check），
    [E] 直接拒绝提交；[E] 才拒绝（退出码 2=警告放行）。--no-gate 可显式跳过。
    治理标准 1：受管 task/* 分支在 `--gate` 下必须先有任务计划（plan.json），
    否则拒绝；`--allow-no-plan` 仅用于应急并需人工确认。
    """
    with locked(holder="run"):
        if gate:
            plan_ok, plan_why = require_task_plan()
            if not plan_ok and not allow_no_plan:
                return False, f"工件即门禁输入：{plan_why}"
            r = subprocess.run([sys.executable, GATE_SCRIPT,
                                "--gate-period", GATE_PERIOD,
                                "--source-gate-period", SOURCE_GATE_PERIOD],
                               cwd=ROOT, capture_output=True, text=True)
            if r.returncode == 1:
                return False, (f"优化流程统一门禁失败（[E]，阻断提交）：\n{r.stdout}\n{r.stderr}")
        if checks:
            for cmd in checks:
                r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
                if r.returncode != 0:
                    return False, f"校验失败：{' '.join(cmd)}\n{r.stdout}\n{r.stderr}"
        if not paths:
            return False, "未指定提交路径"
        add = _git("add", "--", *paths)
        if add.returncode != 0:
            return False, f"git add 失败：{add.stderr.strip()}"
        staged = _git("diff", "--cached", "--name-only")
        if not staged.stdout.strip():
            return False, "无变更可提交"
        c = _git("commit", "-m", message)
        if c.returncode != 0:
            return False, f"commit 失败：{c.stderr.strip()}"
        ok, msg = sync()
        if not ok:
            return False, f"{msg}（提交已保留在本地，修复后可重试 push）"
        return _push(allow_main=allow_main, acquire=False)


# ---------------------------------------------------------------- 直推守卫

GITLAB_RE = re.compile(r"gitlab", re.IGNORECASE)


def _remote_urls() -> list[str]:
    """读取全部远端 URL（git remote -v 的第二列）。"""
    r = subprocess.run(["git", "remote", "-v"], cwd=ROOT, capture_output=True, text=True)
    return [parts[1] for parts in (ln.split() for ln in r.stdout.splitlines()) if len(parts) >= 2]


def gitlab_remote_blocked(urls: list[str] | None = None) -> tuple[bool, str]:
    """本仓库禁止使用 GitLab 远端（用户硬性约束，见 engine/docs/multi-session-git-protocol.md）。

    命中任一远端 URL 含 gitlab 即拒绝：push 钩子与统一网关都会调用本函数。
    """
    urls = _remote_urls() if urls is None else urls
    for u in urls:
        if GITLAB_RE.search(u):
            return True, f"检测到 GitLab 远端 URL：{u}"
    return False, ""


def parse_push_refs(text: str) -> list[tuple[str, str, str, str]]:
    """解析 pre-push 钩子 stdin：`<local ref> <local sha> <remote ref> <remote sha>`。

    删除远程分支时 local ref 为 `(delete)`、local sha 全 0。
    """
    refs: list[tuple[str, str, str, str]] = []
    for line in (text or "").splitlines():
        parts = line.split()
        if len(parts) == 4:
            refs.append((parts[0], parts[1], parts[2], parts[3]))
    return refs


def guard_push(text: str | None = None) -> tuple[bool, str]:
    """判断本次推送是否属于「直推 main」。

    优先按 pre-push stdin 的 remote ref 判定（删除 main 不算直推）；
    无 stdin（手动调用 / 交互终端）时回退到当前分支判定。
    返回 (是否阻断, 依据)。
    """
    if text is None:
        text = "" if sys.stdin.isatty() else sys.stdin.read()
    refs = parse_push_refs(text)
    if refs:
        for local_ref, _local_sha, remote_ref, _remote_sha in refs:
            if remote_ref == MAIN_REF and local_ref != "(delete)":
                return True, f"本次推送包含 {MAIN_REF}（来自 {local_ref}）"
        for local_ref, _local_sha, remote_ref, _remote_sha in refs:
            if local_ref == "(delete)":
                continue
            name = (remote_ref[len("refs/heads/"):]
                    if remote_ref.startswith("refs/heads/") else remote_ref)
            ok, why = branch_naming.validate_managed(name)
            if not ok:
                return True, f"受管分支 {name} 命名不合规：{why}"
        return False, f"{len(refs)} 条 refspec，均非 {MAIN_REF} 直推且命名合规"
    br = current_branch()
    if br == BASE_BRANCH:
        return True, f"当前检出在 {BASE_BRANCH}，且无 refspec 上下文"
    return False, f"当前分支 {br}，且无 refspec 上下文"


def guard_commit() -> tuple[bool, str]:
    """pre-commit 阶段：当前检出若为受管分支，命名不合规则阻断提交。"""
    br = current_branch()
    if branch_naming.is_managed(br):
        ok, why = branch_naming.validate_managed(br)
        if not ok:
            return True, f"当前受管分支 {br} 命名不合规：{why}"
    return False, f"当前分支 {br}（非受管或命名合规）"


# ---------------------------------------------------------------- 分支命名子命令

HOOKS_DIR = ROOT / ".githooks"
HOOK_FILES = ("pre-push", "pre-commit")


def cmd_session() -> tuple[bool, str]:
    """解析并打印当前会话标识（含来源），供建分支与排查使用。"""
    try:
        full, src = branch_naming.resolve_session()
    except branch_naming.BranchNamingError as e:
        return False, str(e)
    return True, (f"会话标识：{full}\n短码：{branch_naming.session_short(full)}"
                  f"\n来源：{src}\n规范：{branch_naming.SPEC_ID}")


def cmd_branch(slug: str, from_ref: str) -> tuple[bool, str]:
    """按规范自动追加会话标识建分支：task/<slug>-<session8>（从 from_ref 出发）。"""
    try:
        full, src = branch_naming.resolve_session()
        name = branch_naming.build_branch(slug, full)
    except branch_naming.BranchNamingError as e:
        return False, str(e)
    if _git("rev-parse", "--verify", "--quiet", f"refs/heads/{name}").returncode == 0:
        return False, f"分支已存在：{name}"
    r = _git("switch", "-c", name, from_ref)
    if r.returncode != 0:
        return False, f"建分支失败：{r.stderr.strip()}"
    reg = branch_naming.load_registry()
    branch_naming.register_branch(reg, name, full, task=slug, note=f"source={src}")
    branch_naming.save_registry(reg)
    return True, (f"已创建 {name}\n会话短码：{branch_naming.session_short(full)}（来源 {src}）\n"
                  f"已登记到 {branch_naming.REGISTRY_PATH.relative_to(ROOT)}")


def cmd_branches() -> tuple[bool, str]:
    """列出手头分支及其登记信息（含合规标记）。"""
    reg = branch_naming.load_registry()
    names = branch_naming.scan_branches()
    if not names:
        return True, "无可见分支"
    lines = []
    for b in names:
        rec = branch_naming.entry_for(reg, b)
        if branch_naming.is_managed(b):
            ok, _ = branch_naming.validate_managed(b)
            mark = "受管OK" if ok else "受管BAD"
            extra = f"{rec['session']} / {rec['task']}" if rec else "未登记"
        elif b == BASE_BRANCH:
            mark, extra = "基座  ", "-"
        else:
            mark, extra = "豁免  ", "系统分支"
        lines.append(f"[{mark}] {b:<46} {extra}")
    return True, "\n".join(lines)


def cmd_branch_audit() -> tuple[bool, str]:
    """扫描存量分支，列出「受管但缺会话标识」的违规项。"""
    ok_list, bad, exempt = branch_naming.audit_branches()
    lines = [f"受管合规 {len(ok_list)} / 违规 {len(bad)} / 豁免 {len(exempt)}"]
    for b in ok_list:
        lines.append(f"  [合规] {b}")
    for b in bad:
        _, why = branch_naming.validate_managed(b)
        lines.append(f"  [违规] {b}：{why}")
    if bad:
        lines.append("整改：python engine/tools/repo_sync.py branch-rename <旧名> <新名>")
        return False, "\n".join(lines)
    return True, "\n".join(lines)


def cmd_branch_rename(old: str, new: str, remote: bool = False) -> tuple[bool, str]:
    """分支改名并同步登记册；--remote 时连同远端旧分支一起迁移。"""
    ok, why = branch_naming.validate_managed(new)
    if not ok:
        return False, f"新分支名不合规：{why}"
    if old == BASE_BRANCH:
        return False, f"不得对 {BASE_BRANCH} 改名"
    if _git("rev-parse", "--verify", "--quiet", f"refs/heads/{old}").returncode != 0:
        if _git("rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{old}").returncode != 0:
            return False, f"分支不存在：{old}"
        c = _git("branch", old, f"origin/{old}")
        if c.returncode != 0:
            return False, f"从远端取回本地失败：{c.stderr.strip()}"
    reg = branch_naming.load_registry()
    rec = branch_naming.entry_for(reg, old)
    if rec:
        session_full = rec["session"]
    else:
        try:
            session_full, _ = branch_naming.resolve_session()
        except branch_naming.BranchNamingError as e:
            return False, f"{old} 未登记且 {e}"
    if old == current_branch():
        r = _git("branch", "-m", new)
    else:
        r = _git("branch", "-m", old, new)
    if r.returncode != 0:
        return False, f"改名失败：{r.stderr.strip()}"
    branch_naming.unregister_branch(reg, old)
    branch_naming.register_branch(reg, new, session_full,
                                  task=(rec or {}).get("task") or branch_naming.parse_branch(new)["slug"],
                                  note=(rec or {}).get("note", ""))
    branch_naming.save_registry(reg)
    msg = f"已改名 {old} → {new}（登记册已更新）"
    if remote:
        p = _git("push", "origin", new)
        if p.returncode != 0:
            return False, f"{msg}；但推送新分支失败：{p.stderr.strip()}"
        d = _git("push", "origin", "--delete", old)
        if d.returncode != 0:
            return False, f"{msg}；但删除远端旧分支失败：{d.stderr.strip()}"
        msg += "；远端已同步"
    return True, msg


def cmd_hook_install() -> tuple[bool, str]:
    """安装本克隆的钩子：git config core.hooksPath .githooks。"""
    missing = [h for h in HOOK_FILES if not (HOOKS_DIR / h).exists()]
    if missing:
        return False, f"钩子文件缺失：{', '.join(missing)}（仓库应内置 .githooks/）"
    if os.name != "nt":
        for h in HOOK_FILES:
            try:
                os.chmod(HOOKS_DIR / h, 0o755)
            except OSError:
                pass
    r = _git("config", "core.hooksPath", ".githooks")
    if r.returncode != 0:
        return False, f"写入 core.hooksPath 失败：{r.stderr.strip()}"
    return True, (f"已安装钩子：core.hooksPath=.githooks（{' / '.join(HOOK_FILES)}）\n"
                  f"卸载：python engine/tools/repo_sync.py hook-uninstall")


def cmd_hook_uninstall() -> tuple[bool, str]:
    r = _git("config", "--unset", "core.hooksPath")
    if r.returncode != 0:
        return False, f"卸载失败（可能本未安装）：{r.stderr.strip()}"
    return True, "已卸载钩子（core.hooksPath 已清除）"


# ---------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(description="多会话统一提交网关")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("lock"); sub.add_parser("unlock")
    p = sub.add_parser("sync"); p.add_argument("base", nargs="?", default=BASE_BRANCH)
    p = sub.add_parser("push"); p.add_argument("--allow-main", action="store_true")
    p = sub.add_parser("pr"); p.add_argument("--title", required=True); p.add_argument("--body", default="")
    p.add_argument("--queue", action="store_true", help="启用自动合并（合并队列入队）")
    p = sub.add_parser("run"); p.add_argument("--message", required=True)
    p.add_argument("--paths", nargs="+", required=True); p.add_argument("--allow-main", action="store_true")
    p.add_argument("--gate", action=argparse.BooleanOptionalAction, default=True,
                   help="提交前运行优化流程统一门禁（默认开启；--no-gate 跳过）")
    p.add_argument("--checks", nargs="*", help="追加自定义校验命令（每项为 shell 字符串）")
    p.add_argument("--allow-no-plan", action="store_true",
                   help="受管 task/* 分支无任务计划时仍允许 --gate（应急，需人工确认）")
    sub.add_parser("session", help="解析并打印当前会话标识（含来源）")
    p = sub.add_parser("branch", help="按规范自动追加会话标识建分支")
    p.add_argument("slug"); p.add_argument("--from", dest="from_ref", default=f"origin/{BASE_BRANCH}")
    sub.add_parser("branches", help="列出手头分支与登记信息")
    sub.add_parser("branch-audit", help="扫描存量分支，列出受管但命名违规项")
    p = sub.add_parser("branch-rename", help="改名并同步登记册")
    p.add_argument("old"); p.add_argument("new")
    p.add_argument("--remote", action="store_true", help="连同远端旧分支一起迁移")
    sub.add_parser("hook-install", help="安装 .githooks（core.hooksPath）")
    sub.add_parser("hook-uninstall", help="卸载 .githooks")
    g = sub.add_parser("guard"); g.add_argument("--stage", choices=["push", "commit"], default="push",
                                     help="push=pre-push 判定；commit=pre-commit 判定")
    args = ap.parse_args()

    try:
        if args.cmd == "status":
            br = current_branch()
            behind, ahead = divergence()
            rec = _read_lock()
            lock_state = "未锁定" if not rec else f"锁定中（{rec.get('holder')}）"
            print(f"分支：{br}\n相对 origin/{BASE_BRANCH}：远端领先 {behind} / 本地领先 {ahead}\n锁：{lock_state}")
            return 0
        if args.cmd == "lock":
            print(f"已获取锁：{acquire_lock('manual')}")
            return 0
        if args.cmd == "unlock":
            release_lock(); print("已释放锁"); return 0
        if args.cmd == "sync":
            ok, msg = sync(args.base); print(("[OK] " if ok else "[FAIL] ") + msg); return 0 if ok else 1
        if args.cmd == "push":
            ok, msg = push(allow_main=args.allow_main); print(("[OK] " if ok else "[FAIL] ") + msg)
            return 0 if ok else 1
        if args.cmd == "pr":
            ok, msg = create_pr(args.title, args.body, queue=args.queue)
            print(("[OK] " if ok else "[FAIL] ") + msg); return 0 if ok else 1
        if args.cmd == "run":
            checks = [c.split() for c in args.checks] if args.checks else None
            ok, msg = run(args.paths, args.message, allow_main=args.allow_main,
                          checks=checks, gate=args.gate,
                          allow_no_plan=args.allow_no_plan)
            print(("[OK] " if ok else "[FAIL] ") + msg); return 0 if ok else 1
        if args.cmd == "session":
            ok, msg = cmd_session(); print(("[OK] " if ok else "[FAIL] ") + msg); return 0 if ok else 1
        if args.cmd == "branch":
            ok, msg = cmd_branch(args.slug, args.from_ref)
            print(("[OK] " if ok else "[FAIL] ") + msg); return 0 if ok else 1
        if args.cmd == "branches":
            ok, msg = cmd_branches(); print(msg); return 0
        if args.cmd == "branch-audit":
            ok, msg = cmd_branch_audit(); print(("[OK] " if ok else "[违规] ") + msg); return 0 if ok else 1
        if args.cmd == "branch-rename":
            ok, msg = cmd_branch_rename(args.old, args.new, remote=args.remote)
            print(("[OK] " if ok else "[FAIL] ") + msg); return 0 if ok else 1
        if args.cmd == "hook-install":
            ok, msg = cmd_hook_install(); print(("[OK] " if ok else "[FAIL] ") + msg); return 0 if ok else 1
        if args.cmd == "hook-uninstall":
            ok, msg = cmd_hook_uninstall(); print(("[OK] " if ok else "[FAIL] ") + msg); return 0 if ok else 1
        if args.cmd == "guard":
            gl_blocked, gl_why = gitlab_remote_blocked()
            if gl_blocked:
                print(f"[拒绝] 本仓库禁止使用 GitLab 远端（用户硬性约束）。\n"
                      f"        依据：{gl_why}\n"
                      f"        请改用 GitHub（origin）或移除该远端后重试。",
                      file=sys.stderr)
                return 1
            blocked, why = guard_commit() if args.stage == "commit" else guard_push()
            if blocked:
                print(f"[拒绝] {'提交' if args.stage == 'commit' else '推送'}被阻断：\n"
                      f"        请按 {branch_naming.SPEC_ID} 整改后重试"
                      f"（见 engine/docs/branch-naming-and-lifecycle.md）。\n"
                      f"        依据：{why}",
                      file=sys.stderr)
                return 1
            print(f"[放行] {why}")
            return 0
    except SyncError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
