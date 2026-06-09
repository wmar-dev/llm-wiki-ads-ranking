---
title: "Pinterest's Foundation Models: From PinFM to Unified Retrieval and Ranking"
type: "synthesis"
sources:
  - "web/pinfm-foundation-model-pinterest.md"
  - "web/pinterest-request-level-deduplication.md"
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

Pinterest has extended the foundation model paradigm into two additional systems:

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
- What is the marginal improvement of PinFM over TransActV2, given that TransActV2 already achieved +13.31% top-3 repin hit with lifelong sequences?

## Related Pages

- [[wiki/synthesis/meta-ad-ranking.md]] — Meta's GEM foundation model and teacher-student architecture
- [[wiki/synthesis/two-tower-factorized-models.md]] — two-tower architecture used in PinRec and Pinterest's retrieval
- [[wiki/concepts/web-scale-learning.md]] — paradigm of large-scale data driving model quality
- [[wiki/synthesis/tiktok-recommendation-algorithm.md]] — comparative recommendation architecture
