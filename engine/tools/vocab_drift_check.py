#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""词库漂移门禁（VOCAB-DRIFT-CHECK v1.0）。

词库是「消除信息差」的基础设施：术语不统一，跨报告检索与对齐成本持续上升。
本门禁把词库的三类机械完整性检查接入统一门禁（optimization_gate）：

  VD-01 同步区块完整（[E]）：含 `VOCAB-SYNC:BEGIN` 的目标文件，BEGIN / END 必须成对；
  VD-02 主题词库非空（[W]）：`layout.json` 已注册主题的 `terms.md` 至少有 1 条词条；
  VD-03 规范形一致（[W]）：提示词声称的「词库规范形（如「X」）」须在对应主题词库命中
       （词条或别名）——防「提示词层与词库两份维护」漂移。

退出码：0 通过；1 存在 [E]；2 仅 [W]。

用法：
    python engine/tools/vocab_drift_check.py
    python engine/tools/vocab_drift_check.py --quiet
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, load_layout  # noqa: E402

VOCAB_ROOT = ROOT / "engine" / "vocabulary"
TERMS_DIR = VOCAB_ROOT / "data"
PROMPTS_DIR = VOCAB_ROOT / "prompts"

_BEGIN_RE = re.compile(r"<!--\s*VOCAB-SYNC:BEGIN\b[^>]*-->")
_END_RE = re.compile(r"<!--\s*VOCAB-SYNC:END\b[^>]*-->")
# 术语表行：| ECO-001 | 词条 | 别名;别名 | ...
_ROW_RE = re.compile(r"^\|\s*([A-Z]+-\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|")
# 提示词中的规范形声明：规范形（如「A」「B」「C」）
_CANON_RE = re.compile(r"规范形[^）\n]*?（?如?([^）\n]*)）?")
_QUOTED_RE = re.compile(r"[「『]([^」』]+)[」』]")

# 规则级别
_ERROR_RULES = {"VD-01"}
_WARN_RULES = {"VD-02", "VD-03"}


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", (s or "").strip()).lower()


def load_terms(theme: str) -> tuple[list[str], int]:
    """-> (词库全部词形 [词条 + 别名], 词条数)。

    词库在 `engine/vocabulary/data/<theme>/terms.md`；词条/别名任一列为空则跳过该行。
    """
    path = TERMS_DIR / theme / "terms.md"
    if not path.exists():
        return [], 0
    forms: list[str] = []
    n_terms = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = _ROW_RE.match(line.strip())
        if not m:
            continue
        term = m.group(2).strip()
        aliases = [a.strip() for a in re.split(r"[;；]", m.group(3)) if a.strip()]
        if not term:
            continue
        n_terms += 1
        forms.append(term)
        forms.extend(aliases)
    return forms, n_terms


def iter_sync_targets() -> list[Path]:
    """含 VOCAB-SYNC 区块的目标文件（content 业务配置 + 词库自身文档）。"""
    out: list[Path] = []
    for base in (ROOT / "content", VOCAB_ROOT):
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*.md")):
            if "sync-backups" in p.parts:
                continue
            try:
                if _BEGIN_RE.search(p.read_text(encoding="utf-8", errors="replace")):
                    out.append(p)
            except OSError:
                continue
    return out


def pair_issue(text: str) -> str | None:
    """单文件同步区块配对结论：BEGIN / END 数量不等时返回说明，否则 None。"""
    n_b, n_e = len(_BEGIN_RE.findall(text)), len(_END_RE.findall(text))
    return f"VOCAB-SYNC BEGIN {n_b} / END {n_e} 不成对" if n_b != n_e else None


def check_sync_blocks() -> list[tuple[str, str]]:
    """VD-01：BEGIN / END 成对。"""
    out: list[tuple[str, str]] = []
    for p in iter_sync_targets():
        issue = pair_issue(p.read_text(encoding="utf-8", errors="replace"))
        if issue:
            out.append(("VD-01", f"{p.relative_to(ROOT).as_posix()}：{issue}"))
    return out


def check_theme_terms() -> list[tuple[str, str]]:
    """VD-02：已注册主题词库非空。"""
    out: list[tuple[str, str]] = []
    for theme in sorted(load_layout().themes):
        _forms, n_terms = load_terms(theme)
        if n_terms == 0:
            out.append(("VD-02", f"主题 {theme} 词库为空（{TERMS_DIR / theme / 'terms.md'} 无词条）"))
    return out


def check_canonical_forms() -> list[tuple[str, str]]:
    """VD-03：提示词声称的规范形须在对应主题词库命中。"""
    out: list[tuple[str, str]] = []
    if not PROMPTS_DIR.is_dir():
        return out
    for theme_dir in sorted(p for p in PROMPTS_DIR.iterdir() if p.is_dir()):
        forms, n_terms = load_terms(theme_dir.name)
        if n_terms == 0:
            continue  # 空词库主题由 VD-02 负责，避免重复告警
        vocabulary = {_norm(f) for f in forms}
        for f in sorted(theme_dir.glob("prompt-*.md")):
            text = f.read_text(encoding="utf-8", errors="replace")
            for m in _CANON_RE.finditer(text):
                for term in _QUOTED_RE.findall(m.group(1)):
                    if _norm(term) not in vocabulary:
                        out.append(("VD-03", f"{f.relative_to(ROOT).as_posix()}：规范形「{term}」"
                                            f"未在主题 {theme_dir.name} 词库中命中"))
    return out


def run() -> tuple[int, int, list[str]]:
    errors = warnings = 0
    lines: list[str] = []
    for rule, msg in check_sync_blocks() + check_theme_terms() + check_canonical_forms():
        level = "E" if rule in _ERROR_RULES else "W"
        if level == "E":
            errors += 1
        else:
            warnings += 1
        lines.append(f"[{level}] {rule} {msg}")
    return errors, warnings, lines


def main() -> int:
    ap = argparse.ArgumentParser(description="词库漂移门禁")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    errors, warnings, lines = run()
    if not args.quiet:
        for line in lines:
            print(line)
    if errors:
        print(f"词库漂移门禁失败：{errors} 项错误，{warnings} 项警告")
        return 1
    if warnings:
        print(f"词库漂移门禁：{warnings} 项警告（不阻断）")
        return 2
    print("词库漂移门禁通过：同步区块成对、已注册主题词库非空、规范形一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
