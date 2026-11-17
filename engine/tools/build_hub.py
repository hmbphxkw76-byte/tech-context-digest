"""汇总页生成（CI: ci.yml --check 校验 / html-sync、scheduled-maintenance 重新生成）。

生成 index.html（报告枢纽：居中标题「宏观资讯报告」+ 地区/区域、主题、报告、
报告类型四项统计，下方为筛选栏与报告列表）与 reader.html（在线阅读器：navy 渐变
头部 + sticky 筛选栏 + 侧栏报告列表 + iframe 阅读区，?report=<路径> 直达）。

主题与报告全部由文件系统自动发现（iter_business_dirs + reports/*.html）；
主题元数据（地区 / 主题名 / 报告类型）取自各业务线 prompts/business-config.md，
类型名称解析自 engine/templates/template-registry.md 第二节。新增业务线或报告
后重新生成即可，统计与列表自动更新，无需改动本文件。

视觉设计沿用仓库 canonical 设计令牌（与 content/economy/dubai/apartment 报告及 md2html 对齐）：
navy 渐变 Hero、sticky 筛选栏、chips 标签栏、卡片网格、页脚与回顶按钮。
reader.html 直接复用 index.html 的设计令牌与公共组件（筛选栏 / chips / 卡片 /
页脚 / 回顶），在其上追加阅读器专属布局（头部 / 侧栏 / iframe / 移动端抽屉），
响应式断点与主页一致（960px / 560px）。

--check 模式（ci.yml 使用）：重新计算内容与现有文件比对；
- 文件存在且一致 -> 退出码 0
- 文件存在但过期 -> 退出码 1（阻断合并）
- 文件不存在    -> 退出码 0 并提示（全新克隆尚未生成，由定时维护首建）

退出码（生成模式）：0 = 成功；1 = 写入失败。
"""
from __future__ import annotations

import argparse
import html as html_mod
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (ROOT, TEMPLATE_DIR, iter_business_dirs,  # noqa: E402
                     iter_business_reports, report_title)

CYCLE_LABEL = {"monthly": "月度", "quarterly": "季度", "annual": "年度", "baseline": "基线", "weekly": "周报"}

# 类型标签简称（用于筛选栏 chips；完整名称见 template-registry.md，hover title 展示全称）
TYPE_SHORT = {
    "market-monitoring": "市场动态",
    "trend-weekly": "行业趋势",
    "employment-research": "职业就业",
    "competitive-intelligence": "竞争情报",
    "sentiment-monitoring": "舆情监测",
    "consumer-research": "用户调研",
    "industry-research": "行业研究",
    "market-sizing": "市场规模",
    "investment-research": "投资分析",
    "policy-analysis": "政策法规",
    "feasibility-study": "市场进入",
    "flash-commentary": "快评点评",
    "whitepaper": "白皮书",
    "decision-dashboard": "决策仪表盘",
}

