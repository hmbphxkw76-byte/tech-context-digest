# 页面构建通用规范（PAGE-BUILD-SPEC v1.0）

> **状态**：现行规范
> **适用范围**：本仓库全部 HTML 页面——枢纽页（`index.html` / `reader.html`）、各业务线报告页（`reports/*.html`），以及后续一切新增主题 / 业务线 / 页面。
> **事实源**：设计令牌与组件样式以 `engine/tools/report_style.py::CANONICAL_CSS`（报告）与 `engine/tools/build_hub.py::_STYLE`（hub）为准；本文档是人类可读规范，与代码冲突时以代码为准并同步修订本文。
> **配套**：落地与门禁见 [page-build-governance.md](./page-build-governance.md)；自动校验见 `engine/tools/page_build_check.py`。
> **最后更新**：2026-11-16

---

## 一、三条不可协商的底线

1. **一个设计系统**：全部页面共用 canonical 令牌与组件，禁止私建主色 / 私有样式分支。
2. **一个事实源**：样式由 `report_style.py` / `build_hub.py` 生成并内联，禁止手工维护平行样式副本。
3. **一个门禁**：所有页面必须通过 `page_build_check.py`，新主题接入必须全绿。

背景：2026-11-14 前仓库并存三套页面样式（md2html 通用极简、trends `report-head`、apartment 专属令牌），根因是交付方式由各业务线自定、缺少统一页面构建标准。本规范把已确认的设计系统、结构骨架、组件、性能 / 可访问性 / 兼容性 / 体验要求固化为唯一标准，并通过 CI 与生成器从机制上防止漂移。

---

## 二、页面分类与骨架

### 2.1 分类

| 类别 | 页面 | 生成方式 | 断点 |
|---|---|---|---|
| **H1 枢纽页** | `index.html`（报告枢纽）、`reader.html`（在线阅读器） | `engine/tools/build_hub.py` 生成 | 960px / 560px |
| **H2 报告页** | 各业务线 `reports/*.html` | 手写 或 `engine/tools/md2html.py` 生成 | 720px |
| **H3 新主题页** | 未来新增主题 / 业务线的报告页 | 同 H2 | 720px |

### 2.2 H1 枢纽页骨架

**`index.html`**：Hero（居中标题 + 四项统计：区域 / 主题 / 报告 / 类型）→ sticky 筛选栏（搜索框 + 主题 chips + 类型 chips + 计数）→ 地区 → 主题 → 报告卡片 → 页脚 → 回顶按钮。

**`reader.html`**：navy 渐变头部（品牌链回 `index.html` + 四项统计 + 移动端 ☰）→ sticky 筛选栏 → 阅读区（侧栏：地区 → 主题 → `.rcard`；右侧 `iframe`）→ 空态 → 页脚 → 回顶按钮。移动端（≤960px）侧栏为**抽屉**（☰ + 遮罩 + Esc 关闭，选中报告后自动收起）。

### 2.3 H2/H3 报告页骨架

```
<header class="report-head">   <!-- apartment 用同义类 .hero -->
  <div class="wrap">
    <h1>标题</h1>
    <p class="sub">副标题（可选）</p>
    <p class="meta">数据截止 / 版本 / 口径说明</p>
  </div>
</header>
<nav class="report-nav" aria-label="报告导航">
  <div class="wrap">
    <div class="nav-url">报告 URL：<a href="...">...</a></div>   <!-- 周期报告（月/季/年）强制 -->
    <div class="nav-tabs"><a href="#s1">一、...</a>...</div>
  </div>
</nav>
<main class="wrap">
  <h2 class="sec" id="s1">一、...</h2>
  ...
</main>
```

**结构约束**：

- `<h2 class="sec" id="sN">` 与 `.nav-tabs a[href="#sN"]` 逐字对应；章节顺序编号 s1..sN。
- `.wrap` 是唯一宽度容器（`max-width:1160px` 居中）；正文不得脱离 `.wrap` 直接全宽。
- 报告为 **app-shell 或长文档**二选一：长文档允许整页滚动；固定高度 shell 须保证侧栏 / 内容区内部滚动、页面不溢出。

