<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan:
`specs/002-content-search-media/plan.md`
<!-- SPECKIT END -->

## Quickstart

**Prerequisite**: Feature `001-llm-wiki-system` must be set up first (`wiki/`, `raw/`, `index.md`, `log.md` must exist).

```sh
make install    # uv sync + playwright install chromium
make serve      # Flask at http://localhost:5000
```

**Ingest sources**:

```sh
make ingest TYPE=webpage TARGET=https://example.com
make ingest TYPE=pdf     TARGET=path/to/paper.pdf
make ingest TYPE=image   TARGET=path/to/photo.png
make ingest TYPE=podcast TARGET=path/to/episode.txt
make ingest TYPE=youtube TARGET=https://www.youtube.com/watch?v=ID
make ingest TYPE=dot     TARGET=path/to/diagram.dot
```

**Rebuild search index** (after bulk edits outside ingest):

```sh
make index
```

**Notes**:

- `search.db` and `access.log*` are gitignored and regenerated automatically.
- Search uses SQLite FTS5 native `bm25()` — no external search service needed.
- Log rotates at 10 MB; all segments remain queryable from `/metrics`.
