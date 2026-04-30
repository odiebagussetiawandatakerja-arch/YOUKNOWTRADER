"""
SQLite database module for dedup tracking and user subscriptions.
"""

import aiosqlite
from config import DB_PATH


async def init_db() -> None:
    """Initialize database tables."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sent_news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                news_hash TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                category TEXT NOT NULL,
                url TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_subscriptions (
                user_id INTEGER NOT NULL,
                chat_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (chat_id, category)
            )
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_news_hash ON sent_news(news_hash)
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_sent_at ON sent_news(sent_at)
        """)
        await db.commit()


async def is_news_sent(news_hash: str) -> bool:
    """Check if a news item has already been sent."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT 1 FROM sent_news WHERE news_hash = ?", (news_hash,)
        )
        row = await cursor.fetchone()
        return row is not None


async def mark_news_sent(
    news_hash: str, title: str, source: str, category: str, url: str
) -> None:
    """Mark a news item as sent."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT OR IGNORE INTO sent_news (news_hash, title, source, category, url)
               VALUES (?, ?, ?, ?, ?)""",
            (news_hash, title, source, category, url),
        )
        await db.commit()


async def subscribe_user(user_id: int, chat_id: int, category: str) -> bool:
    """Subscribe a user/chat to a category. Returns True if new subscription."""
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute(
                """INSERT INTO user_subscriptions (user_id, chat_id, category)
                   VALUES (?, ?, ?)""",
                (user_id, chat_id, category),
            )
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


async def unsubscribe_user(chat_id: int, category: str) -> bool:
    """Unsubscribe a user/chat from a category. Returns True if was subscribed."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM user_subscriptions WHERE chat_id = ? AND category = ?",
            (chat_id, category),
        )
        await db.commit()
        return cursor.rowcount > 0


async def get_user_subscriptions(chat_id: int) -> list[str]:
    """Get all categories a user/chat is subscribed to."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT category FROM user_subscriptions WHERE chat_id = ?",
            (chat_id,),
        )
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def get_subscribers_for_category(category: str) -> list[int]:
    """Get all chat_ids subscribed to a category."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT DISTINCT chat_id FROM user_subscriptions WHERE category = ?",
            (category,),
        )
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def get_all_subscribers() -> list[tuple[int, str]]:
    """Get all (chat_id, category) pairs."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT DISTINCT chat_id, category FROM user_subscriptions"
        )
        rows = await cursor.fetchall()
        return [(row[0], row[1]) for row in rows]


async def cleanup_old_news(days: int = 7) -> int:
    """Remove news older than N days. Returns count of removed items."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM sent_news WHERE sent_at < datetime('now', ?)",
            (f"-{days} days",),
        )
        await db.commit()
        return cursor.rowcount
