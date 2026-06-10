# Approximating Auction Equilibria with Reinforcement Learning

Source: https://arxiv.org/abs/2410.13960 (arXiv:2410.13960, also available as https://arxiv.org/html/2410.13960v1)

**Author:** Pranjal Rawat (Georgetown University)
**Submitted:** October 17, 2024

## Abstract

Traditional methods for computing equilibria in auctions become computationally intractable as auction complexity increases, particularly in multi-item and dynamic auctions. This paper introduces a self-play based reinforcement learning approach that employs advanced algorithms such as Proximal Policy Optimization and Neural Fictitious Self-Play to approximate Bayes-Nash equilibria. This framework allows for continuous action spaces, high-dimensional information states, and delayed payoffs. Through self-play, these algorithms can learn robust and near-optimal bidding strategies in auctions with known equilibria, including those with symmetric and asymmetric valuations, private and interdependent values, and multi-round auctions.

## Key Findings (from full-text review)

- RL agents trained via self-play (PPO, Neural Fictitious Self-Play) **converge to the theoretically predicted Bayes-Nash equilibria** for auction formats with known closed-form solutions.
- **First-price auctions, uniform valuations on [0,1]:** agents converge to the classic shading equilibrium b*(v) = v/2.
- **First-price auctions, power-distributed valuations:** agents converge to b*(v) = v/3.
- **Risk-averse bidders:** agents converge to b*(v) = 2v/3, matching the risk-aversion-adjusted equilibrium.
- **Asymmetric bidders (no closed-form equilibrium):** RL still finds equilibria consistent with theoretical predictions derived numerically.
- **Second-price (and by extension GSP-style) auctions:** agents converge toward truthful bidding, b*(v) = v, the dominant-strategy equilibrium.
- Validation methodology: measures how close the learned strategies are to true equilibria using epsilon-best-response deviations — i.e., how much a bidder could gain by deviating from the learned strategy.
- The paper does not find evidence of collusive or supra-competitive deviations in these settings; all reported convergence is toward standard competitive Bayes-Nash equilibria, not toward non-competitive alternatives.

## Relevance

Directly addresses whether ML-powered (RL) bidding agents converge to the same equilibrium concepts used in classical auction theory (the equilibria proven for GSP and other ad auction mechanisms). The answer, within the settings studied, is yes — RL agents reproduce known Bayes-Nash equilibrium bidding functions for both first-price and second-price auctions.
