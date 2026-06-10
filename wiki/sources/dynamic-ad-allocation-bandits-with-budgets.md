---
title: "Dynamic Ad Allocation: Bandits with Budgets"
type: "source_summary"
sources:
  - "web/dynamic-ad-allocation-bandits-with-budgets.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
---

# Dynamic Ad Allocation: Bandits with Budgets

**Source:** arXiv:1306.0155 (2013)

A theoretical paper connecting **multi-armed bandit (MAB) theory** to **online
ad allocation under budget constraints** — i.e., the pay-per-click setting
where each ad's click-through probability is unknown and must be learned, and
each ad has a finite spend budget that, once exhausted, removes it from
consideration.

## Problem Formulation

- Each round: the algorithm picks **one ad to display**.
- Each ad has an unknown click probability and a **budget** — the maximum
  total amount that can be spent on that ad before it is retired from the
  rotation.
- Goal: maximize cumulative value (e.g., clicks) subject to these budget
  constraints, while learning click probabilities online.

## Algorithm

A **budget-aware extension of UCB1** (Upper Confidence Bound): the algorithm
maintains confidence bounds on each ad's click probability as in standard
UCB1, but additionally tracks remaining per-ad budget and excludes
budget-exhausted ads from future rounds.

## Theoretical Guarantees

The paper proves **regret bounds** — bounds on the gap between the algorithm's
cumulative performance and that of an optimal policy with full prior knowledge
of click probabilities and budgets. (Exact bound expressions were not
recoverable from the abstract alone.)

## Significance for Ad Systems

This work is one of the bridges between classical bandit theory (regret
minimization via optimism-under-uncertainty / UCB) and the operational reality
of ad systems, where **every campaign operates under a finite budget** —
making "budgeted bandits" directly relevant to production ad allocation and
pacing systems.

## Related Pages

- [[wiki/concepts/multi-armed-bandit-algorithms.md]] — UCB1 and budgeted-bandit background
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — synthesis on bandits in ad systems
