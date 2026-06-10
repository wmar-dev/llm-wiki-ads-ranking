# Fatigue-Aware Ad Creative Selection

**Source:** arXiv:1908.08936 — "Fatigue-Aware Ad Creative Selection" (also circulated as "A Contextual Bandit Algorithm for Ad Creative under Ad Fatigue")
**Authors:** Daisuke Moriwaki, Komei Fujita, Shota Yasui, Takahiro Hoshino
**URL:** https://arxiv.org/abs/1908.08936
**Date:** August 2019

## Summary (fetched)

Display advertising systems must select which ad creative to show for each
impression. The effect of an ad creative is not static — it changes with the
number of repetitive exposures a user has had to it ("wear-in" when a creative
is still novel and gaining effectiveness, "wear-out" / ad fatigue when repeated
exposure reduces effectiveness or causes annoyance). Traditional creative
selection algorithms ignore this dynamic, treating each impression's reward
distribution as static.

The paper proposes a contextual bandit algorithm for Demand-Side Platforms
(DSPs) that explicitly incorporates a user's psychological/exposure state
(wear-in/wear-out) as part of the context when selecting which creative to
serve. The system optimizes across multiple objectives relevant to DSPs:
click-through rate, number of conversions, revenue, and brand-improvement
metrics.

The proposed algorithm was deployed in a real-world production environment and
evaluated against baseline creative-selection algorithms. The results show the
fatigue-aware contextual bandit outperforms the baselines on most KPIs.

## Notes

- Full algorithmic details (specific bandit formulation, reward model,
  exploration parameters) were not recoverable from the abstract/landing page
  alone — the abstract does not specify whether the underlying bandit is
  Thompson Sampling, UCB-style, or a custom variant.
- Framing: ad creative = "arm", context = user features + exposure/fatigue
  history with that creative, reward = click/conversion/brand signal.
