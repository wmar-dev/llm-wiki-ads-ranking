---
title: "Statistical Learning from Attribution Sets"
type: "source_summary"
sources:
  - "web/statistical-learning-attribution-sets.md"
source_url: "https://arxiv.org/abs/2602.06276"
status: "current"
source_type: "other"
processing_status: "processed"
ingest_count: 1
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Statistical Learning from Attribution Sets

**Authors:** Lorne Applebaum, Robert Busa-Fekete, August Y. Chen, Claudio Gentile, Tomer Koren, Aryan Mokhtari

**Submitted:** arXiv, February 6, 2026 (preprint)

**Source type:** `other` (academic preprint)

## Overview

This paper directly addresses what happens to ad conversion-prediction model training once third-party cookies are deprecated and browsers expose only privacy-preserving attribution APIs (e.g., Privacy Sandbox's Attribution Reporting API). Instead of a deterministic click→conversion link, the learner only observes that a conversion belongs to an **attribution set** — a group of candidate clicks, any one of which could be the true cause [[raw/web/statistical-learning-attribution-sets.md]].

## Key Findings

- **Coarsened labels, not missing data**: Privacy APIs don't simply remove training signal — they coarsen it. A conversion is still observed, but its causal click is replaced by a *set* of candidates drawn from a known (or estimable) prior distribution.
- **Unbiased loss estimator**: The authors construct an estimator of the population loss for conversion-prediction (pCVR) models that remains unbiased despite this coarsening, even with complex dependencies among overlapping attribution sets.
- **Generalization bounds**: Empirical Risk Minimization with this estimator generalizes with guarantees that scale with the *informativeness of the prior* over candidates, and is robust to prior misspecification.
- **Beats industry heuristics**: On standard benchmarks, the unbiased estimator significantly outperforms common industry heuristics (e.g., naive uniform credit-splitting across an attribution set) — most notably in the large/overlapping attribution-set regime that privacy-preserving APIs push the industry toward.

## Relevance to Ads Ranking

This is a direct, technical answer to the [[wiki/sources/unreasonable-effectiveness-of-data.md]] open question about privacy regulation and signal loss: third-party cookie deprecation and ATT do not eliminate "free" training data so much as **degrade its precision** — converting exact click-conversion labels into coarser attribution sets. The paper shows that with the right estimator, models can still be trained close to the same standard as before, but naive approaches (treating attribution-set members as if individually labeled, or using simple heuristic credit-splitting) lose significant accuracy as attribution sets grow larger and more overlapping — which is the direction privacy APIs are pushing the ecosystem [[raw/web/statistical-learning-attribution-sets.md]].
