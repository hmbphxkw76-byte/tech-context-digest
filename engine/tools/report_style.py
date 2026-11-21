"""canonical 报告样式（设计系统单一事实源）。

背景：仓库报告曾并存三套样式——
  1. md2html.py 的通用极简样式（#1a1a2e / Segoe UI）；
  2. trends 周报的 report-head 富样式（--navy:#123a5c）；
  3. apartment 的富样式（monthly/quarterly/baseline 用 --navy:#1f3d63，
     annual 已与 hub 对齐为 --navy:#16324f）。

本模块把 canonical 定为：**hub 的设计令牌（--navy:#16324f 等）+ trends 的
report-head 组件结构（页头 / sticky 导航 / KPI 卡 / 图表 / 时间线）**，并并入
apartment 已有的组件（kcard / stat-strip / src-head 弹层 / pill / note
/ toc / tiers / flow / risk / redbox / prebox 等），使全部报告共用同一套设计系统。

用法：
  - `md2html.py` 用 `CANONICAL_CSS` 渲染 md 源报告；
  - `restyle_reports.py` 用 `CANONICAL_CSS` 替换既有报告的 <style> 块；
  - 报告 HTML 仍逐份内联本 CSS（满足 monitoring-common-spec「自包含」要求）。
"""
from __future__ import annotations

# ── 设计令牌：与 hub（engine/tools/build_hub.py 的 _STYLE）保持同一套数值 ──
TOKENS = """\
:root{
  --radius-sm:8px; --radius:12px; --radius-lg:16px; --radius-pill:999px;
  --shadow:0 1px 3px rgba(20,40,70,.06); --shadow-md:0 4px 14px rgba(20,40,70,.09);
  --shadow-lg:0 10px 30px rgba(15,35,56,.2);
  --font-sans:"Microsoft YaHei","PingFang SC","Segoe UI",Arial,sans-serif;
  --font-mono:"SFMono-Regular",Consolas,"Liberation Mono",monospace;
  --focus-ring:0 0 0 3px rgba(63,111,176,.35);
  --transition:.15s ease;
  --bg:#f4f6f9; --card:#ffffff; --card2:#fbfcfe; --soft:#f5f8fb;
  --ink:#15202b; --ink2:#465667; --ink3:#657180;
  --line:#e1e7ee; --line2:#eef2f6;
  --navy:#16324f; --navy2:#2f5597; --blue:#3f6fb0; --blue-l:#eaf1fa;
  --red:#a83224; --red-d:#822116; --red-l:#fbece8; --red-bg:#fbece8; --red-line:#f0d4cf;
  --pre:#b8541c; --pre-l:#fdf1e4; --pre-bg:#fdf1e4; --pre-line:#f2ddc9;
  --green:#1c7444; --green-l:#eaf5ef; --green-bg:#eaf5ef; --green-line:#d3ead9;
  --amber:#956612; --amber-l:#fdf4e2; --amber-bg:#fdf4e2; --amber-line:#f0e3c2;
  --gray:#646f7b; --gray-l:#eff2f4; --gray-bg:#eff2f4; --gray-line:#e6eaee;
  /* 别名：兼容既有报告组件的命名习惯 */
  --surface:#ffffff; --surface2:#fbfcfe;
  --navy-2:#2f5597; --muted:#657180; --bg-soft:#f5f8fb; --bg-card:#fbfcfe;
}
"""

