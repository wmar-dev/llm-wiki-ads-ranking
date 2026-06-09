# Ingest Log

- **2026-06-08** | `ingest` | `web` | [Contextual Relevance of Ads at Reddit](wiki/sources/contextual-relevance-of-ads-reddit.md) — [source](https://www.reddit.com/r/RedditEng/comments/1r0hyfu/contextual_relevance_of_ads_reddit/)
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

## [2026-06-08] ingest | Contextual Relevance of Ads at Reddit

Fetched from r/RedditEng via old.reddit.com (WebFetch on new.reddit.com blocked by verification). Single-pass processing (~2000 words). Source: Reddit Engineering blog by Daniel Peters, Aleksandr Plentsov, Anand Natu. Source type: other (company engineering blog). Created source summary (wiki/sources/contextual-relevance-of-ads-reddit.md), concept page (wiki/concepts/contextual-relevance-advertising.md), and updated existing entity (wiki/entities/reddit-ads-system.md) and synthesis (wiki/synthesis/reddit-ads.md). Key findings: LLM-as-judge with Gemini labels <post, ad> relevance; fine-tuned multi-tower embedding model achieves 3.2× PRAUC vs IAB taxonomy; relevance boost applied preferentially for search-referred high-intent traffic. No contradictions with existing pages.

## [2026-06-08] query | how do A/B tests work | pages-read: 1 | sources-ingested: 0

Partial coverage — existing wiki had 1 source on Google's overlapping experiment infrastructure. Web search retrieved methodology from Kohavi et al. (KDD 2013 survey), Tang et al. (KDD 2010 overlapping experiments), Deng et al. (Amazon A/B testing at scale — Wiley textbook). Enrichment URLs were PDF-only (WebFetch couldn't parse). Created synthesis page (wiki/synthesis/how-ab-tests-work.md) consolidating general A/B test methodology (randomization, hypothesis testing, OEC, sample sizing, A/A tests, CUPED, triggering) with Google's layered system as a large-scale case study. CUPED and sequential testing noted as open questions.

## [2026-06-08] query | what are methods for computing confidence intervals | pages-read: 2 | sources-ingested: 0

Partial coverage — existing wiki mentioned delta method and empirical carve-up in passing. Enrichment: fetched Deng et al. (2018) delta method paper from ar5iv HTML (Microsoft ExP, KDD 2018). Created synthesis page (wiki/synthesis/confidence-interval-methods.md) covering 9 methods: t-test/Wald, delta method, Fieller, Edgeworth expansion, bootstrap (3 variants: percentile/BCa/t), outer CI for quantiles, hybrid method, Bayesian credible intervals, and confidence sequences (mSPRT, AsympCS, design-based, SAVI). Includes decision flowcharts, method comparison table, and implementation notes. Open questions: width penalty of confidence sequences, adjustment for network interference.

## [2026-06-08] answer | confidence sequences width penalty + network interference CI adjustment | pages-updated: 1 | sources-ingested: 2

Answered 2 questions in confidence-interval-methods.md: (1) CS width penalty is unavoidable — LIL lower bound O(√(log log n/n)), but factor of ~2× in practice (Waudby-Smith et al., 2024); (2) Network interference CIs require cluster randomization, exposure modeling, or regression adjustment — no universal solution.

## [2026-06-08] answer | feedback loops, contextual relevance dominance, balancing relevance with trust | pages-updated: 1 | sources-ingested: 1

Answered 3 questions in contextual-relevance-of-ads-reddit.md: (1) Feedback loop bias amplified over cycles; self-play frameworks (SPRec) show promise but only 24/347 papers validated in dynamic settings; (2) Contextual relevance critical when privacy, brand safety, or full reach needed — within 5-8% of behavioral CTR at 30-40% lower CPM; (3) Balance requires user-centric formats, AI contextual targeting, and Acceptable Ads standards.

## [2026-06-08] answer | Reddit Max trajectory, conversation velocity, community targeting scale | pages-updated: 1 | sources-ingested: 1

Answered 2 of 3 questions in reddit-ads.md: Max following Advantage+ trajectory but with transparency differentiation; community targeting scalability remains partially unanswered (DAUq growing but below Meta/Google reach). Conversation velocity interaction with auction also partially unanswered.

## [2026-06-08] query | what is the jackknife method | pages-read: 1 | sources-ingested: 1

Total gap — no existing wiki pages on jackknife. Fetched 1 source (Wikipedia). Created source summary (wiki/sources/jackknife-resampling.md) and synthesis page (wiki/synthesis/jackknife-method.md). Key finding: leave-one-out resampling for bias and variance estimation; linear approximation of bootstrap; conservative variance estimates.

## [2026-06-08] ingest | How Search Ads are Ranked and Priced on Google

Downloaded 31 MB PDF from DOJ website (justice.gov); extracted 4,765 words via pdftotext. Single-pass processing. Source: Google's internal briefing paper to UK CMA (2020), submitted as Exhibit UPX0010 in US v. Google. Source type: other (regulatory filing). Created source summary (wiki/sources/google-ad-rank-briefing.md) and concept page (wiki/concepts/google-ad-rank-ltv-scoring.md). Updated existing GSP concept page and second-price synthesis page with rGSP and reserve pricing details. Key findings: LTV score uses cost-side terms (pCQ, pLQ) not present in theoretical GSP models; rGSP launched globally Jan 2019; reserve pricing applies when no competitor clears quality threshold. No contradictions — existing theoretical pages describe the idealized model; this source reveals the production implementation.

- **2026-06-09T06:51:34Z** | `webpage` | [Banner blindness - Wikipedia](raw/web/en-wikipedia-org-wiki-banner-blindness.html)
- **2026-06-09T06:51:38Z** | `webpage` | [Banner Blindness Revisited: Users Dodge Ads on Mobile and Desktop - NN/G](raw/web/www-nngroup-com-articles-banner-blindness-old-and-new-findings.html)
- **2026-06-09** | `query` | ad-blindness definition and mechanisms | pages-read: 2 | sources-ingested: 2

## [2026-06-08] ingest | Ad Click Prediction: a View from the Trenches (McMahan et al., KDD 2013)

Downloaded 1.2 MB PDF from Google Research; extracted 8,663 words via pdftotext. Chunked into 3 segments (2,973 + 2,993 + 2,697 words). Source: peer-reviewed (KDD 2013, ACM). Created source summary, entity pages (Google CTR Prediction System, FTRL-Proximal Algorithm), and updated web-scale-learning concept. Key findings: FTRL-Proximal combines OGD accuracy with RDA sparsity; per-coordinate learning rates reduce AucLoss by 11.2%; q2.13 encoding saves 75% RAM with no accuracy loss; uncertainty score provides cheap prediction confidence. No contradictions with existing pages.

## [2026-06-09] lint | 4 errors, 0 warnings, 13 info

Fixed 2 L-001 orphans (deleted raw webpage copies wrongly placed in wiki/). Remaining: 0 errors, 11 L-009 entity gaps (info). Macro evaluation not triggered (ingest count 5; needs multiple of 10).