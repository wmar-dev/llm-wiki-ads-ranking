# Feature Specification: Content Search, Metrics & Multi-Format Media Ingestion

**Feature Branch**: `002-content-search-media`

**Created**: 2026-06-08

**Status**: Draft

**Input**: User description: "The content must be searchable, keep page visit metrics,
consume webpages, pdfs, images, podcasts, YouTube videos, generate SVG from dot diagrams"

**Depends on**: `001-llm-wiki-system` (core LLM wiki system)

## Clarifications

### Session 2026-06-08

- Q: What serves the wiki and triggers visit records? → A: A web server that renders and
  serves the markdown files so wiki pages are viewable in a browser; page visit = HTTP
  request to a page URL, logged by the web server.
- Q: Podcast transcript — user-supplied or auto-generated? → A: Both: if a transcript
  file is provided alongside the audio, use it; if only audio is provided, prompt the user
  to supply a transcript before proceeding. Audio-only ingest without a transcript blocks
  with a clear message rather than silently failing.
- Q: Webpage ingestion — static HTML only or JS-rendered support? → A: Use a headless
  browser (Playwright) to render pages so JS-heavy and single-page-app URLs are fully
  supported. Static fetch is not the limiting factor.
- Q: Search result ranking signal? → A: BM25 scoring (term frequency × inverse document
  frequency, normalized by page length) — industry-standard full-text ranking that handles
  term density and avoids over-rewarding long pages.
- Q: HTTP access log size management? → A: Rotate when the active log exceeds a size
  threshold (e.g., 10 MB); archive old segments with consistent naming so all historical
  data remains queryable. No manual size management required from the user.

### Session 2026-06-08 (continued)

- Q: YouTube transcript acquisition — URL auto-download or user-provided file? → A: URL
  only — the system auto-downloads the transcript from a YouTube URL using yt-dlp. Users
  provide the YouTube URL; no manual transcript download step is required.
- Q: Paywall/login-wall handling during webpage ingest? → A: Detect common login-wall
  signals, abort with a clear error message, and prompt the user to provide an alternative
  (e.g., saved HTML file). No wiki page is created from a login wall.
- Q: Search index persistence across server restarts? → A: SQLite — the BM25 index is
  stored in a SQLite database file, persists across server restarts, and requires no
  rebuild on startup.
- Q: Page visit metrics — do asset requests (images, SVGs) count as visits? → A: No —
  only requests for wiki HTML pages are counted. Static asset requests are excluded from
  the metrics report.
- Q: Large source sectioning — automatic or interactive? → A: Automatic — system splits
  at fixed boundaries (~50 pages per pass for PDFs; ~30-minute segments for video) and
  processes all sections in one unattended pass. No user confirmation between sections.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Serve the Wiki via Web Browser (Priority: P1)

A user wants to browse the wiki in a standard web browser — navigating between pages,
following cross-links, and reading rendered content — without installing any special editor
or viewer. The web server renders markdown files to HTML and serves them at a local URL.
SVG diagrams, images, and other assets are served alongside the pages.

**Why this priority**: The web server is the primary viewing mechanism for all other
features. Search, metrics, and SVG viewing all depend on the wiki being browser-accessible.

**Independent Test**: Start the web server, open a browser, navigate to the index page,
follow a cross-link to a second page, and verify the content renders correctly (headings,
links, SVG images if present).

**Acceptance Scenarios**:

1. **Given** the web server is running, **When** a user opens a browser and navigates to
   the wiki's root URL, **Then** the `index.md` is rendered as an HTML page with clickable
   links to all wiki pages.
2. **Given** a wiki page with cross-links, **When** the user clicks a link, **Then** the
   linked page loads in the browser without requiring any file system access.
3. **Given** a wiki page containing a generated SVG diagram, **When** the user views it in
   the browser, **Then** the SVG renders inline on the page.
4. **Given** a wiki page with a local image citation (from `raw/images/`), **When** viewed
   in the browser, **Then** the image is displayed inline (served from the web server, not
   from an external URL).
5. **Given** the web server is running, **When** a user navigates to a page that does not
   exist, **Then** a clear 404 page is displayed with a link back to the index.

---

### User Story 2 - Ingest Multi-Format Sources (Priority: P2)

A knowledge worker wants to add sources that are not plain markdown — webpages, PDFs,
images, podcast audio, and YouTube videos. The system accepts each format, extracts the
text/visual content, saves a local copy in `raw/`, and integrates the knowledge into the
wiki. Once ingested, new wiki pages are immediately accessible via the web server.

