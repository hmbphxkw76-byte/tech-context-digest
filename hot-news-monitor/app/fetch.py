"""RSS / Atom 抓取与来源可达性探测（仅标准库实现，无第三方依赖）。

纪律：只请求 config/sources.json 白名单内的 URL；所有网络异常降级为状态记录，
不抛出到调用方（保证调度器长跑稳定）。User-Agent 显式声明用途。
"""
from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any

from .models import NewsItem

USER_AGENT = (
    "TechLifeResearch-HotNewsMonitor/1.0 "
    "(local research dashboard; contact: repository maintainer)"
)

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "sources.json"


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_sources(config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    cfg = config or load_config()
    return [dict(s) for s in cfg.get("sources", ()) if s.get("type") in ("rss", "atom")]


def _to_iso(value: str) -> str:
    """把 RFC822 / ISO 日期统一为 UTC ISO8601（无法解析时返回原串截断）。"""
    value = (value or "").strip()
    if not value:
        return ""
    dt: datetime | None = None
    try:
        dt = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        dt = None
    if dt is None:
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return value[:19]
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _item_id(url: str, title: str) -> str:
    basis = url.strip() or title.strip()
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:12]


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text or "").strip()


def parse_feed(xml_bytes: bytes, source: dict[str, Any]) -> list[NewsItem]:
    """解析 RSS 2.0 / Atom；返回该源的 NewsItem 列表（不做跨源去重）。"""
    root = ET.fromstring(xml_bytes)
    tag = root.tag.lower()
    entries: list[tuple[str, str, str, str]] = []  # title, url, date, desc
    if tag.endswith("rss") or root.find(".//item") is not None:
        for node in root.iter("item"):
            title = (node.findtext("title") or "").strip()
            link = (node.findtext("link") or "").strip()
            date = node.findtext("pubDate") or node.findtext("{http://purl.org/dc/elements/1.1/}date") or ""
            desc = node.findtext("description") or ""
            if title and link:
                entries.append((title, link, date, desc))
    else:  # Atom
        ns = "{http://www.w3.org/2005/Atom}"
        for node in root.iter(f"{ns}entry"):
            title = (node.findtext(f"{ns}title") or "").strip()
            link = ""
            for ln in node.findall(f"{ns}link"):
                href = ln.get("href", "")
                if href and (ln.get("rel") in (None, "alternate")):
                    link = href
                    break
            date = node.findtext(f"{ns}updated") or node.findtext(f"{ns}published") or ""
            desc = node.findtext(f"{ns}summary") or node.findtext(f"{ns}content") or ""
            if title and link:
                entries.append((title, link, date, desc))
    out: list[NewsItem] = []
    seen: set[str] = set()
    for title, url, date, desc in entries:
        iid = _item_id(url, title)
        if iid in seen:
            continue
        seen.add(iid)
        out.append(
            NewsItem(
                id=iid,
                title=_strip_tags(title),
                url=url,
                source_id=str(source["id"]),
                source_name=str(source["name"]),
                tier=str(source.get("tier", "media")),
                published_at=_to_iso(date),
                summary=_strip_tags(desc)[:300],
            )
        )
    return out


def probe(url: str, timeout: float = 8.0) -> dict[str, Any]:
    """单 URL 可达性探测：-> {ok, status, elapsed_ms, note}。"""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/xml, text/xml, */*"})
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = getattr(resp, "status", 200)
            return {"ok": 200 <= int(code) < 400, "status": int(code),
                    "elapsed_ms": int((time.monotonic() - t0) * 1000), "note": ""}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": int(e.code), "elapsed_ms": int((time.monotonic() - t0) * 1000),
                "note": f"HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001 - 探测必须吞掉一切网络异常
        return {"ok": False, "status": -1, "elapsed_ms": int((time.monotonic() - t0) * 1000),
                "note": type(e).__name__}


def fetch_source(source: dict[str, Any], timeout: float = 10.0) -> tuple[list[NewsItem], dict[str, Any]]:
    """抓取单个白名单源（单次请求）；-> (items, status_record)。异常不抛出。"""
    url = str(source.get("url", ""))
    t0 = time.monotonic()
    st: dict[str, Any] = {"source_id": source.get("id"), "url": url}
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = resp.read()
            code = int(getattr(resp, "status", 200))
        items = parse_feed(payload, source)
        st.update({"ok": 200 <= code < 400, "status": code,
                   "elapsed_ms": int((time.monotonic() - t0) * 1000), "fetched": len(items)})
        return items, st
    except urllib.error.HTTPError as e:
        st.update({"ok": False, "status": int(e.code),
                   "elapsed_ms": int((time.monotonic() - t0) * 1000), "fetched": 0, "note": f"HTTP {e.code}"})
        return [], st
    except Exception as e:  # noqa: BLE001
        st.update({"ok": False, "status": -1,
                   "elapsed_ms": int((time.monotonic() - t0) * 1000), "fetched": 0,
                   "note": type(e).__name__})
        return [], st
