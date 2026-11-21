#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""来源归一化（INFORMATION-VERIFICATION-SPEC v1.0 第 3 节）。

为核验台账 / 定期复核 / 机构一致性提供**可复用**的归一化原语：

  - URL：NFKC、小写 scheme/host、去 fragment、去跟踪参数（utm_* / fbclid / gclid …）；
  - 机构名：NFKC、全角→半角、压缩空白、去首尾标点；
  - 主机键：注册域（去 ``www.``），用于跨登记同一机构归并；
  - 日期：多种格式 -> ``YYYY-MM-DD``（含中文年月日）。

与 ``source_check.py`` 内部的 ``normalize_url`` 分工不同：后者服务 R1/R6 的
**可达性**比对，刻意保守（不动 path、不去参数，避免把可访问链接误判为死链）；
本模块服务**登记去重 / 归并 / 复核**，做更激进的清洗。两者不得互相替换。
"""
from __future__ import annotations

import re
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

# 常见跟踪 / 分享参数（登记与复核时剔除，避免同一 URL 因参数不同被当作两条来源）
TRACKING_PARAMS = frozenset({
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "utm_id", "utm_sourceplatform", "utm_creative", "utm_marketing_tactic",
    "fbclid", "gclid", "dclid", "msclkid", "yclid", "mc_eid", "_ga", "_gl",
    "ref", "ref_src", "ref_url", "spm", "scm",
})

_DEFAULT_PORTS = {"http": "80", "https": "443"}

_FULLWIDTH_SPACE_RE = re.compile(r"[\u3000\u00a0]")
_WS_RE = re.compile(r"\s+")
# 机构名首尾噪声标点（含全角）
_EDGE_PUNCT_RE = re.compile(r"^[\s.,，。·•()（）\[\]【】\-—_]+|[\s.,，。·•()（）\[\]【】\-—_]+$")

# 日期：YYYY-MM-DD / YYYY/MM/DD / YYYY.MM.DD
_ISO_DATE_RE = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$")
# 日期：YYYY年M月D日（可缺日）
_CN_DATE_RE = re.compile(r"^(\d{4})\s*年\s*(\d{1,2})\s*月(?:\s*(\d{1,2})\s*日)?$")
# 日期：DD Month YYYY / Month DD, YYYY（英文月份）
_EN_MONTHS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9, "oct": 10,
    "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
}
_EN_DATE_1_RE = re.compile(r"^(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})$")
_EN_DATE_2_RE = re.compile(r"^([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})$")


def normalize_url(url) -> str:
    """URL 归一化：NFKC、小写 scheme/host、去 fragment、去跟踪参数。

    路径保持原样（区分大小写），查询参数顺序保持但剔除跟踪项；
    空 URL / 非字符串返回空串。
    """
    if not isinstance(url, str):
        return ""
    s = unicodedata.normalize("NFKC", url).strip()
    if not s:
        return ""
    s = s.split("#", 1)[0].strip()
    try:
        p = urlparse(s)
    except ValueError:
        return s
    scheme = (p.scheme or "").lower()
    host = (p.hostname or "").lower()
    try:
        port = p.port
    except ValueError:
        port = None
    if port is not None and str(port) != _DEFAULT_PORTS.get(scheme):
        host = f"{host}:{port}"
    kept = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
            if k.lower() not in TRACKING_PARAMS]
    query = urlencode(kept, doseq=True)
    return urlunparse((scheme, host, p.path, p.params, query, ""))


def normalize_publisher(name) -> str:
    """机构名归一：NFKC、全角空格→半角、压缩空白、去首尾噪声标点。"""
    if not isinstance(name, str):
        return ""
    s = unicodedata.normalize("NFKC", name)
    s = _FULLWIDTH_SPACE_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s).strip()
    s = _EDGE_PUNCT_RE.sub("", s).strip()
    return s


def host_key(url) -> str:
    """注册域键：小写 host、去 ``www.`` 前缀；用于跨登记同一机构归并。"""
    s = normalize_url(url)
    if not s:
        return ""
    try:
        host = (urlparse(s).hostname or "").lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def normalize_date(value) -> str | None:
    """多种日期格式 -> ``YYYY-MM-DD``；无法识别返回 ``None``。"""
    if not isinstance(value, str):
        return None
    s = unicodedata.normalize("NFKC", value).strip()
    if not s:
        return None
    m = _ISO_DATE_RE.match(s)
    if m:
        y, mo, d = (int(x) for x in m.groups())
    else:
        m = _CN_DATE_RE.match(s)
        if m:
            y, mo = int(m.group(1)), int(m.group(2))
            d = int(m.group(3)) if m.group(3) else 1
        else:
            m = _EN_DATE_1_RE.match(s)
            if m:
                d, mon, y = int(m.group(1)), _EN_MONTHS.get(m.group(2).lower()), int(m.group(3))
            else:
                m = _EN_DATE_2_RE.match(s)
                if m:
                    mon, d, y = _EN_MONTHS.get(m.group(1).lower()), int(m.group(2)), int(m.group(3))
                else:
                    return None
            if mon is None:
                return None
            mo = int(mon)
    if not (1 <= mo <= 12 and 1 <= d <= 31):
        return None
    return f"{y:04d}-{mo:02d}-{d:02d}"


__all__ = [
    "TRACKING_PARAMS",
    "normalize_url",
    "normalize_publisher",
    "host_key",
    "normalize_date",
]
