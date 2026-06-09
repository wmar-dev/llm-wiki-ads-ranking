# Data Model: Content Search, Metrics & Multi-Format Media Ingestion

**Branch**: `002-content-search-media` | **Date**: 2026-06-08

---

## SQLite Search Index (`search.db`)

### Table: `documents`

| Column | Type | Constraints | Description |
| ------ | ---- | ----------- | ----------- |
| id | INTEGER | PRIMARY KEY | Auto-increment row ID |
| page_path | TEXT | UNIQUE NOT NULL | Relative path: `wiki/page-name.md` |
| title | TEXT | | H1 heading extracted from page content |
| content_hash | TEXT | NOT NULL | SHA-256 of raw markdown; skip re-index if unchanged |
| word_count | INTEGER | NOT NULL | Token count after stopword removal; BM25 length normalization |
| indexed_at | INTEGER | NOT NULL | Unix timestamp of last index update |

### Table: `term_frequencies`

| Column | Type | Constraints | Description |
| ------ | ---- | ----------- | ----------- |
| document_id | INTEGER | NOT NULL, FK → documents.id ON DELETE CASCADE | |
| term | TEXT | NOT NULL | Lowercase normalized token |
| frequency | INTEGER | NOT NULL | Raw occurrence count in document |

PRIMARY KEY: `(document_id, term)`

### Table: `corpus_stats`

| Column | Type | Constraints | Description |
| ------ | ---- | ----------- | ----------- |
| key | TEXT | PRIMARY KEY | `'corpus_size'` or `'avg_doc_length'` |
| value | REAL | NOT NULL | Numeric stat value |

**BM25 computation**: IDF = log((N − df + 0.5) / (df + 0.5) + 1) where N = `corpus_size`
and df = count of documents containing the term (derived from `term_frequencies` join).
Scores computed at query time; no cached score table needed at < 500 pages.

**Incremental update**: On ingest of page P →
`DELETE FROM documents WHERE page_path = P` (cascades to term_frequencies) →
INSERT new document + term rows → UPDATE corpus_stats.

---

## File System Layout

### `raw/` — Source copies (never modified by LLM)

```text
raw/
├── web/           # Playwright-rendered webpage HTML
│   └── <slug>.html
├── papers/        # PDF files (academic)
│   └── <slug>.pdf
├── docs/          # PDF files (other documents)
│   └── <slug>.pdf
├── images/        # Original image files
│   └── <slug>.<ext>          # JPEG, PNG, GIF, WebP
├── podcasts/      # Podcast transcripts
│   ├── <slug>.txt            # Plain text transcript (primary citation)
│   └── <slug>-audio.<ext>   # Audio file if provided alongside transcript
└── videos/        # YouTube transcripts
    ├── <slug>.txt            # Plain text (stripped from VTT)
    └── <slug>.vtt            # Raw WebVTT subtitle file (preserved)
```

**Slug derivation**: URL-safe lowercase kebab-case from source title or URL hostname + path.
Collisions resolved by appending `-2`, `-3`, etc.

### `wiki/` — LLM-written pages

```text
wiki/
├── index.md              # Master index; updated on every ingest
├── <topic-name>.md       # One page per ingested source or concept
├── assets/               # Generated SVG files
│   └── <diagram-name>.svg
└── diagrams/             # Dot source files (preserved for re-rendering)
    └── <diagram-name>.dot
```

### Wiki Page Frontmatter

All wiki pages include YAML frontmatter (required by feature 001 schema):

```yaml
---
title: "Page Title"
source: raw/web/slug.html        # Local raw/ path — required citation (Principle III)
source_type: webpage             # webpage | pdf | image | podcast | video | manual
ingested_at: 2026-06-08T14:00:00Z
tags: []
---
```

The `source` field is the provenance citation. If a page synthesizes multiple sources,
`source` is a YAML list of local paths.

---

## Access Log

### Active log: `access.log` (project root, configurable in `config.py`)

### Archived segments: `access.log.001`, `access.log.002`, ... (rotation at 10 MB)

Segment naming is zero-padded to 3 digits so lexicographic order = chronological order.
The metrics report reads all files matching `access.log*`, sorted by filename.

### Entry format — one NDJSON object per line:

```json
{"ts": 1717862400, "path": "/wiki/some-page", "status": 200}
```

| Field | Type | Description |
| ----- | ---- | ----------- |
| ts | integer | Unix timestamp (seconds) |
| path | string | Request path — wiki HTML pages only; asset requests excluded (FR-009) |
| status | integer | HTTP response status code |

Only `status == 200` responses are counted in the metrics report. The raw log records all
wiki-page requests (including 404s on wiki paths) for complete historical data.

---

## Entity Lifecycle

### Ingest workflow (all formats)

```text
User provides source
  → format handler: validate + detect issues (login-wall, missing transcript, dot syntax)
  → on failure: print error, exit — nothing written
  → on success: save file to raw/<format>/<slug>
  → LLM: write wiki/<slug>.md with YAML frontmatter + citation + content
  → search/index.py: incremental update (delete old + insert new term rows)
  → update corpus_stats
  → append entry to log.md
  → return success
```

### Search workflow

```text
GET /search?q=<query>
  → tokenize query terms
  → rank-bm25: score each document via term_frequencies + corpus_stats
  → fetch top-N page_path + title from documents table
  → extract excerpt: find first sentence containing any query term
  → render search.html with ranked list (title, excerpt, link)
```

### Visit metrics workflow

```text
HTTP request arrives at Flask
  → Flask before_request hook
  → if path matches /wiki/* and method == GET
  → after_request hook: if response.status_code == 200
      → append NDJSON entry to access.log
      → if os.path.getsize(access.log) > 10 MB: rotate
          (rename access.log → access.log.00N, open fresh access.log)
```

### Dot diagram workflow

```text
User provides .dot file
  → graphviz.Source(dot_text).render(format="svg") — validate syntax
  → on error: print error, no file written (FR-012 acceptance scenario 3)
  → on success: write SVG to wiki/assets/<name>.svg
  → copy .dot source to wiki/diagrams/<name>.dot
  → if --page provided: insert SVG reference into wiki page markdown
```
