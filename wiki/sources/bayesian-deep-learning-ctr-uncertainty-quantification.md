---
title: "Click-through Rate Prediction and Uncertainty Quantification Based on Bayesian Deep Learning"
type: "source_summary"
sources:
  - "web/bayesian-deep-learning-ctr-uncertainty-quantification.md"
source_url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC10048037/"
status: "current"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# Click-through Rate Prediction and Uncertainty Quantification Based on Bayesian Deep Learning

**Source:** PMC10048037

**Source type:** `peer_reviewed`

## Summary

Applies Monte Carlo (MC) dropout — dropout kept active at inference time, T
stochastic forward passes averaged — as a tractable variational
approximation to a Bayesian posterior over a deep CTR model's weights,
decomposing predictive uncertainty into epistemic (parameter) and aleatoric
(data-noise) components via mutual information and entropy
[[raw/web/bayesian-deep-learning-ctr-uncertainty-quantification.md]].

## Key Claims

| Claim | Status |
|---|---|
| MC dropout (T stochastic forward passes, averaged) approximates a Bayesian posterior without explicit Bayesian layers | Stated |
| Epistemic uncertainty = mutual information across stochastic predictions; aleatoric uncertainty = entropy of the averaged prediction | Stated |
| MC dropout improves Logloss by 0.19-0.42% and RMSE by 0.07-0.26% vs. non-dropout baselines | Stated (Table 2) |
| Uncertainty estimates decrease as training-set size grows | Stated |
| No comparison to FTRL-Proximal's per-coordinate uncertainty score, and no calibration-curve evaluation | Stated (absence) |

## Relevance to Ads Ranking

This partially addresses the
[[wiki/sources/ad-click-prediction-view-from-the-trenches.md]] open question
on whether the FTRL-Proximal **uncertainty score** (a per-feature,
gradient-sum-derived confidence measure computable as a single sparse dot
product) generalizes to deep, non-linear CTR models: uncertainty
quantification *does* generalize to deep CTR architectures, but via a
structurally different mechanism — a sampling-based, whole-network
distributional measure (MC dropout), not a per-feature closed-form statistic.
The two approaches answer related but different questions (per-feature
confidence vs. whole-prediction confidence), and the paper does not establish
whether one can be derived from, or substitute for, the other.

## Open Questions

- Open question: no source found directly compares FTRL-Proximal's
  per-coordinate uncertainty score against MC-dropout-style (or other
  Bayesian) uncertainty in a deep CTR model on the same dataset, nor examines
  whether MC-dropout uncertainty remains tractable or meaningful at the
  extreme feature-sparsity and billions-of-parameters scale that motivated
  the original per-coordinate score (T forward passes per prediction may be
  prohibitively expensive at Google/Meta-scale serving QPS).

## Related Pages

- [[wiki/synthesis/predicting-uncertainty-in-ads-ml-models.md]] — MC dropout in the broader taxonomy of UQ methods used in ads/ML systems
- [[wiki/sources/ad-click-prediction-view-from-the-trenches.md]]
- [[wiki/synthesis/confidence-interval-methods.md]]
- [[wiki/synthesis/model-structures-for-pcvr.md]]
