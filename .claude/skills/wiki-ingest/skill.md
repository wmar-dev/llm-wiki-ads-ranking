---
name: wiki-ingest
description: Processes a source document (local file or URL) into wiki pages, updates the index and log, and appends a self-evaluation entry. Use when the researcher wants to add a new source to the wiki, ingest a document, or refresh an existing source.
---

# Wiki Ingest Skill

Process a source document (local file or URL) into wiki pages, update the index
and log, and append a micro self-evaluation entry.

**Trigger**: `/wiki-ingest <path-or-url>`

## When to use

Use this skill whenever the researcher wants to add a new source to the wiki or
refresh an existing one. Works with URLs (fetched via WebFetch), and local Markdown,
plain-text, PDF, and image files (read directly).

## Prerequisites

- `wiki/` directory exists
- `raw/` directory exists
- `wiki/index.md` and `wiki/log.md` are created automatically on first ingest if missing

---

## Steps

### Step 0 — Bootstrap (first-ever ingest only)

If `wiki/index.md` does not exist, create it:

```markdown
# Wiki Index

<!-- entries added by /wiki-ingest -->
```

If `wiki/log.md` does not exist, create it:

```markdown
# Wiki Log

<!-- entries added by /wiki-ingest, /wiki-query, /wiki-lint -->
```

If `wiki/meta/evaluations.md` does not exist, create it:

```markdown
# Evaluations

<!-- micro entries appended by /wiki-ingest; macro entries appended by /wiki-lint -->
```

Then proceed to Step 1.

---

### Step 1 — Source acquisition

**If the input is a local file path:**

1. Verify the file exists using Read.
2. If it is a PDF, read as many pages as possible. Note if content was truncated.
3. If the file is an image, read and visually describe the content.
4. Proceed to Step 2.

**If the input is a URL:**

1. Fetch the page using WebFetch.
2. If WebFetch fails, retry once with a slightly different accept header. If still
   failing, try a web search for the page title to find an alternate URL.
3. If all fetch attempts fail, or if the fetched content is <100 words or contains
   paywall/login markers (e.g., "Sign in to read", "Subscribe to continue"):
   - Log: `## [YYYY-MM-DD] fetch-failed | <url> — <reason>`
   - Notify the researcher.
   - Stop.
4. Save fetched content to `raw/web/<slug>.md` where `<slug>` is a kebab-case
   summary of the page title or URL path.
5. Log: `## [YYYY-MM-DD] fetch | <url>`
6. Proceed to Step 2.

---

### Step 2 — Duplicate detection

Read `wiki/index.md`. Check whether the source filename or origin URL is already listed.

**If this is a re-ingest:**

- Log: `## [YYYY-MM-DD] re-ingest | <source title>`
- Set `status: stale` on every wiki page whose `sources[]` frontmatter lists this
  source filename.
- Update `last_updated` on those pages to today's date.
- Continue processing to refresh content.

**If this is a new source:** proceed to Step 3.

---

### Step 3 — Chunking

Estimate the source length in words.

- If the source likely exceeds the context window (>6000 words):
  - Split into sequential chunks of ≤3000 words.
  - Merge the final remainder into the preceding chunk if it is <200 words.
  - Process each chunk through Steps 4–6 sequentially.
  - Consolidate all chunk summaries into one unified source summary page and note
    the chunked processing in the page body.
  - Set `processing_status: chunked` in the `wiki/index.md` entry.
- Otherwise: proceed as a single pass.

---

### Step 4 — Source credibility assessment

Determine the `source_type` using these signals:

| source_type | Signals |
|---|---|
| `peer_reviewed` | DOI present, ISSN, journal name in byline, "Abstract" section, numbered references |
| `industry_report` | Company or consultancy byline, market sizing data, "Executive Summary" |
| `news_article` | News outlet domain or byline, dateline, inverted-pyramid structure |
| `blog_post` | Personal domain, informal/first-person tone, no institutional affiliation |
| `other` | None of the above signals present |

Record `source_type` in the `wiki/index.md` entry for this source.

---

### Step 5 — Write wiki pages

**Read `wiki/index.md` first.** Identify existing pages related to this source's content.
Read at most 5 of those pages. If more than 5 pages are relevant, search `wiki/index.md`
for key terms to pre-filter, then read the top 5.

**Write or update the following pages:**

1. **Source summary** — `wiki/sources/<slug>.md` (`type: source_summary`)
   Always created fresh (or updated if re-ingesting).

2. **Entity pages** — `wiki/entities/<slug>.md` (`type: entity`)
   One page per named actor: company, team, model, system, ranking pipeline, dataset,
   or experiment platform. Create if missing (`status: draft`); update `sources[]`
   and body if existing.

3. **Concept pages** — `wiki/concepts/<slug>.md` (`type: concept`)
   One page per significant domain idea: ads ranking, LLM serving, experiment
   frameworks, feature engineering, retrieval-augmented generation, relevance
   scoring, etc. Create if missing (`status: draft`); update if existing.

All wiki pages MUST include full YAML frontmatter:

```yaml
---
title: "..."
type: "..."           # source_summary | entity | concept | synthesis | comparison
sources:
  - "<raw-filename>"
status: "draft"       # new pages start as draft; set to current once verified
created: "YYYY-MM-DD"
last_updated: "YYYY-MM-DD"
---
```

Set `status: current` immediately if the source is `peer_reviewed` or
`industry_report`. Set `status: draft` for `news_article`, `blog_post`, or `other`.

