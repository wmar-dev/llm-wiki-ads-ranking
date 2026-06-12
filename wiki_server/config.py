import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

load_dotenv(BASE_DIR / ".env")

WIKI_DIR = BASE_DIR / "wiki"
RAW_DIR = BASE_DIR / "raw"
DB_PATH = Path(os.environ.get("WIKI_DB_PATH", BASE_DIR / "wiki.db"))
ACCESS_LOG = Path(os.environ.get("WIKI_ACCESS_LOG", BASE_DIR / "access.log"))
ACCESS_LOG_MAX_BYTES = int(os.environ.get("ACCESS_LOG_MAX_BYTES", 10 * 1024 * 1024))  # 10 MB

HOST = os.environ.get("WIKI_HOST", "127.0.0.1")
PORT = int(os.environ.get("WIKI_PORT", 5000))
