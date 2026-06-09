---

description: "Task list for Content Search, Metrics & Multi-Format Media Ingestion"
---

# Tasks: Content Search, Metrics & Multi-Format Media Ingestion

**Input**: Design documents from `specs/002-content-search-media/`

**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/api.md ✅, contracts/cli.md ✅, quickstart.md ✅

**Search implementation**: SQLite FTS5 native `bm25()` — no `rank-bm25` dependency (plan.md updated 2026-06-08).

**Tests**: Not included (not requested in spec.md).

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no shared state dependencies)
- **[Story]**: Which user story this task belongs to (US1–US5)
- Every task includes an exact file path

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization — pyproject, file structure, Docker, Makefile.

- [X] T001 Create `pyproject.toml` with uv project config: Python 3.12, dependencies (Flask 3.x, markdown-it-py 3.x, Playwright, pdfplumber, Pillow, yt-dlp, graphviz, pytest 8.x, pytest-flask, ruff)
- [X] T002 Create `.python-version` containing `3.12`
- [X] T003 Create `wiki-server/` directory tree with empty `__init__.py` files: `wiki-server/__init__.py`, `wiki-server/search/__init__.py`, `wiki-server/ingest/__init__.py`, `wiki-server/metrics/__init__.py`
- [X] T004 [P] Create `Makefile` with all PHONY targets: `install`, `serve`, `test`, `lint`, `docker-build`, `docker-up`, `docker-down`, `ingest`, `index` (per R-008 in research.md)
- [X] T005 [P] Create `Dockerfile` — two-stage build: builder stage (`uv sync`) + runtime stage (install graphviz system package, run `uv run playwright install chromium --with-deps`, copy app code)
- [X] T006 [P] Create `docker-compose.yml` with volume mounts for `wiki/`, `raw/`, `search.db`, and `access.log` segments (per R-007 in research.md)

**Checkpoint**: Project skeleton ready — `make install` should succeed.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core configuration and shared infrastructure that ALL user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T007 Implement `wiki-server/config.py` — path constants: `WIKI_DIR`, `RAW_DIR`, `SEARCH_DB`, `ACCESS_LOG`, `ACCESS_LOG_MAX_BYTES` (10 MB default), `HOST`, `PORT` (5000)
- [X] T008 [P] Create `wiki-server/app.py` — Flask application factory `create_app()` that registers all blueprints/routes and wires up the access-logging `after_request` hook
- [X] T009 [P] Create `wiki-server/__main__.py` — entry point enabling `python -m wiki_server` to call `create_app().run()`
- [X] T010 Implement SQLite FTS5 schema initialization in `wiki-server/search/__init__.py` — create FTS5 virtual table `CREATE VIRTUAL TABLE IF NOT EXISTS pages USING fts5(title, body, path UNINDEXED)` and metadata table `page_meta(path TEXT PRIMARY KEY, content_hash TEXT NOT NULL, indexed_at INTEGER NOT NULL)`; call on first import
- [X] T011 Implement `wiki-server/ingest/base.py` — shared helpers: `slug_from_title(title)`, `write_wiki_page(slug, frontmatter, body)` (writes YAML frontmatter + markdown body to `wiki/<slug>.md`), `append_log_entry(title, source_type, source_path)` (appends timestamped entry to `log.md`)
- [X] T012 [P] Create `wiki-server/ingest/__init__.py` — CLI dispatcher: parse `sys.argv[1]` as subcommand (`webpage`, `pdf`, `image`, `podcast`, `youtube`, `dot`), route to format handler; print usage on unknown subcommand

**Checkpoint**: Foundation ready — `python -m wiki_server.ingest` prints usage; `python -m wiki_server` starts Flask.

---

## Phase 3: User Story 1 — Serve the Wiki via Web Browser (Priority: P1) 🎯 MVP

**Goal**: Start Flask, open browser, browse wiki pages, follow cross-links, view inline SVGs — all without touching the filesystem directly.

