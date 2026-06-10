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

## [2026-06-09] query | why ads have auctions | pages-read: 5 | sources-ingested: 0

Full coverage from existing wiki pages on GSP auction theory (Edelman et al., AER 2007) and Google Ad Rank mechanics. No web enrichment needed. Created synthesis page (wiki/synthesis/why-ads-have-auctions.md) covering scarcity, perishing inventory, price discovery, and why fixed prices fail.

## [2026-06-09] query | what is pinterest's foundation model | pages-read: 0 | sources-ingested: 2

Total gap — no existing wiki pages on Pinterest. Enriched with 2 sources: PinFM paper (RecSys 2025, peer-reviewed) and Pinterest Engineering blog on request-level deduplication (industry report). Created 2 source summaries (wiki/sources/pinfm-foundation-model-pinterest.md, wiki/sources/pinterest-request-level-deduplication.md) and synthesis page (wiki/synthesis/pinterest-foundation-model.md). Key finding: PinFM is a 20B+ param transformer pretrained on user activity data; uses DCAT for 600% throughput; underpins Pinterest's broader foundation model ecosystem (PinRec, UniPinRec, TransActV2).

## [2026-06-09] query | what are two tower or factorized models | pages-read: 4 | sources-ingested: 2

Partial gap — existing pages mentioned two-tower/multi-tower models in passing (TikTok, Reddit, Meta) but lacked a standalone architecture definition. Enriched with 2 web sources (EngineersOfAI tutorial, Google Cloud reference architecture). Created synthesis page (wiki/synthesis/two-tower-factorized-models.md). Key finding: two-tower models solve billion-scale retrieval via the architectural constraint of independent user/item towers enabling precomputed embeddings + ANN search; the "factorized" name derives from deep-learning generalization of matrix factorization.

## [2026-06-09] ingest | Ranking Engineer Agent (REA): Meta's Autonomous Ads Ranking Optimizer

Fetched from Meta Engineering blog (engineering.fb.com); saved to raw/web/meta-ranking-engineer-agent-rea.md. Created source summary (wiki/sources/meta-ranking-engineer-agent-rea.md). Key finding: autonomous AI agent with dual-source hypothesis engine and three-phase planning (Validation → Combination → Exploitation) doubled average model accuracy across six models.

## [2026-06-09] query | how do you know your auction or ranking is optimal | pages-read: 5 | sources-ingested: 1

Partial gap — existing pages covered theoretical auction optimality (GSP equilibrium, VCG comparison) and general A/B testing well, but lacked systematic treatment of empirical optimality verification (offline metrics like AucLoss, progressive validation, counterfactual evaluation, and automated optimization). Enriched with Meta REA blog post. Created synthesis page (wiki/synthesis/how-to-know-optimality.md) with a 6-layer hierarchy: theory → offline metrics → counterfactual eval → A/B testing → systematic optimization → business outcomes.

## [2026-06-09] lint | 2 errors, 0 warnings, 16 info

L-001: 2 banner-blindness source pages missing from index. L-009: 16 entity gaps (Andromeda, ARM, Bootstrap, FTRL-Proximal, GEM, Google, Lattice, MAX, Meta, Monolith, Reddit, Smart Bidding, TikTok, UTIS, VCG, rGSP). No stale or contested pages. No broken cross-refs or sources.

## [2026-06-09] ingest | Digital Ad Formats: IAB Taxonomy and Format Types

Fetched from Epom blog (epom.com); saved to raw/web/digital-ad-formats-epom.md. Created source summary (wiki/sources/digital-ad-formats-epom.md) and synthesis page (wiki/synthesis/types-of-ads.md) covering 9 ad formats with pricing, performance benchmarks, and platform mappings.

## [2026-06-09] query | what types of ads are there | pages-read: 4 | sources-ingested: 1

Partial gap — existing wiki had scattered ad-type information across platform-specific pages (search GSP, Meta feed ads, Reddit promoted posts, banner blindness) but no comprehensive taxonomy. Enriched with IAB taxonomy from Epom guide. Created synthesis page (wiki/synthesis/types-of-ads.md) with Mermaid format tree, comparison tables by format x pricing x performance, and platform mapping.

