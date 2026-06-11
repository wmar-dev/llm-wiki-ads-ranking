---
title: "Contextual Bandits for Advertising Budget Allocation (Lyft, AdKDD 2020)"
type: "source_summary"
sources:
  - "web/lyft-contextual-bandits-advertising-budget-allocation.md"
source_url: "https://www.adkdd.org/papers/contextual-bandits-for-advertising-budget-allocation/2020"
status: "current"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# Contextual Bandits for Advertising Budget Allocation (Lyft, AdKDD 2020)

**Author:** Benjamin Han (Lyft)

**Source type:** `peer_reviewed` (AdKDD workshop, KDD 2020)

## Summary

Describes Lyft's **Contextual Budgeting System (CBS)**, a production system
of contextual & continuous multi-armed bandits that allocates marketing
budget across campaigns. A supervised model predicts each campaign's payout
as a function of context and proposed budget; predictions are extrapolated to
untested budget levels via a parametric functional form; **Thompson Sampling**
then selects each campaign's next budget level, balancing exploration of
untested budgets against exploitation of campaigns with high predicted
payout. Cold-start for new campaigns is handled via a transfer-learning
mechanism that borrows statistical strength from similar campaigns'
context features [[raw/web/lyft-contextual-bandits-advertising-budget-allocation.md]].

## Key Claims

| Claim | Status |
|---|---|
| CBS architecture = supervised payout prediction -> parametric extrapolation to untested budgets -> Thompson Sampling for budget selection | Stated |
| Cold start for new campaigns handled via transfer learning across campaign context features | Stated |
| CBS manages "hundreds of millions of dollars" of annual marketing spend at Lyft | Stated |
| Applied to new-driver acquisition, CBS achieved a (22 +/- 10)% improvement in mean CPA vs. a previous MCMC-based allocation strategy | Stated |

## Relevance to Ads Ranking

This directly answers the open question on
[[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] asking for a "primary
source for a specific production deployment of contextual budget-allocation
bandits": Lyft's CBS is exactly that — a named, large-scale (hundreds of
millions of dollars/year), peer-reviewed production system combining
supervised payout prediction with Thompson Sampling for budget allocation,
with a measured (22 +/- 10)% CPA improvement.

## Open Questions

- Open question: the available summary does not specify how CBS defines its
  "arms" at the granularity of individual ad sets/creatives vs. whole
  campaigns, nor how often the Thompson Sampling allocation decision is
  re-run (real-time per-auction vs. periodic batch re-allocation).

## Related Pages

- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]]
- [[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]]
- [[wiki/synthesis/ad-pacing.md]]
