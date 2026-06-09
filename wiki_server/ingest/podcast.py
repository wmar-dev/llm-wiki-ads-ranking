import sys
import time
from pathlib import Path

from wiki_server import config
from wiki_server.ingest.base import append_log_entry, slug_from_title, write_wiki_page

AUDIO_EXTENSIONS = {".mp3", ".m4a", ".wav", ".aac", ".ogg", ".flac"}
TRANSCRIPT_EXTENSIONS = {".txt", ".srt"}


def ingest_podcast(file_path: str) -> None:
    src = Path(file_path)
    if not src.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    if src.suffix.lower() in AUDIO_EXTENSIONS:
        # Check for a companion transcript
        companion = src.with_suffix(".txt")
        if not companion.exists():
            companion = src.with_suffix(".srt")
        if not companion.exists():
            print(
                "Transcript required. "
                "Please provide a .txt or .srt file alongside the audio."
            )
            sys.exit(2)
        transcript_src = companion
    elif src.suffix.lower() in TRANSCRIPT_EXTENSIONS:
        transcript_src = src
    else:
        print(f"Unsupported file type: {src.suffix}")
        sys.exit(1)

    dest_dir = config.RAW_DIR / "podcasts"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / transcript_src.name
    if not dest.exists():
        import shutil
        shutil.copy2(transcript_src, dest)
    if src.suffix.lower() in AUDIO_EXTENSIONS:
        audio_dest = dest_dir / src.name
        if not audio_dest.exists():
            import shutil
            shutil.copy2(src, audio_dest)

    source_rel = f"raw/podcasts/{transcript_src.name}"
    transcript_text = transcript_src.read_text(encoding="utf-8")
    title = src.stem.replace("-", " ").replace("_", " ").title()
    slug = slug_from_title(title)

    body = (
        f"\n# {title}\n\n"
        f"Source: `{source_rel}`\n\n"
        f"## Transcript\n\n"
        f"{transcript_text[:3000]}\n"
    )
    if len(transcript_text) > 3000:
        body += f"\n_[Transcript truncated — full text in `{source_rel}`]_\n"

    frontmatter = {
        "title": title,
        "source": source_rel,
        "source_type": "podcast",
        "ingested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tags": [],
    }
    page_path = write_wiki_page(slug, frontmatter, body)

    from wiki_server.search.index import index_page
    index_page(str(page_path))

    append_log_entry(title, "podcast", source_rel)
    print(f"Ingested podcast: {page_path}")
