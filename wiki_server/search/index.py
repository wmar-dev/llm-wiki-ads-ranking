import hashlib
import re
import time
from pathlib import Path

from wiki_server import config
from wiki_server.search import get_db, init_db


def _extract_title(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def _strip_frontmatter(text: str) -> tuple[str, str]:
    """Return (title_from_frontmatter, body_without_frontmatter)."""
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    fm = text[3:end]
    body = text[end + 4:].lstrip("\n")
    title = ""
    for line in fm.splitlines():
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip('"')
            break
    return title, body


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _strip_markdown(text: str) -> str:
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_`~]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def index_page(page_path: str) -> None:
    path = Path(page_path)
    if not path.exists():
        print(f"Page not found: {page_path}")
        return

    raw = path.read_text(encoding="utf-8")
    chash = _content_hash(raw)

    with get_db() as conn:
        row = conn.execute(
            "SELECT content_hash FROM page_meta WHERE path = ?", (page_path,)
        ).fetchone()
        if row and row["content_hash"] == chash:
            return  # unchanged

        fm_title, body = _strip_frontmatter(raw)
        heading_title = _extract_title(body)
        title = fm_title or heading_title or path.stem
        body_text = _strip_markdown(body)

        conn.execute("DELETE FROM pages WHERE path = ?", (page_path,))
        conn.execute(
            "INSERT INTO pages(title, body, path) VALUES (?, ?, ?)",
            (title, body_text, page_path),
        )
        conn.execute(
            """INSERT INTO page_meta(path, content_hash, indexed_at)
               VALUES (?, ?, ?)
               ON CONFLICT(path) DO UPDATE SET
                   content_hash = excluded.content_hash,
                   indexed_at   = excluded.indexed_at""",
            (page_path, chash, int(time.time())),
        )


def rebuild_index() -> None:
    init_db()
    with get_db() as conn:
        conn.execute("DELETE FROM pages")
        conn.execute("DELETE FROM page_meta")

    wiki_dir = config.WIKI_DIR
    if not wiki_dir.exists():
        print(f"wiki/ directory not found: {wiki_dir}")
        return

    pages = sorted(wiki_dir.rglob("*.md"))
    for page in pages:
        index_page(str(page))
    print(f"Rebuilt index: {len(pages)} pages indexed.")
