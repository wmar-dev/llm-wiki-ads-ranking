import sys
import time
from pathlib import Path

from wiki_server import config
from wiki_server.ingest.base import append_log_entry, slug_from_title, write_wiki_page

SECTION_SIZE = 50


def ingest_pdf(file_path: str) -> None:
    import pdfplumber

    src = Path(file_path)
    if not src.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    try:
        pdf = pdfplumber.open(src)
    except Exception as e:
        print(f"Cannot open PDF: {e}")
        sys.exit(1)

    title = src.stem.replace("-", " ").replace("_", " ").title()
    slug = slug_from_title(title)

    # Determine destination subdirectory
    subdir = "papers" if "paper" in str(src).lower() or "arxiv" in str(src).lower() else "docs"
    dest_dir = config.RAW_DIR / subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    if not dest.exists():
        import shutil
        shutil.copy2(src, dest)

    source_rel = f"raw/{subdir}/{src.name}"

    pages = list(pdf.pages)
    pdf.close()
    total = len(pages)

    # Build section bodies
    sections = []
    for start in range(0, total, SECTION_SIZE):
        end = min(start + SECTION_SIZE, total)
        section_num = start // SECTION_SIZE + 1
        pdf2 = pdfplumber.open(src)
        text = "\n".join(
            (p.extract_text() or "").strip()
            for p in pdf2.pages[start:end]
        )
        pdf2.close()
        sections.append((section_num, start + 1, end, text))

    body = f"\n# {title}\n\nSource: `{source_rel}`\n\nTotal pages: {total}\n\n"
    for num, pg_start, pg_end, text in sections:
        body += f"## Section {num} (pages {pg_start}–{pg_end})\n\n"
        if text.strip():
            preview = text[:2000].strip()
            body += f"{preview}\n\n"
        else:
            body += "_No extractable text in this section._\n\n"

    frontmatter = {
        "title": title,
        "source": source_rel,
        "source_type": "pdf",
        "ingested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tags": [],
    }
    page_path = write_wiki_page(slug, frontmatter, body)

    from wiki_server.search.index import index_page
    index_page(str(page_path))

    append_log_entry(title, "pdf", source_rel)
    print(f"Ingested {total}-page PDF: {page_path}")
