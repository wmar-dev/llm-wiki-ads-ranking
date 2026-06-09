---
title: "Methods for Computing Confidence Intervals in A/B Testing"
type: "synthesis"
sources:
  - "pdf/overlapping-experiment-infrastructure.pdf"
  - "web/time-uniform-clt-asymp-cs.md"
  - "web/network-interference-ab-testing.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# Methods for Computing Confidence Intervals in A/B Testing

A confidence interval (CI) quantifies the uncertainty around a treatment effect estimate. Different metrics (means, ratios, quantiles) and different data structures (simple random, clustered, sequential) require different methods. The table below summarizes the main approaches and their use cases.

![synthesis-confidence-interval-methods-diagram-1](/assets/synthesis-confidence-interval-methods-diagram-1.svg)

## Frequentist Methods

### Student's t-test / Wald interval

For a simple mean metric (e.g., average revenue per user) where the randomization unit equals the analysis unit, the standard confidence interval is:

$$\hat{\theta} \pm t_{\alpha/2, n-1} \cdot \frac{s}{\sqrt{n}}$$

where $\hat{\theta}$ is the point estimate, $s$ is the sample standard deviation, and $t$ is the critical value from Student's t-distribution. For large $n$ the normal quantile $z_{\alpha/2}$ replaces $t$. This interval has correct coverage when observations are i.i.d. normal; by the Central Limit Theorem it remains asymptotically valid for non-normal data [[wiki/sources/overlapping-experiment-infrastructure.md]].

### Delta method

For **ratio metrics** (CTR = clicks / impressions, revenue per session) where numerator $Y$ and denominator $D$ are both random variables at the randomization-unit level, the delta method linearizes the ratio using a first-order Taylor expansion:

$$R = \frac{\bar{Y}}{\bar{D}}, \quad \text{Var}(R) \approx \frac{1}{n\bar{D}^2}\left[\sigma_Y^2 + R^2\sigma_D^2 - 2R\,\text{Cov}(Y,D)\right]$$

At Microsoft's ExP platform, this method is applied with a bias correction term $(\bar{Y}s_D^2/\bar{D} - s_{YD})/(n\bar{D})^2$ added to the point estimate to improve small-sample coverage — simulations show all methods achieve nominal ~95% coverage for $n \geq 200$ *(peer_reviewed)*.

The delta method is **general** (works for any smooth function), **memorable** (calculus-level derivation), and **parallelizable** (closed-form formula using sufficient statistics). It extends naturally to cluster-randomized experiments: aggregate to the cluster level, then apply the ratio formula above.

### Fieller's theorem

Fieller's interval provides an exact CI for the ratio of two means under normality. It has a more complex formula (requiring a $g$ term for the denominator's coefficient of variation) but can be more accurate for small samples ($n \leq 50$). For $n \geq 200$, the delta method and Fieller produce nearly identical coverage rates, making the simpler delta method preferable at scale [[wiki/sources/overlapping-experiment-infrastructure.md]].

### Edgeworth expansion

The delta method can be refined by an Edgeworth expansion that corrects for skewness. The correction adds a term involving the skewness of the linearized residuals, yielding CIs with coverage closer to nominal for small samples and non-normal data. Applied at Microsoft ExP but rarely used outside specialized settings.

### Empirical carve-up

Referenced in Google's analysis tool, this method partitions variance empirically across experimental units. Details are not publicly documented; it is considered functionally equivalent to the delta method for ratio metrics.

## Resampling Methods

### Bootstrap (non-parametric)

The bootstrap resamples the data with replacement (typically $B = 1000$–$10{,}000$ replicates), recomputes the metric for each resample, and constructs a CI from the empirical distribution of replicates. Common variants:

