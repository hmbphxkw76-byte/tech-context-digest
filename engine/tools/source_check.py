#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""来源登记前置校验（L0 入口拦截，改造任务 T1）。

依据 engine/report-audits/system-optimization-plan-2026-11-15.md 第 3.1 节。
在报告生成前对「来源登记 / 分级合规 / 双源确认 / 关键数字来源 / 语言规则 / 死链」
做可机器判定的拦截，区别于落盘后的 L1 校验。

规则：
  R1 登记覆盖   报告内全部外部 URL 必须能在来源登记中匹配
                 （业务配置声明 SOURCE_STRATEGY=synthesis_only 的综合层，
                 无外部 URL 时豁免「登记为空」告警；一旦出现外部 URL 仍须登记）
  R2 分级合规   tier=4 媒体转述出现处须邻近『需核实原文』；tier=3 须标『卖方预期/情绪/参考』
  R3 双源确认   进入信号合成（in_synthesis=true）的来源须有 ≥2 个被报告引用
  R4 关键数字   含单位/量级数字的正文断言块（li/p/td）附近 PROXIMITY_WINDOW 内须有来源标记
                 （事实卡片 / 来源编号 / 来源标签 / 外链 / K 指针 / 核验等级 / 机构引用；
                 已声明信息（自算/推断/假设/待核）与咨询容器内块不计）
  R5 语言规则   tier1/2 来源语言须符合业务配置的语言规则（token 化分级）
  R6 死链       明确 404/410/451 = 死链（阻断期内 [E] / 此前 [W] / 历史 [W]）；403/429/5xx/超时 = 网络不可达 [W]
  R7 机构分级   机构级分级主数据与来源登记 / 业务配置的一致性（分级校验）
  R8 登记字段   来源登记条目 verify_status 取值合法（verified / media_unverified / unverifiable）
                 且含 updated（YYYY-MM-DD）；缺失 / 非法仅 [W]（数据卫生，不阻断）

gate-period 前置：周期早于 `--gate-period` 的报告为历史报告，R1–R6 的 [E] 前置
降级为 [W]（不追溯阻断历史）；R7 结构性冲突（重复 source_id / 同机构不同分级）不降级。
R6 死链分级：明确 404/410/451 = 死链；403/429/5xx/超时 = 网络不可达（仅 [W]，需人工复核）。
死链阻断自 `R6_STRICT_PERIOD`（默认 2027-01）起：链接腐烂修复属内容维护（目标对齐方案
P1-8），集中清理完成前死链只告警不阻断；到期后自动转 [E]，滚动基线下不失效。
指向本仓库自身的 GitHub 链接为内部指针，不计入 R1 / R6（见 `is_self_reference`）。

退出码：0 通过；1 存在错误项（CI 阻断）；2 仅警告项 / 用法错误。

用法：
    python engine/tools/source_check.py                     # 全量（业务线正式报告）
    python engine/tools/source_check.py --file <报告路径>    # 单份
    python engine/tools/source_check.py --gate-period 2026-12  # 早于该周期降级为警告
    python engine/tools/source_check.py --probe             # 自动探测外部 URL 可达性（R6）
    python engine/tools/source_check.py --coverage          # 输出来源登记覆盖率
    python engine/tools/source_check.py --self-test         # 内置合成用例自检
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import ROOT, detect_report, iter_business_dirs, iter_business_reports, processed_data_dir  # noqa: E402
from gate_period import is_auto, resolve as resolve_period  # noqa: E402

REGISTRY_SCHEMA = "1.1"

# R8 登记字段：verify_status 合法取值（「无法核实」自 P1-6 起纳入，不再只能降级表达）
VERIFY_STATUS_VALUES = ("verified", "media_unverified", "unverifiable")
UPDATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# R6 死链阻断的生效周期：链接腐烂修复属内容维护（见目标对齐方案 P1-8），
# 集中清理完成前死链只告警不阻断；到期后自动转 [E]（滚动基线下不失效）。
R6_STRICT_PERIOD = "2027-01"

# 指向本仓库自身的 GitHub 链接（blob / raw）是**内部指针**，不是外部来源：
# 不计入 R1 登记覆盖，也不参与 R6 死链判定（私有仓库下外部探测必然 404）。
SELF_LINK_RE = re.compile(r"https?://(?:www\.)?github\.com/[\w.\-]+/tech-context-digest/")


def is_self_reference(url: str) -> bool:
    """URL 是否指向本仓库自身内容（内部指针）。"""
    return bool(SELF_LINK_RE.match(normalize_url(url)))
INSTITUTION_MASTER_PATH = Path(__file__).resolve().parent / "institution_tiers.json"

HREF_RE = re.compile(r'href="(https?://[^"]+)"', re.I)
# 带单位/量级的关键数字（金额、百分比、面积、利率 bp、成交笔数等）
NUMBER_UNIT_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:AED|USD|EUR|GBP|\$|€|£|%|亿|万|千|百万|十亿|bp|bps|pp|sqft|m²"
    r"|套|宗|人|笔|项|次|条|份|美元|日元|英镑|欧元|MW|GW|平方米|平米|公顷|平方公里)"
)
MEDIA_MARKER = "需核实原文"
PORTAL_MARKERS = ("卖方预期", "情绪", "参考")

# ---------------------------------------------------------------- R4 关键数字（块级）

# 正文断言块：列表项 / 段落。
# 不取 <td>：表格数值的来源常写在表注 / 表级来源行 / 报告来源清单，逐单元格判定
# 在语料上产生大量误报（P1-7 实测 164 处，其中绝大多数为表格单元格）；
# 表格数值的溯源由 R2（分级邻近）与来源登记覆盖，本规则与 IGI-05 同口径。
R4_BLOCK_RE = re.compile(r"<li\b[^>]*>.*?</li>|<p\b[^>]*>.*?</p>",
                         re.DOTALL | re.IGNORECASE)
