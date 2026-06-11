---
title: "Progressive Layered Extraction (PLE): A Novel MTL Model for Personalized Recommendations"
type: "source_summary"
sources:
  - "web/ple-progressive-layered-extraction-multitask.md"
source_url: "https://dl.acm.org/doi/10.1145/3383313.3412236"
status: "current"
source_type: "blog_post"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# Progressive Layered Extraction (PLE): A Novel MTL Model for Personalized Recommendations

**Authors:** Hongyan Tang, Junning Liu, Ming Zhao, Xudong Gong (Tencent PCG)

**Venue:** RecSys 2020 (14th ACM Conference on Recommender Systems), ACM DOI
10.1145/3383313.3412236

**Source type:** `blog_post` *(the underlying paper is RecSys 2020
peer-reviewed, but the ACM page returned HTTP 403 on two fetch attempts; this
summary is sourced from a third-party blog mirror — see [[raw/web/ple-progressive-layered-extraction-multitask.md]])*

---

## Overview

Multi-task models that jointly predict related objectives (e.g., CTR and CVR,
or click and watch-time) often suffer from the **seesaw phenomenon**
(improving one task degrades another) and **negative transfer** (naive
parameter sharing hurts all tasks when objectives conflict)
[[raw/web/ple-progressive-layered-extraction-multitask.md]].

## Prior Architectures

| Architecture | Mechanism | Limitation |
|---|---|---|
| **Shared-bottom** | Single shared encoder + per-task heads | Prone to negative transfer on conflicting tasks |
| **MMoE** (Multi-gate Mixture-of-Experts) | Shared expert sub-networks + per-task gating networks | Mitigates but doesn't eliminate seesaw/negative transfer — experts remain fully shared |

[[raw/web/ple-progressive-layered-extraction-multitask.md]]

## PLE / CGC Architecture

PLE's **Customized Gate Control (CGC)** module separates **shared experts**
(available to all tasks) from **task-specific experts** (dedicated per task);
each task's gate combines its own experts with the shared pool. PLE stacks
multiple CGC layers with **progressive routing**, so deeper layers
progressively refine shared-vs-task-specific representations and limit
cross-task interference [[raw/web/ple-progressive-layered-extraction-multitask.md]].

## Key Results

- On a ~1B-sample Tencent video recommendation dataset (complicatedly- and
  normally-correlated task pairs), PLE outperformed shared-bottom, MMoE, and
  other SOTA MTL baselines on both tasks simultaneously.
- **Online A/B test**: +2.23% view-count, +1.84% watch time vs. the best prior
  MTL baseline; deployed in Tencent's production video recommender
  [[raw/web/ple-progressive-layered-extraction-multitask.md]].

## Relevance to Ads Ranking

PLE (and MMoE) are the standard production architectures for **jointly
modeling CTR and CVR as related-but-distinct tasks** — orthogonal to ESMM's
entire-space CTR/CVR/CTCVR framing. ESMM solves *sample selection bias* via an
entire-space training signal; MMoE/PLE solve *negative transfer between tasks*
via expert-sharing architecture. Production systems can combine entire-space
training (ESMM) with a PLE-style expert/gating backbone
[[wiki/sources/esmm-entire-space-multi-task-model.md]].

## Related Pages

- [[wiki/sources/esmm-entire-space-multi-task-model.md]]
- [[wiki/sources/deepfm-factorization-machine-deep-learning-ctr.md]]
- [[wiki/synthesis/how-do-ad-systems-predict-conversions.md]]
