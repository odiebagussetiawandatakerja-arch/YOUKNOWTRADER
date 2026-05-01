import sqlite3
import os
from datetime import datetime
from typing import Optional

DB_PATH = os.environ.get("BOOKMARK_DB_PATH", "bookmarks.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            content_type TEXT NOT NULL DEFAULT 'text',
            url TEXT,
            title TEXT,
            file_id TEXT,
            is_pinned INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            UNIQUE(user_id, name),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS bookmark_tags (
            bookmark_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (bookmark_id, tag_id),
            FOREIGN KEY (bookmark_id) REFERENCES bookmarks(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_bookmarks_user ON bookmarks(user_id);
        CREATE INDEX IF NOT EXISTS idx_bookmarks_pinned ON bookmarks(user_id, is_pinned);
        CREATE INDEX IF NOT EXISTS idx_tags_user ON tags(user_id);
    """)
    conn.commit()
    conn.close()


def ensure_user(user_id: int, username: Optional[str], first_name: Optional[str]) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
        (user_id, username, first_name),
    )
    conn.commit()
    conn.close()


def add_bookmark(
    user_id: int,
    content: str,
    content_type: str = "text",
    url: Optional[str] = None,
    title: Optional[str] = None,
    file_id: Optional[str] = None,
) -> int:
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO bookmarks (user_id, content, content_type, url, title, file_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, content, content_type, url, title, file_id),
    )
    bookmark_id = cur.lastrowid
    conn.commit()
    conn.close()
    return bookmark_id


def get_bookmarks(
    user_id: int,
    limit: int = 5,
    offset: int = 0,
    tag: Optional[str] = None,
    content_type: Optional[str] = None,
    pinned_only: bool = False,
    search: Optional[str] = None,
) -> list[dict]:
    conn = get_connection()
    query = "SELECT DISTINCT b.* FROM bookmarks b"
    params: list = []
    conditions = ["b.user_id = ?"]
    params.append(user_id)

    if tag:
        query += " JOIN bookmark_tags bt ON b.id = bt.bookmark_id JOIN tags t ON bt.tag_id = t.id"
        conditions.append("t.name = ? AND t.user_id = ?")
        params.extend([tag, user_id])

    if content_type:
        conditions.append("b.content_type = ?")
        params.append(content_type)

    if pinned_only:
        conditions.append("b.is_pinned = 1")

    if search:
        conditions.append("(b.content LIKE ? OR b.title LIKE ? OR b.url LIKE ?)")
        s = f"%{search}%"
        params.extend([s, s, s])

    query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY b.is_pinned DESC, b.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def count_bookmarks(
    user_id: int,
    tag: Optional[str] = None,
    content_type: Optional[str] = None,
    pinned_only: bool = False,
    search: Optional[str] = None,
) -> int:
    conn = get_connection()
    query = "SELECT COUNT(DISTINCT b.id) FROM bookmarks b"
    params: list = []
    conditions = ["b.user_id = ?"]
    params.append(user_id)

    if tag:
        query += " JOIN bookmark_tags bt ON b.id = bt.bookmark_id JOIN tags t ON bt.tag_id = t.id"
        conditions.append("t.name = ? AND t.user_id = ?")
        params.extend([tag, user_id])

    if content_type:
        conditions.append("b.content_type = ?")
        params.append(content_type)

    if pinned_only:
        conditions.append("b.is_pinned = 1")

    if search:
        conditions.append("(b.content LIKE ? OR b.title LIKE ? OR b.url LIKE ?)")
        s = f"%{search}%"
        params.extend([s, s, s])

    query += " WHERE " + " AND ".join(conditions)
    count = conn.execute(query, params).fetchone()[0]
    conn.close()
    return count


def get_bookmark_by_id(bookmark_id: int, user_id: int) -> Optional[dict]:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM bookmarks WHERE id = ? AND user_id = ?",
        (bookmark_id, user_id),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def delete_bookmark(bookmark_id: int, user_id: int) -> bool:
    conn = get_connection()
    cur = conn.execute(
        "DELETE FROM bookmarks WHERE id = ? AND user_id = ?",
        (bookmark_id, user_id),
    )
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted


def toggle_pin(bookmark_id: int, user_id: int) -> Optional[bool]:
    conn = get_connection()
    row = conn.execute(
        "SELECT is_pinned FROM bookmarks WHERE id = ? AND user_id = ?",
        (bookmark_id, user_id),
    ).fetchone()
    if not row:
        conn.close()
        return None
    new_val = 0 if row["is_pinned"] else 1
    conn.execute(
        "UPDATE bookmarks SET is_pinned = ? WHERE id = ? AND user_id = ?",
        (new_val, bookmark_id, user_id),
    )
    conn.commit()
    conn.close()
    return bool(new_val)


def add_tag(user_id: int, tag_name: str) -> int:
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO tags (user_id, name) VALUES (?, ?)",
        (user_id, tag_name.lower().strip()),
    )
    row = conn.execute(
        "SELECT id FROM tags WHERE user_id = ? AND name = ?",
        (user_id, tag_name.lower().strip()),
    ).fetchone()
    tag_id = row["id"]
    conn.commit()
    conn.close()
    return tag_id


def tag_bookmark(bookmark_id: int, tag_id: int) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO bookmark_tags (bookmark_id, tag_id) VALUES (?, ?)",
        (bookmark_id, tag_id),
    )
    conn.commit()
    conn.close()


def untag_bookmark(bookmark_id: int, tag_id: int) -> None:
    conn = get_connection()
    conn.execute(
        "DELETE FROM bookmark_tags WHERE bookmark_id = ? AND tag_id = ?",
        (bookmark_id, tag_id),
    )
    conn.commit()
    conn.close()


def get_bookmark_tags(bookmark_id: int) -> list[str]:
    conn = get_connection()
    rows = conn.execute(
        """SELECT t.name FROM tags t
           JOIN bookmark_tags bt ON t.id = bt.tag_id
           WHERE bt.bookmark_id = ?""",
        (bookmark_id,),
    ).fetchall()
    conn.close()
    return [r["name"] for r in rows]


def get_user_tags(user_id: int) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        """SELECT t.id, t.name, COUNT(bt.bookmark_id) as count
           FROM tags t
           LEFT JOIN bookmark_tags bt ON t.id = bt.tag_id
           WHERE t.user_id = ?
           GROUP BY t.id
           ORDER BY count DESC""",
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_tag_by_name(user_id: int, tag_name: str) -> Optional[dict]:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM tags WHERE user_id = ? AND name = ?",
        (user_id, tag_name.lower().strip()),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def delete_tag(tag_id: int, user_id: int) -> bool:
    conn = get_connection()
    cur = conn.execute(
        "DELETE FROM tags WHERE id = ? AND user_id = ?",
        (tag_id, user_id),
    )
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted


def get_stats(user_id: int) -> dict:
    conn = get_connection()
    total = conn.execute(
        "SELECT COUNT(*) FROM bookmarks WHERE user_id = ?", (user_id,)
    ).fetchone()[0]
    pinned = conn.execute(
        "SELECT COUNT(*) FROM bookmarks WHERE user_id = ? AND is_pinned = 1", (user_id,)
    ).fetchone()[0]
    tags_count = conn.execute(
        "SELECT COUNT(*) FROM tags WHERE user_id = ?", (user_id,)
    ).fetchone()[0]
    types = conn.execute(
        "SELECT content_type, COUNT(*) as c FROM bookmarks WHERE user_id = ? GROUP BY content_type",
        (user_id,),
    ).fetchall()
    conn.close()
    return {
        "total": total,
        "pinned": pinned,
        "tags": tags_count,
        "types": {r["content_type"]: r["c"] for r in types},
    }


def export_bookmarks(user_id: int) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM bookmarks WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()
    bookmarks = []
    for r in rows:
        b = dict(r)
        b["tags"] = get_bookmark_tags(b["id"])
        bookmarks.append(b)
    conn.close()
    return bookmarks
