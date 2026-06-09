import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from wiki_server import config
from wiki_server.ingest.base import append_log_entry, slug_from_title, write_wiki_page

_LOGIN_TITLE_PATTERNS = re.compile(
    r"\b(log[\s-]?in|sign[\s-]?in|sign[\s-]?up|access denied|unauthorized)\b",
    re.IGNORECASE,
)
_LOGIN_URL_PATTERNS = re.compile(r"/(login|signin|sign-in|auth|sso)(/|$)", re.IGNORECASE)


def _detect_login_wall(page) -> bool:
    if page.locator('input[type="password"]').count() > 0:
        return True
    title = page.title()
    if _LOGIN_TITLE_PATTERNS.search(title):
        return True
    if _LOGIN_URL_PATTERNS.search(page.url):
        return True
    body_text = page.inner_text("body") if page.locator("body").count() > 0 else ""
    if len(body_text.strip()) < 200:
        return True
    return False


def ingest_webpage(url: str) -> None:
    from playwright.sync_api import sync_playwright

    hostname = urlparse(url).netloc.replace(".", "-")
    path_part = urlparse(url).path.strip("/").replace("/", "-")
    raw_stem = f"{hostname}-{path_part}".strip("-") or hostname

    config.RAW_DIR.mkdir(parents=True, exist_ok=True)
    (config.RAW_DIR / "web").mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000)
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as e:
            print(f"Navigation error for {url}: {e}")
            browser.close()
            sys.exit(1)

        if _detect_login_wall(page):
            print(f"Login wall detected at {url}. Provide a locally saved HTML file instead.")
            browser.close()
            sys.exit(1)

        title = page.title() or raw_stem
        html_content = page.content()
        browser.close()

    slug = slug_from_title(title)
    raw_path = config.RAW_DIR / "web" / f"{slug_from_title(raw_stem)}.html"
    raw_path.write_text(html_content, encoding="utf-8")

    source_rel = f"raw/web/{raw_path.name}"
    frontmatter = {
        "title": title,
        "source": source_rel,
        "source_type": "webpage",
        "ingested_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
        "tags": [],
    }
    body = f"\n# {title}\n\nSource: [{url}]({url})\n\nLocal copy: `{source_rel}`\n"
    page_path = write_wiki_page(slug, frontmatter, body)

    from wiki_server.search.index import index_page
    index_page(str(page_path))

    append_log_entry(title, "webpage", source_rel)
    print(f"Ingested: {page_path}")
