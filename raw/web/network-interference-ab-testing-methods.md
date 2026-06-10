# Network Interference in A/B Testing

**Source:** Multiple peer-reviewed papers (composite summary)
**URL:** see per-method references below
**Date:** 2024-2025

## Summary (fetched)

Modern approaches for handling SUTVA violations in social/network settings:

1. **UNITE** (Shankar et al., AISTATS 2024): GATE estimator requiring only
   superset-of-neighbors knowledge, not full network.
2. **Surrogate Network + Pseudo-Inverse** (WeChat, arXiv 2408.04441): tested on
   53M+ user experiment; detects interference via estimator differences.
3. **Causal Message-Passing** (PMC 2024): models interference as dynamic
   propagation through network; no prior network knowledge needed.
4. **Just Ramp-up** (arXiv 2410.12740): leverages existing ramp-up process
   (different treatment proportions across experiments) with
   regression-based estimators — no additional experiment resources required.
5. **Dyadic Data Estimator** (WeChat, arXiv 2402.12653): unbiased estimator for
   total treatment effect using pairwise outcome data.

*Note: this raw file was reconstructed from the summary embedded in
`wiki/sources/network-interference-ab-testing-methods.md` (no separate raw
fetch was saved at original ingest time, 2026-06-09).*
