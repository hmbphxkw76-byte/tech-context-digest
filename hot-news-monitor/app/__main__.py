"""命令行入口：python -m app <command>（仓库根目录下执行）。"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from .fetch import load_config, load_sources, probe
from .pipeline import DEFAULT_INTERVAL, DEFAULT_THRESHOLD, refresh, summarize
from .scheduler import Scheduler
from .server import make_server
from .store import Store

APP_ROOT = Path(__file__).resolve().parents[1]


def _store() -> Store:
    return Store(APP_ROOT / "runtime")


def cmd_serve(args: argparse.Namespace) -> int:
    store = _store()
    store.ensure()
    # --demo：仅用合成示例数据（离线演示），状态栏如实标注「示例数据」
    config = {"sources": [], "heat_weights": {
        "official": 3.0, "rating": 3.0, "media_t1": 2.5, "media": 2.0}} if args.demo else load_config()
    sched = Scheduler(
        store,
        interval_seconds=args.interval,
        threshold=args.threshold,
        config=config,
        immediate=not args.no_immediate,
        on_tick=lambda msg: print(f"[scheduler] {msg}", flush=True),
    )
    srv = make_server(args.host, args.port, store, threshold=args.threshold,
                      interval=args.interval, config=config)
    sched.start()
    print(f"[serve] http://{args.host}:{args.port}/  周期={args.interval}s  阈值={args.threshold}",
          flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        sched.stop()
        srv.shutdown()
    return 0


def cmd_refresh(args: argparse.Namespace) -> int:
    snap = refresh(_store(), threshold=args.threshold, interval_seconds=args.interval)
    print(summarize(snap))
    return 0


def cmd_probe(args: argparse.Namespace) -> int:
    cfg = load_config()
    rows = []
    for src in load_sources(cfg):
        st = probe(str(src["url"]))
        rows.append({"id": src.get("id"), "url": src.get("url"), **st})
        flag = "OK " if st["ok"] else "FAIL"
        print(f"[{flag}] {src.get('id'):<16} status={st['status']:<4} {st['elapsed_ms']:>6}ms  {src['url']}")
    out = APP_ROOT / "runtime" / "source_probe.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(1 for r in rows if r["ok"])
    print(f"\n探测完成：{ok}/{len(rows)} 可达；明细写入 {out}")
    return 0


def cmd_sample_verify(args: argparse.Namespace) -> int:
    from .verify import verify_from_store

    report = verify_from_store(_store(), n=args.n)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    bad = bool(report["failed"]) or report["heat_mismatch_events"] or report["tag_mismatch_events"]
    return 1 if bad else 0


def _cmd_verify_brief(args: argparse.Namespace) -> int:
    from .verify_brief import main as vb_main

    argv = []
    if args.source:
        argv += ["--source", args.source]
    if args.out:
        argv += ["--out", args.out]
    if args.no_probe:
        argv += ["--no-probe"]
    return int(vb_main(argv))


def _cmd_report_nvidia(args: argparse.Namespace) -> int:
    from .brief import main as brief_main

    argv = []
    if args.source:
        argv += ["--source", args.source]
    if args.out:
        argv += ["--out", args.out]
    return int(brief_main(argv))


def cmd_soak(args: argparse.Namespace) -> int:
    """长跑稳定性测试：连续运行 duration 秒，每 interval 秒刷新一次并核对快照可用。"""
    store = _store()
    store.ensure()
    t0 = time.monotonic()
    ticks = 0
    errors: list[str] = []
    while time.monotonic() - t0 < args.duration:
        try:
            snap = refresh(store, threshold=args.threshold, interval_seconds=args.interval)
            assert snap.events, "快照无事件"
            ticks += 1
            print(f"[soak {ticks:>3}] mode={snap.mode} events={len(snap.events)} "
                  f"items={snap.metrics['total_items']} t+{int(time.monotonic() - t0)}s", flush=True)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{type(exc).__name__}: {exc}")
            print(f"[soak][error] {errors[-1]}", flush=True)
        time.sleep(args.interval)
    print(f"[soak] 完成：ticks={ticks} errors={len(errors)} 时长={int(time.monotonic() - t0)}s")
    if errors:
        print("[soak] 最近错误：", errors[-3:])
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m app", description="热点新闻实时追踪报告系统")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("serve", help="启动调度 + 本地看板服务")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--interval", type=int, default=DEFAULT_INTERVAL, help="全量刷新周期（秒），默认 300")
    p.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="高优先级热度阈值，默认 50（预校准）")
    p.add_argument("--no-immediate", action="store_true", help="启动时不立即刷新")
    p.add_argument("--demo", action="store_true", help="离线演示：只用合成示例数据（不联网）")
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser("refresh", help="立即做一次全量刷新")
    p.add_argument("--interval", type=int, default=DEFAULT_INTERVAL)
    p.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    p.set_defaults(func=cmd_refresh)

    p = sub.add_parser("probe-sources", help="探测白名单信源可达性")
    p.set_defaults(func=cmd_probe)

    p = sub.add_parser("sample-verify", help="随机抽样核验抓取条目（默认 100 条）")
    p.add_argument("--n", type=int, default=100)
    p.set_defaults(func=cmd_sample_verify)

    p = sub.add_parser("soak", help="长跑稳定性测试（秒）")
    p.add_argument("--duration", type=int, default=1800)
    p.add_argument("--interval", type=int, default=DEFAULT_INTERVAL)
    p.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    p.set_defaults(func=cmd_soak)

    p = sub.add_parser("report-nvidia", help="渲染英伟达专题追踪报告页")
    p.add_argument("--source", default=None, help="数据 JSON（默认 config/nvidia-brief-2026-11-26.json）")
    p.add_argument("--out", default=None, help="输出路径（默认 dashboard/report-nvidia.html）")
    p.set_defaults(func=_cmd_report_nvidia)

    p = sub.add_parser("verify-brief", help="专题数据机器核验（结构/引用/链接/可达性）")
    p.add_argument("--source", default=None)
    p.add_argument("--out", default=None)
    p.add_argument("--no-probe", action="store_true")
    p.set_defaults(func=_cmd_verify_brief)

    args = ap.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
