---
title: "Meta Ads Ranking System"
type: "entity"
sources:
  - "web/meta-adaptive-ranking-model.md"
  - "web/meta-gem-ads-foundation-model.md"
  - "web/meta-ads-algorithm-2026-guide.md"
  - "web/meta-utis-user-true-interest-survey.md"
  - "web/llatte-scaling-laws-recommendation.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-09"
---

# Meta Ads Ranking System

Meta's ad ranking and delivery system, as of mid-2026, is a stack of five interlocking AI systems operating under 200-300ms latency constraints across billions of daily impressions.

## Five-System Architecture

![entities-meta-ads-ranking-system-diagram-1](/assets/entities-meta-ads-ranking-system-diagram-1.svg)

| System | Role | Deployed | Reported Impact |
|---|---|---|---|
| **Andromeda** | Neural retrieval — reads creative content to match users | Dec 2024, global Oct 2025 | +6% recall, +8% ads quality |
| **Lattice** | Unified ranking — replaces per-objective siloed models | Through 2025 | +12% ad quality, +6% conversions |
| **GEM** | Foundation model teacher — trains others via distillation | Reels mid-2025, broader late 2025 | 4× efficiency, +5% conversions Reels |
| **UTIS** | Survey-based interest calibration | Jan 14, 2026 | Tier-0 retention improvements |
| **Adaptive Ranking Model** | Infrastructure for O(1T) parameter models | Instagram Q4 2025, rolling out | +3% conversions, +5% CTR |

## Teacher-Student Hierarchy

GEM is too expensive to serve ads directly. It teaches Lattice, Andromeda, and vertical models via knowledge distillation, representation learning, and parameter sharing. UTIS calibrates Lattice's ranking decisions. The Adaptive Ranking Model makes the whole thing servable at sub-100ms latency per impression.

## Auction Mechanism

**Total Value = (Bid × Estimated Action Rate) + Ad Quality**

- **Estimated Action Rate (EAR)**: built from soft signals (CTR, hook rate, hold rate) and hard signals (historical click-to-conversion rate)
- **Ad Quality**: creative assessment, user feedback, landing page experience, UTIS-derived interest match
- Creative quality accounts for ~56% of campaign performance

## Key Infrastructure Components

**Andromeda**: Uses CV and semantic analysis to read ad creative (hook, format, on-screen talent, copy, landing page) and predict which users will convert — regardless of advertiser-defined audience. 10,000× increase in model complexity vs prior retrieval.

**Lattice**: Consolidated hundreds of per-objective/per-surface models into one architecture. Cross-surface learning (Reels → Feed, click → conversion). Includes Sequence Learning, Lattice Zipper (data freshness), Lattice Filter (feature selection).

**GEM**: Wukong-based architecture (stackable factorization machines + cross-layer attention). InterFormer for preserved sequence learning. Pyramid-parallel structure for long user behavior sequences (thousands of events). Multi-domain optimization.

**UTIS**: Random daily in-feed surveys ("How well does this match your interests?" 1-5 scale). Trains Perception Layer on binarized survey responses. Integrates into late-stage ranking, early retrieval, and sequence-based retrieval.

**Adaptive Ranking Model**: Request-centric (compute user signals once per request), selective FP8 quantization, multi-card GPU sharding. 35% MFU, models deployable in <10 minutes. Trillion-parameter scaling at sub-100ms.

## Targeting Inversion

Since Andromeda, creative IS the targeting. The system reads creative content to find users, rather than filtering by advertiser-defined audiences. Entity IDs cluster visually similar ads for retrieval — only genuinely distinct visual concepts generate new retrieval paths.

## Signal Requirements

- **Pixel + CAPI** required. CAPI captures ~60-70% of conversions; browser-only captures less after iOS privacy changes.
- **EMQ ≥ 7.0** target for primary conversion events
- **Learning phase**: 50 optimization events within 7 days to exit

## Relationship to Other Systems

Meta's system differs from [[wiki/concepts/google-ad-rank-ltv-scoring.md]] in that it uses a foundation model teacher-student architecture and combines organic content signals with ad signals. Both use generalized second-price auction principles ([[wiki/concepts/generalized-second-price-auction.md]]).

## Answered Questions

### UTIS and engagement optimization

UTIS does not conflict with engagement — it improves it. Meta's production A/B test (10M+ users) showed UTIS increased total user engagement by +5.2% while also raising satisfaction (+5.4% high ratings). Precision identifying true interests improved from 48.3% (heuristic) to 63.2%. UTIS acts as a Perception Layer in parallel to the Late Stage Ranking, providing a "boost and demote" signal: content with high predicted true interest receives a modest ranking boost; clickbait with low predicted interest is demoted. The results demonstrated that true interest alignment and engagement are *complementary* when the interest signal is integrated as a soft feature in a multi-objective value formula. [[wiki/sources/meta-utis-user-true-interest-survey.md]]

### ARM expansion beyond Instagram

ARM launched on Instagram only in Q4 2025 (+3% conversions, +5% CTR). Meta's language calls it "the first milestone in our journey." A phased expansion to Facebook Feed, Reels, and other surfaces is expected throughout 2026. The latency trade-offs are managed through request-centric computation sharing (sub-linear scaling), selective FP8 quantization (35% MFU), and multi-card GPU sharding for O(1T) parameter models at sub-100ms latency. [[wiki/sources/meta-adaptive-ranking-model.md]] *(company engineering blog)*

### GEM scaling law vs LLM inference-time scaling

GEM follows the same *power-law scaling* as LLMs — recommendation performance improves log-linearly with compute (FLOPs), similar to Chinchilla-style scaling laws. The LLaTTE paper (Meta, Jan 2026) proved this empirically and showed that semantic content features are a *prerequisite* for steep scaling. However, the key difference is architectural: GEM uses *teacher-student distillation* to transfer learning to smaller servable models, while LLM inference-time scaling typically involves chain-of-thought or test-time compute on the same large model. GEM is 4× more efficient per unit data/compute than prior models. [[wiki/sources/llatte-scaling-laws-recommendation.md]] *(peer_reviewed)*
