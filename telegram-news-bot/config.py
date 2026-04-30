"""
Configuration for Telegram News Bot.
All settings are loaded from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token (get from @BotFather)
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Channel/Group ID where news will be posted (optional, for auto-broadcast)
TELEGRAM_CHANNEL_ID: str = os.getenv("TELEGRAM_CHANNEL_ID", "")

# Polling interval in seconds (how often to check for new news)
POLL_INTERVAL: int = int(os.getenv("POLL_INTERVAL", "60"))

# Database path for dedup tracking
DB_PATH: str = os.getenv("DB_PATH", "news_bot.db")

# Target translation language
TARGET_LANG: str = os.getenv("TARGET_LANG", "id")  # Indonesian

# Max news items per fetch per source
MAX_ITEMS_PER_FETCH: int = int(os.getenv("MAX_ITEMS_PER_FETCH", "5"))

# ─── RSS Feed Sources ────────────────────────────────────────────────
# Each category maps to a list of (name, url) tuples.

CRYPTO_FEEDS: list[tuple[str, str]] = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("CoinTelegraph", "https://cointelegraph.com/rss"),
    ("CryptoSlate", "https://cryptoslate.com/feed/"),
    ("Bitcoin Magazine", "https://bitcoinmagazine.com/feed"),
    ("Decrypt", "https://decrypt.co/feed"),
    ("The Block", "https://www.theblock.co/rss.xml"),
    ("CryptoNews", "https://cryptonews.com/news/feed/"),
]

FOREX_FEEDS: list[tuple[str, str]] = [
    ("DailyFX", "https://www.dailyfx.com/feeds/all"),
    ("FXStreet", "https://www.fxstreet.com/rss/news"),
    ("Investing.com Forex", "https://www.investing.com/rss/news_14.rss"),
    ("ForexLive", "https://www.forexlive.com/feed/news"),
]

IDX_FEEDS: list[tuple[str, str]] = [
    ("CNBC Indonesia", "https://www.cnbcindonesia.com/market/rss"),
    ("Kontan", "https://www.kontan.co.id/rss/investasi"),
    ("Bisnis.com Saham", "https://market.bisnis.com/rss"),
    ("IDX Channel", "https://www.idxchannel.com/rss"),
    ("Detik Finance", "https://rss.detik.com/index.php/finance"),
]

COMMODITIES_FEEDS: list[tuple[str, str]] = [
    ("Kitco Gold", "https://www.kitco.com/rss/kitconewsfeed.xml"),
    ("OilPrice", "https://oilprice.com/rss/main"),
    ("Investing.com Commodities", "https://www.investing.com/rss/news_11.rss"),
]

GENERAL_FEEDS: list[tuple[str, str]] = [
    ("Reuters Business", "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best"),
    ("Yahoo Finance", "https://finance.yahoo.com/news/rssindex"),
    ("MarketWatch", "https://www.marketwatch.com/rss/topstories"),
    ("Bloomberg", "https://feeds.bloomberg.com/markets/news.rss"),
]

# All feeds grouped by category
ALL_CATEGORIES: dict[str, list[tuple[str, str]]] = {
    "crypto": CRYPTO_FEEDS,
    "forex": FOREX_FEEDS,
    "idx": IDX_FEEDS,
    "commodities": COMMODITIES_FEEDS,
    "general": GENERAL_FEEDS,
}

# Category display names and emoji
CATEGORY_DISPLAY: dict[str, str] = {
    "crypto": "Crypto",
    "forex": "Forex",
    "idx": "Saham IDX",
    "commodities": "Komoditas",
    "general": "Umum",
}

CATEGORY_EMOJI: dict[str, str] = {
    "crypto": "₿",
    "forex": "💱",
    "idx": "📈",
    "commodities": "🛢",
    "general": "📰",
}
