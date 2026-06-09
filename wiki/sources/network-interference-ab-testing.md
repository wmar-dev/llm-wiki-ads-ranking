---
title: "Network Interference in A/B Testing"
type: "source_summary"
sources:
  - "web/network-interference-ab-testing.md"
source_url: "https://arxiv.org/abs/2411.19789"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

## Overview

Network interference (SUTVA violation) occurs when one unit's treatment affects another's outcome. Adjusting CIs requires either design-based strategies (cluster randomization, used at Facebook/Meta) or analysis-based strategies (exposure modeling, regression adjustment, causal message-passing).

## Key Approaches

- **Cluster-randomized design**: Randomize clusters to contain spillover; requires 2–5× more data than unit-randomized designs (Guber et al., Facebook, KDD 2023)
- **Exposure modeling**: HT estimators weighted by exposure probabilities (Aronow & Samii, 2017)
- **Regression adjustment**: Network covariate adjustment for variance reduction (Han & Ugander, 2023)
- **Causal message-passing**: Multi-period experiments, no network knowledge needed (Shirani & Bayati, PNAS 2024)
- **Block bootstrap**: Valid CIs under network dependence by resampling clusters (Kojevnikov et al.)
