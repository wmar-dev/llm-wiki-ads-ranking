# Ingest Log

- **2026-06-08** | `ingest` | `pdf` | [Overlapping Experiment Infrastructure: More, Better, Faster Experimentation](wiki/sources/overlapping-experiment-infrastructure.md) — [source](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36500.pdf)

## [2026-06-08] query | what is a second price auction? | pages-read: 0 | sources-ingested: 0

## [2026-06-08] ingest | Internet Advertising and the Generalized Second-Price Auction (Edelman, Ostrovsky, Schwarz 2007)

Fetched from NBER/Cramton mirror; saved to raw/web/edelman-ostrovsky-schwarz-gsp-auction.md. Created source summary (wiki/sources/), concept page (wiki/concepts/generalized-second-price-auction.md). Peer-reviewed (AER 2007). Key finding: GSP lacks dominant-strategy truthfulness but its locally envy-free equilibrium recovers VCG-level payoffs while generating higher platform revenue.

## [2026-06-08] ingest | The Unreasonable Effectiveness of Data

Fetched via web search (PDF not text-parseable); saved to raw/web/unreasonable-effectiveness-of-data.md. Created source summary (wiki/sources/) and concept page (wiki/concepts/web-scale-learning.md). Peer-reviewed (IEEE Intelligent Systems 2009). No contradictions found with existing pages. Key thesis: simple models + lots of data outperform complex models + less data.

## [2026-06-08] lint | 2 errors, 0 warnings, 0 info

Fixed L-003 (frontmatter standardized on overlapping-experiment-infrastructure.md) and L-005 (broken cross-ref in second-price-auction.md pointing to wrong path). Macro eval not triggered (ingest count=2, need multiple of 10).

## [2026-06-08] query | how does tiktok algorithm work | pages-read: 0 | sources-ingested: 3

Total gap — no existing wiki pages on TikTok. Fetched 3 sources (TikTok official docs, Kingy AI deep dive, DEV system design). Created 2 source summaries, 1 synthesis page (wiki/synthesis/tiktok-recommendation-algorithm.md). Key finding: unsupervised clustering + embeddings → two-stage candidate generation and ranking → real-time feedback loop.

## [2026-06-08] query | how do reddit ads work | pages-read: 0 | sources-ingested: 3

Total gap — no existing wiki pages on Reddit ads. Fetched 3 sources (Stackmatix practitioner guide, Reddit Inc Max Campaigns announcement, Reddit Business targeting guide). Created 3 source summaries, 1 entity page (wiki/entities/reddit-ads-system.md), 1 synthesis page (wiki/synthesis/reddit-ads.md). Key finding: Reddit uses a second-price auction with community-based targeting; AI-powered MAX Campaigns launched Jan 2026. Comparison table to Meta and Google added.

## [2026-06-08] query | what are vickrey and gsp | pages-read: 3 | sources-ingested: 0

Full coverage — read 3 existing pages (second-price-auction synthesis, GSP concept, Edelman et al. source summary). Created synthesis page (wiki/synthesis/vickrey-and-gsp.md) consolidating Vickrey vs GSP differences, production vs theory differences (LTV scoring, reserve pricing, rGSP from Google Ad Rank briefing), and relevance to ads ranking.

## [2026-06-08] query | how does meta ad ranking work | pages-read: 0 | sources-ingested: 3

Total gap — no existing wiki pages on Meta ad ranking. Fetched 3 sources (Meta Engineering: ARM + GEM; Greg Halno comprehensive guide). Created 3 source summaries, 1 entity page (wiki/entities/meta-ads-ranking-system.md), 1 synthesis page (wiki/synthesis/meta-ad-ranking.md). Key finding: Meta's 2026 stack uses 5 interlocking systems (Andromeda, Lattice, GEM, UTIS, ARM) with a teacher-student distillation architecture and creative-first neural retrieval.

## [2026-06-08] ingest | How Search Ads are Ranked and Priced on Google

Downloaded 31 MB PDF from DOJ website (justice.gov); extracted 4,765 words via pdftotext. Single-pass processing. Source: Google's internal briefing paper to UK CMA (2020), submitted as Exhibit UPX0010 in US v. Google. Source type: other (regulatory filing). Created source summary (wiki/sources/google-ad-rank-briefing.md) and concept page (wiki/concepts/google-ad-rank-ltv-scoring.md). Updated existing GSP concept page and second-price synthesis page with rGSP and reserve pricing details. Key findings: LTV score uses cost-side terms (pCQ, pLQ) not present in theoretical GSP models; rGSP launched globally Jan 2019; reserve pricing applies when no competitor clears quality threshold. No contradictions — existing theoretical pages describe the idealized model; this source reveals the production implementation.
