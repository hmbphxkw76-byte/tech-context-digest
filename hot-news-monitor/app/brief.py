"""专题追踪报告：读取 config/nvidia-brief-*.json，渲染静态中文报告页。

用法：python -m app report-nvidia [--source config/nvidia-brief-2026-11-26.json]
     默认输出 dashboard/report-nvidia.html（可提交产物）。
纪律：来源与核验状态完全由 JSON 数据驱动；未核验条目在页面显式标注「待核实」。
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any

APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = APP_ROOT / "config" / "nvidia-brief-2026-11-26.json"
DEFAULT_OUT = APP_ROOT / "dashboard" / "report-nvidia.html"

TIER_LABEL = {"official": "官方", "rating": "评级", "media_t1": "一线媒体", "media": "主流媒体"}
LEVEL_LABEL = {1: "关键节点", 2: "重要进展"}


def esc(text: Any) -> str:
    return html.escape(str(text if text is not None else ""), quote=True)


def render(data: dict[str, Any]) -> str:
    sources = list(data.get("sources", ()))
    timeline = list(data.get("timeline", ()))
    cross = list(data.get("cross_check", ()))
    verified = sum(1 for s in sources if s.get("verified"))
    by_id = {s["id"]: s for s in sources}
    tiers = sorted({s.get("tier", "") for s in sources})

    def _src_row(s: dict[str, Any]) -> str:
        tier = esc(s.get("tier", ""))
        label = esc(TIER_LABEL.get(s.get("tier"), s.get("tier", "")))
        verify = '<span class="ok">已核验</span>' if s.get("verified") else '<span class="pending">待核实</span>'
        return (
            f'<tr><td>{esc(s["date"])}</td>'
            f'<td><span class="tier {tier}">{label}</span></td>'
            f'<td><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["title"])}</a>'
            f'<br><span class="src-note">{esc(s.get("note", ""))}</span></td>'
            f'<td>{verify}</td></tr>'
        )

    src_rows = "\n".join(_src_row(s) for s in sources)
    tl_items = "\n".join(
        f'<div class="tl-item {("l1" if t.get("level") == 1 else "")}">'
        f'<div class="tl-time">{esc(t["date"])}</div>'
        f'<div class="tl-title">{esc(t["title"])} <span class="lv">{esc(LEVEL_LABEL.get(t.get("level"), ""))}</span></div>'
        f'<div class="tl-src">来源：{esc("、".join(by_id[r]["source"] for r in t.get("refs", ()) if r in by_id))}</div></div>'
        for t in timeline
    )
    cross_rows = "\n".join(
        f'<tr><td>{esc(c["event"])}</td><td>{esc("；".join(c.get("claims", ())))}</td>'
        f'<td>{esc("、".join(by_id[r]["source"] for r in c.get("agreements", ()) if r in by_id))}</td>'
        f'<td>{esc("；".join(c.get("disagreements", ())) or "无")}</td></tr>'
        for c in cross
    )
    metrics = [
        ("事件节点", len(timeline)),
        ("来源条目", len(sources)),
        ("已核验", f"{verified}/{len(sources)}"),
        ("最高信源层级", "官方" if "official" in tiers else ("一线媒体" if "media_t1" in tiers else "媒体")),
    ]
    metric_html = "".join(f'<div class="metric"><div class="v">{esc(v)}</div><div class="k">{esc(k)}</div></div>' for k, v in metrics)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>英伟达事件专题追踪 · 热点新闻实时追踪</title>
<style>
:root{{--navy:#16324f;--accent:#c8a24a;--bg:#f4f6f8;--card:#fff;--ink:#1d2733;--muted:#5d6b7a;--line:#dfe5ec;--chip:#eef2f6;--radius:10px}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:"Segoe UI","PingFang SC","Microsoft YaHei",system-ui,sans-serif;background:var(--bg);color:var(--ink);line-height:1.55;font-size:15px}}
.skip-link{{position:absolute;left:-9999px;top:0;background:var(--navy);color:#fff;padding:8px 14px;z-index:99}}
.skip-link:focus{{left:0}}
a{{color:var(--navy)}} :focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
header.hero{{background:linear-gradient(135deg,#16324f,#0f2438 70%,#0a1a29);color:#fff;padding:30px 0 24px}}
header.hero h1{{margin:0;font-size:26px}} header.hero .sub{{margin-top:6px;color:#c7d3df;font-size:14px}}
.meta-pills{{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}}
.pill{{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:5px 12px;font-size:12.5px}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
main.wrap{{padding:20px 20px 40px}}
section.sec{{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:0 1px 3px rgba(16,36,56,.08);margin-bottom:20px;padding:18px 20px}}
h2.sec{{font-size:18px;margin:0 0 10px;color:var(--navy)}}
.grid-metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}}
.metric{{background:var(--chip);border:1px solid var(--line);border-radius:8px;padding:10px 12px}}
.metric .v{{font-size:20px;font-weight:600;color:var(--navy)}} .metric .k{{font-size:12px;color:var(--muted)}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
thead th{{background:var(--chip);color:var(--navy);font-size:12.5px}}
tr:last-child td{{border-bottom:0}}
.tier{{font-size:11px;border-radius:4px;padding:1px 6px;border:1px solid var(--line);color:var(--muted)}}
.tier.official{{color:#1e7d4f;border-color:#bcd9c8}} .tier.media_t1{{color:var(--navy);border-color:#c3ceda}}
.ok{{color:#1e7d4f;font-weight:600}} .pending{{color:#b25e1f;font-weight:600}}
.src-note{{font-size:12px;color:var(--muted)}}
.table-wrap{{overflow-x:auto}}
.timeline{{position:relative;margin-top:8px;padding-left:22px}}
.timeline::before{{content:"";position:absolute;left:6px;top:6px;bottom:6px;width:2px;background:var(--line)}}
.tl-item{{position:relative;padding:0 0 14px 10px}}
.tl-item::before{{content:"";position:absolute;left:-20px;top:5px;width:10px;height:10px;border-radius:50%;background:var(--navy);border:2px solid #fff;box-shadow:0 0 0 2px var(--line)}}
.tl-item.l1::before{{background:var(--accent)}}
.tl-time{{font-size:12px;color:var(--muted)}} .tl-title{{font-size:14px;font-weight:500;margin:2px 0}}
.tl-src{{font-size:12px;color:var(--muted)}}
.lv{{font-size:11px;color:#8a6d2a;background:#f3ead6;border-radius:4px;padding:1px 6px;margin-left:6px}}
footer{{border-top:1px solid var(--line);padding:16px 0 28px;color:var(--muted);font-size:12.5px;text-align:center}}
@media (max-width:560px){{.wrap{{padding:0 12px}} section.sec{{padding:14px}}}}
@media (prefers-reduced-motion:reduce){{{{*{{animation-duration:.001s!important;transition-duration:.001s!important}}}}}}
@media print{{.skip-link{{display:none}} body{{background:#fff}} section.sec{{box-shadow:none;break-inside:avoid}}}}
</style>
</head>
<body>
<a class="skip-link" href="#main">跳到主要内容</a>
<header class="hero"><div class="wrap">
<h1>英伟达事件专题追踪</h1>
<div class="sub">{esc(data.get("topic", ""))} · 追踪窗口 {esc(data.get("window", ""))}</div>
<div class="meta-pills">
<span class="pill">生成时间 {esc(data.get("generated_at", ""))}</span>
<span class="pill">信源纪律：仅英文权威信源</span>
<span class="pill"><a href="/" style="color:#fff">← 返回实时看板</a></span>
</div>
</div></header>
<main class="wrap" id="main">
<section class="sec">
<h2 class="sec">摘要指标</h2>
<div class="grid-metrics">{metric_html}</div>
<p class="src-note">{esc(data.get("method", ""))}</p>
</section>
<section class="sec">
<h2 class="sec">多信源交叉验证</h2>
<div class="table-wrap"><table><thead><tr><th>事件</th><th>关键主张</th><th>一致来源</th><th>分歧 / 口径差异</th></tr></thead><tbody>{cross_rows}</tbody></table></div>
</section>
<section class="sec">
<h2 class="sec">事件发展时间线</h2>
<div class="timeline">{tl_items}</div>
</section>
<section class="sec">
<h2 class="sec">来源清单（含核验状态）</h2>
<div class="table-wrap"><table><thead><tr><th>日期</th><th>层级</th><th>标题与说明</th><th>核验</th></tr></thead><tbody>{src_rows}</tbody></table></div>
</section>
</main>
<footer>本报告由 hot-news-monitor 专题生成器渲染；数据文件 config/nvidia-brief-2026-11-26.json；未直接核验条目已在页面标注「待核实」。</footer>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m app report-nvidia")
    ap.add_argument("--source", default=str(DEFAULT_SOURCE))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args(argv)
    data = json.loads(Path(args.source).read_text(encoding="utf-8"))
    out = Path(args.out)
    out.write_text(render(data), encoding="utf-8")
    print(f"[report] written {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
