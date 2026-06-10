
## Quickstart

```sh
make install    # uv sync + playwright install chromium
make serve      # Flask at http://localhost:5000
make dev        # Flask at http://localhost:5000 with debug mode + auto-reload
```

**Grow the wiki** — use Claude skills, not shell commands:

- `/wiki-ingest <url-or-path>` — ingest a source into `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`; updates `wiki/index.md` and `wiki/log.md`
- `/wiki-query <question>` — synthesize a cited answer from the wiki, auto-ingesting web sources if coverage is incomplete
- `/wiki-lint` — health-check the wiki (orphans, broken links, missing frontmatter, stale/contested pages, Mermaid syntax)
- `/answer-open-questions` — research and resolve "Open question:" gaps across wiki pages

**Maintenance** (only needed after bulk edits made outside the skills):

```sh
make index             # rebuild search.db
make validate-mermaid  # validate all Mermaid diagrams in wiki/
```

**Notes**:

- `wiki/index.md` and `wiki/log.md` are auto-created by `/wiki-ingest` on first run if missing.
- `search.db` and `access.log*` are gitignored and regenerated automatically.
- Search uses SQLite FTS5 native `bm25()` — no external search service needed.
- Log rotates at 10 MB; all segments remain queryable from `/metrics`.
- Wiki pages support Mermaid diagrams (fenced ` ```mermaid ` blocks), GFM tables, and linked matplotlib chart scripts (`wiki/assets/<slug>-chart.py`).
- `/wiki/<slug>` and `/wiki/<slug>.md` both resolve to the same page.

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
at specs/002-content-search-media/plan.md
<!-- SPECKIT END -->
