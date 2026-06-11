# Offline Reinforcement Learning for Optimizing Production Bidding Policies

**Source URL:** https://arxiv.org/abs/2310.09426
**Authors:** Dmytro Korenkevych, Frank Cheng, Artsiom Balakir, Alex Nikulkov, Lingnan Gao, Zhihao Cen, Zuobing Xu, Zhongwen Zhu — AI at Meta
**Source type:** peer_reviewed

---

## Production system context

Meta's production bidding policy (the baseline being optimized) is a
**heuristic, feedback-based controller**: "a piece-wise polynomial function in
input features with a couple dozen scalar parameters." This is the kind of
explainable, PID-like feedback controller commonly cited as the
industry-standard approach for budget pacing.

## Control-loop frequency

Decisions are made **every (simulated) minute, per campaign** — "one time
step represents one bidding decision (computed every minute for each
campaign)." This is a substantial increase in control-loop frequency compared
to the **15-minute** loops described in the KDD 2015 "Smart Pacing" paper —
roughly 15x more frequent.

## RL approach: offline policy-parameter tuning, not a new real-time controller

The paper does **not** replace the real-time feedback controller with an RL
agent running in production. Instead, it uses **offline reinforcement
learning (Conservative Q-Learning, CQL)**, trained on logged production data,
to **tune the couple-dozen scalar parameters** of the existing heuristic
controller:

- The actor follows a Gaussian stochastic policy whose **mean is
  parameterized by the production bidding policy itself** (the heuristic),
  and whose **variance is parameterized by a deep neural network**.
- After offline training, only the **tuned parameters** of the heuristic
  policy are deployed to production — the neural network itself is
  discarded.
- Production control-loop latency is therefore **unchanged** from the
  baseline (still per-minute, per-campaign) — RL is used as an *offline
  parameter-optimization* tool, not as an online controller.

## Production results

A/B tested at **~50 billion impressions**: **+0.17% performance metric gain
(95% CI: +0.05% to +0.3%)**, statistically significant, consistent across
pre-test and back-test configurations.

## Takeaway for the open question

This is direct evidence of how a major platform (Meta) modernized pacing
control since KDD 2015:

- **Control-loop frequency**: increased from 15 minutes (2015) to 1 minute
  (2023) — but the *type* of controller (a feedback-based, PID-like heuristic
  with a handful of scalar parameters) has **not** been replaced by MPC or an
  RL controller running online.
- **Where RL fits**: as an *offline tuning* method for the heuristic
  controller's parameters (Conservative Q-Learning on logged data), not as a
  real-time decision-making policy. This is a hybrid — "RL-tuned PID," not
  "RL replaces PID."
