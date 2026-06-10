---
title: "Smart Pacing for Effective Online Ad Campaign Optimization"
type: "source_summary"
sources:
  - "web/smart-pacing-online-ad-campaign-optimization.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
---

# Smart Pacing for Effective Online Ad Campaign Optimization

**Source:** Xu et al., KDD 2015 (Yahoo Labs), arXiv:1506.05851

**Source type:** `peer_reviewed` (ACM SIGKDD 2015)

**Processing:** single-pass (via ar5iv HTML)

---

## Summary

A production pacing system from a real DSP that groups ad requests into
layers by predicted response rate and adjusts per-layer pacing rates to
balance smooth budget delivery against performance goals (e.g., effective
CPC).

## Key Claims

- Two constrained-optimization formulations: branding campaigns minimize
  eCPC subject to spending the full budget within a delivery-plan tolerance;
  performance campaigns minimize plan deviation subject to a performance
  constraint and an unspent-budget tolerance
  [[raw/web/smart-pacing-online-ad-campaign-optimization.md]] *(peer-reviewed)*.
- **Layered pacing control**: ad requests are grouped by predicted response
  rate into layers; the online algorithm computes the spend residual
  (target − actual) and raises pacing rates top-down through high-response
  layers when under-spending, or lowers rates bottom-up through low-response
  layers when over-spending, via the proportional update
  `r_l(t) = min(1.0, r_l(t-1) × (c_l(t-1) + R) / c_l(t-1))`
  [[raw/web/smart-pacing-online-ad-campaign-optimization.md]] *(peer-reviewed)*.
- A small "trial rate" (~1% of budget) is reserved for the next-potential
  layer to keep exploring response rates — an explore/exploit mechanism
  conceptually related to bandit-based budget allocation
  [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]].
- **Production A/B results** (3 campaigns, 8 layers): eCPC reduced 72%, 67%,
  79% vs. global pacing; spend-plan adherence within 6.8-9.8% average error;
  baseline failed its performance goal on one campaign while smart pacing met
  it [[raw/web/smart-pacing-online-ad-campaign-optimization.md]] *(peer-reviewed)*.
- Real-time control loop closes within 15-minute time slots at billions of
  impressions/day via an async message-queue feedback pipeline
  [[raw/web/smart-pacing-online-ad-campaign-optimization.md]] *(peer-reviewed)*.

## Related Pages

- [[wiki/synthesis/ad-pacing.md]] — synthesis on ad pacing
- [[wiki/sources/budget-pacing-algorithms-practical-guide.md]] — control-theoretic survey of pacing algorithms
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — explore/exploit framing, "trial rate" parallel
- [[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]] — budgeted UCB1 for ad allocation
