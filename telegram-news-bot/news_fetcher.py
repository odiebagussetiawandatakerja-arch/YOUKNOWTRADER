"""
News fetcher module - aggregates news from multiple RSS feeds.
Designed for maximum speed with async parallel fetching.
"""

import hashlib
import html
import logging
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone

import aiohttp
import feedparser

from config import ALL_CATEGORIES, MAX_ITEMS_PER_FETCH

logger = logging.getLogger(__name__)

# Global aiohttp session (reused for connection pooling / speed)
_session: aiohttp.ClientSession | None = None


@dataclass
class NewsItem:
    """Represents a single news item."""
    title: str
    summary: str
    url: str
    source: str
    category: str
    published: datetime
    hash: str = field(default="")

    def __post_init__(self) -> None:
        if not self.hash:
            raw = f"{self.title.strip().lower()}|{self.url.strip().lower()}"
            self.hash = hashlib.sha256(raw.encode()).hexdigest()[:16]


def _clean_html(raw_html: str) -> str:
    """Remove HTML tags and decode entities."""
    if not raw_html:
        return ""
    clean = re.sub(r"<[^>]+>", "", raw_html)
    clean = html.unescape(clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    # Truncate long summaries
    if len(clean) > 500:
        clean = clean[:497] + "..."
    return clean


def _parse_date(entry: dict) -> datetime:
    """Parse published date from RSS entry."""
    for date_field in ("published_parsed", "updated_parsed"):
        parsed = entry.get(date_field)
        if parsed:
            try:
                return datetime(*parsed[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                pass

    for date_str_field in ("published", "updated"):
        date_str = entry.get(date_str_field, "")
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                pass

    return datetime.now(timezone.utc)


async def get_session() -> aiohttp.ClientSession:
    """Get or create the global aiohttp session."""
    global _session
    if _session is None or _session.closed:
        timeout = aiohttp.ClientTimeout(total=15, connect=5)
        _session = aiohttp.ClientSession(
            timeout=timeout,
            headers={
                "User-Agent": "YouKnowTrader-NewsBot/1.0 (+https://github.com/YOUKNOWTRADER)"
            },
        )
    return _session


async def close_session() -> None:
    """Close the global aiohttp session."""
    global _session
    if _session and not _session.closed:
        await _session.close()
        _session = None


async def fetch_feed(
    source_name: str, feed_url: str, category: str
) -> list[NewsItem]:
    """Fetch and parse a single RSS feed."""
    items: list[NewsItem] = []
    try:
        session = await get_session()
        start = time.monotonic()

        async with session.get(feed_url) as response:
            if response.status != 200:
                logger.warning(
                    "[%s] HTTP %d from %s", source_name, response.status, feed_url
                )
                return items

            content = await response.text()
            elapsed = time.monotonic() - start
            logger.debug("[%s] Fetched in %.2fs", source_name, elapsed)

        feed = feedparser.parse(content)

        for entry in feed.entries[:MAX_ITEMS_PER_FETCH]:
            title = _clean_html(entry.get("title", ""))
            if not title:
                continue

            summary = _clean_html(
                entry.get("summary", entry.get("description", ""))
            )
            url = entry.get("link", entry.get("id", ""))
            published = _parse_date(entry)

            items.append(
                NewsItem(
                    title=title,
                    summary=summary,
                    url=url,
                    source=source_name,
                    category=category,
                    published=published,
                )
            )

    except aiohttp.ClientError as e:
        logger.warning("[%s] Network error: %s", source_name, e)
    except Exception as e:
        logger.warning("[%s] Parse error: %s", source_name, e)

    return items


async def fetch_category(category: str) -> list[NewsItem]:
    """Fetch all feeds for a specific category in parallel."""
    import asyncio

    feeds = ALL_CATEGORIES.get(category, [])
    if not feeds:
        return []

    tasks = [
        fetch_feed(source_name, feed_url, category)
        for source_name, feed_url in feeds
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_items: list[NewsItem] = []
    for result in results:
        if isinstance(result, list):
            all_items.extend(result)
        elif isinstance(result, Exception):
            logger.warning("Feed fetch error: %s", result)

    # Sort by published date (newest first)
    all_items.sort(key=lambda x: x.published, reverse=True)
    return all_items


async def fetch_all_categories() -> dict[str, list[NewsItem]]:
    """Fetch all categories in parallel for maximum speed."""
    import asyncio

    categories = list(ALL_CATEGORIES.keys())
    tasks = [fetch_category(cat) for cat in categories]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    output: dict[str, list[NewsItem]] = {}
    for cat, result in zip(categories, results):
        if isinstance(result, list):
            output[cat] = result
        else:
            logger.warning("Category %s fetch error: %s", cat, result)
            output[cat] = []

    return output
