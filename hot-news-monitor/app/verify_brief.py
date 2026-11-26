"""专题数据机器核验：结构完整性 / 引用闭合 / 链接合规与白名单 / 可达性探测。

用法：python -m app verify-brief [--no-probe] [--json]
输出 runtime/brief-verify.json（可选 --out）。可达性只标注不阻断（网络受限环境友好）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

APP_ROOT = Path(__file__).resolve().parents[1]
BRIEF_PATH = APP_ROOT / "config" / "nvidia-brief-2026-11-26.json"
OUT_PATH = APP_ROOT / "runtime" / "brief-verify.json"

URL_RE = re.compile(r"^https?://[^\s]+$")
ALLOWED_HOST_PARTS = (
    "nvidianews.nvidia.com", "investors.nvidia.com", "nvidia.com",
    "sec.gov", "reuters.com", "cnbc.com", "apnews.com", "bbc.co.uk",
    "bloomberg.com", "ft.com", "wsj.com", "washingtonpost.com",
    "nytimes.com", "theguardian.com", "dw.com", "france24.com",
    "aljazeera.com", "npr.org", "pbs.org", "spglobal.com",
    "moodys.com", "fitchratings.com", "worldbank.org", "imf.org",
)
FORBIDDEN_HOST_PARTS = (
    "xinhuanet", "people.com.cn", "cctv", "cri.cn", "chinadaily",
    "globaltimes", "caixin", "sina.com", "sohu.com", "163.com",
    "qq.com", "thepaper.cn", "huanqiu", "guancha.cn",
)
VERIFICATION_OK = {"verified", "partial", "inferred", "unverified"}
TIER_OK = {"official", "rating", "media_t1", "media"}


def _host(url: str) -> str:
    m = re.match(r"^https?://([^/\s]+)", url)
    return (m.group(1).lower() if m else "")


def check_structure(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("topic", "window", "generated_at", "sources", "timeline"):
        if key not in data:
            errors.append(f"missing_field:{key}")
    srcs = data.get("sources", [])
    refs: list[str] = []
    for s in srcs:
        ref = s.get("ref") or s.get("id")
        if not ref:
            errors.append(f"source_without_ref:{s.get('title', '')[:40]}")
            continue
        refs.append(ref)
        if s.get("verification") not in VERIFICATION_OK:
            errors.append(f"bad_verification:{ref}={s.get('verification')!r}")
        if s.get("tier") not in TIER_OK:
            errors.append(f"bad_tier:{ref}={s.get('tier')!r}")
        if not URL_RE.match(str(s.get("url", ""))):
            errors.append(f"bad_url:{ref}")
    ref_set = set(refs)
    for t in data.get("timeline", []):
        for r in t.get("refs", ()):
            if r not in ref_set:
                errors.append(f"dangling_ref:{r}@{t.get('date')}")
        if t.get("verification") not in VERIFICATION_OK:
            errors.append(f"bad_verification:timeline@{t.get('date')}")
    return errors


def check_links(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for s in data.get("sources", []):
        url = str(s.get("url", ""))
        host = _host(url)
        problems = []
        if not URL_RE.match(url):
            problems.append("malformed")
        else:
            if any(p in host for p in FORBIDDEN_HOST_PARTS):
                problems.append("forbidden_chinese_media")
            if not any(a in host for a in ALLOWED_HOST_PARTS):
                problems.append("host_not_allowlisted")
        rows.append({"ref": s.get("ref"), "host": host, "problems": problems})
    return rows


def probe(url: str, timeout: float = 6.0) -> dict[str, Any]:
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "TechLifeResearch-HotNewsMonitor/1.0 (local research dashboard)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/rss+xml;q=0.9,*/*;q=0.8",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = int(getattr(resp, "status", 200))
            return {"ok": 200 <= code < 400, "status": code}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": int(e.code), "note": f"HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "status": -1, "note": type(e).__name__}


def verify_brief(data: dict[str, Any], do_probe: bool = True) -> dict[str, Any]:
    struct_errors = check_structure(data)
    links = check_links(data)
    reachable: dict[str, dict[str, Any]] = {}
    if do_probe:
        for row in links:
            if row["problems"]:
                reachable[row["ref"]] = {"skipped": True, "reason": ",".join(row["problems"])}
            else:
                url = next(str(s.get("url")) for s in data["sources"] if (s.get("ref") or s.get("id")) == row["ref"])
                reachable[row["ref"]] = probe(url)
    return {
        "ok": not struct_errors and not any(r["problems"] for r in links),
        "structure_errors": struct_errors,
        "link_checks": links,
        "reachable": reachable,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m app verify-brief")
    ap.add_argument("--source", default=str(BRIEF_PATH))
    ap.add_argument("--out", default=str(OUT_PATH))
    ap.add_argument("--no-probe", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    data = json.loads(Path(args.source).read_text(encoding="utf-8"))
    report = verify_brief(data, do_probe=not args.no_probe)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        bad = len(report["structure_errors"]) + sum(1 for r in report["link_checks"] if r["problems"])
        ok_reach = sum(1 for v in report["reachable"].values() if v.get("ok"))
        total = len(report["reachable"])
        print(f"[verify-brief] ok={report['ok']} 结构/链接问题={bad} 可达={ok_reach}/{total} 明细={out}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
