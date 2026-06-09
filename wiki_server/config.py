import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

WIKI_DIR = BASE_DIR / "wiki"
RAW_DIR = BASE_DIR / "raw"
SEARCH_DB = BASE_DIR / "search.db"
ACCESS_LOG = BASE_DIR / "access.log"
ACCESS_LOG_MAX_BYTES = int(os.environ.get("ACCESS_LOG_MAX_BYTES", 10 * 1024 * 1024))  # 10 MB

HOST = os.environ.get("WIKI_HOST", "127.0.0.1")
PORT = int(os.environ.get("WIKI_PORT", 5000))