## [2026-06-09] query | does google shopping ads have a vertical classification | pages-read: 0 | sources-ingested: 1

Total gap — no existing wiki pages on Google Shopping or product taxonomy. Enriched with Google Merchant Center help page. Created source summary (wiki/sources/google-product-taxonomy.md) and synthesis page (wiki/synthesis/google-shopping-vertical-classification.md). Key finding: Google Shopping uses a ~6,000+ category hierarchical taxonomy with 20+ top-level verticals; auto-assignment from product signals, per-category bid management, and versioned taxonomy updates.

## [2026-06-09] answer | UTIS engagement, ARM expansion, GEM scaling, sequential testing, network interference | pages-updated: 2 | sources-ingested: 4

Answered 5 open questions. See entry above.

## [2026-06-09] query | what is semantic id | pages-read: 3 | sources-ingested: 1

Partial gap — existing wiki had passing mentions of Meta's Entity IDs (visual clustering) but no coverage of Semantic IDs as a retrieval paradigm. Enriched with TIGER paper (NeurIPS 2023), FORGE benchmark (Taobao production), and GRID framework (Snap Research). Created source summary and synthesis page. Key finding: SIDs enable generative retrieval by quantizing content embeddings into discrete codeword tuples; similar items share overlapping tokens; used in production at Taobao (250M+ items); cold-start generalization is a key advantage over traditional dense retrieval.

## [2026-06-09] ingest | Monolith: Real Time Recommendation System With Collisionless Embedding Table

Fetched from arXiv (2209.07663) via ar5iv HTML conversion; saved to raw/web/monolith-realtime-recommendation-system.md. Single-pass processing (2,441 words). Source type: peer_reviewed (ORSUM@ACM RecSys 2022). Created source summary (wiki/sources/), entity page for Monolith system (wiki/entities/), and two concept pages: online training for recommendation systems (wiki/concepts/) and collisionless embedding table (wiki/concepts/). Key findings: Cuckoo hash-based collisionless embedding improves AUC vs hash-trick approaches; minute-level parameter sync achieves 79.80 AUC (Criteo) vs 79.43 batch-only; 14–18% AUC improvement in production A/B test. No contradictions with existing pages that reference Monolith (TikTok blog post, TikTok synthesis).

## [2026-06-09] ingest | Better Generalization with Semantic IDs: A Case Study in Ranking for Recommendations

Fetched from arXiv HTML (2306.08121v2). ~7,000 words processed as single pass (chunking not needed despite threshold — dense references section). Source type: peer_reviewed (arXiv, Google/Google DeepMind). Created source summary (wiki/sources/). Updated existing synthesis page (wiki/synthesis/semantic-id.md) with SID ranking model section covering n-gram vs SPM adaptation methods and key findings from YouTube production experiments. No contradictions with existing TIGER source or Semantic ID page — this paper is complementary, covering ranking (not generative retrieval) use of SIDs. Key finding: SPM-based SID tokenization outperforms fixed N-gram for large-scale ranking models on cold-start generalization.

## [2026-06-09] query | what is rgsp | pages-read: 4 | sources-ingested: 1

Partial gap — existing pages (google-ad-rank-ltv-scoring, google-ad-rank-briefing, vickrey-and-gsp, generalized-second-price-auction) all named rGSP (launched Jan 2019) but stated the randomization logic was undocumented. Fetched Search Engine Land's explainer of DOJ trial testimony/exhibits from US v. Google. Created source summary (wiki/sources/rgsp-randomized-second-price-explained.md), new concept page (wiki/concepts/randomized-gsp-rgsp.md, closing the entity gap flagged in the last lint run), and synthesis answer page (wiki/synthesis/rgsp.md). Key findings: rGSP randomizes the slot winner among bidders with close LTV scores rather than always picking the top-ranked ad; winner pays next-highest qualifying bid + $0.01; DOJ claims advertisers must bid ~3.7x higher to avoid randomization, citing a ~10% revenue increase since the Jan 2019 launch. Updated google-ad-rank-ltv-scoring.md's Pricing section and Related Pages with a link to the new concept page. No contradictions — pure enrichment of a previously-undocumented mechanism. Left the existing "rGSP vs. GSP equilibrium" open question in place (only partially answered — formal equilibrium-theoretic treatment of the randomization remains unaddressed in any source reviewed).

