---
status: current
sources: 1
source_type: peer_reviewed
ingest_count: 1
---

# Always-Valid Inference and Anytime-Valid Confidence Sequences

**Source:** Johari et al. — [Always Valid Inference: Continuous Monitoring of A/B Tests](https://dl.acm.org/doi/10.1287/opre.2021.2135) (Operations Research, 2022)

Anytime-valid methods (mSPRT, confidence sequences, AsympCS) enable continuous monitoring of A/B tests without inflating type-I error. Deployed at Optimizely (Johari et al.), Adobe Experience Platform (AsympCS), and Netflix (regression-adjusted sequential tests). Key trade-off: confidence sequences are 1-4× wider than fixed-horizon CIs but enable early stopping, yielding lower expected sample sizes. AsympCS (Waudby-Smith et al., 2021) provides non-parametric, asymptotically narrow confidence sequences practical for industry platforms. Koning (2025) proved anytime validity can be induced from any valid fixed-n test.
