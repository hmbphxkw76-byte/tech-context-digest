"""热点事件专题报告生成器。

- 人工编译专题：config/briefs/index.json（清单）+ config/briefs/<data_file> -> dashboard/brief-<slug>.html
- 当前热点专题：dashboard/brief-current.html，由 rebuild_current() 按 runtime/state.json 的
  Top1 事件自动重建（标题随热点轮换）；命中清单关键词时叠加该专题的人工编译层。
- 用法：python -m app report-nvidia [--source ...] [--out ...]
        python -m app briefs --rebuild     # 重建全部专题页 + current 页
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any

APP_ROOT = Path(__file__).resolve().parents[1]
BRIEF_DIR = APP_ROOT / "config" / "briefs"
MANIFEST_PATH = BRIEF_DIR / "index.json"
DEFAULT_SOURCE = BRIEF_DIR / "nvidia-2026-11-26.json"
DEFAULT_OUT = APP_ROOT / "dashboard" / "brief-nvidia-2026-11-26.html"

TIER_LABEL = {"official": "官方", "rating": "评级", "media_t1": "一线媒体", "media": "主流媒体"}
VERIFY_LABEL = {"verified": "已核验", "partial": "部分核验", "inferred": "推断", "unverified": "待核实"}
STRENGTH_LABEL = {"强": "强", "中": "中", "弱": "弱"}
LEVEL_LABEL = {1: "关键节点", 2: "重要进展"}

_CSS = """
:root{--navy:#16324f;--accent:#c8a24a;--bg:#f4f6f8;--card:#fff;--ink:#1d2733;--muted:#5d6b7a;--line:#dfe5ec;--chip:#eef2f6;--radius:10px}
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI","PingFang SC","Microsoft YaHei",system-ui,sans-serif;background:var(--bg);color:var(--ink);line-height:1.55;font-size:15px}
.skip-link{position:absolute;left:-9999px;top:0;background:var(--navy);color:#fff;padding:8px 14px;z-index:99}
.skip-link:focus{left:0}
a{color:var(--navy)} :focus-visible{outline:2px solid var(--accent);outline-offset:2px}
header.hero{background:linear-gradient(135deg,#16324f,#0f2438 70%,#0a1a29);color:#fff;padding:28px 0 22px}
header.hero h1{margin:0;font-size:24px} header.hero .sub{margin-top:6px;color:#c7d3df;font-size:14px}
.meta-pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.pill{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:5px 12px;font-size:12.5px}
.pill.btn{background:var(--accent);border-color:var(--accent);color:#1d2733;font-weight:600;text-decoration:none;display:inline-block}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
main.wrap{padding:20px 20px 40px}
section.sec{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:0 1px 3px rgba(16,36,56,.08);margin-bottom:20px;padding:18px 20px}
h2.sec{font-size:18px;margin:0 0 10px;color:var(--navy)}
.grid-metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}
.metric{background:var(--chip);border:1px solid var(--line);border-radius:8px;padding:10px 12px}
.metric .v{font-size:20px;font-weight:600;color:var(--navy)} .metric .k{font-size:12px;color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
thead th{background:var(--chip);color:var(--navy);font-size:12.5px}
tr:last-child td{border-bottom:0}
.table-wrap{overflow-x:auto}
.badge{display:inline-block;font-size:11px;border-radius:5px;padding:1px 7px;border:1px solid var(--line);white-space:nowrap}
.badge.ok{color:#1e7d4f;border-color:#bcd9c8;background:#f0f8f3}
.badge.mid{color:#b25e1f;border-color:#e8d3bd;background:#fdf6ee}
.badge.info{color:#3d5a80;border-color:#c6d3e2;background:#f0f4fa}
.badge.pending{color:#a33333;border-color:#e3bcbc;background:#fdf1f1}
.tier{font-size:11px;border-radius:4px;padding:1px 6px;border:1px solid var(--line);color:var(--muted)}
.tier.official{color:#1e7d4f;border-color:#bcd9c8} .tier.media_t1{color:var(--navy);border-color:#c3ceda}
.src-note{font-size:12px;color:var(--muted)}
.ref-no{font-weight:700;color:var(--navy);white-space:nowrap}
.timeline{position:relative;margin-top:8px;padding-left:22px}
.timeline::before{content:"";position:absolute;left:6px;top:6px;bottom:6px;width:2px;background:var(--line)}
.tl-item{position:relative;padding:0 0 14px 10px}
.tl-item::before{content:"";position:absolute;left:-20px;top:5px;width:10px;height:10px;border-radius:50%;background:var(--navy);border:2px solid #fff;box-shadow:0 0 0 2px var(--line)}
.tl-item.l1::before{background:var(--accent)}
.tl-time{font-size:12px;color:var(--muted)} .tl-title{font-size:14px;font-weight:500;margin:2px 0}
.tl-src{font-size:12px;color:var(--muted)}
details.fold{border:1px solid var(--line);border-radius:8px;margin-bottom:10px;background:#fafbfd}
details.fold summary{cursor:pointer;padding:9px 12px;font-size:13.5px;color:var(--navy);list-style-position:inside}
details.fold[open] summary{border-bottom:1px solid var(--line)}
details.fold .fold-body{padding:8px 4px 4px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.chip{border:1px solid var(--line);background:var(--chip);color:var(--ink);border-radius:999px;padding:4px 11px;font-size:12.5px;cursor:pointer}
.chip[aria-pressed="true"]{background:var(--navy);border-color:var(--navy);color:#fff}
.decision-card{display:grid;grid-template-columns:max-content 1fr;gap:6px 14px;font-size:13.5px}
.decision-card dt{font-weight:600;color:var(--navy);white-space:nowrap}
.decision-card dd{margin:0}
.gap-item{font-size:13.5px;margin:0 0 8px}
.heat-badge{display:inline-block;min-width:26px;text-align:center;border-radius:6px;padding:1px 8px;font-size:12.5px;font-weight:600;border:1px solid var(--line);color:var(--muted);background:#fff}
.heat-badge.lvl-hot{color:#7a4a12;border-color:#e0c493;background:#faf3e6}
.heat-badge.lvl-high{color:#fff;border-color:var(--navy);background:var(--navy)}
.heat-badge.lvl-mid{color:var(--muted);border-color:var(--line);background:var(--chip)}
footer{border-top:1px solid var(--line);padding:16px 0 28px;color:var(--muted);font-size:12.5px;text-align:center}
@media (max-width:560px){.wrap{padding:0 12px} section.sec{padding:14px}}
@media print{.skip-link,.chips,.pill.btn{display:none!important} body{background:#fff} section.sec{box-shadow:none;break-inside:avoid} details.fold{display:block}}
"""

_JS = """
(function(){
  var chips = document.querySelectorAll('#tierFilter .chip');
  chips.forEach(function(c){
    c.addEventListener('click', function(){
      var tier = c.getAttribute('data-tier');
      chips.forEach(function(x){ x.setAttribute('aria-pressed', String(x===c)); });
      document.querySelectorAll('#sourceTable tbody tr').forEach(function(tr){
        tr.style.display = (tier==='全部' || tr.getAttribute('data-tier')===tier) ? '' : 'none';
      });
    });
  });
})();
"""


def esc(text: Any) -> str:
    return html.escape(str(text if text is not None else ""), quote=True)


def _badge(kind: str, label: str) -> str:
    return f'<span class="badge {kind}">{esc(label)}</span>'


def _verify_badge(v: str) -> str:
    cls = {"verified": "ok", "partial": "mid", "inferred": "info", "unverified": "pending"}.get(v, "pending")
    return _badge(cls, VERIFY_LABEL.get(v, v))


def _strength_badge(s: str) -> str:
    cls = {"强": "ok", "中": "mid", "弱": "pending"}.get(s, "mid")
    return _badge(cls, f"证据强度·{STRENGTH_LABEL.get(s, s)}")


def heat_tier(h: float, threshold: float) -> tuple[str, str]:
    """三档级别：热（≥阈值）/ 高（≥25）/ 中（<25）。与看板展示口径一致。"""
    if h >= threshold:
        return "热", "lvl-hot"
    if h >= 25:
        return "高", "lvl-high"
    return "中", "lvl-mid"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_verify_report() -> dict[str, Any]:
    path = APP_ROOT / "runtime" / "brief-verify.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def render(data: dict[str, Any], *, data_file_label: str = "") -> str:
    sources = list(data.get("sources", ()))
    timeline = list(data.get("timeline", ()))
    cross = list(data.get("cross_check", ()))
    gaps = list(data.get("gaps", ()))
    by_ref = {(s.get("ref") or s.get("id")): s for s in sources}
    verify = load_verify_report()
    reach = verify.get("reachable", {}) if isinstance(verify, dict) else {}

    verified = sum(1 for s in sources if s.get("verification") == "verified")
    tiers = sorted({s.get("tier", "") for s in sources})
    metrics = [
        ("事件节点", len(timeline)),
        ("来源条目", len(sources)),
        ("已核验", f"{verified}/{len(sources)}"),
        ("最高信源层级", "官方" if "official" in tiers else ("一线媒体" if "media_t1" in tiers else "媒体")),
    ]
    metric_html = "".join(f'<div class="metric"><div class="v">{esc(v)}</div><div class="k">{esc(k)}</div></div>' for k, v in metrics)

    topic = str(data.get("topic", "热点事件专题追踪"))
    pills = [
        f'<span class="pill">数据截至 {esc(data.get("generated_at", ""))}</span>',
        f'<span class="pill">下次复核 {esc(data.get("next_review", "—"))}</span>',
        f'<span class="pill">可重放 {esc(data.get("replay_cmd", "python -m app briefs --rebuild"))}</span>',
    ]
    for link in data.get("dashboard_links", ()):
        pills.append(f'<a class="pill btn" href="{esc(link["url"])}">{esc(link["label"])} ↗</a>')
    pills.append('<a class="pill" href="/" style="color:#fff">← 返回实时看板</a>')

    summary_html = ""
    if data.get("summary_zh"):
        items = "".join(f"<li>{esc(line)}</li>" for line in data["summary_zh"])
        summary_html = f'<section class="sec"><h2 class="sec">决策摘要</h2><ul>{items}</ul>' \
                       '<p class="src-note">仅归纳已核验结论；[S编号] 指向来源清单。</p></section>'

    decision_html = ""
    card = data.get("decision_card")
    if card:
        decision_html = (
            '<section class="sec"><h2 class="sec">决策卡</h2><dl class="decision-card">'
            f'<dt>结论</dt><dd>{esc(card.get("conclusion", ""))}</dd>'
            f'<dt>证据强度</dt><dd>{_strength_badge(card.get("evidence_strength", "中"))} '
            f'信息充分度 {_badge("info", esc(card.get("sufficiency", "—")))}</dd>'
            f'<dt>触发条件</dt><dd>{esc("；".join(card.get("triggers", ())))}</dd>'
            f'<dt>反向证据</dt><dd>{esc("；".join(card.get("counter_evidence", ())))}</dd>'
            "</dl></section>"
        )

    cross_rows = []
    for c in cross:
        srcs = "、".join(by_ref[r]["source"] for r in c.get("agreements", ()) if r in by_ref)
        tier_txt = "、".join(TIER_LABEL.get(t, t) for t in c.get("tiers", ())) or "—"
        cross_rows.append(
            f'<tr><td>{esc(c["event"])}</td><td>{esc("；".join(c.get("claims", ())))}</td>'
            f'<td>{esc(srcs)}</td><td>{esc(c.get("independent_sources", "—"))} 家 · {esc(tier_txt)}</td>'
            f'<td>{_strength_badge(c.get("strength", "中"))}</td>'
            f'<td>{esc("；".join(c.get("disagreements", ())) or "无")}</td></tr>'
        )
    cross_html = (
        '<section class="sec"><h2 class="sec">多信源交叉验证</h2><div class="table-wrap"><table><thead><tr>'
        "<th>事件</th><th>关键主张</th><th>一致来源</th><th>独立信源 × 层级</th><th>结论强度</th><th>分歧 / 口径差异</th>"
        f"</tr></thead><tbody>{''.join(cross_rows)}</tbody></table></div></section>"
    )

    def _tl_group(level: int, title: str) -> str:
        rows = [t for t in timeline if t.get("level") == level]
        inner = "".join(
            '<div class="tl-item {cls}"><div class="tl-time">{date}</div>'
            '<div class="tl-title">{title} {vb} {sb}</div>'
            '<div class="tl-src">来源：{refs}</div></div>'.format(
                cls="l1" if level == 1 else "",
                date=esc(t["date"]),
                title=esc(t["title"]),
                vb=_verify_badge(t.get("verification", "unverified")),
                sb=_strength_badge(t.get("strength", "中")),
                refs=esc("、".join(by_ref[r]["source"] for r in t.get("refs", ()) if r in by_ref)),
            )
            for t in rows
        )
        return f'<details class="fold"{(" open" if level == 1 else "")}><summary>{esc(title)}（{len(rows)} 条）</summary><div class="fold-body"><div class="timeline">{inner}</div></div></details>'

    timeline_html = (
        '<section class="sec"><h2 class="sec">事件发展时间线</h2>'
        + (_tl_group(1, LEVEL_LABEL[1]) + _tl_group(2, LEVEL_LABEL[2]))
        + '<p class="src-note">折叠面板按级别分组；条目附信息等级与证据强度徽标。</p></section>'
    )

    filter_chips = ['<button type="button" class="chip" data-tier="全部" aria-pressed="true">全部</button>']
    for t in ("official", "media_t1", "media"):
        if any(s.get("tier") == t for s in sources):
            filter_chips.append(f'<button type="button" class="chip" data-tier="{t}" aria-pressed="false">{esc(TIER_LABEL[t])}</button>')

    src_rows = []
    for s in sources:
        ref = esc(s.get("ref") or s.get("id"))
        rb = reach.get(ref, {})
        reach_mark = ""
        if rb:
            if rb.get("skipped"):
                reach_mark = f' <span class="badge pending">链接未探测（{esc(rb.get("reason", ""))}）</span>'
            elif rb.get("ok"):
                reach_mark = f' <span class="badge ok">可达 HTTP {esc(rb.get("status", ""))}</span>'
            else:
                reach_mark = f' <span class="badge pending">不可达（{esc(rb.get("note") or rb.get("status") or "未知")}）</span>'
        src_rows.append(
            f'<tr id="src-{ref}" data-tier="{esc(s.get("tier", ""))}">'
            f'<td>{ref}</td><td>{esc(s["date"])}</td>'
            f'<td><span class="tier {esc(s.get("tier", ""))}">{esc(TIER_LABEL.get(s.get("tier"), s.get("tier", "")))}</span></td>'
            f'<td><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["title"])}</a>'
            f'<br><span class="src-note">{esc(s.get("note", ""))}</span>{reach_mark}</td>'
            f'<td>{_verify_badge(s.get("verification", "unverified"))}</td></tr>'
        )
    sources_html = (
        '<section class="sec"><h2 class="sec">来源清单（含核验与可达性状态）</h2>'
        f'<div class="chips" id="tierFilter">{"".join(filter_chips)}</div>'
        '<div class="table-wrap"><table id="sourceTable"><thead><tr><th>编号</th><th>日期</th><th>层级</th><th>标题与说明</th><th>核验</th></tr></thead>'
        f'<tbody>{"".join(src_rows)}</tbody></table></div></section>'
    )

    gaps_html = ""
    if gaps:
        items = "".join(
            f'<li class="gap-item">【{esc(g.get("status", "缺失"))}】{esc(g.get("item", ""))} —— 影响：{esc(g.get("impact", ""))}</li>'
            for g in gaps
        )
        gaps_html = f'<section class="sec"><h2 class="sec">覆盖缺口</h2><ul>{items}</ul></section>'

    method_note = (
        f'<section class="sec"><h2 class="sec">摘要指标</h2><div class="grid-metrics">{metric_html}</div>'
        f'<p class="src-note">{esc(data.get("method", ""))}</p></section>'
    )

    body = (
        f'<header class="hero"><div class="wrap"><h1>{esc(topic)}</h1>'
        f'<div class="sub">追踪窗口 {esc(data.get("window", ""))}</div>'
        f'<div class="meta-pills">{"".join(pills)}</div></div></header>'
        f'<main class="wrap"><a class="skip-link" href="#main">跳到主要内容</a>'
        f'{summary_html}{decision_html}{method_note}{cross_html}{timeline_html}{sources_html}{gaps_html}'
        f'</main><footer>本报告由 hot-news-monitor 专题生成器渲染'
        + (f'（数据文件 {esc(data_file_label)}）' if data_file_label else "")
        + '；未直接核验条目已在页面标注「待核实」。信息等级：已核验 / 部分核验 / 推断 / 待核实。</footer>'
    )
    return (
        '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{esc(topic)} · 热点新闻实时追踪</title>\n'
        f'<style>{_CSS}</style>\n</head>\n<body>\n{body}\n<script>{_JS}</script>\n</body>\n</html>\n'
    )


# ---------------------------------------------------------------- current 页
def match_brief(event_text: str, brief: dict[str, Any]) -> bool:
    text = event_text.lower()
    return any(str(k).lower() in text for k in brief.get("keywords", ()))


def render_current(state: dict[str, Any], manifest: dict[str, Any] | None = None) -> str:
    """按快照 Top1 事件机械生成「当前热点专题」；命中清单关键词时叠加编译层。"""
    manifest = manifest or load_manifest()
    events = list(state.get("events", ()))
    if not events:
        return _shell("当前热点专题", ["<p>快照暂无可用事件，稍后刷新。</p>"], state)
    top = events[0]
    title = str(top.get("title", "")) or "热点事件"
    blob = title + " " + " ".join(i.get("title", "") for i in top.get("items", ()))
    editorial: dict[str, Any] | None = None
    for b in manifest.get("briefs", ()):
        if b.get("status", "active") != "active":
            continue
        if match_brief(blob, b):
            try:
                editorial = json.loads((BRIEF_DIR / str(b["data_file"])).read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError, KeyError):
                editorial = None
            break

    threshold = float(state.get("threshold", 50))
    tier_label, tier_cls = heat_tier(float(top.get("heat", 0)), threshold)
    items = sorted(top.get("items", ()), key=lambda i: i.get("published_at", ""))
    src_rows = []
    for it in items:
        link = (f'<a href="{esc(it["url"])}" target="_blank" rel="noopener noreferrer">原文 ↗</a>'
                if it.get("url") else '<span class="badge pending">示例数据 · 无外部链接</span>')
        src_rows.append(
            f'<tr><td>{esc(it.get("published_at", ""))}</td>'
            f'<td><span class="tier {esc(it.get("tier", ""))}">{esc(TIER_LABEL.get(it.get("tier"), it.get("tier", "")))}</span></td>'
            f'<td>{esc(it.get("source_name", ""))}</td><td>{esc(it.get("title", ""))} {link}</td></tr>'
        )
    src_table = (
        '<div class="table-wrap"><table><thead><tr><th>时间</th><th>层级</th><th>信源</th><th>报道</th></tr></thead>'
        f'<tbody>{"".join(src_rows)}</tbody></table></div>' if src_rows else "<p>暂无关联报道。</p>"
    )
    series = list(top.get("heat_series", ()))
    trend = "趋势采样点：" + (" → ".join(f'{p.get("ts", "")} {p.get("value", 0)}' for p in series[-12:]) if series else "暂无（下一周期累积）")

    body_parts: list[str] = []
    if editorial:
        body_parts.append('<section class="sec"><h2 class="sec">决策摘要（编译层）</h2><ul>'
                          + "".join(f"<li>{esc(x)}</li>" for x in editorial.get("summary_zh", ()))
                          + "</ul></section>")
        card = editorial.get("decision_card")
        if card:
            body_parts.append(
                '<section class="sec"><h2 class="sec">决策卡（编译层）</h2><dl class="decision-card">'
                f'<dt>结论</dt><dd>{esc(card.get("conclusion", ""))}</dd>'
                f'<dt>证据强度</dt><dd>{_strength_badge(card.get("evidence_strength", "中"))}</dd>'
                f'<dt>触发条件</dt><dd>{esc("；".join(card.get("triggers", ())))}</dd>'
                f'<dt>反向证据</dt><dd>{esc("；".join(card.get("counter_evidence", ())))}</dd></dl></section>'
            )
    body_parts.append(
        f'<section class="sec"><h2 class="sec">事件画像</h2><div class="grid-metrics">'
        f'<div class="metric"><div class="v"><span class="heat-badge {tier_cls}">{tier_label}</span></div><div class="k">热度级别（≥{threshold:.0f} 为热）</div></div>'
        f'<div class="metric"><div class="v">{len(top.get("source_ids", ()))}</div><div class="k">独立信源</div></div>'
        f'<div class="metric"><div class="v">{len(items)}</div><div class="k">关联报道</div></div>'
        f'<div class="metric"><div class="v">{esc(top.get("tag", "—"))}</div><div class="k">分类标签</div></div>'
        "</div>"
        f'<p class="src-note">{esc(trend)}</p>'
        f'<p><a class="pill btn" href="http://127.0.0.1:8765/?q={esc(_kw(title))}#event/{esc(top.get("id", ""))}" '
        f'style="border-radius:8px;text-decoration:none;display:inline-block">在看板中打开该事件 ↗</a></p></section>'
    )
    body_parts.append(f'<section class="sec"><h2 class="sec">事件发展时间线（机械聚合）</h2>{src_table}</section>')

    matched_note = ("已命中已登记专题，叠加人工编译层。" if editorial else
                    "未命中已登记专题关键词；本页为纯机械聚合视图。新专题可在 config/briefs/ 登记后自动生效。")
    return _shell(f"热点事件专题 · {title}", body_parts, state,
                  extra_note=f"本页由调度器每次刷新（每 5 分钟）自动重建，标题随当前最热事件轮换。{matched_note}")


def _kw(title: str) -> str:
    return title.split(":")[0][:24]


def _shell(topic: str, body_parts: list[str], state: dict[str, Any], extra_note: str = "") -> str:
    pills = [
        f'<span class="pill">快照 {esc(state.get("generated_at", ""))}</span>',
        f'<span class="pill">模式 {esc(state.get("mode", ""))}</span>',
        '<a class="pill" href="/" style="color:#fff">← 返回实时看板</a>',
        '<a class="pill" href="/report-nvidia.html" style="color:#fff">英伟达专题</a>',
    ]
    note = f'<p class="src-note">{esc(extra_note)}</p>' if extra_note else ""
    body = (
        f'<header class="hero"><div class="wrap"><h1>{esc(topic)}</h1>'
        f'<div class="sub">当前热点自动轮换 · 每 5 分钟随快照重建</div>'
        f'<div class="meta-pills">{"".join(pills)}</div></div></header>'
        f'<main class="wrap"><a class="skip-link" href="#main">跳到主要内容</a>{"".join(body_parts)}{note}</main>'
        f'<footer>由 hot-news-monitor 自动生成；信源纪律与核验口径与实时看板一致。</footer>'
    )
    return (
        '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>{esc(topic)} · 热点新闻实时追踪</title>\n'
        f'<style>{_CSS}</style>\n</head>\n<body>\n{body}\n<script>{_JS}</script>\n</body>\n</html>\n'
    )


def rebuild_all(out_dir: Path | None = None) -> list[Path]:
    """重建：每个 active 专题 -> dashboard/<out_name>（默认 report-<slug>.html），并重建 current 页。"""
    out = out_dir or (APP_ROOT / "dashboard")
    out.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    written: list[Path] = []
    for b in manifest.get("briefs", ()):
        if b.get("status", "active") != "active":
            continue
        data = json.loads((BRIEF_DIR / str(b["data_file"])).read_text(encoding="utf-8"))
        target = out / str(b.get("out_name") or f'brief-{b["slug"]}.html')
        target.write_text(render(data, data_file_label=str(b["data_file"])), encoding="utf-8")
        written.append(target)
    state_path = APP_ROOT / "runtime" / "state.json"
    cur = out / "brief-current.html"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        cur.write_text(render_current(state, manifest), encoding="utf-8")
    else:
        cur.write_text(_shell("当前热点专题",
                              ["<p>实时快照尚未就绪，等待首次抓取（每 5 分钟自动刷新）。</p>"],
                              {"generated_at": "—", "mode": "none"}), encoding="utf-8")
    written.append(cur)
    return written


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m app report-nvidia")
    ap.add_argument("--source", default=str(DEFAULT_SOURCE))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args(argv)
    data = json.loads(Path(args.source).read_text(encoding="utf-8"))
    out = Path(args.out)
    out.write_text(render(data, data_file_label=Path(args.source).name), encoding="utf-8")
    print(f"[report] written {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