**Independent Test**: `make serve` → open `http://localhost:5000` → index loads → click a cross-link → page loads → SVG renders inline. Navigate to `/wiki/nonexistent` → 404 page with link back to `/`.

- [X] T013 [US1] Create `wiki-server/templates/base.html` — shared layout: `<nav>` with index link, search bar (`<form action="/search">`), link to `static/style.css`, and a `{% block content %}` slot
- [X] T014 [P] [US1] Create `wiki-server/static/style.css` — minimal readable CSS: body max-width, heading sizes, nav bar, inline SVG `max-width: 100%`, no external framework
- [X] T015 [US1] Implement `GET /` route in `wiki-server/app.py` — render `wiki/index.md` as HTML using markdown-it-py (`MarkdownIt("commonmark").enable("linkify").enable("table")`); if `wiki/` empty or `index.md` absent, render "No pages yet" message; log to `access.log`
- [X] T016 [US1] Implement `GET /wiki/<path:page>` route in `wiki-server/app.py` — resolve `wiki/<page>.md`, render with markdown-it-py, return 200 with `page.html`; if file absent return 404 with `404.html`; log both outcomes to `access.log`
- [X] T017 [P] [US1] Create `wiki-server/templates/page.html` — extends `base.html`; renders `{{ content | safe }}` (HTML from markdown-it-py); inline SVG support via `<img>` or direct `<svg>` tag passthrough
- [X] T018 [P] [US1] Create `wiki-server/templates/404.html` — extends `base.html`; "Page not found" message with link back to `/`
- [X] T019 [US1] Implement `GET /assets/<filename>` route in `wiki-server/app.py` — serve files from `wiki/assets/` with `image/svg+xml` MIME type; 404 if absent; not logged
- [X] T020 [US1] Implement `GET /raw/images/<filename>` route in `wiki-server/app.py` — serve files from `raw/images/` with MIME type detected from extension (JPEG/PNG/GIF/WebP); 404 if absent; not logged
- [X] T021 [US1] Wire markdown rendering helper `render_page(path)` in `wiki-server/app.py` — reads file, calls `MarkdownIt("commonmark").enable("linkify").enable("table").render()`, returns HTML string; used by GET / and GET /wiki/<page>

**Checkpoint**: `make serve` → all five US1 acceptance scenarios pass per spec.md. V-001 and V-002 from quickstart.md pass.

---

## Phase 4: User Story 2 — Ingest Multi-Format Sources (Priority: P2)

**Goal**: `make ingest TYPE=<format> TARGET=<source>` ingests any of five formats — raw copy saved, wiki page created with frontmatter citation, page immediately accessible via web server.

**Independent Test**: Ingest one source of each type; verify `raw/<format>/` file exists, `wiki/<slug>.md` has correct `source:` frontmatter, page loads in browser at `http://localhost:5000/wiki/<slug>`, `log.md` has new entry with `source_type`.

