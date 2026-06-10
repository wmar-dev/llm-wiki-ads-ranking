# Dynamic Ad Allocation: Bandits with Budgets

**Source:** arXiv:1306.0155 — "Dynamic Ad Allocation: Bandits with Budgets"
**URL:** https://arxiv.org/abs/1306.0155
**Date:** June 2013

## Summary (fetched)

Addresses online ad allocation in pay-per-click models where each ad's
click-through probability is unknown and must be learned online. The key
addition over prior multi-armed-bandit (MAB) treatments of ad allocation is a
**budget constraint**: each ad has a maximum spend ("budget") that can be
consumed before it must stop being shown. In each round, the algorithm picks
one ad to display; once an ad's budget is exhausted it is removed from
consideration.

## Algorithmic Approach

The paper proposes a natural extension of **UCB1** (Upper Confidence Bound)
adapted to the budget-constrained setting. The algorithm maintains confidence
bounds on each ad's click probability (as in standard UCB1) while additionally
tracking remaining budget per ad and respecting per-ad spending limits when
selecting which ad to show in each round.

## Theoretical Guarantees

The paper proves regret bounds for the budgeted-UCB algorithm: bounds on the
performance gap between the learned policy and an optimal allocation that
would be possible with full prior knowledge of click probabilities and
budgets. The abstract does not give the exact bound expression.

## Significance

Connects classical multi-armed bandit theory (regret minimization,
exploration via confidence bounds) to a practical operational constraint that
is ubiquitous in real ad systems — advertisers operate under finite budgets /
spend caps, not infinite-horizon optimization. This moves bandit-based ad
allocation closer to production deployment realities.
