---
title: "How Are Bandit Algorithms Used in Ad Systems?"
type: "synthesis"
sources:
  - "web/fatigue-aware-ad-creative-selection.md"
  - "web/dynamic-ad-allocation-bandits-with-budgets.md"
  - "web/comparison-lift-bandit-experimentation.md"
  - "web/lyft-contextual-bandits-advertising-budget-allocation.md"
  - "web/google-smart-bidding-exploration.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-10"
---

# How Are Bandit Algorithms Used in Ad Systems?

Ad systems are full of decisions under uncertainty where the "true" payoff of
an option — a creative, a budget level, a targeting variant — is unknown and
can only be learned by trying it and observing the outcome. **Multi-armed
bandit (MAB)** algorithms ([[wiki/concepts/multi-armed-bandit-algorithms.md]])
formalize this explore/exploit trade-off, and in production ad systems they
show up at (at least) three distinct layers: **creative selection**, **budget
allocation**, and **experimentation infrastructure**.

## The Explore/Exploit Loop

Every bandit-driven component of an ad system follows the same basic loop: a
request arrives with some context, a policy picks an "arm" to serve, a reward
is observed, and the policy's model is updated for the next round.

![synthesis-bandit-algorithms-in-ad-systems-diagram-1](/assets/synthesis-bandit-algorithms-in-ad-systems-diagram-1.svg)

What differs across applications is **what counts as an "arm"** — a candidate
creative, a campaign's next budget increment, or an experiment's treatment
variant.

## Application 1: Ad Creative Selection Under Fatigue

[[wiki/sources/fatigue-aware-ad-creative-selection.md]] *(peer_reviewed)*
describes a contextual bandit deployed at a Demand-Side Platform (DSP) where:

- **Arms** = candidate ad creatives for an impression
- **Context** = user/page features *plus* the user's wear-in/wear-out exposure
  history with each creative (ad fatigue)
- **Reward** = a combination of CTR, conversions, revenue, and brand-lift
  signals

The key idea is that a creative's effectiveness is **non-stationary** — it
changes as a function of how often a given user has already seen it. By
folding exposure history into the bandit's context, the system learns
creative-specific wear-in/wear-out curves directly from feedback rather than
relying on hand-tuned frequency caps. Deployed in production, this fatigue-aware
contextual bandit outperformed baseline creative-selection algorithms on most
KPIs.

## Application 2: Budget Allocation Under Bandit Constraints

[[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]] *(peer_reviewed)*
extends classical UCB1 to the setting every real ad campaign faces: a finite
spend budget. Here:

- **Arms** = ads/campaigns competing for impressions
- **Constraint** = each arm has a budget; once exhausted, it drops out of the
  rotation
- **Algorithm** = "budgeted UCB1" — maintain confidence bounds on each ad's
  click probability as in standard UCB1, but also track and respect remaining
  per-ad budget
- **Guarantee** = provable regret bounds relative to an optimal allocation
  with full knowledge of click probabilities and budgets

*Inference: This budget-aware framing is what makes bandit theory
deployable for real campaign management — a pure regret-minimizing bandit with
no budget concept would happily keep "spending" on a high-CTR ad past an
advertiser's actual cap.*

**Production deployment: Lyft's Contextual Budgeting System (CBS).** Lyft
runs exactly this combination — a supervised model predicts each campaign's
payout from context features, predictions are extrapolated to untested budget
levels, and **Thompson Sampling** selects each campaign's next budget level —
in production for marketplace ad spend allocation. CBS manages "hundreds of
millions of dollars" of annual marketing spend, and on new-driver-acquisition
spend it improved mean CPA by **(22 +/- 10)%** versus Lyft's previous
MCMC-based allocation strategy. New campaigns are cold-started via a
transfer-learning mechanism that borrows statistical strength from similar
campaigns' context features
[[wiki/sources/lyft-contextual-bandits-advertising-budget-allocation.md]]
*(peer_reviewed)*.

- Open question: the available summary of Lyft's CBS does not specify the
  granularity of its "arms" (individual ad sets/creatives vs. whole
  campaigns) or how frequently the Thompson Sampling allocation is re-run
  (real-time per-auction vs. periodic batch re-allocation).

## Application 3: Bandit-Based Experimentation (an A/B Test Alternative)

[[wiki/sources/comparison-lift-bandit-experimentation.md]] *(peer_reviewed)*
describes **Comparison Lift**, an experimentation-as-a-service platform
deployed at JD.com since May 2019 that replaces fixed-sample A/B allocation
for ad campaign tests with adaptive bandit reallocation:

- **Arms** = treatment variants under test (audiences, creatives, etc.)
- Traffic shifts toward better-performing variants *during* the test instead
  of holding a fixed split for the full duration
- Results: **1,500+ experiments**, a **46% average CTR increase** for
  participating campaigns, and **27% additional clicks generated during the
  testing period itself** versus a traditional fixed-sample A/B design

