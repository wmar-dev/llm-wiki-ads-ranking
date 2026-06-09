---
title: "Two-Tower and Factorized Models: Architecture for Billion-Scale Retrieval"
type: "synthesis"
sources:
  - "web/two-tower-models-engineers-of-ai.md"
  - "web/implement-two-tower-retrieval-google-cloud.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Two-Tower and Factorized Models: Architecture for Billion-Scale Retrieval

Two-tower (also called dual-encoder or factorized) models are the dominant architecture for the retrieval stage of large-scale recommendation and ad delivery systems. They solve a fundamental engineering problem: how to find relevant items from a catalog of billions in under 20 milliseconds.

## The Core Idea

Two-tower models impose a deliberate architectural constraint: **the user and item computations must be completely independent**. This constraint makes it possible to precompute item embeddings offline and serve them via fast nearest-neighbor search — transforming an otherwise intractable problem into one solvable on commodity hardware. [[wiki/sources/two-tower-models-engineers-of-ai.md]] *(blog post)*

A NeuMF-style model that concatenates user and item features requires a full forward pass for every user-item pair. At 0.1ms per pair, scoring 100 million items takes nearly 3 hours per user. The two-tower constraint reduces this to under 15ms: one user tower forward pass (~1ms) plus ANN search (~5-10ms).

![synthesis-two-tower-factorized-models-diagram-1](/assets/synthesis-two-tower-factorized-models-diagram-1.svg)

## Architecture

The defining equation is a dot product in a shared embedding space:

**s(u,i) = ⟨f_θ(x_u), g_ϕ(x_i)⟩**

| Component | Role | Examples |
|---|---|---|
| **User tower** f_θ | Maps user features to a k-dimensional embedding | User ID, demographics, watch/search history, device, time-of-day |
| **Item tower** g_ϕ | Maps item features to same k-dimensional space | Item ID, category, tags, content embeddings, creator features |
| **Score** | Dot product or cosine similarity of the two embeddings | Similarity measure |
| **k** | Embedding dimension (typically 64-256) | Trade-off: expressiveness vs ANN speed |

Both towers can be arbitrarily complex internally (MLPs, attention, transformers). The only constraint is that **no information crosses from one tower to the other** during the forward pass. [[wiki/sources/two-tower-models-engineers-of-ai.md]] *(blog post)*

### Relation to Matrix Factorization

Traditional matrix factorization (MF) learns user and item embeddings d such that UV^T ≈ P (the interaction matrix). Two-tower models are the deep-learning generalization: instead of lookup tables, the towers are feature-engineered neural networks that can incorporate content features, context, and metadata. The Google factorized deep retrieval paper (Yi et al., MLSys 2019) extends WALS factorization with content features and distributed TensorFlow Serving for a 1.2 TB production model. [[wiki/sources/two-tower-models-engineers-of-ai.md]] *(blog post)*

This is why the term **"factorized models"** is used interchangeably: the interaction matrix is factorized into independent user and item representations, but with deep neural networks replacing simple embedding lookups.

## Training: In-Batch Negatives and Bias Correction

Two-tower models are trained with **in-batch negatives** (InfoNCE / batch softmax loss). For a batch of B positive (user, item) pairs, every other item in the batch serves as a negative for each user. This is free — the forward pass already computed all embeddings.

