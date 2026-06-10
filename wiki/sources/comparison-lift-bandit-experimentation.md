---
title: "Comparison Lift: Bandit-Based Experimentation System for Online Advertising"
type: "source_summary"
sources:
  - "web/comparison-lift-bandit-experimentation.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
---

# Comparison Lift: Bandit-Based Experimentation System for Online Advertising

**Source:** arXiv:2009.07899 (2020)

Describes **Comparison Lift**, an experimentation-as-a-service (EaaS) platform
deployed at **JD.com** that replaces fixed-sample-size A/B testing for ad
campaigns (audiences, creatives, etc.) with an **adaptive multi-armed-bandit
allocation algorithm**.

## Problem with Fixed A/B Testing for Ads

A fixed-sample A/B test must keep sending traffic to under-performing variants
for the full test duration to preserve statistical validity — wasting ad spend
on arms that are already known (probabilistically) to be worse, and delaying
the decision.

## Bandit-Based Alternative

Comparison Lift dynamically reallocates traffic toward better-performing
variants as evidence accumulates during the test, rather than holding a fixed
split. The authors frame this as:

1. **Goal alignment** — the randomization used *during* the test is aligned
   with the advertiser's actual optimization objective, so the test itself
   spends less on inferior variants.
2. **Cost reduction** — less ad spend "wasted" on confirmed-inferior arms
   during testing.

## Production Results (since May 2019)

| Metric | Result |
|---|---|
| Experiments run | 1,500+ |
| Avg. CTR increase for participating campaigns | 46% |
| Additional clicks generated *during testing* vs. fixed A/B | 27% |

## Significance

This is a direct, large-scale production example of **multi-armed bandits used
as an alternative to traditional A/B testing** for ad campaign experimentation
— complementary to the wiki's existing coverage of A/B testing methodology
([[wiki/synthesis/how-ab-tests-work.md]]) and confidence-sequence-based
sequential testing ([[wiki/synthesis/confidence-interval-methods.md]]), which
notes that "Bayesian methods are used in specialized settings (e.g., bandit
algorithms...)".

## Related Pages

- [[wiki/concepts/multi-armed-bandit-algorithms.md]] — general bandit algorithm background
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — synthesis on bandits in ad systems
- [[wiki/synthesis/confidence-interval-methods.md]] — CI/CS methods, including bandit-adjacent Bayesian and design-based approaches
- [[wiki/synthesis/how-ab-tests-work.md]] — traditional fixed-sample A/B testing
