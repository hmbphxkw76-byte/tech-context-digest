"""公共模块：仓库结构识别、报告命名解析、周期计算。

所有 engine/tools/*.py 共享；纯函数部分供 engine/tests/ 直接调用。
目录结构单一事实源为 engine/tools/layout.json（校验见 validate_layout.py）。

三层架构：content/（内容层：主题 → 业务线）、
engine/（引擎层：跨主题复用的模板 / 提示词 / 工具 / 质量 / 审计）、
data/（资产层：raw / processed / assets）。

业务线默认位于 content/<theme>/<维度段...>/，维度顺序由 layout.json 各主题自行声明：
economy 为 region→category（地区优先），tech 为 category→subcategory→region（AI 安全 /
AI 应用两大类 → 业务线 → 地区），education / international / political / society 为
category→region（细分优先）。region 为可选维度（theme 以 optional_dimensions
声明）：业务线可省略 region 段，直接以 category（+subcategory）段落位（如
content/economy/trends、content/tech/ai-application/dubai）；省略时剩余段按声明
顺序剔除 region 后逐位映射。theme 下允许存在不含业务配置的分组目录（如
content/tech/ai-security），其层级深度须小于该主题维度数。
无 region 维度的主题可按声明维度建。

硬性规则：维度先后按主题声明，不得在未改 layout.json 的情况下倒置；新增主题须在
layout.json 的 themes 中显式声明 dimensions。

分类体系版本号：layout.json 的 classification_version（YYYY-MM-DD.<n>）+ changelog
留痕分类变更；跨主题互斥性检查见 validate_layout.py（重合度 > 0.9 判疑似，先 [W]）。
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

# 仓库根目录：engine/tools/_common.py -> parents[2]
ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "engine"
CONTENT = ROOT / "content"
DATA = ROOT / "data"

# 目录结构单一事实源（与本文件同目录）
LAYOUT_PATH = Path(__file__).resolve().parent / "layout.json"

# 站点身份单一事实源：枢纽页（index.html / reader.html）与索引页（INDEX.md）统一引用，
# 避免品牌名在多处复述导致漂移（历史遗留：hub 曾硬编码旧名「宏观资讯报告」）。
SITE_BRAND = "Tech Life Research"

# 公共资源统一收拢于 engine/：通用模板层 / 通用提示词层 / 合规审计目录
TEMPLATE_DIR = ENGINE / "templates"
PROMPT_DIR = ENGINE / "prompts"
AUDIT_DIR = ENGINE / "report-audits"


@dataclass(frozen=True)
class Layout:
    """layout.json 的强类型视图。

    themes: 主题 ID -> (主题名, 维度序列)；维度序列长度 + 1 = 业务线层级深度。
    content_root: 内容层根目录（默认 content）；regional_segment: 地区分组字面段
    （默认空串，即无独立地区分组段，region 直接作为维度段）。
    """

    root_reserved: frozenset[str]
    themes: dict[str, tuple[str, tuple[str, ...]]]
    regions: frozenset[str]
    naming_pattern: str
    max_depth: int
    content_root: str = "content"
    regional_segment: str = ""
    theme_segments: dict[str, str] = field(default_factory=dict)
    optional_dimensions: dict[str, tuple[str, ...]] = field(default_factory=dict)
    # theme -> {category 段: 中文名}（分组目录展示名，如 tech 的 ai-security → AI安全）
    category_names: dict[str, dict[str, str]] = field(default_factory=dict)
    # 分类体系版本号（YYYY-MM-DD.<n>）与变更留痕；缺省空串 / 空元组表示未登记
    classification_version: str = ""
    classification_changelog: tuple[dict, ...] = ()

    def dimensions(self, theme: str) -> tuple[str, ...]:
        """主题的维度序列（如 ("region", "category")）。"""
        return self.themes.get(theme, ("", ()))[1]

    def optional_dims(self, theme: str) -> tuple[str, ...]:
        """主题声明为可选的维度名（如 ("region",)）；缺省为空元组。"""
        return self.optional_dimensions.get(theme, ())

    def segment(self, theme: str) -> str:
        """主题的地区分组段：默认 regional_segment；主题可声明 segment 覆盖（空串表示无该段）。

        默认即为空串（无独立地区分组段）。
        """
        return self.theme_segments.get(theme, self.regional_segment)

    def depth(self, theme: str) -> int:
        """主题下业务线目录的层级深度（含主题自身）。"""
        return 1 + len(self.dimensions(theme))


@lru_cache(maxsize=1)
def load_layout() -> Layout:
    """读取 layout.json（进程内缓存）；缺失或非法时抛 RuntimeError。"""
    try:
        data = json.loads(LAYOUT_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise RuntimeError(f"缺少目录结构事实源: {LAYOUT_PATH}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"layout.json 非法 JSON: {e}") from e
    themes = {
        name: (str(spec.get("name", name)), tuple(spec.get("dimensions", ())))
        for name, spec in data.get("themes", {}).items()
    }
    default_segment = str(data.get("regional_segment", ""))
    theme_segments = {
        name: str(spec.get("segment", default_segment))
        for name, spec in data.get("themes", {}).items()
    }
    optional_dimensions = {
        name: tuple(spec.get("optional_dimensions", ()))
        for name, spec in data.get("themes", {}).items()
    }
    category_names = {
        name: {str(k): str(v) for k, v in spec.get("category_names", {}).items()}
        for name, spec in data.get("themes", {}).items()
    }
    naming = data.get("naming", {})
    return Layout(
        root_reserved=frozenset(data.get("root_reserved", ())),
        themes=themes,
        regions=frozenset(data.get("regions", ())),
        naming_pattern=str(naming.get("pattern", r"^[a-z0-9]+(?:-[a-z0-9]+)*$")),
        max_depth=int(naming.get("max_depth", 6)),
        content_root=str(data.get("content_root", "content")),
        regional_segment=default_segment,
        theme_segments=theme_segments,
        optional_dimensions=optional_dimensions,
        category_names=category_names,
        classification_version=str(data.get("classification_version", "")),
        classification_changelog=tuple(data.get("changelog", ())),
    )


# 历史根条目（目录规范化 / 三层重构前的旧根，用于识别旧引用；现结构根条目由 layout.json 提供）
LEGACY_ROOTS = {"src", "prompts", "report_templates", "vocabulary", "docs", "tests",
                "report-audits", "dubai", "trends", "economy", "technology"}


def known_roots() -> set[str]:
    """现结构根条目 + 历史根条目（路径引用判定 / 批量改写共用）。"""
    layout = load_layout()
    return set(layout.root_reserved) | set(layout.themes) | LEGACY_ROOTS


def resolve_segments(layout: Layout, theme: str, segments: tuple[str, ...]) -> dict[str, str]:
    """将业务线维度段映射为 {维度名: 段}。

    规则：段数 = 维度数 -> 逐位映射；段数 = 维度数 - 1 且 theme 声明 region 可选
    -> 剔除 region 后逐位映射（region 缺省）。其他情况抛 ValueError。
    """
    dims = layout.dimensions(theme)
    optional = layout.optional_dims(theme)
    segs = tuple(segments)
    if len(segs) == len(dims):
        return dict(zip(dims, segs))
    if len(segs) == len(dims) - 1 and "region" in dims and "region" in optional:
        rest = tuple(d for d in dims if d != "region")
        return dict(zip(rest, segs))
    raise ValueError(
        f"业务线维度段数 {len(segs)} 与主题 {theme} 声明维度 {dims} 不匹配"
    )

# 报告文件命名约定（与 monitoring-common-spec.md 第 1 节一致；月份限 01–12）
MONTHLY_RE = re.compile(r"^(\d{4}-(?:0[1-9]|1[0-2]))_monthly\.(html|md)$")
QUARTERLY_RE = re.compile(r"^(\d{4}-Q[1-4])_quarterly\.(html|md)$")
ANNUAL_RE = re.compile(r"^(\d{4})_annual\.(html|md)$")
BASELINE_RE = re.compile(r"^(\d{4}-(?:0[1-9]|1[0-2]))_baseline(?:_report)?\.(html|md)$")
# 周报：period 为数据截止日（ISO 日期），与月/季/年的日历周期不同
WEEKLY_RE = re.compile(r"^(\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01]))_weekly\.(html|md)$")

REPORT_RES = (
    ("monthly", MONTHLY_RE),
    ("quarterly", QUARTERLY_RE),
    ("annual", ANNUAL_RE),
    ("baseline", BASELINE_RE),
    ("weekly", WEEKLY_RE),
)

# 各周期提示词文件名
PROMPT_FILES = {
    "baseline": "prompt-baseline-setup.md",
    "monthly": "prompt-monthly-monitor.md",
    "quarterly": "prompt-quarterly-analysis.md",
    "annual": "prompt-annual-review.md",
    "weekly": "prompt-weekly-monitor.md",
}

# 周期提示词文件名别名：部分类型模板使用与标准名不同的文件名
# （如行业深度研究型 / 市场规模测算型用 prompt-annual-refresh.md）。
PROMPT_FILE_ALIASES = {
    "annual": ("prompt-annual-refresh.md",),
}


def prompt_file_candidates(cycle: str) -> tuple:
    """某周期的候选提示词文件名（标准名在前，类型特有别名在后）。"""
    primary = PROMPT_FILES.get(cycle)
    aliases = PROMPT_FILE_ALIASES.get(cycle, ())
    return (primary, *aliases) if primary else aliases

# 提示词可声明「本周期不产出报告文件」（条件节拍 / 核验型轻运行）。
# 约定：提示词正文含 `<!-- report-output: none -->` 时，规划器不为该周期派发任务。
REPORT_OUTPUT_NONE_RE = re.compile(r"report-output\s*:\s*none\b")


def prompt_produces_report(prompt_path: Path) -> bool:
    """提示词是否产出报告文件。

    含 `<!-- report-output: none -->` 的提示词为条件节拍 / 核验型轻运行，
    不产出报告文件（如 content/tech/ai-security/security/dubai 的月度核验提示词）。
    读取失败时按「产出」处理（不改变既有行为）。
    """
    try:
        text = prompt_path.read_text(encoding="utf-8")
    except OSError:
        return True
    return REPORT_OUTPUT_NONE_RE.search(text) is None


BASELINE_DATE_RE = re.compile(r"\{\{BASELINE_DATE\}\}\s*=\s*(\d{4})-(\d{2})")


def baseline_year_month(business: "Business") -> tuple[int, int] | None:
    """从 business-config 解析 {{BASELINE_DATE}} 的 (年, 月)；解析失败返回 None。

    规划器据此跳过早于业务线基线的周期任务（新建立业务线不应被派历史任务）。
    """
    try:
        text = (business.path / "prompts" / "business-config.md").read_text(encoding="utf-8")
    except OSError:
        return None
    m = BASELINE_DATE_RE.search(text)
    return (int(m.group(1)), int(m.group(2))) if m else None

# 通用层根部必备文件（validate.py 使用；类型中立共享文件）
REQUIRED_TEMPLATE_FILES = (
    "prompt-generic-base.md",
    "monitoring-common-spec.md",
    "information-layering-spec.md",
    "decision-delivery-spec.md",
    "template-registry.md",
    "report-classification.md",
    "compliance-rules.json",
)

# 类型模板目录：类型 ID -> 该类型必备模板（相对 engine/templates/<类型ID>/）
# 与 engine/templates/template-registry.md 第二节登记一致；新增类型时同步两处。
TEMPLATE_TYPE_DIRS = {
    "market-monitoring": (
        "prompt-baseline-setup-template.md",
        "prompt-monthly-monitor-template.md",
        "prompt-quarterly-analysis-template.md",
        "prompt-annual-review-template.md",
    ),
    "employment-research": (
        "prompt-baseline-setup-template.md",
        "prompt-update-template.md",
        "operations-guide.md",
        "README.md",
    ),
    "competitive-intelligence": (
        "prompt-baseline-setup-template.md",
        "prompt-monthly-update-template.md",
    ),
    "sentiment-monitoring": (
        "prompt-baseline-setup-template.md",
        "prompt-monthly-update-template.md",
    ),
    "consumer-research": (
        "prompt-baseline-setup-template.md",
        "prompt-study-template.md",
    ),
    "industry-research": (
        "prompt-baseline-setup-template.md",
        "prompt-annual-refresh-template.md",
    ),
    "market-sizing": (
        "prompt-baseline-setup-template.md",
        "prompt-annual-refresh-template.md",
    ),
    "investment-research": (
        "prompt-baseline-setup-template.md",
        "prompt-target-update-template.md",
    ),
    "policy-analysis": (
        "prompt-baseline-setup-template.md",
        "prompt-policy-review-template.md",
    ),
    "feasibility-study": (
        "prompt-baseline-setup-template.md",
        "prompt-study-template.md",
    ),
    "flash-commentary": (
        "prompt-baseline-setup-template.md",
        "prompt-flash-note-template.md",
    ),
    "whitepaper": (
        "prompt-baseline-setup-template.md",
        "prompt-topic-study-template.md",
    ),
    "trend-weekly": (
        "prompt-baseline-setup-template.md",
        "prompt-weekly-monitor-template.md",
        "operations-guide.md",
        "README.md",
    ),
    "decision-dashboard": (
        "prompt-baseline-setup-template.md",
    ),
}

# 类型声明结构化（P1-4）：business-config 优先用 `{{REPORT_TYPE}} = <类型ID>` 声明；
# 缺声明时回落到继承声明中的 `engine/templates/<类型ID>/` 引用（非结构化）。
REPORT_TYPE_VAR_RE = re.compile(r"\{\{REPORT_TYPE\}\}\s*=\s*([a-z0-9]+(?:-[a-z0-9]+)*)")
REPORT_TYPE_REF_RE = re.compile(r"engine/templates/([a-z0-9]+(?:-[a-z0-9]+)*)/")

# 已注册类型的节拍（文件名周期）白名单：classify 双校验的第二信号。
TYPE_CADENCE: dict[str, tuple[str, ...]] = {
    "market-monitoring": ("monthly", "quarterly", "annual", "baseline"),
    "employment-research": ("monthly", "quarterly", "annual", "baseline"),
    "trend-weekly": ("weekly", "baseline"),
    "competitive-intelligence": ("monthly", "baseline"),
    "sentiment-monitoring": ("monthly", "baseline"),
    "consumer-research": ("baseline",),
    "industry-research": ("baseline", "annual"),
    "market-sizing": ("baseline", "annual"),
    "investment-research": ("baseline", "target_update", "quarterly", "annual"),
    "policy-analysis": ("baseline", "monthly", "review"),
    "feasibility-study": ("baseline", "study"),
    "flash-commentary": ("baseline", "flash_note"),
    "whitepaper": ("baseline", "topic_study"),
    "decision-dashboard": ("baseline", "quarterly"),
}


def parse_report_type(config_text: str) -> tuple[str | None, bool]:
    """解析业务配置的报告类型 -> (类型 ID, 是否结构化声明)。

    结构化声明（`{{REPORT_TYPE}}`）优先；否则回落继承声明引用（structured=False）。
    两者都缺失返回 (None, False)。
    """
    text = config_text or ""
    m = REPORT_TYPE_VAR_RE.search(text)
    if m:
        return m.group(1), True
    m = REPORT_TYPE_REF_RE.search(text)
    if m:
        return m.group(1), False
    return None, False


def type_cadence(type_id: str | None) -> tuple[str, ...] | None:
    """类型的文件名周期白名单；未注册类型返回 None（不做节拍校验）。"""
    if not type_id:
        return None
    return TYPE_CADENCE.get(type_id)


def business_report_type(b: "Business") -> tuple[str | None, bool, str]:
    """业务线报告类型 -> (类型 ID, 是否结构化, 说明)。读取失败时返回 (None, False, 说明)。"""
    cfg = b.path / "prompts" / "business-config.md"
    try:
        text = cfg.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, False, f"{b.rel}: 缺少 prompts/business-config.md"
    type_id, structured = parse_report_type(text)
    if not type_id:
        return None, False, f"{b.rel}: 未声明报告类型（{{REPORT_TYPE}} 或模板引用）"
    return type_id, structured, ""


# 通用层禁现的业务关键词（与 2026-11-13 重构验证口径一致）
BUSINESS_KEYWORDS = (
    "迪拜", "公寓", "Dubai", "UAE", "阿联酋", "DLD", "CBUAE", "EIBOR",
    "AED", "Bayut", "Knight Frank", "CBRE", "JLL", "Savills", "Ejari",
    "Peak Trust", "ValuStrat", "DXBinteract", "PropertyIndex",
)


@dataclass(frozen=True)
class Business:
    """一个业务线目录：content/<theme>/<维度段...>（维度顺序见 layout.json）。

    rel       仓库相对路径，如 "content/economy/dubai/apartment"
    theme     一级主题，如 "economy"
    segments  剔除 content/<theme>/<theme_segments> 后的维度段，如
                ("dubai", "apartment")
    """

    rel: str
    theme: str
    segments: tuple[str, ...]

    @property
    def path(self) -> Path:
        return ROOT / self.rel

    @property
    def dim_map(self) -> dict[str, str]:
        """维度名 -> 段（region 缺省时不含 region 键）。"""
        return resolve_segments(load_layout(), self.theme, self.segments)

    @property
    def category(self) -> str:
        """category 维度段；无 category 维度时取第一维度段。"""
        d = self.dim_map
        if "category" in d:
            return d["category"]
        return self.segments[0] if self.segments else ""

    @property
    def region(self) -> str:
        """地区段：region 维度缺省时返回空串。"""
        return self.dim_map.get("region", "")

    @property
    def property_type(self) -> str:
        """细分领域/方向段：剔除 region 后的末段（如 apartment / security）。

        维度序列中 region 可能位于 category 之前或之后（按主题声明），
        因此按声明顺序取非 region 维度的末段。
        """
        dims = load_layout().dimensions(self.theme)
        d = self.dim_map
        non_region = [d[dim] for dim in dims if dim != "region" and dim in d]
        return non_region[-1] if non_region else ""


def _walk_to_depth(base: Path, depth: int):
    """产出 base 下层级为 depth 的全部子目录（base 自身深度为 1）。"""
    if depth <= 1:
        yield base
        return
    if not base.is_dir():
        return
    for child in sorted(base.iterdir()):
        if child.is_dir() and not child.name.startswith("."):
            yield from _walk_to_depth(child, depth - 1)


def _walk_upto_depth(base: Path, max_depth: int):
    """产出 base 下层级 1..max_depth 的全部子目录（base 自身深度为 1）。"""
    if max_depth < 1 or not base.is_dir():
        return
    for child in sorted(base.iterdir()):
        if child.is_dir() and not child.name.startswith("."):
            yield child
            yield from _walk_upto_depth(child, max_depth - 1)


def iter_business_dirs() -> list[Business]:
    """按 layout.json 发现全部业务线（以 prompts/business-config.md 为锚点）。

    业务线默认位于 content/<theme>/<维度段...>/（维度先后按主题声明）；
    主题可声明 segment 覆盖（空串表示无地区分组段）。region 为可选维度时，
    业务线可省略 region 段（段数 = 维度数 - 1），故按 1..维度数 深度锚点发现。
    segments 为剔除 content/<theme>/<segment> 前缀后的维度段。
    """
    layout = load_layout()
    out: list[Business] = []
    content_root = ROOT / layout.content_root
    for theme in sorted(layout.themes):
        seg = layout.segment(theme)
        base = content_root / theme / seg if seg else content_root / theme
        if not base.is_dir():
            continue
        for d in _walk_upto_depth(base, len(layout.dimensions(theme))):
            if (d / "prompts" / "business-config.md").exists():
                rel = d.relative_to(ROOT).as_posix()
                out.append(Business(rel=rel, theme=theme,
                                    segments=tuple(d.relative_to(base).parts)))
    return out


@dataclass(frozen=True)
class ReportRef:
    """一份报告的发现结果（统一 hub / audit 口径）。

    category ∈ report（正式，发布 + 审计）/ archived（归档，轻量复核）/
    legacy（存档，不发布不审计）。
    """

    rel: str
    business_line: str
    cycle: str
    period: str
    category: str


def iter_business_reports(b: "Business", include_archives: bool = False,
                          include_legacy: bool = False) -> list[ReportRef]:
    """单业务线的报告发现（统一口径）。

    规则：reports/*.html 为正式；reports/archives/ 为归档（默认不计入正式）；
    reports/legacy/ 为存档（默认不发布不审计）。
    """
    reports = b.path / "reports"
    if not reports.is_dir():
        return []
    out: list[ReportRef] = []
    for f in sorted(reports.rglob("*.html")):
        rel = f.relative_to(ROOT).as_posix()
        sub = f.relative_to(reports).parts
        if "legacy" in sub:
            category = "legacy"
            if not include_legacy:
                continue
        elif "archives" in sub:
            category = "archived"
            if not include_archives:
                continue
        else:
            category = "report"
        det = detect_report(f.name)
        cycle, period = (det[0], det[1]) if det else ("", "")
        out.append(ReportRef(rel=rel, business_line=b.rel, cycle=cycle,
                             period=period, category=category))
    return out


def iter_reports(include_archives: bool = False,
                 include_legacy: bool = False) -> list[ReportRef]:
    """全部业务线的报告发现（统一口径）。"""
    out: list[ReportRef] = []
    for b in iter_business_dirs():
        out.extend(iter_business_reports(b, include_archives=include_archives,
                                         include_legacy=include_legacy))
    return out


def iter_theme_dirs() -> list[Path]:
    """返回全部已注册且已存在的主题目录（按主题 ID 排序）。"""
    layout = load_layout()
    content_root = ROOT / layout.content_root
    return [content_root / t for t in sorted(layout.themes) if (content_root / t).is_dir()]


def business_depth(theme: str) -> int:
    """返回主题的业务线层级深度（含主题自身）。"""
    return load_layout().depth(theme)


def processed_data_dir(business_rel: str) -> Path:
    """业务线清洗后数据目录：data/processed/<theme>/<维度段...>。

    维度段为剔除 content/<theme> 与主题地区分组段（默认空串）后的路径段；
    数据层统一收口于 data/processed/，不再散落在各业务线内。
    """
    layout = load_layout()
    parts = business_rel.split("/")
    if len(parts) >= 2 and parts[0] == layout.content_root:
        theme = parts[1]
        seg = layout.segment(theme)
        rest = parts[2:]
        if seg and rest and rest[0] == seg:
            rest = rest[1:]
        out = DATA / "processed" / theme
        for part in rest:
            out = out / part
        return out
    raise ValueError(f"无法识别的业务线路径: {business_rel}")


def detect_report(name: str):
    """按文件名识别报告 -> (cycle, period, ext)；不匹配返回 None。

    例：'2026-11_monthly.html' -> ('monthly', '2026-11', 'html')
    """
    for cycle, rx in REPORT_RES:
        m = rx.match(name)
        if m:
            return cycle, m.group(1), m.group(2)
    return None


def detect_report_loose(name: str):
    """宽松周期识别（classify 双校验用）：允许文件名带地区/主题前缀。

    例：'dubai_apartment_2026-11_monthly.html' -> ('monthly', '')；
    无法识别返回 None（项目制命名）。
    """
    m = re.search(r"_(monthly|quarterly|annual|baseline|weekly)\.(?:html|md)$", name or "")
    return (m.group(1), "") if m else None


def parse_period(s: str):
    """解析周期标识 -> (cycle, y, n)。cycle in {'month','quarter','year'}。

    '2026-11' -> ('month', 2026, 11)；'2026-Q3' -> ('quarter', 2026, 3)；
    '2026' -> ('year', 2026, None)。非法输入抛 ValueError。
    """
    m = re.fullmatch(r"(\d{4})-(\d{2})", s)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12:
            return "month", y, mo
    m = re.fullmatch(r"(\d{4})-Q([1-4])", s)
    if m:
        return "quarter", int(m.group(1)), int(m.group(2))
    m = re.fullmatch(r"(\d{4})", s)
    if m:
        return "year", int(m.group(1)), None
    raise ValueError(f"无法识别的周期: {s}")


# ── 报告周期窗口（单一事实源，REPORT-CYCLE-WINDOWS-SPEC v1.0）──
# retention：reports/ 内保留时长（月），超出由 archive_reports.py 滚动归档。
# direct  ：hub 直接展示时长（月）；monthly 超出 direct 的部分折叠进「更多」完整展示。
# max_reports：hub 最多展示的该周期报告份数（annual = 近 60 个月的 5 份）。
# 周报 / 基线不参与环比高亮：周报按周单独展示；基线为对比锚，常驻展示。
CYCLE_WINDOWS = {
    "monthly": {"retention": 18, "direct": 6},
    "quarterly": {"retention": 24},
    "annual": {"retention": 60, "max_reports": 5},
    "baseline": {},
    "weekly": {},
}

# 参与「本期更新」环比高亮的周期（周报 / 基线除外）
HIGHLIGHT_CYCLES = ("monthly", "quarterly", "annual")

# 周期展示顺序（hub 分组顺序：月 → 季 → 年 → 基线 → 周报）
CYCLE_ORDER = ("monthly", "quarterly", "annual", "baseline", "weekly")


def period_months(period: str) -> int:
    """周期标识 -> 绝对月序（月 / 季 / 年统一到月），用于窗口比较。

    '2026-11' -> 2026*12+10；'2026-Q3' -> 2026*12+6；'2026' -> 2026*12。
    """
    kind, y, n = parse_period(period)
    if kind == "month":
        return y * 12 + (n - 1)
    if kind == "quarter":
        return y * 12 + (n - 1) * 3
    return y * 12  # year：按 1 月锚定


def prev_period(period: str) -> str:
    """上一期标识（环比基期）：2026-11 -> 2026-10；2026-Q3 -> 2026-Q2；2026 -> 2025。"""
    kind, y, n = parse_period(period)
    if kind == "month":
        return f"{y}-{n - 1:02d}" if n > 1 else f"{y - 1}-12"
    if kind == "quarter":
        return f"{y}-Q{n - 1}" if n > 1 else f"{y - 1}-Q4"
    return f"{y - 1}"


def expected_output(cycle: str, y: int, n) -> str:
    """某周期报告的落盘文件名（业务目录相对路径）。"""
    if cycle == "monthly":
        return f"{y}-{n:02d}_monthly.html"
    if cycle == "quarterly":
        return f"{y}-Q{n}_quarterly.html"
    if cycle == "annual":
        return f"{y}_annual.html"
    return f"{y}-{n:02d}_baseline_report.html"


def tasks_for_period(cycle: str, y: int, n):
    """给定周期应执行的任务清单 -> [(report_cycle, y, n), ...]。

    月度期：月度任务；季首月追加该季度任务；1 月追加上一自然年年度任务。
    季度期：仅该季度。年度期：仅该年度。
    """
    if cycle == "month":
        tasks = [("monthly", y, n)]
        if n in (1, 4, 7, 10):
            tasks.append(("quarterly", y, (n - 1) // 3 + 1))
        if n == 1:
            tasks.append(("annual", y - 1, None))
        return tasks
    if cycle == "quarter":
        return [("quarterly", y, n)]
    return [("annual", y, None)]


def report_title(html_text: str) -> str:
    """从 HTML 文本提取 <title>；缺失时返回空串。"""
    m = re.search(r"<title>(.*?)</title>", html_text, re.DOTALL)
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip()
