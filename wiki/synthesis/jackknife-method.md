---
title: "The Jackknife Method"
type: "synthesis"
sources:
  - "web/jackknife-resampling.md"
  - "web/jackknife-delta-method-equivalence.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-09"
---

# The Jackknife Method

The jackknife is a **resampling technique** in statistics used to estimate the bias and variance of an estimator $\hat{\theta}$ without parametric assumptions. It predates the bootstrap and is conceptually simpler: for a sample of size $n$, compute the statistic of interest $n$ times, each time leaving out one observation, yielding $n$ "leave-one-out" estimates $\hat{\theta}_{(1)}, \dots, \hat{\theta}_{(n)}$.

## How It Works

![synthesis-jackknife-method-diagram-1](/assets/synthesis-jackknife-method-diagram-1.svg)

## Key Uses

### Bias correction

The jackknife estimates bias as $\widehat{\text{bias}}(\hat{\theta})_{\text{jack}} = (n-1)(\hat{\theta}_{\text{jack}} - \hat{\theta})$. The bias-corrected estimator $\hat{\theta}^*_{\text{jack}} = n\hat{\theta} - (n-1)\hat{\theta}_{\text{jack}}$ eliminates bias of order $O(n^{-1})$ and reduces it to $O(n^{-2})$ otherwise [[wiki/sources/jackknife-resampling.md]].

### Variance estimation

Tukey's jackknife variance estimator $\widehat{\text{var}}(\hat{\theta})_{\text{jack}} = \frac{n-1}{n}\sum_{i=1}^n (\hat{\theta}_{(i)} - \hat{\theta}_{\text{jack}})^2$ tends to be conservative (upward-biased) [[wiki/sources/jackknife-resampling.md]].

For the sample mean, this simplifies to the familiar $s^2/n$, showing the jackknife recovers the standard variance formula for simple estimators.

## Example

To estimate the variance of a correlation coefficient:
1. Compute the correlation $r$ on all $n$ data points.
2. For each $i$, compute $r_{(i)}$ on the $n-1$ points excluding observation $i$.
3. Apply Tukey's formula to get $\widehat{\text{var}}(r)_{\text{jack}}$.

This avoids parametric assumptions (e.g., Fisher's $z$-transformation) and works for any estimator.

## Jackknife vs Bootstrap

| Property | Jackknife | Bootstrap |
|---|---|---|
| Replications | $n$ (deterministic) | $B \geq 1000$ (random) |
| Approximation | Linear approximation of bootstrap | More accurate for non-smooth statistics |
| Computational cost | Lower | Higher |
| Bias correction | $O(n^{-1})$ → $O(n^{-2})$ | General |
| Variance estimation | Conservative (upward bias) | Less biased |
| Non-smooth statistics | Fails (e.g., median) | Works |

*Inference:* The jackknife is best used as a quick, computationally cheap diagnostic. For final inference, the bootstrap is generally preferred when computational budget allows [[wiki/sources/jackknife-resampling.md]].

## History

- **1949**: Maurice Quenouille invents the method for bias estimation.
- **1956**: Quenouille refines the technique (published in *Biometrika*).
- **1958**: John Tukey extends it to variance estimation and coins the name "jackknife" — a rough-and-ready tool for many problems.
- **1982**: Bradley Efron unifies the jackknife, bootstrap, and other resampling plans in his SIAM monograph [[wiki/sources/jackknife-resampling.md]].

## Relevance to A/B Testing

The jackknife is used for confidence interval estimation of ratio metrics and other complex statistics where closed-form variance formulas are unavailable. It provides a nonparametric alternative to the delta method and is particularly useful as a cross-check when parametric assumptions are suspect [[wiki/sources/jackknife-resampling.md]] [[wiki/synthesis/confidence-interval-methods.md]].

For ratio metrics — smooth functions of the means of clicks and impressions — the jackknife and delta-method variance estimators are **asymptotically equivalent**: their difference vanishes faster than $n^{-1/2}$, so at $n > 10^6$ both converge to the same variance estimate. The delta method needs only per-cluster sums and cross-products in a single pass, while the jackknife requires $n$ leave-one-out recomputations — computationally prohibitive at this scale unless reduced to incremental formulas that, for smooth statistics, converge to the delta-method formula anyway. **The delta method dominates on both accuracy and cost for ratio metrics at $n > 10^6$**; the jackknife retains value mainly for non-smooth statistics (medians, trimmed means, quantiles) where no delta-method linearization exists, or as a finite-sample cross-check at smaller $n$ [[wiki/sources/jackknife-delta-method-equivalence.md]].
