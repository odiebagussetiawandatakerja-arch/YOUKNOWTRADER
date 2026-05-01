import re
import logging
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

URL_PATTERN = re.compile(
    r"https?://[^\s<>\"']+",
    re.IGNORECASE,
)


def extract_urls(text: str) -> list[str]:
    if not text:
        return []
    return URL_PATTERN.findall(text)


async def fetch_page_title(url: str) -> Optional[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=8),
                headers={"User-Agent": "Mozilla/5.0 BookmarkBot/1.0"},
                allow_redirects=True,
            ) as resp:
                if resp.status != 200:
                    return None
                ct = resp.headers.get("Content-Type", "")
                if "text/html" not in ct:
                    return None
                html = await resp.text(errors="replace")
                soup = BeautifulSoup(html, "html.parser")
                if soup.title and soup.title.string:
                    title = soup.title.string.strip()
                    if len(title) > 200:
                        title = title[:200] + "..."
                    return title
    except Exception as e:
        logger.debug("Failed to fetch title for %s: %s", url, e)
    return None


def truncate(text: str, max_len: int = 100) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def format_bookmark(bookmark: dict, tags: list[str] | None = None) -> str:
    lines = []
    pin = "\U0001F4CC " if bookmark.get("is_pinned") else ""
    type_emoji = {
        "text": "\U0001F4DD",
        "link": "\U0001F517",
        "photo": "\U0001F5BC",
        "video": "\U0001F3AC",
        "document": "\U0001F4CE",
        "audio": "\U0001F3B5",
        "voice": "\U0001F3A4",
        "sticker": "\U0001F600",
    }.get(bookmark["content_type"], "\U0001F4DD")

    lines.append(f"{pin}{type_emoji} <b>#{bookmark['id']}</b>")

    if bookmark.get("title"):
        lines.append(f"<b>{bookmark['title']}</b>")

    if bookmark.get("url"):
        lines.append(f"\U0001F517 {bookmark['url']}")

    content = bookmark.get("content", "")
    if content and content != bookmark.get("url", ""):
        lines.append(truncate(content, 200))

    if tags:
        tag_str = " ".join(f"#{t}" for t in tags)
        lines.append(f"\U0001F3F7 {tag_str}")

    lines.append(f"\U0001F552 {bookmark['created_at']}")
    return "\n".join(lines)


def format_bookmark_short(bookmark: dict) -> str:
    pin = "\U0001F4CC" if bookmark.get("is_pinned") else ""
    title = bookmark.get("title") or truncate(bookmark.get("content", ""), 50)
    return f"{pin}<b>#{bookmark['id']}</b> {title}"
