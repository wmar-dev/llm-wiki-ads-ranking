---
title: "What Are Ways of Predicting Uncertainty in ML Models and Ads Systems?"
type: "synthesis"
sources:
  - "web/survey-uncertainty-deep-neural-networks-gawlikowski.md"
  - "web/ad-click-prediction-view-from-the-trenches.md"
  - "web/bayesian-deep-learning-ctr-uncertainty-quantification.md"
  - "web/linucb-contextual-bandit-news-recommendation.md"
status: "current"
created: "2026-06-12"
last_updated: "2026-06-12"
---

# What Are Ways of Predicting Uncertainty in ML Models and Ads Systems?

"Uncertainty" in a model's output answers a different question than the
prediction itself: not just *what* is the predicted CTR/CVR/reward, but *how
much should we trust that number*. [[wiki/sources/survey-uncertainty-deep-neural-networks-gawlikowski.md]]
*(peer_reviewed)* frames this with a foundational distinction:

- **Epistemic (model) uncertainty** — uncertainty from the model itself
  (limited training data, model misspecification). In principle **reducible**
  with more data or a better model — and *this* is the kind of uncertainty
  that's useful for **exploration** decisions (try the thing we're unsure
  about).
- **Aleatoric (data) uncertainty** — irreducible noise in the
  data-generating process itself (e.g., two users with identical features who
  genuinely click at different rates). No amount of additional data removes
  this.

Ads systems care about both: epistemic uncertainty drives **exploration**
(bandits, Smart Bidding Exploration), while aleatoric uncertainty and
**calibration** drive whether a predicted pCTR/pCVR can be plugged directly
into an auction's expected-value formula
([[wiki/synthesis/what-is-ad-rank.md]]).

## General ML Methods for Uncertainty Quantification

[[wiki/sources/survey-uncertainty-deep-neural-networks-gawlikowski.md]]
*(peer_reviewed)* groups UQ methods for deep models into four families:

