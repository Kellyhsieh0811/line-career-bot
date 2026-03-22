"""SQLite storage for user messages and intent history."""
import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "line_bot.db")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with _conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS messages (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     TEXT    NOT NULL,
                display_name TEXT,
                message     TEXT    NOT NULL,
                intent      TEXT    NOT NULL,
                score       INTEGER NOT NULL,
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS users (
                user_id      TEXT PRIMARY KEY,
                display_name TEXT,
                first_seen   DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_seen    DATETIME DEFAULT CURRENT_TIMESTAMP,
                message_count INTEGER DEFAULT 0
            );
        """)


@contextmanager
def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def save_message(user_id: str, display_name: str, message: str, intent: str, score: int):
    with _conn() as conn:
        conn.execute(
            "INSERT INTO messages (user_id, display_name, message, intent, score) VALUES (?,?,?,?,?)",
            (user_id, display_name, message, intent, score),
        )
        conn.execute("""
            INSERT INTO users (user_id, display_name, last_seen, message_count)
            VALUES (?, ?, CURRENT_TIMESTAMP, 1)
            ON CONFLICT(user_id) DO UPDATE SET
                display_name   = excluded.display_name,
                last_seen      = CURRENT_TIMESTAMP,
                message_count  = message_count + 1
        """, (user_id, display_name))


def get_recent_messages(limit: int = 50) -> list[dict]:
    with _conn() as conn:
        rows = conn.execute(
            "SELECT * FROM messages ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_high_intent_users() -> list[dict]:
    with _conn() as conn:
        rows = conn.execute("""
            SELECT user_id, display_name, MAX(created_at) as last_seen, COUNT(*) as msg_count
            FROM messages
            WHERE intent = 'HIGH'
            GROUP BY user_id
            ORDER BY last_seen DESC
        """).fetchall()
    return [dict(r) for r in rows]
