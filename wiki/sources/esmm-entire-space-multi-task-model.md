---
title: "Entire Space Multi-Task Model (ESMM) for Post-Click CVR Prediction"
type: "source_summary"
sources:
  - "web/esmm-entire-space-multi-task-model.md"
source_url: "https://arxiv.org/abs/1804.07931"
status: "current"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# Entire Space Multi-Task Model (ESMM) for Post-Click CVR Prediction

**Authors:** Xiao Ma, Liqin Zhao, Guan Huang, Zhi Wang, Zelin Hu, Xiaoqiang Zhu, Kun Gai (Alibaba)

**Venue:** SIGIR 2018 (submitted April 21, 2018)

**Source type:** `peer_reviewed`

---

## Overview

ESMM addresses two problems specific to **post-click conversion rate (CVR)**
prediction that don't affect CTR prediction in the same way: **sample
selection bias** (a CVR model trained only on clicked impressions is applied
at inference time to the entire impression space — a train/serve distribution
mismatch) and **data sparsity** (conversions are far rarer than clicks, so the
clicked-only training set is orders of magnitude smaller)
[[raw/web/esmm-entire-space-multi-task-model.md]].

## How ESMM Works

ESMM exploits the sequential dependency **impression -> click -> conversion**
by modeling two auxiliary probabilities over the *entire* impression space,
where labels are always defined:

- **CTR** = P(click | impression)
- **CTCVR** = P(click and conversion | impression) = CTR x CVR

The CVR sub-network is a shared component whose output is multiplied by the
CTR tower's output to produce CTCVR. Because CTR and CTCVR labels exist for
every impression (not just clicked ones), gradients for the CVR sub-network
flow from entire-space supervision — eliminating sample selection bias — and
the CVR sub-network shares embedding parameters with the data-rich CTR tower,
mitigating data sparsity via implicit transfer learning
[[raw/web/esmm-entire-space-multi-task-model.md]].

## Key Results

- Evaluated on Taobao production logs and a newly released public benchmark
  (Product dataset) with sequential click->conversion labels — the first
  public dataset of its kind for CVR research.
- ESMM significantly outperformed prior CVR modeling approaches (naive
  clicked-only deep models, oversampling-based DivisionModel) on both
  clicked-impression CVR AUC and entire-space CTCVR AUC
  [[raw/web/esmm-entire-space-multi-task-model.md]].
- The framework is model-agnostic: any architecture can serve as the CTR/CVR
  sub-network base.

## Relevance to Ads Ranking

ESMM (and its descendants, e.g., ESCM2 which adds counterfactual
regularization) is the standard production pattern for **pCVR**, the signal
that feeds oCPM, CPA/ROAS Smart Bidding, and Maximize Conversions strategies
[[wiki/synthesis/what-is-a-conversion.md]]. It is the architectural answer to
*how* a ranking system produces a calibrated conversion probability for every
candidate impression — including the ~99% that were never clicked — rather
than only for the small clicked subset where conversion outcomes are directly
observed.

## Open Questions

- How do production systems combine ESMM-style entire-space multi-task
  architectures with delayed-feedback correction
  [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]] — are these
  trained jointly or as separate stages?

## Related Pages

- [[wiki/synthesis/what-is-a-conversion.md]]
- [[wiki/sources/follow-the-prophet-delayed-feedback-cvr.md]]
- [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
- [[wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md]]