# ── 基础：令牌 / 排版 / 页头 / 导航 / 章节 / 表格 / 来源 / 卡片 / 组件 ──
BASE = """\
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}
}
body{font-family:var(--font-sans);background:var(--bg);color:var(--ink);line-height:1.76;font-size:14.5px}
.wrap{max-width:1160px;margin:0 auto;padding:0 24px 64px}
a{color:var(--navy2);text-decoration:none}
a:hover{text-decoration:underline}
a:focus-visible,button:focus-visible{outline:none;box-shadow:var(--focus-ring)}
.skip-link{position:absolute;left:12px;top:-48px;z-index:100;background:var(--navy);color:#fff;padding:8px 16px;border-radius:0 0 8px 8px;font-size:12.5px;transition:top var(--transition)}
.skip-link:focus{top:0;color:#fff;text-decoration:none}

/* ── 页头：report-head（生成器基础版） ── */
header.report-head{
  background:linear-gradient(128deg,#0f2338 0%,var(--navy) 52%,var(--navy2) 100%);
  color:#fff;padding:40px 0 30px;
}
header.report-head .wrap{padding:0 24px}
header.report-head h1{margin:0 0 8px;font-size:27px;font-weight:700;letter-spacing:.4px;line-height:1.35}
header.report-head .eyebrow{font-size:11.5px;letter-spacing:2.4px;color:rgba(255,255,255,.62);text-transform:uppercase}
header.report-head .sub{font-size:14px;color:rgba(255,255,255,.82);margin:2px 0}
header.report-head .meta{font-size:12.3px;color:rgba(255,255,255,.75);margin-top:14px;line-height:1.9}
header.report-head .meta b{color:#fff}
header.report-head .nav-url{font-size:11.5px;color:rgba(255,255,255,.78);margin-top:10px;word-break:break-all}
header.report-head .nav-url a{color:#cfe0ee;text-decoration:none;border-bottom:1px dashed #cfe0ee}
header.report-head .tag{display:inline-block;background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.2);border-radius:14px;padding:2px 11px;margin:5px 6px 0 0;font-size:11.5px}

/* ── 页头：hero（jp-life-work 风格：navy 标题带 + 浅色 meta 面板） ── */
.hero{margin-bottom:20px}
.hero .wrap{padding:0 24px}
.hero-band{background:linear-gradient(128deg,#0f2338 0%,var(--navy) 52%,var(--navy2) 100%);color:#fff;
  padding:14px 0 12px;border-radius:0 0 14px 14px}
.hero-top{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.hero-band .eyebrow,.hero-band .kicker,.hero-band .hero-kicker{font-size:10.5px;letter-spacing:2px;color:rgba(255,255,255,.62);text-transform:uppercase;margin:0}
.hero-band h1{font-size:21px;font-weight:700;letter-spacing:.3px;margin:5px 0 0;line-height:1.3}
.hero-band .tags{display:flex;flex-wrap:wrap;gap:6px}
.hero-band .tag{display:inline-block;background:rgba(255,255,255,.11);border:1px solid rgba(255,255,255,.2);
  border-radius:14px;padding:1px 10px;font-size:11px}
.hero-panel{display:flex;flex-wrap:wrap;align-items:center;gap:8px 16px;
  background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:8px 12px;margin-top:8px;box-shadow:var(--shadow)}
.meta-grid{flex:1 1 0;min-width:0;column-count:2;column-gap:20px;
  font-size:11.4px;line-height:1.45;color:var(--ink2)}
.meta-grid .meta-item{break-inside:avoid;margin:0 0 2px;min-width:0;overflow-wrap:anywhere}
.meta-grid .meta-item b{color:var(--navy)}
.meta-grid p,.meta-grid dl,.meta-grid .hero-meta,.meta-grid .hero-abstract p{
  margin:0 0 4px;break-inside:avoid}
.meta-grid dl{display:block}
.meta-grid dt{display:block;font-weight:700;color:var(--navy);margin-top:2px}
.meta-grid dd{display:block;margin:0 0 4px}
.meta-grid .tag-row{margin:2px 0 4px}
.hero-panel .audit-badge{margin:0;flex:0 0 300px;font-size:12px;padding:6px 12px}
.audit-badge{display:inline-flex;align-items:center;gap:10px;flex-wrap:wrap;
  background:var(--green-l);border:1px solid var(--green);border-radius:10px;
  padding:8px 14px;font-size:12.5px;color:var(--green)}
.audit-badge .audit-seal{font-weight:700;white-space:nowrap}
.audit-badge .audit-meta{color:var(--ink2)}
@media (max-width:900px){
  .hero-panel{flex-direction:column;align-items:stretch}
  .hero-panel .audit-badge{flex:1 1 auto}
  .meta-grid{column-count:1}
}

/* ── 顶部固定导航 ── */
nav.report-nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.96);border-bottom:1px solid var(--line);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);margin-bottom:26px}
nav.report-nav .wrap{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center;padding-top:10px;padding-bottom:10px}
/* apartment monthly/quarterly/baseline 的 .nav-tabs 是 nav 直接子元素（无 .wrap） */
nav.report-nav > .nav-tabs{max-width:1160px;margin:0 auto;padding:10px 24px}
.nav-url{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;font-size:11.5px;line-height:1.6;color:var(--ink3);padding-bottom:6px;margin-bottom:6px;border-bottom:1px dashed var(--line);width:100%}
.nav-url-label{font-weight:700;color:var(--ink2);white-space:nowrap}
.nav-url a{color:var(--blue);text-decoration:none;word-break:break-all}
.nav-url a:hover{text-decoration:underline}
.nav-tabs{display:flex;flex-wrap:wrap;gap:6px}
.nav-tabs a{color:var(--navy);text-decoration:none;font-size:12.5px;padding:4px 10px;border-radius:14px;border:1px solid var(--line);background:var(--bg-soft);white-space:nowrap;transition:background var(--transition),color var(--transition)}
.nav-tabs a:hover{background:var(--blue-l);border-color:#b9cfe2;text-decoration:none}
.nav-tabs a.active{background:var(--blue-l);color:var(--blue);font-weight:700}

/* ── 章节与排版 ── */
main{padding-top:0}
h2.sec{font-size:19px;color:var(--navy);margin:38px 0 14px;padding-bottom:8px;border-bottom:2px solid var(--navy);scroll-margin-top:100px;font-weight:700}
h2.sec .en{font-size:10.8px;color:var(--ink3);font-weight:400;margin-left:10px;letter-spacing:1.1px}
h3{font-size:15.5px;color:var(--navy);margin:22px 0 8px;font-weight:700;scroll-margin-top:100px}
h4{font-size:14px;color:var(--navy);margin:16px 0 6px;font-weight:700}
p{margin:8px 0}
ul,ol{margin:8px 0;padding-left:22px}
li{margin:5px 0}
ul.tight,ol.tight{margin:7px 0}
ul.tight li,ol.tight li{margin-bottom:6px}
b,strong{font-weight:650;color:var(--ink)}
blockquote{border-left:4px solid var(--line);margin:12px 0;padding:2px 0 2px 14px;color:var(--ink2)}
code{background:var(--bg-soft);padding:2px 5px;border-radius:4px;font-family:var(--font-mono);font-size:.92em}
pre{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius-sm);padding:12px 14px;overflow-x:auto;margin:12px 0}
pre code{background:none;padding:0}
img{max-width:100%}
.lead{color:var(--ink2);font-size:13.8px;margin:6px 0 14px}
.muted{color:var(--ink3)}
.small{font-size:11.7px;color:var(--ink3)}
hr{border:0;border-top:1px solid var(--line);margin:26px 0 0}
.hr{height:1px;background:var(--line);margin:26px 0 0}
b.red,color.red{color:var(--red)} b.pre{color:var(--pre)} b.green{color:var(--green)}
b.amber{color:var(--amber)} b.navy{color:var(--navy)}

/* ── 表格 ── */
table{width:100%;border-collapse:collapse;font-size:13px;background:var(--card);margin:12px 0}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;line-height:1.62}
thead th{background:var(--navy);color:#fff;font-weight:600;white-space:nowrap}
tbody th{background:var(--blue-l);color:var(--navy);font-weight:600}
tbody tr:nth-child(even) td{background:var(--bg-soft)}
tbody tr:hover td{background:var(--blue-l)}
table.fixed{table-layout:fixed}
.num{text-align:right;font-variant-numeric:tabular-nums}
.tblwrap{overflow-x:auto;border-radius:var(--radius-sm);border:1px solid var(--line);margin:12px 0}
.tblwrap table{margin:0;border:0}

/* ── 来源：表头弹层 / 行内链接 / 来源清单 ── */
.src-head{position:relative;cursor:help;border-bottom:1px dotted var(--blue);white-space:nowrap}
.src-head .src-pop{position:absolute;left:0;top:100%;z-index:60;display:none;background:var(--navy);color:#fff;font-size:12px;font-weight:400;padding:9px 12px;border-radius:8px;box-shadow:var(--shadow-lg);max-width:min(560px,86vw);white-space:normal;line-height:1.65;border:1px solid rgba(255,255,255,.14)}
.src-pop .pop-title{font-weight:600;display:block;margin-bottom:4px;color:#fff}
.src-pop .pop-url{display:block;margin-top:6px;word-break:break-all;color:var(--blue-l)}
.src-pop .pop-url a{color:#a9c8ee}
.src-head:hover .src-pop,.src-head:focus .src-pop,.src-head:focus-within .src-pop{display:block}
.src-inline{color:var(--ink3);font-size:12px;word-break:break-all}
.src-inline a{color:var(--blue);text-decoration:none;border-bottom:1px dotted var(--blue)}
.src-inline a:hover{background:#eaf3fa}
.src{font-size:11.1px;color:var(--ink3);word-break:break-word;line-height:1.58}
.src a{color:#5b7bb4;text-decoration:none}
.src a:hover{text-decoration:underline}
.refs{font-size:12.5px;color:var(--ink3)}
.refs ol{padding-left:20px}
.refs a{color:var(--navy);text-decoration:none;border-bottom:1px dashed var(--navy);word-break:break-all}
.refs a:hover{background:#e8f0f8}

/* ── 卡片 / 结论框 ── */
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:18px 20px;box-shadow:var(--shadow);margin:14px 0}
.card.tight{padding:14px 16px}
.leadbox{border-left:4px solid var(--navy2);background:linear-gradient(125deg,#f5f9fd,#edf3fa);border-color:#cfdded}
.leadbox h3:first-child{margin-top:0}

/* ── KPI 卡（trends .kpi / apartment .kcard） ── */
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:12px;margin:14px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--navy);border-radius:var(--radius-sm);padding:12px 14px;box-shadow:var(--shadow)}
.kpi.red{border-left-color:var(--red)} .kpi.green{border-left-color:var(--green)}
.kpi.amber{border-left-color:var(--amber)} .kpi.blue{border-left-color:var(--blue)}
.kpi .v{font-size:22px;font-weight:700;color:var(--navy);line-height:1.2}
.kpi.red .v{color:var(--red)} .kpi.green .v{color:var(--green)}
.kpi.amber .v{color:var(--amber)} .kpi.blue .v{color:var(--blue)}
.kpi .l{font-size:12px;color:var(--ink3);margin-top:4px}
.kpi .s{font-size:11px;color:#8a98a6;margin-top:2px}
.kcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:11px;margin:14px 0}
.kcard{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--navy2);border-radius:10px;padding:13px 15px;box-shadow:var(--shadow)}
.kcard.warn,.kcard.pre{border-left-color:var(--pre);background:linear-gradient(180deg,var(--pre-bg),#fff 62%)}
.kcard.bad,.kcard.red{border-left-color:var(--red);background:linear-gradient(180deg,var(--red-bg),#fff 62%)}
.kcard.good{border-left-color:var(--green);background:linear-gradient(180deg,var(--green-bg),#fff 62%)}
.kcard .lab,.kcard .t{font-size:12.4px;color:var(--ink2)}
.kcard .val,.kcard .v{font-size:22px;font-weight:700;color:var(--navy);margin:3px 0 2px;line-height:1.25}
.kcard.warn .val,.kcard.pre .val{color:var(--pre)}
.kcard.bad .val,.kcard.red .val{color:var(--red)}
.kcard.good .val{color:var(--green)}
.kcard .note,.kcard .s{font-size:11.5px;color:var(--ink3);line-height:1.6;margin-top:4px;word-break:break-word}

/* ── 数据条 / 信号灯 ── */
.stat-strip{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:12px 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:11px 13px;text-align:center}
.stat .lab,.stat .l{font-size:11.4px;color:var(--ink3);margin-top:2px}
.stat .n{font-size:23px;font-weight:700;line-height:1.2}
.stat.hard .n{color:var(--red)} .stat.pre .n{color:var(--pre)} .stat.yel .n{color:var(--amber)}
.stat.grn .n{color:var(--green)} .stat.gry .n{color:var(--gray)}
.lamp{display:inline-block;min-width:9px;width:9px;height:9px;border-radius:50%;margin-right:4px;vertical-align:0}
.lamp.r{background:var(--red)} .lamp.p{background:var(--pre)} .lamp.y{background:var(--amber)}
.lamp.g{background:var(--green)} .lamp.k{background:var(--gray)}

/* ── 标签 / 标注 ── */
.tag{display:inline-block;font-size:11px;padding:1px 7px;border-radius:10px;background:var(--blue-l);color:var(--navy);border:1px solid var(--line);margin-right:4px}
.tag.red{background:var(--red-l);color:var(--red);border-color:var(--red-line)}
.tag.green{background:var(--green-l);color:var(--green);border-color:var(--green-line)}
.tag.amber{background:var(--amber-l);color:var(--amber);border-color:var(--amber-line)}
.pill{display:inline-block;border-radius:3px;padding:0 7px;font-size:11.3px;white-space:nowrap;line-height:1.72}
.pill.r{background:var(--red-l);color:var(--red)} .pill.p{background:var(--pre-l);color:var(--pre)}
.pill.y{background:var(--amber-l);color:var(--amber)} .pill.g{background:var(--green-l);color:var(--green)}
.pill.k{background:var(--gray-l);color:var(--gray)} .pill.b{background:var(--blue-l);color:var(--navy2)}
.pill.act{background:#e8eef6;color:#2b4a70}
.callout{border-left:4px solid var(--amber);background:var(--amber-l);padding:12px 16px;border-radius:0 6px 6px 0;margin:14px 0;font-size:13.5px}
.callout.red{border-left-color:var(--red);background:var(--red-l)}
.callout.green{border-left-color:var(--green);background:var(--green-l)}
.note{border:1px solid var(--line);border-left:4px solid var(--navy2);background:var(--card2);border-radius:var(--radius-sm);padding:12px 15px;margin:14px 0;font-size:13.5px}
.note.gap{border-left-color:var(--gray);background:var(--gray-l)}
.note.check{border-left-color:var(--green);background:var(--green-l)}
.note.correct{border-left-color:var(--red);background:var(--red-l)}
.note.preline{border-left-color:var(--pre);background:var(--pre-l)}
.term{font-size:12.5px;color:var(--ink3);background:var(--bg-soft);border:1px solid var(--line);border-radius:6px;padding:8px 12px;margin:14px 0}
.term b{color:var(--navy)}

/* ── 图表（trends .chart 卡片 / apartment .chart-box + .chart-eh 容器） ── */
.chart{margin:18px 0;padding:16px;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
.chart h4{margin:0 0 4px;font-size:14.5px;color:var(--navy)}
.chart .unit{font-size:12px;color:var(--ink3);font-weight:400}
.chart-note{font-size:11.5px;color:var(--ink3);margin:0 0 12px;line-height:1.7}
.chart svg{display:block;max-width:100%;height:auto;margin:6px auto 0}
.chart-box{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:14px 14px 6px;box-shadow:var(--shadow);margin:16px 0}
.chart-eh{width:100%;height:352px;margin:6px 0}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:12px;color:var(--ink2);margin:6px 0 12px}
.legend span{display:inline-flex;align-items:center;gap:5px}
.legend i{display:inline-block;width:11px;height:11px;border-radius:2px}

/* ── 时间线 ── */
.timeline{margin:16px 0;padding-left:8px}
.tl-item{display:flex;gap:14px;margin:0 0 14px}
.tl-date{flex:0 0 78px;font-size:12.5px;font-weight:700;color:var(--navy);text-align:right;padding-top:2px}
.tl-body{flex:1;border-left:2px solid var(--line);padding:0 0 0 14px;position:relative}
.tl-body::before{content:"";position:absolute;left:-6px;top:6px;width:10px;height:10px;border-radius:50%;background:var(--navy);border:2px solid #fff;box-shadow:0 0 0 1px var(--navy)}
.tl-body.red::before{background:var(--red);box-shadow:0 0 0 1px var(--red)}
.tl-body.green::before{background:var(--green);box-shadow:0 0 0 1px var(--green)}
.tl-body.amber::before{background:var(--amber);box-shadow:0 0 0 1px var(--amber)}
.tl-body .t{font-weight:600;color:var(--ink)}
.tl-body .d{font-size:13px;color:var(--ink3);margin-top:2px}

/* ── 风险条 / 风险框 ── */
.rl-track{position:relative;height:12px;background:var(--gray-line);border-radius:999px;margin:14px 0 6px;overflow:hidden}
.rl-fill{position:absolute;left:0;top:0;bottom:0;background:var(--green);border-radius:999px}
.rl-marker{position:absolute;top:-3px;bottom:-3px;width:2px;background:var(--red);left:50%}
.risk{background:linear-gradient(125deg,#fdf3f1,var(--red-l));border:1px solid #eec8c1;border-left:5px solid var(--red);border-radius:10px;padding:16px 18px;margin:14px 0}
.risk h4{font-size:14.4px;color:var(--red);margin-bottom:8px}
.risk .kpis{display:flex;flex-wrap:wrap;gap:22px;margin:10px 0 12px}
.risk .kpis>div{min-width:150px}
.risk .kpis .n{font-size:22px;font-weight:700;color:var(--red);line-height:1.25}
.risk .kpis .l{font-size:11.4px;color:var(--ink2)}
.redbox{background:linear-gradient(135deg,#fff8f6,var(--red-l));border:1px solid #eec8c1;border-left:5px solid var(--red);border-radius:10px;padding:15px 18px;margin:14px 0}
.redbox h4{color:var(--red-d);margin-top:0}
.prebox{background:linear-gradient(135deg,#fffaf4,var(--pre-l));border:1px solid #efd3b6;border-left:5px solid var(--pre);border-radius:10px;padding:15px 18px;margin:14px 0}
.prebox h4{color:var(--pre);margin-top:0}
.preline{border-left:4px solid var(--pre);background:var(--pre-l);padding:10px 14px;border-radius:0 6px 6px 0;margin:10px 0;font-size:13px}

/* ── 目录 / 流程 / 分层（年度） ── */
.toc{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 6px}
.toc a{font-size:12.3px;color:var(--navy2);background:var(--blue-l);border-radius:15px;padding:3px 12px;text-decoration:none}
.toc a:hover{background:#dae6f5}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.flow{display:flex;align-items:stretch;gap:7px;flex-wrap:wrap;margin:12px 0}
.node{flex:1;min-width:150px;background:var(--blue-l);border:1px solid #cfddf3;border-radius:8px;padding:11px 12px}
.node b{display:block;color:var(--navy);font-size:12.8px;margin-bottom:3px}
.node span{font-size:11.4px;color:var(--ink2);line-height:1.55;display:block}
.arrow{display:flex;align-items:center;color:var(--blue);font-size:18px;font-weight:700}
.tiers{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0}
.tier{border:1px solid var(--line);border-radius:10px;padding:14px 15px;background:var(--card)}
.tier.t1{border-top:4px solid var(--red)} .tier.t2{border-top:4px solid var(--pre)} .tier.t3{border-top:4px solid var(--amber)}
.tier h4{margin:0 0 6px} .tier p{font-size:12.2px;color:var(--ink2);margin:0}

/* ── 标注 / 页脚 / 索引链接 ── */
.disc{margin-top:34px;padding:16px 18px;background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);font-size:13px;color:var(--ink3)}
.disc strong{color:var(--ink)}
footer,.footer{font-size:11.4px;color:var(--ink3);text-align:center;margin-top:22px;line-height:1.8}
.idx-link{color:var(--navy);text-decoration:none;border-bottom:1px dotted #9db9da;font-weight:600}
.idx-link:hover{color:var(--navy2);border-bottom:1px solid var(--blue)}
.idx-link .ext{font-size:10px;color:var(--blue);margin-left:2px;font-weight:400}

/* ── 消费端反馈入口（T-06）：静态链接 + data 属性占位，无外部依赖 ── */
.feedback-link{color:var(--navy2);text-decoration:none;border-bottom:1px dotted #9db9da;font-weight:600}
.feedback-link:hover{color:var(--navy);border-bottom:1px solid var(--blue)}
.report-foot{border-top:1px solid var(--line);padding:16px 0 34px}

/* ── 报告特有组件（apartment 基线 / 季度） ── */
.tldr{background:linear-gradient(180deg,#fff,#f8fafe);border-left:5px solid var(--navy2)}
.verdict{font-size:17px;font-weight:700;color:var(--blue);margin:0 0 12px}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0}
.tbl-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px;margin:12px 0}
.src-pop .src-pop-title{display:block;font-size:11px;color:var(--ink3);margin-bottom:4px;border-bottom:1px solid var(--line);padding-bottom:4px}
.t-red{background:var(--red-l);color:var(--red)} .t-green{background:var(--green-l);color:var(--green)}
.t-amber{background:var(--amber-l);color:var(--amber)} .t-grey{background:var(--gray-l);color:var(--ink3)}
.t-blue{background:var(--blue-l);color:var(--blue)}
.toggle{display:inline-flex;border:1px solid var(--line);border-radius:6px;overflow:hidden;margin-bottom:8px}
.toggle button{border:0;background:#fff;color:var(--ink2);padding:5px 14px;font-size:12px;cursor:pointer;font-family:inherit}
.toggle button.on{background:var(--navy2);color:#fff}
.hide{display:none}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.layer{display:grid;grid-template-columns:110px 1fr;gap:0;border:1px solid var(--line);border-radius:8px;overflow:hidden;margin-bottom:10px;background:#fff}
.layer .lb{background:var(--navy2);color:#fff;padding:14px 12px;font-weight:700;font-size:13px;display:flex;align-items:center;justify-content:center;text-align:center}
.layer .lb.q{background:#4472C4} .layer .lb.y{background:var(--navy2)}
.layer .ct{padding:12px 16px;font-size:12.5px;color:var(--ink2)}
.layer .ct b{color:var(--ink)}
.note-box{background:var(--amber-l);border:1px solid var(--amber-line);border-radius:8px;padding:12px 16px;color:#6b4e0a;font-size:12.5px;margin:12px 0}
.risk-box{background:var(--red-l);border:1px solid var(--red-line);border-radius:8px;padding:12px 16px;color:#8c2f24;font-size:12.5px;margin:12px 0}
.ok-box{background:var(--green-l);border:1px solid var(--green-line);border-radius:8px;padding:12px 16px;color:#155c39;font-size:12.5px;margin:12px 0}
.sig-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:12px}
.sig{display:flex;gap:12px;align-items:flex-start;border:1px solid var(--line);border-radius:8px;padding:11px 13px;background:#fff}
.sig .dot{width:10px;height:10px;border-radius:50%;margin-top:6px;flex:0 0 10px}
.sig .dot.r{background:var(--red)} .sig .dot.g{background:var(--green)}
.sig .dot.a{background:var(--amber)} .sig .dot.k{background:var(--gray)}
.sig b{font-size:13px;color:var(--ink)} .sig p{margin:2px 0 0;font-size:11.5px}
b.dr{color:var(--red-d)}
.metric-link{color:var(--navy);text-decoration:none;border-bottom:1px dotted #9db4cf;font-weight:600}
.metric-link:hover{color:var(--navy2);border-bottom-color:var(--navy2);background:var(--blue-l)}
.metric-link::after{content:" ↗";font-size:10px;color:#7d96b3;font-weight:400}
.rl-banner{background:linear-gradient(125deg,#5c1512,#7a1f19 60%,#8a2b20);color:#fff;border-radius:12px;padding:16px 20px;margin:16px 0;border:1px solid #4d100d;box-shadow:0 2px 8px rgba(110,27,22,.18)}
.rl-banner h3{color:#fff;margin:0 0 6px;font-size:16px}
.rl-banner p{font-size:12.8px;color:rgba(255,255,255,.88);margin-bottom:6px}
.rl-banner .rl-kpis{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0 4px}
.rl-banner .rl-kpis div{background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.18);border-radius:8px;padding:8px 12px;min-width:156px}
.rl-banner .n{font-size:20px;font-weight:700;line-height:1.3}
.rl-banner .l{font-size:11.4px;color:rgba(255,255,255,.78)}
.rl-card{border:2px solid var(--red-d);background:linear-gradient(180deg,#fff,#fdf6f4);border-radius:12px;padding:18px 20px;margin:16px 0;box-shadow:0 2px 8px rgba(110,27,22,.08)}
.rl-card h3{color:var(--red-d);margin-top:0}
.rl-table th{background:var(--red-d)}
.rl-table tbody tr:nth-child(even) td{background:#fdf7f5}
.rl-table tbody tr:hover td{background:var(--red-l)}
.rl-table td:first-child{border-left:3px solid var(--red-d)}
.rl-rule{background:#fdf6f4;border-left:4px solid var(--red-d);padding:10px 14px;border-radius:0 7px 7px 0;font-size:12.8px;margin:10px 0}
.rl-mark{display:inline-block;background:var(--red-d);color:#fff;border-radius:3px;padding:0 6px;font-size:11px;font-weight:700;letter-spacing:.5px}
details.registry{margin:12px 0;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px}
details.registry summary{cursor:pointer;font-weight:700;color:var(--navy);font-size:14px}
details.registry[open]{padding-bottom:18px}
.mini{background:#fff;border:1px solid var(--line);border-radius:9px;padding:12px 14px}
.mini h4{margin-top:0}

/* ── 信息等级标签（四级，信息分层规范） ── */
.lvl{display:inline-block;font-size:11px;line-height:1.5;padding:1px 7px;border-radius:9px;
  border:1px solid transparent;white-space:nowrap;font-weight:600;vertical-align:1px}
.lvl-verified{background:var(--green-l);color:var(--green);border-color:var(--green-line,#d3ead9)}
.lvl-partial{background:var(--amber-l);color:var(--amber);border-color:var(--amber-line,#f0e3c2)}
.lvl-inferred{background:var(--blue-l);color:var(--navy2);border-color:#cdddf0}
.lvl-assumption{background:var(--gray-l);color:var(--gray);border-color:var(--gray-line,#e6eaee)}

/* ── 新增信息统计条（本期新增/修正/无变化/假设核验进度） ── */
.delta-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0}
.delta-strip .d{background:var(--card);border:1px solid var(--line);border-radius:10px;
  padding:12px 14px;box-shadow:var(--shadow)}
.delta-strip .d .n{font-size:22px;font-weight:700;color:var(--navy);line-height:1.25}
.delta-strip .d .l{font-size:11.6px;color:var(--ink3);margin-top:2px}
.delta-strip .d.add .n{color:var(--green)}
.delta-strip .d.fix .n{color:var(--amber)}
.delta-strip .d.same .n{color:var(--ink3)}
.delta-strip .d.hyp .n{color:var(--navy2)}

/* ── 行动协议卡（触发条件+阈值+责任角色+时限+验证指标） ── */
.action-card{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--navy2);
  border-radius:10px;padding:14px 16px;margin:12px 0;box-shadow:var(--shadow)}
.action-card.immediate{border-left-color:var(--red)}
.action-card.watch{border-left-color:var(--amber)}
.action-card.archive{border-left-color:var(--gray)}
.action-card .a-head{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px}
.action-card .a-title{font-weight:700;color:var(--navy);font-size:14.5px}
.action-card .a-meta{font-size:12.3px;color:var(--ink2);line-height:1.7}
.action-card .a-meta b{color:var(--navy)}
.prio{display:inline-block;font-size:11px;padding:1px 8px;border-radius:9px;font-weight:700}
.prio.immediate{background:var(--red-l);color:var(--red)}
.prio.watch{background:var(--amber-l);color:var(--amber)}
.prio.archive{background:var(--gray-l);color:var(--gray)}

/* ── 决策卡（结论/证据强度/触发条件/反向证据/信息充分度） ── */
.decision-card{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:16px 18px;margin:14px 0;box-shadow:var(--shadow)}
.decision-card .dc-head{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:8px}
.decision-card .dc-title{font-weight:700;color:var(--navy);font-size:15px}
.decision-card .dc-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px 18px;font-size:12.8px;line-height:1.7}
.decision-card .dc-grid .k{color:var(--ink3);font-weight:600}
.suff{display:inline-block;font-size:11px;padding:1px 8px;border-radius:9px;font-weight:700}
.suff.ok{background:var(--green-l);color:var(--green)}
.suff.need{background:var(--amber-l);color:var(--amber)}
.ev-strong{color:var(--green);font-weight:700}
.ev-mid{color:var(--amber);font-weight:700}
.ev-weak{color:var(--red);font-weight:700}

/* ── 场景切片 / 事实卡片指针 ── */
.slice{border:1px dashed var(--navy2);border-radius:10px;padding:12px 16px;margin:12px 0;background:var(--blue-l)}
.slice .slice-head{font-weight:700;color:var(--navy);margin-bottom:4px}
.fact-ref{font-family:var(--font-mono);font-size:11.5px;color:var(--navy2);
  background:var(--blue-l);border:1px solid #cdddf0;border-radius:5px;padding:0 5px;white-space:nowrap}

/* ── 响应式 / 打印 ── */
@media (max-width:720px){
  body{font-size:14px}
  .wrap{padding:0 14px 48px}
  header.report-head{padding:26px 0 22px}
  header.report-head h1{font-size:21px}
  .hero-band{padding:12px 0 10px}
  .hero-band h1{font-size:19px}
  nav.report-nav .nav-url{display:none}
  table{display:block;overflow-x:auto;white-space:nowrap}
  th,td{padding:7px 8px;font-size:12.5px}
  .chart-eh{height:300px}
  .grid2,.tiers{grid-template-columns:1fr}
  .kpi-grid{grid-template-columns:repeat(2,1fr)}
  .two-col,.sig-grid{grid-template-columns:1fr}
  .stat-strip{grid-template-columns:repeat(2,1fr)}
  .delta-strip{grid-template-columns:repeat(2,1fr)}
  .decision-card .dc-grid{grid-template-columns:1fr}
  .tl-date{flex-basis:64px;font-size:11.5px}
}
@media print{
  nav.report-nav,.skip-link{display:none}
  .card,.chart,.kpi,.kcard,.chart-box{box-shadow:none}
  body{font-size:12px}
}
"""

