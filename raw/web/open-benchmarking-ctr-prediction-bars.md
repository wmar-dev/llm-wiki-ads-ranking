# Open Benchmarking for Click-Through Rate Prediction (BARS)

**Source URL:** https://arxiv.org/abs/2009.05794
**Source type:** peer_reviewed

---

## Overview

BARS (Benchmarks for Ads/Recommender Systems) is an open, reproducible
benchmarking framework for CTR prediction models. It evaluates shallow
(logistic regression, FM) and deep (Wide & Deep, DeepFM, DCN, xDeepFM,
FiBiNET, AutoInt, etc.) architectures under a unified, exhaustively-tuned
protocol on standard sparse, high-cardinality datasets (Criteo, Avazu).

## Key results: LR vs. deep models

Both Criteo and Avazu are extremely sparse, high-cardinality categorical
datasets with millions of distinct feature values.

**Criteo (40-dim embeddings):**

| Model | Logloss | AUC |
|---|---|---|
| LR | 0.4566 | 79.36% |
| DeepFM | 0.4378 | 81.41% |
| DCN | 0.4378 | 81.41% |
| xDeepFM | 0.4375 | 81.44% |

**Avazu (40-dim embeddings):**

| Model | Logloss | AUC |
|---|---|---|
| LR | 0.3799 | 78.04% |
| DeepFM | 0.3702 | 79.62% |
| xDeepFM | 0.3697 | 79.67% |
| FiBiNET | 0.3675 | 80.03% |

Deep cross/factorization-based architectures (DeepFM, DCN, xDeepFM, FiBiNET)
consistently outperform a plain LR baseline by roughly 1.5-2.0 absolute AUC
points (and correspondingly lower logloss) on both datasets, despite the
extreme feature sparsity.

## Sparsity-accuracy discussion

The paper does not frame its results as an explicit "sparsity vs. accuracy"
tradeoff curve. It does note that after exhaustive, fair hyperparameter
tuning, the *differences among modern deep architectures* (DeepFM, xDeepFM,
DCN, FiBiNET, AutoInt, etc.) become small relative to each other — much of
the "new model beats prior SOTA" gap reported in original papers shrinks once
baselines are tuned equally hard. This convergence is among deep models only;
the gap between deep models and the linear LR baseline persists even on the
sparsest datasets tested.

## Caveats

- The LR baseline here is plain L2-regularized logistic regression within the
  BARS framework, not the production FTRL-Proximal system from McMahan et al.
  (2013). FTRL-Proximal with L1 regularization produces a similarly sparse
  linear model class, so the LR-vs-deep gap is informative for that
  comparison, but not a direct substitute.
- The paper's headline message ("many claimed deep-model gains shrink under
  fair tuning") concerns deep-vs-deep comparisons, not the linear-vs-deep
  gap, which remains large and consistent.
- The benchmark does not test the billions-of-coefficients, streaming
  online-learning regime that motivated FTRL-Proximal.
