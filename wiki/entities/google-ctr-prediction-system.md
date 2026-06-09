---
title: "Google CTR Prediction System"
type: "entity"
sources:
  - "web/ad-click-prediction-view-from-the-trenches.md"
status: "draft"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# Google CTR Prediction System

Google's production system for predicting ad click-through rates in sponsored search advertising, as described in McMahan et al. (KDD 2013). Serves billions of predictions per day using an online learning architecture with per-coordinate learning rates and aggressive memory optimization [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]].

## Architecture

### Online Learning Pipeline

![entities-google-ctr-prediction-system-diagram-1](/assets/entities-google-ctr-prediction-system-diagram-1.svg)

### Key Components

| Component | Description | Details |
|---|---|---|
| **Feature vector** | Extreme sparse, billions of dimensions | Hundreds of non-zero values per example |
| **Model** | Logistic regression with L1 + L2 regularization | Single-layer (not deep); billions of coefficients |
| **Learning algorithm** | FTRL-Proximal with per-coordinate rates | Combines OGD accuracy with RDA sparsity |
| **Training data** | Streaming from Photon system | Billions of daily events |
| **Serving** | Replicated to multiple data centers | Sparsification at serving time |
| **Calibration** | Isotonic regression correction | Maps predicted CTR to observed CTR |

## Important Algorithms

### FTRL-Proximal

The Follow The (Proximally) Regularized Leader algorithm uses the update:

w_{t+1} = argmin_w (g_{1:t} · w + ½ Σ_{s=1}^{t} σ_s ‖w − w_s‖²₂ + λ₁‖w‖₁)

Stores z ∈ R^d (accumulated gradient minus accumulated σ_s w_s) rather than w directly, enabling effective L1 regularization. At λ₁ = 0, produces identical results to online gradient descent. With λ₁ > 0, achieves significantly better sparsity than RDA, FOBOS, or truncated gradient [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]].

### Per-Coordinate Learning Rates

Each feature i uses η_{t,i} = α / (β + √(n_{t,i})) where n_{t,i} = Σ_{s=1}^{t} g_{s,i}². This means rare features maintain higher learning rates longer. Reduced AucLoss by 11.2% versus a global learning rate [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]].

## Memory Optimization Stack

The system combines multiple techniques to handle billion-coefficient models:

1. **L1 regularization** during training for serving-time sparsity
2. **Probabilistic feature inclusion** (Bloom filter, n=1) — 55% RAM savings, 0.003% AucLoss cost
3. **q2.13 fixed-point encoding** — 16-bit instead of 64-bit — 75% RAM savings, no measurable accuracy loss
4. **Shared hash tables** for training similar model variants — amortized key storage
5. **Single Value Structure** — shared coefficients across variants — order-of-magnitude RAM savings
6. **Count-based learning rates** — replace full gradient sum with PN/(N+P) approximation
7. **Subsampling** — include all clicked queries, fraction r of unclicked — importance weight correction

## Evaluation

Primary metrics: AucLoss (1 − AUC) and LogLoss. Progressive validation (online loss) replaces cross-validation — uses 100% of data for both training and testing. GridViz interactive visualization enables multi-dimensional performance analysis across hundreds of data slices [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]].

## Relationship to Other Entities

- [[wiki/entities/meta-ads-ranking-system.md]] — Meta's ads ranking system (different architecture, similar scale)
- [[wiki/sources/google-ad-rank-briefing.md]] — Google's auction and Ad Rank formula context
- [[wiki/sources/overlapping-experiment-infrastructure.md]] — Google's experimentation platform (separate system)
