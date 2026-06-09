---
title: "Time-uniform Central Limit Theory and Asymptotic Confidence Sequences"
type: "source_summary"
sources:
  - "web/time-uniform-clt-asymp-cs.md"
source_url: "https://arxiv.org/abs/2103.06476"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

**Authors**: Ian Waudby-Smith, David Arbour, Ritwik Sinha, Edward H. Kennedy, Aaditya Ramdas
**Venue**: Annals of Statistics, 52(6), 2613–2640 (2024) *(peer_reviewed)*

## Overview

Introduces asymptotic confidence sequences (AsympCS) — time-uniform analogues of CLT-based confidence intervals. Provides valid inference at arbitrary stopping times without penalizing peeking. The key finding is that the width penalty for anytime validity is bounded: nonasymptotic CSs stay within ~2× of fixed-sample CLT bounds over five orders of magnitude in time (Howard et al., 2021).

## Key Results

- CS width lower bound: O(√(log log n / n)) by the law of the iterated logarithm
- AsympCS achieves optimal LIL rate asymptotically
- Gaussian mixture boundary is tighter at moderate sample sizes
- The penalty for anytime validity is a factor of ~2× in width, or 2–7× in sample size depending on construction
- Extends to causal inference (ATE) in randomized experiments and observational studies
