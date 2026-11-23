# -*- coding: utf-8 -*-
"""生成物重生成比对自检（REGEN-DRIFT-CHECK v1.0）。

背景：各类索引产物（根索引 INDEX.md 与词库索引 INDEX.md）这类「机器生成、应可由生成器重放」的产物，
曾在没有任何门禁或 CI 负责重生成的情况下**静默漂移**（词条数与词条库不符）。
本检查把「重生成后是否与已提交版本一致」变成确定性比对。

设计要点：
- **非破坏性**：先保存已提交字节，重跑生成器，比对后无条件还原原始字节；
- **可重放**：带墙钟戳的产物按行归一（剔除时间戳行），其余必须逐字节一致；
- **分组复用**：同一生成器产出的多个产物只跑一次。

接入：`optimization_gate.py` 的 `regen_drift` 项（阻断级）。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):  # 直接执行时把 engine/tools 加入 import 路径
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT  # noqa: E402


@dataclass(frozen=True)
class _Group:
    """一组由同一生成命令产出的产物。"""

    outputs: tuple[str, ...]
    argv: tuple[str, ...]
    marker: str = ""  # 非空则把该标记后的墙钟戳值归一为占位符


# 仅纳入**无其他门禁覆盖**的生成物：汇总页的两个页面已由 `hub` 项校验，
# 发布指纹与发布日历另有 `fingerprint` / `calendar_check`，此处均不重复。
# 留白处即本检查的价值：防「无人重生成」的静默漂移。
_GROUPS: tuple[_Group, ...] = (
    _Group(
        outputs=("INDEX.md",),
        argv=("build_index.py",),
        marker="最近生成",
    ),
    _Group(
        outputs=("engine/vocabulary/INDEX.md",),
        argv=("engine/vocabulary/script/vocab_tool.py", "index"),
        marker="生成时间",
    ),
)


_TS_VALUE = (
    r"\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?)?"
)


def _normalize(text: str | None, marker: str) -> str:
    """归一化：None 视为不存在；把墙钟戳值替换为占位符。

    两处生成器都把时间戳嵌在引用行内，且格式不同：
    `> 最近生成：2026-11-23 11:03 UTC（…）` / `…生成时间：2026-11-24T06:24:14`，
    故不能整行剔除，只把戳值归一。
    """
    if text is None:
        return ""
    if not marker:
        return text
    pat = re.compile(r"(" + re.escape(marker) + r"\s*[：:])\s*" + _TS_VALUE)
    return pat.sub(r"\1<TS>", text)


def _read(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def _restore(path: Path, before: str | None) -> None:
    """无条件还原到检查前状态（非破坏性）。"""
    if before is None:
        path.unlink(missing_ok=True)
    else:
        path.write_text(before, encoding="utf-8")


def check(verbose: bool = False) -> list[str]:
    """重放生成器并比对；返回漂移条目（空 = 无漂移）。"""
    drift: list[str] = []
    for grp in _GROUPS:
        paths = [ROOT / o for o in grp.outputs]
        before = {p: _read(p) for p in paths}
        proc = subprocess.run(
            [sys.executable, *grp.argv],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        if verbose and proc.stdout.strip():
            print(proc.stdout.strip())
        if verbose and proc.returncode:
            print(f"[regen] {' '.join(grp.argv)} 退出码 {proc.returncode}", file=sys.stderr)
        for p in paths:
            after = _read(p)
            if _normalize(before[p], grp.marker) != _normalize(after, grp.marker):
                drift.append(
                    f"{p.relative_to(ROOT).as_posix()} 重生成后与已提交版本不一致"
                    "（生成物已漂移，请运行对应生成器并提交）"
                )
            _restore(p, before[p])
    return drift


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="生成物重生成比对自检")
    ap.add_argument("--verbose", action="store_true", help="打印生成器输出")
    args = ap.parse_args(argv)

    drift = check(verbose=args.verbose)
    if drift:
        print(f"[E] 生成物重生成比对自检失败（{len(drift)} 项）：")
        for d in drift:
            print(f"  - {d}")
        return 1
    print("[OK] 生成物重生成比对自检通过：全部产物与生成器一致")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
