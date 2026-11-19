#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""指标登记册 sidecar 生成（确定性、可重放、无墙钟时间戳）。

数据源：`data/processed/economy/dubai/apartment/*indicator_registry*.xlsx`
（取文件名周期最新者）的「年度基线2027 / 首期基线值」表。
输出：`data/processed/economy/dubai/apartment/indicator_latest.json`，
为 A-03 真值核对提供结构化的「指标编号 -> 最新值 / 统计周期 / 来源」。

口径：
- 「年度基线2027」为主表（v2.0 起承接基线）；「首期基线值」仅补主表缺失编号（历史锚）。
- 每行固定六项：indicator_id / value / unit / period / source / updated。
- value 保留登记册原文（不伪造、不合并多口径），由 `a03_truth_check` 解析。
- updated 取登记册期间（文件名周期，如 2027-01），**不取墙钟时间戳**。
- 输出按 indicator_id 字典序排序，同输入同输出（可重放）。

用法：
    python engine/tools/indicator_sidecar.py build
    python engine/tools/indicator_sidecar.py build --registry <path> --out <path>
    python engine/tools/indicator_sidecar.py check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT  # noqa: E402

APARTMENT_DATA_DIR = ROOT / "data" / "processed" / "economy" / "dubai" / "apartment"
DEFAULT_GLOB = "*indicator_registry*.xlsx"
SIDECAR_PATH = APARTMENT_DATA_DIR / "indicator_latest.json"
BUSINESS_LINE = "content/economy/dubai/apartment"
# 主表在前：年度基线 2027 优先，首期基线值仅补缺
DEFAULT_SHEETS = ("年度基线2027", "首期基线值")
FIELDS = ("indicator_id", "value", "unit", "period", "source", "updated")
PERIOD_RE = re.compile(r"(\d{4}-\d{2})")
# 值列表头：年度基线为「v2.0 基线值」，首期基线为「基线值」
VALUE_HEADERS = ("v2.0 基线值", "基线值")
HEADER_ALIASES = {
    "indicator_id": ("指标编号",),
    "value": VALUE_HEADERS,
    "unit": ("单位",),
    "period": ("统计周期",),
    "source": ("来源机构",),
}


def latest_registry(data_dir: Path = APARTMENT_DATA_DIR, glob: str = DEFAULT_GLOB) -> Path | None:
    """文件名周期最新的登记册；无则 None。"""
    files = sorted(Path(data_dir).glob(glob))
    return files[-1] if files else None


def registry_period(path: Path) -> str:
    """登记册期间（文件名周期，如 2027-01）；解析不到返回空串。"""
    m = PERIOD_RE.search(Path(path).stem)
    return m.group(1) if m else ""


def _column_index(header: list[str], aliases: tuple[str, ...]) -> int | None:
    for name in aliases:
        if name in header:
            return header.index(name)
    return None


def read_sheet(path: Path, sheet: str) -> list[dict]:
    """读取登记册单表 -> 规范字段行（仅含已识别列）。

    表头行以首列 == 「指标编号」定位；列名按 HEADER_ALIASES 映射。
    读不到 / 表不存在返回空列表（不抛异常，便于历史登记册降级）。
    """
    import openpyxl

    try:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception:
        return []
    try:
        if sheet not in wb.sheetnames:
            return []
        rows = list(wb[sheet].iter_rows(values_only=True))
    finally:
        wb.close()
    hi = next((i for i, r in enumerate(rows) if r and r[0] == "指标编号"), None)
    if hi is None:
        return []
    header = [str(c).strip() if c is not None else "" for c in rows[hi]]
    cols = {key: _column_index(header, aliases) for key, aliases in HEADER_ALIASES.items()}
    out: list[dict] = []
    for r in rows[hi + 1:]:
        if not r or r[0] is None or str(r[0]).strip() == "":
            continue
        rec = {}
        for key, idx in cols.items():
            rec[key] = "" if idx is None or idx >= len(r) or r[idx] is None else str(r[idx]).strip()
        out.append(rec)
    return out


def build(registry: Path | None = None,
          data_dir: Path = APARTMENT_DATA_DIR) -> dict:
    """生成 sidecar 字典（确定性：按 indicator_id 排序，无墙钟）。"""
    path = Path(registry) if registry is not None else latest_registry(data_dir)
    if path is None:
        raise FileNotFoundError(f"未找到登记册：{data_dir}/{DEFAULT_GLOB}")
    period = registry_period(path)
    merged: dict[str, dict] = {}
    for sheet in DEFAULT_SHEETS:
        for rec in read_sheet(path, sheet):
            iid = rec.get("indicator_id", "")
            if not iid or iid in merged:
                continue
            merged[iid] = {
                "indicator_id": iid,
                "value": rec.get("value", ""),
                "unit": rec.get("unit", ""),
                "period": rec.get("period", ""),
                "source": rec.get("source", ""),
                "updated": period,
            }
    indicators = [merged[k] for k in sorted(merged)]
    return {
        "schema_version": "1.0",
        "business_line": BUSINESS_LINE,
        "registry": path.name,
        "sheets": list(DEFAULT_SHEETS),
        "updated": period,
        "count": len(indicators),
        "indicators": indicators,
    }


def write(sidecar: dict, out: Path = SIDECAR_PATH) -> Path:
    """落盘 sidecar（UTF-8、缩进 2、尾随换行；同输入同字节）。"""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(sidecar, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    return out


def load(path: Path = SIDECAR_PATH) -> dict:
    """读取 sidecar；缺失 / 非法抛异常（由调用方决定降级）。"""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="指标登记册 sidecar 生成（确定性、可重放）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--registry", help="登记册 xlsx 路径（默认取最新一期）")
    b.add_argument("--out", help="输出 JSON 路径（默认 indicator_latest.json）")
    c = sub.add_parser("check")
    c.add_argument("--registry", help="登记册 xlsx 路径（默认取最新一期）")
    c.add_argument("--sidecar", help="已落盘 sidecar 路径（默认 indicator_latest.json）")
    args = ap.parse_args()

    if args.cmd == "build":
        sidecar = build(Path(args.registry) if args.registry else None)
        out = write(sidecar, Path(args.out) if args.out else SIDECAR_PATH)
        print(f"[sidecar] {sidecar['count']} 项指标写入 {out}（登记册 {sidecar['registry']}，"
              f"期间 {sidecar['updated']}）")
        return 0

    sidecar = build(Path(args.registry) if args.registry else None)
    on_disk = load(Path(args.sidecar) if args.sidecar else SIDECAR_PATH)
    if on_disk == sidecar:
        print(f"[sidecar] 重放一致：{sidecar['count']} 项指标，登记册 {sidecar['registry']}")
        return 0
    print(f"[sidecar] 重放不一致：落盘 {on_disk.get('registry')} / 重放 {sidecar['registry']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
