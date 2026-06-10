---
title: "Approximating Auction Equilibria with Reinforcement Learning"
type: "source_summary"
sources:
  - "web/approximating-auction-equilibria-rl.md"
source_url: "https://arxiv.org/abs/2410.13960"
status: "current"
source_type: "other"
processing_status: "processed"
ingest_count: 1
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Approximating Auction Equilibria with Reinforcement Learning

**Author:** Pranjal Rawat (Georgetown University)

**Submitted:** arXiv, October 17, 2024 (preprint)

**Source type:** `other` (academic working paper, not yet confirmed published in a peer-reviewed venue)

## Overview

This paper trains reinforcement learning agents — using self-play with Proximal Policy Optimization (PPO) and Neural Fictitious Self-Play — to bid in auctions, then checks whether the learned bidding strategies match the Bayes-Nash equilibria predicted by classical auction theory. The framework supports continuous action spaces, high-dimensional information states, and delayed payoffs, making it applicable to multi-item and dynamic auctions where closed-form equilibria are intractable to compute analytically [[raw/web/approximating-auction-equilibria-rl.md]].

## Key Findings

- **First-price auctions, uniform valuations on [0,1]:** RL agents converge to the classic equilibrium shading strategy b\*(v) = v/2.
- **First-price auctions, power-distributed valuations:** agents converge to b\*(v) = v/3.
- **Risk-averse bidders:** agents converge to b\*(v) = 2v/3, matching the risk-adjusted equilibrium.
- **Asymmetric bidders (no closed-form solution):** RL still finds equilibria consistent with numerically-derived theoretical predictions.
- **Second-price auctions:** agents converge toward truthful bidding b\*(v) = v — the dominant-strategy equilibrium that also underlies GSP's locally envy-free equilibrium.
- Validation uses epsilon-best-response deviations: how much a bidder could gain by unilaterally deviating from the learned strategy. No collusive or supra-competitive deviations were found in these settings — convergence is to standard competitive equilibria.

## Relevance to Ads Ranking

This is direct evidence that **ML-powered (RL) bidding agents reproduce the equilibrium concepts that auction-theoretic results (e.g., Edelman-Ostrovsky-Schwarz's locally envy-free equilibrium for GSP) assume rational human bidders converge to** — at least in single-item first- and second-price settings with known closed-form equilibria. This suggests that as automated bidding becomes more prevalent in ad auctions, the equilibrium-based revenue and efficiency guarantees of GSP need not break down purely because the bidders are algorithmic, *provided* the auction format and information structure resemble the settings tested here (no explicit collusion incentives, single-round or simple multi-round formats). The paper does not test settings with explicit communication channels between bidders or repeated-game structures known to produce algorithmic collusion in other contexts (e.g., Q-learning pricing agents in oligopoly), so the question of whether automated bidders could learn *non-competitive* equilibria in richer ad-auction settings remains open [[raw/web/approximating-auction-equilibria-rl.md]].
