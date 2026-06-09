---
title: "Meta's Generative Ads Model (GEM)"
type: "source_summary"
sources:
  - "web/meta-gem-ads-foundation-model.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# Meta's Generative Ads Model (GEM)

**Source:** Engineering at Meta

**URL:** [engineering.fb.com](https://engineering.fb.com/2025/11/10/ml-applications/metas-generative-ads-model-gem-the-central-brain-accelerating-ads-recommendation-ai-innovation/)

**Source type:** `other` (official Meta engineering blog)

---

Meta's largest RecSys foundation model, trained at LLM scale across thousands of GPUs. Wukong-based architecture with stackable factorization machines, cross-layer attention, InterFormer for cross-feature learning. Teacher-student architecture: GEM teaches downstream vertical models via knowledge distillation, representation learning, and parameter sharing (2× effectiveness of standard distillation). +5% conversions Instagram, +3% Facebook Feed (Q2 2025). 4× efficiency vs prior ranking models.
