---
name: answer-open-questions
description: Scans the wiki for unresolved open questions, researches answers via web search, ingests relevant sources, and updates wiki pages to convert open questions into cited claims.
---

# Answer Open Questions Skill

Scan the wiki for unresolved open questions, research answers via web search,
ingest relevant sources, and update wiki pages to convert open questions into
cited claims.

**Trigger**: `/answer-open-questions`

## When to use

Use this skill when you want to close gaps in the wiki's knowledge. It finds all
"Open question:" labels across wiki pages, researches each one via web search and
source ingestion, then updates the originating page with the answer. Run after
several ingests have accumulated, or periodically as a knowledge-gap maintenance
cycle.

## Prerequisites

- `wiki/index.md` exists with at least one entry
- Web search / web fetch tools are available
- `/wiki-ingest` skill workflow is understood (Step 4 delegates to it)

---

## Steps

### Step 1 — Scan for open questions

Search the wiki for occurrences of "Open question:" inline labels and `## Open Questions` section headings across all page types:

```bash
rg -n "Open question:|^## Open Questions$" wiki/
```

After grep, for each file containing `## Open Questions`, read the page and
extract the bullet items (`- ` prefix) under that heading — each is an open
question.

Parse each match. For each result, capture:
- **File path** (e.g., `wiki/concepts/thermal-management.md`)
- **Line number** (exact line of the match)
- **Full text** of the open question (inline: everything from "Open question:"
  to the next blank line, heading, or end of the section; section-format: the
  full bullet item under `## Open Questions`)
- **Page type** (concept, synthesis, entity — from frontmatter `type:` field)
- **Existing sources** on that page (from frontmatter `sources[]`)

Present the complete list to the researcher in a numbered format:

```
Found N open questions across M pages:

1. wiki/concepts/thermal-management.md:36 — What is the maximum radiator area practically deployable on an orbital platform given launch mass and deployment complexity constraints?
2. wiki/concepts/space-datacenter-component-lifetimes.md:61 — No source in the wiki quantifies radiator degradation rates over multi-year LEO missions.
...

Which would you like to research? (enter numbers, "all", or "none")
```

Wait for the researcher's selection.

---

### Step 2 — Research each selected question (loop)

For each selected open question, in order:

#### 2a — Formulate search queries

From the open question text, derive 2–3 web search queries that are likely to
yield authoritative answers. Consider:

- **If the question asks for a specific quantity** (e.g., "maximum radiator area",
  "radiator degradation rates"): use technical/academic search terms
- **If the question asks about a company or program** (e.g., "Is TeraWave a data
  center or laser constellation?"): use news/company-specific terms
- **If the question asks about feasibility** (e.g., "Can orbital data centers be
  serviced or refueled?"): search for on-orbit servicing (OOS) literature,
  refueling missions, and satellite servicing programs

Use `websearch` tool for each query. Set `livecrawl: "preferred"` for news-related
questions, `type: "deep"` for technical/quantitative questions.

#### 2b — Evaluate search results

From the search results and any fetched pages, determine whether a satisfactory
answer exists:

| Finding | Action |
| ------- | ------ |
| Clear answer found in one source | Proceed to Step 2c |
| Multiple sources converge on same answer | Pick the most authoritative; proceed to Step 2c |
| Partial answer (covers some but not all aspects) | Note what is still unknown; proceed to Step 2c for what is answerable |
| No credible source found | Mark question as unresolved; log it; skip to next question |

**Credibility filters:**
- Prefer peer-reviewed (DOI, journal) > industry report > news article > blog post
- Reject sources that are paywalled behind login (cannot be ingested) or pure
  speculation without data
- For quantitative claims: require at least one source with explicit numbers,
  not hand-wavy ranges

#### 2c — Ingest the source

Run the full `/wiki-ingest` skill workflow for each new source found:

1. Fetch the source content (URL -> save to `raw/<slug>.md`)
2. Write wiki pages (source summary, entity/concept pages as needed)
3. Update `wiki/index.md` and `wiki/log.md`

If multiple sources are needed for a single open question, ingest them all before
proceeding to Step 2d. Limit to 3 sources per open question to stay within token
budget.

#### 2d — Update the originating wiki page

Read the page that contained the open question. Edit the page:

1. **Replace** the "Open question: ..." line with the answered claim, cited:
   ```
   Claim text. [[wiki/sources/new-source-slug.md]]
   ```
2. **Add** the new source filename(s) to the page's frontmatter `sources[]` array.
3. **Update** `last_updated:` to today's date in the frontmatter.
4. **If the answer is partial** (covers some aspects but leaves sub-questions open):
   - Replace the original open question with the partial answer
   - Add a new "Open question:" bullet for whatever remains unknown
5. **If the answer reveals a contradiction** with existing claims on the page:
   - Follow the contradiction check protocol from the ingest skill (Step 6):
     add a note in both the source summary and the affected page; if 3+ sources
     disagree, set `status: contested` and add a "Dispute" section.

**Editing rules:**
- Preserve all other content on the page
- Keep existing citations; add new ones, do not remove
- Match the existing section structure (the open question may be in an
  "## Implications" or "## Open Questions" section — adapt to context)
- If the page has no `## Open Questions` section (the question was inline in prose),
  just replace it inline

---

### Step 3 — Open question cleanup across related pages

After each page is updated in Step 2d, check whether any **other** wiki pages
reference the same open question text (e.g., the same question might appear in
both a concept page and a synthesis page).

Use ripgrep to find duplicates:

```bash
rg -n "<distinctive fragment of the open question>" wiki/
```

If other pages contain the identical or substantially similar open question,
propose updating them too. Wait for researcher confirmation before editing
multiple pages for the same question.

---

### Step 4 — Log

Append to `wiki/log.md`:

```
## [YYYY-MM-DD] answer | <open-question-summary> | pages-updated: N | sources-ingested: N

<1–2 sentence summary of what was found and which pages were modified>
```

For each question that could not be answered (no credible sources found), also log:

```
## [YYYY-MM-DD] answer-unresolved | <open-question-summary> — no credible sources found
```

---

### Step 5 — Micro self-evaluation

Append to `wiki/meta/evaluations.md`:

```
- [YYYY-MM-DD answer] <brief observation about what was answered, any gaps remaining, or tool issues>
```

---

## Token budget

- 1 read: scan results (Step 1 — built from `rg` output, not file reads)
- 5 reads: selected open-question pages (read when updating)
- 3 web searches per open question (Step 2a)
- 3 ingest operations per open question (Step 2c — each follows the ingest skill's
  own 8-read budget)
- 1 read per page being updated (Step 2d)
- 1 read: `wiki/log.md` (Step 4)
- 1 read: `wiki/meta/evaluations.md` (Step 5)

**Budget per open question**: 3 fetches/ingests + 1 page update + 1 log write.
**Batch budget**: for N selected questions, total = 5 + 2N reads, plus N × 3 ingest
operations.

If the budget is exceeded for any question, append a tool-gap observation to
`wiki/meta/evaluations.md`.

---

## Error handling

| Condition | Action |
| --------- | ------ |
| Web search returns no useful results for a question | Mark as unresolved; log `answer-unresolved`; skip |
| Ingest fails for a promising source | Try one alternative source; if that also fails, mark unresolved |
| Page update would create 3+ contradictions | Stop; present the situation to the researcher for direction |
| Same open question appears on 3+ pages | Batch-update all affected pages in a single edit pass |
