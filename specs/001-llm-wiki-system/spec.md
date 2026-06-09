# Feature Specification: LLM Wiki System

**Feature Branch**: `001-llm-wiki-system`

**Created**: 2026-06-08

**Status**: Draft

**Input**: User description: "Read @llm-wiki.md and implement a LLM wiki system."

## Clarifications

### Session 2026-06-08

- Q: How are wiki operations (ingest, query, lint) triggered? → A: Via dedicated Claude
  Code skills (slash commands). Skills are the authoring and maintenance interface; the
  web server (spec 002) is the read/browse interface. Clear separation: skills write,
  the web server serves.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ingest a Source (Priority: P1)

A knowledge worker drops a local file into `raw/` and runs `/wiki-ingest <path>`. The
skill reads the source, discusses key takeaways, writes a summary page, updates the index
and relevant entity/concept pages, and appends a log entry — all without modifying the
raw source.

**Why this priority**: Ingestion is the primary growth mechanism of the wiki. Without it,
no knowledge accumulates. Every other operation depends on content having been ingested.

**Independent Test**: Drop a markdown article into `raw/`, run `/wiki-ingest <path>`, and
verify: (a) a new summary page appears in `wiki/`, (b) `index.md` lists the new page,
(c) `log.md` has a new entry referencing the source path, (d) the raw file is unchanged.

**Acceptance Scenarios**:

1. **Given** a markdown article in `raw/articles/`, **When** the user runs
   `/wiki-ingest raw/articles/article.md`, **Then** a summary page is created in `wiki/`
   with at least one citation to the raw path.
2. **Given** a PDF in `raw/papers/`, **When** the user runs `/wiki-ingest <path>`,
   **Then** the system extracts key information, writes a summary page, and updates at
   least one entity or concept page that the PDF references.
3. **Given** a source already ingested, **When** a revised version is placed in `raw/`
   and `/wiki-ingest` is run again, **Then** the wiki page is updated and any contradiction
   between old and new content is explicitly flagged.
4. **Given** a raw source that contradicts an existing wiki claim, **When** ingest
   completes, **Then** the contradiction is flagged on the affected wiki page — not
   silently overwritten.

---

### User Story 2 - Query the Wiki (Priority: P2)

A user runs `/wiki-query "<question>"` to ask a natural language question against the
accumulated knowledge base. The skill reads the index to identify relevant pages,
synthesizes a cited answer, and offers to file the response back into the wiki as a new
page so insights compound over time.

**Why this priority**: Querying is the primary way users extract value from the wiki.
Without it the wiki is write-only.

**Independent Test**: With at least 3 ingested sources, run `/wiki-query "<question>"`.
Verify: (a) the answer cites specific wiki pages, (b) the response is richer than any
single source provides, (c) the user can accept filing the answer as a new wiki page.

**Acceptance Scenarios**:

1. **Given** a wiki with multiple pages on a topic, **When** the user runs
   `/wiki-query "<question>"`, **Then** the response cites at least two wiki pages and
   synthesizes across them.
2. **Given** a question whose answer spans three sources, **When** queried, **Then** the
   answer is deeper than any individual summary page provides.
3. **Given** a valuable query response, **When** the user accepts filing it, **Then** a
   new wiki page is created and `index.md` is updated to include it.
4. **Given** a question about a topic not yet in the wiki, **When** queried, **Then** the
   skill clearly indicates which aspects are missing rather than hallucinating coverage.

---

### User Story 3 - Lint / Health-Check the Wiki (Priority: P3)

The user runs `/wiki-lint` to health-check the wiki. The skill scans for contradictions,
stale claims, orphan pages, and missing entity pages. It produces a structured report in
the terminal and appends a lint entry to `log.md`.

**Why this priority**: Without periodic linting, the wiki silently degrades as it grows.
Lint is what keeps the knowledge base trustworthy over time.

**Independent Test**: With a known contradiction between two wiki pages, run `/wiki-lint`
and verify the contradiction appears in the report. Verify orphan pages are listed.

**Acceptance Scenarios**:

1. **Given** two wiki pages with contradicting claims, **When** the user runs
   `/wiki-lint`, **Then** both pages are listed in the contradiction section of the report.
2. **Given** a wiki page with no inbound links, **When** `/wiki-lint` runs, **Then** it
   is listed as an orphan page in the report.
3. **Given** a concept mentioned across five pages but lacking its own page, **When**
   `/wiki-lint` runs, **Then** the skill recommends creating an entity page for it.
4. **Given** a lint pass completes, **Then** a timestamped entry is appended to `log.md`.

---

### User Story 4 - Browse and Navigate the Wiki (Priority: P4)

A user browses the wiki in a web browser — navigating between pages, following
cross-links, and reading rendered content. The web server (spec `002-content-search-media`)
serves the wiki. The skill layer ensures every ingest and query operation keeps `index.md`
current so the browser view is always up to date.

**Why this priority**: Browsability is what makes the wiki useful day-to-day. The skill
layer creates and maintains the content; the web server makes it readable.

**Independent Test**: After running `/wiki-ingest` on a new source, open the wiki in a
browser and verify the new page appears in the index and all cross-links resolve.

**Acceptance Scenarios**:

1. **Given** a wiki with 10+ pages, **When** the user opens the wiki in a browser,
   **Then** every page is listed in `index.md` with a link and a one-line summary
   organized by category.
2. **Given** an entity page, **When** the user reads it, **Then** it contains cross-links
   to at least one related concept or source page.
3. **Given** any wiki page, **When** the user follows a cross-link, **Then** the linked
   page exists and contains relevant content.

---

### Edge Cases