| Method family | How it works | Cost | Captures |
|---|---|---|---|
| **Bayesian NN / MC dropout** | Treat weights as distributions; MC dropout reinterprets dropout as a variational posterior, sampled via T stochastic forward passes | T forward passes per prediction | Epistemic (+ can decompose epistemic/aleatoric via mutual information/entropy) |
| **Deep ensembles** | Train N independent models; spread across predictions = uncertainty | N forward passes (and N training runs) | Epistemic |
| **Single deterministic (internal/external)** | One forward pass; either the network outputs distribution parameters directly (e.g., evidential deep learning), or an auxiliary estimator runs alongside an unmodified model | ~1x (same as plain prediction) | Varies — often can't cleanly separate epistemic/aleatoric |
| **Test-time augmentation** | Apply multiple input transforms to one model; variance across outputs = uncertainty | 1x training, Kx inference (K = #augmentations) | Mostly aleatoric (sensitivity to input perturbation) |
| **Calibration (temp/Platt/isotonic scaling)** | Post-hoc remap raw scores so predicted confidence matches observed accuracy; measured via reliability diagrams / Expected Calibration Error | ~free at inference (one extra function) | Neither directly — corrects the *absolute scale* of an existing prediction |

Bayesian methods and ensembles are the "gold standard" for principled
uncertainty but multiply inference cost by the sample/ensemble size — a
direct conflict with the tight latency budgets ad-ranking systems operate
under [[wiki/synthesis/what-is-the-latency-budget-for-ad-ranking.md]]. This
tension is exactly why ad systems have developed **cheaper, specialized**
alternatives to the general-purpose methods above.

![predicting-uncertainty-in-ads-ml-models-diagram-1](/assets/predicting-uncertainty-in-ads-ml-models-diagram-1.svg)

## Ads-System-Specific Approaches

### 1. FTRL-Proximal's Per-Feature Uncertainty Score

Google's production CTR system computes a heuristic confidence measure in a
**single sparse dot product** — the same cost as the prediction itself:

```
u(x) = alpha * eta . x
```

This upper-bounds how much the model's log-odds score would change if it
observed one more training example with features x. It was validated against
a ground-truth model trained on re-labeled data and **performed comparably to
bootstrapping with 32 models — at a fraction of the cost**
[[wiki/sources/ad-click-prediction-view-from-the-trenches.md]] *(peer_reviewed)*.
In the Gawlikowski taxonomy, this is a **single deterministic, external**
method: it bolts an uncertainty estimate onto an unmodified linear model
without retraining or sampling.

### 2. Monte Carlo Dropout for Deep CTR Models

[[wiki/sources/bayesian-deep-learning-ctr-uncertainty-quantification.md]]
*(peer_reviewed)* applies MC dropout — T stochastic forward passes with
dropout active at inference — to deep CTR models, decomposing predictive
uncertainty into **epistemic** (mutual information across the T passes) and
**aleatoric** (entropy of the averaged prediction) components. This improved
Logloss by 0.19-0.42% and RMSE by 0.07-0.26% over non-dropout baselines, and
uncertainty estimates **shrink as the training set grows** — the expected
epistemic-uncertainty behavior. This is the Bayesian
variational-inference family from the general taxonomy, specialized to CTR.

*Open question (carried from [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]):
no source directly compares FTRL's single-dot-product uncertainty score
against MC-dropout's T-forward-pass estimate on the same dataset, or whether
MC dropout's cost is tractable at Google/Meta-scale serving QPS.*

### 3. Bandit Confidence Bounds (LinUCB)

[[wiki/synthesis/what-is-linucb.md]] shows that LinUCB's exploration bonus,
`alpha * sqrt(x^T A^-1 x)`, **is** a closed-form uncertainty estimate: A^-1 is
the posterior covariance of a Bayesian linear regression over per-arm
rewards, so the bonus is literally the posterior predictive standard
deviation at the current context
[[wiki/sources/linucb-contextual-bandit-news-recommendation.md]]
*(peer_reviewed)*. This is the **Laplace-approximation** Bayesian family,
specialized to a linear model where the "Gaussian around the MAP estimate" is
exact rather than approximate. Crucially, this uncertainty estimate isn't
just reported — it directly **drives the exploration decision**: arms with
high uncertainty get a selection boost, which is how
[[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] frames creative
selection, budget allocation, and (per
[[wiki/concepts/multi-armed-bandit-algorithms.md]]) Thompson Sampling's
posterior-sampling alternative.

### 4. Calibration: Isotonic Regression on Predicted CTR

Even a well-ranked model can be miscalibrated in absolute terms — e.g.,
systematically predicting 3% CTR for impressions that actually convert at 5%.
McMahan et al. fit a **piecewise-linear, monotonically increasing** isotonic
regression function tau(p) mapping predicted CTR to observed CTR, which
"significantly reduced bias at both high and low prediction ranges"
[[wiki/sources/ad-click-prediction-view-from-the-trenches.md]] *(peer_reviewed)*.
This is exactly the isotonic-regression calibration method in the general
taxonomy — necessary because **absolute** pCTR/pCVR values feed directly into
the eCPM/LTV computation in [[wiki/synthesis/what-is-ad-rank.md]], where a
miscalibrated probability directly distorts ranking and pricing, not just
ranking order.

### 5. Population-Level Uncertainty: Confidence Intervals for Experiments

The methods above quantify uncertainty in a **single prediction**. A
different but related question is uncertainty in an **aggregate metric**
(e.g., "is this model's CTR lift in the A/B test real?"). [[wiki/synthesis/confidence-interval-methods.md]]
covers this side: t-test/Wald intervals, the delta method for ratio metrics,
bootstrap variants, and — notably — **Bayesian credible intervals** and
**confidence sequences**, which the page notes are explicitly used "in
specialized settings (e.g., bandit algorithms, hierarchical modeling)" and
are "valid for multi-arm bandits." This is the bridge between per-prediction
uncertainty (sections 1-4 above) and the population-level uncertainty
framework used to validate that a model change actually improved things
[[wiki/synthesis/how-ab-tests-work.md]].

## Summary Table

| Approach | Uncertainty type | Inference cost | Used for |
|---|---|---|---|
| FTRL uncertainty score | Epistemic (per-feature) | 1 extra dot product | Confidence-aware serving decisions at billion-coefficient scale |
| MC dropout (deep CTR) | Epistemic + aleatoric (decomposed) | T forward passes | Research-stage deep CTR uncertainty |
| LinUCB confidence bound | Epistemic (per-arm, Bayesian linear) | O(d^2) incremental update | Driving exploration in contextual bandits |
| Isotonic regression calibration | Calibration (not epistemic/aleatoric per se) | ~free | Correcting absolute pCTR/pCVR for auction pricing |
| Bayesian credible intervals / CS | Population-level (metric estimate) | Standard CI/CS computation | A/B test validity, bandit final read-outs |

## Related Pages

- [[wiki/sources/survey-uncertainty-deep-neural-networks-gawlikowski.md]]
- [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
- [[wiki/sources/bayesian-deep-learning-ctr-uncertainty-quantification.md]]
- [[wiki/synthesis/what-is-linucb.md]]
- [[wiki/concepts/multi-armed-bandit-algorithms.md]]
- [[wiki/synthesis/confidence-interval-methods.md]]
- [[wiki/synthesis/what-is-ad-rank.md]]