---

## 三、设计系统（canonical 令牌）

**唯一数值来源**：`engine/tools/report_style.py::TOKENS`（报告）与 `engine/tools/build_hub.py` 的 `_STYLE`（hub）。两类页面共享下表数值（由 `test_hub_tokens_match_canonical` 保证）。

| 令牌 | 值 | 用途 |
|---|---|---|
| `--navy` | `#16324f` | 主色：标题、表头、强调 |
| `--navy2` | `#2f5597` | 次强调、链接、左边框 |
| `--blue` | `#3f6fb0` | 链接、信息 |
| `--bg` | `#f4f6f9` | 页面底色 |
| `--card` | `#ffffff` | 卡片底 |
| `--ink` / `--ink2` / `--ink3` | `#15202b` / `#465667` / `#657180` | 正文 / 次要 / 弱化 |
| `--line` / `--line2` | `#e1e7ee` / `#eef2f6` | 边框 / 分隔 |
| `--red` / `--pre` / `--green` / `--amber` | `#a83224` / `#b8541c` / `#1c7444` / `#956612` | 风险 / 预警 / 安全 / 注意 |
| `--gray` | `#646f7b` | 中性 |
| `--radius` / `--radius-sm` | `12px` / `8px` | 圆角 |
| `--shadow` / `--shadow-md` / `--shadow-lg` | 见代码 | 阴影 |
| `--font-sans` | `"Microsoft YaHei","PingFang SC","Segoe UI",Arial,sans-serif` | 全局字体 |

**禁止使用**（漂移色，CI 直接判错）：`#1f3d63`、`#123a5c`、`#1a1a2e`、`#16213e`，以及任何未在上表中的主色。

**渐变**：页头统一 `linear-gradient(128deg,#0f2338 0%,var(--navy) 52%,var(--navy2) 100%)`（与 hub Hero 一致）。

---

## 四、组件标准

组件样式全部来自 `CANONICAL_CSS`；新增组件必须先并入 canonical，再在页面使用。

| 组件 | 类名 | 适用 | 说明 |
|---|---|---|---|
| 页头 | `.report-head` / `.hero` | 报告 | 全宽渐变、白字、`.wrap` 或内联 padding 约束到 1160px |
| 导航 | `.report-nav` + `.nav-url` + `.nav-tabs` | 报告 | sticky、pill 标签、`scroll-margin-top:100px` |
| 章节 | `h2.sec` | 报告 | 下边框 2px navy；`h3`/`h4` 同族 |
| 容器 | `.wrap` | 报告 | `max-width:1160px` 居中 |
| 卡片 | `.card` / `.leadbox` | 报告 | 白底、边框、圆角、阴影 |
| KPI | `.kpis` + `.kpi`（trends）/ `.kcards` + `.kcard`（apartment） | 报告 | 左侧色条；`.red/.green/.amber/.blue` |
| 图表 | `.chart`（卡片，内嵌 SVG）/ `.chart-box` + `.chart-eh`（echarts 容器） | 报告 | **echarts 容器必须用 `.chart-eh`** |
| 表格 | `table.fixed` | 报告 | `table-layout:fixed`；`thead th` navy；隔行变色；`.tblwrap` 横向滚动 |
| 来源 | `.src-head`+`.src-pop` / `.refs` / `.src-inline` | 报告 | 弹层式 / 清单式 / 行内链接式 |
| 标签 | `.tag` / `.pill` / `.lamp` | 报告 | 语义色变体 |
| 标注 | `.note` / `.callout` / `.disc` | 报告 | 提示 / 结论 |
| 时间线 | `.timeline` + `.tl-*` | 报告 | 时间轴 |
| 筛选栏 | `.filterbar` + `.chip` + `.count` | hub | sticky、搜索、chips |
| 报告卡 | `.rcard` + `.tag` + `.period` + `.path` | hub | 枢纽卡片 |
| 回顶 | `.totop` | hub / 报告 | 滚动超过阈值出现 |
| 跳转 | `.skip-link` | **全部** | 键盘可跳到主内容 |