| Variant | Method | Properties |
|---|---|---|
| **Percentile** | $[\hat{\theta}^*_{(\alpha/2)}, \hat{\theta}^*_{(1-\alpha/2)}]$ | Simple but can be biased |
| **BCa** | Bias-corrected and accelerated | Adjusts for skewness; recommended general-purpose |
| **Bootstrap-t** | $( \hat{\theta} - t^* \cdot \hat{SE} )$ | Better coverage for non-pivotal statistics |

Bootstrap is computationally expensive — computing $B$ quantiles requires sorting, which involves costly data shuffling in distributed systems. At scale, closed-form methods (delta method, outer CI) are typically preferred.

### Bootstrap matching

For non-randomized A/B tests or experiments with selection bias, bootstrap matching combines bootstrap resampling with propensity score matching. Each bootstrap iteration samples a subset of observations, matches treatment and control units, and estimates the effect. P-values are aggregated using Local False Discovery Rate (LFDR) to control type I error.

## Quantile Metrics

### Outer confidence interval (outer CI)

For quantile metrics (e.g., 95th percentile of page load time), the standard asymptotic formula requires estimating the density $f$ at the quantile, which is difficult in practice. The **outer CI** method avoids density estimation:

Given $n$ i.i.d. observations and desired quantile $p$, the count of observations below the quantile follows $\text{Binomial}(n, p)$. Inverting this gives rank bounds $[L, U]$ where:

$$L = n(p - z_{\alpha/2}\sqrt{p(1-p)/n}), \quad U = n(p + z_{\alpha/2}\sqrt{p(1-p)/n}) + 1$$

The CI is $[X_{(L)}, X_{(U)}]$. Pre-adjustment (widening ranks) gives more conservative coverage; post-adjustment (tightening) is recommended for $n \geq 1000$. At $n = 1000$, outer CI provides coverage comparable to bootstrap at ~20× lower computational cost *(peer_reviewed)*.

### Hybrid method (Deng et al.)

A novel hybrid extends the delta method framework to outer CI for quantile metrics when data is clustered or stratified. The procedure computes two additional quantiles (for the CI bounds) in a single pass, costing almost no extra runtime compared to computing just the point estimate. Maintains the parallelizability of closed-form methods while handling complex data structures.

## Bayesian Methods

### Credible intervals

Bayesian CIs (credible intervals) are quantiles of the posterior distribution of the treatment effect. With a conjugate prior (e.g., Normal-Normal), the posterior mean is a weighted average of the prior mean and the observed data mean, and the credible interval is:

$$\mu \mid \text{data} \sim \mathcal{N}\left(\frac{\mu_0/\sigma_0^2 + n\bar{x}/\sigma^2}{1/\sigma_0^2 + n/\sigma^2}, \frac{1}{1/\sigma_0^2 + n/\sigma^2}\right)$$

Bayesian intervals provide correct coverage only when the prior is well-specified. Mismatched priors can produce severely miscalibrated coverage. For this reason, frequentist methods remain the default in production A/B testing platforms, though Bayesian methods are used in specialized settings (e.g., bandit algorithms, hierarchical modeling).

## Anytime-Valid Methods (Sequential)

Traditional fixed-horizon CIs lose validity under continuous monitoring ("peeking"). **Confidence sequences** are sequences of intervals that maintain uniform coverage guarantees for all stopping times.

### mSPRT-based confidence sequences (Johari et al.)

The **mixture sequential probability ratio test (mSPRT)** constructs always-valid CIs by inverting a sequential test. For a treatment effect $\theta$ with variance $\sigma^2$:

$$CS_n = \left\{\hat{\theta}_n \pm \sqrt{ \frac{2\hat{\sigma}_n^2(n\rho^2+1)}{n^2\rho^2} \log\left( \frac{\sqrt{n\rho^2+1}}{\alpha} \right) }\right\}$$

where $\rho$ is a tuning parameter. This sequence is wider than a fixed-horizon CI at any given $n$ but preserves coverage under arbitrary stopping rules. Deployed in a large-scale commercial platform (Optimizely) analyzing hundreds of thousands of experiments.

### Asymptotic confidence sequences (Waudby-Smith et al.)

