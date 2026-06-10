---
title: "A Practical Guide to Budget Pacing Algorithms in Digital Advertising"
type: "source_summary"
sources:
  - "web/budget-pacing-algorithms-practical-guide.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
source_type: "other"
processing_status: "processed"
ingest_count: 1
---

# A Practical Guide to Budget Pacing Algorithms in Digital Advertising

**Source:** arXiv:2503.06942 (March 2025)

**Source type:** `other` (arXiv preprint, practitioner survey — not yet
peer-reviewed)

**Processing:** single-pass (via ar5iv HTML)

---

## Summary

A 2025 practitioner survey of budget pacing — controlling how an ad
campaign's budget is spent over time. Frames pacing as a constrained
optimization problem (Max Delivery vs. Cost Cap formulations) solved via
primal-dual / control-theoretic methods, and surveys the two dominant
algorithm families: throttling and bid modulation.

## Key Claims

- Two pacing objectives: **Max Delivery** (maximize delivery subject to a
  fixed budget) and **Cost Cap** (hit a conversion target while keeping
  average cost under a ceiling)
  [[raw/web/budget-pacing-algorithms-practical-guide.md]].
- **Throttling**: probabilistically accept/reject each bid opportunity based
  on remaining budget vs. remaining time — simple but unstable under bursty
  traffic [[raw/web/budget-pacing-algorithms-practical-guide.md]].
- **Bid modulation**: continuously scale the bid price to control spend pace.
  Three control approaches — PID controllers (feedback, interpretable,
  reactive), Model Predictive Control (forecasts supply, optimal but
  expensive), and Dual Online Gradient Descent / online optimal control
  (solves the Lagrangian dual via Lagrange-multiplier "shadow prices", proven
  convergence) [[raw/web/budget-pacing-algorithms-practical-guide.md]].
- Pacing is formulated as constrained maximization solved via primal-dual /
  KKT methods; under second-price/GSP auctions truthful bidding is dominant
  so the pacing multiplier simply scales the bid, while first-price auctions
  require bid shading that interacts with the pacing multiplier
  [[raw/web/budget-pacing-algorithms-practical-guide.md]].
- **Even/smooth delivery** spreads spend evenly to maximize reach and
  predictability; **accelerated delivery** spends rapidly to capture volume
  before a deadline or under uncertain supply
  [[raw/web/budget-pacing-algorithms-practical-guide.md]].
- Extends to multi-channel budget allocation (dual decomposition), shared
  campaign-group budgets, post-conversion ("deep retention") optimization,
  and reach/frequency capping
  [[raw/web/budget-pacing-algorithms-practical-guide.md]].

## Related Pages

- [[wiki/synthesis/ad-pacing.md]] — synthesis on ad pacing
- [[wiki/sources/smart-pacing-online-ad-campaign-optimization.md]] — production case study (KDD 2015)
- [[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]] — budgeted UCB1, related budget-constrained allocation
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — explore/exploit framing for budget allocation
- [[wiki/synthesis/bidding-types.md]] — first-price vs second-price auction context