## [2026-06-09] ingest | Fatigue-Aware Ad Creative Selection (Moriwaki et al., arXiv 2019)

Fetched abstract/landing page from arXiv (1908.08936); saved to raw/web/fatigue-aware-ad-creative-selection.md. Single-pass (abstract-level only — full PDF not fetched). Source type: peer_reviewed. Created source summary (wiki/sources/). Key finding: contextual bandit for DSP ad creative selection that folds wear-in/wear-out exposure history into the bandit's context; outperformed baselines on most KPIs in production.

## [2026-06-09] ingest | Dynamic Ad Allocation: Bandits with Budgets (arXiv 2013)

Fetched abstract/landing page from arXiv (1306.0155); saved to raw/web/dynamic-ad-allocation-bandits-with-budgets.md. Single-pass. Source type: peer_reviewed. Created source summary (wiki/sources/). Key finding: budgeted extension of UCB1 for pay-per-click ad allocation with per-ad spend caps, with provable regret bounds vs. an optimal allocation.

## [2026-06-09] ingest | Comparison Lift: Bandit-Based Experimentation System for Online Advertising (arXiv 2020)

Fetched abstract/landing page from arXiv (2009.07899); saved to raw/web/comparison-lift-bandit-experimentation.md. Single-pass. Source type: peer_reviewed. Created source summary (wiki/sources/), cross-linked to existing confidence-interval-methods.md and how-ab-tests-work.md. Key finding: JD.com's Comparison Lift platform replaces fixed-sample A/B allocation with adaptive bandit reallocation for ad campaign tests — 1,500+ experiments, +46% avg CTR, +27% extra clicks during testing vs. fixed A/B.

## [2026-06-09] query | how are bandit algorithms used in ad systems | pages-read: 2 | sources-ingested: 3

