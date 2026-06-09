# Meta's Generative Ads Model (GEM): The Central Brain Accelerating Ads Recommendation AI Innovation

**Source:** Engineering at Meta (Meta Platforms, Inc.)
**URL:** https://engineering.fb.com/2025/11/10/ml-applications/metas-generative-ads-model-gem-the-central-brain-accelerating-ads-recommendation-ai-innovation/
**Type:** Official engineering blog post
**Date:** November 10, 2025

---

Meta's foundation model for ads recommendation. Largest RecSys foundation model in the industry, trained at LLM scale across thousands of GPUs.

**Architecture**: Wukong-based with stackable factorization machines + cross-layer attention. Processed sequence features (activity history) and non-sequence features (user/ad attributes) with customized attention. InterFormer for cross-feature learning preserving full sequence information.

**Pyramid-parallel structure**: Multiple parallel interaction modules stacked pyramidally for complex user-ad relationships at scale. Processes sequences of thousands of events.

**Multi-domain learning**: Cross-surface learning (Facebook, Instagram, WhatsApp) while maintaining domain-specific predictions.

**Knowledge Transfer**: Teacher-student architecture — GEM teaches downstream vertical models via:
- Knowledge distillation (with Student Adapter for stale-supervision correction)
- Representation learning (semantically aligned features)
- Parameter sharing (selective component reuse by latency-sensitive VMs)

**Direct transfer** to major VMs; **hierarchical transfer** distills through domain-specific FMs first. 2× effectiveness of standard knowledge distillation.

**Training**: 23× FLOPs increase with 16× more GPUs; 1.43× MFU improvement. Multi-dimensional parallelism, custom GPU kernels, NCCLX for SM-free communication collectives. 5× startup time reduction; 7× PyTorch 2.0 compilation via caching.

**Results**: +5% conversions Instagram, +3% Facebook Feed (Q2). 4× efficiency vs prior ranking models. Q3 architecture improvements doubled ROI per unit of data/compute.
