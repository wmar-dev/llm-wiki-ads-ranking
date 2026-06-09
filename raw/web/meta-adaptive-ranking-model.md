# Meta Adaptive Ranking Model: Bending the Inference Scaling Curve to Serve LLM-Scale Models for Ads

**Source:** Engineering at Meta (Meta Platforms, Inc.)
**URL:** https://engineering.fb.com/2026/03/31/ml-applications/meta-adaptive-ranking-model-bending-the-inference-scaling-curve-to-serve-llm-scale-models-for-ads/
**Type:** Official engineering blog post
**Date:** March 31, 2026

---

Meta's infrastructure layer for serving LLM-scale ads ranking models at production latency. Key innovations:

1. **Inference-Efficient Model Scaling**: Request-centric architecture computes user signals once per request (not per user-ad pair), transforming scaling from linear to sub-linear. Request-Oriented Computation Sharing shares embeddings across candidates in-GPU-kernel.

2. **Deep Model-System Co-Design**: Selective FP8 quantization via micro-benchmark guided selection; hardware-aware graph/kernel specialization (operator fusion, Grouped GMM, horizontal fusion). Achieves 35% MFU across heterogeneous hardware.

3. **Reimagined Serving Infrastructure**: Multi-card GPU sharding for O(1T) parameter scaling; unified embeddings for memory efficiency; accelerated model loading (<10 min deploys); auto-scaling based on SM utilization.

**Wukong Turbo**: Optimized runtime evolution of the Wukong architecture (stackable factorization machines + sequence learning + cross-layer attention). No-bias training, small parameter delegation (FSDP→DDP), sparsity-based simplification.

**Results**: Launched Instagram Q4 2025. +3% conversions, +5% CTR. O(100ms) bounded latency.