Total gap — wiki had only passing mentions of bandits (TikTok's fixed-ratio exploration/exploitation, and a brief note on Bayesian methods for bandits in confidence-interval-methods.md). Read tiktok-recommendation-algorithm.md and confidence-interval-methods.md (partial). Fetched and ingested 3 arXiv sources covering the three main production application areas: ad creative selection under fatigue (contextual bandit), budget allocation (budgeted UCB1 with regret bounds), and bandit-based experimentation as an A/B test alternative (JD.com Comparison Lift). Created 1 new concept page (multi-armed-bandit-algorithms.md) and 1 synthesis page (bandit-algorithms-in-ad-systems.md) with a Graphviz explore/exploit-loop diagram. Contrasted formal bandit policies against TikTok's fixed exploration ratio. One Lyft-related claim (contextual budgeting via Thompson Sampling) could not be sourced after a failed fetch (PDF + Semantic Scholar both failed) — flagged as an open question rather than cited.

## [2026-06-09] answer | privacy/signal-loss training data, FTRL rare features, RL bidder equilibria, PinFM vs TransActV2, TikTok watch-time/well-being + DSA auditability, jackknife vs delta method | pages-updated: 6 | sources-ingested: 5

Answered 7 open questions (Q30/Q31 shared one source) across 6 pages, from a researcher-selected subset of the ~recommended 6 most-answerable questions out of 38 found. Ingested: "Statistical Learning from Attribution Sets" (arXiv 2602.06276) → unreasonable-effectiveness-of-data.md (privacy APIs degrade label precision, not "free" data availability, if estimators are corrected); "Approximating Auction Equilibria with Reinforcement Learning" (arXiv 2410.13960) → why-ads-have-auctions.md (RL bidders converge to classical first-/second-price equilibria, no collusion found); "TransAct V2" (Pinterest, arXiv 2506.02267) → pinterest-foundation-model.md (new lifelong-sequence subsection; +13.31% offline HIT@3/repin); EPRS "Addictive Design on Online Platforms" → tiktok-recommendation-algorithm.md (Feb 2026 EU DSA preliminary breach finding answers both the watch-time/well-being and DSA-auditability questions); Gottlieb (2003, arXiv math/0301363) → jackknife-method.md (jackknife and delta method asymptotically equivalent for smooth ratio metrics; delta method dominates at n > 10^6). The FTRL rare-feature question on ad-click-prediction-view-from-the-trenches.md was answered from the already-ingested McMahan et al. source, no new ingestion needed. The PinFM-vs-TransActV2 question was answered by establishing that no published head-to-head comparison exists. Step 3 duplicate check: ripgrep across wiki/ for the original open-question phrasings found no other pages containing the same questions — no batch edits needed.

## [2026-06-09] query | what are the different bidding types | pages-read: 4 | sources-ingested: 2

Partial gap — existing pages covered pricing models (CPM/CPC/CPA/CPV in types-of-ads.md), Google's Smart Bidding strategies (google-ad-rank-ltv-scoring.md), Reddit's manual/automatic bidding (reddit-ads.md), and second-price/GSP theory (vickrey-and-gsp.md), but lacked oCPM/Cost-Cap-style automated bidding and any treatment of first-price auctions in programmatic RTB. Fetched and ingested 2 sources: TikTok's official bidding guide (oCPM, Cost Cap, Maximum Delivery) and a Setupad explainer of the first-price vs. second-price shift driven by header bidding. Created synthesis page (wiki/synthesis/bidding-types.md) organizing bidding into three independent axes — pricing model, bid strategy, and auction-clearing mechanism — with a Graphviz diagram. No open questions answered in source pages read.

## [2026-06-09] query | what is ad pacing | pages-read: 2 | sources-ingested: 2

Total gap — wiki had only passing mentions of "pacing" (Reddit's Standard/Accelerated delivery setting, a budget-pacing open question in bandit-algorithms-in-ad-systems.md, and a one-line mention in two-tower-factorized-models.md). Read bandit-algorithms-in-ad-systems.md and dynamic-ad-allocation-bandits-with-budgets.md for related context. Fetched and ingested 2 arXiv sources via ar5iv: "A Practical Guide to Budget Pacing Algorithms in Digital Advertising" (2025, control-theoretic survey: throttling vs. bid modulation via PID/MPC/dual online gradient descent) and "Smart Pacing for Effective Online Ad Campaign Optimization" (Xu et al., KDD 2015, Yahoo — production layered-pacing system, 67-79% eCPC reduction). Created synthesis page (wiki/synthesis/ad-pacing.md) with a Graphviz control-loop diagram, distinguishing pacing (spend-over-time control) from bidding (per-auction price) and budgeted bandits (which-arm-to-show), and connecting Reddit's Standard/Accelerated pacing UI to the smooth-vs-accelerated delivery framing in the literature. Left the existing bandit/pacing open question in bandit-algorithms-in-ad-systems.md in place (only partially addressed — new sources cover a Yahoo DSP, not Google/Meta/Reddit specifically).

## [2026-06-10] query | how does youtube shorts recommendation work | pages-read: 3 | sources-ingested: 3

Total gap — wiki had no page on YouTube's recommendation architecture or Shorts. Read semantic-id.md, better-generalization-semantic-ids-ranking.md, and two-tower-factorized-models.md, which only mentioned YouTube in passing (Semantic IDs in its ranking model, and as the two-tower architecture's pioneer). Fetched and ingested 3 sources: Covington, Adams & Sargin's foundational 2016 RecSys paper "Deep Neural Networks for YouTube Recommendations" (candidate-generation/ranking dichotomy, expected-watch-time objective, "example age" freshness feature); a 2026 overview "How the YouTube Algorithm Works (5 Systems Explained)" (Home/Suggested/Search/Subscriptions/Shorts as separate systems; Shorts' explore & exploit promotion model; 2025 satisfaction-weighted discovery shift); and a 2026 Mediacube practitioner guide to Shorts-specific ranking signals (swipe/skip rate, rewatch/loop count, engagement actions, watch-history personalization, promotion mechanism). Created synthesis page (wiki/synthesis/youtube-shorts-recommendation.md) with a Graphviz diagram contrasting the long-form candidate-generation/ranking funnel against the Shorts explore-and-exploit loop, a comparison table of ranking signals, and a comparison to TikTok's FYP. No existing open questions answered (none of the read pages had open questions specific to YouTube/Shorts recommendation architecture).