**Sampling bias correction** (Yi et al., Google Brain 2019) is critical: popular items appear as negatives in more batches, biasing the model against them. The fix subtracts log q(i) (the log of item i's sampling probability) from its logit before softmax. Skipping this is a common mistake that silently degrades long-tail performance. [[wiki/sources/two-tower-models-engineers-of-ai.md]] *(blog post)*

Key hyperparameters:
- **Batch size**: 1024-4096 (small batches kill two-tower training)
- **Temperature τ**: 0.05-0.2 (learnable parameter often works better than fixed)

## Serving: The Multi-Stage Pipeline

Two-tower models are used for the **retrieval** stage only. The full production pipeline has 3-4 stages:

| Stage | Model | Candidate count | Latency budget |
|---|---|---|---|
| 1. Retrieval | Two-tower + ANN | 100M → ~1,000 | ~20ms |
| 2. Pre-ranking | Light model (shallow MLP) | 1,000 → ~200 | ~10ms |
| 3. Ranking | Heavy model (DIN, DLRM, NeuMF) | 200 → ~50 | ~50-80ms |
| 4. Post-processing | Business rules | 50 → final | Variable |

Each stage uses a more expensive model because the candidate set shrinks. Only the retrieval stage needs the two-tower constraint — ranking models can (and should) use joint user-item features. [[wiki/sources/two-tower-models-engineers-of-ai.md]] *(blog post)*

## Cold-Start and Freshness

New items with no interaction history cannot be retrieved by the precomputed item index. Solutions include:
- **Content-based warm start**: build the item tower to operate on content features alone (randomly zero out item ID during training at probability p=0.1)
- **Streaming updates**: after 50-100 interactions, re-run the item through the tower and push the new embedding
- **Exploration injection**: explicitly inject new items via a rule-based policy

The co-learning of towers means new items can be described in terms of similar known items via their content features, even without training data. [[wiki/sources/implement-two-tower-retrieval-google-cloud.md]] *(reference architecture)*

## Ecosystem Examples

The two-tower architecture appears throughout modern recommendation and ad systems:

| System | Two-Tower / Factorized Component | Role |
|---|---|---|
| **TikTok FYP** | Deep retrieval model with MLP + tree-structured EM training | Candidate generation from billions of videos |
| **Meta Andromeda** | Neural retrieval reading creative content (CV + semantics) | Pre-rank candidate retrieval for Facebook/Instagram ads |
| **Reddit Relevance** | Multi-tower architecture with Stella encoder + subreddit embeddings | Post-level contextual relevance for ad targeting |
| **Google CTR System** | FTRL-Proximal (not two-tower but factorized) | Online learning of per-coefficient models at billion-parameter scale |
| **YouTube DNN** | Deep retrieval with user/item neural towers (2016 paper) | Pioneer of the two-tower retrieval paradigm |

The common thread: all face the same scaling problem — retrieve relevant candidates from billions of items within strict latency budgets. The two-tower constraint is the practical solution, even though each system implements it differently. [[wiki/sources/two-tower-models-engineers-of-ai.md]] *(blog post)*

## Limitations

- **Limited feature interactions**: by design, no user-item crossing until the final dot product. Cannot learn conditional preferences ("user likes this brand but only in that category") — delegated to the ranking stage
- **Embedding staleness**: FAISS embeddings must be refreshed when the model retrains; production bugs arise from forgotten index rebuilds
- **Bias amplification**: can capture and amplify popularity, exposure, and other biases from training data; negative sampling strategy heavily influences this
- **Simple scoring**: dot product may be too simplistic for complex affinity; newer work (Mixture-of-Logits, 2024) attempts to learn richer similarity functions while preserving ANN efficiency

## Open Questions

- How do two-tower retrieval and joint-stage deep learning models (e.g., TDM, generative retrieval) compare in ad systems where the item catalog is smaller (~10M vs 100M+)?
- Can cross-tower information flow be introduced at training time (e.g., via knowledge distillation from a joint model) without breaking the serving-time independence constraint?
- How should sampling bias correction be adapted for ad delivery, where items (ads) have unequal budget constraints and pacing requirements?

## Related Pages

- [[wiki/synthesis/tiktok-recommendation-algorithm.md]] — TikTok's two-stage pipeline using embeddings for candidate generation
- [[wiki/synthesis/meta-ad-ranking.md]] — Andromeda neural retrieval for ad candidate generation
- [[wiki/synthesis/reddit-ads.md]] — Reddit's multi-tower relevance model in the delivery funnel
- [[wiki/concepts/web-scale-learning.md]] — the paradigm that makes data-driven retrieval viable
- [[wiki/concepts/contextual-relevance-advertising.md]] — multi-tower embedding approach for ad relevance