**Why this priority**: Ingest is the primary growth mechanism. All wiki content originates
from ingested sources.

**Independent Test**: Ingest one source of each type (webpage, PDF, image, podcast
transcript, YouTube URL) and verify: (a) a local copy exists in `raw/`, (b) a wiki
summary page is created with a citation to the local path, (c) the new page is accessible
via the web server, (d) `index.md` is updated and served correctly.

**Acceptance Scenarios**:

1. **Given** a webpage URL (static or JS-rendered), **When** the user triggers ingest,
   **Then** the page is fetched via headless browser, content is saved locally in
   `raw/web/`, a summary page is written to `wiki/`, the citation references the local
   file (not just the URL), and the new page is browsable via the web server.
2. **Given** a PDF file, **When** ingested, **Then** the text content is extracted, a
   summary page is created, the PDF is stored in `raw/papers/` or `raw/docs/`, and the
   page is browsable via the web server.
3. **Given** an image file, **When** ingested, **Then** the system describes the visual
   content, a summary page is written with the description, the image is stored in
   `raw/images/`, and it renders inline when the summary page is viewed in a browser.
4. **Given** a podcast audio file with a transcript provided, **When** ingested, **Then**
   the transcript is saved to `raw/podcasts/` and the wiki page summarizes key topics and
   timestamps. **Given** a podcast audio file with no transcript, **When** the user
   triggers ingest, **Then** the system prompts for a transcript and does not proceed until
   one is supplied.
5. **Given** a YouTube video URL, **When** ingested, **Then** yt-dlp auto-downloads the
   transcript, it is saved locally in `raw/videos/`, and a wiki summary is created with
   chapter-level breakdowns where available.
6. **Given** any source format, **When** ingest completes, **Then** the log entry notes the
   source format type alongside the title and timestamp.

---

### User Story 3 - Search Wiki Content via Browser (Priority: P3)

A user wants to search for a keyword or phrase across all wiki pages from within the
browser. They type a query into a search interface served by the web server and see ranked
results with excerpts — clicking a result navigates directly to the matching page.

**Why this priority**: Search is how users find content that can't easily be located by
browsing as the wiki grows. Being browser-accessible makes it the natural first stop.

**Independent Test**: With a 20+ page wiki, use the browser search interface to find a
term known to appear in 3 pages. Verify results list those pages ranked by relevance with
excerpts, and clicking a result navigates to the correct page.

**Acceptance Scenarios**:

1. **Given** the web server is running, **When** a user navigates to the search page or
   uses the search bar, **Then** they can type a query and submit it without leaving the
   browser.
2. **Given** a keyword search, **When** results are returned, **Then** they are ranked by
   relevance with a one-sentence excerpt per result showing the match in context.
3. **Given** a multi-word query, **When** searched, **Then** pages matching all query terms
   rank above pages matching only some.
4. **Given** a search with zero results, **When** the results page loads, **Then** the
   system states no pages were found and suggests related terms if possible.
5. **Given** a search result, **When** the user clicks it, **Then** they navigate to the
   matching wiki page in the browser.

---

### User Story 4 - Track Page Visit Metrics (Priority: P4)

The web server automatically records which wiki pages are accessed and how often via HTTP
request logging. A user can view a metrics report in the browser showing the most-visited
pages, zero-visit pages (candidate orphans), and visit trends — informing decisions about
where to invest in deeper coverage or linting.

**Why this priority**: HTTP-level visit tracking requires no user action and produces
accurate, real-time data about which knowledge is actively used.

**Independent Test**: Access three specific wiki pages in a browser (some multiple times),
then open the metrics report page. Verify each page's visit count matches the number of
browser requests made.

**Acceptance Scenarios**:

1. **Given** a user requests a wiki page in their browser, **When** the web server serves
   it, **Then** an HTTP access log entry is recorded with the page URL and timestamp.
2. **Given** accumulated access logs, **When** the user navigates to the metrics report
   page, **Then** they see: total HTTP requests per page, most-visited pages ranked, and
   pages with zero requests flagged.
3. **Given** the metrics report, **When** cross-referenced with the lint report, **Then**
   pages flagged as orphans AND with zero HTTP visits are highlighted as highest priority
   for review or deletion.
4. **Given** a page is removed from the wiki, **When** the metrics are checked, **Then**
   its visit history is preserved in the archived access log rather than discarded.