## [2026-06-10] query | what is VCG | pages-read: 5 | sources-ingested: 1

Partial gap — the wiki references VCG repeatedly as a comparison point against GSP (vickrey-and-gsp.md, second-price-auction.md, generalized-second-price-auction.md, edelman-ostrovsky-schwarz-gsp-auction.md, how-to-know-optimality.md) but never explained the VCG mechanism itself. Read all 5 of those pages. Fetched and ingested the Wikipedia "Vickrey-Clarke-Groves mechanism" page (source_type: other), covering the Clarke pivot payment rule (payment = externality imposed on others), dominant-strategy truthfulness, allocative efficiency, single-item reduction to Vickrey, and practical limitations (budget imbalance, NP-hard combinatorial computation, collusion vulnerability). Created synthesis page (wiki/synthesis/what-is-vcg.md) with a Graphviz diagram illustrating the Clarke pivot "with vs. without bidder" externality computation, and a VCG-vs-GSP comparison table. No open questions in the read pages were fully answered (existing open questions concern ML quality-score calibration and RTB generalization, not the VCG mechanism itself).

## [2026-06-10] query | what is a conversion | pages-read: 3 | sources-ingested: 1

Partial gap — "conversion"/CPA/CVR/pCVR/attribution were referenced across many pages (bidding-types.md, google-ad-rank-ltv-scoring.md, statistical-learning-attribution-sets.md, llatte-scaling-laws-recommendation.md, reddit-max-campaigns-trajectory.md) but never defined as a standalone concept. Read bidding-types.md, statistical-learning-attribution-sets.md, and google-ad-rank-ltv-scoring.md. Fetched and ingested Google's official "About conversions" Ads Help page (source_type: official_documentation): conversion definitions (website/app/call/offline/imported), tracking mechanisms (tags, app SDKs, call forwarding, Enhanced Conversions/Conversion API), attribution windows, and the link to Smart Bidding. Created new "Conversion Tracking & Attribution" index section and synthesis page (wiki/synthesis/what-is-a-conversion.md) with a Graphviz pipeline diagram (impression -> conversion event -> tracking -> attribution -> pCVR -> Smart Bidding -> Ad Rank), distinguishing conversions (demand-side bid input) from Ad Rank (supply-side allocation). No existing open questions fully answered.

## [2026-06-10] query | how does google analytics work | pages-read: 1 | sources-ingested: 2

Total gap — the wiki had no page on Google Analytics/GA4. Read the freshly created what-is-a-conversion.md (which already referenced GA4 as a conversion-import source) for context. Fetched and ingested 2 official Google Analytics Help pages: "How Google Analytics 4 Collects Data" (gtag.js/GTM/Firebase SDK collection, enhanced measurement, recommended/custom events) and "GA4 BigQuery Export Schema" (events_YYYYMMDD/intraday tables, event_params/user_properties/items records; predictive purchase/churn scores; gclid join to Google Ads click data). Created new synthesis page (wiki/synthesis/how-does-google-analytics-work.md) with a Graphviz architecture diagram (collection -> GA4 event model -> reports/BigQuery export -> predictive scores -> Google Ads conversion import/audiences/Smart Bidding), framing GA4 as the measurement layer upstream of conversion tracking and Ad Rank. Flagged the data-driven-attribution claim as an inference since it came from aggregated WebSearch results rather than the two primary fetched docs, which didn't cover attribution models in depth — left as an open question for future verification. No existing open questions answered (no prior GA-related pages existed).

## [2026-06-10] query | what is the latency budget for ad ranking | pages-read: 5 | sources-ingested: 1

