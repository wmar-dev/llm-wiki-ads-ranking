---
title: "Offline Reinforcement Learning for Optimizing Production Bidding Policies"
type: "source_summary"
sources:
  - "web/offline-rl-production-bidding-meta.md"
source_url: "https://arxiv.org/abs/2310.09426"
status: "current"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# Offline Reinforcement Learning for Optimizing Production Bidding Policies

**Authors:** Dmytro Korenkevych, Frank Cheng, Artsiom Balakir, Alex Nikulkov, Lingnan Gao, Zhihao Cen, Zuobing Xu, Zhongwen Zhu — AI at Meta (arXiv:2310.09426)

**Source type:** `peer_reviewed`

## Summary

Describes a Meta production system that uses **offline reinforcement learning
(Conservative Q-Learning, CQL)**, trained on logged production data, to tune
the scalar parameters of an existing **heuristic, PID-like, feedback-based
bidding/pacing controller** — rather than replacing that controller with a
new real-time RL or MPC policy. Decisions are made **every minute, per
campaign**. A/B tested at ~50 billion impressions, the tuned policy achieved a
statistically significant **+0.17% performance gain (95% CI: +0.05% to
+0.3%)** [[raw/web/offline-rl-production-bidding-meta.md]].

## Key Claims

| Claim | Status |
|---|---|
| Meta's production bidding/pacing controller is a heuristic "piece-wise polynomial function" with a couple dozen scalar parameters — a PID-like feedback controller | Stated |
| Production control loop runs at 1-minute granularity per campaign | Stated |
| Offline RL (CQL) is used to tune the heuristic controller's parameters from logged data; the trained neural network is discarded post-training and only tuned parameters are deployed | Stated |
| A/B test on ~50B impressions: +0.17% performance gain (95% CI 0.05%-0.3%), statistically significant | Stated |

## Relevance to Ads Ranking

This directly addresses the [[wiki/synthesis/ad-pacing.md]] open question on
how production pacing control loops have evolved since the KDD 2015 "Smart
Pacing" paper (15-minute loops): at Meta, the control-loop **frequency**
increased roughly 15x (15 min -> 1 min), but the controller **type** remains a
PID-like heuristic feedback controller. **Reinforcement learning has entered
production, but as an offline tuner of that heuristic's parameters — not as a
real-time MPC/RL controller replacing it.** This is a more incremental
modernization than "the field shifted to MPC or RL controllers."

## Open Questions

- Open question: this paper documents Meta's approach; no source found
  describes Google's equivalent modernization (control-loop frequency or
  whether/how RL is used) for Smart Bidding's pacing layer since 2015.

## Related Pages

- [[wiki/synthesis/ad-pacing.md]]
- [[wiki/sources/smart-pacing-online-ad-campaign-optimization.md]]
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]]
