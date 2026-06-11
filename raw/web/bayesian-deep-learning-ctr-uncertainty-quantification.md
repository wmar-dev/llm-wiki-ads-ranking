# Click-through Rate Prediction and Uncertainty Quantification Based on Bayesian Deep Learning

**Source URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10048037/
**Source type:** peer_reviewed

---

## Method: Monte Carlo dropout for uncertainty

The paper applies **Monte Carlo (MC) dropout** — keeping dropout active at
inference time and running T stochastic forward passes — as a tractable
variational approximation to a Bayesian posterior over a deep CTR model's
weights, with no explicit Bayesian layers required:

```
prediction = (1/T) * sum_{t=1}^{T} Softmax(f_omega_hat_t(x*))
```

Predictive uncertainty is decomposed into:

- **Epistemic uncertainty** (model/parameter uncertainty) — measured via
  mutual information across the T stochastic predictions.
- **Aleatoric uncertainty** (irreducible data noise) — quantified via the
  information entropy of the averaged prediction.

## Results

- MC dropout improves Logloss by 0.19-0.42% and RMSE by 0.07-0.26% versus
  non-dropout baselines (Table 2).
- Uncertainty estimates decrease as training-set size grows (more data ->
  lower epistemic uncertainty), consistent with the Bayesian interpretation.
- No calibration curves (confidence vs. empirical accuracy) or
  error-prediction analyses are reported.

## Relation to FTRL-Proximal's per-coordinate uncertainty score

The paper does not reference or compare against McMahan et al.'s (2013)
per-coordinate "uncertainty score" u(x) = alpha*eta . x — a single sparse dot
product derived from the per-coordinate sum-of-squared-gradients (Sigma
g_i^2), used as a proxy for how often a feature has been observed.

The two approaches are conceptually distinct:

- FTRL-Proximal's score is a **closed-form, per-feature statistic** computed
  from the online optimizer's own state (gradient-sum accumulators) — cheap
  (one dot product) but tied to a linear model's structure, where each
  feature's contribution to the prediction is additive and separable.
- MC-dropout uncertainty is a **distributional, sampling-based** measure over
  the whole network's output — it does not decompose into a per-feature
  confidence score, and costs T forward passes instead of one dot product.

The paper provides no evidence on whether a per-coordinate-style heuristic
could be extracted from a deep model's embedding tables (e.g., per-embedding
update counts as a confidence proxy), nor whether MC-dropout-style
uncertainty remains tractable or meaningful under the extreme feature-sparsity
regime (millions of rarely-seen features) that motivated the original
FTRL-Proximal uncertainty score. This remains an open gap between the two
literatures.
