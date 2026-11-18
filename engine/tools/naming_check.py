#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""命名规范全量扫描门禁（NAMING-CHECK v1.0）。

依据 `engine/docs/structure-and-naming-spec.md`（STRUCTURE-AND-NAMING-SPEC）
对仓库现行文件 / 目录做机械扫描，补齐「文件级命名」缺口（S4）。

  NC-01 目录命名（[W]）：content / engine / data / .github 下目录须 kebab-case
        （白名单：Python 包目录 snake_case、点目录、生成目录、legacy 冻结）。
  NC-02 文件命名（[W]）：按位置规则矩阵校验扩展名与形态
        （engine/tools/*.py snake、engine/tests/test_*.py、engine/docs/*.md kebab、
        content/**/reports/<period>_<cycle>.html、content/**/prompts/business-config.md
        + prompt-<cycle>.md、.github/workflows/*.yml 等）。

生成物豁免：`engine/audit/records/**`、`engine/vocabulary/data/**`、`data/raw/**`、
`archives/**`、`__pycache__/**`、legacy 冻结项。

退出码：0 = 通过；1 = 存在 [E]；2 = 仅 [W]。
用法：python engine/tools/naming_check.py [--quiet]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT  # noqa: E402

KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SNAKE_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
REPORT_RE = re.compile(r"^\d{4}(?:-\d{2}(?:-\d{2})?)?(?:-Q[1-4])?_[a-z0-9_]+\.html$")
PROMPT_RE = re.compile(r"^prompt-[a-z0-9-]+\.md$")
ADR_RE = re.compile(r"^\d{4}-[a-z0-9-]+\.md$")
AUDIT_REPORT_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:-\d{4}-\d{2}-\d{2})?$")
DATA_FILE_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]*\.(?:md|json|csv|xlsx)$")
LEGACY_JSON = {"institution_tiers.json", "pipeline_manifest.json", "branch_registry.json"}

EXEMPT_DIR_PARTS = {
    "__pycache__", "archives", "node_modules",
}
EXEMPT_DIR_PREFIXES = (
    "engine/audit/records/", "engine/vocabulary/data/", "data/raw/",
)
EXEMPT_DIR_NAMES = {
    ".github", ".githooks", ".meituan-catpaw", ".git",
    "fact_cards",  # legacy 冻结
}
# 生成目录（随生成器命名，豁免 kebab 约束）
GENERATED_DIRS = {"imports", "exports", "reviews", "semantic", "backups"}


def _is_exempt_dir(rel: str) -> bool:
    parts = rel.split("/")
    if any(p in EXEMPT_DIR_NAMES for p in parts):
        return True
    if any(p in EXEMPT_DIR_PARTS for p in parts):
        return True
    if any(rel.startswith(pre) for pre in EXEMPT_DIR_PREFIXES):
        return True
    if any(p in GENERATED_DIRS for p in parts):
        return True
    return False


def _is_python_pkg(rel: str) -> bool:
    return (ROOT / rel).parent.joinpath("__init__.py").exists()


def check_dirs() -> list[str]:
    warns: list[str] = []
    for base in ("content", "engine", "data", ".github"):
        root = ROOT / base
        if not root.is_dir():
            continue
        for d in root.rglob("*"):
            if not d.is_dir():
                continue
            rel = d.relative_to(ROOT).as_posix()
            if _is_exempt_dir(rel):
                continue
            name = d.name
            if name.startswith("."):
                continue
            if (d / "__init__.py").exists():
                if not SNAKE_RE.match(name):
                    warns.append(f"NC-01 Python 包目录非 snake_case：{rel}")
                continue
            if not KEBAB_RE.match(name):
                warns.append(f"NC-01 目录非 kebab-case：{rel}")
    return warns


def _check_file(rel: str, name: str) -> str | None:
    parts = rel.split("/")
    stem = name.rsplit(".", 1)[0] if "." in name else name
    # engine/tools/*.py（仅顶层）
    if rel.startswith("engine/tools/") and name.endswith(".py") and rel.count("/") == 2:
        return None if re.match(r"^_?[a-z0-9]+(?:_[a-z0-9]+)*$", stem) else f"NC-02 engine/tools 非 snake_case：{rel}"
    if rel.startswith("engine/tests/") and name.endswith(".py"):
        return None if re.match(r"^test_[a-z0-9_]+$", stem) else f"NC-02 测试命名非 test_*.py：{rel}"
    if rel.startswith("engine/tools/") and name.endswith(".json") and rel.count("/") == 2:
        if name in LEGACY_JSON:
            return None
        return None if KEBAB_RE.match(stem) else f"NC-02 engine/tools/*.json 非 kebab：{rel}"
    if rel.startswith("engine/docs/") and name.endswith(".md"):
        if parts[2] == "adr":
            return None if ADR_RE.match(name) else f"NC-02 ADR 命名非 NNNN-slug.md：{rel}"
        return None if KEBAB_RE.match(stem) else f"NC-02 engine/docs/*.md 非 kebab：{rel}"
    if rel.startswith("engine/report-audits/") and name.endswith(".md"):
        return None if AUDIT_REPORT_RE.match(stem) else f"NC-02 report-audits 命名不合规：{rel}"
    if rel.startswith("content/") and "/reports/" in rel and name.endswith(".html"):
        return None if REPORT_RE.match(name) else f"NC-02 报告命名非 <period>_<cycle>.html：{rel}"
    if rel.startswith("content/") and "/prompts/" in rel and name.endswith(".md"):
        ok = name == "business-config.md" or PROMPT_RE.match(name)
        return None if ok else f"NC-02 业务提示词命名不合规：{rel}"
    if rel.startswith(".github/workflows/") and name.endswith((".yml", ".yaml")):
        return None if name.endswith(".yml") and KEBAB_RE.match(stem) else f"NC-02 工作流命名不合规：{rel}"
    if rel.startswith("data/processed/") and name.endswith((".md", ".json", ".csv", ".xlsx")):
        if name.endswith(".README.md"):
            return None
        return None if DATA_FILE_RE.match(name) else f"NC-02 data/processed 命名不合规：{rel}"
    return None


def check_files() -> list[str]:
    warns: list[str] = []
    for base in ("content", "engine", "data", ".github"):
        root = ROOT / base
        if not root.is_dir():
            continue
        for f in root.rglob("*"):
            if not f.is_file():
                continue
            rel = f.relative_to(ROOT).as_posix()
            if _is_exempt_dir(str(Path(rel).parent)):
                continue
            if "/archives/" in rel or rel.startswith("archives/"):
                continue
            msg = _check_file(rel, f.name)
            if msg:
                warns.append(msg)
    return warns


def main() -> int:
    ap = argparse.ArgumentParser(description="命名规范全量扫描门禁")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    warns = check_dirs() + check_files()
    for w in warns:
        print(f"[W] {w}")
    if not args.quiet or warns:
        print(f"命名规范校验：{len(warns)} 警告")
    return 2 if warns else 0


if __name__ == "__main__":
    sys.exit(main())
