"""离线示例数据（合成占位，非真实新闻）。

用途：网络不可达 / 首次启动时的兜底，保证看板与验证流程可演示。
所有条目 is_demo=True、url 为空，前端禁用外部链接；标题统一「示例·」前缀，
避免与真实抓取内容混淆。绝不作为事实依据，也不出现在准确性核验的通过口径中。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from .models import NewsItem

_DEMO_SOURCES = {
    "bbc-world": ("BBC News - World", "media_t1"),
    "guardian-world": ("The Guardian - World", "media_t1"),
    "nyt-world": ("The New York Times - World", "media_t1"),
    "wapo-world": ("The Washington Post - World", "media_t1"),
    "france24-en": ("France 24 - English", "media"),
    "dw-en": ("Deutsche Welle - English", "media"),
    "aljazeera-en": ("Al Jazeera - English", "media"),
    "npr-world": ("NPR - World", "media"),
    "cnn-edition": ("CNN - International Edition", "media"),
    "pbs-newshour": ("PBS NewsHour", "media"),
    "whitehouse": ("The White House", "official"),
    "imf-news": ("International Monetary Fund - News", "official"),
}


def _demo_id(source_id: str, slug: str) -> str:
    return f"demo-{source_id}-{slug}"


def _item(source_id: str, slug: str, title: str, age_h: float, summary: str) -> NewsItem:
    name, tier = _DEMO_SOURCES[source_id]
    ts = (datetime.now(timezone.utc) - timedelta(hours=age_h)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return NewsItem(
        id=_demo_id(source_id, slug),
        title=f"示例·{title}",
        url="",
        source_id=source_id,
        source_name=name,
        tier=tier,
        published_at=ts,
        summary=summary,
        is_demo=True,
    )


def build_seed_items() -> list[NewsItem]:
    """约 26 条示例报道，聚成 10 个事件簇（标题相似以便聚类器合并）。"""
    rows: list[tuple[str, str, str, float, str]] = [
        ("bbc-world", "hormuz-1", "Strait of Hormuz shipping reroutes after fresh security warnings", 1.0, "示例摘要：合成事件，仅演示布局。"),
        ("guardian-world", "hormuz-1", "Strait of Hormuz shipping reroutes as insurers raise war-risk premiums", 2.5, "示例摘要：合成事件，仅演示布局。"),
        ("aljazeera-en", "hormuz-1", "Strait of Hormuz traffic thins amid war-risk insurance surge", 4.0, "示例摘要：合成事件，仅演示布局。"),
        ("nyt-world", "fed-1", "Federal Reserve holds interest rates steady, signals caution on inflation", 0.8, "示例摘要：合成事件，仅演示布局。"),
        ("wapo-world", "fed-1", "Federal Reserve keeps interest rates unchanged amid inflation debate", 1.6, "示例摘要：合成事件，仅演示布局。"),
        ("pbs-newshour", "fed-1", "Federal Reserve decision on interest rates draws mixed reactions", 3.2, "示例摘要：合成事件，仅演示布局。"),
        ("aljazeera-en", "opec-1", "OPEC+ weighs output increase as oil prices steady", 2.0, "示例摘要：合成事件，仅演示布局。"),
        ("bbc-world", "opec-1", "OPEC+ output decision in focus as crude oil markets react", 5.5, "示例摘要：合成事件，仅演示布局。"),
        ("france24-en", "ai-1", "EU ministers debate new AI regulation package for data centers", 1.2, "示例摘要：合成事件，仅演示布局。"),
        ("guardian-world", "ai-1", "European AI regulation talks intensify over chip export rules", 2.8, "示例摘要：合成事件，仅演示布局。"),
        ("dw-en", "ai-1", "Berlin hosts European talks on artificial intelligence regulation", 6.0, "示例摘要：合成事件，仅演示布局。"),
        ("bbc-world", "climate-1", "Climate summit negotiators clash over emission targets", 3.5, "示例摘要：合成事件，仅演示布局。"),
        ("france24-en", "climate-1", "Climate summit draft text divides emitters and island states", 7.0, "示例摘要：合成事件，仅演示布局。"),
        ("cnn-edition", "election-1", "Election officials certify results after tight coalition talks", 1.8, "示例摘要：合成事件，仅演示布局。"),
        ("npr-world", "election-1", "Election aftermath: coalition talks dominate parliament agenda", 4.5, "示例摘要：合成事件，仅演示布局。"),
        ("pbs-newshour", "vaccine-1", "WHO panel reviews vaccine guidance for outbreak response", 2.2, "示例摘要：合成事件，仅演示布局。"),
        ("npr-world", "vaccine-1", "Health agencies update vaccine guidance as outbreak spreads", 5.0, "示例摘要：合成事件，仅演示布局。"),
        ("wapo-world", "tariff-1", "Trade talks stall as tariff threat returns to agenda", 0.9, "示例摘要：合成事件，仅演示布局。"),
        ("nyt-world", "tariff-1", "Tariff dispute shadows trade talks between major economies", 2.6, "示例摘要：合成事件，仅演示布局。"),
        ("cnn-edition", "tariff-1", "Trade representatives meet to defuse tariff standoff", 6.5, "示例摘要：合成事件，仅演示布局。"),
        ("bbc-world", "quake-1", "Earthquake rescue teams search rubble as aftershocks continue", 1.4, "示例摘要：合成事件，仅演示布局。"),
        ("dw-en", "quake-1", "Earthquake response shifts to shelter as death toll rises", 3.8, "示例摘要：合成事件，仅演示布局。"),
        ("france24-en", "sanc-1", "Sanctions package cleared after marathon negotiation session", 2.1, "示例摘要：合成事件，仅演示布局。"),
        ("aljazeera-en", "sanc-1", "New sanctions measures draw cautious diplomatic response", 4.9, "示例摘要：合成事件，仅演示布局。"),
        ("guardian-world", "chip-1", "Semiconductor supply chain faces new export control strain", 1.1, "示例摘要：合成事件，仅演示布局。"),
        ("dw-en", "chip-1", "Chip makers warn over semiconductor export controls", 3.3, "示例摘要：合成事件，仅演示布局。"),
    ]
    return [_item(*row) for row in rows]


def seed_config() -> dict[str, Any]:
    """示例数据对应的热度权重（与白名单配置一致，单独返回避免依赖文件路径）。"""
    return {"heat_weights": {"official": 3.0, "rating": 3.0, "media_t1": 2.5, "media": 2.0}}
