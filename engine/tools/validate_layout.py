"""目录结构校验（CI: ci.yml / scheduled-maintenance 的结构关卡）。

单一事实源：engine/tools/layout.json。校验项：
- 一级根目录合规：无未注册的业务 / 公共目录（白名单之外）
- 主题注册完整：themes / root_reserved / regions / naming 字段齐全
- 业务线层级：每条业务线深度与主题维度数一致（region 为可选维度时可省略该段）
- 命名规范：全部目录段符合 kebab-case（layout.naming.pattern）
- 地域白名单：region 维度段命中 layout.regions
- 维度声明：维度序列自洽（无重复、无未登记维度名）；先后顺序由 layout.json 按主题声明（economy 为 region→category，tech 等主题为 category→region）；optional_dimensions 必须是已声明维度

退出码：0 = 通过；1 = 存在错误；2 = 仅警告（含已注册未创建的主题）。

用法：
    python engine/tools/validate_layout.py
    python engine/tools/validate_layout.py --check   # 与缺省行为一致（显式声明）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    ROOT,
    iter_business_dirs,
    load_layout,
    resolve_segments,
)

ERRORS: list[str] = []
WARNINGS: list[str] = []
INFOS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNINGS.append(msg)


def info(msg: str) -> None:
    INFOS.append(msg)


# 已登记维度名（layout.json 各主题 dimensions 的取值域）
KNOWN_DIMENSIONS = {
    "region", "category", "subcategory", "sector", "tech_field",
    "sub_direction", "segment",
}


def check_dimension_priority(layout) -> None:
    """维度声明校验：序列自洽（无重复、无未登记维度名）。

    历史硬性规则「category 必须先于 region」随三层重构回滚取消：维度先后由
    layout.json 各主题自行声明（economy 为 region→category，tech 等主题为
    category→region），与重构前「旧维度」一致；校验器不再强制单一顺序，
    实例路径的段序由 check_theme 的地域白名单校验兜住。
    """
    for theme, (_name, dims) in layout.themes.items():
        if len(set(dims)) != len(dims):
            err(f"主题 {theme} 维度序列存在重复维度：{list(dims)}")
        for d in dims:
            if d not in KNOWN_DIMENSIONS:
                err(f"主题 {theme} 含未登记维度名：{d}")
        for d in layout.optional_dims(theme):
            if d not in dims:
                err(f"主题 {theme} 的 optional_dimensions 含未声明维度：{d}")


def check_layout_integrity(layout) -> None:
    """layout.json 字段完整性。"""
    if not layout.themes:
        err("layout.json 未注册任何主题（themes 为空）")
    if not layout.root_reserved:
        err("layout.json 未声明根级保留项（root_reserved 为空）")
    if "engine" not in layout.root_reserved:
        err("layout.json 的 root_reserved 未包含 engine（公共资源唯一归宿）")
    if "content" not in layout.root_reserved:
        err("layout.json 的 root_reserved 未包含 content（内容层唯一归宿）")
    if not layout.regions:
        warn("layout.json 未声明地域白名单（regions 为空）")
    check_dimension_priority(layout)
    for theme, (name, dims) in layout.themes.items():
        if not name:
            err(f"主题 {theme} 缺少中文名")
        if not dims:
            err(f"主题 {theme} 未声明维度序列（dimensions 为空）")
        if len(dims) + 1 > layout.max_depth:
            err(f"主题 {theme} 层级深度 {len(dims) + 1} 超出 naming.max_depth {layout.max_depth}")


def check_root(layout) -> None:
    """一级根目录：不得存在未注册目录。"""
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        if d.name not in layout.themes and d.name not in layout.root_reserved:
            err(f"未注册的一级目录: {d.name}/（请迁入 engine/ 或在 layout.json 注册）")


def _walk_theme_dirs(base: Path, max_depth: int):
    """产出主题下 1..max_depth 层目录，但不进入业务线内部（业务线为叶子）。

    业务线以 prompts/business-config.md 为锚点；其下 prompts/ reports/ 等
    子目录不是维度段，不参与层级 / 地域校验。
    """
    if max_depth < 1 or not base.is_dir():
        return
    for child in sorted(base.iterdir()):
        if child.is_dir() and not child.name.startswith("."):
            yield child
            if (child / "prompts" / "business-config.md").exists():
                continue
            yield from _walk_theme_dirs(child, max_depth - 1)


def check_theme(theme: str, layout) -> None:
    """单个主题的层级、命名与地域白名单。"""
    theme_dir = ROOT / layout.content_root / theme
    if not theme_dir.is_dir():
        info(f"主题 {theme} 已注册但尚未创建目录（待扩展）")
        return
    dims = layout.dimensions(theme)
    naming = re.compile(layout.naming_pattern)
    optional = layout.optional_dims(theme)
    region_idx = dims.index("region") if "region" in dims else None
    allow_short = region_idx is not None and "region" in optional

    for d in _walk_theme_dirs(theme_dir, len(dims)):
        rel = d.relative_to(theme_dir).as_posix()
        segments = rel.split("/")
        for seg in segments:
            if not naming.match(seg):
                err(f"{theme}/{rel}: 目录段「{seg}」不符合命名规范 {layout.naming_pattern}")
        dims_segments = segments
        if dims_segments and dims_segments[0] == layout.regional_segment:
            dims_segments = dims_segments[1:]
        if len(dims_segments) == len(dims):
            if region_idx is not None and layout.regions and dims_segments[region_idx] not in layout.regions:
                err(f"{theme}/{rel}: 地域段「{dims_segments[region_idx]}」未在 layout.regions 白名单注册")
        elif not (allow_short and len(dims_segments) == len(dims) - 1):
            err(f"{theme}/{rel}: 层级深度 {len(dims_segments)} 与主题 {theme} 声明维度 {list(dims)} 不匹配")


def check_business_depth(layout) -> None:
    """业务线实际段数与主题维度数一致（region 可缺省时允许少一段）。

    业务线全路径默认为 content/<theme>/<维度段...>，段数 = 1（content）+
    维度数；region 为可选维度时可省略该段。主题可声明 segment 覆盖
    （空串表示无地区分组段，不额外加段）。
    """
    for b in iter_business_dirs():
        dims = layout.dimensions(b.theme)
        optional = layout.optional_dims(b.theme)
        n = len(b.segments)
        allowed = {len(dims)}
        if "region" in dims and "region" in optional:
            allowed.add(len(dims) - 1)
        if n not in allowed:
            err(f"{b.rel}: 层级深度 {n + 1} 与主题 {b.theme} 期望维度 {list(dims)} 不一致")
            continue
        try:
            mapping = resolve_segments(layout, b.theme, b.segments)
        except ValueError as e:
            err(f"{b.rel}: {e}")
            continue
        region = mapping.get("region")
        if region is not None and layout.regions and region not in layout.regions:
            err(f"{b.rel}: 地域段「{region}」未在 layout.regions 白名单注册")


def main() -> int:
    ap = argparse.ArgumentParser(description="目录结构校验（layout.json 单一事实源）")
    ap.add_argument("--check", action="store_true", help="与缺省行为一致（显式声明）")
    ap.parse_args()

    try:
        layout = load_layout()
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        return 1

    check_layout_integrity(layout)
    check_root(layout)
    for theme in sorted(layout.themes):
        check_theme(theme, layout)
    check_business_depth(layout)

    for i in INFOS:
        print(f"[INFO] {i}")
    for w in WARNINGS:
        print(f"[WARN] {w}")
    for err in ERRORS:
        print(f"[ERROR] {err}")

    if ERRORS:
        print(f"目录结构校验失败：{len(ERRORS)} 项错误，{len(WARNINGS)} 项警告")
        return 1
    if WARNINGS:
        print(f"目录结构校验存在 {len(WARNINGS)} 项警告（无错误）")
        return 2
    print("目录结构校验通过：一级目录合规、层级与命名符合 layout.json")
    return 0


if __name__ == "__main__":
    if ROOT.is_dir():
        sys.exit(main())
    sys.exit(1)
