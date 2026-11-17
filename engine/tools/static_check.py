#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""静态检查适配层（ruff / mypy）→ 统一门禁退出码。

《方案》Phase 3.1：把 ruff / mypy 纳入 `optimization_gate`（默认 `[W]`，稳定后评 `[E]`）。
本模块**只适配退出码**，不重写任何检查规则：

- exit 0：无发现；
- exit 2：有非阻断发现（警告，由 `optimization_gate` 的 `warn_ok` 处理）；
- exit 1：工具执行错误 / 配置错误。

工具未安装时返回 2（警告），避免阻断未安装静态检查的本地环境；CI 由
`requirements.txt` 保证安装。

用法：
    python engine/tools/static_check.py ruff
    python engine/tools/static_check.py mypy
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _emit(out: str) -> None:
    if out:
        print(out, end="")


def _map(code: int, out: str) -> int:
    _emit(out)
    if code == 0:
        return 0
    if code == 1:
        # ruff / mypy 的发现退出码为 1 → 映射为门禁警告（2）
        return 2
    return 1


def ruff() -> int:
    exe = shutil.which("ruff")
    if exe is None:
        print("[W] 未安装 ruff，跳过（pip install ruff）")
        return 2
    r = subprocess.run([exe, "check", "engine"], cwd=ROOT,
                       capture_output=True, text=True)
    return _map(r.returncode, (r.stdout or "") + (r.stderr or ""))


def mypy() -> int:
    r = subprocess.run([sys.executable, "-m", "mypy", "engine/tools",
                        "--ignore-missing-imports"],
                       cwd=ROOT, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0 and "No module named mypy" in out:
        print("[W] 未安装 mypy，跳过（pip install mypy）")
        return 2
    return _map(r.returncode, out)


def main() -> int:
    ap = argparse.ArgumentParser(description="静态检查适配层（ruff / mypy）")
    ap.add_argument("tool", choices=["ruff", "mypy"])
    args = ap.parse_args()
    return {"ruff": ruff, "mypy": mypy}[args.tool]()


if __name__ == "__main__":
    sys.exit(main())