R4_TAG_RE = re.compile(r"<[^>]+>")
# 窗口内任一命中即视为「有来源标记」：事实卡片 / 来源编号 / 来源标签 /
# 外链 / K 指针 / 核验等级标 / 机构引用（含年份的括号注）
R4_SRC_MARKER_RE = re.compile(
    r"\[FC-[A-Z]+-\d+\]|\[S-\d{3}\]|\[Source:|data-source-id=\"|fact-ref"
    r"|lvl-verified|lvl-partial|已核验|部分核验"
    r"|(?:来源|出处|来源机构|source_id)\s*[:：]"
    r"|<a\b[^>]*href\s*=\s*\"https?://|\bK\d{2}\b"
    r"|[（(][^（）()]{0,40}?(?:19|20)\d{2}[^（）()]{0,40}?[)）]"
    r"|\b[A-Z][A-Za-z&.\-]{2,20}\s*,\s*(?:19|20)\d{2}\b",
    re.IGNORECASE)
# 已声明的非核验信息（自算派生值 / 推断 / 假设 / 待确认）——不属于「悄悄无来源的关键数字」
R4_DECL_RE = re.compile(r"自算|推断|假设性测算|假设乘积|待核|待确认|待补|待官方")
# 说明性段落（方法 / 说明 / 注 / 定义 / 口径 / 入选标准 / 来源与时点）：自身即声明，不要求逐点指针
R4_NOTE_PREFIX_RE = re.compile(r"^(?:方法|说明|注|注释|定义|口径|入选标准|来源与时点)[：:]")
# 咨询 / 声明容器（场景切片、行动卡、口径提示、图表脚注、决策卡、时间线等），
# 其内数值为建议 / 阈值 / 声明 / 图表读数，不是待溯源的事实断言
R4_ADVISORY_CLASS = ("slice", "a-meta", "a-head", "note", "delta-strip", "callout",
                     "tl-body", "tl-item", "scenario", "chart-note", "chart-box",
                     "chart-eh", "dc-grid", "dc-head", "dc-body")
# 说明性 / 声明性 / 机制推断章节：其数字为复用、说明或判定，不要求逐点指针
R4_ADV_HEAD_RE = re.compile(
    r"建议|路径|场景|行动|切入|修正|反向|排除|伪信号|方法|说明|口径|局限|治理"
    r"|附录|备注|声明|未核验|传导|断裂点|加速点|缓冲点|复盘|判读")
R4_SKIP_REGION_RE = re.compile(
    r"<header\b.*?</header>|<footer\b.*?</footer>|<nav\b.*?</nav>",
    re.DOTALL | re.IGNORECASE)
R4_DIV_TOKEN_RE = re.compile(r"<div\b[^>]*>|</div>", re.IGNORECASE)
R4_HEAD_RE = re.compile(r"<h[2-4]\b[^>]*>(.*?)</h[2-4]>", re.DOTALL | re.IGNORECASE)
R4_HEAD_SPAN = 4000
# 非 div 的咨询 / 声明元素（如 <p class="note">、<li class="note">）
R4_ADVISORY_EL_RE = re.compile(
    r"<(p|li)\b[^>]*class=\"[^\"]*(?:note|chart-note|callout|delta-strip|scenario"
    r"|slice|a-meta|a-head|tl-body|tl-item)[^\"]*\"[^>]*>.*?</\1>",
    re.DOTALL | re.IGNORECASE)

# R2 邻近判定：标注须出现在来源链接之后的本段落窗口内（字符数）
PROXIMITY_WINDOW = 240

# 任何周期都不得降级为警告的规则（真阻断）。当前为空：R1–R6 均按 gate-period 降级，
# 历史报告不追溯阻断，新报告（周期 >= gate-period）一律 [E]，避免历史死链卡死当前 PR。
BLOCKING_RULES: set[str] = set()

# ---------------------------------------------------------------- 基础工具

def normalize_url(url: str) -> str:
    """URL 归一化：小写 host、去片段、去末尾斜杠，便于登记比对。"""
    try:
        p = urlparse(url.strip())
    except ValueError:
        return url.strip().rstrip("/").lower()
    host = (p.netloc or "").lower()
    path = (p.path or "").rstrip("/")
    return f"{p.scheme.lower()}://{host}{path}".lower()


def extract_urls(text: str) -> list[str]:
    """提取报告中的外部 URL（去重、保序）。"""
    seen: dict[str, None] = {}
    for m in HREF_RE.finditer(text):
        seen.setdefault(m.group(1), None)
    return list(seen)


def load_registry(path: Path) -> dict:
    """读取来源登记；缺失或非法时返回空登记（不抛异常，便于历史报告降级）。"""
    if not path or not Path(path).exists():
        return {"schema_version": REGISTRY_SCHEMA, "sources": []}
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"schema_version": REGISTRY_SCHEMA, "sources": []}
    if not isinstance(data.get("sources", []), list):
        data["sources"] = []
    return data


def _registry_index(registry: dict) -> dict[str, dict]:
    """归一化 URL -> 来源条目。"""
    out: dict[str, dict] = {}
    for s in registry.get("sources", []):
        u = s.get("url")
        if u:
            out[normalize_url(u)] = s
    return out


def _period_key(period: str) -> tuple:
    """周期字符串 -> 可比较元组（与 research_kernel_check 同口径）。"""
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", period or "")
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"(\d{4})-(\d{2})", period or "")
    if m:
        return (int(m.group(1)), int(m.group(2)), 0)
    m = re.fullmatch(r"(\d{4})-Q([1-4])", period or "")
    if m:
        return (int(m.group(1)), int(m.group(2)) * 3, 0)
    m = re.fullmatch(r"(\d{4})", period or "")
    if m:
        return (int(m.group(1)), 12, 31)
    return (0, 0, 0)


def valid_period(period: str) -> bool:
    """gate-period 是否可解析（auto / YYYY-MM / YYYY-Qn / YYYY / YYYY-MM-DD）。"""
    if is_auto(period):
        return True
    return _period_key(period) != (0, 0, 0)


# ---------------------------------------------------------------- 邻近判定