---

## 五、代码结构与命名

### 5.1 目录与职责

```
engine/tools/            # 生成器与校验器（Python，无第三方依赖或仅 markdown）
  report_style.py     # canonical 报告样式单一事实源
  build_hub.py        # 生成 index.html / reader.html
  md2html.py          # md -> canonical HTML
  restyle_reports.py  # 既有报告迁移到 canonical
  page_build_check.py # 规范校验（本规范门禁）
  build_index.py / classify_reports.py / archive_reports.py / ...
engine/templates/ # 报告类型模板与通用规范（md）
  monitoring-common-spec.md  # 报告渲染/排版/交付最低标准
reports/*.html        # 报告产物（纯 HTML 交付）
sources/*.md          # 报告 md 源稿存档（不参与 md2html 自动转换）
```

### 5.2 命名与 JS 模式

- CSS 类名使用 canonical 词汇（`report-head` / `report-nav` / `sec` / `wrap` / `card` / `kpi` ...）；**不得新增同义异名类**。
- 生成器函数名保持 `render_*` / `build_*` / `check_*`；校验器统一 `[E]`/`[W]` 前缀与退出码约定（见 §九）。
- 变量 / 常量用大写下划线（`CANONICAL_CSS`、`TOKENS`、`COLOR_MAP`）。
- 交互页：单个 IIFE，`const state = {...}` 集中状态；`apply*()` 单向渲染；搜索防抖 120ms；chips 用 `aria-pressed`；事件委托绑定；URL 同步用 `history.replaceState` 且**只接受白名单内的值**（如 `?report=` 仅接受列表内已知路径）；不内联敏感信息、不依赖外部数据文件。

---

## 六、性能标准

| 指标 | 预算 | 说明 |
|---|---|---|
| hub 页体积 | ≤ 100 KB | 当前 index 26.4KB / reader 34.2KB |
| 报告页体积 | ≤ 1.5 MB | 当前最大 212KB |
| 外部依赖 | CDN 白名单：`cdn.jsdelivr.net`（echarts） | 其余外部脚本需先在规范登记 |
| 数据依赖 | **零外部数据文件** | 全部 CSS/JS/数据内联或 CDN |
| 首屏渲染 | CSS 全内联、无阻塞渲染；图表容器定高避免布局抖动 | `.chart-eh{height:352px}` |
| CSS | 选择器扁平、避免过深嵌套与通配重置滥用 | 单一 `<style>` 块 |
| 生成确定性 | 生成物不得包含 mtime / 「最近生成」等时间戳 | 仅 `INDEX.md` 心跳例外 |

**性能劣化处置**：新增依赖 / 大图 / 大表格前必须评估体积；超过预算由 `page_build_check.py` 告警。

---

## 七、可访问性要求（A11y）

**强制项**（`[E]`，缺失即阻断）：

1. `<html lang="zh-CN">`、`<meta charset>`、`<meta name="viewport">`。
2. `.skip-link` 跳转主内容（`:focus` 时可见）。
3. 焦点可见：`:focus-visible`（或 `:focus`）有焦点环。
4. 尊重 `prefers-reduced-motion`（关闭平滑滚动 / 动画）。
5. `@media print` 打印样式（隐藏导航 / 回顶，去阴影）。
6. 表格语义：`<thead>` / `<tbody>` 成对配平；表头用 `<th>`。
7. 交互控件可访问名：导航 `aria-label`；chips `aria-pressed`；抽屉 `aria-expanded`。

**推荐项**（`[W]`）：

- `img` 提供 `alt`；装饰图 `alt=""`。
- 文本与背景对比度 ≥ 4.5:1（navy on white 满足）。
- 标题层级连续（h1 → h2 → h3），不跳级。
- 抽屉 / 弹层支持 Esc 关闭与焦点管理。

---

## 八、兼容性与用户体验

### 8.1 兼容性

