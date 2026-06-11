---
title: "DeepFM: A Factorization-Machine based Neural Network for CTR Prediction"
type: "source_summary"
sources:
  - "web/deepfm-factorization-machine-deep-learning-ctr.md"
source_url: "https://arxiv.org/abs/1703.04247"
status: "current"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# DeepFM: A Factorization-Machine based Neural Network for CTR Prediction

**Authors:** Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, Xiuqiang He (Huawei Noah's Ark Lab)

**Venue:** IJCAI 2017 (submitted March 13, 2017; arXiv:1703.04247)

**Source type:** `peer_reviewed`

---

## Overview

DeepFM addresses the **feature-interaction** problem common to CTR (and CVR)
prediction: low-order interactions (FM's strength), high-order interactions
(DNNs' strength), and Wide & Deep's reliance on hand-engineered cross-feature
inputs for its wide component
[[raw/web/deepfm-factorization-machine-deep-learning-ctr.md]].

## Architecture

DeepFM is an end-to-end model with two components sharing a single embedding
layer:

- **FM component** — models order-1 and order-2 (pairwise) feature
  interactions directly from the shared embeddings, replacing Wide & Deep's
  manually-engineered wide component.
- **Deep component** — a standard feed-forward DNN over the same embeddings,
  capturing higher-order, implicit interactions.

The two components' outputs are summed and passed through a sigmoid for the
final prediction. Because both halves consume the same embeddings and require
no manual cross-feature engineering, DeepFM trains end-to-end
[[raw/web/deepfm-factorization-machine-deep-learning-ctr.md]].

## Key Results

On benchmark and commercial (Huawei App Store) datasets, DeepFM outperformed
logistic regression, standalone FM, and Wide & Deep on CTR AUC/Logloss while
avoiding Wide & Deep's separate feature-engineering pipeline
[[raw/web/deepfm-factorization-machine-deep-learning-ctr.md]].

## Relevance to Ads Ranking

DeepFM is one of the standard **feature-interaction backbone architectures**
for the CTR/CVR towers inside production ranking models — it answers *what
network computes pCTR/pCVR from raw features*, complementary to ESMM's
entire-space framing of *which population the CVR tower trains on*
[[wiki/sources/esmm-entire-space-multi-task-model.md]].

## Related Pages

- [[wiki/sources/esmm-entire-space-multi-task-model.md]]
- [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
- [[wiki/synthesis/how-do-ad-systems-predict-conversions.md]]
