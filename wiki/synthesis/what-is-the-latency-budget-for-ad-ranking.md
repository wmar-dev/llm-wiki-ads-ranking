---
title: "What Is the Latency Budget for Ad Ranking?"
type: "synthesis"
sources:
  - "web/two-tower-models-engineers-of-ai.md"
  - "web/implement-two-tower-retrieval-google-cloud.md"
  - "web/meta-adaptive-ranking-model.md"
  - "web/meta-ads-algorithm-2026-guide.md"
  - "web/rtb-latency-budget-systemdr.md"
  - "web/pinterest-request-level-deduplication.md"
status: "current"
created: "2026-06-10"
last_updated: "2026-06-10"
---

# What Is the Latency Budget for Ad Ranking?

The **latency budget** is the total wall-clock time a system has — from the
moment an ad request arrives to the moment a response (an ad to serve, or a bid
to submit) must be returned — before the request is dropped or scored as a
non-response. Across both ad-platform ranking pipelines and open programmatic
RTB, this budget converges on the **same order of magnitude: roughly 100ms**,
though the exact figure and its internal breakdown differ by system.

![what-is-the-latency-budget-for-ad-ranking-diagram-1](/assets/what-is-the-latency-budget-for-ad-ranking-diagram-1.svg)

## The Headline Numbers

| System | Total budget | Source |
|---|---|---|
| Google Ad Rank auction | ~100ms | [[wiki/synthesis/meta-ad-ranking.md]] (comparison table) |
| Open RTB (DSP bid response) | ~80-120ms (industry standard 100-300ms incl. RTT) | [[wiki/sources/rtb-latency-budget-systemdr.md]] *(blog post)* |
| Meta ad ranking (end-to-end) | 200-300ms | [[wiki/synthesis/meta-ad-ranking.md]] |

**Inference:** Meta's larger budget likely reflects its multi-stage,
LLM-scale ranking stack (Andromeda → light ranking → Lattice/GEM → auction)
serving richer creative-understanding models, versus Google's more
keyword/quality-score-driven retrieval for search ads.

## How the Budget Is Allocated: the Multi-Stage Pipeline

Within a single request, the budget is divided across pipeline stages that
progressively narrow the candidate set while applying increasingly expensive
models [[wiki/synthesis/two-tower-factorized-models.md]]:

| Stage | Model | Candidates in → out | Latency budget |
|---|---|---|---|
| 1. Retrieval | Two-tower + ANN | 100M → ~1,000 | ~20ms |
| 2. Pre-ranking | Light model (shallow MLP) | 1,000 → ~200 | ~10ms |
| 3. Ranking | Heavy model (DIN, DLRM, Lattice) | 200 → ~50 | ~50-80ms |
| 4. Post-processing / auction | Business rules + Ad Rank / GSP / rGSP | 50 → final | Variable |

Summing stages 1-3 (~80-110ms) lands close to the ~100ms headline figure for
Google's auction, with the auction/pricing computation itself folded into the
remaining margin.

## How Open RTB Allocates the Same ~100ms

For programmatic/RTB exchanges, the budget is split across network and
multiple parties rather than model stages
[[wiki/sources/rtb-latency-budget-systemdr.md]] *(blog post)*:

| Stage | Budget |
|---|---|
| Publisher → exchange (network) | ~10ms |
| Exchange processing + fanout to DSPs | ~15ms |
| **DSP bid calculation** | **~50ms** |
| Response aggregation + auction logic | ~15ms |
| Exchange → publisher (network return) | ~10ms |

The ~50ms DSP compute window is the dominant share — directly comparable to
the ~50-80ms heavy-ranking stage in the platform pipeline above, despite the
two systems having very different architectures. **OpenRTB enforces this with a
hard cutoff**: a bid response that arrives even 1ms late is dropped entirely
(HTTP 408 Timeout), not scored late [[wiki/sources/rtb-latency-budget-systemdr.md]].

## How Systems Engineer Within the Budget

Hitting ~100ms with billion-parameter (or trillion-parameter) models requires
specific architectural choices, all represented elsewhere in this wiki:

- **Precompute what you can offline.** Two-tower retrieval moves the expensive
  item-side computation offline (embeddings precomputed and indexed via ANN), so
  only a single user-tower forward pass plus an ANN lookup happen at request time
  [[wiki/synthesis/two-tower-factorized-models.md]].
- **Cache aggressively, skip on timeout.** RTB systems maintain hot caches of
  user profiles and targeting rules; if an auxiliary lookup would take >5ms, it's
  often skipped entirely rather than risk the deadline
  [[wiki/sources/rtb-latency-budget-systemdr.md]].
- **Make per-request compute sub-linear.** Meta's Adaptive Ranking Model (ARM)
  uses **request-centric computation sharing** — computing high-density user
  signals once per page load rather than once per user-ad pair — plus selective
  FP8 quantization and multi-card GPU sharding, enabling LLM-scale models (GEM,
  Lattice) to run within the 200-300ms budget
  [[wiki/sources/meta-adaptive-ranking-model.md]] *(other)*.
- **Deduplicate redundant work across candidates.** Pinterest's request-level
  deduplication (DCAT) avoids reprocessing the same 16K-token user sequence for
  every candidate item, yielding a 7x serving-throughput increase for ranking —
  throughput headroom that can be reinvested as either lower latency or larger
  models within the same budget [[wiki/sources/pinterest-request-level-deduplication.md]]
  *(industry report)*.
- **Sparsify at serving time.** Google's CTR system stores billion-coefficient
  models with fixed-point encoding and probabilistic feature inclusion
  specifically to keep per-prediction latency low
  [[wiki/entities/google-ctr-prediction-system.md]].

## Why It Matters for Ads Ranking

- The latency budget is a **hard architectural constraint**, not a soft target —
  in RTB, missing it means the bid is discarded and the impression is lost
  entirely [[wiki/sources/rtb-latency-budget-systemdr.md]].
- It directly explains **why GSP (not VCG) is used for ad auctions**: VCG's
  exact mechanism requires re-solving the welfare-maximizing allocation once per
  bidder — NP-hard in combinatorial settings — which is infeasible inside a
  ~10-15ms auction/pricing window. GSP's local "next-bid ÷ quality-score"
  computation is a constant-time alternative [[wiki/synthesis/what-is-vcg.md]].
- It is the reason **retrieval, pre-ranking, and ranking exist as separate
  stages** at all: each stage trades model complexity for candidate-set size to
  keep the total within budget [[wiki/synthesis/two-tower-factorized-models.md]].
- Infrastructure investments that "just" increase throughput (Pinterest's DCAT,
  Meta's ARM) are really **latency-budget investments** — they let teams deploy
  larger/better models without exceeding the same wall-clock ceiling.

## Open Questions

- Open question: How much of the ~100ms Google Ad Rank budget is consumed by
  the rGSP randomization step (selecting among close-LTV bidders) versus the
  base GSP pricing computation?
- Open question: Do any major platforms publish a breakdown of their latency
  budget by stage the way the two-tower retrieval pipeline table does — or are
  Google's and Meta's per-stage allocations purely inferred from aggregate
  totals?

## Related Pages

- [[wiki/synthesis/two-tower-factorized-models.md]]
- [[wiki/synthesis/meta-ad-ranking.md]]
- [[wiki/sources/meta-adaptive-ranking-model.md]]
- [[wiki/sources/rtb-latency-budget-systemdr.md]]
- [[wiki/sources/pinterest-request-level-deduplication.md]]
- [[wiki/entities/google-ctr-prediction-system.md]]
- [[wiki/synthesis/what-is-vcg.md]]
