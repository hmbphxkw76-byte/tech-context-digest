#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""发布指纹（P2-2）：正式报告的 sha256 指纹登记 / 查重 / 漂移检测。

指纹 = 报告文件字节的 sha256（确定性、无时间戳）。用途：
  - 发布留痕：记录每次正式报告的发布指纹；
  - 重复检测：不同报告路径内容完全一致时告警（疑似误复制）；
  - 漂移检测：与已登记指纹比对，识别新增 / 变更 / 移除。

用法：
    python engine/tools/publish_fingerprint.py --emit     # 采集并写入指纹库
    python engine/tools/publish_fingerprint.py --check    # 与指纹库比对
    python engine/tools/publish_fingerprint.py --list

退出码：0 一致 / 通过；2 存在漂移或重复（不阻断，提示 --emit）；1 用法错误。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, iter_reports  # noqa: E402

STORE_PATH = ROOT / "engine" / "audit" / "records" / "publish_fingerprints.json"
SCHEMA_VERSION = "1.0"


def fingerprint_file(path: Path) -> str:
    """文件内容 sha256（十六进制）。

    指纹对 `\\r\\n` 归一为 `\\n` 后再哈希：仓库在 Windows（core.autocrlf=true）
    工作区为 CRLF、CI 为 LF，按原始字节哈希会平台相关并恒报漂移。归一后
    跨平台一致，与生成物「确定性、无时间戳」要求对齐。
    """
    data = Path(path).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def collect() -> dict[str, str]:
    """采集全部正式报告指纹 -> {rel: sha256}（确定性排序）。"""
    out: dict[str, str] = {}
    for ref in iter_reports():
        p = ROOT / ref.rel
        if p.is_file():
            out[ref.rel] = fingerprint_file(p)
    return dict(sorted(out.items()))


def duplicates(fingerprints: dict[str, str]) -> list[list[str]]:
    """相同指纹的不同报告路径分组（内容完全一致）。"""
    by_hash: dict[str, list[str]] = {}
    for rel, h in fingerprints.items():
        by_hash.setdefault(h, []).append(rel)
    return [sorted(v) for v in by_hash.values() if len(v) > 1]


def build_document(fingerprints: dict[str, str]) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "comment": "正式发布报告指纹（sha256，确定性无时间戳）。由 publish_fingerprint.py --emit 生成。",
        "fingerprints": fingerprints,
    }


def load_store(path: Path = STORE_PATH) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    fps = data.get("fingerprints", {})
    return fps if isinstance(fps, dict) else {}


def emit(path: Path = STORE_PATH) -> dict[str, str]:
    fps = collect()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_document(fps), ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    return fps


def diff(store: dict[str, str], current: dict[str, str]) -> dict:
    """指纹漂移 -> {new, changed, removed}。"""
    new = sorted(set(current) - set(store))
    removed = sorted(set(store) - set(current))
    changed = sorted(k for k in set(store) & set(current) if store[k] != current[k])
    return {"new": new, "changed": changed, "removed": removed}


def main() -> int:
    ap = argparse.ArgumentParser(description="发布指纹登记 / 查重 / 漂移检测")
    ap.add_argument("--emit", action="store_true", help="采集并写入指纹库")
    ap.add_argument("--check", action="store_true", help="与指纹库比对（漂移 / 重复）")
    ap.add_argument("--list", action="store_true", help="列出当前指纹")
    ap.add_argument("--store", help="指纹库路径覆盖（仓库相对或绝对）")
    args = ap.parse_args()

    store_path = STORE_PATH
    if args.store:
        store_path = Path(args.store) if Path(args.store).is_absolute() else ROOT / args.store

    current = collect()
    if args.emit:
        fps = emit(store_path)
        dups = duplicates(fps)
        print(f"[emit] {len(fps)} 份正式报告指纹写入 {store_path.relative_to(ROOT)}；"
              f"重复内容 {len(dups)} 组")
        for g in dups:
            print(f"[DUP] {' = '.join(g)}")
        return 0

    if args.list:
        for rel, h in current.items():
            print(f"{h[:12]}  {rel}")
        return 0

    if args.check:
        store = load_store(store_path)
        d = diff(store, current)
        dups = duplicates(current)
        drift = d["new"] or d["changed"] or d["removed"]
        print(f"[check] 当前 {len(current)} 份；已登记 {len(store)} 份；"
              f"新增 {len(d['new'])} / 变更 {len(d['changed'])} / 移除 {len(d['removed'])}；"
              f"重复内容 {len(dups)} 组")
        for rel in d["new"]:
            print(f"[NEW] {rel}")
        for rel in d["changed"]:
            print(f"[CHANGED] {rel}: {store[rel][:12]} -> {current[rel][:12]}")
        for rel in d["removed"]:
            print(f"[REMOVED] {rel}")
        for g in dups:
            print(f"[DUP] {' = '.join(g)}")
        if drift:
            print("存在指纹漂移：请运行 python engine/tools/publish_fingerprint.py --emit")
            return 2
        if dups:
            print("存在内容完全相同的报告（疑似误复制），请人工确认")
            return 2
        print("发布指纹检查通过：与指纹库一致，无重复内容")
        return 0

    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
