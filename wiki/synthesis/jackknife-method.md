---
title: "The Jackknife Method"
type: "synthesis"
sources:
  - "web/jackknife-resampling.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# The Jackknife Method

The jackknife is a **resampling technique** in statistics used to estimate the bias and variance of an estimator $\hat{\theta}$ without parametric assumptions. It predates the bootstrap and is conceptually simpler: for a sample of size $n$, compute the statistic of interest $n$ times, each time leaving out one observation, yielding $n$ "leave-one-out" estimates $\hat{\theta}_{(1)}, \dots, \hat{\theta}_{(n)}$.

## How It Works

```mermaid
flowchart LR
  S["Full sample<br/>n observations"] --> L1["Remove obs 1"] --> E1["Estimate θ̂(1)"]
  S --> L2["Remove obs 2"] --> E2["Estimate θ̂(2)"]
  S --> L3["Remove ..."] --> E3["..."]
  S --> Ln["Remove obs n"] --> En["Estimate θ̂(n)"]
  E1 --> Avg["Average → θ̂_jack"]
  E2 --> Avg
  E3 --> Avg
  En --> Avg
  Avg --> B["Bias estimate<br/>(n−1)(θ̂_jack − θ̂)"]
  Avg --> V["Variance estimate<br/>((n−1)/n)Σ(θ̂(i) − θ̂_jack)²"]
```

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

*Open question:* How does the jackknife compare to the delta method for ratio metrics in A/B testing at very large sample sizes ($n > 10^6$)?
