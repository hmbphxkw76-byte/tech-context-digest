"""自动化状态记录（CI: content-update / scheduled-maintenance 的 status 步骤与活跃度检查）。

状态文件：仓库根 automation-status.json（content-update / scheduled-maintenance
工作流提交该文件）。

用法：
    python engine/tools/automation_status.py record --phase content-update \
        --result success --run-url <url>
    python engine/tools/automation_status.py activity --threshold 45 [--porcelain]

activity 输出：
    --porcelain -> 距最近一次记录的天数（整数）或 unknown（无记录）
    普通模式    -> 人读说明

退出码：0 = 正常（record 成功 / activity 有记录或无记录）；2 = 参数错误。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT  # noqa: E402

STATUS_FILE = ROOT / "automation-status.json"

# 占位 / 本机主机：不得写入状态文件（避免假记录污染活跃度统计）
_PLACEHOLDER_HOSTS = ("example.local", "example.com", "localhost", "127.0.0.1")


def is_placeholder_url(url: str) -> bool:
    """占位 / 本机 URL 判定（用于拒绝假运行记录入库）。"""
    u = (url or "").strip().lower()
    return any(h in u for h in _PLACEHOLDER_HOSTS)


def load_status() -> dict:
    if STATUS_FILE.exists():
        try:
            data = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("records"), list):
                return data
        except (OSError, json.JSONDecodeError):
            pass
    return {"records": []}


def record(phase: str, result: str, run_url: str) -> int:
    if is_placeholder_url(run_url):
        print(f"[SKIP] 占位 / 本机 URL 不入状态文件：{run_url or '(空)'}")
        return 0
    data = load_status()
    data["records"].append(
        {
            "phase": phase,
            "result": result,
            "run_url": run_url,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
        }
    )
    STATUS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已记录：phase={phase} result={result}")
    return 0


def days_since_latest(now: datetime, records: list[dict]):
    """纯函数：距最近一次记录的天数（向下取整）；无记录返回 None。"""
    latest = None
    for r in records:
        ts = r.get("timestamp")
        if not ts:
            continue
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        if latest is None or dt > latest:
            latest = dt
    if latest is None:
        return None
    return int((now - latest).total_seconds() // 86400)


def activity(threshold: int, porcelain: bool) -> int:
    records = load_status()["records"]
    now = datetime.now(tz=timezone.utc)
    days = days_since_latest(now, records)
    if days is None:
        if porcelain:
            print("unknown")
        else:
            print("尚无自动化执行记录（首次运行 record 后开始计时）")
        return 0
    if porcelain:
        print(str(days))
    else:
        note = "（已超阈值，建议产生一次提交或手动触发维护）" if days > threshold else ""
        print(f"距上次自动化记录 {days} 天（阈值 {threshold} 天）{note}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="自动化状态记录与活跃度检查")
    sub = ap.add_subparsers(dest="command", required=True)

    p_rec = sub.add_parser("record", help="记录一次自动化执行")
    p_rec.add_argument("--phase", required=True, choices=["content-update", "maintenance"])
    p_rec.add_argument("--result", required=True, choices=["success", "failure"])
    p_rec.add_argument("--run-url", default="")

    p_act = sub.add_parser("activity", help="活跃度检查：距最近一次记录的天数")
    p_act.add_argument("--threshold", type=int, default=45)
    p_act.add_argument("--porcelain", action="store_true", help="仅输出天数或 unknown")

    args = ap.parse_args()
    if args.command == "record":
        return record(args.phase, args.result, args.run_url)
    return activity(args.threshold, args.porcelain)


if __name__ == "__main__":
    sys.exit(main())
