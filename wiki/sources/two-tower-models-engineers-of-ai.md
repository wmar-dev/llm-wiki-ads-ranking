---
title: "Two-Tower Models: The Architecture Powering Google, TikTok, and YouTube"
type: "source_summary"
sources:
  - "web/two-tower-models-engineers-of-ai.md"
status: "draft"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Two-Tower Models: The Architecture Powering Google, TikTok, and YouTube

**Source:** EngineersOfAI

**URL:** [engineersofai.com](https://engineersofai.com/docs/ml/recommender-systems/Two-Tower-Models)

**Source type:** `other` (technical education)

---

A comprehensive tutorial on the two-tower architecture for large-scale recommendation retrieval. Covers the architectural constraint (independent user and item towers → precomputable item embeddings → billion-scale ANN search), training with in-batch negatives (InfoNCE loss, batch size 1024-4096), sampling bias correction (Yi et al. 2019: subtract log q(i) from logits), and the production retrieval-to-ranking pipeline. Includes PyTorch implementation with user/item tower classes, FAISS index building (IVF-PQ), Recall@K evaluation, and serving example. Notes foundational papers: DSSM (2013, Microsoft), YouTube DNN (2016, Google), sampling-bias-corrected neural modeling (2019, Yi et al.), FAISS (2021, Meta). Covers common mistakes: forgetting bias correction, using the same model for retrieval and ranking, item embedding staleness, and small batch sizes. Includes fresh content handling via content-based warm start, streaming incremental updates, and exploration injection.