**AsympCS** are non-parametric anytime-valid analogues of CLT-based intervals. They require no parametric assumptions and are asymptotically as narrow as fixed-horizon intervals. The "t" variant explicitly accounts for variance estimation uncertainty, making them more conservative at small $n$.

### Design-based confidence sequences (Ham et al.)

Extends confidence sequences to design-based inference (conditioning on potential outcomes, not on a generative model). Valid for multi-arm bandits, time series, and panel experiments. Deployed at Netflix for sequential experimentation.

### SAVI confidence bounds (Howard & Ramdas)

**Safe Anytime Valid Inference (SAVI)** bounds apply to entire distributions (all quantiles simultaneously) using Ville's inequality and martingale techniques. SAVI bounds are wider than mean-focused methods (mSPRT) but detect distributional differences beyond mean shifts.

| Method | Valid for | Width | Assumptions |
|---|---|---|---|
| mSPRT | Mean shift | Moderate | Parametric (exponential family) |
| AsympCS (Gaussian) | Mean | Narrow | Asymptotic, CLT |
| AsympCS (t) | Mean | Wider at small n | Asymptotic + variance uncertainty |
| Design-based CS | ATE | Moderate | Randomization, no model |
| SAVI | All quantiles | Wider | None — fully nonparametric |

## Variance Reduction (Related)

### CUPED

CUPED (Controlled Experiments Using Pre-Experiment Data) uses pre-experiment data as a covariate to reduce metric variance. A transformed metric $Y' = Y - \theta X$ (where $X$ is the pre-experiment [pre-period] value) has variance $\text{Var}(Y' = (1 - \rho^2)\text{Var}(Y))$, where $\rho$ is the correlation between pre- and during-experiment values. This directly narrows all downstream confidence intervals.

## Decision Framework

![synthesis-confidence-interval-methods-diagram-2](/assets/synthesis-confidence-interval-methods-diagram-2.svg)

## Implementation Notes

- **Always check coverage** via A/A tests: at $\alpha = 0.05$, ~5% of metrics should produce significant results. Calibrate CI methods on uniform data before trusting results [[wiki/sources/overlapping-experiment-infrastructure.md]].
- **For ratio metrics in distributed systems**, the delta method requires only per-cluster sums, sums of squares, and cross-products — trivially parallelizable.
- **For sequential monitoring**, always use confidence sequences rather than repeated fixed-horizon CIs. At scale, automate the stopping rule: stop when the confidence sequence excludes zero or narrows below a practical significance threshold.

## Answered Questions

**Confidence intervals for network interference** require either design-based or analysis-based adjustments, with no universal solution:

- **Design**: cluster-randomized trials contain spillover within clusters (Facebook/Meta uses this; requires 2–5× more data). Staggered rollout designs leveraging multiple treatment proportions can identify global treatment effects.
- **Analysis**: exposure-modeling HT estimators (Aronow & Samii), regression adjustment with network covariates (Han & Ugander), causal message-passing for unknown interference structures (Shirani & Bayati, PNAS 2024), and block bootstrap for valid CIs by resampling network clusters.

The choice depends on whether the interference structure is known, the network size, and data availability [[wiki/sources/network-interference-ab-testing.md]].

## Answered Questions

**Confidence sequences cannot match fixed-horizon CI width in the worst case**: there is an unavoidable penalty. The law of the iterated logarithm imposes a lower bound of $O(\sqrt{\log\log n/n})$ on CS width, versus $O(1/\sqrt{n})$ for fixed-horizon CIs. However, this penalty is modest in practice: nonasymptotic CSs stay within a factor of ~2× of fixed-sample CLT bounds over five orders of magnitude in time (Howard et al., 2021), and asymptotic CSs (AsympCS) achieve the optimal LIL rate (Waudby-Smith et al., 2024). The practical cost is 2–7× more data depending on the specific construction [[wiki/sources/time-uniform-clt-asymp-cs.md]].