Partial gap — the wiki already had substantial scattered latency data (two-tower-factorized-models.md's per-stage pipeline table: ~20ms retrieval / ~10ms pre-rank / ~50-80ms ranking; meta-ad-ranking.md's Meta-vs-Google comparison: 200-300ms vs ~100ms; meta-adaptive-ranking-model.md's "sub-second latency" via ARM) but no unified treatment, and no industry-wide (open RTB) reference point. Read meta-adaptive-ranking-model.md, two-tower-factorized-models.md, meta-ad-ranking.md, google-ctr-prediction-system.md, and pinterest-request-level-deduplication.md. Fetched and ingested a practitioner blog post on RTB latency budgets (source_type: blog_post): ~80-120ms auction cycle (industry standard 100-300ms incl. RTT), broken into network/exchange/DSP-compute(~50ms)/aggregation/return, plus OpenRTB's hard 408-timeout cutoff. Created synthesis page (wiki/synthesis/what-is-the-latency-budget-for-ad-ranking.md) with a Graphviz pipeline diagram, a cross-system comparison table, and an explicit link back to what-is-vcg.md (VCG's NP-hard combinatorial computation is infeasible within this budget, motivating GSP). No existing open questions fully answered.

## [2026-06-10] query | what are the components of an ad ranking system | pages-read: 5 | sources-ingested: 0

Full coverage — after 14 pages read across this session's earlier queries plus 5 new pages this query (bandit-algorithms-in-ad-systems.md, ad-pacing.md, how-ab-tests-work.md, contextual-relevance-advertising.md, why-ads-have-auctions.md), the wiki already documents every major subsystem of an ad ranking pipeline (retrieval/two-tower, pCTR/pCVR ranking, contextual relevance/quality scoring, Ad Rank/GSP/rGSP auction, Smart Bidding, pacing, conversion tracking & attribution, bandit-based exploration, layered A/B-test experimentation, and the ~100ms latency budget) — no new ingestion was needed. Created an overview synthesis page (wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md) as the new lead entry in the "Ad Ranking & Delivery" index section, with a Graphviz architecture diagram (3 clusters: online serving pipeline, bidding & delivery control, feedback & learning loop) and a 10-row component summary table linking each component to its deep-dive page; `sources:` frontmatter cites the 10 underlying raw sources backing the synthesized claims per the project's no-empty-sources convention. Two open questions carried over (unresolved) from ad-pacing.md and bandit-algorithms-in-ad-systems.md regarding pacing/bid-strategy unification and bandit-based exploration inside Smart Bidding — neither is answered by this overview, so no Step 7 edits were made to those pages.

## [2026-06-10] query | why does google charge per click while meta charges per impression | pages-read: 5 | sources-ingested: 1

Partial gap — the wiki had thorough mechanics on pricing models (bidding-types.md), Google's eCPM/LTV formula (google-ad-rank-ltv-scoring.md), and Meta's Total Value formula (meta-ad-ranking.md), plus general auction rationale (why-ads-have-auctions.md, what-is-a-conversion.md), but no page addressed the historical/economic "why" behind CPC-vs-CPM as platform defaults. Re-read bidding-types.md, google-ad-rank-ltv-scoring.md, and meta-ad-ranking.md (plus reused why-ads-have-auctions.md and what-is-a-conversion.md from this session). Fetched and ingested a MarTech industry explainer (source_type: blog_post) covering CPM's 1995-96 origin (Netscape/Infoseek/DoubleClick) vs CPC's 1998 Goto.com origin (adopted by Google in 2002), a risk-allocation framing (CPM = advertiser bears the risk of unproductive impressions; CPC = platform bears it), and the eCPM normalization formula (eCPM = CPC x pCTR x 1000, etc.) that lets any auction compare CPM/CPC/CPA bids on one scale. Created synthesis page (wiki/synthesis/why-does-google-charge-per-click-while-meta-charges-per-impression.md) with a Graphviz diagram contrasting Google Search's CPC/high-intent lineage against Meta Feed's CPM/discovery lineage, both converging on an eCPM-equivalent auction currency, plus a summary table and a note on oCPM/Smart Bidding as the bridge between billing unit and auction currency. Per Step 7, removed the now-answered open question from bidding-types.md ("how does the effective CPM an advertiser pays under oCPM relate to the platform's internal per-impression auction price") and added a Related Pages link to the new synthesis.

## [2026-06-10] query | how much fraud is there in Meta ads | pages-read: 3 | sources-ingested: 3

Total gap — none of the existing Meta pages (meta-ads-ranking-system.md, meta-ad-ranking.md, meta-ads-algorithm-2026-guide.md, all read this query) addressed fraud, scam ads, or platform-trust enforcement. Fetched and ingested 3 sources: Meta's own H1 2026 Transparency Center Integrity Reports (source_type: official_documentation; 159M scam ads removed in 2025, 92% proactive, 10.9M scam-center accounts removed, 344K+ "nudify" app ads removed); a Lawfare legal-analysis writeup of a late-2025 Reuters investigation based on cached internal Meta documents (source_type: news_article; ~10%/$16B of 2024 revenue projected from scam/banned-goods ads, $3.5B/6mo from "higher legal risk" ads, 95%-confidence ban threshold with "penalty bid" mechanism for sub-threshold advertisers, China as top scam-exporting nation at ~25% of global volume / ~$3B of Meta's $18B China ad revenue); and a PPC Land report on the April 21, 2026 Consumer Federation of America class action (source_type: news_article; ~15B "higher-risk" scam ads/day, $7B/year annualized high-risk revenue, 134M scam ads removed in 2025, 96% of fraud reports ignored/incorrectly rejected). Created new "Ad Fraud & Platform Trust" index section, a concept page (wiki/concepts/scam-ads-and-ad-fraud.md) distinguishing scam-ad vs. click-fraud categories and framing stock-vs-flow measurement, and the synthesis page (wiki/synthesis/meta-ad-fraud.md) with a Graphviz diagram of the fraud-scoring/penalty-bid enforcement funnel and a matplotlib chart script comparing the revenue figures. Flagged a contradiction (Step 6) between Meta's 159M and the CFA complaint's 134M scam-ads-removed-in-2025 figures — documented as a Dispute section in wiki/sources/meta-integrity-report-h1-2026-fraud-scams.md rather than marking either page `contested`, since both numbers may be accurate under different definitions/scopes and only 2 of 3 new sources are involved (not the ≥3 needed for `contested`). Added a "Fraud, Scams & Enforcement" section to wiki/entities/meta-ads-ranking-system.md linking the auction mechanism to the penalty-bid incentive problem. No existing open questions were answered by this query (none of the 3 read pages had fraud-related open questions); 3 new open questions were added to the new synthesis/concept pages instead.

## [2026-06-10] query | what is ad rank | pages-read: 4 | sources-ingested: 0

Full coverage — the wiki already had deep, directly-on-topic material: google-ad-rank-ltv-scoring.md (the canonical LTV = eCPM - costs formula and component definitions), randomized-gsp-rgsp.md and rgsp.md (rGSP randomization layer and DOJ findings), google-ad-rank-briefing.md (primary source: DOJ exhibit UPX0010), and generalized-second-price-auction.md (textbook GSP theory), plus this session's what-is-vcg.md, vickrey-and-gsp.md, what-is-a-conversion.md, how-does-google-analytics-work.md, and why-does-google-charge-per-click-while-meta-charges-per-impression.md for the VCG/GSP comparison, demand-side bid inputs, and Meta's Total Value contrast — no new ingestion needed. Created wiki/synthesis/what-is-ad-rank.md (exact filename required to resolve forward-references already placed in what-is-a-conversion.md and how-does-google-analytics-work.md), with a Graphviz pipeline diagram (bid/pCTR/pCQ/pLQ -> LTV -> eligibility -> rGSP -> Actual CPC), a "bid x quality_score vs. LTV" reformulation table, an Ad Rank/GSP/VCG comparison table, and a section on Meta's Total Value as the same conceptual family. `sources:` frontmatter cites 6 real underlying raw sources per the project's no-empty-sources convention. Added as the new entry immediately after google-ad-rank-ltv-scoring.md in the "Auction Mechanisms & Pricing" index section. Step 7: checked the 3 open questions each in randomized-gsp-rgsp.md and rgsp.md (LTV band width, randomization probability distribution, technical documentation existence) — none are resolved by this overview, so no edits were made to those pages. This completes all 7 questions queued in PROMPT.md.