def href_positions(text: str, url: str) -> list[int]:
    """返回某 URL 在文本中的全部 href 出现位置。"""
    return [m.start() for m in HREF_RE.finditer(text) if normalize_url(m.group(1)) == normalize_url(url)]


def proximity_ok(text: str, url: str, markers, window: int = PROXIMITY_WINDOW) -> bool:
    """来源出现处是否『邻近』标注。

    判定：任一次 href 出现后的 window 字符内出现任一 marker 即视为邻近；
    若链接在文末（其后不足 window），窗口取到文本末尾。
    """
    marker_list = [markers] if isinstance(markers, str) else list(markers)
    positions = href_positions(text, url)
    if not positions:
        return True  # 该来源未在报告出现，R2 不判定
    for pos in positions:
        tail = text[pos: pos + window]
        if any(m in tail for m in marker_list):
            return True
    return False


# ---------------------------------------------------------------- 来源策略（综合层豁免）

# 业务线的来源策略：synthesis_only = 无外部来源的综合层（只收敛仓库内已文档化事实，
# 引用走事实卡片 / 来源登记指针，不新采外部数据）。声明于 business-config 的
# {{SOURCE_STRATEGY}}，供 R1 区分「按设计无外部来源」与「登记缺失」。
SYNTHESIS_STRATEGY = "synthesis_only"

SOURCE_STRATEGY_TOKENS = {
    "synthesis_only": SYNTHESIS_STRATEGY,
    "no_external": SYNTHESIS_STRATEGY,
    "no_external_sources": SYNTHESIS_STRATEGY,
    "无外部来源": SYNTHESIS_STRATEGY,
    "综合层": SYNTHESIS_STRATEGY,
}


def parse_source_strategy(rule: str) -> str:
    """解析 business-config 的 `{{SOURCE_STRATEGY}}` -> 策略键（未知 / 空返回 ""）。

    支持精确 token（synthesis_only / no_external）与自然语言表述
    （『无外部来源…』/『综合层…』）。无法识别时返回 ""（不改变既有行为）。
    """
    s = str(rule or "").strip()
    if not s:
        return ""
    key = SOURCE_STRATEGY_TOKENS.get(s.lower()) or SOURCE_STRATEGY_TOKENS.get(s)
    if key:
        return key
    low = s.lower()
    if "无外部来源" in s or "综合层" in s or "synthesis_only" in low or "no_external" in low:
        return SYNTHESIS_STRATEGY
    return ""


# ---------------------------------------------------------------- R5 语言规则 token 化

LANGUAGE_RULES = {
    "official_en": {
        "allowed": {"en"},
        "severity": "E",
        "label": "仅英文（官方一手 / 行业机构来源须英文）",
    },
    "official_en_media_zh": {
        "allowed": {"en", "zh"},
        "severity": "E",
        "label": "官方英文 + 媒体中文（中文转述须标『需核实原文』）",
    },
    "en_or_zh": {
        "allowed": {"en", "zh"},
        "severity": "W",
        "label": "英文或中文（不限定来源语言）",
    },
}

# token -> 规则键（精确 token 优先）
LANGUAGE_RULE_TOKENS = {
    "official_en": "official_en",
    "en": "official_en",
    "en_only": "official_en",
    "仅英文": "official_en",
    "official_en+media_zh": "official_en_media_zh",
    "en_or_zh": "en_or_zh",
    "allow_en_zh": "en_or_zh",
    "中英": "en_or_zh",
    "英文或中文": "en_or_zh",
}

_LANG_ALIAS = {
    "en": "en", "en/us": "en", "en/uk": "en", "en-us": "en", "en-gb": "en",
    "english": "en", "英文": "en",
    "zh": "zh", "zh-cn": "zh", "zh-tw": "zh", "zh-hans": "zh", "中文": "zh",
    "ja": "ja", "jp": "ja", "日语": "ja", "日本語": "ja",
}


def normalize_lang(lang) -> str:
    """语言标记归一（en/us -> en，zh-CN -> zh）。"""
    s = str(lang or "").strip().lower()
    if not s:
        return ""
    return _LANG_ALIAS.get(s, s)


def parse_language_rule(rule: str):
    """把业务配置的 `{{SOURCE_LANGUAGE_RULE}}` 解析为规则键 -> 规则字典；无法解析返回 None。

    支持精确 token（official_en / en_or_zh / official_en+media_zh）与自然语言
    （『仅英文…』 / 『英文或中文』）。解析结果携带 severity，供 R5 分级。
    """
    s = str(rule or "").strip()
    if not s:
        return None
    key = LANGUAGE_RULE_TOKENS.get(s.lower()) or LANGUAGE_RULE_TOKENS.get(s)
    if key:
        spec = dict(LANGUAGE_RULES[key])
        spec["tokens"] = [key]
        return spec
    low = s.lower()
    # 「仅英文…」优先（可能含『严禁中文来源』的否定式表述）
    if "仅英文" in s or "英文" in s and "中文" not in s or low in ("en", "english"):
        spec = dict(LANGUAGE_RULES["official_en"])
        spec["tokens"] = ["official_en"]
        return spec
    if "中文" in s and ("英文" in low or "en" in low):
        spec = dict(LANGUAGE_RULES["en_or_zh"])
        spec["tokens"] = ["en_or_zh"]
        return spec
    return None


def check_language(sources, rule: str) -> list[tuple[str, str]]:
    """R5：按解析后的语言规则校验来源语言 -> [(level, msg)]。"""
    spec = parse_language_rule(rule)
    if not spec:
        return [("W", f"R5 语言规则：无法解析规则「{rule}」，跳过语言校验")]
    out: list[tuple[str, str]] = []
    for s in sources:
        lang = normalize_lang(s.get("lang"))
        if not lang:
            continue
        if lang not in spec["allowed"]:
            out.append((spec["severity"],
                        f"R5 语言规则：{s.get('source_id')} lang={lang} 与规则"
                        f"「{rule}」不符（允许：{'/'.join(sorted(spec['allowed']))}）"))
    return out


