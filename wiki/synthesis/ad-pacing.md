---
title: "What Is Ad Pacing?"
type: "synthesis"
sources:
  - "web/budget-pacing-algorithms-practical-guide.md"
  - "web/smart-pacing-online-ad-campaign-optimization.md"
  - "web/dynamic-ad-allocation-bandits-with-budgets.md"
  - "web/reddit-ads-how-it-works.md"
  - "web/meta-bid-and-budget-pacing.md"
  - "web/google-marketing-live-2026-bidding-budgeting.md"
  - "web/offline-rl-production-bidding-meta.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-10"
---

# What Is Ad Pacing?

**Pacing** is the layer of an ad-delivery system that controls *when within
a campaign's flight* its budget gets spent — distinct from the auction logic
that decides *whether a given impression is won* and the bid-strategy logic
that decides *what to bid*. Without pacing, a campaign with a daily budget
would simply win every auction it could afford until the budget ran out —
often within minutes of a day starting — leaving the rest of the day
(and most of the audience) unreached.

![synthesis-ad-pacing-diagram-1](/assets/synthesis-ad-pacing-diagram-1.svg)

---

## Why Pacing Exists

A campaign has a **budget** and a **delivery window** (e.g., "$1,000 over
24 hours"). At each impression opportunity, a pacing controller decides
whether/how aggressively to participate, based on the gap between **target
spend so far** and **actual spend so far**
[[wiki/sources/budget-pacing-algorithms-practical-guide.md]]. Two delivery
objectives are common:

- **Even / smooth delivery** — spread spend evenly across the window to
  maximize reach (more distinct users/times-of-day) and produce predictable,
  comparable performance day-to-day.
- **Accelerated delivery** ("ASAP") — spend as fast as possible, useful for
  time-limited promotions or when inventory supply is uncertain and an
  advertiser would rather "lock in" delivery early.

Reddit's ad platform exposes this choice directly to advertisers: **Standard
pacing** (even spread) vs. **Accelerated pacing** (as fast as possible)
[[wiki/synthesis/reddit-ads.md]] — the same two objectives the pacing
literature formalizes as "smooth delivery" vs. "accelerated delivery"
[[wiki/sources/budget-pacing-algorithms-practical-guide.md]].

A related but distinct framing: **Max Delivery** (maximize
impressions/conversions subject to a fixed budget) vs. **Cost Cap** (hit a
conversion target while keeping average cost under a ceiling)
[[wiki/sources/budget-pacing-algorithms-practical-guide.md]] — note this
"Cost Cap" is the same naming TikTok uses for one of its automated *bid
strategies* [[wiki/synthesis/bidding-types.md]], underscoring that pacing and
bid-strategy logic are tightly intertwined in production systems even though
they are conceptually separable.

---

## Two Algorithm Families

### 1. Throttling

Probabilistically accept or reject each incoming auction opportunity based
on a participation probability proportional to remaining budget vs.
remaining time — effectively a biased coin-flip per impression
[[wiki/sources/budget-pacing-algorithms-practical-guide.md]]. If the campaign
is over-delivering, the probability is decreased; if under-delivering, it's
increased. Simple and low-overhead, but unstable under bursty traffic — a
sudden spike in cheap inventory can blow through the budget before the
throttle adjusts.

### 2. Bid Modulation

Instead of skipping auctions, continuously scale the *bid itself* by a
pacing multiplier so the campaign participates in every auction but bids
less aggressively when ahead of pace
[[wiki/sources/budget-pacing-algorithms-practical-guide.md]]. Three control
approaches are used in practice:

| Approach | Mechanism | Tradeoff |
|---|---|---|
| **PID controller** | Classical feedback control: proportional + integral + derivative terms react to the gap between target and actual spend | Stable, interpretable, but reactive — adapts only after a deviation appears |
| **Model Predictive Control (MPC)** | Forecasts future supply/demand and solves for an optimal bid trajectory over a horizon | Best performance, but computationally expensive and sensitive to forecast error |
| **Dual Online Gradient Descent (DOGD)** | Online optimal control: solves the Lagrangian dual of the constrained pacing problem, updating "shadow price" multipliers in real time | Proven convergence guarantees, but needs unbiased constraint observations |

[[wiki/sources/budget-pacing-algorithms-practical-guide.md]]

---

## Production Case Study: Layered Pacing (Yahoo DSP, KDD 2015)

[[wiki/sources/smart-pacing-online-ad-campaign-optimization.md]]
*(peer-reviewed)* describes a real DSP system that buckets ad requests into
**layers by predicted response rate** and adjusts pacing rates per layer
rather than globally:

- Compute the spend residual `R = target spend − actual spend`.
- If under-delivering, raise pacing rates **top-down** through the
  highest-response layers first (spend more on the best-performing
  inventory).
- If over-delivering, lower rates **bottom-up** through the lowest-response
  layers first (cut the weakest inventory first).
- A small **trial rate** (~1% of budget) is reserved for not-yet-explored
  layers to keep learning response rates.

In production A/B tests across 3 campaigns this reduced effective CPC by
67-79% versus global pacing while keeping spend within ~7-10% of the delivery
plan [[wiki/sources/smart-pacing-online-ad-campaign-optimization.md]].

**Inference:** The "trial rate" reserved for unexplored layers is structurally
the same explore/exploit pattern as the bandit-based budget allocation
described in [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — both
keep a small fraction of budget flowing to under-tried options so the system
doesn't get stuck exploiting an early estimate. However, layered pacing
control is framed as a control-theory/optimization problem (PID/MPC/DOGD
operating on response-rate layers), not as an explicit multi-armed bandit —
which is consistent with the open question on
[[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] about whether major
platforms frame budget pacing as bandit exploration vs. supervised
forecasting: in this production system, it's the latter (a supervised
response-rate model) with a bandit-*like* trial-rate heuristic layered on top,
rather than a formal bandit policy.

---

## How Pacing Interacts with the Auction

The auction mechanism (covered in [[wiki/synthesis/bidding-types.md]])
shapes how the pacing multiplier is applied:

- **Second-price / GSP** (search, social feeds): truthful bidding is the
  dominant strategy, so the pacing multiplier can simply scale the
  advertiser's true-value bid up or down
  [[wiki/sources/budget-pacing-algorithms-practical-guide.md]].
- **First-price** (programmatic RTB): winners already need to **shade** bids
  below true value to avoid overpaying
  [[wiki/sources/first-price-second-price-auction-setupad.md]]; the pacing
  multiplier and the bid-shading factor interact, since both push the
  submitted bid below the advertiser's raw valuation for different reasons
  (one for budget control, one for auction economics)
  [[wiki/sources/budget-pacing-algorithms-practical-guide.md]].

---

## Relationship to Budget-Constrained Bandits

[[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]] *(peer-reviewed)*
addresses a closely related but distinct problem: a **budgeted UCB1** bandit
that learns each ad's unknown click probability *while* respecting a
per-ad budget, removing an ad from rotation once its budget is exhausted.

- **Budgeted bandits** (Dynamic Ad Allocation paper): the open question is
  *which ad/arm to show next*, under uncertainty about click probability,
  subject to a hard budget cutoff.
- **Pacing** (this page): the open question is *how fast to spend* a single
  campaign's budget over time, given (approximately) known response rates and
  a fixed delivery window.

**Inference:** These are complementary layers of the same production stack —
a budgeted bandit might decide *which* campaigns/ads get impressions in a
given auction, while each winning campaign's own pacing controller decides
*how aggressively* it bid into that auction given its remaining budget and
time. Neither source describes the two as formally integrated, but they
operate on the same underlying state (remaining budget, remaining time,
predicted response rate).

---

## Open Questions

Google and Meta describe materially different couplings between pacing and
bid strategy. **Meta's official documentation states that "budget pacing and
bid pacing are one process"**: a per-ad-set **pacing multiplier** is applied
directly to the same "total value" term the auction ranks on (advertiser bid
x estimated action rate x ad quality), based on remaining budget and time —
pacing is not a separate admission-control layer, it is folded into the bid
calculation itself
[[wiki/sources/meta-bid-and-budget-pacing.md]] *(official documentation)*.
**Google's 2026 "demand-led pacing"**, by contrast, is described as operating
*alongside* Smart Bidding rather than as one unified mechanism — pacing
redistributes the daily budget toward higher-demand days (within monthly/daily
caps), while Smart Bidding separately decides what to bid within whatever
budget is available that day
[[wiki/sources/google-marketing-live-2026-bidding-budgeting.md]]
*(official documentation)*.

- Open question: Google's public materials do not disclose whether pacing
  modifies the per-auction bid value submitted to Ad Rank directly (a
  Meta-style multiplier on the bid itself), or operates purely at the
  coarser daily-budget-allocation level within which Smart Bidding then
  optimizes — i.e., whether Google's architecture is actually closer to
  Meta's "one process" framing than its public messaging suggests.
At Meta, the modernization since KDD 2015 has been **incremental rather than
a wholesale shift to MPC or online RL controllers**: a 2023 production system
increased the control-loop frequency roughly 15x — from the KDD 2015 paper's
15-minute loops to **per-minute, per-campaign** decisions — while keeping the
controller itself a **PID-like heuristic** (a piece-wise polynomial function
with a couple dozen scalar parameters). Reinforcement learning (Conservative
Q-Learning) is used **offline**, on logged production data, to tune that
heuristic's parameters; the trained neural network is discarded and only the
tuned parameters ship to production. A/B tested at ~50 billion impressions,
this yielded a statistically significant **+0.17% performance gain (95% CI
+0.05% to +0.3%)**
[[wiki/sources/offline-rl-production-bidding-meta.md]] *(peer_reviewed)*. In
short: faster control loop, RL-tuned PID — not "RL replaces PID."

- Open question: this evidence is Meta-specific. No source found describes
  Google's equivalent modernization (control-loop frequency, or whether/how
  RL is used) for Smart Bidding's pacing layer since 2015 — whether Google
  has followed a similar "RL-tuned heuristic at higher frequency" path, or
  adopted a structurally different (e.g., MPC-based) controller, remains
  unknown.

## Related Pages

- [[wiki/synthesis/bidding-types.md]] — pricing models, bid strategies, and auction mechanisms that pacing operates within
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — explore/exploit framing for budget allocation, including the related open question on bandit-based pacing
- [[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]] — budgeted UCB1 for ad allocation
- [[wiki/synthesis/reddit-ads.md]] — Standard vs. Accelerated pacing as a user-facing advertiser setting
- [[wiki/sources/meta-bid-and-budget-pacing.md]] — Meta's "pacing multiplier" folded into the auction total-value calculation
- [[wiki/sources/google-marketing-live-2026-bidding-budgeting.md]] — Google's 2026 demand-led pacing, positioned alongside Smart Bidding
- [[wiki/sources/offline-rl-production-bidding-meta.md]] — Meta's offline-RL-tuned PID-like pacing controller, 1-minute control loops, +0.17% A/B result at 50B impressions
- [[wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md]] — duplicate framing of the pacing/bid-strategy coupling question
- [[wiki/sources/budget-pacing-algorithms-practical-guide.md]] — control-theoretic survey of pacing algorithms
- [[wiki/sources/smart-pacing-online-ad-campaign-optimization.md]] — production layered-pacing case study (KDD 2015)