For claims from non-peer-reviewed material, append a credibility label:
> "Claim text." — [[wiki/sources/slug.md]] *(blog post)*

Label inferences explicitly: `Inference: <claim>`
Label unanswerable gaps: `Open question: <question>`

---

### Step 5b — Visuals

When writing or updating wiki pages, enrich them with tables, diagrams, and plots where helpful. Use the decision table below:

| Content type | When to use | Format |
|---|---|---|
| **Markdown table** | Comparing ≥3 items across ≥2 attributes; listing metrics or parameters | Standard GFM table in the page body |
| **Graphviz diagram (preferred)** | Pipelines, architectures, data flows, decision trees, timelines, entity relationships | DOT source in `wiki/diagrams/<slug>-diagram-N.dot`, rendered to `wiki/assets/<slug>-diagram-N.svg` |
| **Mermaid diagram (fallback)** | Same use cases, only when Graphviz isn't suitable | Fenced code block: ` ```mermaid ` |
| **Matplotlib script** | Quantitative data with numeric trends, distributions, or comparisons | `wiki/assets/<slug>-chart.py` with `plt.savefig("wiki/assets/<slug>-chart.png")` |

**Graphviz diagram guidance (preferred):**
- Write DOT source to `wiki/diagrams/<slug>-diagram-N.dot` (N increments per page, starting at 1)
- Render it: `uv run python scripts/render_dot.py wiki/diagrams/<slug>-diagram-N.dot`
- Embed the result in the page: `![<slug>-diagram-N](/assets/<slug>-diagram-N.svg)`
- Use `rankdir=LR` for pipelines and data flows, `rankdir=TB` for hierarchies and decision trees
- Use `shape=box, style=rounded` for steps/nodes, `shape=diamond` for decisions, `cluster_<name>` subgraphs for groupings
- Keep node labels short (≤5 words); add a prose caption below the image
- If the `.dot` source is edited later, re-render it so the SVG stays in sync

**Mermaid diagram guidance (fallback):**
- Use only if `scripts/render_dot.py` or the `dot` CLI is unavailable, Graphviz rendering
  errors out, or the researcher explicitly asks for an editable Mermaid diagram
- Use `flowchart LR` for pipelines and data flows
- Use `sequenceDiagram` for request/response or multi-system interactions
- Use `classDiagram` for model or schema relationships
- Use `gantt` for timelines
- Keep node labels short (≤5 words); add a prose caption below the diagram block

**Matplotlib guidance:**
- Only generate a script when the source contains actual numeric data worth plotting
- Add a prose note in the page: `*Chart: run `python wiki/assets/<slug>-chart.py` to regenerate.*`
- Do not execute the script; the researcher runs it

**Table guidance:**
- Always add a header row; align columns left
- Prefer tables over prose lists when rows share the same attributes

---

### Step 6 — Contradiction check

Compare new claims from this source against existing `current` and `contested` pages
read in Step 5.

**On any disagreement between this source and an existing page:**
- Add a note in both the new source summary and the affected existing page.
- Log: `## [YYYY-MM-DD] contradiction | <affected page> vs <new source>`

**When ≥3 sources disagree on a claim:**
- Set `status: contested` on the affected wiki page.
- Add a "Dispute" section to that page:

```markdown
## Dispute

3+ sources disagree on [claim]. See:
- [[wiki/sources/source-a.md]] — claims X *(peer_reviewed)*
- [[wiki/sources/source-b.md]] — claims Y *(industry_report)*
- [[wiki/sources/source-c.md]] — claims Z *(blog_post)*

Credibility-weighted assessment: [which claim is better supported and why]
```

---

### Step 7 — Update wiki/index.md

For every wiki page written or modified in Step 5, add or update its entry:

```
- [Title](wiki/type/slug.md) — one-line summary [status: current] [sources: N]
```

- `status` tag reflects the page's current status field.
- `sources: N` count must match the page's `sources[]` array length.
- `stale` and `contested` pages MUST include their status tag.

---

### Step 8 — Update wiki/log.md

Append:

```
## [YYYY-MM-DD] ingest | <source title>

<1–2 sentence summary of what was processed and any notable findings>
```

---

### Step 9 — Micro self-evaluation

Append ≤3 brief observations to `wiki/meta/evaluations.md`:

```
- [YYYY-MM-DD ingest] <brief observation>
```

Observations should note one or more of:
- Token usage (e.g., "read 4/5 allowed pages; no search needed")
- Any contradiction or credibility issue encountered
- A coverage gap identified

Do NOT write the full macro evaluation table here — that is triggered by the lint skill.

---

### Step 10 — Finalize

Set source metadata in `wiki/index.md`:
- `processing_status: processed` (or `chunked` if Step 3 applied)
- `ingest_count: N` (1 for new source; incremented for re-ingest)

Report to the researcher:
- Path of the new wiki page(s)
- Path of the raw source copy
- Whether `wiki/index.md` was updated
- Any contradictions or credibility issues found

---

## Error handling

| Condition | Action |
|---|---|
| WebFetch fails after retry | Log `fetch-failed`; notify researcher; stop |
| Fetched content <100 words or paywalled | Treat as fetch failure (above) |
| PDF content truncated | Note truncation in wiki page body; proceed with available content |
| Mid-ingest failure | Set `processing_status: failed`; log failure with reason |

---

## Token budget

- 1 read: `wiki/index.md`
- ≤5 reads: related wiki pages
- 1 read: source file or fetched content
- Total target: ≤8 file reads per ingest

If this budget is exceeded, append a tool-gap observation to `wiki/meta/evaluations.md`.
