---
title: "Asymptotic Equivalence of the Jackknife and Infinitesimal Jackknife Variance Estimators for Some Smooth Statistics"
type: "source_summary"
sources:
  - "web/jackknife-delta-method-equivalence.md"
source_url: "https://arxiv.org/abs/math/0301363"
status: "current"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Asymptotic Equivalence of the Jackknife and Infinitesimal Jackknife Variance Estimators for Some Smooth Statistics

**Author:** Alex D. Gottlieb

**Published:** Annals of the Institute of Statistical Mathematics (Springer); arXiv preprint math/0301363, January 31, 2003

**Source type:** `peer_reviewed`

## Overview

This paper proves that, for smooth functions of the sample mean (and trimmed L-statistics with Hölder continuous weights), the **jackknife variance estimator** and the **infinitesimal jackknife / delta-method (linearization) variance estimator** are **asymptotically equivalent** — their difference vanishes faster than $n^{-1/2}$, even when the estimators themselves are not asymptotically normal [[raw/web/jackknife-delta-method-equivalence.md]].

## Key Findings

- For smooth statistics — including ratio metrics such as CTR = clicks/impressions, which are smooth functions of the means of clicks and impressions — the jackknife and delta-method variance estimators converge to **the same value** as $n \to \infty$.
- The equivalence extends to delete-$d$ jackknife variants.
- The jackknife provides **no asymptotic accuracy advantage** over the delta method for smooth statistics once the sample is large enough for the asymptotic regime to apply.

## Relevance to A/B Testing at Scale ($n > 10^6$)

This directly answers how the jackknife compares to the delta method for ratio metrics at very large sample sizes:

- **Accuracy**: Asymptotically equivalent — both converge to the same variance estimate for smooth ratio metrics.
- **Cost**: The delta method needs only per-cluster sums/cross-products in a single pass (see [[wiki/synthesis/confidence-interval-methods.md]], which notes it is "trivially parallelizable"). The jackknife requires $n$ leave-one-out recomputations, which at $n > 10^6$ is computationally prohibitive unless reduced to incremental formulas — and for smooth statistics those incremental formulas converge to the delta-method formula anyway.
- **Net conclusion**: At $n > 10^6$, the delta method dominates on both accuracy and cost for smooth ratio metrics. The jackknife retains value for **non-smooth statistics** (e.g., medians, trimmed means, quantiles) where no delta-method linearization exists, or as a robustness cross-check at smaller sample sizes where the asymptotic regime hasn't fully taken hold [[raw/web/jackknife-delta-method-equivalence.md]].