- [X] T022 [US2] Implement `wiki-server/ingest/webpage.py` — Playwright sync API: launch chromium per-ingest, navigate to URL, detect login-wall (password input, title patterns, URL redirect to `/login|/signin|/auth|/sso`, body < 200 chars), abort with exit code 1 if detected; on success save HTML to `raw/web/<slug>.html`, call `base.write_wiki_page()` and `base.append_log_entry(source_type="webpage")`
- [X] T023 [P] [US2] Implement `wiki-server/ingest/pdf.py` — pdfplumber: open PDF, iterate pages in 50-page sections (`## Section N (pages X–Y)`), extract text per section, write single wiki summary page with all section headings; store PDF in `raw/papers/<slug>.pdf` (default) or `raw/docs/<slug>.pdf`; call `base.append_log_entry(source_type="pdf")`
- [X] T024 [P] [US2] Implement `wiki-server/ingest/image.py` — Pillow: open and validate image format (JPEG/PNG/GIF/WebP); pass to multimodal LLM for description; write wiki page with description and inline `![image](/raw/images/<slug>.<ext>)` reference; save image to `raw/images/<slug>.<ext>`; call `base.append_log_entry(source_type="image")`
- [X] T025 [P] [US2] Implement `wiki-server/ingest/podcast.py` — detect if `file_path` is audio-only (`.mp3`, `.m4a`, `.wav`) with no accompanying `.txt`/`.srt`; if audio-only: print `Transcript required. Please provide a .txt or .srt file alongside the audio.` and exit with code 2; if transcript: save to `raw/podcasts/<slug>.txt`, write wiki page summarizing key topics; call `base.append_log_entry(source_type="podcast")`
- [X] T026 [P] [US2] Implement `wiki-server/ingest/youtube.py` — yt-dlp Python API with `skip_download=True, writesubtitles=True, writeautomaticsub=True, subtitleslangs=["en"]`; on `DownloadError`: print `No transcript available for <url>.` and exit 1; on success: strip VTT timestamps → plain text, save both `raw/videos/<slug>.vtt` and `raw/videos/<slug>.txt`; write wiki page with chapter-level section headings where chapters are available; call `base.append_log_entry(source_type="youtube")`
- [X] T027 [US2] Wire all ingest handlers into `wiki-server/ingest/__init__.py` CLI dispatcher — route `webpage`, `pdf`, `image`, `podcast`, `youtube` subcommands to their respective modules; each handler calls `wiki-server/search/index.py` incremental update after writing wiki page

**Checkpoint**: V-003 through V-007 from quickstart.md pass. Each ingest format independently testable.

---

## Phase 5: User Story 3 — Search Wiki Content via Browser (Priority: P3)

**Goal**: Type a query in the browser search bar, get BM25-ranked results with excerpts, click a result to navigate to the page.

**Independent Test**: With 20+ pages indexed, search a term known to appear in 3 pages → 3 results ranked by relevance with excerpts → click result → correct page loads. Search unknown term → "No results found."

- [X] T028 [US3] Implement `wiki-server/search/index.py` — FTS5 index builder: `index_page(page_path)` reads `wiki/<page>.md`, extracts frontmatter title, computes SHA-256 `content_hash` (skip re-index if unchanged via `page_meta`), executes `DELETE FROM pages WHERE path=?` then `INSERT INTO pages(title, body, path) VALUES(?,?,?)`, upserts `page_meta`; `rebuild_index()` drops and recreates both tables then indexes all `wiki/*.md` files; expose as `python -m wiki_server.search rebuild`
- [X] T029 [US3] Implement `wiki-server/search/query.py` — `search(query, limit=10)`: tokenize query, execute `SELECT path, title, snippet(pages,1,'<mark>','</mark>','…',20), bm25(pages) FROM pages WHERE pages MATCH ? ORDER BY bm25(pages) LIMIT ?`, return list of `SearchResult(path, title, excerpt, score)`
- [X] T030 [US3] Implement `GET /search` route in `wiki-server/app.py` — read `?q=` param, call `search_query.search(q)`, pass results to `search.html`; if empty query render blank search form; route is not logged in `access.log`
- [X] T031 [P] [US3] Create `wiki-server/templates/search.html` — extends `base.html`; search form with pre-populated `?q=` value; ranked result list (title as link to `/wiki/<path>`, excerpt); "No results found" branch; result excerpts use `{{ result.excerpt | safe }}` for `<mark>` highlight tags
- [X] T032 [US3] Wire `search update <page_path>` command in `wiki-server/search/__init__.py` — parse `sys.argv[2]` as page path, call `index.index_page(page_path)`; `rebuild` subcommand calls `index.rebuild_index()`; ensure `T027` ingest handlers call `index_page()` after writing each wiki page

**Checkpoint**: V-009 from quickstart.md passes. BM25 search returns correct ranking. Multi-word query ranks pages with both terms above single-term pages.

---

## Phase 6: User Story 4 — Track Page Visit Metrics (Priority: P4)

