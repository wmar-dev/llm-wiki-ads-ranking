# CLI Contract: Ingest & Index Commands

All commands are invoked via `python -m wiki_server.<module>` or Makefile shortcuts.

---

## Ingest Commands

```sh
python -m wiki_server.ingest <subcommand> [args]
# or
make ingest TYPE=<subcommand> TARGET=<arg>
```

---

### `ingest webpage <url>`

Fetches URL via Playwright (headless Chromium), detects login-wall, saves HTML to `raw/web/`,
writes wiki summary page, updates search index, appends `log.md`.

| Argument | Required | Description |
| -------- | -------- | ----------- |
| url | yes | Full URL including scheme (`https://...`) |

**Exit codes**:

| Code | Condition |
| ---- | --------- |
| 0 | Success — `raw/web/<slug>.html` written, wiki page created, index updated |
| 1 | Login-wall detected — error message printed naming the URL; no files written |
| 1 | Network error or Playwright navigation timeout |
| 1 | Playwright / chromium not installed |

**Login-wall error message format**:
`Login wall detected at <url>. Provide a locally saved HTML file instead.`

---

### `ingest pdf <file_path>`

Extracts text from PDF with pdfplumber, auto-sections at 50-page boundaries, writes wiki
summary page with section headings.

| Argument | Required | Description |
| -------- | -------- | ----------- |
| file_path | yes | Local path to PDF file |

**Exit codes**:

| Code | Condition |
| ---- | --------- |
| 0 | Success — PDF stored in `raw/papers/` or `raw/docs/`, wiki page created |
| 1 | File not found, unreadable, or not a valid PDF |

---

### `ingest image <file_path>`

Validates image with Pillow, passes to multimodal LLM for description, writes wiki summary
page, stores image in `raw/images/`.

| Argument | Required | Description |
| -------- | -------- | ----------- |
| file_path | yes | Local path to image file (JPEG, PNG, GIF, WebP) |

**Exit codes**:

| Code | Condition |
| ---- | --------- |
| 0 | Success — image stored in `raw/images/`, wiki page with description created |
| 1 | File not found or unsupported format |

---

### `ingest podcast <file_path>`

Accepts a transcript file (`.txt` or `.srt`) directly. If given an audio file with no
accompanying transcript, blocks with a clear error message (FR-015).

| Argument | Required | Description |
| -------- | -------- | ----------- |
| file_path | yes | Path to transcript (`.txt`, `.srt`) or audio file (`.mp3`, `.m4a`, `.wav`) |

**Exit codes**:

| Code | Condition |
| ---- | --------- |
| 0 | Transcript provided — saved to `raw/podcasts/`, wiki page created |
| 2 | Audio-only input — transcript required error, no files written |
| 1 | File not found |

**Audio-only error message**:
`Transcript required. Please provide a .txt or .srt file alongside the audio.`

---

### `ingest youtube <url>`

Downloads transcript via yt-dlp, converts VTT → plain text, saves both to `raw/videos/`,
writes wiki page with chapter-level breakdown where chapters are available.

| Argument | Required | Description |
| -------- | -------- | ----------- |
| url | yes | YouTube video URL |

**Exit codes**:

| Code | Condition |
| ---- | --------- |
| 0 | Success — `raw/videos/<slug>.txt` and `.vtt` written, wiki page created |
| 1 | No transcript/subtitle track available for this video |
| 1 | yt-dlp not installed or network error |

**No-transcript error message**:
`No transcript available for <url>. The video may lack subtitles.`

---

### `ingest dot <dot_file> [--page <wiki_page>]`

Renders Graphviz dot source to SVG, saves SVG to `wiki/assets/`, preserves dot source in
`wiki/diagrams/`. Optionally embeds an SVG reference in a wiki page.

| Argument | Required | Description |
| -------- | -------- | ----------- |
| dot_file | yes | Path to `.dot` source file |
| --page | no | Wiki page path to embed SVG in (e.g., `wiki/architecture.md`) |

**Exit codes**:

| Code | Condition |
| ---- | --------- |
| 0 | Success — SVG written to `wiki/assets/<name>.svg`, dot source to `wiki/diagrams/<name>.dot` |
| 1 | Dot syntax error — error message printed, no SVG or partial file written |
| 1 | Graphviz system package not installed |

**Syntax error message format**:
`Dot syntax error in <file>: <graphviz error>. No SVG written.`

---

## Index Commands

```sh
python -m wiki_server.search <subcommand> [args]
# or
make index
```

---

### `search rebuild`

Drops and rebuilds the entire SQLite BM25 index from all current `wiki/*.md` files.

**When to use**: After bulk wiki edits outside the ingest workflow, or to repair a corrupted
`search.db`. Normal ingest uses incremental update automatically.

| Exit code | Condition |
| --------- | --------- |
| 0 | Success — `search.db` rebuilt; corpus_stats updated |
| 1 | `wiki/` directory not found or unreadable |

---

### `search update <page_path>`

Incrementally updates the index for a single wiki page (delete old entry + reindex).
Called automatically by every ingest operation.

| Argument | Required | Description |
| -------- | -------- | ----------- |
| page_path | yes | Path to the wiki page: `wiki/page-name.md` |

| Exit code | Condition |
| --------- | --------- |
| 0 | Success |
| 1 | Page file not found |