---

### User Story 5 - Generate SVG Diagrams from Dot Notation (Priority: P5)

When wiki pages describe relationships, workflows, or architectures, a dot-notation diagram
can be rendered as an SVG and served by the web server so diagrams are visible inline in
the browser. The dot source is preserved for future edits.

**Why this priority**: Certain knowledge is better communicated visually. SVG is natively
supported by all browsers, requires no plugins, and integrates seamlessly with HTML pages.

**Independent Test**: Provide a dot diagram, trigger rendering, then open the wiki page in
a browser. Verify the SVG diagram renders inline without plugins and that the dot source is
accessible alongside it.

**Acceptance Scenarios**:

1. **Given** a dot-notation diagram associated with a wiki page, **When** rendered,
   **Then** an SVG file is produced and served by the web server from the assets directory.
2. **Given** an SVG is generated, **When** the user views the wiki page in a browser,
   **Then** the diagram is visible inline on the page — no download or plugin required.
3. **Given** a dot diagram with a syntax error, **When** the user attempts to render it,
   **Then** the error is reported on the page and no partial SVG is saved.
4. **Given** an updated dot diagram (source changed), **When** re-rendered, **Then** the
   SVG is replaced and the wiki page in the browser reflects the updated diagram on next
   load.

---

### Edge Cases

- What happens when the web server is started but the `wiki/` directory is empty?
- When a webpage requires login or is behind a paywall: the system detects common
  login-wall signals, aborts ingest with a clear error message, and prompts the user to
  supply an alternative (e.g., a locally saved HTML file). No wiki page is created.
- How does the system handle a podcast with no available transcript?
- How are images in languages the system cannot read handled?
- What if a dot diagram references external fonts not available locally?
- How are very large PDFs (200+ pages) handled without exhausting token budgets?
- Access logs rotate at a size threshold; all archived segments are included in the metrics
  report — verified by checking that deleted-page visit counts persist across rotations.
- How are concurrent browser requests to the same page handled?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST include a web server that serves wiki markdown files rendered
  as HTML pages, accessible in any standard web browser at a local URL.
- **FR-002**: The web server MUST serve all wiki assets alongside pages: generated SVG
  files, locally stored images, and other referenced media from `raw/images/`.
- **FR-003**: The web server MUST serve a 404 page with a link back to the index when a
  requested page does not exist.
- **FR-004**: The system MUST support ingestion of: webpages (rendered via headless browser,
  saved as local files), PDFs (text extracted), images (described), podcast audio
  (transcript saved locally), and YouTube videos (transcript auto-downloaded via yt-dlp
  and saved locally). All ingested pages MUST be immediately accessible via the web server
  after ingest.
- **FR-005**: For every ingested source, a local copy MUST be saved in `raw/` under a
  format-appropriate subdirectory before any wiki page is written.
- **FR-006**: The ingest log entry in `log.md` MUST record the source format type alongside
  the title and timestamp.
- **FR-007**: The web server MUST provide a search interface accessible in the browser.
  Search MUST return results ranked by BM25 score (term frequency × inverse document
  frequency, normalized by page length), with excerpt snippets showing the match in
  context and clickable links to the matching page.
- **FR-008**: The search index MUST cover wiki pages only (not raw sources), MUST be stored
  in a SQLite database file that persists across server restarts, and MUST be incrementally
  updatable after each ingest without a full rebuild.
- **FR-009**: The web server MUST log all HTTP requests for wiki HTML pages. Static asset
  requests (images, SVGs, CSS) MUST NOT be counted as page visits. Each access log entry
  MUST include: the page URL and a timestamp.
- **FR-010**: The web server MUST serve a metrics report page showing: total HTTP request
  count per wiki page, most-visited pages ranked, and pages with zero requests flagged.
- **FR-011**: HTTP access log records for deleted wiki pages MUST be archived, not
  discarded, so historical visit patterns remain queryable.
- **FR-017**: The HTTP access log MUST rotate automatically when it exceeds a configured
  size threshold (default: 10 MB). Rotated segments MUST be archived with consistent,
  sortable naming (e.g., `access.log.001`, `access.log.002`). All archived segments MUST
  remain queryable for the visit metrics report.
- **FR-012**: The system MUST accept Graphviz dot notation and produce a valid SVG file
  served by the web server from the wiki's assets directory.
