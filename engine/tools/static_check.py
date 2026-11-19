#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""静态检查适配层（ruff / mypy）→ 统一门禁退出码 + baseline 只拦新增。

《方案》Phase 3.1 / 11-19 方案 P1-5：把 ruff / mypy 纳入 `optimization_gate`，
并以**显式 baseline** 收口历史债务——baseline 内遗留计 `[W]`（不阻断），
baseline 之外的新增计 `[E]`（阻断），避免「门禁全绿」公信力被稀释。

退出码（CLI / 门禁口径）：
- 0：无发现；
- 2：有发现但均在 baseline 额度内（非阻断警告）；
- 1：出现 baseline 之外的新增发现（阻断），或工具执行 / 配置错误。

baseline 口径：按 `(path, code)` **计数**（不看行号，避免代码移动导致漂移）。
`current > baseline` 即视为新增。baseline 文件：
`engine/quality/lint-baseline.json`。

`ruff()` / `mypy()` 为**旧口径包装**（发现即 2，不比对 baseline），供既有测试与
临时调用；门禁统一走 `main()`（CLI）。工具未安装时返回 2（警告），避免阻断未
安装静态检查的本地环境；CI 由 `requirements.txt` 保证安装。

用法：
    python engine/tools/static_check.py ruff
    python engine/tools/static_check.py mypy
    python engine/tools/static_check.py ruff --update-baseline
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = ROOT / "engine" / "quality" / "lint-baseline.json"
BASELINE_SCHEMA = "1.0"
MYPY_LINE_RE = re.compile(r"^(?P<path>[^:]+):\d+: error: .* \[(?P<code>[A-Za-z0-9_-]+)\]$")


def _norm(path: str) -> str:
    return str(path).replace("\\", "/")


def _emit(out: str) -> None:
    if out:
        print(out, end="")


def _map(code: int, out: str) -> int:
    """旧口径：ruff / mypy 的发现退出码 1 → 门禁警告 2；0 → 0；其余 → 1。"""
    _emit(out)
    if code == 0:
        return 0
    if code == 1:
        return 2
    return 1


# ---------------------------------------------------------------- 执行

def _run_ruff(json_out: bool) -> tuple[int, str, str] | None:
    """-> (returncode, stdout, stderr)；ruff 未安装返回 None。"""
    exe = shutil.which("ruff")
    if exe is None:
        return None
    cmd = [exe, "check", "engine"] + (["--output-format=json"] if json_out else [])
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def _run_mypy() -> tuple[int, str, str]:
    r = subprocess.run([sys.executable, "-m", "mypy", "engine/tools",
                        "--ignore-missing-imports"],
                       cwd=ROOT, capture_output=True, text=True)
    return r.returncode, (r.stdout or ""), (r.stderr or "")


# ---------------------------------------------------------------- 旧口径包装

def ruff() -> int:
    res = _run_ruff(False)
    if res is None:
        print("[W] 未安装 ruff，跳过（pip install ruff）")
        return 2
    code, out, err = res
    return _map(code, out + err)


def mypy() -> int:
    code, out, err = _run_mypy()
    if "No module named mypy" in (out + err):
        print("[W] 未安装 mypy，跳过（pip install mypy）")
        return 2
    return _map(code, out + err)


# ---------------------------------------------------------------- 发现提取

def ruff_violations() -> list[tuple[str, str]] | None:
    """-> [(path, code)]（baseline 口径）；ruff 未安装返回 None。"""
    res = _run_ruff(True)
    if res is None:
        return None
    code, out, err = res
    if code not in (0, 1):
        raise RuntimeError(f"ruff 执行失败：{(err or out).strip()}")
    data = json.loads(out or "[]")
    return [(_norm(v.get("filename", "")), str(v.get("code") or "?"))
            for v in data if isinstance(v, dict)]


def mypy_violations() -> list[tuple[str, str]] | None:
    """-> [(path, code)]（baseline 口径）；mypy 未安装返回 None。"""
    _code, out, err = _run_mypy()
    text = out + err
    if "No module named mypy" in text:
        return None
    pairs: list[tuple[str, str]] = []
    for line in text.splitlines():
        m = MYPY_LINE_RE.match(line.strip())
        if m:
            pairs.append((_norm(m.group("path")), m.group("code")))
    return pairs


# ---------------------------------------------------------------- baseline

def _counts(pairs: list[tuple[str, str]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for path, code in pairs:
        per = out.setdefault(path, {})
        per[code] = per.get(code, 0) + 1
    return out


def _total(counts: dict[str, dict[str, int]]) -> int:
    return sum(sum(v.values()) for v in counts.values())


def _new_items(cur: dict[str, dict[str, int]],
               base: dict[str, dict[str, int]]) -> list[str]:
    """baseline 之外的新增项（current > baseline 的差额）。"""
    out: list[str] = []
    for path in sorted(set(cur) | set(base)):
        codes = set(cur.get(path, {})) | set(base.get(path, {}))
        for code in sorted(codes):
            c = cur.get(path, {}).get(code, 0)
            b = base.get(path, {}).get(code, 0)
            if c > b:
                out.append(f"{path}: {code} baseline={b} 当前={c}（新增 {c - b}）")
    return out


def _load_baseline() -> dict:
    if not BASELINE_PATH.exists():
        return {"schema_version": BASELINE_SCHEMA, "ruff": {}, "mypy": {}}
    data = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    return {"schema_version": BASELINE_SCHEMA,
            "ruff": data.get("ruff", {}) or {}, "mypy": data.get("mypy", {}) or {}}


def _save_baseline(base: dict) -> None:
    BASELINE_PATH.write_text(
        json.dumps({"schema_version": BASELINE_SCHEMA,
                    "policy": "只拦新增：按 (path, code) 计数，current > baseline 即新增；"
                             "baseline 内遗留计 [W]，新增计 [E]。",
                    "ruff": base["ruff"], "mypy": base["mypy"]},
                   ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="静态检查适配层（ruff / mypy）+ baseline 只拦新增")
    ap.add_argument("tool", choices=["ruff", "mypy"])
    ap.add_argument("--update-baseline", action="store_true",
                    help="以当前实测刷新该工具的 baseline（不比对）")
    args = ap.parse_args()

    base = _load_baseline()
    try:
        pairs = ruff_violations() if args.tool == "ruff" else mypy_violations()
    except (RuntimeError, json.JSONDecodeError) as e:
        print(f"[E] {args.tool}：{e}")
        return 1
    if pairs is None:
        print(f"[W] 未安装 {args.tool}，跳过（pip install {args.tool}）")
        return 2

    cur = _counts(pairs)
    if args.update_baseline:
        base[args.tool] = cur
        _save_baseline(base)
        print(f"[OK] baseline 已更新：{BASELINE_PATH.relative_to(ROOT).as_posix()}"
              f"（{args.tool} {_total(cur)} 项）")
        return 0

    ref = base.get(args.tool, {}) or {}
    new = _new_items(cur, ref)
    print(f"[{args.tool}] 当前 {_total(cur)} 项 / baseline {_total(ref)} 项 / 新增 {len(new)} 项")
    for item in new:
        print(f"  [NEW] {item}")
    if new:
        print(f"[E] {args.tool}：{len(new)} 类发现超出 baseline（新增 {_total(cur) - _total(ref)} 项）")
        return 1
    if cur:
        print(f"[W] {args.tool}：{_total(cur)} 项均在 baseline 额度内（不阻断；只拦新增）")
        return 2
    print(f"[OK] {args.tool}：无发现")
    return 0


if __name__ == "__main__":
    sys.exit(main())
