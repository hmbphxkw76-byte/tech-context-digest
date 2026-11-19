#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""分支命名规范与登记册（BRANCH-NAMING-SPEC v1.0）。

单一事实源：engine/docs/branch-naming-and-lifecycle.md。

解决的问题：多个 Agent 会话 / CI 共用同一仓库时，分支名（如 task/<slug>）无法回答
「这条分支属于哪个会话、对应哪件任务」，事后无法把分支还原到任务上下文。

规范要点（详见文档）：
  - 受管分支：task/*（开发分支）。模板 task/<slug>-<session8>，会话标识**后置**；
  - 系统分支：ci/*、main 豁免（CI 用固定分支名，不参与会话标识）；
  - session8 = 会话标识归一化（小写、去连字符）后的前 8 位十六进制；
  - 会话标识解析链：TECH_CTX_SESSION_ID → CATPAW_CONVERSATION_ID → X_AI_SESSIONID
    → git config techctx.sessionId；全部缺失即**拒绝**自动建分支（杜绝不可追溯分支）。

登记册：engine/tools/branch_registry.json（分支 → 会话 / 任务 的映射台账）。
本模块只做纯逻辑与文件读写，不触发网络；CLI 入口在 repo_sync.py。
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

from _common import ROOT

SPEC_ID = "BRANCH-NAMING-SPEC v1.0"
BASE_BRANCH = "main"
MANAGED_KIND = "task"
# 系统 / 平台分支：不参与会话标识校验（CI 用固定分支名，钩子与 CI 自身不能被自己拦死）
EXEMPT_KINDS = ("ci",)

SESSION_ENV_KEYS = ("TECH_CTX_SESSION_ID", "CATPAW_CONVERSATION_ID", "X_AI_SESSIONID")
SESSION_GIT_KEY = "techctx.sessionId"
SESSION_MIN_LEN = 8
SESSION_MAX_LEN = 64
SHORT_LEN = 8

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SESSION_RE = re.compile(r"^[0-9a-f]{8,64}$")
TASK_BRANCH_RE = re.compile(r"^task/[a-z0-9]+(?:-[a-z0-9]+)*-[0-9a-f]{8}$")

REGISTRY_PATH = ROOT / "engine" / "tools" / "branch_registry.json"
REGISTRY_SCHEMA = 1


class BranchNamingError(Exception):
    """会话标识无法解析或分支命名不合规。"""


# ---------------------------------------------------------------- 会话标识

def normalize_session(raw: str) -> str:
    """归一化会话标识：小写、去连字符，限定为 8–64 位十六进制。

    接受标准 UUID（如 5f37e90d-eb60-4247-988a-9207d64048f5）或纯 hex 串。
    """
    s = (raw or "").strip().lower().replace("-", "")
    if not SESSION_RE.match(s):
        raise BranchNamingError(
            f"会话标识非法：{raw!r}（需为 8–64 位十六进制，可含连字符，"
            f"如 CATPAW_CONVERSATION_ID 的 UUID）"
        )
    return s


def session_short(full: str) -> str:
    """取会话标识前 8 位作为分支名内嵌短码。"""
    return normalize_session(full)[:SHORT_LEN]


def _git_config_get(key: str) -> str | None:
    try:
        r = subprocess.run(["git", "config", "--get", key], cwd=ROOT,
                           capture_output=True, text=True)
    except OSError:
        return None
    if r.returncode != 0:
        return None
    return r.stdout.strip() or None


def resolve_session(env: dict | None = None, use_git_config: bool = True) -> tuple[str, str]:
    """按优先级解析当前会话标识，返回 (完整标识, 来源)。

    来源取值：env:<变量名> / git:<配置键>。全部缺失抛 BranchNamingError。
    """
    env_map: dict = dict(os.environ) if env is None else env
    for key in SESSION_ENV_KEYS:
        val = (env_map.get(key) or "").strip()
        if not val:
            continue
        try:
            return normalize_session(val), f"env:{key}"
        except BranchNamingError as e:
            # 显式设置的值非法 → 直接失败，避免悄悄换用别的来源产生歧义
            raise BranchNamingError(f"{key} 取值非法：{e}") from e
    if use_git_config:
        val = _git_config_get(SESSION_GIT_KEY)
        if val:
            try:
                return normalize_session(val), f"git:{SESSION_GIT_KEY}"
            except BranchNamingError as e:
                raise BranchNamingError(f"git config {SESSION_GIT_KEY} 取值非法：{e}") from e
    raise BranchNamingError(
        "未解析到会话标识。请设置其一："
        + "、".join(SESSION_ENV_KEYS)
        + f"，或 `git config {SESSION_GIT_KEY} <会话标识>`"
        + "（见 engine/docs/branch-naming-and-lifecycle.md）"
    )


# ---------------------------------------------------------------- 分支命名

def is_managed(branch: str) -> bool:
    """是否为受管开发分支（仅 task/*）。"""
    return branch.startswith(f"{MANAGED_KIND}/")


def is_exempt(branch: str) -> bool:
    """是否为豁免分支（main 与 ci/* 等系统分支）。"""
    if branch == BASE_BRANCH:
        return True
    return any(branch.startswith(f"{k}/") for k in EXEMPT_KINDS)


def validate_slug(slug: str) -> tuple[bool, str]:
    if not slug:
        return False, "slug 为空"
    if not SLUG_RE.match(slug):
        return False, (f"slug {slug!r} 需为 kebab-case（小写字母 / 数字 / 单连字符，"
                       f"如 ci-permissions-fix）")
    return True, ""


def build_branch(slug: str, session_full: str) -> str:
    """按规范生成受管分支名：task/<slug>-<session8>。"""
    ok, why = validate_slug(slug)
    if not ok:
        raise BranchNamingError(why)
    return f"{MANAGED_KIND}/{slug}-{session_short(session_full)}"


def parse_branch(branch: str) -> dict | None:
    """解析受管分支名，返回 {"slug", "session_short"}；不合规返回 None。"""
    if not is_managed(branch):
        return None
    if not TASK_BRANCH_RE.match(branch):
        return None
    body = branch[len(f"{MANAGED_KIND}/"):]
    slug, _, short = body.rpartition("-")
    return {"slug": slug, "session_short": short}


def validate_managed(branch: str) -> tuple[bool, str]:
    """校验受管分支名是否合规（含会话标识是否存在且格式正确）。"""
    if not is_managed(branch):
        return True, f"{branch} 非受管分支（仅 {MANAGED_KIND}/* 纳管）"
    body = branch[len(f"{MANAGED_KIND}/"):]
    ok, why = validate_slug(body)
    if not ok:
        return False, (f"受管分支 {branch} 不合规：{why}；"
                       f"正确模板：{MANAGED_KIND}/<slug>-<session8>")
    if not TASK_BRANCH_RE.match(branch):
        short = body.rpartition("-")[2]
        if not re.match(r"^[0-9a-f]{8}$", short):
            return False, (f"受管分支 {branch} 缺少会话标识后缀（应为 -<session8>，"
                           f"8 位十六进制）；可用 `repo_sync.py branch-rename` 补全")
        return False, (f"受管分支 {branch} 不合规：完整模板 {TASK_BRANCH_RE.pattern}")
    return True, ""


def expected_session_short(branch: str) -> str | None:
    """从受管分支名取出会话短码；无法解析返回 None。"""
    parsed = parse_branch(branch)
    return parsed["session_short"] if parsed else None


# ---------------------------------------------------------------- 登记册

def load_registry(path: Path | None = None) -> dict:
    """读取登记册；不存在或损坏时返回空登记册（不抛错，便于首建）。"""
    p = path or REGISTRY_PATH
    if not p.exists():
        return {"schema": REGISTRY_SCHEMA, "spec": SPEC_ID, "branches": {}}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"schema": REGISTRY_SCHEMA, "spec": SPEC_ID, "branches": {}}
    data.setdefault("schema", REGISTRY_SCHEMA)
    data.setdefault("spec", SPEC_ID)
    data.setdefault("branches", {})
    return data


def save_registry(reg: dict, path: Path | None = None) -> Path:
    """原子写入登记册（确定性格式：排序键、2 空格缩进、UTF-8、尾换行）。"""
    p = path or REGISTRY_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(
        json.dumps(reg, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp.replace(p)
    return p


def register_branch(reg: dict, branch: str, session_full: str,
                    task: str = "", note: str = "") -> dict:
    """写入 / 更新一条分支登记。返回更新后的登记册。"""
    parsed = parse_branch(branch)
    if parsed is None:
        raise BranchNamingError(f"无法登记非受管分支：{branch}")
    reg["branches"][branch] = {
        "session": normalize_session(session_full),
        "session_short": parsed["session_short"],
        "slug": parsed["slug"],
        "task": task or parsed["slug"],
        "note": note,
    }
    return reg


def unregister_branch(reg: dict, branch: str) -> dict:
    reg["branches"].pop(branch, None)
    return reg


def entry_for(reg: dict, branch: str) -> dict | None:
    return reg["branches"].get(branch)


def session_ledger(reg: dict) -> dict:
    """按会话短码归并，便于从会话反查分支。"""
    out: dict[str, list[str]] = {}
    for branch, rec in sorted(reg["branches"].items()):
        out.setdefault(rec.get("session_short", ""), []).append(branch)
    return out


# ---------------------------------------------------------------- 存量梳理

def scan_branches(remote: bool = True) -> list[str]:
    """列出手头可见的分支名（本地 heads + 远端 origin/*，可去重排序）。"""
    names: set[str] = set()
    r = subprocess.run(["git", "for-each-ref", "--format=%(refname:short)",
                        "refs/heads"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode == 0:
        names.update(n for n in r.stdout.split() if n)
    if remote:
        r = subprocess.run(["git", "for-each-ref", "--format=%(refname:short)",
                            "refs/remotes/origin"], cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            # 只取 origin/<branch>；排除符号引用 origin/HEAD 与裸 origin（无斜杠）
            names.update(n[len("origin/"):] for n in r.stdout.split()
                         if n.startswith("origin/") and n != "origin/HEAD")
    return sorted(names)


def audit_branches(branches: list[str] | None = None) -> tuple[list[str], list[str], list[str]]:
    """把分支分为 (合规, 违规, 豁免)。违规 = 受管但命名不合规。"""
    ok: list[str] = []
    bad: list[str] = []
    exempt: list[str] = []
    for name in (branches if branches is not None else scan_branches()):
        if is_managed(name):
            (ok if validate_managed(name)[0] else bad).append(name)
        else:
            exempt.append(name)
    return ok, bad, exempt
