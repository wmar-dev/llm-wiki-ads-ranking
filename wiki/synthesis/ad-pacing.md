---
title: "What Is Ad Pacing?"
type: "synthesis"
sources:
  - "web/budget-pacing-algorithms-practical-guide.md"
  - "web/smart-pacing-online-ad-campaign-optimization.md"
  - "web/dynamic-ad-allocation-bandits-with-budgets.md"
  - "web/reddit-ads-how-it-works.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
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

- Open question: How do major platforms (Google Smart Bidding, Meta) combine
  pacing (spend-over-time control) with their bid-strategy layer (Target
  CPA/ROAS, Cost Cap)? The 2025 practical guide treats these as adjacent but
  separable systems; no source reviewed describes a unified production
  architecture at Google or Meta scale.
- Open question: The KDD 2015 system used 15-minute control loops at
  billions of impressions/day in 2015 — what control-loop latency and
  algorithm (PID/MPC/DOGD) do current (2026) production systems use, and has
  the field shifted toward MPC or learned (RL-based) controllers as compute
  costs have fallen?

## Related Pages

- [[wiki/synthesis/bidding-types.md]] — pricing models, bid strategies, and auction mechanisms that pacing operates within
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — explore/exploit framing for budget allocation, including the related open question on bandit-based pacing
- [[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]] — budgeted UCB1 for ad allocation
- [[wiki/synthesis/reddit-ads.md]] — Standard vs. Accelerated pacing as a user-facing advertiser setting
- [[wiki/sources/budget-pacing-algorithms-practical-guide.md]] — control-theoretic survey of pacing algorithms
- [[wiki/sources/smart-pacing-online-ad-campaign-optimization.md]] — production layered-pacing case study (KDD 2015)