CANONICAL_CSS = TOKENS + BASE

# ── 消费端反馈入口（T-06）──────────────────────────────────────────────
# 静态链接指向仓库 issue 追踪器（见 engine/docs/agents/issue-tracker.md），
# 不引入外部反馈服务；data-feedback 属性供后续接线消费侧指标
# （metrics-dictionary.json 的 consumer_metrics_draft，当前 probe 未接线）。
FEEDBACK_URL = (
    "https://github.com/hmbphxkw76-byte/tech-context-digest/issues/new"
    "?title=%E5%8F%8D%E9%A6%88%20/%20%E7%BA%A0%E9%94%99"
)
FEEDBACK_ATTR = "consumer-feedback-v1"


def feedback_link(label: str = "反馈 / 纠错") -> str:
    """返回 canonical 反馈入口链接（hub 页脚 / 报告页脚共用，无 JS 依赖）。"""
    return (f'<a class="feedback-link" data-feedback="{FEEDBACK_ATTR}" '
            f'href="{FEEDBACK_URL}" target="_blank" rel="noopener">{label}</a>')


def report_foot() -> str:
    """返回 canonical 报告页脚（``.report-foot``，置于 ``</main>`` 之后）。

    单一事实源：监控通用规范 §5 要求每份报告页脚含「反馈 / 纠错」入口。
    由 ``restyle_reports.py --add-footer`` 与生成器共用，避免各处手写。
    """
    return f'<footer class="report-foot"><p>{feedback_link()}</p></footer>'


def style_block() -> str:
    """返回 <style> 块（供报告内联，满足自包含要求）。"""
    return f"<style>\n{CANONICAL_CSS}\n</style>"
