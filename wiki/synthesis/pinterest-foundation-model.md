---
title: "Pinterest's Foundation Models: From PinFM to Unified Retrieval and Ranking"
type: "synthesis"
sources:
  - "web/pinfm-foundation-model-pinterest.md"
  - "web/pinterest-request-level-deduplication.md"
  - "web/transact-v2-pinterest.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Pinterest's Foundation Models: From PinFM to Unified Retrieval and Ranking

Pinterest's primary foundation model is **PinFM** (RecSys 2025), a 20B+ parameter transformer pretrained on user activity sequences. It follows the pretrain-then-finetune paradigm from NLP/CV, adapted to the constraints of real-time recommendation at scale. PinFM is deployed for over 500 million users, and Pinterest has since built additional foundation models (PinRec, UniPinRec) that extend the paradigm into generative retrieval and unified ranking.

## PinFM: The Core Foundation Model

PinFM is a transformer model with **20B+ parameters** pretrained on years of user activity data across multiple Pinterest surfaces. It is not used directly for serving; instead, it is fine-tuned for downstream ranking models in each application. This creates a **teacher-student architecture** analogous to Meta's GEM, where the large pretrained model transfers knowledge to smaller per-surface models. [[wiki/sources/pinfm-foundation-model-pinterest.md]] *(peer_reviewed)*

![synthesis-pinterest-foundation-model-diagram-1](/assets/synthesis-pinterest-foundation-model-diagram-1.svg)

### The Scaling Problem

PinFM represented a **100x increase** in transformer dense parameters and a **10x increase** in model dimension over prior Pinterest systems. Without infrastructure innovation, this would have made serving cost-prohibitive. [[wiki/sources/pinterest-request-level-deduplication.md]] *(industry_report)*

### DCAT: Making the Scale Affordable

The key innovation enabling PinFM's deployment is the **Deduplicated Cross-Attention Transformer (DCAT)** , which separates user sequence processing into two stages:

1. **Context encoding**: The transformer processes the user's 16K-token action sequence **once** per request. Keys and values (KV) from each layer are cached.
2. **Candidate crossing**: Each candidate item performs **cross-attention** with the cached KV, reusing the deduplicated computation.

This is implemented with custom Triton kernels for both training and serving. The result: **600% throughput improvement** over standard self-attention with FlashAttention. [[wiki/sources/pinfm-foundation-model-pinterest.md]] *(peer_reviewed)*

### Request-Level Deduplication Payoff

DCAT is one component of a broader **request-level deduplication** strategy at Pinterest:

| Layer | Technique | Gain |
|---|---|---|
| **Storage** | Apache Iceberg with request-sorted data | 10-50x compression on user feature columns |
| **Training (retrieval)** | Two-tower natural dedup + user-level masking | 4x speedup |
| **Training (ranking)** | DCAT cross-attention + deduplicated data loading | 2.8x speedup |
| **Serving (ranking)** | DCAT KV cache sharing | 7x throughput increase |

Training fixes required to preserve model quality with request-sorted data:
- **SyncBatchNorm**: aggregated batch statistics across devices to solve IID disruption
- **User-level masking**: excluded negatives belonging to the same user to fix false negatives in in-batch softmax loss [[wiki/sources/pinterest-request-level-deduplication.md]] *(industry_report)*

## Beyond PinFM: The Foundation Model Ecosystem

Pinterest has extended the foundation model paradigm into several additional systems:

### TransActV2 (2025): Lifelong Sequence Ranking for Homefeed

TransActV2 is Pinterest's production CTR ranking model for the Homefeed, extending lifelong user action sequences to **~16,000 actions** (a ~160x scale-up over real-time-only sequences) and adding a **Next Action Loss** auxiliary objective. Offline, this improved **HIT@3/repin by +13.31%** and reduced **HIT@3/hide by 11.25%** versus an RT-only baseline; online A/B tests showed **+6.35% Homefeed Repin Volume**, **−12.80% Hide Volume**, **+0.45% Impression Diversity**, and **+1.41% Time Spent on App** [[wiki/sources/transact-v2-pinterest.md]] *(other)*.