- **浏览器**：Chrome / Edge / Firefox / Safari 最近两个大版本；不使用实验性 CSS/JS。
- **响应式断点**：报告 720px；hub 960px / 560px。窄屏表格横向滚动、导航换行、抽屉化。
- **打印**：保留表格边框与来源备注，隐藏导航 / 回顶，字号收敛。
- **嵌入**：报告在 `reader.html` 的 `iframe` 中同源自包含运行，不依赖父页面样式。

### 8.2 用户体验准则

- **导航一致**：页头 / 导航 / 章节三级一致；sticky 常驻；当前章节高亮（`.active`）。
- **状态可见**：筛选计数实时更新；空态给出下一步指引；加载 / 错误有兜底。
- **反馈即时**：hover / focus 有视觉反馈；回顶按钮滚动超过阈值出现。
- **信息密度**：KPI 卡优先、表格承载明细、图与表不重复同一口径。
- **可分享**：报告页提供 `?report=` / `#sN` 直达；URL 与状态同步。

---

## 九、校验与门禁

`python engine/tools/page_build_check.py`（退出码：0 通过 / 1 有 `[E]` / 2 仅 `[W]`）。

| 编号 | 级别 | 检查项 | 适用 |
|---|---|---|---|
| P01 | E | `lang` / `viewport` / `charset` | 全部 |
| P02 | E | canonical 主色令牌 `--navy:#16324f` | 全部 |
| P03 | E | 无漂移色（`#1f3d63`/`#123a5c`/`#1a1a2e`/`#16213e`） | 全部 |
| P04 | E | `.skip-link` | 全部 |
| P05 | E | `:focus-visible` / `:focus` | 全部 |
| P06 | E | `prefers-reduced-motion` | 全部 |
| P07 | E | `@media print` | 全部 |
| P08 | E | `<thead>/<tbody>` 配平 | 含表格页 |
| P09 | E | 报告骨架：`header.report-head`/`.hero` + `nav.report-nav` + `.wrap` | 报告 |
| P10 | E | `h2.sec` 与导航锚点对应 | 报告 |
| P11 | E | echarts 容器用 `.chart-eh`（不得用 `.chart`） | 含 echarts |
| P12 | E | 生成物无「最近生成」等时间戳 | 生成页 |
| P13 | W | `.nav-url`（周期报告） | 报告 |
| P14 | W | 体积预算（hub 100KB / 报告 1.5MB） | 全部 |
| P15 | W | `img[alt]` | 含图页 |

**门禁规则**：`[E]` 阻断合并与定时维护提交；`[W]` 记录不阻断（见治理文档 §三）。当前实测：15 页 0E / 0W。

---

## 十、版本迭代约束

- 版本号 `PAGE-BUILD-SPEC vX.Y`；**修订必须走变更流程**（见治理文档 §五）。
- **令牌 / 组件变更**：先改 `report_style.py`（+ `build_hub.py` 同值），再改本文档，再用 `restyle_reports.py` 迁移存量，最后跑全量校验。
- **破坏性变更**（类名 / 结构 / 令牌含义变化）：提升主版本号，提供迁移工具与一个迭代周期的并行期，并在 CI 同时放行新旧（仅并行期内）。
- **新主题 / 新页面**：必须复用 canonical 样式与结构；接入前跑 `page_build_check.py`，全绿方可合并。
- **漂移防护**：CI 每次 push/PR 校验；`scheduled-maintenance` 定期审计；私建主色 / 私有样式一律判错。

---

## 十一、快速自检清单（新页面 / 新主题）

- [ ] 复用 `CANONICAL_CSS` 或 `build_hub.py`，未私建样式分支
- [ ] 令牌只用 §三 表内取值，无漂移色
- [ ] 骨架符合 §二（页头 / 导航 / `.wrap` / `h2.sec`）
- [ ] A11y 强制项齐全（§七）
- [ ] 断点 / 打印 / 窄屏正常（§八）
- [ ] 体积在预算内（§六）
- [ ] `python engine/tools/page_build_check.py` 全绿
- [ ] `python -m unittest discover -s engine/tests` 通过