This is a direct production example of the trade-off discussed in
[[wiki/synthesis/confidence-interval-methods.md]]: fixed-sample A/B testing
([[wiki/synthesis/how-ab-tests-work.md]]) optimizes for a clean final
effect-size estimate, while bandit-based testing optimizes for cumulative
reward *during* the test, at some cost to the precision of that final
estimate. The same page notes that Bayesian methods (which underlie Thompson
Sampling) are used "in specialized settings (e.g., bandit algorithms,
hierarchical modeling)," and that design-based confidence sequences are
explicitly "valid for multi-arm bandits" — i.e., platforms that run bandits
*and* need a rigorous final read-out can use confidence-sequence machinery on
top of the bandit's collected data.

## Algorithm Choices in Practice

| Bandit family | Where it shows up in ad systems |
|---|---|
| Epsilon-greedy | Rarely used directly in production; common as a textbook baseline |
| UCB1 / budgeted UCB1 | Budget-constrained allocation across campaigns/ads — [[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]] |
| Thompson Sampling | Adaptive experimentation and budget allocation; Bayesian framing composes with priors and posteriors |
| Contextual bandits (LinUCB-style) | Per-impression personalization, e.g., fatigue-aware creative selection — [[wiki/sources/fatigue-aware-ad-creative-selection.md]] |

See [[wiki/concepts/multi-armed-bandit-algorithms.md]] for the underlying
algorithm definitions and selection rules.

## Bandits vs. Heuristic Exploration in Recommendation Feeds

It's worth contrasting formal bandit policies with the simpler heuristic
exploration used in some recommendation feeds.
[[wiki/synthesis/tiktok-recommendation-algorithm.md]] describes TikTok's
For You Page as exploiting known interests for roughly **30-50%** of
recommendations and exploring outside the user's taste cluster for the
remaining **50-70%** — a largely **fixed ratio** applied uniformly to drive
discovery and generate training data.

*Inference: A bandit-based system instead makes the explore/exploit ratio
**adaptive** — driven by the algorithm's current uncertainty about each arm
(e.g., UCB's confidence bonus shrinks as an arm is pulled more, and Thompson
Sampling's posterior narrows with more observations) — rather than applying a
constant exploration percentage to every request. The two approaches solve
related problems (avoiding filter bubbles / stale rankings vs. minimizing
regret on a well-defined reward), but a fixed exploration ratio is not itself
a bandit algorithm.*

## Open Questions

Google's Smart Bidding **does** ship an explore/exploit-shaped mechanism:
**Smart Bidding Exploration** (announced May 2025) gives Target-ROAS
campaigns an advertiser-configurable **ROAS-tolerance band (10-30%)** that is
spent bidding into previously-untargeted "potentially high-performing" search
queries, trading short-term ROAS for coverage of untested query categories —
the same tradeoff structure as a bandit's explore/exploit balance. March-April
2025 testing showed **+18%** more unique converting query categories and
**+19%** more conversions. However, Google frames this publicly as
"opportunity expansion," not as a named bandit algorithm — there is no
mention of UCB, Thompson Sampling, confidence bounds, or regret
[[wiki/sources/google-smart-bidding-exploration.md]] *(official documentation)*.

- Open question: Google has not disclosed the underlying algorithm behind the
  ROAS-tolerance band (e.g., whether it resembles a Thompson-Sampling- or
  UCB-style posterior/confidence mechanism, or a simpler rule-based
  threshold), nor how it composes with the pacing layer described in
  [[wiki/synthesis/ad-pacing.md]]. Whether Meta or Reddit document an
  equivalent mechanism is also unknown.

## Related Pages

- [[wiki/concepts/multi-armed-bandit-algorithms.md]] — bandit algorithm fundamentals (UCB1, Thompson Sampling, contextual bandits, regret)
- [[wiki/sources/fatigue-aware-ad-creative-selection.md]] — contextual bandit for ad creative selection under ad fatigue *(peer_reviewed)*
- [[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]] — budgeted UCB1 for ad allocation *(peer_reviewed)*
- [[wiki/sources/comparison-lift-bandit-experimentation.md]] — bandit-based experimentation at JD.com *(peer_reviewed)*
- [[wiki/sources/lyft-contextual-bandits-advertising-budget-allocation.md]] — Lyft's Contextual Budgeting System: production contextual bandit for ad budget allocation *(peer_reviewed)*
- [[wiki/sources/google-smart-bidding-exploration.md]] — Google's Smart Bidding Exploration: ROAS-tolerance-based exploration of new query categories *(official documentation)*
- [[wiki/synthesis/confidence-interval-methods.md]] — CI/CS methods, including Bayesian and design-based approaches relevant to bandits
- [[wiki/synthesis/how-ab-tests-work.md]] — fixed-sample A/B testing, the alternative bandits replace
- [[wiki/synthesis/tiktok-recommendation-algorithm.md]] — heuristic exploration vs. exploitation in a recommendation feed
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]] — Google's Smart Bidding, now confirmed to include exploration via Smart Bidding Exploration
- [[wiki/synthesis/ad-pacing.md]] — pacing/bid-strategy coupling, including the related open question on whether Google's pacing and Smart Bidding Exploration mechanisms compose
