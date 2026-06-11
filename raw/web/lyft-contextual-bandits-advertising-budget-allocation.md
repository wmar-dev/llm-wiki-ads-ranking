# Contextual Bandits for Advertising Budget Allocation (Lyft, AdKDD 2020)

**Source URL:** https://www.adkdd.org/papers/contextual-bandits-for-advertising-budget-allocation/2020
**Author:** Benjamin Han (Lyft)
**Source type:** peer_reviewed (AdKDD workshop, KDD 2020)

---

## System architecture: Contextual Budgeting System (CBS)

Lyft's production budget-allocation system is a **multi-agent system of
contextual & continuous multi-armed bandits**, framed as a convex
optimization problem whose objective is drawn via **Thompson Sampling**:

1. A **supervised learning model** predicts each ad campaign's payout (e.g.,
   new-user signups/rides) as a function of context features (campaign
   metadata, historical performance, market conditions) and a proposed
   budget level.
2. The model's predictions are **extrapolated to out-of-sample budget
   levels** using a simple parametric functional form for the
   payout-vs-budget curve, since historically-tested budgets cluster around a
   narrow range.
3. **Thompson Sampling** draws from the predicted payout distributions to
   select the next budget allocation per campaign — balancing exploration
   (try untested budget levels) against exploitation (allocate more to
   campaigns with high predicted payout).

## Cold start

A **transfer-learning mechanism** augments the simple parametric payout model
with supervised learning across campaigns, so new campaigns with little or no
historical data can borrow statistical strength from similar campaigns'
context features rather than starting from an uninformative prior.

## Production scale and results

- "This system is now responsible for managing **hundreds of millions of
  dollars** of annual marketing spend at Lyft."
- Applied to all new-driver-acquisition spend, the system achieved a
  **(22 +/- 10)% improvement in mean Cost Per Acquisition (CPA)** over
  Lyft's previous (non-contextual, MCMC-based) budget allocation strategy.

---

## Relevance

This is a directly-named, large-scale, production deployment of contextual
bandits for ad budget allocation — exactly the kind of "specific production
deployment" that prior research on this wiki could not locate. It confirms
that the "contextual bandit + Thompson Sampling for budget levels" framing
(previously described only abstractly) is in active production use, managing
hundreds of millions of dollars/year, with a measured (22 +/- 10)% CPA
improvement.
