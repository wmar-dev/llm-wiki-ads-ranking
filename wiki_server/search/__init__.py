import sqlite3
from wiki_server import config


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(config.SEARCH_DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.executescript("""
            CREATE VIRTUAL TABLE IF NOT EXISTS pages
                USING fts5(title, body, path UNINDEXED);

            CREATE TABLE IF NOT EXISTS page_meta (
                path        TEXT PRIMARY KEY,
                content_hash TEXT NOT NULL,
                indexed_at  INTEGER NOT NULL
            );
        """)


init_db()
