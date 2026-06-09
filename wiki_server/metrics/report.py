import glob
import json
import os
from dataclasses import dataclass, field

from wiki_server import config


@dataclass
class PageStat:
    path: str
    count: int


@dataclass
class MetricsReport:
    pages: list[PageStat] = field(default_factory=list)


def generate_report() -> MetricsReport:
    log_base = str(config.ACCESS_LOG)
    # Glob all segments: access.log, access.log.001, access.log.002, ...
    pattern = f"{log_base}*"
    log_files = sorted(glob.glob(pattern))

    counts: dict[str, int] = {}
    for log_file in log_files:
        try:
            with open(log_file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if entry.get("status") == 200:
                        path = entry.get("path", "")
                        if path:
                            counts[path] = counts.get(path, 0) + 1
        except FileNotFoundError:
            continue

    pages = [
        PageStat(path=path, count=count)
        for path, count in sorted(counts.items(), key=lambda x: -x[1])
    ]
    return MetricsReport(pages=pages)
