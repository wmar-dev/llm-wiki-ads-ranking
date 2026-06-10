# A Practical Guide to Budget Pacing Algorithms in Digital Advertising

**Source:** arXiv:2503.06942 — "A Practical Guide to Budget Pacing Algorithms in Digital Advertising"
**URL:** https://arxiv.org/abs/2503.06942
**Date:** March 2025

## Summary (fetched via ar5iv)

A practitioner-oriented survey of budget pacing in real-time ad serving,
addressing a gap the authors identify in existing literature: pacing "lacks
a systematic treatment specifically tailored for engineers."

## Problem Definition

Budget pacing controls how a campaign's budget is distributed across time
while respecting constraints. Two primary formulations:

- **Max Delivery**: maximize impressions/conversions subject to a fixed
  budget over the campaign period.
- **Cost Cap**: hit a target conversion volume while keeping average cost
  below a ceiling.

## Algorithm Families

### Throttling-Based Pacing

Probabilistic throttling accepts/rejects each incoming bid opportunity with
a probability proportional to remaining budget vs. remaining time. Simple,
low overhead, but unstable under bursty traffic.

### Bid Modulation Approaches

Continuously adjust the bid price (rather than accept/reject) to control
spend pace:

- **PID controllers** — feedback control comparing actual vs. target spend;
  proportional, integral, derivative terms adjust bids. Proven stability,
  interpretable, but reactive (slower to adapt).
- **Model Predictive Control (MPC)** — solves an optimization over a future
  time horizon, predicting supply patterns and computing optimal bid
  trajectories. Best performance, highest compute cost, sensitive to
  prediction error.
- **Dual Online Gradient Descent (DOGD)** — an online adaptive optimal
  control approach that solves the Lagrangian dual of the pacing problem,
  updating dual variables (Lagrange multipliers / "shadow prices") in
  real time based on constraint violations. Proven convergence guarantees,
  but requires unbiased constraint observations.

## Theoretical Foundation

Pacing is framed as constrained maximization, solved via primal-dual /
Lagrangian methods and Karush-Kuhn-Tucker (KKT) conditions. Under Slater's
condition, strong duality holds, enabling efficient dual-based solutions.
Online algorithms rely on stochastic gradient descent with learning rates
satisfying Σεₜ = ∞ and Σεₜ² < ∞ for convergence.

## Auction Mechanism Integration

- **Second-price / GSP**: truthful bidding is the dominant strategy,
  simplifying pacing design (the pacing multiplier just scales the truthful
  bid).
- **First-price**: requires bid shading — winners must shade bids below true
  value, which interacts with the pacing multiplier.
- **VCG**: allocates to highest valuations with externality-based payments.

## Pacing Objectives

- **Even/Smooth delivery** — spreads budget evenly across the period,
  reducing variance, enabling predictable performance and broader reach.
- **Accelerated delivery** — spends rapidly early to capture volume before
  budget exhaustion; useful when supply is uncertain or time-limited.

## Algorithm Comparison

| Approach | Advantage | Disadvantage |
|---|---|---|
| Throttling | Simple, low overhead | Unstable with variable traffic |
| PID control | Proven stability, interpretable | Reactive to errors, slower adaptation |
| MPC | Optimal with horizon forecasting | Computational cost, sensitive to predictions |
| DOGD (online optimal control) | Proven convergence | Requires unbiased constraint observations |

## Multi-Constraint Extensions

The framework extends to multi-channel budget allocation (dual
decomposition across platforms), campaign groups sharing budgets,
post-conversion ("deep retention") optimization, and reach/frequency
objectives.

## Significance

This is the most comprehensive and recent (2025) primary-source treatment of
pacing as a control-theory / online-optimization problem, complementing the
older "Smart Pacing" (KDD 2015) production case study.