- What happens when a raw source is unreadable (corrupted PDF, broken video transcript)?
- How does the system handle a source that is 100% duplicate of an already-ingested one?
- What if the index grows so large it exceeds the LLM's context window?
- How are sources in languages other than English handled?
- What happens when `/wiki-ingest` is run with a path that does not exist in `raw/`?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST maintain three isolated layers: raw sources (immutable),
  wiki (LLM-written markdown), and schema/system configuration (human-controlled).
- **FR-002**: Raw sources MUST be preserved as local copies in a designated `raw/`
  directory. Supported formats include: markdown, HTML, PDF, images, and plain-text
  transcripts. URL-only references are NOT sufficient.
- **FR-003**: The wiki layer MUST be entirely LLM-managed via Claude Code skills. The user
  MUST NOT be required to manually edit wiki pages for normal operation.
- **FR-004**: The system MUST maintain an `index.md` file that catalogs every wiki page
  with: a relative link, a one-line summary, and a category tag. The skill MUST update it
  on every ingest and every filed query response.
- **FR-005**: The system MUST maintain a `log.md` file as an append-only chronological
  record of all operations (ingest, query, lint) with timestamps and source references.
  Each entry MUST use a parseable prefix format (e.g., `## [2026-06-08] ingest | Title`).
- **FR-006**: Ingest MUST produce at least one new or updated wiki page per source, with
  at least one citation to the local `raw/` path of that source.
- **FR-007**: The system MUST explicitly flag contradictions between sources on the
  affected wiki pages rather than silently resolving them.
- **FR-008**: Lint passes MUST detect and report: contradictions, orphan pages (no inbound
  links), stale claims, and missing cross-references for well-known entities.
- **FR-009**: Query responses MUST cite their sources (wiki pages or raw source paths).
  Valuable query responses MUST be fileable back into the wiki as new pages via a single
  user confirmation in the skill interaction.
- **FR-010**: All workflows MUST be fully documented in the project schema file (`CLAUDE.md`)
  so a new agent session can operate without external state.
- **FR-011**: The system MUST require only: git, local file storage, a `raw/` directory,
  and a Claude Code environment. No external databases or embedding infrastructure required
  by default.
- **FR-012**: Large binary files in `raw/` (PDFs, images, videos) MAY be excluded from
  git history (via `.gitignore` or Git LFS) but MUST exist on local disk.
- **FR-013**: The system MUST expose three Claude Code skills as the primary authoring
  interface: `/wiki-ingest`, `/wiki-query`, and `/wiki-lint`.
- **FR-014**: `/wiki-ingest <path-or-url>` MUST accept a local `raw/` file path as its
  argument, execute the full ingest workflow, and report the path of the resulting wiki
  page on completion.
- **FR-015**: `/wiki-query "<question>"` MUST accept a natural language question, read
  the index, synthesize a cited answer from relevant wiki pages, and offer a single
  confirmation prompt to file the answer as a new wiki page.
- **FR-016**: `/wiki-lint` MUST run a full health check and output a structured report
  with findings grouped by category: contradictions, orphan pages, stale claims, and
  missing entity pages. It MUST append a timestamped entry to `log.md`.

### Key Entities

- **Raw Source**: An immutable local file in `raw/` — the ground truth. Has a local path,
  format type, and ingest status.
- **Wiki Page**: An LLM-generated markdown file. Has a title, category, creation date,
  source citations, and cross-links to other wiki pages.
- **Index Entry**: A record in `index.md` for each wiki page — link, summary, category.
- **Log Entry**: A timestamped, append-only record in `log.md` documenting an operation
  triggered by a skill.
- **Schema File**: `CLAUDE.md` — defines wiki structure, page conventions, citation
  format, and skill workflow procedures.
- **Wiki Skill**: A Claude Code slash command (`/wiki-ingest`, `/wiki-query`,
  `/wiki-lint`) that triggers an LLM-driven wiki operation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can run `/wiki-ingest <path>` and see a new wiki page with citations
  appear in the browser within a single session, without manually editing any files.
- **SC-002**: After ingesting 10 sources across different categories, a user can navigate
  from the index to any page in 2 browser clicks or fewer.
- **SC-003**: `/wiki-query` on a question spanning 3+ sources produces a synthesized
  answer that cites the specific wiki pages used — not just the raw sources.
- **SC-004**: `/wiki-lint` on a wiki with 20+ pages produces a report identifying all
  known contradictions and orphan pages.
- **SC-005**: Any claim in the wiki can be traced back to its originating raw source file
  by following citations — provenance is 100% verifiable for ingested content.
- **SC-006**: A new Claude Code session can resume wiki operations using only the
  repository and the `raw/` directory — no additional setup required.
- **SC-007**: Log entries are parseable with standard unix tools — e.g.,
  `grep "^## \[" log.md | tail -5` returns the 5 most recent skill operations.

## Assumptions

- The primary LLM agent is Claude Code; skills are implemented as Claude Code slash
  commands documented in `.claude/skills/`.
- Workflows are documented in `CLAUDE.md` as the schema file so sessions are stateless.
- The web server from spec `002-content-search-media` is the browsing layer; spec 001
  covers only the skill-driven write/maintain operations.
- Sources are ingested one at a time by default; batch ingestion is out of scope for v1
  but the architecture MUST NOT prevent it.
- The wiki is a personal/team knowledge base; no authentication or multi-user access
  control is required.
- The initial wiki size is expected to reach ~100 sources and ~hundreds of pages before
  a dedicated search tool becomes necessary; `index.md` navigation via the web server is
  sufficient for v1.
- YouTube sources are handled as plain-text transcripts saved to `raw/`; video playback
  is not required.
- The system does not need to support real-time collaborative editing; sessions are
  sequential.