# ---------------------------------------------------------------- 机构分级主数据

def load_institution_master(path: Path | None = None) -> dict:
    """读取机构级分级主数据；缺失或非法时返回空主数据（不抛异常）。"""
    p = Path(path) if path else INSTITUTION_MASTER_PATH
    if not p or not p.exists():
        return {"schema_version": "1.0", "institutions": []}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"schema_version": "1.0", "institutions": []}
    if not isinstance(data.get("institutions", []), list):
        data["institutions"] = []
    return data


def _norm_name(name: str) -> str:
    """机构名归一：小写、去空白与常见标点，供主数据比对。"""
    s = str(name or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s.strip(" .,，。()")


def master_lookup(master: dict, publisher: str):
    """按名称 / 别名查主数据 -> institution 条目或 None。"""
    key = _norm_name(publisher)
    if not key:
        return None
    for inst in master.get("institutions", []):
        names = [inst.get("name", ""), *inst.get("aliases", [])]
        if any(_norm_name(n) == key for n in names):
            return inst
    return None


def parse_config_tier_map(config_text: str) -> dict[str, int]:
    """从 business-config「来源优先级」段落解析 机构 -> tier。

    识别 ①②③④ / 1) 2) 等序号引导的行，按行内出现的机构名（主数据 name/alias）
    归属该 tier。解析失败返回空字典（不改变既有行为）。
    """
    out: dict[str, int] = {}
    if not config_text:
        return out
    markers = {"①": 1, "②": 2, "③": 3, "④": 4, "➄": 4}
    for line in config_text.splitlines():
        tier = None
        for mk, t in markers.items():
            if mk in line:
                tier = t
                break
        if tier is None:
            m = re.match(r"\s*([1-4])[)）.、]\s*", line)
            if m:
                tier = int(m.group(1))
        if tier is None:
            continue
        # 机构名按行内出现的关键主体粗提取（去序号与符号后按 、/ 分段）
        body = re.sub(r"[①②③④➄]|\d[)）.、]", "", line)
        for seg in re.split(r"[、,，/（）()]+", body):
            seg = seg.strip()
            if seg:
                out[seg] = tier
    return out


def check_institution_consistency(registry: dict, master: dict, config_text: str = "",
                                 ctx: dict | None = None) -> list[tuple[str, str]]:
    """R7 机构级分级主数据一致性 -> [(level, msg)]。

    分级逻辑：
      M1 登记机构在主数据中分级不同          -> 新报告 [E] / 历史 [W]
      M2 登记机构未录入主数据                -> [W]（提示补录，不阻断）
      M3 同一登记内 source_id 重复           -> [E]（结构性，不降级）
      M4 同一机构在同一登记内分级不一致      -> [E]（结构性，不降级）
      M5 business-config 来源优先级与主数据不一致 -> 新报告 [E] / 历史 [W]
    """
    ctx = ctx or {}
    historical = bool(ctx.get("historical"))
    issues: list[tuple[str, str]] = []
    sources = registry.get("sources", []) if isinstance(registry, dict) else []

    # M3 重复 source_id
    seen_ids: dict[str, int] = {}
    for s in sources:
        sid = str(s.get("source_id", "")).strip()
        if not sid:
            continue
        seen_ids[sid] = seen_ids.get(sid, 0) + 1
    for sid, n in seen_ids.items():
        if n > 1:
            issues.append(("E", f"R7 机构分级：source_id「{sid}」重复 {n} 次（须唯一）"))

    # M1 / M2 / M4
    by_norm: dict[str, set[int]] = {}
    for s in sources:
        pub = str(s.get("publisher", "")).strip()
        if not pub:
            continue
        inst = master_lookup(master, pub)
        if inst is None:
            issues.append(("W", f"R7 机构分级：机构「{pub}」未录入机构级分级主数据（请补录）"))
            continue
        tier = s.get("tier")
        if tier is not None and int(tier) != int(inst.get("tier")):
            lvl = "W" if historical else "E"
            issues.append((lvl, f"R7 机构分级：机构「{pub}」登记 tier={tier} 与主数据 "
                                f"tier={inst.get('tier')}（{inst.get('name')}）不一致"))
        by_norm.setdefault(_norm_name(inst.get("name", pub)), set()).add(int(tier))
    for name, tiers in by_norm.items():
        if len(tiers) > 1:
            issues.append(("E", f"R7 机构分级：机构「{name}」在同一登记内出现分级不一致 "
                                f"{sorted(tiers)}（须统一）"))

    # M5 配置 ↔ 主数据
    cfg_map = parse_config_tier_map(config_text)
    for seg, cfg_tier in cfg_map.items():
        inst = master_lookup(master, seg)
        if inst and int(inst.get("tier")) != int(cfg_tier):
            lvl = "W" if historical else "E"
            issues.append((lvl, f"R7 机构分级：business-config 来源优先级「{seg}」tier={cfg_tier} "
                                f"与主数据 tier={inst.get('tier')} 不一致"))
    return issues


def check_registry_fields(registry: dict, ctx: dict | None = None) -> list[tuple[str, str]]:
    """R8 登记字段完备 -> [(level, msg)]（仅 [W]，数据卫生不阻断）。

    verify_status ∈ verified / media_unverified / unverifiable；updated 为 YYYY-MM-DD。
    缺失 / 非法只告警，不追溯阻断（与 R1–R6 的 gate-period 降级口径一致）。
    """
    issues: list[tuple[str, str]] = []
    sources = registry.get("sources", []) if isinstance(registry, dict) else []
    for s in sources:
        sid = str(s.get("source_id", "")).strip() or "<无 source_id>"
        vs = s.get("verify_status")
        if vs not in VERIFY_STATUS_VALUES:
            issues.append(("W", f"R8 登记字段：{sid} 的 verify_status「{vs}」非法"
                                 f"（须为 {' / '.join(VERIFY_STATUS_VALUES)}）"))
        if not UPDATED_RE.match(str(s.get("updated", "")).strip()):
            issues.append(("W", f"R8 登记字段：{sid} 缺 updated（YYYY-MM-DD）"))
    return issues


# ---------------------------------------------------------------- 覆盖率度量

def coverage_report(registry: dict, text: str) -> dict:
    """来源登记覆盖率：报告引用 URL 与登记条目的匹配情况。"""
    idx = _registry_index(registry)
    urls = extract_urls(text)
    matched = [u for u in urls if normalize_url(u) in idx]
    return {
        "cited": len(urls),
        "registered": len(idx),
        "matched": len(matched),
        "unmatched": len(urls) - len(matched),
        "coverage": (len(matched) / len(urls)) if urls else 1.0,
    }


# ---------------------------------------------------------------- URL 探测（R6）

UA = {"User-Agent": "tech-context-digest-source-check/1.0"}
# 明确死链状态码（内容确已不存在）；403/429/5xx 属反爬 / 瞬时故障，归可疑
DEAD_STATUS = {404, 410, 451}


def _classify_status(status: int) -> str:
    return "dead" if status in DEAD_STATUS else "unreachable"


def _probe_one(url: str, timeout: float, opener=None) -> tuple[str, str]:
    """探测单个 URL -> (归一化 URL, 'ok' | 'dead' | 'unreachable')。

    dead = 404/410/451（真死链）；unreachable = 网络异常 / 超时 / 反爬（403/429）
    与 5xx 瞬时故障（环境相关，不应直接等同于死链）。HEAD 被拒时回退 GET 复核。
    """
    norm = normalize_url(url)
    last = "unreachable"
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers=UA)
        try:
            with (opener or urllib.request).urlopen(req, timeout=timeout) as resp:
                return (norm, "ok") if resp.status < 400 else (norm, _classify_status(resp.status))
        except urllib.error.HTTPError as e:
            code = getattr(e, "code", 0)
            if code in DEAD_STATUS:
                return norm, "dead"
            last = "unreachable"   # 反爬 / 瞬时故障，回退 GET 复核
        except Exception:
            return norm, "unreachable"   # 网络异常 / 超时，不再回退
    return norm, last


