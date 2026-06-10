# Always Valid Inference: Continuous Monitoring of A/B Tests

**Source:** Johari, Pekelis, Walsh — Operations Research, 2022
**URL:** https://dl.acm.org/doi/10.1287/opre.2021.2135
**Date:** 2022

## Summary (fetched)

Anytime-valid methods (mSPRT, confidence sequences, AsympCS) enable continuous
monitoring of A/B tests without inflating type-I error. Deployed at Optimizely
(Johari et al.), Adobe Experience Platform (AsympCS), and Netflix
(regression-adjusted sequential tests). Key trade-off: confidence sequences are
1-4x wider than fixed-horizon CIs but enable early stopping, yielding lower
expected sample sizes. AsympCS (Waudby-Smith et al., 2021) provides
non-parametric, asymptotically narrow confidence sequences practical for
industry platforms. Koning (2025) proved anytime validity can be induced from
any valid fixed-n test.

*Note: this raw file was reconstructed from the summary embedded in
`wiki/sources/always-valid-sequential-testing.md` (no separate raw fetch was
saved at original ingest time, 2026-06-09).*
