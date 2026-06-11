---
title: "Open Benchmarking for Click-Through Rate Prediction (BARS)"
type: "source_summary"
sources:
  - "web/open-benchmarking-ctr-prediction-bars.md"
source_url: "https://arxiv.org/abs/2009.05794"
status: "current"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# Open Benchmarking for Click-Through Rate Prediction (BARS)

**Authors:** Jieming Zhu, Jinyang Liu, Shuai Yang, Qi Zhang, Xiuqiang He — arXiv:2009.05794

**Source type:** `peer_reviewed`

## Summary

BARS is a reproducible, exhaustively-tuned benchmark comparing shallow
(logistic regression, FM) and deep (Wide & Deep, DeepFM, DCN, xDeepFM,
FiBiNET, AutoInt, etc.) CTR prediction architectures on standard sparse,
high-cardinality datasets (Criteo, Avazu)
[[raw/web/open-benchmarking-ctr-prediction-bars.md]].

## Key Claims

| Claim | Status |
|---|---|
| On Criteo (40-dim embeddings), LR scores 79.36% AUC / 0.4566 logloss vs. DeepFM/DCN at 81.41% AUC / 0.4378 logloss | Stated (Table 3) |
| On Avazu (40-dim embeddings), LR scores 78.04% AUC / 0.3799 logloss vs. xDeepFM/FiBiNET at ~79.7-80.0% AUC / ~0.367-0.370 logloss | Stated (Table 3) |
| Deep cross/factorization architectures outperform a plain LR baseline by ~1.5-2.0 absolute AUC points on both datasets, despite extreme feature sparsity (millions of features) | Stated |
| After exhaustive, fair hyperparameter tuning, differences *among* modern deep architectures shrink relative to their originally-published gaps | Stated |
| The deep-vs-linear AUC gap persists even at the highest feature-sparsity levels tested — sparsity itself does not appear to favor LR | Inference |

## Relevance to Ads Ranking

This directly addresses the
[[wiki/sources/ad-click-prediction-view-from-the-trenches.md]] open question
on how DLRM/DCN-style deep CTR models compare with the FTRL-Proximal (linear,
L1-sparse) approach on sparsity-accuracy tradeoffs: even on the sparsest
standard CTR benchmarks, deep cross-interaction architectures retain a
consistent ~1.5-2 AUC-point advantage over a linear baseline. BARS does not
benchmark FTRL-Proximal itself (its LR baseline is L2-regularized, not online
FTRL with L1), but FTRL-Proximal's L1 term produces a model in the same
sparse-linear class, so the gap is informative
[[wiki/synthesis/model-structures-for-pcvr.md]].

## Open Questions

- Open question: BARS does not benchmark FTRL-Proximal itself, and does not
  evaluate the extreme feature-cardinality / streaming online-learning regime
  (billions of coefficients, continuous updates) that motivated FTRL-Proximal
  in McMahan et al. (2013) — whether the ~1.5-2 AUC-point deep-model
  advantage holds at that scale, or whether deep models' embedding tables
  become operationally impractical first, is not addressed.

## Related Pages

- [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
- [[wiki/synthesis/model-structures-for-pcvr.md]]
- [[wiki/sources/deepfm-factorization-machine-deep-learning-ctr.md]]
