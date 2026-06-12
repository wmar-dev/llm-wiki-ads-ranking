from dataclasses import dataclass
from pathlib import Path
from wiki_server import config
from wiki_server.db import get_db


@dataclass
class SearchResult:
    path: str
    url: str
    title: str
    excerpt: str
    score: float


def suggest(prefix: str, limit: int = 8) -> list[dict]:
    """Return page title suggestions matching the given prefix."""
    if len(prefix.strip()) < 2:
        return []
    terms = prefix.strip().split()
    fts_query = " AND ".join(f"{w}*" for w in terms)

    with get_db() as conn:
        rows = conn.execute(
            "SELECT title, path FROM pages WHERE pages MATCH ? ORDER BY bm25(pages) LIMIT ?",
            (fts_query, limit),
        ).fetchall()

    results = []
    for row in rows:
        page_path = row["path"]
        url = "/wiki/" + str(Path(page_path).relative_to(config.WIKI_DIR).with_suffix(""))
        results.append({"title": row["title"] or Path(page_path).stem, "url": url})
    return results


def search(query: str, limit: int = 10) -> list[SearchResult]:
    if not query.strip():
        return []

    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT
                path,
                title,
                snippet(pages, 1, '<mark>', '</mark>', '…', 20) AS excerpt,
                bm25(pages) AS score
            FROM pages
            WHERE pages MATCH ?
            ORDER BY bm25(pages)
            LIMIT ?
            """,
            (query, limit),
        ).fetchall()

    results = []
    for row in rows:
        page_path = row["path"]
        # Convert filesystem path to URL: /abs/path/wiki/s/s.md -> /wiki/s/s
        url = "/wiki/" + str(Path(page_path).relative_to(config.WIKI_DIR).with_suffix(""))
        results.append(
            SearchResult(
                path=page_path,
                url=url,
                title=row["title"] or page_path,
                excerpt=row["excerpt"] or "",
                score=row["score"],
            )
        )
    return results
