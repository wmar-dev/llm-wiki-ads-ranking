---
title: "How TikTok's Algorithm Really Works: Deep Dive Into the Unsupervised Learning Engine"
type: "source_summary"
sources:
  - "web/tiktok-unsupervised-algorithm-deep-dive.md"
status: "draft"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# How TikTok's Algorithm Really Works: Deep Dive Into the Unsupervised Learning Engine

**Source:** Kingy AI (Curtis Pyke)

**URL:** [kingy.ai](https://kingy.ai/uncategorized/how-tiktoks-algorithm-really-works-a-deep-dive-into-the-unsupervised-learning-engine-behind-the-for-you-page/)

**Source type:** `blog_post`

---

A technical deep-dive arguing that TikTok's FYP is primarily an unsupervised/self-supervised system. Covers the full pipeline: video ingestion (CV, NLP, metadata) → feature vectors → clustering (K-means, hierarchical, DBSCAN, GMM) → embeddings (autoencoders, contrastive learning, two-tower models) → candidate generation (approximate nearest-neighbor) → ranking (multi-task deep model predicting like, completion, share, comment, watch-time). References ByteDance's Monolith paper (arXiv 2022) for real-time training architecture. Reports 30-50% exploitation, with the remainder exploration. Includes a case study of a new user's first 50 swipes, showing how implicit signals reshape embedding coordinates without explicit feedback. Raises concerns about opacity, rabbit holes, and regulatory compliance.
