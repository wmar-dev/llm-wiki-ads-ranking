# Wiki Index

## Experimentation & A/B Testing

- [Overlapping Experiment Infrastructure: More, Better, Faster Experimentation](wiki/sources/overlapping-experiment-infrastructure.md) — Google's layered A/B testing system (KDD 2010); introduces domains/layers/launch layers and supporting tools for running thousands of simultaneous experiments

## Auction Mechanisms & Pricing

- [What Is a Second Price Auction?](wiki/synthesis/second-price-auction.md) — Vickrey/GSP auction mechanics, incentive compatibility, revenue equivalence, and relevance to ads ranking systems [status: current] [sources: 1]
- [Internet Advertising and the GSP Auction](wiki/sources/edelman-ostrovsky-schwarz-gsp-auction.md) — Edelman, Ostrovsky & Schwarz (AER 2007); proves GSP lacks dominant-strategy truthfulness but has a unique locally envy-free equilibrium with VCG-equivalent payoffs [status: current] [sources: 1] [source_type: peer_reviewed]
- [Generalized Second-Price Auction (GSP)](wiki/concepts/generalized-second-price-auction.md) — multi-slot auction mechanism used in search advertising; bid × quality score ranking; locally envy-free equilibrium [status: current] [sources: 1]
- [Google Ad Rank and LTV Scoring](wiki/concepts/google-ad-rank-ltv-scoring.md) — production Ad Rank system: LTV = eCPM - costs (pCTR, pCQ, pLQ); thresholds, reserve pricing, rGSP, Smart Bidding [status: draft] [sources: 2]
- [What Are Vickrey and GSP Auctions?](wiki/synthesis/vickrey-and-gsp.md) — Vickrey second-price auction (1961) and Generalized Second-Price auction for multi-slot ad allocation; incentive compatibility, locally envy-free equilibrium, production differences [status: current] [sources: 2]

## Machine Learning at Scale

- [The Unreasonable Effectiveness of Data](wiki/sources/unreasonable-effectiveness-of-data.md) — Halevy, Norvig & Pereira (IEEE Intelligent Systems 2009); argues simple models + lots of data outperform complex models + less data; foundational paper for web-scale learning [status: current] [sources: 1] [source_type: peer_reviewed] [processing_status: processed] [ingest_count: 1]
- [Web-Scale Learning](wiki/concepts/web-scale-learning.md) — paradigm of training ML on naturally occurring large-scale data; threshold of sufficient data; memorization at scale [status: draft] [sources: 2]

## Ad Ranking & Delivery