def probe_urls_detail(urls, timeout: float = 3.0, opener=None, workers: int = 8) -> tuple[set[str], set[str]]:
    """并发探测 -> (明确死链, 网络不可达)。opener 注入时退化为串行（测试用）。"""
    dead: set[str] = set()
    unreachable: set[str] = set()

    def _one(url: str) -> None:
        norm, status = _probe_one(url, timeout, opener)
        if status == "dead":
            dead.add(norm)
        elif status == "unreachable":
            unreachable.add(norm)

    if opener is not None:
        for url in urls:
            _one(url)
    else:
        import concurrent.futures as _cf
        with _cf.ThreadPoolExecutor(max_workers=max(1, int(workers))) as ex:
            list(ex.map(_one, urls))
    return dead, unreachable


def probe_urls(urls, timeout: float = 3.0, opener=None, workers: int = 8) -> set[str]:
    """探测外部 URL 可达性 -> 不可达 URL 集合（归一化，明确死链 + 网络不可达）。

    兼容旧调用；需要区分死链与环境性不可达时用 probe_urls_detail。
    """
    dead, unreachable = probe_urls_detail(urls, timeout=timeout, opener=opener, workers=workers)
    return dead | unreachable


# ---------------------------------------------------------------- 核心校验

def r4_advisory_spans(text: str) -> list[tuple[int, int]]:
    """平衡配对 <div>，返回类名命中「咨询 / 声明容器」的区间。

    场景切片、行动卡、口径提示、时间线等容器内的数值是建议 / 阈值 / 声明，
    不是待溯源的事实断言；用栈平衡而非正则贪婪，避免嵌套 div 截断。
    """
    spans: list[tuple[int, int]] = []
    stack: list[tuple[str, int]] = []
    for m in R4_DIV_TOKEN_RE.finditer(text):
        tok = m.group(0)
        if tok.startswith("</"):
            if stack:
                cls, start = stack.pop()
                if any(k in cls for k in R4_ADVISORY_CLASS):
                    spans.append((start, m.end()))
        else:
            cm = re.search(r'class="([^"]*)"', tok, re.IGNORECASE)
            stack.append((cm.group(1) if cm else "", m.start()))
    return spans


def r4_advisory_heading(text: str, pos: int) -> bool:
    """块是否位于「建议 / 路径 / 场景 / 行动」标题下（4000 字符内最近的 h2–h4）。"""
    last = None
    for m in R4_HEAD_RE.finditer(text, 0, pos):
        last = m
    if last is None or pos - last.end() > R4_HEAD_SPAN:
        return False
    return bool(R4_ADV_HEAD_RE.search(R4_TAG_RE.sub("", last.group(1))))


def r4_assertion_gaps(text: str) -> list[str]:
    """-> 附近窗口内无来源标记的「含单位/量级数字」正文断言块（纯文本摘要）。

    设计口径（P1-7 重新设计，替代原「全文有来源词即豁免」）：
    - 仅测正文断言块（li / p，与 IGI-05 同口径）；表格数值溯源由 R2 与来源登记承担；
    - 仅测「带单位/量级」的关键数字（NUMBER_UNIT_RE），年份 / 版本号 / 编号不算；
    - 已声明信息（自算 / 推断 / 假设 / 待核）与咨询容器 / 咨询章节内块不计；
    - 窗口内任一来源标记（事实卡片 / 来源编号 / 来源标签 / 外链 / K 指针 /
      核验等级标 / 含年份机构引用）即视为已标。
    """
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<script\b.*?</script>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    spans = [(m.start(), m.end()) for m in R4_SKIP_REGION_RE.finditer(text)]
    spans += [(m.start(), m.end()) for m in R4_ADVISORY_EL_RE.finditer(text)]
    spans += r4_advisory_spans(text)
    gaps: list[str] = []
    for m in R4_BLOCK_RE.finditer(text):
        if any(a <= m.start() < b for a, b in spans):
            continue
        plain = R4_TAG_RE.sub("", m.group(0))
        if not NUMBER_UNIT_RE.search(plain):
            continue
        if R4_DECL_RE.search(plain) or R4_NOTE_PREFIX_RE.match(plain.strip()):
            continue
        if r4_advisory_heading(text, m.start()):
            continue
        window = text[max(0, m.start() - PROXIMITY_WINDOW): m.end() + PROXIMITY_WINDOW]
        if R4_SRC_MARKER_RE.search(window):
            continue
        gaps.append(re.sub(r"\s+", " ", plain).strip())
    return gaps


