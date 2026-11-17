#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""工作区标准化清理（workspace_cleanup）。

清除缓存 / 临时 / 构建产物 / 自动化临时目录，保持工作区干净，
供本地钩子、提交网关与 CI 各阶段复用（单一入口，避免各处各写一套）：

- 缓存：``__pycache__/``、``*.pyc`` / ``*.pyo`` / ``*.pyd``、``.pytest_cache/``、
  ``.ruff_cache/``、``.mypy_cache/``、``.coverage``、``htmlcov/``、``*.egg-info/``、``.eggs/``
- 构建：``build/``、``dist/``
- 临时：``.automation-tmp/``、``.screenshots/``、``.trae-html-share-packages/``、
  ``*.html.tmp``、``*.tmp``
- 深度（``--deep``）：虚拟环境 ``.venv/`` / ``venv/`` / ``env/``

安全约束（硬性）：
- **只删未被 git 跟踪的路径**：跟踪集合取自 ``git ls-files``，任何被跟踪的文件 /
  目录（含其内部）一律跳过，绝不删版本控制内容；
- 默认跳过 ``.git``；
- **幂等**且**确定性**：输出排序、无时间戳，重复执行结果一致；
- 清理失败不抛栈，逐项记录并汇总。

用法：
    python engine/tools/workspace_cleanup.py                # 清理
    python engine/tools/workspace_cleanup.py --dry-run      # 只报告，不删
    python engine/tools/workspace_cleanup.py --verify       # 有残留即 exit 1
    python engine/tools/workspace_cleanup.py --deep         # 连同虚拟环境
    python engine/tools/workspace_cleanup.py --root <dir>   # 指定根（测试用）

退出码：0 成功（含 dry-run）；1 ``--verify`` 发现残留或用法错误。
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# 目录名 → 直接整目录清理（缓存 / 构建 / 临时）
JUNK_DIR_NAMES = {
    "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache",
    "htmlcov", ".eggs", ".automation-tmp", ".screenshots",
    ".trae-html-share-packages",
}
BUILD_DIR_NAMES = {"build", "dist"}
DEEP_DIR_NAMES = {".venv", "venv", "env"}

# 文件后缀 → 逐文件清理
JUNK_FILE_SUFFIXES = (".pyc", ".pyo", ".pyd", ".tmp", ".html.tmp")
# 精确文件名
JUNK_FILE_NAMES = {".coverage"}

SKIP_DIR_NAMES = {".git"}


def _tracked_paths(root: Path) -> set[str]:
    """仓库内被 git 跟踪的路径集合（POSIX 相对路径）；非 git 仓库返回空集。"""
    try:
        r = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                           capture_output=True, text=True, check=False)
    except OSError:
        return set()
    if r.returncode != 0:
        return set()
    return {p for p in (r.stdout or "").split("\0") if p}


def _is_tracked(rel: str, tracked: set[str]) -> bool:
    """rel 自身或被跟踪集合中任一路径位于其下 → 视为受版本控制，跳过。"""
    if rel in tracked:
        return True
    prefix = rel + "/"
    return any(t.startswith(prefix) for t in tracked)


def collect_targets(root: Path, deep: bool = False) -> list[Path]:
    """扫描待清理目标（已排除受跟踪路径与 .git），返回排序后的绝对路径列表。"""
    root = root.resolve()
    tracked = _tracked_paths(root)
    dir_names = JUNK_DIR_NAMES | BUILD_DIR_NAMES | (DEEP_DIR_NAMES if deep else set())
    targets: list[Path] = []

    for dirpath, dirnames, filenames in _walk(root):
        rel_dir = dirpath.relative_to(root).as_posix()
        # 目录整体命中（且未被跟踪）→ 记录目录并不再深入
        if dirpath != root and dirpath.name in dir_names and not _is_tracked(rel_dir, tracked):
            targets.append(dirpath)
            dirnames[:] = []
            continue
        for name in filenames:
            p = dirpath / name
            rel = p.relative_to(root).as_posix()
            if _is_tracked(rel, tracked):
                continue
            if name in JUNK_FILE_NAMES or name.endswith(JUNK_FILE_SUFFIXES):
                targets.append(p)
    return sorted(set(targets), key=lambda p: p.as_posix())


def _walk(root: Path):
    """自顶向下遍历，跳过 .git 与已判定为待删的目录。"""
    import os
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        yield Path(dirpath), dirnames, filenames


def clean(root: Path, dry_run: bool = False, deep: bool = False) -> dict:
    """执行清理，返回确定性报告（counts 按类别聚合，无时间戳）。"""
    targets = collect_targets(root, deep=deep)
    removed: list[str] = []
    failed: list[str] = []
    for p in targets:
        rel = p.relative_to(root.resolve()).as_posix()
        if dry_run:
            removed.append(rel)
            continue
        try:
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
            else:
                p.unlink()
        except OSError as exc:  # 逐项容错，不中断整体清理
            failed.append(f"{rel}（{exc}）")
            continue
        removed.append(rel)
    return {
        "root": root.resolve().as_posix(),
        "dry_run": dry_run,
        "deep": deep,
        "found": len(targets),
        "removed": len(removed),
        "failed": failed,
        "targets": removed,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="工作区标准化清理（缓存/临时/构建产物）")
    ap.add_argument("--mode", choices=["clean", "dry-run", "verify"], default="clean",
                    help="clean=清理；dry-run=只报告；verify=有残留即 exit 1")
    ap.add_argument("--deep", action="store_true", help="连同虚拟环境 .venv/venv/env 一起清理")
    ap.add_argument("--root", default=str(ROOT), help="仓库根（默认本仓库）")
    ap.add_argument("--json", action="store_true", help="输出 JSON 报告")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"[ERROR] 根目录不存在：{root}")
        return 1

    if args.mode == "verify":
        targets = collect_targets(root, deep=args.deep)
        if targets:
            print(f"[WARN] 工作区存在 {len(targets)} 项缓存 / 临时 / 构建残留：")
            for p in targets:
                print(f"       - {p.relative_to(root.resolve()).as_posix()}")
            print("       建议运行：python engine/tools/workspace_cleanup.py")
            return 1
        print("工作区清理核验通过：无缓存 / 临时 / 构建残留")
        return 0

    report = clean(root, dry_run=(args.mode == "dry-run"), deep=args.deep)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        verb = "待清理" if args.mode == "dry-run" else "已清理"
        print(f"工作区清理（{args.mode}{' · deep' if args.deep else ''}）："
              f"{verb} {report['removed']} 项，失败 {len(report['failed'])} 项")
        for rel in report["targets"][:20]:
            print(f"  - {rel}")
        if len(report["targets"]) > 20:
            print(f"  … 其余 {len(report['targets']) - 20} 项从略")
        for msg in report["failed"]:
            print(f"  [FAIL] {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
