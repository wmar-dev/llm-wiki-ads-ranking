---
title: "How Meta Ad Ranking Works"
type: "synthesis"
sources:
  - "web/meta-adaptive-ranking-model.md"
  - "web/meta-gem-ads-foundation-model.md"
  - "web/meta-ads-algorithm-2026-guide.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# How Meta Ad Ranking Works

Meta's ad ranking system decides which ad to show in every Facebook, Instagram, Messenger, and WhatsApp impression — within 200-300 milliseconds, billions of times per day. As of 2026, it is a stack of five AI systems running at LLM-scale compute.

## The 4-Step Delivery Pipeline

![synthesis-meta-ad-ranking-diagram-1](/assets/synthesis-meta-ad-ranking-diagram-1.svg)

### Step 1: Retrieval (Andromeda)

From billions of eligible ads, Andromeda narrows to ~1,000-1,500 candidates per impression. Unlike the old rule-based system (filter by audience → match ads), Andromeda reads the **creative content** itself — hook, format, on-screen talent, copy, landing page — using computer vision and semantic analysis, then predicts which users are most likely to convert regardless of advertiser-defined audience.

*Inference: This is why "creative is your targeting" has become the dominant Meta strategy — the retrieval engine treats creative as the primary targeting signal.* [[wiki/sources/meta-ads-algorithm-2026-guide.md]] *(blog post)*

**Entity IDs**: Andromeda's CV system clusters visually similar ads under shared Entity IDs. Only genuinely distinct visual concepts create new retrieval paths — headline changes, color shifts, or aspect ratio variations on the same asset do not.

### Step 2: Light Ranking

A fast filter that strips the long tail of clearly poor matches, reducing candidates from thousands to a few hundred.

### Step 3: Heavy Ranking (Lattice + GEM)

The remaining candidates are scored by Lattice, Meta's unified ranking model. Lattice replaced the previous system of hundreds of siloed per-objective models (separate models for purchases vs leads vs app installs vs video views, separate again for Feed vs Reels vs Stories) with one architecture that learns from all of them simultaneously. Reels performance informs Feed ranking; click optimization informs conversion optimization.

The scoring is driven by predictions from **GEM** (Generative Ads Model), Meta's LLM-scale foundation model. GEM does not serve ads directly — it is too computationally expensive. Instead, it acts as a teacher, transferring knowledge to Lattice, Andromeda, and vertical models through knowledge distillation, representation learning, and parameter sharing.

**UTIS** (User True Interest Survey) calibrates Lattice's scores using daily in-feed survey responses ("How well does this match your interests?"), correcting for the gap between engagement signals (clicks, watch time) and genuine interest. [[wiki/sources/meta-ads-algorithm-2026-guide.md]] *(blog post)*

### Step 4: The Auction

The final ranking is determined by:

**Total Value = (Bid × Estimated Action Rate) + Ad Quality**

| Component | Description |
|---|---|
| **Bid** | Advertiser's maximum willingness to pay (auto-set in Lowest Cost bidding) |
| **Estimated Action Rate** | Predicted probability of the conversion action, built from soft signals (CTR, hook rate) and hard signals (historical conversion rate) |
| **Ad Quality** | Creative quality, user feedback, landing page experience, UTIS interest-match, negative feedback |

Creative quality accounts for roughly **56% of campaign performance** outcomes — more than targeting, budget, placement, and timing combined.

## Infrastructure: Adaptive Ranking Model

Serving LLM-scale ranking models at sub-second latency requires the Adaptive Ranking Model (ARM), Meta's infrastructure layer launched on Instagram in Q4 2025. ARM achieves this through:

- **Request-centric computation**: computes high-density user signals once per page load, not once per user-ad pair, transforming scaling from linear to sub-linear
- **Selective FP8 quantization**: lower precision only where it doesn't degrade outcomes
- **Multi-card GPU sharding**: distributes trillion-parameter embeddings across GPUs
- **35% MFU** across heterogeneous hardware; model updates in <10 minutes

*Inference: ARM is largely invisible to advertisers but explains how Meta can keep adding model complexity (GEM scales up, Lattice consolidates more signals) without latency degrading.*

## Learning Phase and Signal Requirements

New ad sets require **50 optimization events within a 7-day window** to exit the learning phase. Minimum daily budget = (Target CPA × 50) ÷ 7.

**Tracking infrastructure is required, not optional:**
- **Pixel** (browser-based) captures ~60-70% of conversions
- **Conversions API (CAPI)** (server-side) captures the rest, bypassing browser restrictions
- **Event Match Quality (EMQ)** target ≥ 7.0 for primary conversion events
- Running both Pixel + CAPI with deduplication is industry standard

## Comparison: Meta vs Google Ad Ranking

| Dimension | Meta | Google ([[wiki/concepts/google-ad-rank-ltv-scoring.md]]) |
|---|---|---|
| **Ranking formula** | (Bid × EAR) + Ad Quality | LTV = eCPM - (impression cost + click cost) |
| **Foundation model** | GEM (teacher-student distillation) | None published |
| **Retrieval** | Andromeda (creative-first neural retrieval) | Keyword + quality score matching |
| **Auction type** | Generalized second-price (GSP) | rGSP (randomized GSP) |
| **Key differentiator** | Creative IS targeting; cross-surface unified learning | Cost-side terms (pCQ, pLQ) in ranking |
| **Latency budget** | 200-300ms | ~100ms |

## Open Questions

- How does UTIS's interest-match calibration interact with Meta's revenue optimization in the long tail?
- Can the teacher-student architecture (GEM → Lattice → VMs) be audited for fairness and bias effectively?
- Does the targeting inversion (creative-as-targeting) create a barrier to entry for small advertisers with limited creative production capacity?
