from dataclasses import dataclass, field

from wiki_server.db import get_db


@dataclass
class PageStat:
    path: str
    count: int


@dataclass
class MetricsReport:
    pages: list[PageStat] = field(default_factory=list)


def generate_report() -> MetricsReport:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT path, count FROM page_views ORDER BY count DESC, path ASC"
        ).fetchall()

    pages = [PageStat(path=row["path"], count=row["count"]) for row in rows]
    return MetricsReport(pages=pages)
