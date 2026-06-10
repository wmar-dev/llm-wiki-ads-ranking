---
title: "LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation"
type: "source_summary"
sources:
  - "web/llatte-scaling-laws-recommendation.md"
status: "current"
source_type: peer_reviewed
ingest_count: 1
created: "2026-06-09"
last_updated: "2026-06-09"
---

# LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation

**Source:** arXiv — [LLaTTE (LLM-Style Latent Transformers for Temporal Events)](https://arxiv.org/html/2601.20083v1)

**Date:** January 2026

Establishes that recommendation sequence models follow predictable power-law scaling similar to LLMs. Key findings: semantic features are a prerequisite for scaling (bend the scaling curve); model width must be sufficient before depth scaling becomes effective; upstream improvements transfer to downstream ranking (~50% transfer ratio). Production deployment at Meta: 4.3% conversion uplift on Facebook Feed and Reels using a two-stage architecture with a 45× larger upstream user model. Deployed as Meta's largest user model.
