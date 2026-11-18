#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""main 首亲历史直推审计（GIT-HISTORY-AUDIT v1.0）。

单一事实源：engine/docs/multi-session-git-protocol.md（§二 三层隔离、§六 异常处理）。

解决的问题：本仓库为 GitHub **private 免费方案**，服务端分支保护不可用
（`gh api .../branches/main/protection` 返回 403），直推 `main` 只能靠客户端
钩子与 `repo_sync.py` 网关拦截。一旦有人在不安装钩子的克隆上强制推送，缺少
服务端检测。本工具在 CI 中扫描 `main` 的**首亲历史**，识别「非 PR 合并」的
直接提交，作为**补偿性检测**（discovery），不替代拦截。

判定（首亲提交）：
  - 合并提交（≥2 父）                     → 放行（PR 合并）
  - 提交信息含 PR 引用 `(#NN)`            → 放行（squash / rebase 合并）
  - 提交信息含 `由 CI 生成`               → 放行（CI 留痕）
  - SHA 命中历史白名单                     → 放行（协议生效前的历史直接提交）
  - 其余                                   → 违规（疑似直推）

本模块只做纯逻辑 + git 只读命令；CLI 入口为本文件。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field

SPEC_ID = "GIT-HISTORY-AUDIT v1.0"
BASE_BRANCH = "main"
DEFAULT_MAX_COMMITS = 200

# 协议生效前的历史直接提交（初始化 / 重置），首亲非合并且无 PR 引用，显式白名单
HISTORICAL_ALLOW = (
    "c5056e9b78d22e0bbdc8673d38bbd16075fc6de3",  # 初始化 tech-context-digest
    "c39cd305abc9fb0854153e19608ac749db226173",  # 重置历史日志为中性状态
)

PR_REF_RE = re.compile(r"\(#\d+\)")
CI_MARK = "由 CI 生成"


class AuditError(RuntimeError):
    """git 命令或参数错误。"""


@dataclass
class Commit:
    sha: str
    parents: list[str]
    subject: str
    author: str = ""

    @property
    def is_merge(self) -> bool:
        return len(self.parents) >= 2


@dataclass
class Violation:
    sha: str
    subject: str
    reason: str


@dataclass
class AuditResult:
    branch: str
    checked: int = 0
    allowed_merge: int = 0
    allowed_pr_ref: int = 0
    allowed_ci: int = 0
    allowed_historical: int = 0
    violations: list[Violation] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations

    def to_dict(self) -> dict:
        return {
            "spec": SPEC_ID,
            "branch": self.branch,
            "ok": self.ok,
            "checked": self.checked,
            "allowed": {
                "merge": self.allowed_merge,
                "pr_ref": self.allowed_pr_ref,
                "ci": self.allowed_ci,
                "historical": self.allowed_historical,
            },
            "violations": [
                {"sha": v.sha, "subject": v.subject, "reason": v.reason}
                for v in self.violations
            ],
        }


def _git(args: list[str], *, check: bool = True, cwd: str | None = None) -> str:
    proc = subprocess.run(
        ["git", *args], capture_output=True, text=True, encoding="utf-8", cwd=cwd
    )
    if check and proc.returncode != 0:
        raise AuditError(f"git {' '.join(args)} 失败：{proc.stderr.strip()}")
    return proc.stdout


def first_parent_commits(
    branch: str = BASE_BRANCH,
    max_commits: int = DEFAULT_MAX_COMMITS,
    repo: str | None = None,
) -> list[Commit]:
    """读取 branch 的首亲历史（最近 max_commits 条）。"""
    if max_commits <= 0:
        raise AuditError(f"max_commits 必须为正整数，收到 {max_commits}")
    out = _git(["rev-list", "--first-parent", "-n", str(max_commits), branch], cwd=repo)
    shas = [s for s in out.splitlines() if s.strip()]
    commits: list[Commit] = []
    for sha in shas:
        parents = _git(["rev-list", "--parents", "-n", "1", sha], cwd=repo).split()
        # rev-list --parents 输出：<sha> <parent...>
        parent_list = parents[1:] if len(parents) > 1 else []
        fmt = _git(["show", "-s", "--format=%s%n%an", sha], cwd=repo)
        lines = fmt.splitlines()
        subject = lines[0] if lines else ""
        author = lines[1] if len(lines) > 1 else ""
        commits.append(Commit(sha=sha, parents=parent_list, subject=subject, author=author))
    return commits


def audit(
    branch: str = BASE_BRANCH,
    max_commits: int = DEFAULT_MAX_COMMITS,
    allow_shas: tuple[str, ...] = HISTORICAL_ALLOW,
    repo: str | None = None,
) -> AuditResult:
    """审计首亲历史，返回结果（不抛异常，违规写入 violations）。"""
    result = AuditResult(branch=branch)
    allow = {s.lower() for s in allow_shas}
    for commit in first_parent_commits(branch, max_commits, repo):
        result.checked += 1
        if commit.is_merge:
            result.allowed_merge += 1
            continue
        if PR_REF_RE.search(commit.subject):
            result.allowed_pr_ref += 1
            continue
        if CI_MARK in commit.subject:
            result.allowed_ci += 1
            continue
        if commit.sha.lower() in allow:
            result.allowed_historical += 1
            continue
        result.violations.append(
            Violation(
                sha=commit.sha,
                subject=commit.subject,
                reason="首亲提交非合并、无 PR 引用、非 CI 留痕、不在历史白名单",
            )
        )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"main 首亲历史直推审计（{SPEC_ID}）")
    parser.add_argument("--branch", default=BASE_BRANCH)
    parser.add_argument("--repo", default=None, help="git 仓库路径（默认当前目录）")
    parser.add_argument("--max-commits", type=int, default=DEFAULT_MAX_COMMITS)
    parser.add_argument("--allow-sha", action="append", default=None,
                        help="追加历史白名单 SHA（可多次）")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args(argv)

    allow = HISTORICAL_ALLOW
    if args.allow_sha:
        allow = tuple(dict.fromkeys((*HISTORICAL_ALLOW, *args.allow_sha)))

    try:
        result = audit(args.branch, args.max_commits, allow, repo=args.repo)
    except AuditError as exc:
        print(f"[E] {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"[{'OK' if result.ok else 'E'}] {SPEC_ID} 分支={result.branch} "
              f"检查={result.checked} 合并={result.allowed_merge} "
              f"PR引用={result.allowed_pr_ref} CI={result.allowed_ci} "
              f"历史白名单={result.allowed_historical} 违规={len(result.violations)}")
        for v in result.violations:
            print(f"  - {v.sha[:10]} {v.subject} ← {v.reason}")
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
