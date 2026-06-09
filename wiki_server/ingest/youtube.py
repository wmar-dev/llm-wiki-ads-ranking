import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from wiki_server import config
from wiki_server.ingest.base import append_log_entry, slug_from_title, write_wiki_page


def _video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname in ("youtu.be",):
        return parsed.path.lstrip("/")
    qs = parse_qs(parsed.query)
    return qs.get("v", ["unknown"])[0]


def _strip_vtt(vtt_text: str) -> str:
    lines = []
    seen = set()
    for line in vtt_text.splitlines():
        # Skip WebVTT header, timestamp lines, and blank lines
        if line.startswith("WEBVTT") or "-->" in line or not line.strip():
            continue
        # Strip HTML tags
        clean = re.sub(r"<[^>]+>", "", line).strip()
        if clean and clean not in seen:
            seen.add(clean)
            lines.append(clean)
    return "\n".join(lines)


def ingest_youtube(url: str) -> None:
    import yt_dlp

    vid_id = _video_id(url)
    dest_dir = config.RAW_DIR / "videos"
    dest_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "outtmpl": str(dest_dir / vid_id),
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", vid_id)
            chapters = info.get("chapters") or []
    except yt_dlp.utils.DownloadError as e:
        print(f"No transcript available for {url}. The video may lack subtitles.")
        sys.exit(1)

    # Find the downloaded VTT file
    vtt_files = list(dest_dir.glob(f"{vid_id}*.vtt"))
    if not vtt_files:
        print(f"No transcript available for {url}. The video may lack subtitles.")
        sys.exit(1)

    vtt_path = vtt_files[0]
    vtt_text = vtt_path.read_text(encoding="utf-8")
    plain_text = _strip_vtt(vtt_text)

    slug = slug_from_title(title)
    txt_path = dest_dir / f"{slug}.txt"
    txt_path.write_text(plain_text, encoding="utf-8")
    # Rename VTT to consistent name
    vtt_dest = dest_dir / f"{slug}.vtt"
    if not vtt_dest.exists():
        vtt_path.rename(vtt_dest)

    source_rel = f"raw/videos/{slug}.txt"

    body = f"\n# {title}\n\nSource: [{url}]({url})\n\nTranscript: `{source_rel}`\n\n"

    if chapters:
        body += "## Chapters\n\n"
        for ch in chapters:
            start_min = int(ch.get("start_time", 0)) // 60
            start_sec = int(ch.get("start_time", 0)) % 60
            body += f"### {ch.get('title', 'Chapter')} ({start_min}:{start_sec:02d})\n\n"
    else:
        body += "## Transcript\n\n"
        body += plain_text[:3000]
        if len(plain_text) > 3000:
            body += f"\n\n_[Transcript truncated — full text in `{source_rel}`]_\n"

    frontmatter = {
        "title": title,
        "source": source_rel,
        "source_type": "youtube",
        "ingested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tags": [],
    }
    page_path = write_wiki_page(slug, frontmatter, body)

    from wiki_server.search.index import index_page
    index_page(str(page_path))

    append_log_entry(title, "youtube", source_rel)
    print(f"Ingested YouTube: {page_path}")
