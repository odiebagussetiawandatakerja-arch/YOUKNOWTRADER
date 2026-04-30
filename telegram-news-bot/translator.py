"""
Translation module - auto-translate news to Indonesian.
Uses deep-translator with Google Translate (free, no API key needed).
Falls back gracefully if translation fails.
"""

import logging
import asyncio
from functools import partial
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

# Reusable translator instance
_translator = GoogleTranslator(source="auto", target="id")

# Simple in-memory cache to avoid re-translating the same text
_cache: dict[str, str] = {}
_CACHE_MAX_SIZE = 5000


def _translate_sync(text: str) -> str:
    """Synchronous translation (runs in thread pool)."""
    if not text or not text.strip():
        return text

    if text in _cache:
        return _cache[text]

    try:
        # deep-translator has a max char limit per request (~5000)
        # Split long texts if needed
        if len(text) > 4500:
            chunks = _split_text(text, 4500)
            translated_chunks = [_translator.translate(chunk) for chunk in chunks]
            result = " ".join(translated_chunks)
        else:
            result = _translator.translate(text)

        if result:
            # Manage cache size
            if len(_cache) >= _CACHE_MAX_SIZE:
                # Remove oldest half of cache
                keys_to_remove = list(_cache.keys())[: _CACHE_MAX_SIZE // 2]
                for k in keys_to_remove:
                    del _cache[k]
            _cache[text] = result
            return result
        return text
    except Exception as e:
        logger.warning("Translation failed for '%s...': %s", text[:50], e)
        return text


def _split_text(text: str, max_len: int) -> list[str]:
    """Split text into chunks at sentence boundaries."""
    sentences = text.replace(". ", ".|").split("|")
    chunks: list[str] = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) > max_len:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += sentence

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks if chunks else [text[:max_len]]


async def translate_text(text: str) -> str:
    """Async wrapper for translation. Runs in thread pool to avoid blocking."""
    if not text or not text.strip():
        return text

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(_translate_sync, text))


async def translate_news_item(title: str, summary: str) -> tuple[str, str]:
    """Translate both title and summary of a news item."""
    translated_title, translated_summary = await asyncio.gather(
        translate_text(title),
        translate_text(summary),
    )
    return translated_title, translated_summary


def is_indonesian(text: str) -> bool:
    """
    Simple heuristic to detect if text is already in Indonesian.
    Checks for common Indonesian words to avoid unnecessary translation.
    """
    if not text:
        return False

    indo_markers = [
        "yang", "dan", "dari", "untuk", "dengan", "ini", "itu",
        "pada", "akan", "telah", "sudah", "tidak", "juga", "atau",
        "dalam", "oleh", "karena", "bahwa", "saham", "harga",
        "rupiah", "persen", "naik", "turun", "pasar", "investasi",
    ]
    lower_text = text.lower()
    word_count = len(lower_text.split())

    if word_count < 3:
        return False

    matches = sum(1 for marker in indo_markers if marker in lower_text)
    # If more than 15% of markers are found relative to word count, likely Indonesian
    return matches >= max(2, word_count * 0.15)
