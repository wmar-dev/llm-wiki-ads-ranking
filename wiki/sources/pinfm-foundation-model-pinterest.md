---
title: "PinFM: Foundation Model for User Activity Sequences at Pinterest"
type: "source_summary"
sources:
  - "web/pinfm-foundation-model-pinterest.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# PinFM: Foundation Model for User Activity Sequences at Pinterest

**Source:** Chen et al., Pinterest Labs

**URL:** [arxiv.org/abs/2507.12704](https://arxiv.org/abs/2507.12704)

**Source type:** `peer_reviewed` (ACM RecSys 2025, oral spotlight)

---

Pinterest's first foundation model for user activity sequences. A 20B+ parameter transformer pretrained on extensive user activity data, then fine-tuned for downstream ranking applications. Introduces the Deduplicated Cross-Attention Transformer (DCAT) which separates context encoding (one pass per request) from candidate crossing (cross-attention with cached KV), achieving 600% throughput improvement on internal data. Key results: 20% increase in engagement with new items, deployed for 500M+ users across multiple applications. Represents a 100x increase in transformer dense parameter counts and 10x increase in model dimension over prior Pinterest systems.