**Goal**: Every wiki HTML page request is logged as NDJSON. Metrics page shows per-page counts, most-visited ranking, zero-visit flags. Log auto-rotates at 10 MB. Deleted page history preserved in archived segments.

**Independent Test**: Access 3 pages in browser (some multiple times) → open `/metrics` → counts match browser history → asset requests absent from counts. Check raw `access.log` matches report.

- [X] T033 [US4] Implement HTTP access logging in `wiki-server/app.py` — Flask `after_request` hook: if `request.path` starts with `/wiki/` or equals `/` and `request.method == "GET"`, append `{"ts": int(time.time()), "path": request.path, "status": response.status_code}` as NDJSON line to `access.log`; asset paths (`/assets/`, `/raw/`, `/static/`) must not be logged
- [X] T034 [US4] Implement log rotation in `wiki-server/app.py` — after each `access.log` write, if `os.path.getsize(ACCESS_LOG) > ACCESS_LOG_MAX_BYTES`: find next available segment number (glob `access.log.*`, parse 3-digit suffix, increment), rename `access.log` → `access.log.00N`, open fresh `access.log`
- [X] T035 [US4] Implement `wiki-server/metrics/report.py` — `generate_report()`: glob `access.log*` sorted by filename (lexicographic = chronological), parse each line as JSON, filter `status == 200`, aggregate count per `path`, return `MetricsReport(pages: list[PageStat(path, count)], sorted descending by count, with zero_count pages flagged)`
- [X] T036 [US4] Implement `GET /metrics` route in `wiki-server/app.py` — call `report.generate_report()`, render `metrics.html`; route is not logged in `access.log`
- [X] T037 [P] [US4] Create `wiki-server/templates/metrics.html` — extends `base.html`; table of wiki pages with request counts (descending); most-visited section (top 10); zero-visit pages flagged with "⚠ No visits" indicator; note that deleted-page history is preserved from archived log segments

**Checkpoint**: V-010, V-011, V-012 from quickstart.md pass. Counts verifiable against raw `access.log`. Rotation produces `access.log.001`; metrics include both segments.

---

## Phase 7: User Story 5 — Generate SVG Diagrams from Dot Notation (Priority: P5)

**Goal**: `make ingest TYPE=dot TARGET=<file.dot>` validates dot syntax, renders SVG to `wiki/assets/`, preserves dot source in `wiki/diagrams/`. SVG renders inline in browser. Syntax errors abort with no partial output.

**Independent Test**: `echo 'digraph G { A -> B }' > /tmp/t.dot && make ingest TYPE=dot TARGET=/tmp/t.dot` → `wiki/assets/t.svg` exists and is valid SVG → `wiki/diagrams/t.dot` preserved → open wiki page in browser → SVG renders inline. Syntax error → error printed, no SVG written.

- [X] T038 [US5] Implement `wiki-server/ingest/dot.py` — parse args: `dot_file` (required), `--page <wiki_page>` (optional); call `graphviz.Source(dot_text).render(format="svg", outfile=dest)` inside try/except `graphviz.backend.CalledProcessError`; on error: print `Dot syntax error in <file>: <detail>. No SVG written.` and exit 1; on success: write SVG to `wiki/assets/<name>.svg`, copy dot source to `wiki/diagrams/<name>.dot`; if `--page` provided: append `![diagram](/assets/<name>.svg)` reference to wiki page markdown
- [X] T039 [US5] Wire `ingest dot <dot_file> [--page <wiki_page>]` into `wiki-server/ingest/__init__.py` CLI dispatcher

**Checkpoint**: V-008 from quickstart.md passes (both success and syntax-error cases).

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final wiring, deployment validation, and `.gitignore`.

