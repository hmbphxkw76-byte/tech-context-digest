"""结构与规范校验（CI: scheduled-maintenance / content-update 的 validate 步骤）。

退出码：0 = 通过；1 = 存在错误项；2 = 仅存在警告项。

校验项：
- 通用层根部必备文件齐全（engine/templates/ 5 份共享文件）
- 类型模板目录齐全（engine/templates/<类型ID>/，清单见 _common.TEMPLATE_TYPE_DIRS）
- 通用层（含全部类型子目录）无业务关键词（地区 / 业务类型 / 专属机构等）
- 业务线目录结构（prompts/business-config.md、reports/、数据目录 data/processed/<theme>/…）
- 业务配置含运行变量区
- 报告文件命名符合通用规范
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    BUSINESS_KEYWORDS,
    REQUIRED_TEMPLATE_FILES,
    TEMPLATE_DIR,
    TEMPLATE_TYPE_DIRS,
    REPORT_TYPE_REF_RE,
    REPORT_TYPE_VAR_RE,
    detect_report,
    iter_business_dirs,
    processed_data_dir,
    ROOT,
)

ERRORS: list[str] = []
WARNINGS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def check_templates() -> None:
    tpl_dir = TEMPLATE_DIR
    if not tpl_dir.is_dir():
        err(f"缺少通用模板目录 {tpl_dir.relative_to(ROOT)}/")
        return
    for name in REQUIRED_TEMPLATE_FILES:
        if not (tpl_dir / name).exists():
            err(f"通用层缺少必备文件: {tpl_dir.relative_to(ROOT)}/{name}")
    for type_id, files in TEMPLATE_TYPE_DIRS.items():
        type_dir = tpl_dir / type_id
        if not type_dir.is_dir():
            err(f"缺少类型模板目录: {tpl_dir.relative_to(ROOT)}/{type_id}/")
            continue
        for name in files:
            if not (type_dir / name).exists():
                err(f"类型 {type_id} 缺少必备模板: {tpl_dir.relative_to(ROOT)}/{type_id}/{name}")
    for md in tpl_dir.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        for kw in BUSINESS_KEYWORDS:
            if kw in text:
                err(f"通用层出现业务关键词「{kw}」: {md.relative_to(ROOT)}")


def check_business_dirs() -> None:
    businesses = iter_business_dirs()
    if not businesses:
        warn("未识别到任何业务线目录（{地区}/{物业类型}）")
        return
    for b in businesses:
        config = b.path / "prompts" / "business-config.md"
        if not config.exists():
            warn(f"{b.rel}: 缺少业务配置 prompts/business-config.md")
        else:
            text = config.read_text(encoding="utf-8", errors="replace")
            for var in ("{{REGION}}", "{{TOPIC}}", "{{REGISTRY_PATH}}", "{{SOURCE_REGISTRY_PATH}}"):
                if var not in text:
                    warn(f"{b.rel}: business-config.md 缺少变量 {var}")
        for sub in ("reports",):
            if not (b.path / sub).is_dir():
                warn(f"{b.rel}: 缺少 {sub}/ 目录（空目录不入 git，首次产出后自动补齐）")
        # 数据层统一收口于 data/processed/<theme>/<维度段…>（三层架构，业务线内不再存数据）
        try:
            pdir = processed_data_dir(b.rel)
        except ValueError:
            pdir = None
        if pdir is not None and not pdir.is_dir():
            warn(
                f"{b.rel}: 缺少数据目录 {pdir.relative_to(ROOT).as_posix()}/"
                "（空目录不入 git，首次产出后自动补齐）"
            )
        reports = b.path / "reports"
        if reports.is_dir():
            for f in sorted(reports.iterdir()):
                # 占位文件（如 .gitkeep）用于保留空目录，不视为报告，不参与命名判定
                if f.is_file() and not f.name.startswith(".") and detect_report(f.name) is None:
                    warn(f"{b.rel}/reports/{f.name}: 文件名不符合报告命名约定")


def check_report_type_declarations() -> None:
    """类型声明结构化（P1-4）：{{REPORT_TYPE}} 必填，且与继承声明引用一致。"""
    for b in iter_business_dirs():
        config = b.path / "prompts" / "business-config.md"
        try:
            text = config.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        mv = REPORT_TYPE_VAR_RE.search(text)
        mr = REPORT_TYPE_REF_RE.search(text)
        if not mv:
            warn(f"{b.rel}: business-config.md 缺结构化类型声明 {{{{REPORT_TYPE}}}}（建议补登）")
            continue
        type_id = mv.group(1)
        if type_id not in TEMPLATE_TYPE_DIRS:
            err(f"{b.rel}: {{{{REPORT_TYPE}}}}={type_id} 未在 _common.TEMPLATE_TYPE_DIRS 登记")
        if mr and mr.group(1) != type_id:
            err(f"{b.rel}: {{{{REPORT_TYPE}}}}={type_id} 与继承声明引用 {mr.group(1)} 不一致")


def main() -> int:
    check_templates()
    check_business_dirs()
    check_report_type_declarations()
    for e in ERRORS:
        print(f"[ERROR] {e}")
    for w in WARNINGS:
        print(f"[WARN] {w}")
    if not ERRORS and not WARNINGS:
        print("结构与规范校验通过：通用层完整、业务线结构齐全、命名合规")
    if ERRORS:
        print(f"校验失败：{len(ERRORS)} 项错误，{len(WARNINGS)} 项警告")
        return 1
    if WARNINGS:
        print(f"校验存在 {len(WARNINGS)} 项警告（无错误）")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
