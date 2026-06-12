---
title: "A Survey of Uncertainty in Deep Neural Networks"
type: "source_summary"
sources:
  - "web/survey-uncertainty-deep-neural-networks-gawlikowski.md"
status: "current"
created: "2026-06-12"
last_updated: "2026-06-12"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
---

# A Survey of Uncertainty in Deep Neural Networks

**Authors:** Gawlikowski et al. — arXiv:2107.03342 (2021; *Artificial
Intelligence Review*).

A broad taxonomy of uncertainty-quantification (UQ) methods for deep neural
networks, organized around the **epistemic vs. aleatoric** distinction:
epistemic (model) uncertainty is reducible with better models/data; aleatoric
(data) uncertainty is irreducible noise in the data-generating process.

## Method Families

- **Bayesian neural networks**: model parameters as distributions, not point
  estimates. Three approximations: **variational inference** (incl. **Monte
  Carlo dropout** — dropout layers reinterpreted as a Bernoulli variational
  posterior, sampled via repeated stochastic forward passes), **MCMC/SG-MCMC
  sampling** (unbiased but expensive), and **Laplace approximation**
  (post-hoc Gaussian around the MAP estimate using the Hessian).
- **Single deterministic methods**: one forward pass yields an uncertainty
  estimate. **Internal** methods (e.g., Evidential Deep Learning) output
  distribution parameters (e.g., a Dirichlet over class probabilities)
  directly; **external** methods bolt an auxiliary uncertainty estimator onto
  an unmodified base model.
- **Deep ensembles**: train multiple networks independently; the spread
  across members' predictions is the uncertainty signal. Strong empirical
  performance, cost scales with ensemble size.
- **Test-time augmentation**: apply multiple input transforms at inference to
  a single model; prediction variance across transforms is the uncertainty
  estimate.

## Calibration

Confidence scores often don't match true accuracy. Post-hoc fixes:
**temperature scaling** (single learned scalar dividing logits), **Platt
scaling** (fit a sigmoid on raw scores), and **isotonic regression**
(non-parametric monotone mapping). Measured via **reliability diagrams** and
**Expected Calibration Error (ECE)**.

## Relevance to Ads Ranking

This survey's taxonomy gives the general-ML vocabulary for uncertainty methods
that ads systems specialize: [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]'s
FTRL-Proximal **uncertainty score** is a *single deterministic, external*
method (one extra dot product on top of an unmodified linear model);
[[wiki/sources/bayesian-deep-learning-ctr-uncertainty-quantification.md]]'s
**MC dropout** for deep CTR models is the *variational-inference* family
described here; and [[wiki/sources/linucb-contextual-bandit-news-recommendation.md]]'s
LinUCB confidence bound is a closed-form **Bayesian linear** posterior
variance — the Laplace-approximation family specialized to linear models.
McMahan et al.'s **isotonic regression** calibration step for CTR predictions
is exactly the isotonic-regression calibration method described here.

## Related Pages

- [[wiki/synthesis/predicting-uncertainty-in-ads-ml-models.md]]
- [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
- [[wiki/sources/bayesian-deep-learning-ctr-uncertainty-quantification.md]]
- [[wiki/sources/linucb-contextual-bandit-news-recommendation.md]]
