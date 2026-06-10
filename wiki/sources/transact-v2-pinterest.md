---
title: "TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation"
type: "source_summary"
sources:
  - "web/transact-v2-pinterest.md"
source_url: "https://arxiv.org/abs/2506.02267"
status: "current"
source_type: "other"
processing_status: "processed"
ingest_count: 1
created: "2026-06-09"
last_updated: "2026-06-09"
---

# TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation

**Authors:** Xue Xia, Saurabh Vishwas Joshi, Kousik Rajesh, Kangnan Li, Yangyi Lu, Nikil Pancha, Dhruvil Deven Badani, Jiajing Xu, Pong Eksombatchai (Pinterest)

**Submitted:** arXiv, June 2, 2025 (preprint)

**Source type:** `other` (industry/academic preprint)

## Overview

TransActV2 is Pinterest's production CTR ranking model for the Homefeed, extending the original TransAct model with **lifelong user action sequences** (up to ~16,000 actions — a ~160x scale-up over real-time-only sequences) and a **Next Action Loss (NAL)** auxiliary objective integrated into point-wise ranking [[raw/web/transact-v2-pinterest.md]].

## Key Findings

- **Offline**: RT + Lifelong-sequence + NAL improves **HIT@3/repin by +13.31%** and reduces **HIT@3/hide by 11.25%** versus an RT-only sequence baseline.
- **Online A/B test** (vs. RT-only TransAct): **+6.35% Homefeed Repin Volume**, **−12.80% Homefeed Hide Volume**, **+0.45% Impression Diversity**, **+1.41% Time Spent on App**.
- **Infrastructure**: scalable low-latency serving built specifically to handle 16K-action sequences in real-time ranking.

## Relationship to PinFM

TransActV2 (this paper) and PinFM ([[wiki/sources/pinfm-foundation-model-pinterest.md]]) are **not benchmarked against each other** in either paper. They address different parts of Pinterest's stack:

- **TransActV2** is a production point-wise ranking model for one surface (Homefeed), evaluated on HIT@k offline metrics and online engagement A/B tests (repins, hides, diversity, time spent).
- **PinFM** is a 20B+ parameter pretrained foundation model for user activity sequences, fine-tuned per-surface, evaluated primarily on engagement-with-new-items (+20%) and serving throughput (DCAT, +600%).

The two were developed in parallel as **complementary components** rather than competing solutions — Pinterest's broader foundation-model ecosystem (PinFM, PinRec, UniPinRec) is positioned as pretraining infrastructure that surface-specific ranking models like TransActV2 could eventually consume, but no published source quantifies that integration or a "marginal improvement" of one over the other [[raw/web/transact-v2-pinterest.md]].
