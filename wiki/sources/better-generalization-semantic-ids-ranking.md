---
title: "Better Generalization with Semantic IDs: A Case Study in Ranking for Recommendations"
type: "source_summary"
sources:
  - "web/better-generalization-semantic-ids-ranking.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Better Generalization with Semantic IDs: A Case Study in Ranking for Recommendations

**Authors:** Anima Singh, Trung Vu, Nikhil Mehta, Raghunandan Keshavan (Google), Maheswaran Sathiamoorthy (Google DeepMind), Yilin Zheng (Google), Lichan Hong (Google DeepMind), Lukasz Heldt (Google), Li Wei (Google), Devansh Tandon (Google), Ed H. Chi (Google DeepMind), Xinyang Yi (Google DeepMind)

**Source:** arXiv:2306.08121 (cs.IR, cs.LG)

**Source type:** `peer_reviewed`

---

## Summary

This paper tackles the problem of replacing randomly-hashed item IDs in production recommendation ranking models with semantically meaningful content-derived representations. It proposes using **Semantic IDs (SIDs)** — discrete codeword tuples from RQ-VAE quantization — as a drop-in replacement for video IDs in YouTube's ranking model. The key contribution is adapting SIDs for resource-constrained ranking models (as opposed to the original TIGER usage for generative retrieval).

## Key Findings

### Two-Stage Framework

1. **Stage 1 (offline):** Train an RQ-VAE model to compress frozen content embeddings (2048-dim from a Video-BERT encoder) into discrete SIDs. The RQ-VAE uses L=8 quantization levels with codebook size K=2048, producing an 8-tuple per video.
2. **Stage 2 (online):** Freeze the RQ-VAE. Train the ranking model using SID-derived features via hashing sub-pieces of the SID sequence.

### SID Adaptation Methods for Ranking

| Method | Description | Embedding Table Size | Notes |
|--------|-------------|---------------------|-------|
| **Unigram-SID** | Each of the 8 codes maps to a separate embedding table row | 8 × K rows | L=8 subwords per item |
| **Bigram-SID** | Pairs of consecutive codes; each pair maps to a shared row | 4 × K² rows | L/2=4 subwords per item |
| **SPM-SID** | SentencePiece learns variable-length subwords from SID distribution | Configurable table size | Dynamic: popular codes combine, rare codes stay unigram |

### Key Results

- **Directly replacing IDs with raw content embeddings (Dense Input) degrades quality** — ranking models rely on memorization from ID-based embedding tables. Content embeddings alone lack this memorization capacity.
- **When user history is used as input**, both Unigram-SID and Bigram-SID outperform random hashing on overall CTR AUC and cold-start CTR/1D AUC. The diverse content in watch history ensures uniform embedding table usage.
- **SPM-SID consistently outperforms N-gram methods with large embedding tables**, especially on cold-start generalization (CTR/1D AUC). SPM dynamically generates subwords based on training data distribution, reducing embedding lookups for head items.
- **For smaller embedding tables**, N-gram methods show a slight advantage over SPM-SID because SPM's smaller vocabulary struggles to capture complex semantic relationships.
- A **0.1% change in CTR AUC** is considered significant for YouTube's ranking model.

### Stability of Semantic IDs

RQ-VAE models trained on older vs. recent data produce SIDs with comparable downstream ranking performance, indicating that learned semantic representations are stable over time despite corpus evolution.

## Relevance to Ads Ranking

While this paper focuses on YouTube video recommendations (not ads), the core problem — replacing randomly-hashed item IDs with semantically meaningful representations to improve cold-start and long-tail generalization — is directly applicable to ad item representation. The techniques for adapting SIDs in latency-sensitive ranking models (hashing via SPM subwords) translate to ad ranking systems where ad catalogs are similarly large, power-law distributed, and dynamically evolving.

## Related Pages

- [[wiki/synthesis/semantic-id.md]] — synthesis page on Semantic ID concept
- [[wiki/sources/tiger-transformer-index-generative-recommenders.md]] — original TIGER paper proposing SIDs for generative retrieval
- [[wiki/concepts/web-scale-learning.md]] — web-scale learning paradigm relevant to large-vocabulary item representation
