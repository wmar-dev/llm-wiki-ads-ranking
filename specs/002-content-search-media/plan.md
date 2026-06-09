# Implementation Plan: Content Search, Metrics & Multi-Format Media Ingestion

**Branch**: `002-content-search-media` | **Date**: 2026-06-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-content-search-media/spec.md`

## Summary

Build a local Flask web server (Python 3.12, uv, Makefile, Docker) that renders the LLM wiki
as browsable HTML, supports multi-format source ingestion (webpages via Playwright, PDFs via
pdfplumber, images via multimodal LLM, podcasts via transcript, YouTube via yt-dlp), provides
BM25 full-text search backed by a persistent SQLite3 index, records HTTP page visit metrics
with size-based log rotation, and renders Graphviz dot diagrams as inline SVGs.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**:

- Flask 3.x — web server, Jinja2 templating, static file serving
- markdown-it-py 3.x — CommonMark-compliant markdown → HTML (best spec compliance)
- sqlite3 — stdlib; persistent FTS5 virtual table with native `bm25()` ranking (`search.db`)
- Playwright sync API — JS-rendered webpage ingest + login-wall detection
- yt-dlp — YouTube transcript auto-download (VTT → plain text)
- pdfplumber — PDF text extraction with page-level metadata
- graphviz Python bindings — dot → SVG rendering (requires graphviz system package)
- Pillow — image format validation before multimodal description pass

**Storage**:

- `search.db` — SQLite3 BM25 term index; persists across server restarts
- Flat files — `wiki/` markdown pages, `raw/` source copies, `access.log` + rotated segments

**Testing**: pytest 8.x + pytest-flask

**Target Platform**: macOS (dev via uv), Linux (Docker)

**Project Type**: Local web service + CLI ingest tool

**Performance Goals**:

- SC-001: Server start and first page served in < 5 seconds
- SC-003: BM25 search over 50-page wiki returns results in < 3 seconds

**Constraints**:

- localhost only; no HTTPS, no auth, single-user (v1)
- No proprietary cloud services; Docker is additive (not mandatory per Constitution V)
- System dependencies: graphviz, chromium (Playwright) must be installed

**Scale/Scope**: 50–500 wiki pages; single concurrent user; access.log rotates at 10 MB

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Status | Notes |
| --------- | ------ | ----- |
| I. Content-System Isolation & Source Preservation | ✅ PASS | `wiki-server/` is System layer (version-controlled). `raw/` never touched by Flask or ingest writer. `wiki/` owned by LLM. No layer writes upward. |
| II. Token Economy | ✅ PASS | BM25 search, HTTP serving, log rotation, and metrics consume zero LLM tokens. Ingest follows one-pass rule (FR-004). Large sources auto-section in one unattended pass (FR-016). |
| III. Grounded Analysis & Provenance | ✅ PASS | Every ingest writes a frontmatter `source:` citation to local `raw/` path (FR-005). `log.md` gets timestamped entry per ingest with source type (FR-006). Access log archives historical visit data (FR-011). |
| IV. Quality Gates & Testing | ✅ PASS | Ingest validates page + citation before success. 404 handling (FR-003). Login-wall detection aborts without writing (FR-018). Dot syntax error aborts without partial SVG (FR-012 acceptance scenario 3). pytest covers all workflows. |
| V. Deployability & Documentation | ✅ PASS | Requires only git, markdown, `raw/`, LLM agent, Python 3.12. Docker is additive per constitution. Single `make serve` start command (SC-001). All workflows documented in quickstart.md. |

**Post-design re-check**: All five principles remain satisfied — no external service dependencies
introduced beyond user-specified tools (Flask, SQLite3, Playwright, yt-dlp, Graphviz).

## Project Structure

### Documentation (this feature)

```text
specs/002-content-search-media/
├── plan.md              # This file
├── research.md          # Phase 0: technology decisions + rationale
├── data-model.md        # Phase 1: SQLite schema, file layout, log format
├── quickstart.md        # Phase 1: runnable validation guide
├── contracts/
│   ├── api.md           # Flask HTTP route contracts
│   └── cli.md           # CLI ingest/index command contracts
└── tasks.md             # Phase 2 output (/speckit-tasks — not created here)
```

### Source Code (repository root)

```text
wiki-server/
├── app.py               # Flask application factory + route registration
├── __main__.py          # Entry point: python -m wiki_server
├── config.py            # Path constants (wiki/, raw/, search.db, access.log)
├── search/
│   ├── __init__.py
│   ├── index.py         # BM25 index builder: tokenize pages → SQLite
│   └── query.py         # BM25 query executor: term lookup → ranked results + excerpts
├── ingest/
│   ├── __init__.py
│   ├── base.py          # Shared: save raw/, write wiki page, update index, append log.md
│   ├── webpage.py       # Playwright fetch + login-wall detection + local HTML save
│   ├── pdf.py           # pdfplumber extraction + 50-page auto-sectioning
│   ├── image.py         # Pillow validation + multimodal description prompt
│   ├── podcast.py       # Transcript-present check; blocks on audio-only input
│   ├── youtube.py       # yt-dlp VTT download → plain text + chapter extraction
│   └── dot.py           # graphviz render → SVG save to wiki/assets/ + dot preservation
├── metrics/
│   ├── __init__.py
│   └── report.py        # Parse all access.log* segments → per-page counts + ranking
├── templates/
│   ├── base.html        # Shared nav, search bar, CSS link
│   ├── page.html        # Rendered wiki page with inline SVG support
│   ├── search.html      # Search form + BM25 ranked results with excerpts
│   ├── metrics.html     # Visit counts table, most-visited ranking, zero-visit flags
│   └── 404.html         # 404 with link back to /
└── static/
    └── style.css        # Minimal readable CSS (no external framework)

tests/
├── integration/
│   ├── test_routes.py        # GET /, /wiki/page, /search, /metrics, /assets, 404
│   ├── test_search.py        # Index build + BM25 query accuracy + incremental update
│   └── test_metrics.py       # Log parse + per-page count accuracy + rotation
└── unit/
    ├── test_bm25.py               # BM25 scoring correctness vs known values
    ├── test_ingest_webpage.py     # Login-wall detection heuristics
    ├── test_ingest_pdf.py         # 50-page section boundary logic
    ├── test_ingest_podcast.py     # Audio-only blocking (exit code 2)
    ├── test_ingest_youtube.py     # yt-dlp transcript extraction
    └── test_log_rotation.py       # 10 MB threshold + archive naming (access.log.001...)

Makefile
Dockerfile
docker-compose.yml
pyproject.toml           # uv project manifest (Python 3.12, all deps)
.python-version          # 3.12
```

**Structure Decision**: Single project layout. No frontend build step — Jinja2 templates +
minimal static CSS. `search.db` and `access.log` live at project root (configurable via
`config.py`). `wiki/` and `raw/` remain at project root as defined by feature 001.

## Complexity Tracking

No constitution violations. No complexity justification required.
