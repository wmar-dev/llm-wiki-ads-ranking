# Wiki Index

## Ad Blindness & User Behavior

- [Ad Blindness and Banner Blindness](wiki/synthesis/ad-blindness.md) — definition, mechanisms, triggers, mobile vs desktop, cognitive impact, and countermeasures for the phenomenon where users ignore perceived advertisements [status: current] [sources: 2]

## Auction & Ranking Optimality

- [How Do You Know Your Auction or Ranking Is Optimal?](wiki/synthesis/how-to-know-optimality.md) — theoretical, offline, counterfactual, online, and business-level criteria for assessing ranking/auction optimality [status: current] [sources: 5]

## Experimentation & A/B Testing

- [Overlapping Experiment Infrastructure: More, Better, Faster Experimentation](wiki/sources/overlapping-experiment-infrastructure.md) — Google's layered A/B testing system (KDD 2010); introduces domains/layers/launch layers and supporting tools for running thousands of simultaneous experiments
- [How A/B Tests Work](wiki/synthesis/how-ab-tests-work.md) — comprehensive overview: randomization, hypothesis testing, OEC, sample sizing, A/A tests, CUPED, triggering, overlapping/layered experiments, and common pitfalls [status: current] [sources: 1]
- [Methods for Computing Confidence Intervals in A/B Testing](wiki/synthesis/confidence-interval-methods.md) — decision framework for CI method selection: t-test/Wald, delta method, Fieller, bootstrap (BCa/percentile/t), outer CI for quantiles, hybrid method, Bayesian credible intervals, confidence sequences (mSPRT, AsympCS, design-based, SAVI), and CUPED [status: current] [sources: 1]
- [The Jackknife Method](wiki/synthesis/jackknife-method.md) — leave-one-out resampling for bias and variance estimation; compares to bootstrap; relevance to A/B testing [status: current] [sources: 1]

## Auction Mechanisms & Pricing

- [Why Ads Have Auctions](wiki/synthesis/why-ads-have-auctions.md) — economic rationale: scarcity, price discovery, allocative efficiency, perishing inventory; why fixed prices fail and GSP prevails [status: current] [sources: 2]
- [What Is a Second Price Auction?](wiki/synthesis/second-price-auction.md) — Vickrey/GSP auction mechanics, incentive compatibility, revenue equivalence, and relevance to ads ranking systems [status: current] [sources: 1]
- [Internet Advertising and the GSP Auction](wiki/sources/edelman-ostrovsky-schwarz-gsp-auction.md) — Edelman, Ostrovsky & Schwarz (AER 2007); proves GSP lacks dominant-strategy truthfulness but has a unique locally envy-free equilibrium with VCG-equivalent payoffs [status: current] [sources: 1] [source_type: peer_reviewed]
- [Generalized Second-Price Auction (GSP)](wiki/concepts/generalized-second-price-auction.md) — multi-slot auction mechanism used in search advertising; bid × quality score ranking; locally envy-free equilibrium [status: current] [sources: 1]
- [Google Ad Rank and LTV Scoring](wiki/concepts/google-ad-rank-ltv-scoring.md) — production Ad Rank system: LTV = eCPM - costs (pCTR, pCQ, pLQ); thresholds, reserve pricing, rGSP, Smart Bidding [status: draft] [sources: 2]
- [What Are Vickrey and GSP Auctions?](wiki/synthesis/vickrey-and-gsp.md) — Vickrey second-price auction (1961) and Generalized Second-Price auction for multi-slot ad allocation; incentive compatibility, locally envy-free equilibrium, production differences [status: current] [sources: 2]

## Machine Learning at Scale

- [The Unreasonable Effectiveness of Data](wiki/sources/unreasonable-effectiveness-of-data.md) — Halevy, Norvig & Pereira (IEEE Intelligent Systems 2009); argues simple models + lots of data outperform complex models + less data; foundational paper for web-scale learning [status: current] [sources: 1] [source_type: peer_reviewed] [processing_status: processed] [ingest_count: 1]
- [Web-Scale Learning](wiki/concepts/web-scale-learning.md) — paradigm of training ML on naturally occurring large-scale data; threshold of sufficient data; memorization at scale [status: draft] [sources: 3]
- [Ad Click Prediction: a View from the Trenches](wiki/sources/ad-click-prediction-view-from-the-trenches.md) — McMahan et al. (KDD 2013); Google's CTR prediction system: FTRL-Proximal algorithm, per-coordinate learning rates, memory optimization at billion-coefficient scale [status: current] [sources: 1] [source_type: peer_reviewed] [processing_status: chunked] [ingest_count: 1]

## Ad Ranking & Delivery

