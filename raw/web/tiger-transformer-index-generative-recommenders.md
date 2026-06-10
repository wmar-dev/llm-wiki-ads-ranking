# TIGER: Transformer Index for GEnerative Recommenders

**Source:** Rajput et al. — Recommender Systems with Generative Retrieval (NeurIPS 2023)
**URL:** https://dl.acm.org/doi/10.5555/3666122.3666574
**Date:** 2023

## Summary (fetched)

First paper to propose Semantic IDs for generative retrieval in recommendation.
Two-stage pipeline: (1) encode item content via SentenceT5 -> quantize embedding
via RQ-VAE into discrete codeword tuple (Semantic ID); (2) train
sequence-to-sequence Transformer to autoregressively decode next item's SID from
past SID sequences. Outperformed SASRec, BERT4Rec, and other SOTA on multiple
benchmarks. Demonstrated cold-start generalization: unseen items map to existing
semantic clusters.

### Related Work

- **FORGE** (Taobao, arXiv 2509.20904): Systematic benchmark of SID
  construction; +0.35% transaction lift in production on 250M+ items. Proposed
  Embedding HitRate and Gini coefficient as SID quality metrics.
- **GRID** (Snap Research, RecSys 2025): Open-source modular framework for
  SID-based generative recommendation. Systematic ablation of architectural
  components.
- **Joint S&R** (Spotify, RecSys 2025): Bi-encoder multi-task training for SIDs
  that generalize across search and recommendation.

*Note: this raw file was reconstructed from the summary embedded in
`wiki/sources/tiger-transformer-index-generative-recommenders.md` (no separate
raw fetch was saved at original ingest time, 2026-06-09).*
