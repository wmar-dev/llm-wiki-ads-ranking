import sys
import time
from pathlib import Path

from wiki_server import config
from wiki_server.ingest.base import append_log_entry, slug_from_title, write_wiki_page

SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def ingest_image(file_path: str) -> None:
    from PIL import Image

    src = Path(file_path)
    if not src.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)
    if src.suffix.lower() not in SUPPORTED_FORMATS:
        print(f"Unsupported format: {src.suffix}. Supported: {', '.join(SUPPORTED_FORMATS)}")
        sys.exit(1)

    try:
        with Image.open(src) as img:
            img.verify()
    except Exception as e:
        print(f"Invalid image file: {e}")
        sys.exit(1)

    dest_dir = config.RAW_DIR / "images"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    if not dest.exists():
        import shutil
        shutil.copy2(src, dest)

    source_rel = f"raw/images/{src.name}"
    title = src.stem.replace("-", " ").replace("_", " ").title()
    slug = slug_from_title(title)

    # Multimodal description placeholder — the LLM agent fills this in
    description = (
        f"_Image description: {src.name} — "
        "describe the visual content of this image here._"
    )

    body = (
        f"\n# {title}\n\n"
        f"![{title}](/raw/images/{src.name})\n\n"
        f"Source: `{source_rel}`\n\n"
        f"## Description\n\n{description}\n"
    )
    frontmatter = {
        "title": title,
        "source": source_rel,
        "source_type": "image",
        "ingested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tags": [],
    }
    page_path = write_wiki_page(slug, frontmatter, body)

    from wiki_server.search.index import index_page
    index_page(str(page_path))

    append_log_entry(title, "image", source_rel)
    print(f"Ingested image: {page_path}")