- [X] T040 [P] Create `.gitignore` — exclude: `search.db`, `access.log`, `access.log.*`, `__pycache__/`, `.venv/`, `*.pyc`, `.pytest_cache/`, `wiki/assets/*.svg` (generated, not source-controlled)
- [X] T041 [P] Update `CLAUDE.md` — add quickstart section: single `make install && make serve` start; dependency on feature `001-llm-wiki-system`; note that `search.db` and `access.log` are gitignored and regenerated via `make index`
- [X] T042 Validate all quickstart scenarios V-001 through V-013 per `quickstart.md` — work through each scenario manually or via `make test`; record any deviations
- [X] T043 [P] Verify `Makefile` `ingest` target correctly passes `TYPE` and `TARGET` make variables as subcommand args to `python -m wiki_server.ingest $(TYPE) $(TARGET)`
- [X] T044 [P] Verify Docker deployment: `make docker-build && make docker-up` → V-013 from quickstart.md passes; `wiki/` and `raw/` persist across `docker-down && docker-up`

**Checkpoint**: All 44 tasks complete. All quickstart validation scenarios pass locally and in Docker.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately; T004/T005/T006 are parallel
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories; T008/T009/T012 parallel after T007
- **User Story Phases (3–7)**: All depend on Phase 2 completion; can then proceed in priority order or in parallel if staffed
- **Polish (Phase 8)**: Depends on all desired user story phases being complete

### User Story Dependencies

- **US1 (P1)**: No inter-story dependencies — start after Phase 2
- **US2 (P2)**: Depends on `base.py` (T011) being complete — independent of US1
- **US3 (P3)**: Depends on FTS5 schema (T010) — independent of US1/US2 for search itself; T027 wires the ingest→index call
- **US4 (P4)**: Depends on Flask app (T008) — independent of US1/US2/US3
- **US5 (P5)**: Depends on CLI dispatcher (T012) — independent of all other stories

### Within Each Phase

- Models/helpers before services
- Services before route handlers
- Route handlers before templates
- Ingest handler before CLI wiring

### Parallel Opportunities

- T004, T005, T006 (Phase 1) — all parallel
- T008, T009, T011, T012 (Phase 2) — parallel after T007 and T010
- T013, T014, T017, T018 (Phase 3) — parallel; T015/T016/T019/T020/T021 sequential after T013
- T022, T023, T024, T025, T026 (Phase 4) — all parallel after T011; T027 after all handlers
- T028, T031 (Phase 5) — parallel; T029 after T028; T030/T032 after T029
- T033, T037 (Phase 6) — parallel; T034 after T033; T035 after T034; T036 after T035
- T038, T039 sequential; T039 after T038

---

## Parallel Example: User Story 2

```
# All five format handlers can be written simultaneously (different files):
T022 — wiki-server/ingest/webpage.py
T023 — wiki-server/ingest/pdf.py
T024 — wiki-server/ingest/image.py
T025 — wiki-server/ingest/podcast.py
T026 — wiki-server/ingest/youtube.py

# Then wire together:
T027 — wiki-server/ingest/__init__.py (depends on T022–T026)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (US1)
4. **STOP and VALIDATE**: `make serve` → V-001 and V-002 pass
5. Deploy/demo: wiki is browser-accessible

### Incremental Delivery

1. Setup + Foundational → skeleton ready
2. US1 → wiki browsable in browser (MVP)
3. US2 → ingest all five source formats
4. US3 → full-text search with BM25 ranking
5. US4 → visit metrics and log rotation
6. US5 → dot → inline SVG diagrams
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers after Phase 2 completes:

- Developer A: US1 (web server + templates)
- Developer B: US2 (ingest handlers)
- Developer C: US3 (FTS5 search) + US4 (metrics)

---

## Notes

- **FTS5 BM25**: Use SQLite's native `bm25(pages)` and `snippet(pages,...)` — no `rank-bm25` Python package needed (plan.md updated 2026-06-08). `data-model.md` still shows the old 3-table schema; the FTS5 schema in T010 supersedes it.
- **[P]**: task operates on different files from adjacent tasks — safe to run in parallel
- **[USN]**: maps task to user story for traceability and independent testing
- Each user story phase is independently completable and testable before the next begins
- Commit after each task or logical group
- Stop at any checkpoint to validate the story independently before proceeding
