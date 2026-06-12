# LLM Wiki — Ads Ranking & Recommendation Systems

A personal knowledge base on **ads ranking, auction mechanisms, A/B testing, and
large-scale recommendation systems**, incrementally built and maintained by an LLM
agent (Claude Code).

Rather than re-deriving answers from raw documents on every question (the typical
RAG pattern), an LLM agent reads new sources, integrates them into a structured wiki
of interlinked markdown pages, flags contradictions, and keeps the synthesis current.
The wiki is a compounding artifact — see [llm-wiki.md](llm-wiki.md) for the underlying
pattern.

## Architecture

```text
raw/        immutable copies of source documents (papers, articles, transcripts)
wiki/       LLM-maintained markdown pages (sources, entities, concepts, synthesis)
CLAUDE.md   the schema — tells the agent how to ingest, query, and lint the wiki
```

A small Flask app (`wiki_server/`) renders `wiki/` as browsable HTML with full-text
search (SQLite FTS5 / BM25), Mermaid diagrams, GFM tables, and matplotlib charts.

## Quickstart

```sh
make install    # uv sync + playwright install chromium
make serve      # Flask at http://localhost:8000
make dev        # Flask with debug mode + auto-reload
```

## Growing the wiki

The wiki is built and maintained through Claude Code skills — no manual editing or
shell commands required:

| Skill | Purpose |
| --- | --- |
| `/wiki-ingest <url-or-path>` | Ingest a source: save raw copy, write/update wiki pages, update index and log |
| `/wiki-query <question>` | Synthesize a cited answer from the wiki, auto-ingesting web sources if coverage is incomplete |
| `/wiki-lint` | Health-check the wiki (orphans, broken links, missing frontmatter, stale/contested pages, Mermaid syntax) |
| `/answer-open-questions` | Research and resolve `Open question:` gaps left across wiki pages |

## Wiki structure

```text
wiki/
├── index.md      # catalog of all pages, organized by topic
├── log.md        # chronological record of ingests, queries, and lint passes
├── sources/      # one page per ingested source, with citation
├── entities/     # companies, systems, models, teams
├── concepts/     # domain ideas (ranking, auctions, retrieval, experimentation, ...)
├── synthesis/    # cross-source answers and overviews
├── diagrams/     # standalone DOT/SVG diagrams
├── assets/       # matplotlib chart scripts and generated images
└── meta/         # self-evaluation log
```

## Topics covered

Ad formats & blindness, auction mechanisms (GSP/Vickrey), ranking optimality,
A/B testing & experimentation infrastructure, ad rank/LTV scoring, CTR prediction
at scale (FTRL-Proximal), two-tower & generative retrieval (Semantic IDs), and
production ranking systems at Google, Meta, Reddit, TikTok, and Pinterest.

## Maintenance

```sh
make index             # rebuild search index in wiki.db after bulk edits made outside the skills
make validate-mermaid  # validate all Mermaid diagrams in wiki/
make test              # run pytest
```
