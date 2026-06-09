<!--
Sync Impact Report
==================
Version change: N/A (initial authoring) → 1.0.0
Status: New constitution — all sections authored from template.

Principles added (5):
  I.   Content-System Isolation & Source Preservation
  II.  Token Economy
  III. Grounded Analysis & Provenance
  IV.  Quality Gates & Testing
  V.   Deployability & Documentation

Templates reviewed:
  ✅ plan-template.md    — Constitution Check gate compatible; no changes needed
  ✅ spec-template.md    — FR/SC format and acceptance scenario structure compatible
  ✅ tasks-template.md   — Testing discipline and documentation tasks align with Principle IV
  ✅ checklist-template.md — No conflicts

Deferred TODOs: none
-->

# LLM Wiki Constitution

## Core Principles

### I. Content-System Isolation & Source Preservation

The wiki MUST maintain strict separation across three immutable layers:

- **Raw sources** — human-curated, never modified by the LLM. Copies of ALL source
  materials (HTML, PDF, images, YouTube transcripts/videos, data files, etc.) MUST be
  preserved locally in a designated `raw/` directory. Large binaries MAY be excluded from
  git history (via `.gitignore` or Git LFS) but MUST still exist on disk and be referenced
  by their local path in the wiki. URLs to online sources alone are insufficient — the
  local copy is the authoritative source of truth.
- **The wiki** — LLM-written and LLM-maintained markdown. The LLM owns this layer entirely.
- **The system** — schema files, tooling, agent configuration. Human-approved and version-
  controlled. The system MUST NOT be modified during an ingest or query operation.

No layer may write to a layer above it. The LLM MUST NEVER modify raw sources.

**Rationale**: Source preservation ensures correctness can be verified against the original
artifact even if the online URL disappears. Strict layer isolation keeps the ground truth
auditable and the system configuration stable.

### II. Token Economy

All operations MUST be designed to minimize token consumption:

- Read `index.md` before scanning individual pages — never perform a full-corpus scan when
  targeted retrieval suffices.
- Batch all page updates for a single ingest into one pass; avoid re-reading content already
  in context.
- Prefer structured formats (tables, definition lists) over prose where information density
  is higher.
- Ingest operations MUST touch only the pages directly affected by the new source.

**Rationale**: Token cost grows with wiki size. Without discipline, operations become
prohibitively expensive. Economy is a first-class design constraint, not an afterthought.

### III. Grounded Analysis & Provenance

All wiki content MUST be factual and traceable:

- Every substantive claim MUST cite its local source path (e.g., `raw/papers/foo.pdf`).
- The LLM MUST prefer depth and synthesis over surface breadth — a well-reasoned page that
  integrates three sources outweighs three thin summaries.
- Contradictions between sources MUST be explicitly flagged on the relevant wiki page, not
  silently resolved.
- `log.md` MUST record every ingest, query, and lint operation with a timestamp and the
  source(s) involved, enabling full reconstruction of the wiki's evolution.
- Answers filed back into the wiki (from queries or analysis) MUST note that their primary
  source is prior wiki content, not raw sources directly.

**Rationale**: The wiki's value is reliable, compounding knowledge. Provenance makes every
claim independently verifiable and the wiki trustworthy over months and years.

### IV. Quality Gates & Testing

Quality MUST be enforced at three levels:

1. **Ingest validation** — each new source MUST produce at least one new or updated wiki
   page with at least one citation to the local source path.
2. **Lint passes** — periodic health checks MUST detect and report: contradictions between
   pages, orphan pages (no inbound links), stale claims superseded by newer sources, and
   missing cross-references to well-known entities.
3. **Schema compliance** — all generated pages MUST conform to the conventions in the
   project schema file. The schema MUST document at least: page structure, frontmatter
   fields, citation format, and index update procedure.

Workflows and schema conventions MUST have documented test scenarios so they can be
validated after any schema amendment.

**Rationale**: Without enforced gates the wiki degrades silently. Testing the system — not
only the content — ensures workflows remain correct as the schema evolves.

### V. Deployability & Documentation

The system MUST require only: git, markdown files, a local `raw/` directory, and an LLM
agent. No proprietary infrastructure, embedding databases, or external services are
required by default (optional tools such as a local search engine are additive, not
mandatory).

All workflows (ingest, query, lint) MUST be fully documented in the project schema file so
that a new agent session can continue without external state or tribal knowledge.
Deployment MUST be reproducible from the repository plus the local `raw/` directory alone.

**Rationale**: A system that requires specialized infrastructure or undocumented steps will
be abandoned. Simplicity and documentation are what make the wiki last.

## Operations

Approved workflows — each MUST be followed consistently and documented in the schema file:

- **Ingest**: Confirm local copy of source exists in `raw/` → read source → discuss key
  takeaways with user → write summary page (with citation) → update `index.md` → update
  relevant entity/concept pages → append entry to `log.md`. Touch only affected pages.
- **Query**: Read `index.md` → identify relevant pages → read them → synthesize answer
  with citations → file valuable answers back into the wiki as new pages.
- **Lint**: Scan for contradictions, orphan pages, stale claims, missing cross-references,
  and entity pages that should exist but don't. Propose new sources or questions to fill
  gaps. Append lint pass entry to `log.md`.

## Quality Checklist

Before closing any session, verify:

- [ ] All new or updated pages cite their local `raw/` source path
- [ ] Local copy of every new source exists in `raw/`
- [ ] `index.md` reflects current wiki state
- [ ] `log.md` has a timestamped entry for this session's operations
- [ ] No contradictions introduced without explicit flagging on the relevant page
- [ ] Token budget respected — no unnecessary full-corpus scans performed

## Governance

This constitution supersedes all other practices and conventions for this project.
Amendments require: (1) a documented rationale, (2) a version bump per the rules below,
and (3) propagation to all dependent templates.

All feature work MUST include a Constitution Check gate before implementation begins.
Complexity beyond what the principles permit MUST be explicitly justified in the plan.

Use the project schema file (e.g., `CLAUDE.md`) as the runtime development guidance
document — keep it synchronized with this constitution.

Version bump rules:

- **MAJOR**: A principle is removed, renamed, or fundamentally redefined in a backward-
  incompatible way.
- **MINOR**: A new principle or section is added, or existing guidance is materially
  expanded.
- **PATCH**: Clarifications, wording improvements, or non-semantic refinements.

**Version**: 1.0.0 | **Ratified**: 2026-06-08 | **Last Amended**: 2026-06-08