- **FR-013**: The dot source MUST be preserved alongside the generated SVG so diagrams
  remain editable and re-renderable.
- **FR-014**: Wiki pages that include a dot diagram MUST render the SVG inline when viewed
  in the browser.
- **FR-015**: Podcast ingestion MUST accept either a pre-provided transcript file or an
  audio file. If only audio is provided with no transcript, the system MUST prompt the user
  to supply a transcript before proceeding — it MUST NOT silently skip the ingest or
  produce a wiki page without source text. The transcript MUST be saved in `raw/podcasts/`.
- **FR-016**: Large sources (PDFs > 50 pages, long videos) MUST be automatically split at
  fixed section boundaries (~50 pages per pass for PDFs; ~30-minute segments for video)
  and processed in a single unattended pass. No user confirmation between sections is
  required. Section boundaries MUST be noted in the wiki summary page.
- **FR-018**: Webpage ingest MUST detect common login-wall and paywall signals (e.g., login
  form present, content length significantly below expected, known paywall patterns). When
  detected, ingest MUST abort with a clear error message naming the URL and prompting the
  user to supply content via an alternative method (e.g., locally saved HTML). No wiki page
  MUST be written from a login-wall response.

### Key Entities

- **Web Server** — the process serving the wiki at a local URL; renders markdown to HTML,
  serves assets, handles search queries, and logs HTTP access events.
- **Source** — an ingested artifact with: local path, format type (webpage/PDF/image/
  podcast/video), ingest timestamp, and wiki page link.
- **Transcript** — a text representation of audio or video content, saved in `raw/` and
  cited by the corresponding wiki page.
- **Search Index** — a SQLite database storing the BM25 term index mapping terms to wiki
  page paths and excerpt positions; persists across server restarts; queried by the web
  server's search interface.
- **Search Result** — a ranked match containing: page title, relative URL, relevance
  score, and excerpt.
- **HTTP Access Log** — append-only record of web server page requests; each entry has
  page URL and timestamp.
- **Visit Metrics Report** — a web page generated from the HTTP access log showing
  aggregated request counts per page, ranked list, and zero-visit pages.
- **Dot Source** — a plain-text Graphviz dot diagram saved alongside a wiki page.
- **SVG Asset** — the rendered diagram saved in the wiki's assets directory and served
  by the web server.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The web server starts and serves the wiki index page in a browser within
  5 seconds of launch, with no installation required beyond running a single start command.
- **SC-002**: A user can ingest sources of all five supported formats and immediately view
  the resulting wiki page in a browser — no manual file-system steps required.
- **SC-003**: A keyword search via the browser search interface across a 50-page wiki
  returns relevant results in under 3 seconds, with the correct page ranked first for an
  unambiguous single-term query.
- **SC-004**: The visit metrics report page accurately reflects the number of HTTP requests
  per page — counts are verifiable against the raw access log file.
- **SC-005**: A valid dot diagram produces an SVG that renders inline in the browser
  without any plugins or browser extensions.
- **SC-006**: Ingesting a 50-page PDF produces a wiki summary covering all major sections
  without exceeding a single ingest session's token budget.
- **SC-007**: After a wiki page is deleted, its historical HTTP request count remains
  queryable from the archived access log.

## Assumptions

- The web server runs locally (localhost); public internet hosting is out of scope for v1.
- Podcast ingestion accepts either a pre-provided transcript or an audio-only file. When
  only audio is provided, the system prompts the user to supply a transcript rather than
  silently failing or attempting transcription internally. Real-time in-session audio
  transcription is out of scope.
- YouTube videos are ingested via URL; yt-dlp auto-downloads the transcript before ingest.
  Video streaming is not served by the web server.
- Search is powered by a BM25 full-text index stored in SQLite over local wiki files;
  embedding-based vector search is out of scope for v1 but the architecture must not
  prevent it.
- Webpage ingestion uses a headless browser (Playwright) to render pages before saving
  locally; Playwright must be installed in the environment.
- Dot diagram rendering requires a local Graphviz installation or equivalent accessible to
  the ingest pipeline; cloud rendering APIs are not assumed.
- Image ingestion relies on the system's multimodal capability to describe image content.
- The feature assumes the core wiki system (`001-llm-wiki-system`) is in place: `raw/`,
  `wiki/`, `index.md`, `log.md`, and the schema file all exist.
- The web server need not support HTTPS, user authentication, or concurrent multi-user
  sessions for v1.
