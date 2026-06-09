---
name: wiki-lint
description: Health-checks the wiki for structural issues (orphaned pages, broken cross-references, missing frontmatter, stale or contested pages), surfaces findings with proposed fixes, and triggers macro self-evaluation at ingest milestones. Use after accumulating several sources, when wiki quality is in question, or to run a periodic health check.
---

# Wiki Lint Skill

Health-check the wiki for structural issues, surface findings with proposed fixes,
and trigger macro self-evaluation when the ingest count reaches a milestone.

**Trigger**: `/wiki-lint`

## When to use

Use this skill to maintain wiki quality after accumulating several sources, or
whenever the researcher suspects broken cross-references, stale pages, or missing
index entries. Also used to trigger the macro self-evaluation cycle.

## Prerequisites

- `wiki/index.md` exists
- `wiki/` directory exists with at least one page

---

## Steps

### Step 1 — Build page inventory

Read `wiki/index.md`. Extract every wiki page path listed. Build:
- A set of **index-listed slugs** (paths in `wiki/index.md`)
- A set of **filesystem slugs** (files actually present under `wiki/`)

Use Bash `find wiki/ -name "*.md" -not -path "wiki/meta/*"` to enumerate
filesystem slugs without reading file contents yet.

---

### Step 2 — Scan all pages

Read every page found in Step 1. For each page, extract:
- All YAML frontmatter fields (`title`, `type`, `sources`, `status`, `created`,
  `last_updated`)
- All outbound `[[wiki/...]]` cross-references
- The `sources[]` array (raw filenames cited)
- Key claims and named entities mentioned

Track inbound link counts per page across the full scan.

---

### Step 3 — Run lint checks

#### L-001: Orphan (filesystem)
Flag any page file that has no entry in `wiki/index.md`.

#### L-002: Orphan (index)
Flag any `wiki/index.md` entry whose path does not exist on the filesystem.

#### L-003: Missing frontmatter
Flag any page missing one or more required fields: `title`, `type`, `sources`,
`status`, `created`, `last_updated`.

#### L-004: Broken sources
Flag any page whose `sources[]` lists a filename not present in `raw/`.

#### L-005: Broken cross-references
Flag any `[[wiki/...]]` link in a page that points to a path that does not exist.

#### L-006: Stale pages
Flag pages with `status: stale`.

#### L-007: Contested without Dispute section
Flag pages with `status: contested` that have no `## Dispute` section.

#### L-008: No-source pages
Flag pages with `sources: []` (informational only).

#### L-009: Missing entity pages
Identify named entities (companies, models, systems, teams) mentioned across ≥3
pages that have no dedicated `wiki/entities/` page. These are gaps worth filling.

---

### Step 4 — Classify all issues

Combine all findings into three groups:

- **Error**: L-001, L-002, L-003, L-004, L-005
- **Warning**: L-006, L-007
- **Info**: L-008, L-009

---

### Step 5 — Generate lint report

Output a structured summary:

```markdown
## Lint Report — [YYYY-MM-DD]

| Severity | Count |
|---|---|
| Error    | N     |
| Warning  | N     |
| Info     | N     |

### Errors
- `wiki/concepts/ranking.md`: L-003 missing-frontmatter (missing: status)
- `wiki/entities/acme.md`: L-005 broken cross-ref → wiki/concepts/nonexistent.md

### Warnings
- `wiki/sources/old-report.md`: L-006 stale

### Info
- `wiki/synthesis/overview.md`: L-008 no-sources
- "Experiment Framework" mentioned in 4 pages; no entity page exists (L-009)
```

If there are zero issues, output:

```markdown
## Lint Report — [YYYY-MM-DD]

Wiki is healthy. No errors, warnings, or info items found.
```

---

### Step 6 — Propose fixes

For each Error or Warning, propose one or two concrete options:

| Issue | Proposed fixes |
|---|---|
| L-001 orphan (filesystem) | (A) Add index entry, or (B) Delete the orphaned page |
| L-002 orphan (index) | Remove the dangling index entry |
| L-003 missing frontmatter | Add default values for missing fields |
| L-004 broken sources | (A) Remove invalid filename from `sources[]`, or (B) locate correct file in `raw/` |
| L-005 broken cross-ref | (A) Remove the broken `[[...]]` ref, or (B) create a stub page at the target path |
| L-006 stale | Re-ingest the original source using `/wiki-ingest` |
| L-007 contested, no Dispute | Add a `## Dispute` section summarising the conflicting claims |

---

### Step 7 — Apply fixes (if researcher confirms)

For each Error where the researcher confirms a fix:

1. Read the affected wiki page.
2. Apply the fix (edit frontmatter, remove broken ref, add index entry, etc.).
3. Update `wiki/index.md` if entries were added or removed.
4. Write the updated file.

Do not modify Warning or Info items unless the researcher explicitly requests it.

---

### Step 8 — Macro self-evaluation trigger

Count ingest-only log entries (lines matching `## [YYYY-MM-DD] ingest |`) in `wiki/log.md`.
Read `wiki/meta/evaluations.md` to find the `ingest-count-at-trigger:` value from
the most recent macro evaluation entry (or 0 if none).

**Trigger condition**: current count is a multiple of 10 AND current count > last
trigger count.

**When triggered**, append a macro evaluation to `wiki/meta/evaluations.md`:

```markdown
## [YYYY-MM-DD] Evaluation — macro-N-sources
ingest-count-at-trigger: N

| Dimension      | Score           | Target                    | Notes |
|---|---|---|---|
| Token Economy  | On/Below Target | ≤8 reads/ingest           | avg N reads across last 10 ingests |
| Wiki Health    | On/Below Target | 0 unresolved errors       | N errors found this lint pass |
| Ingest Quality | On/Below Target | ≥80% update ≥2 pages      | N/10 sources updated ≥2 pages |
| Query Yield    | On/Below Target | ≥50% queries filed back   | N/M queries filed back |
| Coverage Gaps  | On/Below Target | ≤2 open questions/query   | avg N open questions |

**Highest-impact improvement**: <proposed action and rationale>
```

Also log: `## [YYYY-MM-DD] evaluation | macro-N-sources`

---

### Step 9 — Log entry

Append to `wiki/log.md`:

```
## [YYYY-MM-DD] lint | <N errors, N warnings, N info>
```

---

## Token budget

- 1 read: `wiki/index.md`
- N reads: all wiki pages (bounded by wiki size; read all for correctness)
- 1 read: `wiki/log.md` (for macro trigger count)
- 1 read: `wiki/meta/evaluations.md` (macro eval only)
- Total target: proportional to wiki size; flag if >20 pages read in a single pass