def check_report(text: str, registry: dict, ctx: dict | None = None) -> list[tuple[str, str]]:
    """对单份报告执行 R1–R6 -> [(level, message)]，level ∈ {'E','W','I'}。

    纯函数，供 engine/tests/ 直接调用。ctx 可含：
      language_rule（如 'official_en'）、dead_urls（不可达 URL 集合）、
      source_strategy（如 'synthesis_only'：无外部来源的综合层，
        R1 空登记 + 无外部 URL 时豁免告警）、
      historical（历史报告：R1–R5 的 E 前置降级为 W；R6 不降级）。
    """
    ctx = ctx or {}
    issues: list[tuple[str, str]] = []
    sources = registry.get("sources", []) if isinstance(registry, dict) else []
    idx = _registry_index(registry)
    urls = extract_urls(text)
    norm_urls = {normalize_url(u) for u in urls}
    historical = bool(ctx.get("historical"))

    def level(rule: str, base: str) -> str:
        """gate-period 前置降级：历史报告的非阻断规则 E -> W。"""
        if historical and base == "E" and rule not in BLOCKING_RULES:
            return "W"
        return base

    # R1 登记覆盖
    strategy = ctx.get("source_strategy", "")
    if not sources:
        if urls:
            issues.append((level("R1", "E"), "R1 登记覆盖：来源登记为空，但报告含外部 URL（须先登记来源）"))
        elif strategy != SYNTHESIS_STRATEGY:
            # 综合层（synthesis_only）按设计不新采外部来源，空登记 + 无外部 URL 属预期，不告警
            issues.append(("W", "R1 登记覆盖：来源登记为空，无法校验外部 URL"))
    elif urls:
        unmatched = [u for u in urls
                      if normalize_url(u) not in idx and not is_self_reference(u)]
        if unmatched:
            issues.append((level("R1", "E"), f"R1 登记覆盖：{len(unmatched)} 个外部 URL 未在来源登记中"
                                            f"（示例：{unmatched[0]}）"))

    # R2 分级合规（邻近判定）
    for s in sources:
        u = s.get("url")
        if not u or normalize_url(u) not in norm_urls:
            continue
        sid = s.get("source_id", "?")
        if s.get("tier") == 4 and not proximity_ok(text, u, MEDIA_MARKER):
            issues.append((level("R2", "E"), f"R2 分级合规：媒体转述来源 {sid} 出现处未邻近"
                                            f"『{MEDIA_MARKER}』标注"))
        if s.get("tier") == 3 and not proximity_ok(text, u, PORTAL_MARKERS):
            issues.append(("W", f"R2 分级合规：挂牌门户来源 {sid} 未标『卖方预期/情绪/参考』"))

    # R3 双源确认
    synthesis = [s for s in sources if s.get("in_synthesis")]
    if synthesis:
        referenced = {
            s.get("source_id") for s in synthesis
            if s.get("url") and normalize_url(s["url"]) in norm_urls
        }
        if len(referenced) < 2:
            issues.append((level("R3", "E"), f"R3 双源确认：进入信号合成的来源仅 {len(referenced)} 个被引用（需 ≥2）"))

    # R4 关键数字来源（块级逐点指针）
    gaps = r4_assertion_gaps(text)
    if gaps:
        issues.append((level("R4", "E"),
                       f"R4 关键数字来源：{len(gaps)} 个含单位/量级数字的断言块附近 "
                       f"{PROXIMITY_WINDOW} 字符内无来源标记（示例：{gaps[0][:60]}）"))

    # R5 语言规则（token 化分级）
    rule = ctx.get("language_rule", "")
    if rule:
        for lvl, msg in check_language(sources, rule):
            issues.append((level("R5", lvl), msg))

    # R6 死链：明确 4xx/5xx = 真阻断；网络异常/超时/反爬 = 可疑告警（环境相关）
    dead = ctx.get("dead_urls") or set()
    unreachable = ctx.get("unreachable_urls") or set()
    dead_norm = {normalize_url(d) for d in dead}
    unreach_norm = {normalize_url(d) for d in unreachable}
    bad = [u for u in urls if normalize_url(u) in dead_norm and not is_self_reference(u)]
    if bad:
        # 死链修复属内容维护（P1-8）：R6 阻断自 R6_STRICT_PERIOD 起，此前仅告警
        r6_level = level("R6", "E") if ctx.get("r6_strict") else "W"
        issues.append((r6_level,
                       f"R6 死链：{len(bad)} 个登记 URL 明确不可达（404/410/451，示例：{bad[0]}）"))
    elif urls and unreachable:
        susp = [u for u in urls if normalize_url(u) in unreach_norm]
        if susp:
            issues.append(("W", f"R6 可疑：{len(susp)} 个登记 URL 网络不可达（超时/反爬，需人工复核，示例：{susp[0]}）"))

    return issues


# ---------------------------------------------------------------- 运行入口

def _registry_path_for(business_rel: str, override: str | None) -> Path:
    if override:
        return ROOT / override
    return processed_data_dir(business_rel) / "source_registry.json"


def _business_rel_for(rel_path: str) -> str:
    """由仓库相对报告路径推导业务线目录（<业务线>/reports/x.html -> <业务线>）。

    单份校验（--file）也必须取到该业务线的来源登记，否则会回退到仓库根
    data/processed/ 而永远报「登记为空」。
    """
    parts = Path(rel_path).parts
    if "reports" in parts:
        i = parts.index("reports")
        if i > 0:
            return "/".join(parts[:i])
    return ""


