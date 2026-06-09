---
title: "Meta Ads Ranking System"
type: "entity"
sources:
  - "web/meta-adaptive-ranking-model.md"
  - "web/meta-gem-ads-foundation-model.md"
  - "web/meta-ads-algorithm-2026-guide.md"
status: "draft"
created: "2026-06-08"
last_updated: "2026-06-08"
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

## Open Questions

- How does UTIS's survey-based interest signal interact with short-term engagement optimization?
- Will the Adaptive Ranking Model expand beyond Instagram, and what latency trade-offs apply?
- How does GEM's scaling law compare to inference-time compute scaling in LLMs?
