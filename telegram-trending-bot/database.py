"""SQLite database for storing scraped trending hotel & attraction data."""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "trending.db"


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            name TEXT NOT NULL,
            stars INTEGER DEFAULT 3,
            rating REAL,
            reviews INTEGER DEFAULT 0,
            price TEXT,
            platform TEXT,
            highlight TEXT,
            url TEXT,
            scraped_at TEXT NOT NULL,
            UNIQUE(city, name, platform)
        );

        CREATE TABLE IF NOT EXISTS attractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            name TEXT NOT NULL,
            price TEXT,
            platform TEXT,
            booked TEXT,
            highlight TEXT,
            url TEXT,
            scraped_at TEXT NOT NULL,
            UNIQUE(city, name, platform)
        );

        CREATE TABLE IF NOT EXISTS scrape_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            category TEXT NOT NULL,
            source TEXT NOT NULL,
            status TEXT NOT NULL,
            items_found INTEGER DEFAULT 0,
            scraped_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_hotels_city ON hotels(city);
        CREATE INDEX IF NOT EXISTS idx_attractions_city ON attractions(city);
        CREATE INDEX IF NOT EXISTS idx_scrape_log_city ON scrape_log(city, scraped_at);
    """)
    conn.commit()
    conn.close()


def upsert_hotel(
    city: str,
    name: str,
    stars: int,
    rating: float | None,
    reviews: int,
    price: str,
    platform: str,
    highlight: str,
    url: str,
) -> None:
    conn = get_db()
    now = datetime.now().isoformat()
    conn.execute(
        """
        INSERT INTO hotels (city, name, stars, rating, reviews, price, platform, highlight, url, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(city, name, platform) DO UPDATE SET
            stars=excluded.stars,
            rating=excluded.rating,
            reviews=excluded.reviews,
            price=excluded.price,
            highlight=excluded.highlight,
            url=excluded.url,
            scraped_at=excluded.scraped_at
        """,
        (city, name, stars, rating, reviews, price, platform, highlight, url, now),
    )
    conn.commit()
    conn.close()


def upsert_attraction(
    city: str,
    name: str,
    price: str,
    platform: str,
    booked: str,
    highlight: str,
    url: str,
) -> None:
    conn = get_db()
    now = datetime.now().isoformat()
    conn.execute(
        """
        INSERT INTO attractions (city, name, price, platform, booked, highlight, url, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(city, name, platform) DO UPDATE SET
            price=excluded.price,
            booked=excluded.booked,
            highlight=excluded.highlight,
            url=excluded.url,
            scraped_at=excluded.scraped_at
        """,
        (city, name, price, platform, booked, highlight, url, now),
    )
    conn.commit()
    conn.close()


def log_scrape(city: str, category: str, source: str, status: str, items: int) -> None:
    conn = get_db()
    now = datetime.now().isoformat()
    conn.execute(
        "INSERT INTO scrape_log (city, category, source, status, items_found, scraped_at) VALUES (?, ?, ?, ?, ?, ?)",
        (city, category, source, status, items, now),
    )
    conn.commit()
    conn.close()


def get_hotels(city: str, limit: int = 10) -> list[dict]:
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM hotels WHERE city=? ORDER BY rating DESC, reviews DESC LIMIT ?",
        (city, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_attractions(city: str, limit: int = 10) -> list[dict]:
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM attractions WHERE city=? ORDER BY id ASC LIMIT ?",
        (city, limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_last_scrape(city: str | None = None) -> str | None:
    conn = get_db()
    if city:
        row = conn.execute(
            "SELECT scraped_at FROM scrape_log WHERE city=? ORDER BY scraped_at DESC LIMIT 1",
            (city,),
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT scraped_at FROM scrape_log ORDER BY scraped_at DESC LIMIT 1"
        ).fetchone()
    conn.close()
    return row["scraped_at"] if row else None


def get_scrape_stats() -> list[dict]:
    conn = get_db()
    rows = conn.execute("""
        SELECT city,
               COUNT(DISTINCT CASE WHEN category='hotel' THEN source END) as hotel_sources,
               SUM(CASE WHEN category='hotel' THEN items_found ELSE 0 END) as total_hotels,
               COUNT(DISTINCT CASE WHEN category='attraction' THEN source END) as attraction_sources,
               SUM(CASE WHEN category='attraction' THEN items_found ELSE 0 END) as total_attractions,
               MAX(scraped_at) as last_update
        FROM scrape_log
        WHERE status='success'
        GROUP BY city
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_hotel_count(city: str) -> int:
    conn = get_db()
    row = conn.execute("SELECT COUNT(*) as cnt FROM hotels WHERE city=?", (city,)).fetchone()
    conn.close()
    return row["cnt"]


def get_attraction_count(city: str) -> int:
    conn = get_db()
    row = conn.execute("SELECT COUNT(*) as cnt FROM attractions WHERE city=?", (city,)).fetchone()
    conn.close()
    return row["cnt"]