def _ctx_for(business_rel: str) -> dict:
    """从 business-config 读取语言规则与配置正文（读取失败按空处理，不改变行为）。"""
    cfg = ROOT / business_rel / "prompts" / "business-config.md"
    ctx: dict = {"config_text": ""}
    try:
        text = cfg.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ctx
    ctx["config_text"] = text
    m = re.search(r"\{\{SOURCE_LANGUAGE_RULE\}\}\s*=\s*(.+)", text)
    if m:
        ctx["language_rule"] = m.group(1).strip()
    m = re.search(r"\{\{SOURCE_STRATEGY\}\}\s*=\s*(.+)", text)
    if m:
        ctx["source_strategy"] = parse_source_strategy(m.group(1))
    return ctx


def _is_historical(rel: str, gate_period: str | None) -> bool:
    """报告周期是否早于 gate-period（gate-period 前置判定）。"""
    if not gate_period:
        return False
    det = detect_report(Path(rel).name)
    if not det:
        return False
    return _period_key(det[1]) < _period_key(gate_period)


def run(only_file: str | None, gate_period: str | None = None,
        registry_override: str | None = None, probe: bool = False,
        coverage: bool = False, master_path: str | None = None,
        probe_timeout: float = 3.0, probe_workers: int = 8,
        probe_lenient: bool = False) -> tuple[int, int, list[str]]:
    """执行校验 -> (errors, warnings, 输出行)。"""
    gate_period = resolve_period(gate_period) if gate_period else None
    errors = warnings = 0
    lines: list[str] = []

    if only_file:
        p = ROOT / only_file
        if not p.exists():
            lines.append(f"[ERROR] 报告不存在：{only_file}")
            return 1, 0, lines
        targets = [(only_file, p.read_text(encoding="utf-8", errors="replace"),
                    _business_rel_for(only_file))]
    else:
        targets = []
        for b in iter_business_dirs():
            for ref in iter_business_reports(b):
                f = ROOT / ref.rel
                targets.append((ref.rel, f.read_text(encoding="utf-8", errors="replace"), b.rel))

    if not targets:
        lines.append("来源校验：未发现报告，跳过")
        return 0, 0, lines

    master = load_institution_master(Path(master_path) if master_path else None)
    cov_rows: list[tuple[str, dict]] = []

    for rel, text, business_rel in targets:
        reg_path = _registry_path_for(business_rel, registry_override)
        registry = load_registry(reg_path)
        ctx = _ctx_for(business_rel) if business_rel else {"config_text": ""}
        ctx["historical"] = _is_historical(rel, gate_period)
        det = detect_report(Path(rel).name)
        ctx["r6_strict"] = bool(det and det[1]) and _period_key(det[1]) >= _period_key(R6_STRICT_PERIOD)

        if probe:
            urls = set(extract_urls(text)) | {s.get("url") for s in registry.get("sources", []) if s.get("url")}
            dead, unreachable = probe_urls_detail(sorted(urls), timeout=probe_timeout,
                                                workers=probe_workers)
            # lenient（CI 口径）：明确死链阻断，网络不可达仅告警；strict：两者都阻断
            ctx["dead_urls"] = dead | unreachable if not probe_lenient else dead
            ctx["unreachable_urls"] = unreachable if probe_lenient else set()

        issues = check_report(text, registry, ctx)
        issues += check_institution_consistency(registry, master, ctx.get("config_text", ""), ctx)
        issues += check_registry_fields(registry, ctx)

        for level, msg in issues:
            lines.append(f"[{level}] {rel}: {msg}")
            if level == "E":
                errors += 1
            elif level == "W":
                warnings += 1

        if coverage:
            cov = coverage_report(registry, text)
            cov_rows.append((rel, cov))
            lines.append(f"[COV] {rel}: 引用 {cov['cited']} / 登记 {cov['registered']} / "
                         f"匹配 {cov['matched']} / 覆盖率 {cov['coverage']:.1%}")

    if coverage and cov_rows:
        cited = sum(c["cited"] for _, c in cov_rows)
        matched = sum(c["matched"] for _, c in cov_rows)
        lines.append(f"[COV] 合计：引用 {cited} / 匹配 {matched} / 覆盖率 "
                     f"{(matched / cited if cited else 1.0):.1%}")

    return errors, warnings, lines


