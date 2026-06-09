# HTTP API Contract: Wiki Web Server

**Server**: Flask 3.x, `http://localhost:5000` (configurable via `config.py`)
**Format**: All responses are `text/html`; no JSON API endpoints
**Auth**: None (single-user local server, v1)

---

## Routes

### `GET /`

Serves the wiki index page (`wiki/index.md` rendered as HTML).

**Response**:

| Status | Condition |
| ------ | --------- |
| 200 OK | `wiki/index.md` rendered as HTML with clickable page links |
| 200 OK | "No pages yet" startup message if `wiki/` is empty or `index.md` absent |

**Logged**: Yes — entry appended to `access.log` (path `/`, status 200)

---

### `GET /wiki/<path:page>`

Serves a wiki page (`wiki/<page>.md` rendered as HTML).

**Path parameter**: `page` — relative path within `wiki/`, without `.md` extension.
Examples: `wiki/some-topic`, `wiki/subfolder/page`

**Response**:

| Status | Condition |
| ------ | --------- |
| 200 OK | Page content rendered as HTML; inline SVGs and local images served |
| 404 Not Found | `wiki/<page>.md` does not exist; renders `404.html` with link back to `/` |

**Logged**: Yes — entry appended to `access.log` (path, status)

**Note**: Static asset sub-requests triggered by viewing a wiki page (images, SVGs) are
NOT logged as separate page visits (FR-009).

---

### `GET /search`

Full-text BM25 search across all wiki pages.

**Query parameters**:

| Param | Required | Description |
| ----- | -------- | ----------- |
| q | yes | Search query string; one or more words |

**Response**:

| Status | Condition |
| ------ | --------- |
| 200 OK | `search.html` with ranked results (title, excerpt, link) |
| 200 OK | `search.html` with "No results found" message + suggested terms if applicable |

**Result fields per item**: page title, relative URL (`/wiki/<page>`), BM25 relevance score
(not shown to user), one-sentence excerpt with match in context.

**Multi-word queries**: pages matching all query terms rank above pages matching only some.

**Logged**: No (search is a system interface, not a wiki page visit)

---

### `GET /metrics`

Visit metrics report computed from all `access.log*` segments.

**Response**:

| Status | Condition |
| ------ | --------- |
| 200 OK | `metrics.html` — total requests per wiki page, most-visited ranking, zero-visit pages flagged |

**Report includes**:

- Total HTTP request count per wiki page (HTML pages only; assets excluded)
- Most-visited pages ranked descending by count
- Pages with zero requests flagged (candidate orphans, cross-referenceable with lint report)
- Deleted pages whose visit history is archived in rotated log segments (FR-011)

**Logged**: No (metrics is a system page)

---

### `GET /assets/<filename>`

Serves a generated SVG from `wiki/assets/<filename>`.

**Response**:

| Status | Condition |
| ------ | --------- |
| 200 OK | SVG content (`image/svg+xml`) |
| 404 Not Found | File does not exist |

**Logged**: No (static asset)

---

### `GET /raw/images/<filename>`

Serves a local image from `raw/images/<filename>` for inline display in wiki pages.

**Response**:

| Status | Condition |
| ------ | --------- |
| 200 OK | Image bytes with appropriate MIME type (image/jpeg, image/png, etc.) |
| 404 Not Found | File does not exist |

**Logged**: No (static asset)

---

## Error Responses

| Condition | Response |
| --------- | -------- |
| Wiki page not found | `404 Not Found` + `404.html` with link back to `/` |
| Server error | `500 Internal Server Error` + plain-text error description |

---

## Access Log Entry Format

One NDJSON line per wiki HTML page request (GET /wiki/* or GET /), appended after response:

```json
{"ts": 1717862400, "path": "/wiki/some-page", "status": 200}
```

Rotation: when `access.log` exceeds 10 MB → rename to `access.log.001` (incrementing) →
open fresh `access.log`. All segments included in `/metrics` report.
