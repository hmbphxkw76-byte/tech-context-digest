"""本地 HTTP 服务：看板静态页 + JSON API（标准库实现）。

路由：
- GET  /                  -> dashboard/index.html
- GET  /api/state         -> 完整快照（无快照时先触发一次刷新）
- GET  /api/health        -> {ok, generated_at, mode}
- GET  /api/events/<id>   -> 单事件详情（时间线 + 背景溯源说明）
- POST /api/refresh       -> 立即全量刷新并返回新快照
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from .aggregate import background_note
from .pipeline import DEFAULT_INTERVAL, DEFAULT_THRESHOLD, refresh
from .store import Store

DASHBOARD_DIR = Path(__file__).resolve().parents[1] / "dashboard"


def _json_bytes(data: dict[str, Any]) -> bytes:
    return json.dumps(data, ensure_ascii=False).encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    store: Store
    threshold: float = DEFAULT_THRESHOLD
    interval: int = DEFAULT_INTERVAL
    config: dict[str, Any] | None = None

    def log_message(self, fmt: str, *args: Any) -> None:  # 静默默认访问日志
        return

    # ---------------------------------------------------------- helpers
    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _snapshot(self) -> dict[str, Any]:
        snap = self.store.load_state()
        if snap is None:
            snap = refresh(self.store, config=self.config, threshold=self.threshold,
                           interval_seconds=self.interval)
        return snap.to_dict()

    # ---------------------------------------------------------- routes
    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/" or path.endswith(".html"):
            target = (DASHBOARD_DIR / "index.html").resolve()
            if not str(target).startswith(str(DASHBOARD_DIR.resolve())):
                self._send(403, b"forbidden", "text/plain; charset=utf-8")
                return
            self._send(200, target.read_bytes(), "text/html; charset=utf-8")
            return
        if path == "/api/state":
            self._send(200, _json_bytes(self._snapshot()), "application/json; charset=utf-8")
            return
        if path == "/api/health":
            snap = self.store.load_state()
            body = {"ok": True, "generated_at": snap.generated_at if snap else None,
                    "mode": snap.mode if snap else "none"}
            self._send(200, _json_bytes(body), "application/json; charset=utf-8")
            return
        if path.startswith("/api/events/"):
            eid = unquote(path[len("/api/events/"):])
            state = self._snapshot()
            event_dict = next((e for e in state["events"] if e["id"] == eid), None)
            if event_dict is None:
                self._send(404, _json_bytes({"error": "not found"}), "application/json; charset=utf-8")
                return
            event = _event_obj(event_dict)
            payload = dict(event_dict)
            payload["background"] = background_note(event)
            payload["timeline"] = sorted(event_dict["items"], key=lambda i: i.get("published_at", ""))
            self._send(200, _json_bytes(payload), "application/json; charset=utf-8")
            return
        self._send(404, b"not found", "text/plain; charset=utf-8")

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path == "/api/refresh":
            snap = refresh(self.store, config=self.config, threshold=self.threshold,
                           interval_seconds=self.interval)
            self._send(200, _json_bytes(snap.to_dict()), "application/json; charset=utf-8")
            return
        self._send(404, b"not found", "text/plain; charset=utf-8")


def _event_obj(event_dict: dict[str, Any]) -> Any:
    from .models import HotEvent, NewsItem

    return HotEvent(
        id=str(event_dict["id"]), title=str(event_dict["title"]), tag=str(event_dict["tag"]),
        heat=float(event_dict.get("heat", 0)), level=int(event_dict.get("level", 2)),
        first_seen=str(event_dict.get("first_seen", "")), last_seen=str(event_dict.get("last_seen", "")),
        source_ids=[str(s) for s in event_dict.get("source_ids", ())],
        items=[NewsItem(**i) for i in event_dict.get("items", ())],
    )


def make_server(host: str, port: int, store: Store, *, threshold: float, interval: int,
                config: dict[str, Any] | None) -> ThreadingHTTPServer:
    Handler.store = store
    Handler.threshold = threshold
    Handler.interval = interval
    Handler.config = config
    return ThreadingHTTPServer((host, port), Handler)
