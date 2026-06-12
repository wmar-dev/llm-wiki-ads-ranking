import glob
import json
import sqlite3

from wiki_server import config


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db() as conn:
        had_page_views = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='page_views'"
        ).fetchone() is not None

        conn.executescript("""
            CREATE VIRTUAL TABLE IF NOT EXISTS pages
                USING fts5(title, body, path UNINDEXED);

            CREATE TABLE IF NOT EXISTS page_meta (
                path        TEXT PRIMARY KEY,
                content_hash TEXT NOT NULL,
                indexed_at  INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS page_views (
                path  TEXT PRIMARY KEY,
                count INTEGER NOT NULL DEFAULT 0
            );
        """)

        if not had_page_views:
            _backfill_page_views(conn)


def _backfill_page_views(conn: sqlite3.Connection) -> None:
    """One-time import of historical visit counts from existing access.log* segments."""
    counts: dict[str, int] = {}
    for log_file in glob.glob(f"{config.ACCESS_LOG}*"):
        with open(log_file, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("status") == 200:
                    path = entry.get("path", "")
                    if path:
                        counts[path] = counts.get(path, 0) + 1

    conn.executemany(
        "INSERT INTO page_views(path, count) VALUES (?, ?)",
        counts.items(),
    )


init_db()
