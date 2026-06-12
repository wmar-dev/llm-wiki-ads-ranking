---
title: "Multi-Armed Bandit Algorithms"
type: "concept"
sources:
  - "web/fatigue-aware-ad-creative-selection.md"
  - "web/dynamic-ad-allocation-bandits-with-budgets.md"
  - "web/comparison-lift-bandit-experimentation.md"
status: "draft"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# Multi-Armed Bandit Algorithms

A **multi-armed bandit (MAB)** is a sequential decision problem: at each
round, an agent picks one of $K$ "arms," observes a stochastic reward for that
arm only, and must balance **exploration** (trying arms to learn their reward
distributions) against **exploitation** (picking the arm currently believed
best). Performance is measured as **regret** — the gap between cumulative
reward earned and the reward an oracle that always picks the best arm would
have earned.

Bandits are a single-state special case of reinforcement learning (no state
transitions), which makes them tractable enough to run online, in production,
at the granularity of individual ad impressions or experiment arms.

## Core Algorithms

| Algorithm | Selection rule | Strengths | Weaknesses |
|---|---|---|---|
| **Epsilon-greedy** | With probability $\varepsilon$ pick a random arm; otherwise pick the empirically best arm | Trivial to implement | Wastes exploration on arms already known to be bad; $\varepsilon$ must be tuned/decayed |
| **UCB1** (Upper Confidence Bound) | Pick the arm maximizing $\hat{\mu}_i + \sqrt{\frac{2\ln t}{n_i}}$ — empirical mean plus a confidence bonus that shrinks as the arm is pulled more | Strong, well-known regret bounds; deterministic, no tuning of randomness | Confidence bonus is the same shape for every arm; doesn't natively use context features |
| **Thompson Sampling** | Maintain a posterior distribution over each arm's reward; sample one value per arm from its posterior and pick the arm with the highest sample | Empirically very strong; naturally extends to contextual settings; Bayesian framing fits naturally with hierarchical priors | Requires a (reasonably well-specified) generative/posterior model per arm |
| **Contextual bandits (e.g., LinUCB)** | Model expected reward as a function of a context vector $x_t$ (user, page, ad features) plus arm-specific parameters; select the arm maximizing predicted reward (+ UCB bonus or posterior sample) | Personalizes the explore/exploit decision per-request instead of treating all rounds identically | Needs feature engineering; model misspecification biases the learned policy |
| **Budgeted / constrained bandits** | Extend the above with a resource constraint per arm (e.g., a spend cap); the arm is removed from consideration once its budget is exhausted | Matches real ad systems, where every campaign has a finite budget — [[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]] *(peer_reviewed)* | Adds combinatorial/scheduling complexity on top of the learning problem |

## Contextual Bandits in Practice

Most production ad-system applications use **contextual** bandits rather than
context-free MAB: the "right" arm to pick (which creative, which budget level,
which experiment variant) genuinely depends on who the user is, what page
they're on, and the user's prior exposure history. [[wiki/sources/fatigue-aware-ad-creative-selection.md]]
*(peer_reviewed)* is a concrete example — the context includes the user's
wear-in/wear-out exposure state with respect to each candidate ad creative.

## Relationship to A/B Testing

Bandit algorithms and A/B testing solve a related problem — comparing variants
under uncertainty — but optimize for different things:

- **Fixed-sample A/B testing** allocates traffic in fixed proportions for the
  whole test duration, prioritizing a clean, unbiased estimate of the
  treatment effect at the end.
- **Bandit-based experimentation** continuously reallocates traffic toward
  better-performing variants *during* the test, prioritizing cumulative reward
  (less spend "wasted" on inferior variants) over a precise final effect-size
  estimate. [[wiki/sources/comparison-lift-bandit-experimentation.md]]
  *(peer_reviewed)* is a production example of this trade-off at JD.com.

[[wiki/synthesis/confidence-interval-methods.md]] notes that Bayesian credible
intervals are used "in specialized settings (e.g., bandit algorithms,
hierarchical modeling)," and that design-based confidence sequences are
explicitly "valid for multi-arm bandits" — i.e., the same anytime-valid
inference machinery used for sequential A/B tests also applies to bandit
deployments that need to report a final effect estimate.

## Related Pages

- [[wiki/synthesis/what-is-linucb.md]] — deep dive on LinUCB's ridge-regression confidence bounds, disjoint/hybrid models, and offline evaluation
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — how these algorithms map onto ad-system applications
- [[wiki/sources/fatigue-aware-ad-creative-selection.md]] — contextual bandit for ad creative selection *(peer_reviewed)*
- [[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]] — budgeted UCB1 for ad allocation *(peer_reviewed)*
- [[wiki/sources/comparison-lift-bandit-experimentation.md]] — bandit-based experimentation at JD.com *(peer_reviewed)*
- [[wiki/synthesis/confidence-interval-methods.md]] — CI/CS methods, including bandit-adjacent Bayesian and design-based approaches
- [[wiki/synthesis/tiktok-recommendation-algorithm.md]] — exploration vs. exploitation in a recommendation (non-bandit-framed) context