- [How Meta Ad Ranking Works](wiki/synthesis/meta-ad-ranking.md) — Meta's 2026 ads ranking: 5-system stack (Andromeda, Lattice, GEM, UTIS, ARM); creative-first neural retrieval; unified cross-surface ranking; foundation model teacher-student architecture; GSP auction [status: current] [sources: 3]
- [Meta Ads Ranking System](wiki/entities/meta-ads-ranking-system.md) — entity overview of Meta's 5-system architecture, auction equation, targeting inversion, and infrastructure [status: draft] [sources: 3]
- [Meta Adaptive Ranking Model](wiki/sources/meta-adaptive-ranking-model.md) — Meta Engineering blog on ARM: request-centric computation, selective FP8 quantization, multi-card GPU sharding for O(1T) parameter models [status: current] [sources: 1] [source_type: other]
- [Meta's Generative Ads Model (GEM)](wiki/sources/meta-gem-ads-foundation-model.md) — Meta Engineering blog on the GEM foundation model teacher with knowledge distillation to downstream models [status: current] [sources: 1] [source_type: other]
- [The Meta Ads Algorithm in 2026](wiki/sources/meta-ads-algorithm-2026-guide.md) — practitioner analysis of 5-system stack, auction equation, targeting inversion, learning phase, and campaign structure [status: draft] [sources: 1] [source_type: blog_post]
- [How Reddit Ads Work](wiki/synthesis/reddit-ads.md) — Reddit's second-price auction, 4-stage delivery funnel, contextual relevance system, community-based targeting, MAX AI campaigns, pricing, and delivery [status: current] [sources: 4]
- [Reddit Ads System](wiki/entities/reddit-ads-system.md) — entity overview of Reddit's auction, 4-stage delivery funnel, contextual relevance system, targeting, and bidding [status: draft] [sources: 4]
- [Google CTR Prediction System](wiki/entities/google-ctr-prediction-system.md) — entity overview of Google's deployed CTR prediction system: FTRL-Proximal online learning, per-coordinate rates, memory optimization stack, progressive validation [status: draft] [sources: 1]
- [FTRL-Proximal Algorithm](wiki/entities/ftrl-proximal-algorithm.md) — online learning algorithm combining OGD accuracy with RDA sparsity; per-coordinate learning rates; L1/L2 regularization [status: draft] [sources: 1]
- [How Reddit Advertising Works](wiki/sources/reddit-ads-how-it-works.md) — practitioner guide: auction mechanics, ranking factors, bidding strategies, learning phase [status: draft] [sources: 1] [source_type: blog_post]
- [Reddit Max Campaigns](wiki/sources/reddit-max-campaigns.md) — official Reddit announcement: AI-powered fully automated campaigns with Community Intelligence [status: current] [sources: 1] [source_type: other]
- [Reddit Audience Targeting](wiki/sources/reddit-audience-targeting.md) — official documentation: community, interest, and keyword targeting; custom audiences; funnel mapping [status: current] [sources: 1] [source_type: other]
- [Contextual Relevance of Ads at Reddit](wiki/sources/contextual-relevance-of-ads-reddit.md) — Reddit Engineering blog: LLM-as-judge labeling, fine-tuned embedding model for post-level contextual relevance, auction utility boosting [status: draft] [sources: 1] [source_type: other]
- [Contextual Relevance in Advertising](wiki/concepts/contextual-relevance-advertising.md) — matching ads to content context; embedding vs taxonomy vs LLM-as-judge; Reddit's multi-tower model [status: draft] [sources: 1]

## Recommendation Systems

- [How the TikTok Recommendation Algorithm Works](wiki/synthesis/tiktok-recommendation-algorithm.md) — two-stage pipeline (candidate generation + ranking); unsupervised clustering + embeddings; implicit signal-driven feedback loop; exploration vs exploitation [status: current] [sources: 3]
- [How TikTok Recommends Content](wiki/sources/tiktok-recommender-system.md) — TikTok official documentation on recommender signals (user interactions, content info, user info) [status: current] [sources: 1] [source_type: other]
- [How TikTok's Algorithm Really Works](wiki/sources/tiktok-unsupervised-algorithm-deep-dive.md) — unsupervised learning engine behind FYP; embeddings, Monolith real-time training, two-stage architecture [status: draft] [sources: 1] [source_type: blog_post]
- [Two-Tower and Factorized Models: Architecture for Billion-Scale Retrieval](wiki/synthesis/two-tower-factorized-models.md) — dual-encoder architecture for retrieval stage; independent user/item towers; in-batch negatives; sampling bias correction; FAISS ANN search; multi-stage pipeline; cold-start handling [status: current] [sources: 2]
- [Monolith Real-Time Recommendation System](wiki/entities/monolith-realtime-system.md) — ByteDance's production real-time recommendation system: collisionless embedding (Cuckoo hash), online training, minute-level parameter sync, deployed in BytePlus Recommend [status: current] [sources: 1]
- [Online Training for Recommendation Systems](wiki/concepts/online-training-recommendation.md) — continuous model updating on streaming user feedback; Kafka/Flink streaming, incremental parameter sync, trade-offs between reliability and real-time learning [status: draft] [sources: 2]
- [Collisionless Embedding Table](wiki/concepts/collisionless-embedding-table.md) — collision-free sparse feature embedding via Cuckoo hashing; frequency filtering and expirable embeddings for memory efficiency [status: draft] [sources: 1]
- [Pinterest's Foundation Models: From PinFM to Unified Retrieval and Ranking](wiki/synthesis/pinterest-foundation-model.md) — PinFM 20B+ param transformer; DCAT 600% throughput gain; PinRec generative retrieval; UniPinRec full-stack unification; request-level deduplication stack [status: current] [sources: 2]

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
- [Contextual Relevance of Ads at Reddit](wiki/sources/contextual-relevance-of-ads-reddit.md) — Reddit Engineering blog: LLM-as-judge labeling, fine-tuned embedding model for post-level contextual relevance, auction utility boosting [status: draft] [sources: 1] [source_type: other] [processing_status: processed] [ingest_count: 1]
- [Jackknife Resampling](wiki/sources/jackknife-resampling.md) — leave-one-out resampling for bias and variance estimation; pre-dates the bootstrap; developed by Quenouille (1949) and Tukey (1958) [status: current] [sources: 1] [source_type: other]
- [Time-uniform CLT and Asymptotic Confidence Sequences](wiki/sources/time-uniform-clt-asymp-cs.md) — Waudby-Smith et al. (Annals of Statistics 2024); AsympCS with optimal LIL rate; CS width penalty ~2× vs fixed-horizon [status: current] [sources: 1] [source_type: peer_reviewed]
- [Network Interference in A/B Testing](wiki/sources/network-interference-ab-testing.md) — cluster randomization, exposure modeling, regression adjustment, causal message-passing for SUTVA violation [status: current] [sources: 1] [source_type: peer_reviewed]
- [Contextual Relevance, Feedback Loops, and User Trust](wiki/sources/contextual-relevance-feedback-trust.md) — bias feedback loops in ranker training; contextual vs behavioral advertising performance; balancing ad relevance with trust [status: current] [sources: 1] [source_type: other]
- [Reddit Max Campaigns Trajectory vs Meta Advantage+](wiki/sources/reddit-max-campaigns-trajectory.md) — Max CPA -17%, conversions +27%; Advantage+ became default Q2 2026; Reddit differentiates on transparency [status: current] [sources: 1] [source_type: other]
- [Ad Click Prediction: a View from the Trenches](wiki/sources/ad-click-prediction-view-from-the-trenches.md) — McMahan et al. (KDD 2013); CTR prediction at Google: FTRL-Proximal, per-coordinate rates, memory optimization [status: current] [sources: 1] [source_type: peer_reviewed] [processing_status: chunked] [ingest_count: 1]
- [Ranking Engineer Agent (REA): Meta's Autonomous Ads Ranking Optimizer](wiki/sources/meta-ranking-engineer-agent-rea.md) — autonomous AI agent for end-to-end ML experimentation on ads ranking; 2× accuracy improvement over baseline [status: current] [sources: 1] [source_type: other]
- [Two-Tower Models: The Architecture Powering Google, TikTok, and YouTube](wiki/sources/two-tower-models-engineers-of-ai.md) — comprehensive tutorial on two-tower: architecture constraint, in-batch negatives, sampling bias correction, FAISS serving, multi-stage pipeline [status: draft] [sources: 1] [source_type: other] [processing_status: processed] [ingest_count: 1]
- [Implement Two-Tower Retrieval for Large-Scale Candidate Generation](wiki/sources/implement-two-tower-retrieval-google-cloud.md) — Google Cloud reference architecture: Vertex AI two-tower deployment, decoupled tower serving, cold-start handling [status: draft] [sources: 1] [source_type: other] [processing_status: processed] [ingest_count: 1]
- [Monolith: Real Time Recommendation System With Collisionless Embedding Table](wiki/sources/monolith-realtime-recommendation-system.md) — ByteDance's real-time recommendation system with Cuckoo hash collisionless embedding, online training, and parameter sync trade-offs (ORSUM@ACM RecSys 2022) [status: current] [sources: 1] [source_type: peer_reviewed] [processing_status: processed] [ingest_count: 1]
- [PinFM: Foundation Model for User Activity Sequences at Pinterest](wiki/sources/pinfm-foundation-model-pinterest.md) — 20B+ param transformer pretrained user activity encoder; DCAT for 600% throughput; fine-tuned for per-surface ranking [status: current] [sources: 1] [source_type: peer_reviewed] [processing_status: processed] [ingest_count: 1]
- [Scaling Recommendation Systems with Request-Level Deduplication at Pinterest](wiki/sources/pinterest-request-level-deduplication.md) — infrastructure for PinFM deployment: 10-50x storage compression, 4x training speedup, 7x serving throughput [status: draft] [sources: 1] [source_type: industry_report] [processing_status: processed] [ingest_count: 1]
