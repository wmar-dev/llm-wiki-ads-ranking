---
title: "A Contextual-Bandit Approach to Personalized News Article Recommendation"
type: "source_summary"
sources:
  - "web/linucb-contextual-bandit-news-recommendation.md"
status: "current"
created: "2026-06-12"
last_updated: "2026-06-12"
source_type: "peer_reviewed"
processing_status: "processed"
ingest_count: 1
---

# A Contextual-Bandit Approach to Personalized News Article Recommendation

**Authors:** Lihong Li, Wei Chu, John Langford, Robert E. Schapire (Yahoo!
Labs / Princeton) — WWW 2010, arXiv:1003.0146.

The paper that introduces **LinUCB**, frames personalized news-article
recommendation as a **contextual bandit**: at each trial the algorithm
observes a context vector x_{t,a} per candidate article (arm), picks one
article, and observes a click/no-click reward whose expectation is its
click-through rate (CTR).

## LinUCB (disjoint linear models)

- **Linear payoff model**: E[r_{t,a} | x_{t,a}] = x_{t,a}^T theta_a*, with a
  separate ("disjoint") coefficient vector theta_a per arm.
- **Ridge regression**: theta_hat_a = (D_a^T D_a + I_d)^{-1} D_a^T c_a, where
  D_a is the design matrix of contexts observed for arm a and c_a the
  corresponding rewards. Define A_a = D_a^T D_a + I_d (so theta_hat_a =
  A_a^{-1} b_a with b_a = D_a^T c_a).
- **UCB rule**: choose a_t = argmax_a ( x_{t,a}^T theta_hat_a + alpha *
  sqrt(x_{t,a}^T A_a^{-1} x_{t,a}) ) — predicted payoff plus a confidence-width
  exploration bonus, alpha being the single tunable parameter (alpha = 1 +
  sqrt(ln(2/delta)/2) gives a (1-delta) confidence bound).
- **Update**: A_{a_t} += x_{t,a_t} x_{t,a_t}^T; b_{a_t} += r_t * x_{t,a_t}.
- Bayesian reading: A_a^{-1} is the posterior covariance of theta_a under a
  Gaussian prior/likelihood, so the confidence bonus is the posterior
  predictive standard deviation — UCB selection trades off predicted reward
  against expected reduction in model uncertainty.

## LinUCB (hybrid linear models)

Adds a term shared across all arms: E[r_{t,a}|x_{t,a}] = z_{t,a}^T beta* +
x_{t,a}^T theta_a*, where z_{t,a} is a user-article interaction feature and
beta* is common to all arms. Because beta* couples arms together, the UCB
must be computed via block matrix inversion (Algorithm 2 in the paper);
amortized cost is O(d^2 + k^2) with periodic cache refresh of the inverses.

## Offline evaluation

Proposes a provably unbiased offline policy evaluator: replay logs collected
under a uniformly-random logging policy, retaining an event only if the
policy under evaluation would have chosen the same arm the logger did. This
made it feasible to benchmark new bandit algorithms against historical
production logs without live A/B exposure.

## Results

On ~36M Yahoo! Front Page "Today Module" events (May 2009), LinUCB achieved a
**12.5% CTR lift** over a context-free bandit baseline, with the advantage
growing further as data per arm becomes scarcer — i.e., contextual
generalization helps most for new/low-traffic articles (a cold-start
benefit).

## Related Pages

- [[wiki/concepts/multi-armed-bandit-algorithms.md]] — general bandit
  algorithm background, including LinUCB's place in the taxonomy
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — production ad-system
  applications of contextual bandits
- [[wiki/synthesis/what-is-linucb.md]] — synthesis answering "what is LinUCB
  and how does it work?"
