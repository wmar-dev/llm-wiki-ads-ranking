# Quickstart & Validation Guide: Content Search, Metrics & Multi-Format Media Ingestion

**Branch**: `002-content-search-media` | **Date**: 2026-06-08

---

## Prerequisites

| Requirement | Version | Install |
| ----------- | ------- | ------- |
| Python | 3.12+ | pyenv or system package |
| uv | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Graphviz | any | `brew install graphviz` (macOS) / `apt-get install graphviz` (Linux) |
| Playwright Chromium | via uv | `make install` runs `playwright install chromium` |
| yt-dlp | via uv | bundled in `pyproject.toml`; no manual install |
| Docker (optional) | 24+ | [docs.docker.com](https://docs.docker.com/get-docker/) |

**Feature dependency**: Feature `001-llm-wiki-system` must be set up first — `wiki/`,
`raw/`, `index.md`, `log.md`, and the project schema file must already exist.

---

## Setup

Local dev:

```sh
make install    # uv sync + playwright install chromium
make serve      # Flask on http://localhost:5000
```

Docker:

```sh
make docker-build
make docker-up  # http://localhost:5000 (wiki/ and raw/ mounted as volumes)
```

---

## Validation Scenarios

### V-001 — Wiki index loads in browser (SC-001)

```sh
make serve
# Open http://localhost:5000
```

**Pass**: `index.md` renders as HTML with clickable page links. Server reaches first page
in < 5 seconds.

**Edge case**: Empty `wiki/` shows a "No pages yet" message without errors.

---

### V-002 — 404 page (FR-003)

Navigate to `http://localhost:5000/wiki/nonexistent-page`.

**Pass**: 404 page with a link back to `/`. No stack trace shown to user.

---

### V-003 — Webpage ingest (FR-004, FR-005, FR-006)

```sh
make ingest TYPE=webpage TARGET=https://example.com
```

**Pass**:

1. `raw/web/example-com.html` exists
2. `wiki/example-com.md` exists with `source: raw/web/example-com.html` in frontmatter
3. `http://localhost:5000/wiki/example-com` loads in browser
4. `index.md` updated; `log.md` has new entry with `source_type: webpage`

---

### V-004 — Login-wall detection (FR-018)

```sh
make ingest TYPE=webpage TARGET=https://app.example.com/members-only
```

**Pass**: Command prints `Login wall detected at <url>. Provide a locally saved HTML file
instead.` Exit code 1. No file created in `raw/web/`. No wiki page created.

---

### V-005 — PDF ingest with auto-sectioning (FR-004, FR-016)

```sh
make ingest TYPE=pdf TARGET=path/to/large-paper.pdf   # PDF > 50 pages
```

**Pass**: Wiki summary page contains `## Section 1 (pages 1–50)`, `## Section 2 ...`, etc.
No user prompts issued between sections.

---

### V-006 — Podcast: transcript required, audio-only blocked (FR-015)

```sh
# Audio only — must block
make ingest TYPE=podcast TARGET=raw/podcasts/episode.mp3
```

**Pass**: Prints `Transcript required. Please provide a .txt or .srt file alongside the
audio.` Exit code 2. No wiki page created.

```sh
# With transcript — must succeed
make ingest TYPE=podcast TARGET=raw/podcasts/episode.txt
```

**Pass**: Wiki page created, `raw/podcasts/episode.txt` referenced in frontmatter.

---

### V-007 — YouTube ingest via yt-dlp (FR-004)

```sh
make ingest TYPE=youtube TARGET=https://www.youtube.com/watch?v=<id>
```

**Pass**:

1. `raw/videos/<slug>.vtt` and `raw/videos/<slug>.txt` exist
2. Wiki page created with chapter-level section headings (if chapters available)
3. Page accessible in browser

---

### V-008 — Dot diagram → inline SVG (FR-012, FR-013, FR-014)

```sh
echo 'digraph G { A -> B -> C }' > /tmp/test.dot
make ingest TYPE=dot TARGET=/tmp/test.dot
# Open http://localhost:5000/wiki/index (or link the SVG to a page with --page)
```

**Pass**:

1. `wiki/assets/test.svg` exists and is valid SVG
2. `wiki/diagrams/test.dot` exists (dot source preserved)
3. SVG renders inline in browser without plugins

**Dot syntax error case**:

```sh
echo 'invalid dot {{{' > /tmp/bad.dot
make ingest TYPE=dot TARGET=/tmp/bad.dot
```

**Pass**: Error message printed with dot error detail. No SVG written.

---

### V-009 — BM25 search (FR-007, FR-008, SC-003)

With 20+ pages ingested:

1. Navigate to `http://localhost:5000/search?q=<term-in-3-pages>`
2. Verify 3 results ranked by BM25 relevance, each with a one-sentence excerpt
3. Click a result — verify navigation to the correct wiki page
4. Search for a term in zero pages — verify "No results found" message

**Performance**: Response time < 3 seconds (SC-003).

**Multi-word query**: search `word-a word-b` — pages containing both should rank above
pages containing only one.

---

### V-010 — Visit metrics (FR-009, FR-010, SC-004)

1. Visit three wiki pages in browser (some multiple times), total N requests
2. Navigate to `http://localhost:5000/metrics`
3. Verify each page shows exact count matching browser history
4. Load an SVG asset directly — verify it does NOT appear in the metrics counts
5. Cross-check counts against raw `access.log` entries

---

### V-011 — Log rotation (FR-017)

Populate `access.log` to > 10 MB (can be done with a test helper that writes synthetic
entries), then trigger one more page request.

**Pass**:

- `access.log.001` exists (old segment renamed)
- Fresh `access.log` exists for new entries
- `/metrics` report includes counts from both files

---

### V-012 — Deleted page history preserved (FR-011, SC-007)

1. Ingest a page; visit it N times in browser
2. Delete `wiki/<page>.md`
3. Navigate to `http://localhost:5000/metrics`

**Pass**: Deleted page's visit count still appears in the metrics report (read from archived
log segments).

---

### V-013 — Docker deployment (SC-001, V)

```sh
make docker-build && make docker-up
```

**Pass**: All V-001 through V-012 pass against `http://localhost:5000`. After
`make docker-down && make docker-up`, `wiki/` and `raw/` data persist via volume mounts.
`search.db` survives container restart.

---

## Common Failure Modes

| Symptom | Likely cause | Fix |
| ------- | ------------ | --- |
| Pages 404 after `make serve` | `wiki/` empty or feature 001 not set up | Run feature 001 setup first |
| Search returns no results | `search.db` empty or missing | Run `make index` |
| `playwright: command not found` | chromium not installed | `make install` |
| yt-dlp fails with `DownloadError` | Video has no subtitle track | See no-transcript error message |
| `dot: command not found` | Graphviz not in PATH | Install graphviz system package |
| Metrics counts seem low | Asset requests mistakenly excluded | Expected — FR-009 excludes assets by design |
