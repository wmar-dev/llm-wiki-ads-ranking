# Asymptotic Equivalence of the Jackknife and Infinitesimal Jackknife Variance Estimators for Some Smooth Statistics

Source: https://arxiv.org/abs/math/0301363 (arXiv:math/0301363)

**Author:** Alex D. Gottlieb
**Submitted:** January 31, 2003
**Venue:** Annals of the Institute of Statistical Mathematics (Springer)

## Summary

The jackknife variance estimator and the **infinitesimal jackknife** variance estimator (which, for smooth statistics, coincides with the **delta-method / linearization** variance estimator) are shown to be **asymptotically equivalent** for smooth functions of the mean and for trimmed L-statistics with Hölder continuous weight functions.

## Key Results

- For a smooth functional $\theta = f(\bar{X})$ of the sample mean, the jackknife variance estimator $\widehat{\text{var}}_{\text{jack}}$ and the delta-method (linearization / infinitesimal jackknife) variance estimator $\widehat{\text{var}}_{\text{delta}}$ converge to each other faster than the standard $n^{-1/2}$ rate — i.e., the *difference* between the two estimators vanishes asymptotically faster than the estimators themselves converge to the true variance.
- This equivalence holds even in cases where the estimators are not asymptotically normal.
- The result extends to delete-$d$ jackknife variants, which also converge to delta-method-type linearization estimators in large samples.
- Practical implication: for smooth statistics (including ratio metrics like CTR = clicks/impressions, which are smooth functions of the means of clicks and impressions), the jackknife and the delta method give **the same answer asymptotically** — the jackknife does not provide additional accuracy over the delta method once $n$ is large enough for the asymptotic regime to apply.

## Relevance to A/B Testing at Scale

For ratio metrics in A/B tests with $n > 10^6$, this theoretical result implies:

1. **Accuracy**: The jackknife and delta method should produce essentially identical variance estimates and confidence intervals — neither has an asymptotic accuracy advantage over the other for smooth ratio statistics.
2. **Computational cost**: The delta method requires only first and second moments / cross-products (computable in a single pass, trivially parallelizable via per-cluster sums). The jackknife requires recomputing the statistic for each of $n$ leave-one-out subsamples — at $n > 10^6$, this is computationally far more expensive unless approximated via incremental/closed-form updates (which, for smooth statistics, reduce to the delta-method formula anyway).
3. **Conclusion**: At very large sample sizes, the delta method is preferred for ratio metrics on both accuracy *and* cost grounds. The jackknife's main value — robustness for non-smooth statistics (e.g., medians, trimmed means) where no delta-method linearization exists, or as a finite-sample cross-check at smaller $n$ — does not apply to smooth ratio metrics at $n > 10^6$, where the asymptotic regime has fully kicked in [[raw/web/jackknife-delta-method-equivalence.md]].
