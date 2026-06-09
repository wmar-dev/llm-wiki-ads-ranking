# Research: Content Search, Metrics & Multi-Format Media Ingestion

**Branch**: `002-content-search-media` | **Date**: 2026-06-08

---

## R-001: Markdown Rendering in Flask

**Decision**: markdown-it-py 3.x with `commonmark` preset, `linkify` and `table` plugins enabled

**Rationale**: Best CommonMark spec compliance among Python markdown libraries. Actively
maintained. Supports extensions cleanly via plugin API. Produces predictable HTML that
integrates well with Jinja2 templates.

**Alternatives considered**:

- mistune 3.x: faster, but CommonMark compliance gaps (footnotes, some edge cases)
- python-markdown: mature but not CommonMark-spec-compliant; verbose extension API
- marko: spec-compliant but smaller ecosystem, fewer adopters

**Usage pattern**:

```python
from markdown_it import MarkdownIt
md = MarkdownIt("commonmark").enable("linkify").enable("table")
html = md.render(markdown_source)
```

---

## R-002: BM25 Scoring with SQLite3 Persistence

**Decision**: rank-bm25 library (BM25Okapi variant) + custom SQLite3 schema for persistence

**Rationale**: rank-bm25 is a well-tested pure-Python BM25 implementation. BM25Okapi matches
the spec requirement (FR-007: "term frequency × inverse document frequency, normalized by
page length"). SQLite3 is Python stdlib — no extra dependency for persistence. At < 500 pages
the index fits comfortably in a single SQLite file with sub-millisecond lookups.

**Alternatives considered**:

- Whoosh: adds a dependency; upstream abandoned (last release 2013)
- tantivy-py (Rust-backed): fast but binary dependency; overkill for < 500 pages
- Manual BM25: ~50 LOC but error-prone to implement correctly; rank-bm25 is battle-tested

**Incremental update**: On ingest of page P → DELETE FROM documents WHERE page_path = P
(cascades to term_frequencies) → INSERT new document + term rows → UPDATE corpus_stats.
Full rebuild only for `make index` (repair/migration scenario).

---

## R-003: Playwright Python Sync API

**Decision**: Playwright sync API (`playwright.sync_api`) with per-ingest browser instantiation

**Rationale**: Flask routes are synchronous. The Playwright async API requires an event loop
that conflicts with Flask's sync context. The sync API works directly in CLI ingest commands
and Flask handlers without extra scaffolding. Per-ingest instantiation avoids holding a browser
process open between ingest operations.

**Login-wall detection heuristics** (FR-018) — abort if any of:

1. Rendered page contains `<input type="password">` (login form present)
2. Page `<title>` matches patterns: "login", "sign in", "sign up", "access denied", "unauthorized" (case-insensitive)
3. Final URL after navigation diverges from original URL and contains `/login`, `/signin`, `/auth`, `/sso`
4. Rendered body text length < 200 characters (minimal content — likely a redirect gate)

**Heuristics are OR-combined**: any single match triggers the abort with a clear error message.

---

## R-004: yt-dlp Python API for Transcript Download

**Decision**: yt-dlp Python API with subtitle-only download; prefer manual subtitles, fall
back to auto-generated captions; convert VTT → plain text

**Rationale**: yt-dlp is the actively maintained successor to youtube-dl. Its Python API
(`yt_dlp.YoutubeDL`) allows subtitle-only download (no video file), keeping `raw/videos/`
small. VTT is the native format; a simple text pass strips timestamp lines.

**Transcript format stored**: plain text in `raw/videos/<slug>.txt` (primary citation),
original VTT in `raw/videos/<slug>.vtt` (preserved for re-processing).

**Failure mode**: If no subtitle/transcript track exists, yt-dlp raises `DownloadError`.
Catch and exit with a user-facing message naming the URL. No wiki page created.

**ydl options**:

```python
{
    "skip_download": True,
    "writesubtitles": True,
    "writeautomaticsub": True,
    "subtitleslangs": ["en"],
    "outtmpl": f"raw/videos/{slug}",
}
```

---

## R-005: PDF Sectioning with pdfplumber

**Decision**: pdfplumber for text extraction; automatic 50-page sections; single unattended
pass (FR-016)

**Rationale**: pdfplumber preserves text layout better than PyPDF2/pypdf for structured
documents (tables, columns). Page-level iteration makes fixed-boundary sectioning natural.
pdfplumber handles most PDFs without poppler as a system dependency.

**Section titles in wiki summary**: `## Section 1 (pages 1–50)`, `## Section 2 (pages 51–100)`,
etc. All sections are processed sequentially in one pass; no user prompts between sections.

**Alternatives considered**:

- PyPDF2 / pypdf: simpler API, less reliable text extraction for complex layouts
- pdfminer.six: more accurate for complex PDFs but heavier, lower-level API
- Tika (Apache): requires Java runtime — violates Constitution Principle V

---

## R-006: Access Log Rotation

**Decision**: Custom rotation check before each write; rotate when `access.log` exceeds 10 MB;
archive as `access.log.001`, `access.log.002`, ... (zero-padded 3 digits)

**Rationale**: Python's `RotatingFileHandler` uses `.1`, `.2` naming which does not sort
lexicographically by age. The spec requires "consistent, sortable naming." A lightweight
custom rotator (< 30 LOC) checks `os.path.getsize` before each write and renames on threshold.
Zero-padded 3 digits gives up to 999 segments before naming overflow.

**Metrics reader**: glob `access.log*`, sort by name, parse all files. Deleted-page entries
remain in archived segments (FR-011, SC-007).

---

## R-007: Docker + uv Multi-Stage Build

**Decision**: Two-stage Dockerfile — builder (uv sync) + runtime (system deps + app code)

**Rationale**: Separating build and runtime reduces final image size. System dependencies
(graphviz, chromium for Playwright) are installed only in the runtime stage.

**System packages (runtime stage)**:

```dockerfile
RUN apt-get update && apt-get install -y graphviz && rm -rf /var/lib/apt/lists/*
RUN uv run playwright install chromium --with-deps
```

**Volume mounts** (docker-compose.yml):

```yaml
volumes:
  - ./wiki:/app/wiki
  - ./raw:/app/raw
  - ./search.db:/app/search.db
```

`access.log` and rotated segments also mounted or persisted inside a named volume.

---

## R-008: Makefile Design

**Decision**: PHONY targets for all operations; `uv run` for local dev; `docker-compose` for
containerized deployment

**Key targets**:

```makefile
.PHONY: install serve test lint docker-build docker-up docker-down ingest index

install:
	uv sync && uv run playwright install chromium

serve:
	uv run flask --app wiki_server.app run --host 127.0.0.1 --port 5000

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check wiki_server/ tests/

docker-build:
	docker build -t llm-wiki .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

ingest:
	uv run python -m wiki_server.ingest $(TYPE) $(TARGET)

index:
	uv run python -m wiki_server.search rebuild
```

`make ingest TYPE=webpage TARGET=https://example.com` passes TYPE/TARGET as make variables.
