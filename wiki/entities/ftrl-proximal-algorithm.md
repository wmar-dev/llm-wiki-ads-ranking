---
title: "FTRL-Proximal Algorithm"
type: "entity"
sources:
  - "web/ad-click-prediction-view-from-the-trenches.md"
status: "draft"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# FTRL-Proximal Algorithm

**FTRL-Proximal** (Follow The Regularized Leader with Proximal updates) is an online learning algorithm for generalized linear models that combines the prediction accuracy of online gradient descent (OGD) with the sparsity of Regularized Dual Averaging (RDA). Without L1 regularization it is identical to OGD; with L1 regularization it produces significantly sparser models without accuracy loss [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]].

## Algorithm

For each round t, given gradient g_t ∈ R^d and per-coordinate learning rate schedule σ_s:

```
w_{t+1} = argmin_w (g_{1:t} · w + ½ Σ_{s=1}^{t} σ_s ‖w − w_s‖²₂ + λ₁‖w‖₁)
```

### Per-Coordinate Update (Algorithm 1 in McMahan et al., 2013)

```
Input: parameters α, β, λ₁, λ₂
Initialize z_i = 0, n_i = 0 for all i

for t = 1 to T:
    Receive feature vector x_t
    For each i where x_{t,i} ≠ 0:
        w_{t,i} = 0                  if |z_i| ≤ λ₁
        w_{t,i} = -(η_t)(z_i - sign(z_i)λ₁)   otherwise
                  where η_t = 1 / ((β + √n_i)/α + λ₂)
    
    Predict p_t = σ(w_t · x_t)
    Observe label y_t
    
    For each i where x_{t,i} ≠ 0:
        g_i = (p_t - y_t) x_{t,i}                # gradient
        σ_i = (1/α)(√(n_i + g_i²) - √n_i)        # learning rate decay
        z_i ← z_i + g_i - σ_i w_{t,i}            # accumulated + proximal correction
        n_i ← n_i + g_i²                         # gradient sum of squares
```

## Properties

| Property | Value |
|---|---|
| **Sparsity** | Excellent — significantly outperforms RDA, FOBOS, truncated gradient |
| **Accuracy** | Matches OGD (same as OGD at λ₁ = 0) |
| **Memory per coefficient** | One float (z_i) + one float (n_i) for full version; one float for count-based version |
| **Regularization** | L1 (sparsity) + L2 (shrinkage) |
| **Learning rates** | Per-coordinate: η_{t,i} = α / (β + √n_{t,i}) |
| **Convergence** | Theoretical regret bounds via adaptive online convex optimization |

## Experimental Results

| Method | Non-Zero Coefficients | AucLoss Detriment |
|---|---|---|
| FTRL-Proximal | baseline | baseline |
| RDA | +3% | 0.6% |
| FOBOS | +38% | 0.0% |
| OGD-Count | +216% | 0.0% |

Per-coordinate learning rates reduced AucLoss by 11.2% versus a global learning rate [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]].

## Relationship

- [[wiki/entities/google-ctr-prediction-system.md]] — production system using FTRL-Proximal
- [[wiki/concepts/web-scale-learning.md]] — scale paradigm where FTRL-Proximal operates