def _self_test() -> int:
    """内置合成用例自检（不依赖仓库文件）。"""
    reg = {
        "schema_version": "1.0",
        "sources": [
            {"source_id": "S1", "tier": 1, "url": "https://imf.org/a", "lang": "en", "in_synthesis": True},
            {"source_id": "S2", "tier": 2, "url": "https://oecd.org/b", "lang": "en", "in_synthesis": True},
            {"source_id": "S3", "tier": 4, "url": "https://news.example/c", "lang": "en"},
        ],
    }
    good = ('<a href="https://imf.org/a">IMF</a> <a href="https://oecd.org/b">OECD</a>'
            '<a href="https://news.example/c">Media</a> 需核实原文 来源 1,000 亿')
    bad = '<a href="https://unknown.example/x">x</a> 500 亿'
    ok = True
    if any(lvl == "E" for lvl, _ in check_report(good, reg, {"language_rule": "official_en"})):
        print("[FAIL] 合规样例不应有 E"); ok = False
    if not any(lvl == "E" and "R1" in msg for lvl, msg in check_report(bad, reg)):
        print("[FAIL] 未登记 URL 应触发 R1"); ok = False

    # 邻近判定：标注远离链接（超出窗口）应判 E
    far = ('<a href="https://news.example/c">media</a>' + "填充" * 200 + "需核实原文")
    if not any(lvl == "E" and "R2" in msg for lvl, msg in check_report(far, reg)):
        print("[FAIL] 远离链接的标注不应视为邻近"); ok = False

    # R5 token 化分级：official_en -> E；en_or_zh 对集外语言 -> W
    zh_reg = {"schema_version": "1.0", "sources": [
        {"source_id": "Z1", "tier": 1, "url": "https://x.example/a", "lang": "zh"}]}
    ja_reg = {"schema_version": "1.0", "sources": [
        {"source_id": "J1", "tier": 1, "url": "https://x.example/a", "lang": "ja"}]}
    if not any(lvl == "E" and "R5" in msg for lvl, msg in check_report(
            '<a href="https://x.example/a">a</a>', zh_reg, {"language_rule": "official_en"})):
        print("[FAIL] official_en 规则应判 E"); ok = False
    if not any(lvl == "W" and "R5" in msg for lvl, msg in check_report(
            '<a href="https://x.example/a">a</a>', ja_reg, {"language_rule": "en_or_zh"})):
        print("[FAIL] en_or_zh 规则对集外语言应为 W"); ok = False
    # 自然语言规则解析：『仅英文…』-> official_en
    if parse_language_rule("仅英文（全部取自英文网站，严禁中文来源）")["severity"] != "E":
        print("[FAIL] 『仅英文』应解析为 official_en / E"); ok = False

    # gate-period 前置：历史报告 R1 / R6 均降级为 W，新报告 R6 仍 [E]
    hist = {"schema_version": "1.0", "sources": [
        {"source_id": "S1", "tier": 1, "url": "https://imf.org/a"}]}
    h_issues = check_report('<a href="https://unknown.example/x">x</a>', hist, {"historical": True})
    if not any(lvl == "W" and "R1" in msg for lvl, msg in h_issues):
        print("[FAIL] 历史报告 R1 应降级为 W"); ok = False
    d_issues = check_report('<a href="https://imf.org/a">a</a>', hist,
                            {"historical": True, "dead_urls": {"https://imf.org/a"}})
    if not any(lvl == "W" and "R6" in msg for lvl, msg in d_issues):
        print("[FAIL] 历史报告 R6 死链应降级为 W（不追溯阻断）"); ok = False
    n_issues = check_report('<a href="https://imf.org/a">a</a>', hist,
                            {"dead_urls": {"https://imf.org/a"}, "r6_strict": True})
    if not any(lvl == "E" and "R6" in msg for lvl, msg in n_issues):
        print("[FAIL] R6 阻断期内的报告死链应阻断"); ok = False
    pre_issues = check_report('<a href="https://imf.org/a">a</a>', hist,
                              {"dead_urls": {"https://imf.org/a"}})
    if not any(lvl == "W" and "R6" in msg for lvl, msg in pre_issues):
        print("[FAIL] R6 阻断生效前死链应仅告警（P1-8 集中清理期）"); ok = False

    # 机构分级主数据一致性
    master = {"schema_version": "1.0", "institutions": [
        {"name": "IMF", "tier": 1, "aliases": ["International Monetary Fund"]}]}
    mreg = {"schema_version": "1.0", "sources": [
        {"source_id": "S1", "tier": 2, "publisher": "IMF", "url": "https://imf.org/a"}]}
    if not any("R7" in msg for _, msg in check_institution_consistency(mreg, master)):
        print("[FAIL] 机构分级与主数据不一致应触发 R7"); ok = False

    # 综合层来源策略：synthesis_only + 空登记 + 无 URL 豁免；含 URL 仍须登记
    empty_reg = {"schema_version": "1.0", "sources": []}
    syn = check_report("纯文本无链接", empty_reg, {"source_strategy": "synthesis_only"})
    if any("R1" in msg for _, msg in syn):
        print("[FAIL] synthesis_only 综合层不应触发 R1 空登记告警"); ok = False
    syn_url = check_report('<a href="https://x.example/a">a</a>', empty_reg,
                           {"source_strategy": "synthesis_only"})
    if not any(lvl == "E" and "R1" in msg for lvl, msg in syn_url):
        print("[FAIL] synthesis_only 含外部 URL 仍应触发 R1"); ok = False

    print("[self-test] " + ("通过" if ok else "失败"))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="来源登记前置校验（L0 入口拦截）")
    ap.add_argument("--file", help="只校验单份报告（仓库相对路径）")
    ap.add_argument("--registry", help="来源登记路径覆盖（仓库相对路径）")
    ap.add_argument("--gate-period", help="早于该周期的报告降级为警告（如 2026-12）")
    ap.add_argument("--master", help="机构级分级主数据路径覆盖（仓库相对路径）")
    ap.add_argument("--probe", action="store_true", help="自动探测外部 URL 可达性并接入 R6（并发，默认 8 线程 / 3s 超时）")
    ap.add_argument("--probe-timeout", type=float, default=3.0, help="单 URL 探测超时（秒）")
    ap.add_argument("--probe-workers", type=int, default=8, help="并发探测线程数")
    ap.add_argument("--probe-lenient", action="store_true",
                    help="网络不可达仅告警（CI 口径）；默认严格模式将超时/反爬也计为死链")
    ap.add_argument("--coverage", action="store_true", help="输出来源登记覆盖率")
    ap.add_argument("--quiet", action="store_true", help="仅输出汇总")
    ap.add_argument("--self-test", action="store_true", help="内置合成用例自检")
    args = ap.parse_args()

    if args.self_test:
        return _self_test()

    if args.gate_period and not valid_period(args.gate_period):
        print(f"[ERROR] --gate-period 无法解析：{args.gate_period}（支持 auto / YYYY-MM / YYYY-Qn / YYYY）")
        return 2

    errors, warnings, lines = run(args.file, args.gate_period, args.registry,
                                  probe=args.probe, coverage=args.coverage,
                                  master_path=args.master,
                                  probe_timeout=args.probe_timeout, probe_workers=args.probe_workers,
                                  probe_lenient=args.probe_lenient)
    if not args.quiet:
        for line in lines:
            print(line)
    if errors:
        print(f"来源校验失败：{errors} 项错误，{warnings} 项警告（错误项阻断）")
        return 1
    if warnings:
        print(f"来源校验存在 {warnings} 项警告（无错误，不阻断）")
        return 2
    print("来源校验通过：全部报告来源登记合规")
    return 0


if __name__ == "__main__":
    sys.exit(main())
