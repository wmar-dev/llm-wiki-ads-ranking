---
title: "What Is a Semantic ID?"
type: "synthesis"
sources:
  - "web/tiger-transformer-index-generative-recommenders.md"
  - "web/better-generalization-semantic-ids-ranking.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# What Is a Semantic ID?

A **Semantic ID (SID)** is a discrete tuple of codewords that encodes an item's semantic meaning, used in generative retrieval for recommendation and search systems. Unlike traditional integer IDs (arbitrary, no semantic structure) or embedding vectors (continuous, no discrete decoding), Semantic IDs occupy a middle ground: they are discrete and interpretable but preserve semantic relationships — similar items have overlapping IDs.

## The Pipeline

```mermaid
flowchart LR
    A[Item Content\n(title, description, image)] --> B[Pre-trained Encoder\n(SentenceT5, BERT, CLIP)]
    B --> C[Dense Embedding\n~768d vector]
    C --> D[Quantizer\n(RQ-VAE / RQ-KMeans)]
    D --> E[Semantic ID\n(c0, c1, c2)]
    E --> F[Seq-to-Seq Model\n(T5, Transformer)]
    F --> G[Autoregressive Decode\nnext item's SID tokens]
```

## How It Works

### 1. Embedding

Each item's content features (title, description, image) are encoded by a pre-trained model into a dense vector. Common choices: SentenceT5, BERT, CLIP, or task-specific bi-encoders.

### 2. Quantization

The embedding is compressed into a fixed-length tuple of discrete tokens via hierarchical quantization. Each token comes from a separate codebook. The hierarchy means:

```
Semantic ID = (c0, c1, c2)

c0 = coarse cluster (e.g., "Electronics")
c1 = mid cluster    (e.g., "Audio")
c2 = fine cluster   (e.g., "Headphones")
```

**Quantization methods:**

| Method | Description | Used By |
|--------|-------------|---------|
| **RQ-VAE** | Residual Vector Quantization-VAE; learned hierarchical codebooks | TIGER (NeurIPS 2023) |
| **RQ-KMeans** | Residual k-means clustering; faster, more stable than RQ-VAE | FORGE (Taobao production), GRID |
| **VQ-VAE** | Vector Quantization-VAE; single-level codebook | Earlier generative models |

### 3. Generative Retrieval

A sequence-to-sequence model (T5, Transformer decoder) is trained on user behavior sequences of Semantic IDs. Given past items `[(a0,a1,a2), (b0,b1,b2), ...]`, the model learns to autoregressively decode the next item's SID token-by-token. At inference, beam search generates top-K candidates.

## Why Semantic IDs Matter

| Aspect | Traditional Integer ID | Dense Embedding | Semantic ID |
|--------|----------------------|-----------------|-------------|
| **Semantic structure** | None | Continuous, implicit | Discrete, explicit hierarchy |
| **Cold-start** | Fails — unseen items have no ID | Works if content-based | Works — new item maps to existing clusters |
| **Storage** | O(N) embedding vectors | O(N) embedding vectors | O(C) where C << N (codebook size) |
| **Retrieval** | Embedding + ANN search | Embedding + ANN search | Autoregressive beam search |
| **Interpretability** | None | Low | High — tokens map to semantic clusters |

## Key Results

- **TIGER** (Rajput et al., NeurIPS 2023): First to propose SIDs for recommendation. Outperformed SASRec, BERT4Rec, and other SOTA dense models on multiple benchmarks. Showed cold-start generalization: unseen items with similar content get similar or overlapping SIDs.
- **FORGE** (Taobao, 2025): Systematic benchmark of SID construction strategies. +0.35% transaction lift in online A/B on Taobao's "Guess You Like" section. Deployed at full scale on Taobao with 250M+ items.
- **GRID** (Snap Research, 2025): Open-source modular framework for SID-based generative recommendation. Found that de-duplication and tokenizer choice significantly impact performance.
- **Joint Search & Recommendation** (Spotify, RecSys 2025): Task-specific SIDs fail to generalize across search and recommendation. Multi-task bi-encoder SIDs (jointly tuned) achieve best cross-task balance.

## Relationship to Meta's Entity IDs

Meta's Andromeda system uses a related but distinct concept: **Entity IDs** cluster visually similar ad creatives via CV, where only genuinely distinct visual concepts create new retrieval paths. This is a form of semantic clustering but at the visual level and without the quantization → generative retrieval pipeline. [[wiki/synthesis/meta-ad-ranking.md]]

## Semantic IDs in Ranking Models

Beyond generative retrieval, Semantic IDs can replace item IDs directly in production ranking models. Singh et al. (2024) demonstrated this at YouTube scale: SIDs from RQ-VAE (L=8, K=2048) replace video IDs in a multi-task ranking model serving billions of embeddings [[wiki/sources/better-generalization-semantic-ids-ranking.md]] *(peer_reviewed)*.

### Adaptation Methods

| Method | How It Works | Embedding Lookups per Item | Best For |
|--------|-------------|---------------------------|----------|
| **Unigram** | Each SID code maps to its own embedding table row | L (e.g., 8) | Simple baseline |
| **Bigram** | Pairs of consecutive codes share an embedding row | L/2 (e.g., 4) | Fewer lookups, larger table |
| **SPM** | SentencePiece learns variable-length subwords from SID distribution | Dynamic (reduced for head items) | Large-scale production |

### Key Findings

- **Raw content embeddings cannot replace IDs**: directly feeding frozen content embeddings as features degrades CTR — ranking models depend on learnable memorization from embedding tables. Increasing model depth helps but at prohibitive serving cost.
- **SIDs succeed where raw embeddings fail**: by providing learnable embedding tables keyed by discrete SID subwords, the model retains memorization capacity while gaining semantic generalization.
- **SentencePiece tokenization outperforms fixed N-grams** for SID adaptation in large embedding tables. SPM dynamically groups co-occurring code sequences into subwords, reducing lookups for head items while preserving rare-code distinctions for tail items — analogous to subword tokenization in LLMs.
- **Semantic representations are stable over time**: RQ-VAE models trained on older vs. recent data produce SIDs with comparable downstream ranking quality.

## Limitations

- **Performance gap**: Generative retrieval with SIDs still underperforms dense retrieval on some benchmarks, especially for head/torso items where dense embeddings provide finer discrimination.
- **Cold-start generation**: The autoregressive decoding process can fail to generate valid SIDs for truly novel items, even when the embedding space captures them.
- **ID collision**: Multiple items can map to the same SID after quantization, requiring de-duplication strategies.
- **Task specificity**: SIDs tuned for search degrade recommendation and vice versa — a unified embedding space is an open research problem.