# 类型模板引用正则（与 compliance_check.TYPE_REF_RE 保持一致）
TYPE_REF_RE = re.compile(r"engine/templates/([a-z0-9]+(?:-[a-z0-9]+)*)/")
# template-registry.md 第二节类型清单行：| 类型 ID | 类型名称 | ...
TYPE_ROW_RE = re.compile(r"^\|\s*([a-z0-9]+(?:-[a-z0-9]+)*)\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)
TYPE_SECTION_RE = re.compile(r"##\s*二、已注册类型清单(.*?)(?:\n##\s|\Z)", re.DOTALL)

# 设计令牌与组件样式（canonical，与 content/economy/dubai/apartment 报告 / md2html 对齐）
_STYLE = """\
:root{
  --radius-sm:8px; --radius:12px; --radius-lg:16px; --radius-pill:999px;
  --shadow:0 1px 3px rgba(20,40,70,.06); --shadow-md:0 4px 14px rgba(20,40,70,.09);
  --shadow-lg:0 10px 30px rgba(15,35,56,.2);
  --space-1:4px; --space-2:8px; --space-3:12px; --space-4:16px; --space-5:24px; --space-6:32px;
  --font-sans:"Microsoft YaHei","PingFang SC","Segoe UI",Arial,sans-serif;
  --font-mono:"SFMono-Regular",Consolas,"Liberation Mono",monospace;
  --focus-ring:0 0 0 3px rgba(63,111,176,.35);
  --transition:.15s ease;
  --bg:#f4f6f9; --card:#ffffff; --ink:#15202b; --ink2:#465667; --ink3:#657180;
  --line:#e1e7ee; --line2:#eef2f6;
  --navy:#16324f; --navy2:#2f5597; --blue:#3f6fb0; --blue-l:#eaf1fa;
  --red:#a83224; --red-d:#822116; --red-l:#fbece8;
  --pre:#b8541c; --pre-l:#fdf1e4;
  --green:#1c7444; --green-l:#eaf5ef;
  --amber:#956612; --amber-l:#fdf4e2;
  --gray:#646f7b; --gray-l:#eff2f4;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{font-family:var(--font-sans);background:var(--bg);color:var(--ink);line-height:1.76;font-size:14.5px}
a{color:var(--navy2);text-decoration:none}
a:hover{text-decoration:underline}

/* ── Hero：居中标题 + 四项统计 ── */
.hero{background:linear-gradient(128deg,#0f2338 0%,#16324f 52%,#2f5597 100%);
  color:#fff;padding:30px 40px 36px;text-align:center}
.hero h1{font-size:45px;font-weight:700;letter-spacing:.5px;line-height:1.3}
.hero .stats{display:flex;flex-wrap:wrap;justify-content:center;gap:14px;margin-top:28px}
.hero .stat{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22);
  border-radius:var(--radius);padding:14px 26px;min-width:128px;
  font-size:13px;color:rgba(255,255,255,.85)}
.hero .stat b{display:block;font-size:26px;font-weight:700;color:#fff;
  letter-spacing:.5px;line-height:1.3}

/* ── 筛选栏 ── */
.filterbar{position:sticky;top:0;z-index:40;
  background:rgba(244,246,249,.95);backdrop-filter:blur(6px);
  border-bottom:1px solid var(--line);padding:12px 24px;
  display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.filterbar>input{flex:1;min-width:200px;max-width:360px;padding:8px 14px;
  border:1px solid var(--line);border-radius:18px;font-size:13.5px;background:#fff;
  outline:none;font-family:inherit;color:var(--ink)}
.filterbar>input:focus{border-color:var(--blue);box-shadow:var(--focus-ring)}
.chips{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.chips .chips-label{font-size:12px;color:var(--ink3);margin-right:2px;white-space:nowrap}
.chip{border:1px solid var(--line);background:#fff;border-radius:14px;padding:4px 12px;
  font-size:12.5px;color:var(--ink2);cursor:pointer;user-select:none;font-family:inherit;
  transition:background var(--transition),border-color var(--transition),color var(--transition)}
.chip:hover{border-color:var(--blue)}
.chip.on{background:var(--navy);border-color:var(--navy);color:#fff}
.chips-type{flex-basis:100%;flex-wrap:wrap;gap:5px;min-width:0}
.chips-type .chip{font-size:12px;padding:3px 10px}
.filterbar .count{font-size:12px;color:var(--ink3);margin-left:auto;white-space:nowrap}

/* ── 主区：地区 → 主题 → 报告 ── */
.main{max-width:1240px;margin:0 auto;padding:8px 24px 50px}
.region{margin-bottom:12px}
.region-head{display:flex;align-items:baseline;gap:10px;margin:26px 0 4px}
.region-head h2{font-size:20px;color:var(--navy)}
.region-head .rcount{font-size:11.5px;color:var(--ink3)}
.topic{margin:18px 0 6px;scroll-margin-top:64px}
.topic-head{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;
  border-left:4px solid var(--navy2);padding:2px 0 2px 12px;margin:0 0 12px}
.topic-head h3{font-size:17px;color:var(--navy)}
.topic-head .badge{font-size:11px;border-radius:3px;padding:1px 7px;background:var(--blue-l);
  color:var(--navy2);white-space:nowrap;font-weight:600}
.topic-head .count{font-size:11.5px;color:var(--ink3);margin-left:auto;white-space:nowrap}
.reports{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));
  gap:14px;margin:0 0 6px}
.rcard{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:14px 16px;display:flex;flex-direction:column;gap:6px;box-shadow:var(--shadow);
  transition:border-color var(--transition),box-shadow var(--transition)}
.rcard:hover{border-color:#c9d6e6;box-shadow:var(--shadow-md)}
.rcard .row1{display:flex;align-items:center;gap:8px}
.tag{display:inline-block;font-size:11px;padding:1px 7px;border-radius:10px;
  background:#eef3f8;color:var(--navy);border:1px solid var(--line);white-space:nowrap}
.rcard .period{font-size:12px;color:var(--ink3);font-variant-numeric:tabular-nums}
.rcard h4{font-size:14.5px;color:var(--navy);line-height:1.5}
.rcard h4 a{color:var(--navy)}
.rcard .path{font-size:11px;color:var(--ink3);font-family:var(--font-mono);
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.noresult{padding:44px 20px;text-align:center;color:var(--ink3);font-size:13.5px;
  grid-column:1/-1}

/* ── 页脚 / 回到顶部 ── */
.footer{text-align:center;color:var(--ink3);font-size:11.5px;padding:26px 20px 36px;
  line-height:1.9;border-top:1px solid var(--line)}
.totop{position:fixed;right:22px;bottom:22px;width:40px;height:40px;border-radius:50%;
  background:var(--navy);color:#fff;border:0;font-size:17px;cursor:pointer;
  box-shadow:0 4px 14px rgba(15,35,56,.3);opacity:0;pointer-events:none;
  transition:opacity var(--transition);z-index:70;font-family:inherit}
.totop.show{opacity:1;pointer-events:auto}

/* ── 跳转链接 / 打印 ── */
.skip-link{position:absolute;left:12px;top:-48px;z-index:100;background:var(--navy);color:#fff;
  padding:8px 16px;border-radius:0 0 8px 8px;font-size:12.5px;transition:top var(--transition)}
.skip-link:focus{top:0;color:#fff;text-decoration:none}
@media print{
  .filterbar,.totop,.skip-link{display:none}
  body{background:#fff}
  .main{padding:0}
}

/* ── 响应式 ── */
@media (max-width:960px){
  .filterbar{padding:10px 14px}
  .filterbar>input{max-width:none}
  .hero{padding:26px 22px 28px}
  .hero h1{font-size:36px}
  .main{padding:6px 14px 40px}
  .reports{grid-template-columns:1fr}
  .totop{right:14px;bottom:14px}
}
@media (max-width:560px){
  .hero{padding:20px 16px 20px}
  .hero h1{font-size:31.5px}
  .hero .stats{gap:10px;margin-top:22px}
  .hero .stat{min-width:calc(50% - 5px);padding:12px 14px}
  .topic-head h3{font-size:15.5px}
  .filterbar .count{margin-left:0;width:100%}
}
"""

_SCRIPT = """\
(function () {
  var qInput = document.getElementById('hub-search');
  var countEl = document.getElementById('hub-count');
  var noResult = document.createElement('div');
  noResult.className = 'noresult';
  noResult.textContent = '未找到匹配的报告，请调整关键词或筛选条件。';
  noResult.style.display = 'none';
  document.querySelector('.main').appendChild(noResult);

  var state = { q: '', topic: 'all', type: 'all' };

  function applyFilter() {
    var visibleReports = 0;
    var visibleTopics = 0;
    document.querySelectorAll('.topic').forEach(function (topicEl) {
      var okTopic = state.topic === 'all' || topicEl.dataset.topic === state.topic;
      var okType = state.type === 'all' || topicEl.dataset.type === state.type;
      var shownInTopic = 0;
      topicEl.querySelectorAll('.rcard').forEach(function (card) {
        var okQ = !state.q || card.dataset.search.indexOf(state.q) >= 0;
        var show = okTopic && okType && okQ;
        card.style.display = show ? '' : 'none';
        if (show) { shownInTopic++; visibleReports++; }
      });
      var topicVisible = shownInTopic > 0;
      topicEl.style.display = topicVisible ? '' : 'none';
      if (topicVisible) visibleTopics++;
      var tc = topicEl.querySelector('.js-topic-count');
      if (tc) tc.textContent = shownInTopic + ' 份报告';
    });
    document.querySelectorAll('.region').forEach(function (reg) {
      var shownInRegion = Array.prototype.filter.call(
        reg.querySelectorAll('.topic'), function (t) { return t.style.display !== 'none'; }).length;
      reg.style.display = shownInRegion ? '' : 'none';
      var rc = reg.querySelector('.js-region-count');
      if (rc) rc.textContent = shownInRegion + ' 个主题';
    });
    noResult.style.display = visibleReports ? 'none' : '';
    countEl.textContent = '共 ' + visibleTopics + ' 个主题 · ' + visibleReports + ' 份报告';
  }

  var t;
  qInput.addEventListener('input', function () {
    clearTimeout(t);
    t = setTimeout(function () {
      state.q = qInput.value.trim().toLowerCase();
      applyFilter();
    }, 120);
  });

  function bindChips(wrapId, key) {
    var wrap = document.getElementById(wrapId);
    wrap.addEventListener('click', function (e) {
      var btn = e.target.closest('.chip');
      if (!btn) return;
      wrap.querySelectorAll('.chip').forEach(function (c) {
        c.classList.remove('on');
        c.setAttribute('aria-pressed', 'false');
      });
      btn.classList.add('on');
      btn.setAttribute('aria-pressed', 'true');
      state[key] = btn.dataset[key];
      applyFilter();
    });
  }
  bindChips('chips-topic', 'topic');
  bindChips('chips-type', 'type');

  var totop = document.getElementById('totop');
  window.addEventListener('scroll', function () {
    totop.classList.toggle('show', window.scrollY > 400);
  });
  totop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  applyFilter();
})();
"""

# 阅读器专属样式：直接拼在 _STYLE 之后，复用主页全部设计令牌与公共组件
# （筛选栏 / chips / rcard / 页脚 / 回顶），仅追加阅读器特有布局与响应式规则。
_READER_STYLE = """\

/* ── 阅读器：头部 ── */
body{display:flex;flex-direction:column;height:100vh;overflow:hidden}
.reader-head{background:linear-gradient(128deg,#0f2338 0%,#16324f 52%,#2f5597 100%);
  color:#fff;padding:14px 24px;flex:0 0 auto}
.reader-head-inner{max-width:1240px;margin:0 auto;display:flex;align-items:center;
  gap:12px;flex-wrap:wrap}
.reader-brand{display:flex;align-items:baseline;gap:8px;font-size:17px;font-weight:700;
  letter-spacing:.3px;min-width:0}
.reader-brand .brand-link{color:#fff;white-space:nowrap}
.reader-brand .brand-link:hover{text-decoration:underline}
.reader-brand .brand-sep{opacity:.55;font-weight:400}
.reader-brand .brand-sub{font-size:12.5px;font-weight:400;opacity:.85;white-space:nowrap}
.reader-head-stats{margin-left:auto;font-size:12px;color:rgba(255,255,255,.88);
  white-space:nowrap;font-variant-numeric:tabular-nums}
.menu-btn{display:none;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);
  color:#fff;border-radius:var(--radius-sm);width:36px;height:32px;font-size:16px;
  line-height:1;cursor:pointer;font-family:inherit}
.menu-btn:hover{background:rgba(255,255,255,.24)}

/* ── 阅读器：阅读区布局 ── */
.reader-body{flex:1;min-height:0;display:grid;
  grid-template-columns:300px 1fr;grid-template-rows:minmax(0,1fr)}
.sidebar{background:var(--bg);border-right:1px solid var(--line);overflow-y:auto;
  min-height:0;padding-bottom:20px}
.sidebar-head{position:sticky;top:0;z-index:5;background:rgba(244,246,249,.95);
  backdrop-filter:blur(6px);border-bottom:1px solid var(--line);padding:10px 16px;
  font-size:13px;font-weight:600;color:var(--navy);display:flex;align-items:center;
  justify-content:space-between;gap:8px}
.sidebar-head .count{font-weight:400;color:var(--ink3)}
.sidebar-nav{padding:2px 12px 0}
.sidebar-nav .region{margin-bottom:4px}
.sidebar-nav .region-head{margin:12px 0 2px}
.sidebar-nav .region-head h2{font-size:14px}
.sidebar-nav .topic{margin:6px 0 2px;scroll-margin-top:0}
.sidebar-nav .topic-head{border-left-width:3px;padding:1px 0 1px 9px;margin:0 0 5px}
.sidebar-nav .topic-head h3{font-size:13px}
.sidebar-nav .topic-head .badge{font-size:10px;padding:0 5px}
.sidebar-nav .topic-head .count{font-size:10.5px}
.sidebar-nav .reports{display:block;margin:0}
.sidebar-nav .rcard{padding:9px 11px;gap:4px;cursor:pointer}
.sidebar-nav .rcard h4{font-size:13px;line-height:1.45}
.sidebar-nav .rcard .path{font-size:10px}
.sidebar-nav .rcard.active{border-color:var(--navy2);box-shadow:var(--shadow-md)}
.sidebar-nav .noresult{padding:18px 8px;font-size:12.5px;text-align:center}
.reader-main{position:relative;min-width:0;min-height:0;background:var(--bg)}
.reader-main iframe{width:100%;height:100%;border:0;display:block;background:var(--card)}
.empty{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;
  justify-content:center;gap:6px;color:var(--ink3);text-align:center;padding:20px;
  font-size:13.5px}
.empty[hidden]{display:none}
.empty-icon{font-size:34px;opacity:.5;line-height:1}
.overlay{display:none}

/* ── 阅读器：响应式（断点与主页一致） ── */
@media (max-width:960px){
  .reader-head{padding:12px 14px}
  .reader-head-stats{display:none}
  .menu-btn{display:block}
  .reader-body{grid-template-columns:1fr}
  .sidebar{position:fixed;top:0;left:0;bottom:0;width:300px;max-width:84vw;z-index:60;
    transform:translateX(-102%);transition:transform var(--transition);
    box-shadow:var(--shadow-lg);border-right:1px solid var(--line)}
  .sidebar.open{transform:translateX(0)}
  .overlay{display:block;position:fixed;inset:0;background:rgba(15,35,56,.45);z-index:55;
    opacity:0;pointer-events:none;transition:opacity var(--transition)}
  .overlay.show{opacity:1;pointer-events:auto}
}
@media (max-width:560px){
  .reader-brand{font-size:15px}
  .sidebar{width:280px}
}
@media print{
  .reader-head,.sidebar,.overlay,.totop,.skip-link{display:none}
  body{height:auto;overflow:visible}
  .reader-body{display:block}
}
"""

_READER_SCRIPT = """\
(function () {
  var qInput = document.getElementById('reader-search');
  var countEl = document.getElementById('reader-count');
  var sidebarCountEl = document.getElementById('sidebar-count');
  var frame = document.getElementById('frame');
  var emptyEl = document.getElementById('empty');
  var sidebar = document.getElementById('sidebar');
  var overlay = document.getElementById('overlay');
  var menuBtn = document.getElementById('menuBtn');
  var nav = document.getElementById('sidebar-nav');

  var noResult = document.createElement('div');
  noResult.className = 'noresult';
  noResult.textContent = '未找到匹配的报告，请调整关键词或筛选条件。';
  noResult.style.display = 'none';
  nav.appendChild(noResult);

  var state = { q: '', topic: 'all', type: 'all' };

  function applyFilter() {
    var visibleReports = 0;
    var visibleTopics = 0;
    nav.querySelectorAll('.topic').forEach(function (topicEl) {
      var okTopic = state.topic === 'all' || topicEl.dataset.topic === state.topic;
      var okType = state.type === 'all' || topicEl.dataset.type === state.type;
      var shownInTopic = 0;
      topicEl.querySelectorAll('.rcard').forEach(function (card) {
        var okQ = !state.q || card.dataset.search.indexOf(state.q) >= 0;
        var show = okTopic && okType && okQ;
        card.style.display = show ? '' : 'none';
        if (show) { shownInTopic++; visibleReports++; }
      });
      var topicVisible = shownInTopic > 0;
      topicEl.style.display = topicVisible ? '' : 'none';
      if (topicVisible) visibleTopics++;
      var tc = topicEl.querySelector('.js-topic-count');
      if (tc) tc.textContent = shownInTopic + ' 份报告';
    });
    nav.querySelectorAll('.region').forEach(function (reg) {
      var shownInRegion = Array.prototype.filter.call(
        reg.querySelectorAll('.topic'), function (t) { return t.style.display !== 'none'; }).length;
      reg.style.display = shownInRegion ? '' : 'none';
      var rc = reg.querySelector('.js-region-count');
      if (rc) rc.textContent = shownInRegion + ' 个主题';
    });
    noResult.style.display = visibleReports ? 'none' : '';
    countEl.textContent = '共 ' + visibleTopics + ' 个主题 · ' + visibleReports + ' 份报告';
    if (sidebarCountEl) sidebarCountEl.textContent = visibleReports + ' 份报告';
  }

  var t;
  qInput.addEventListener('input', function () {
    clearTimeout(t);
    t = setTimeout(function () {
      state.q = qInput.value.trim().toLowerCase();
      applyFilter();
    }, 120);
  });

  function bindChips(wrapId, key) {
    var wrap = document.getElementById(wrapId);
    wrap.addEventListener('click', function (e) {
      var btn = e.target.closest('.chip');
      if (!btn) return;
      wrap.querySelectorAll('.chip').forEach(function (c) {
        c.classList.remove('on');
        c.setAttribute('aria-pressed', 'false');
      });
      btn.classList.add('on');
      btn.setAttribute('aria-pressed', 'true');
      state[key] = btn.dataset[key];
      applyFilter();
    });
  }
  bindChips('reader-chips-topic', 'topic');
  bindChips('reader-chips-type', 'type');

  function closeDrawer() {
    sidebar.classList.remove('open');
    overlay.classList.remove('show');
    menuBtn.setAttribute('aria-expanded', 'false');
  }

  function openDrawer() {
    sidebar.classList.add('open');
    overlay.classList.add('show');
    menuBtn.setAttribute('aria-expanded', 'true');
  }

  menuBtn.addEventListener('click', function () {
    if (sidebar.classList.contains('open')) { closeDrawer(); } else { openDrawer(); }
  });
  overlay.addEventListener('click', closeDrawer);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeDrawer(); }
  });

  function selectReport(path, title) {
    frame.src = path;
    emptyEl.hidden = true;
    nav.querySelectorAll('.rcard').forEach(function (c) {
      c.classList.toggle('active', c.dataset.path === path);
    });
    if (history.replaceState) {
      history.replaceState(null, '', '?report=' + encodeURIComponent(path));
    }
    if (title) { document.title = title + ' · 宏观资讯报告 · 阅读器'; }
    closeDrawer();
    var active = nav.querySelector('.rcard.active');
    if (active && active.scrollIntoView) { active.scrollIntoView({ block: 'nearest' }); }
  }

  nav.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="?report="]');
    if (!a) return;
    e.preventDefault();
    var card = a.closest('.rcard');
    if (!card) return;
    selectReport(card.dataset.path, a.textContent.trim());
  });

  // 初始加载：?report=<路径>（仅接受列表内已知报告，避免任意 src 注入）
  var p = new URLSearchParams(location.search).get('report');
  if (p) {
    var cards = nav.querySelectorAll('.rcard');
    for (var i = 0; i < cards.length; i++) {
      if (cards[i].dataset.path === p) {
        var a = cards[i].querySelector('a');
        selectReport(p, a ? a.textContent.trim() : '');
        break;
      }
    }
  }

  // 阅读器为 app-shell（外层不滚动）：回顶按钮作用于侧栏与报告内容
  var totop = document.getElementById('totop');
  sidebar.addEventListener('scroll', function () {
    totop.classList.toggle('show', sidebar.scrollTop > 400);
  });
  totop.addEventListener('click', function () {
    sidebar.scrollTo({ top: 0, behavior: 'smooth' });
    try { frame.contentWindow.scrollTo({ top: 0, behavior: 'smooth' }); } catch (e) {}
  });

  applyFilter();
})();
"""


@dataclass
class ReportEntry:
    cycle: str
    period: str
    path: str
    title: str


@dataclass
class Topic:
    rel: str
    region: str
    name: str
    type_id: str
    type_name: str
    reports: list[ReportEntry] = field(default_factory=list)


def parse_type_names() -> dict[str, str]:
    """从 template-registry.md 第二节解析 类型 ID -> 类型名称。"""
    f = TEMPLATE_DIR / "template-registry.md"
    if not f.exists():
        return {}
    text = f.read_text(encoding="utf-8", errors="replace")
    m = TYPE_SECTION_RE.search(text)
    section = m.group(1) if m else text
    return {tid: name.strip() for tid, name in TYPE_ROW_RE.findall(section)}


def parse_business_meta(config_path: Path) -> tuple[str | None, str | None, str | None]:
    """解析 business-config.md 的 {{REGION}} / {{TOPIC}} / 类型模板引用。"""
    if not config_path.exists():
        return None, None, None
    text = config_path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\{\{REGION\}\}\s*=\s*(.+)", text)
    region = m.group(1).strip() if m else None
    m = re.search(r"\{\{TOPIC\}\}\s*=\s*(.+)", text)
    topic = m.group(1).strip() if m else None
    m = TYPE_REF_RE.search(text)
    type_id = m.group(1) if m else None
    return region, topic, type_id


def collect_topics() -> list[Topic]:
    """自动发现全部业务线（主题）与其报告。"""
    type_names = parse_type_names()
    topics: list[Topic] = []
    for b in iter_business_dirs():
        region, name, type_id = parse_business_meta(b.path / "prompts" / "business-config.md")
        region = region or b.region
        name = name or b.property_type
        type_id = type_id or ""
        type_name = type_names.get(type_id, type_id or "未分类")
        reports: list[ReportEntry] = []
        for ref in iter_business_reports(b, include_archives=False, include_legacy=False):
            if ref.category != "report" or not ref.cycle:
                continue
            text = (ROOT / ref.rel).read_text(encoding="utf-8", errors="replace")
            reports.append(ReportEntry(ref.cycle, ref.period, ref.rel, report_title(text)))
        reports.sort(key=lambda e: e.period, reverse=True)
        topics.append(Topic(b.rel, region, name, type_id, type_name, reports))
    return topics


def group_by_region(topics: list[Topic]) -> list[tuple[str, list[Topic]]]:
    """按地区分组，保留业务线出现顺序。"""
    regions: list[tuple[str, list[Topic]]] = []
    index: dict[str, int] = {}
    for t in topics:
        if t.region not in index:
            index[t.region] = len(regions)
            regions.append((t.region, []))
        regions[index[t.region]][1].append(t)
    return regions


def _esc(text: str) -> str:
    return html_mod.escape(text, quote=True)


def _search_text(topic: Topic, report: ReportEntry) -> str:
    return " ".join([
        topic.region, topic.name, topic.type_name, topic.rel,
        CYCLE_LABEL.get(report.cycle, report.cycle), report.period, report.title, report.path,
    ]).lower()


def render_hub(topics: list[Topic]) -> str:
    regions = group_by_region(topics)
    n_topics = len(topics)
    n_reports = sum(len(t.reports) for t in topics)
    n_regions = len(regions)
    n_types = len({t.type_id for t in topics if t.type_id})

    # 类型清单：全部 13 个已注册类型（按注册表顺序）
    all_types = list(parse_type_names().items())

    parts = [
        "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">",
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        "<title>宏观资讯报告</title>",
        f"<style>{_STYLE}</style>\n</head>\n<body>",
        '<a class="skip-link" href="#main-content">跳到主要内容</a>',
        '<section class="hero">',
        "<h1>宏观资讯报告</h1>",
        '<div class="stats">',
        f'<div class="stat"><b>{n_regions}</b>区域</div>',
        f'<div class="stat"><b>{n_topics}</b>主题</div>',
        f'<div class="stat"><b>{n_reports}</b>报告</div>',
        f'<div class="stat"><b>{n_types}</b>类型</div>',
        "</div>",
        "</section>",
        '<div class="filterbar">',
        '<input id="hub-search" type="search" placeholder="搜索主题 / 报告标题…" aria-label="搜索主题或报告">',
        '<div class="chips" id="chips-topic" role="group" aria-label="主题筛选">',
        '<span class="chips-label">主题</span>',
        '<button class="chip on" data-topic="all" aria-pressed="true">全部主题</button>',
    ]
    for t in topics:
        parts.append(
            f'<button class="chip" data-topic="{_esc(t.rel)}" aria-pressed="false">{_esc(t.name)}</button>'
        )
    parts += [
        "</div>",
        '<div class="chips chips-type" id="chips-type" role="group" aria-label="类型筛选">',
        '<span class="chips-label">类型</span>',
        '<button class="chip on" data-type="all" aria-pressed="true">全部类型</button>',
    ]
    for tid, tname in all_types:
        short = TYPE_SHORT.get(tid, tname)
        parts.append(
            f'<button class="chip" data-type="{_esc(tid)}" aria-pressed="false" '
            f'title="{_esc(tname)}">{_esc(short)}</button>'
        )
    parts += [
        "</div>",
        '<span class="count" id="hub-count"></span>',
        "</div>",
        '<main class="main" id="main-content">',
    ]

    if not topics:
        parts.append("<p>暂无已产出报告。</p>")

    for region_name, region_topics in regions:
        parts.append(f'<section class="region" data-region="{_esc(region_name)}">')
        parts.append(
            f'<div class="region-head"><h2>{_esc(region_name)}</h2>'
            f'<span class="rcount js-region-count">{len(region_topics)} 个主题</span></div>'
        )
        for t in region_topics:
            parts.append(
                f'<section class="topic" id="topic-{_esc(t.rel.replace("/", "-"))}" '
                f'data-topic="{_esc(t.rel)}" data-type="{_esc(t.type_id)}">'
            )
            parts.append(
                f'<div class="topic-head"><h3>{_esc(t.name)}</h3>'
                f'<span class="badge">{_esc(t.type_name)}</span>'
                f'<span class="count js-topic-count">{len(t.reports)} 份报告</span></div>'
            )
            if t.reports:
                parts.append('<div class="reports">')
                for r in t.reports:
                    label = CYCLE_LABEL.get(r.cycle, r.cycle)
                    title = _esc(r.title or r.period)
                    parts.append(
                        f'<article class="rcard" data-search="{_esc(_search_text(t, r))}">'
                        f'<div class="row1"><span class="tag">{_esc(label)}</span>'
                        f'<span class="period">{_esc(r.period)}</span></div>'
                        f'<h4><a href="{_esc(r.path)}" target="_blank" rel="noopener" '
                        f'title="{title}">{title}</a></h4>'
                        f'<div class="path">{_esc(r.path)}</div>'
                        f"</article>"
                    )
                parts.append("</div>")
            else:
                parts.append(
                    '<div class="noresult">该主题暂无已产出报告。</div>'
                )
            parts.append("</section>")
        parts.append("</section>")

    parts += [
        "</main>",
        '<footer class="footer">',
        "<p>由 <code>engine/tools/build_hub.py</code> 自动生成 · "
        "报告源文件见各业务线 <code>reports/</code> 目录</p>",
        "</footer>",
        '<button class="totop" id="totop" aria-label="回到顶部">↑</button>',
        f"<script>{_SCRIPT}</script>",
        "</body>\n</html>",
    ]
    return "\n".join(parts)


def render_reader(topics: list[Topic]) -> str:
    """在线阅读器：与 index.html 同一设计系统（_navy 渐变头部 + sticky 筛选栏 +
    侧栏报告列表 + iframe 阅读区），复用主页公共组件与交互逻辑。"""
    regions = group_by_region(topics)
    n_topics = len(topics)
    n_reports = sum(len(t.reports) for t in topics)
    n_regions = len(regions)
    n_types = len({t.type_id for t in topics if t.type_id})
    all_types = list(parse_type_names().items())

    parts = [
        "<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">",
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        "<title>宏观资讯报告 · 阅读器</title>",
        f"<style>{_STYLE}{_READER_STYLE}</style>\n</head>\n<body>",
        '<a class="skip-link" href="#main-content">跳到主要内容</a>',
        '<header class="reader-head">',
        '<div class="reader-head-inner">',
        '<div class="reader-brand">',
        '<a class="brand-link" href="index.html">宏观资讯报告</a>',
        '<span class="brand-sep">·</span><span class="brand-sub">阅读器</span>',
        "</div>",
        f'<div class="reader-head-stats">{n_regions} 区域 · {n_topics} 主题 · '
        f"{n_reports} 报告 · {n_types} 类型</div>",
        '<button class="menu-btn" id="menuBtn" aria-label="打开报告列表" '
        'aria-expanded="false" aria-controls="sidebar">☰</button>',
        "</div>",
        "</header>",
        '<div class="filterbar">',
        '<input id="reader-search" type="search" placeholder="搜索主题 / 报告标题…" '
        'aria-label="搜索主题或报告">',
        '<div class="chips" id="reader-chips-topic" role="group" aria-label="主题筛选">',
        '<span class="chips-label">主题</span>',
        '<button class="chip on" data-topic="all" aria-pressed="true">全部主题</button>',
    ]
    for t in topics:
        parts.append(
            f'<button class="chip" data-topic="{_esc(t.rel)}" '
            f'aria-pressed="false">{_esc(t.name)}</button>'
        )
    parts += [
        "</div>",
        '<div class="chips chips-type" id="reader-chips-type" role="group" aria-label="类型筛选">',
        '<span class="chips-label">类型</span>',
        '<button class="chip on" data-type="all" aria-pressed="true">全部类型</button>',
    ]
    for tid, tname in all_types:
        short = TYPE_SHORT.get(tid, tname)
        parts.append(
            f'<button class="chip" data-type="{_esc(tid)}" aria-pressed="false" '
            f'title="{_esc(tname)}">{_esc(short)}</button>'
        )
    parts += [
        "</div>",
        '<span class="count" id="reader-count"></span>',
        "</div>",
        '<div class="reader-body">',
        '<aside class="sidebar" id="sidebar" aria-label="报告列表">',
        '<div class="sidebar-head"><span>报告列表</span>'
        '<span class="count" id="sidebar-count"></span></div>',
        '<nav class="sidebar-nav" id="sidebar-nav">',
    ]

    if not topics:
        parts.append('<div class="noresult">暂无已产出报告。</div>')

    for region_name, region_topics in regions:
        parts.append(f'<section class="region" data-region="{_esc(region_name)}">')
        parts.append(
            f'<div class="region-head"><h2>{_esc(region_name)}</h2>'
            f'<span class="rcount js-region-count">{len(region_topics)} 个主题</span></div>'
        )
        for t in region_topics:
            parts.append(
                f'<section class="topic" data-topic="{_esc(t.rel)}" '
                f'data-type="{_esc(t.type_id)}">'
            )
            parts.append(
                f'<div class="topic-head"><h3>{_esc(t.name)}</h3>'
                f'<span class="badge">{_esc(t.type_name)}</span>'
                f'<span class="count js-topic-count">{len(t.reports)} 份报告</span></div>'
            )
            if t.reports:
                parts.append('<div class="reports">')
                for r in t.reports:
                    label = CYCLE_LABEL.get(r.cycle, r.cycle)
                    title = _esc(r.title or r.period)
                    parts.append(
                        f'<article class="rcard" data-path="{_esc(r.path)}" '
                        f'data-search="{_esc(_search_text(t, r))}">'
                        f'<div class="row1"><span class="tag">{_esc(label)}</span>'
                        f'<span class="period">{_esc(r.period)}</span></div>'
                        f'<h4><a href="?report={_esc(r.path)}" title="{title}">{title}</a></h4>'
                        f'<div class="path">{_esc(r.path)}</div>'
                        f"</article>"
                    )
                parts.append("</div>")
            else:
                parts.append('<div class="noresult">该主题暂无已产出报告。</div>')
            parts.append("</section>")
        parts.append("</section>")

    parts += [
        "</nav>",
        "</aside>",
        '<div class="overlay" id="overlay"></div>',
        '<main class="reader-main" id="main-content">',
        '<iframe id="frame" title="报告内容"></iframe>',
        '<div class="empty" id="empty">',
        '<div class="empty-icon">📄</div>',
        "<p>请从左侧选择一份报告开始阅读</p>",
        "<p>使用搜索或筛选快速定位主题与类型</p>",
        "</div>",
        "</main>",
        "</div>",
        '<footer class="footer">',
        "<p>由 <code>engine/tools/build_hub.py</code> 自动生成 · "
        "报告源文件见各业务线 <code>reports/</code> 目录</p>",
        "</footer>",
        '<button class="totop" id="totop" aria-label="回到顶部">↑</button>',
        f"<script>{_READER_SCRIPT}</script>",
        "</body>\n</html>",
    ]
    return "\n".join(parts)


def build_outputs() -> dict[str, str]:
    topics = collect_topics()
    return {"index.html": render_hub(topics), "reader.html": render_reader(topics)}


GENERATED_TS_RE = re.compile(r'(<p class="muted">最近生成：)[^<]*(</p>)')


def normalize_for_check(text: str) -> str:
    """--check 比对专用归一化：抹平「最近生成」生成时刻时间戳（不参与一致性判定）。

    纯函数，供 tests/ 直接调用。
    """
    return GENERATED_TS_RE.sub(r"\g<1>TIMESTAMP\g<2>", text)


def compare_outputs(outputs: dict[str, str]) -> tuple[list[str], list[str]]:
    """现有汇总页与重算内容比对 -> (stale, missing)。"""
    stale: list[str] = []
    missing: list[str] = []
    for name, content in outputs.items():
        f = ROOT / name
        if not f.exists():
            missing.append(name)
        elif normalize_for_check(f.read_text(encoding="utf-8", errors="replace")) != normalize_for_check(content):
            stale.append(name)
    return stale, missing


def main() -> int:
    ap = argparse.ArgumentParser(description="生成汇总页 index.html / reader.html")
    ap.add_argument("--check", action="store_true", help="校验现有汇总页是否为最新")
    args = ap.parse_args()

    outputs = build_outputs()
    if args.check:
        stale, missing = compare_outputs(outputs)
        if stale:
            print(f"[ERROR] 汇总页已过期：{', '.join(stale)}（运行 python engine/tools/build_hub.py 重新生成）")
            return 1
        if missing:
            print(f"[WARN] 汇总页尚未生成：{', '.join(missing)}（由定时维护首建，不阻断）")
            return 0
        print("汇总页校验通过：index.html / reader.html 均为最新")
        return 0

    try:
        for name, content in outputs.items():
            (ROOT / name).write_text(content, encoding="utf-8")
    except OSError as e:
        print(f"[ERROR] 写入汇总页失败: {e}")
        return 1
    n_topics = len(collect_topics())
    print(f"汇总页已生成：index.html / reader.html（{n_topics} 个主题）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
