# Jackknife resampling

Source: https://en.wikipedia.org/wiki/Jackknife_resampling

## Summary

In statistics, the jackknife (jackknife cross-validation) is a cross-validation technique and a form of resampling. It is especially useful for bias and variance estimation. The jackknife pre-dates other common resampling methods such as the bootstrap. Given a sample of size n, a jackknife estimator can be built by aggregating the parameter estimates from each subsample of size (n-1) obtained by omitting one observation. The jackknife is a linear approximation of the bootstrap.

## History

The jackknife technique was developed by Maurice Quenouille from 1949 and refined in 1956. John Tukey expanded on the technique in 1958 and proposed the name "jackknife" because, like a physical jack-knife (a compact folding knife), it is a rough-and-ready tool that can improvise a solution for a variety of problems even though specific problems may be more efficiently solved with a purpose-designed tool.

## Procedure

The jackknife estimator of a parameter is found by systematically leaving out each observation from a dataset and calculating the parameter estimate over the remaining observations and then aggregating these calculations.

For each i in {1,...,n}, compute the i-th jackknife replicate:
θ̂_(i) = f_{n-1}(x_1, …, x_{i-1}, x_{i+1}, …, x_n)

Then the jackknife estimate is the average:
θ̂_jack = (1/n) Σ θ̂_(i)

## Bias estimation

The jackknife estimate of the bias of θ̂ is:
biaŝ(θ̂)_jack = (n-1)(θ̂_jack - θ̂)

The bias-corrected jackknife estimate:
θ̂*_jack = θ̂ - biaŝ(θ̂)_jack = n θ̂ - (n-1) θ̂_jack

This removes the bias when it is O(n⁻¹) and reduces it to O(n⁻²) otherwise.

## Variance estimation

Tukey's jackknife variance estimate:
var̂(θ̂)_jack = ((n-1)/n) Σ (θ̂_(i) - θ̂_jack)²

For the special case of the sample mean, this reduces to the familiar formula s²/n. The jackknife variance estimate tends to be conservative (biased upward).

## Relationship to bootstrap

The jackknife is a linear approximation of the bootstrap (Efron, 1979). The bootstrap is conceptually simpler and generally preferred when computational cost is not prohibitive, but the jackknife requires fewer computations (n replications vs. B bootstrap replications, typically B ≥ 1000). Efron's monograph "The Jackknife, the Bootstrap and Other Resampling Plans" (SIAM, 1982) unifies these methods.

## Key references

- Quenouille, M.H. (1949). "Problems in Plane Sampling". Annals of Mathematical Statistics. 20 (3): 355–375.
- Quenouille, M.H. (1956). "Notes on Bias in Estimation". Biometrika. 43 (3–4): 353–360.
- Tukey, J.W. (1958). "Bias and confidence in not-quite large samples (abstract)". Annals of Mathematical Statistics. 29 (2): 614.
- Efron, B. (1982). The Jackknife, the Bootstrap, and Other Resampling Plans. SIAM.
- Efron, B.; Tibshirani, R.J. (1994). An Introduction to the Bootstrap. Chapman and Hall.
- Efron, B.; Stein, C. (1981). "The Jackknife Estimate of Variance". Annals of Statistics. 9 (3): 586–596.
