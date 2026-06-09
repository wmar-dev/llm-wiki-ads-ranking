---
title: "Jackknife Resampling"
type: "source_summary"
sources:
  - "web/jackknife-resampling.md"
source_url: "https://en.wikipedia.org/wiki/Jackknife_resampling"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

**Authors**: Maurice Quenouille (1949, 1956), John Tukey (1958), Bradley Efron (1982)
**Venue**: Multiple venues; Wikipedia summary

## Overview

The jackknife is a resampling technique in statistics, also known as jackknife cross-validation. It is especially useful for bias and variance estimation and pre-dates the bootstrap. Given a sample of size n, a jackknife estimator aggregates parameter estimates from each subsample of size n−1 obtained by omitting one observation. The jackknife is a linear approximation of the bootstrap.

## Key Concepts

### Leave-One-Out Replicates

For each observation i = 1, ..., n, the i-th jackknife replicate θ̂_(i) is computed on the sample with the i-th observation removed. The jackknife estimate is the average of all n replicates.

### Bias Correction

The jackknife bias estimate is (n−1)(θ̂_jack − θ̂). The bias-corrected estimator is θ̂*_jack = n θ̂ − (n−1) θ̂_jack. This eliminates bias of order O(n⁻¹) and reduces it to O(n⁻²) otherwise.

### Variance Estimation

Tukey's jackknife variance estimator: var̂(θ̂)_jack = ((n−1)/n) Σ (θ̂_(i) − θ̂_jack)². For the sample mean, this reduces to s²/n. The estimator tends to be conservative (upward-biased).

## Relationship to Bootstrap

The bootstrap (Efron, 1979) is conceptually simpler and generally preferred. The jackknife requires n replications; the bootstrap typically requires B ≥ 1000. The jackknife is a linear approximation of the bootstrap. Efron's monograph (1982) unifies both methods alongside cross-validation, random subsampling, and balanced repeated replications.

## Significance for A/B Testing

The jackknife is used in confidence interval estimation, particularly for ratio metrics and complex estimators where closed-form variance formulas are unavailable. It provides a nonparametric alternative to the delta method.
