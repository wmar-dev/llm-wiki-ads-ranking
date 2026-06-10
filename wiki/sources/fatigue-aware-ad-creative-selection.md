---
title: "Fatigue-Aware Ad Creative Selection"
type: "source_summary"
sources:
  - "web/fatigue-aware-ad-creative-selection.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
---

# Fatigue-Aware Ad Creative Selection

**Authors:** Daisuke Moriwaki, Komei Fujita, Shota Yasui, Takahiro Hoshino — arXiv:1908.08936 (2019)

A contextual bandit algorithm for **ad creative selection at a Demand-Side
Platform (DSP)** that explicitly models *ad fatigue* — the wear-in (a creative
gaining effectiveness as it becomes familiar) and wear-out (a creative losing
effectiveness or annoying users after repeated exposure) dynamics of repeated
ad exposure.

## Problem

For each impression, a DSP must choose which ad creative to serve. A
creative's expected reward is **not stationary** — it depends on how many
times, and how recently, the user has already seen it. Standard
creative-selection algorithms treat each creative's reward distribution as
fixed, ignoring this exposure history.

## Approach

The bandit's **context** includes the user's exposure/fatigue state with
respect to each candidate creative (in addition to standard user/page
features); the **arms** are the candidate creatives; the **reward** combines
multiple DSP objectives — click-through rate, conversions, revenue, and
brand-improvement signals.

*Inference: Framing fatigue as part of the context (rather than a separate
filter or cooldown rule) lets the bandit learn creative-specific wear-in/wear-out
curves directly from reward feedback, rather than relying on hand-tuned frequency
caps.*

## Production Results

The algorithm was deployed in a live production environment and compared
against baseline creative-selection algorithms. It **outperformed the
baselines on most KPIs**. The publicly available abstract does not specify the
exact bandit family used (e.g., Thompson Sampling vs. UCB-style) or give
numeric KPI deltas.

## Related Pages

- [[wiki/concepts/multi-armed-bandit-algorithms.md]] — general bandit algorithm background
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — synthesis on bandits in ad systems