TransActV2 was developed in parallel with PinFM and is **not benchmarked against it** — TransActV2 is a per-surface ranking model, while PinFM is upstream pretraining infrastructure. Both represent Pinterest's broader move toward foundation-model-style architectures across the stack.

### PinRec (2025): Unified Generative Retrieval

PinRec is a generative retrieval model pretrained on cross-surface user activity and fine-tuned per surface (Home Feed, Search, Related Pins). Key innovation: **outcome-conditioned generation** — the model generates candidate sequences conditioned on specific outcomes (saves, clicks) to optimize per-surface business goals. Uses auto-regressive decoding + FAISS for retrieval. +4% search saves in online experiments.

### UniPinRec (2026): Full-Stack Unification

UniPinRec unifies retrieval and ranking into one model with one input format, one training stage, and shared serving infrastructure. Three innovations:
1. **Masked Action Modeling (MAM)** : ranking supervision on the same non-interleaved user sequence used for retrieval
2. **Blended training**: pairs action sequences with impression slates to satisfy both objectives
3. **Cross-stage KV cache sharing**: ranking reuses user-history computation from retrieval

Results: ~+1% online engagement, -11.1% latency, +63.6% QPS vs serving two independent models.

## Relationship to Other Foundation Models

Pinterest's foundation model approach shares the pretrain-finetune paradigm with:

| Platform | Foundation Model | Role |
|---|---|---|
| **Pinterest** | PinFM (20B+ param transformer) | Pretrained user activity encoder; fine-tuned for per-surface ranking |
| **Meta** | GEM (LLM-scale, undisclosed size) | Teacher model distilling into Lattice, Andromeda, vertical models |
| **Google** | None published at CTR/ranking level | FTRL-Proximal online learning instead (no pretrain-finetune) |

*Inference: Pinterest and Meta independently converged on the pretrain-finetune paradigm for ads/ranking foundation models at roughly the same time (2025-2026). Both use a teacher-student architecture where a large pretrained model transfers knowledge to smaller per-surface models. Pinterest's innovation is DCAT's efficiency and the unification of retrieval + ranking in UniPinRec.*

## Open Questions

- How does PinFM's 20B+ parameter count compare to Meta's GEM in terms of cost per inference and quality per parameter?
- Does UniPinRec's full-stack unification generalize to platforms with distinct retrieval and ranking pipelines (e.g., Meta, Google, TikTok)?
- **No published source directly compares PinFM and TransActV2** — the +13.31% HIT@3/repin figure (and the matching +6.35% online Homefeed Repin Volume from A/B testing) comes from TransActV2's own paper, evaluated against an RT-only-sequence baseline of the *prior* TransAct model, not against PinFM. TransActV2 is a production point-wise ranking model for Homefeed; PinFM is a 20B+ parameter pretrained foundation encoder fine-tuned per surface. The two were developed in parallel as complementary pieces of Pinterest's stack — PinFM as upstream pretraining infrastructure, TransActV2 as a downstream ranking model — rather than as competing solutions to the same task, so a "marginal improvement" framing doesn't map onto any existing benchmark [[wiki/sources/transact-v2-pinterest.md]].

## Related Pages

- [[wiki/synthesis/meta-ad-ranking.md]] — Meta's GEM foundation model and teacher-student architecture
- [[wiki/synthesis/two-tower-factorized-models.md]] — two-tower architecture used in PinRec and Pinterest's retrieval
- [[wiki/concepts/web-scale-learning.md]] — paradigm of large-scale data driving model quality
- [[wiki/synthesis/tiktok-recommendation-algorithm.md]] — comparative recommendation architecture
- [[wiki/sources/transact-v2-pinterest.md]] — TransActV2 lifelong sequence ranking model for Homefeed