- [How Meta Ad Ranking Works](wiki/synthesis/meta-ad-ranking.md) — Meta's 2026 ads ranking: 5-system stack (Andromeda, Lattice, GEM, UTIS, ARM); creative-first neural retrieval; unified cross-surface ranking; foundation model teacher-student architecture; GSP auction [status: current] [sources: 3]
- [Meta Ads Ranking System](wiki/entities/meta-ads-ranking-system.md) — entity overview of Meta's 5-system architecture, auction equation, targeting inversion, and infrastructure [status: draft] [sources: 3]
- [Meta Adaptive Ranking Model](wiki/sources/meta-adaptive-ranking-model.md) — Meta Engineering blog on ARM: request-centric computation, selective FP8 quantization, multi-card GPU sharding for O(1T) parameter models [status: current] [sources: 1] [source_type: other]
- [Meta's Generative Ads Model (GEM)](wiki/sources/meta-gem-ads-foundation-model.md) — Meta Engineering blog on the GEM foundation model teacher with knowledge distillation to downstream models [status: current] [sources: 1] [source_type: other]
- [The Meta Ads Algorithm in 2026](wiki/sources/meta-ads-algorithm-2026-guide.md) — practitioner analysis of 5-system stack, auction equation, targeting inversion, learning phase, and campaign structure [status: draft] [sources: 1] [source_type: blog_post]
- [How Reddit Ads Work](wiki/synthesis/reddit-ads.md) — Reddit's second-price auction, community-based targeting, MAX AI campaigns, pricing, and delivery [status: current] [sources: 3]
- [Reddit Ads System](wiki/entities/reddit-ads-system.md) — entity overview of Reddit's auction, targeting (community/interest/keyword), bidding, and campaign structure [status: draft] [sources: 3]
- [How Reddit Advertising Works](wiki/sources/reddit-ads-how-it-works.md) — practitioner guide: auction mechanics, ranking factors, bidding strategies, learning phase [status: draft] [sources: 1] [source_type: blog_post]
- [Reddit Max Campaigns](wiki/sources/reddit-max-campaigns.md) — official Reddit announcement: AI-powered fully automated campaigns with Community Intelligence [status: current] [sources: 1] [source_type: other]
- [Reddit Audience Targeting](wiki/sources/reddit-audience-targeting.md) — official documentation: community, interest, and keyword targeting; custom audiences; funnel mapping [status: current] [sources: 1] [source_type: other]

## Recommendation Systems

- [How the TikTok Recommendation Algorithm Works](wiki/synthesis/tiktok-recommendation-algorithm.md) — two-stage pipeline (candidate generation + ranking); unsupervised clustering + embeddings; implicit signal-driven feedback loop; exploration vs exploitation [status: current] [sources: 3]
- [How TikTok Recommends Content](wiki/sources/tiktok-recommender-system.md) — TikTok official documentation on recommender signals (user interactions, content info, user info) [status: current] [sources: 1] [source_type: other]
- [How TikTok's Algorithm Really Works](wiki/sources/tiktok-unsupervised-algorithm-deep-dive.md) — unsupervised learning engine behind FYP; embeddings, Monolith real-time training, two-stage architecture [status: draft] [sources: 1] [source_type: blog_post]

## Sources

- [Overlapping Experiment Infrastructure](wiki/sources/overlapping-experiment-infrastructure.md) — Google's layered A/B testing system (KDD 2010) [status: current] [sources: 1] [source_type: peer_reviewed] [processing_status: processed] [ingest_count: 1]
- [Internet Advertising and the GSP Auction](wiki/sources/edelman-ostrovsky-schwarz-gsp-auction.md) — Edelman, Ostrovsky & Schwarz (AER 2007) [status: current] [sources: 1] [source_type: peer_reviewed]
- [The Unreasonable Effectiveness of Data](wiki/sources/unreasonable-effectiveness-of-data.md) — Halevy, Norvig & Pereira (IEEE Intelligent Systems 2009) [status: current] [sources: 1] [source_type: peer_reviewed] [processing_status: processed] [ingest_count: 1]
- [How TikTok Recommends Content](wiki/sources/tiktok-recommender-system.md) — TikTok official documentation on recommender signals [status: current] [sources: 1] [source_type: other]
- [How TikTok's Algorithm Really Works](wiki/sources/tiktok-unsupervised-algorithm-deep-dive.md) — unsupervised learning engine behind FYP [status: draft] [sources: 1] [source_type: blog_post]
- [How Search Ads are Ranked and Priced on Google](wiki/sources/google-ad-rank-briefing.md) — Google's internal briefing paper to UK CMA (submitted in DOJ case); reveals LTV scoring formula, thresholds, rGSP, and pricing mechanics [status: current] [sources: 1] [source_type: other] [processing_status: processed] [ingest_count: 1]
- [Meta Adaptive Ranking Model](wiki/sources/meta-adaptive-ranking-model.md) — Meta Engineering: request-centric ARM, selective FP8, multi-card GPU sharding for O(1T) parameter models [status: current] [sources: 1] [source_type: other] [processing_status: processed] [ingest_count: 1]
- [Meta's Generative Ads Model (GEM)](wiki/sources/meta-gem-ads-foundation-model.md) — Meta Engineering: GEM foundation model teacher with knowledge distillation [status: current] [sources: 1] [source_type: other] [processing_status: processed] [ingest_count: 1]
- [The Meta Ads Algorithm in 2026](wiki/sources/meta-ads-algorithm-2026-guide.md) — practitioner guide: 5-system stack, auction equation, targeting inversion [status: draft] [sources: 1] [source_type: blog_post] [processing_status: processed] [ingest_count: 1]
- [How Reddit Advertising Works](wiki/sources/reddit-ads-how-it-works.md) — practitioner guide: auction mechanics, ranking factors, bidding strategies, learning phase [status: draft] [sources: 1] [source_type: blog_post] [processing_status: processed] [ingest_count: 1]
- [Reddit Max Campaigns](wiki/sources/reddit-max-campaigns.md) — Reddit Inc: AI-powered fully automated MAX campaigns with Community Intelligence [status: current] [sources: 1] [source_type: other] [processing_status: processed] [ingest_count: 1]
- [Reddit Audience Targeting](wiki/sources/reddit-audience-targeting.md) — Reddit Business: official targeting guide with Community, Interest, Keyword + custom audiences [status: current] [sources: 1] [source_type: other] [processing_status: processed] [ingest_count: 1]
