---
title: "What Are the Components That Make Up an Ad Ranking System?"
type: "synthesis"
sources:
  - "web/two-tower-models-engineers-of-ai.md"
  - "web/ad-click-prediction-view-from-the-trenches.md"
  - "web/google-ad-rank-briefing-paper.md"
  - "web/edelman-ostrovsky-schwarz-gsp-auction.md"
  - "web/budget-pacing-algorithms-practical-guide.md"
  - "web/google-ads-about-conversions.md"
  - "web/fatigue-aware-ad-creative-selection.md"
  - "pdf/overlapping-experiment-infrastructure.pdf"
  - "web/rtb-latency-budget-systemdr.md"
  - "web/reddit-contextual-relevance-ads.md"
status: "current"
created: "2026-06-10"
last_updated: "2026-06-10"
---

# What Are the Components That Make Up an Ad Ranking System?

An ad ranking system is not a single model — it is a pipeline of cooperating
subsystems, each solving a different sub-problem, all operating under a shared
~100ms latency constraint and a shared economic objective (maximize long-term
value to users, advertisers, and the platform). The components fall into three
groups: an **online serving pipeline** that turns a request into a served ad in
real time, a **bidding & delivery control** layer that translates advertiser
goals into per-auction bids, and a **feedback & learning loop** that supplies
training signal and continuously evolves every other component.

![what-are-the-components-of-an-ad-ranking-system-diagram-1](/assets/what-are-the-components-of-an-ad-ranking-system-diagram-1.svg)

## 1. Retrieval (Candidate Generation)

The first stage narrows a universe of potentially millions of ads down to a
manageable candidate set (often ~1,000) within a few milliseconds. This is
done with **two-tower (dual-encoder) models**: a user/query tower and an
item/ad tower are trained so that relevant pairs land close together in
embedding space, and the item-side embeddings are precomputed offline and
served via approximate nearest-neighbor (ANN) search (e.g., FAISS) at request
time [[wiki/synthesis/two-tower-factorized-models.md]]. Retrieval typically
consumes ~20ms of the total budget
[[wiki/synthesis/what-is-the-latency-budget-for-ad-ranking.md]].

## 2. Pre-Ranking and Heavy Ranking (Prediction Models)

Retrieved candidates pass through a **funnel of progressively more expensive
models**: a light pre-ranking model cuts ~1,000 candidates to ~200 (~10ms),
and a heavy ranking model (DLRM, DIN, Meta's Lattice) scores the final ~50
candidates with the full feature set (~50-80ms)
[[wiki/synthesis/what-is-the-latency-budget-for-ad-ranking.md]]. The output of
this stage is a set of **predicted probabilities** — most importantly **pCTR**
(predicted click-through rate) and **pCVR** (predicted conversion rate) — that
feed directly into the auction.

Google's production CTR model is a canonical example of how this is done at
scale: the **FTRL-Proximal** online-learning algorithm trains a
billion-coefficient logistic-regression model with per-coordinate learning
rates, L1/L2 regularization for sparsity, and aggressive memory tricks
(fixed-point encoding, probabilistic feature inclusion) so that inference
stays cheap enough to run on every candidate on every request
[[wiki/entities/google-ctr-prediction-system.md]]. Meta's stack instead layers
multiple specialized systems — **Andromeda** (retrieval), **Lattice** (deep
ranking), **GEM** (a foundation model that distills knowledge into smaller
production models), and **ARM** (serving infrastructure that makes
trillion-parameter inference affordable) — onto the same retrieve→rank funnel
[[wiki/synthesis/meta-ad-ranking.md]].

## 3. Quality / Relevance Scoring

Predicted engagement (pCTR/pCVR) is necessary but not sufficient — a system
that only optimized for clicks would surface clickbait. A separate **quality
or relevance score** captures how well an ad matches the user's current
context (the page, query, or feed content they're looking at), independent of
the advertiser's bid. Approaches range from taxonomy matching (IAB categories)
to embedding similarity to LLM-as-judge labeling
[[wiki/concepts/contextual-relevance-advertising.md]]. Reddit's production
pipeline is a concrete example: an Airflow + BigQuery ML + Gemini 2.5 Flash
Lite labeling job scores millions of `<ad, post>` pairs daily, and a
fine-tuned multi-tower relevance model feeds targeting, retrieval, and both
ranking stages
[[wiki/sources/contextual-relevance-of-ads-reddit.md]] *(other)*. This quality
signal is one of the inputs (alongside pCTR) to the auction-level score in the
next component.

## 4. Auction & Pricing

The auction takes the ranked, scored candidates and decides **what gets
shown and what the winner pays**. Ad slots are scarce, perishable, and
heterogeneous in value, so platforms use real-time auctions rather than fixed
prices to discover the market-clearing price for every individual impression
[[wiki/synthesis/why-ads-have-auctions.md]].

- **Allocation**: candidates are ranked by a composite score — Google's
  **Ad Rank** is `LTV = eCPM - costs`, where `eCPM = bid x pCTR` and `costs`
  folds in predicted click quality (pCQ) and landing-page quality (pLQ)
  [[wiki/concepts/google-ad-rank-ltv-scoring.md]]. Meta's analogous score is
  `Total Value = Bid x EAR (estimated action rate) + Ad Quality`
  [[wiki/synthesis/meta-ad-ranking.md]].
- **Pricing**: the winner pays roughly the minimum bid needed to beat the
  next-highest competitor, divided by the relative quality scores — the
  **Generalized Second-Price (GSP)** rule
  [[wiki/concepts/generalized-second-price-auction.md]]. Google additionally
  applies **rGSP**, randomizing the winner among bidders with close LTV scores
  [[wiki/concepts/randomized-gsp-rgsp.md]].
- **Why GSP and not VCG**: VCG is dominant-strategy truthful and efficient,
  but its exact payment rule requires re-solving the allocation once per
  bidder — computationally infeasible inside a ~10-15ms auction window at
  Google's scale, and it generates **less revenue** than GSP's locally
  envy-free equilibrium [[wiki/synthesis/what-is-vcg.md]].

## 5. Bid Strategy (Smart Bidding)

Advertisers rarely set per-auction bids manually. **Bid strategies** translate
a high-level goal (Target CPA, Target ROAS, Maximize Conversions, Cost Cap)
into a per-auction bid using the ranking model's own pCTR/pCVR predictions —
this is "Smart Bidding" or its equivalents across platforms
[[wiki/synthesis/bidding-types.md]]. Bidding decomposes into three largely
independent axes: the **pricing model** (CPM, CPC, CPA, oCPM — what the
advertiser is charged for), the **bid strategy** (how the per-auction bid is
computed), and the **auction mechanism** (GSP/second-price for owned platforms
vs. first-price for programmatic RTB) [[wiki/synthesis/bidding-types.md]].

## 6. Pacing

Pacing controls **when within a campaign's flight** its budget is spent — a
layer distinct from both the auction (which decides if an impression is won)
and the bid strategy (which decides what to bid)
[[wiki/synthesis/ad-pacing.md]]. Without pacing, a campaign would win every
affordable auction until its daily budget exhausted, often within minutes.
Two algorithm families are used in production
[[wiki/sources/budget-pacing-algorithms-practical-guide.md]]:

| Approach | Mechanism |
|---|---|
| **Throttling** | Probabilistically skip auctions based on remaining budget vs. remaining time |
| **Bid modulation** | Continuously scale the submitted bid by a pacing multiplier (PID, MPC, or Dual Online Gradient Descent control) |

A production case study at Yahoo (KDD 2015) bucketed requests into layers by
predicted response rate and adjusted pacing per layer, cutting effective CPC
by 67-79% versus global pacing while keeping spend within ~10% of plan
[[wiki/sources/smart-pacing-online-ad-campaign-optimization.md]].

## 7. Conversion Tracking & Attribution (Training Signal)

The pCVR predictions used in ranking and the reward signal used by Smart
Bidding both depend on knowing which impressions and clicks led to a
**conversion** — an advertiser-defined valuable action (purchase, signup,
lead, call, install)
[[wiki/synthesis/what-is-a-conversion.md]]. Conversions are observed via tags,
pixels, app SDKs, call tracking, and server-side Conversion APIs, then joined
back to the originating ad click/impression through **attribution** —
deciding which touchpoints get credit, within an attribution window, often
under privacy-preserving constraints that only reveal aggregated "attribution
sets" rather than individual user-level joins
[[wiki/sources/statistical-learning-attribution-sets.md]]. Platform analytics
systems (e.g., GA4) extend this by exporting event-level data to BigQuery and
joining it back to ad clicks via identifiers like `gclid`, closing the loop
between on-site behavior and the ranking/bidding models
[[wiki/synthesis/how-does-google-analytics-work.md]].

## 8. Exploration (Bandit Algorithms)

Every prediction model above is only as good as the data it was trained on,
and that data is itself shaped by what the system has chosen to show in the
past — a feedback loop. **Multi-armed bandit algorithms** address this by
deliberately trading some exploitation (showing what the model currently
believes is best) for exploration (trying under-tried options to keep
learning) [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]]. In production
ad systems this shows up in at least three places:

- **Creative selection**: a contextual bandit chooses among candidate
  creatives per impression, with exposure history (ad fatigue) folded into
  the context
  [[wiki/sources/fatigue-aware-ad-creative-selection.md]] *(peer_reviewed)*.
- **Budget allocation**: "budgeted UCB1" learns each ad's click probability
  while respecting a hard per-ad spend cap
  [[wiki/sources/dynamic-ad-allocation-bandits-with-budgets.md]]
  *(peer_reviewed)*.
- **Experimentation**: bandit-based traffic allocation (vs. fixed A/B splits)
  shifted traffic toward better variants in real time, producing a 46%
  average CTR increase across 1,500+ experiments at JD.com
  [[wiki/sources/comparison-lift-bandit-experimentation.md]] *(peer_reviewed)*.

## 9. Experimentation Infrastructure

Every other component — a new ranking model, a new bid-strategy formula, a
new pacing controller, a new relevance signal — is shipped through **A/B
testing**, the mechanism by which an ad ranking system evolves without
breaking production [[wiki/synthesis/how-ab-tests-work.md]]. At the scale of
Google, Meta, or LinkedIn, thousands of experiments run concurrently using
**overlapping/layered experiment infrastructure**: traffic is partitioned into
domains and layers so that an experiment on the ranking model and an
experiment on the auction's reserve price can run simultaneously on the same
traffic without interfering
[[wiki/sources/overlapping-experiment-infrastructure.md]] *(peer_reviewed)*.
Counterfactual logging and triggering ensure that only impressions actually
affected by a change are included in its analysis — critical in ads, where a
ranking change typically affects only a subset of queries
[[wiki/synthesis/how-ab-tests-work.md]].

## The Latency Budget Ties Everything Together

All of the above must execute within a **hard wall-clock budget** — roughly
100ms for Google's auction and open RTB, 200-300ms for Meta's larger
multi-stage stack [[wiki/synthesis/what-is-the-latency-budget-for-ad-ranking.md]].
This budget is *why* the architecture looks the way it does:

- It is why retrieval, pre-ranking, and ranking exist as **separate stages**
  at all — each trades model complexity for candidate-set size
  [[wiki/synthesis/two-tower-factorized-models.md]].
- It is why **GSP, not VCG**, prices the auction — VCG's combinatorial
  payment computation does not fit a ~10-15ms window
  [[wiki/synthesis/what-is-vcg.md]].
- In open RTB, it is enforced as a **hard cutoff**: a DSP bid response that
  arrives even 1ms late is dropped (HTTP 408), not scored late
  [[wiki/sources/rtb-latency-budget-systemdr.md]] *(blog post)*.

## Component Summary

| Component | Question it answers | Key mechanisms | Deep dive |
|---|---|---|---|
| Retrieval | Which ~1,000 ads *could* this user see? | Two-tower + ANN | [[wiki/synthesis/two-tower-factorized-models.md]] |
| Pre-ranking / ranking | How likely is this user to click/convert on each? | pCTR/pCVR models (FTRL-Proximal, DLRM, Lattice) | [[wiki/entities/google-ctr-prediction-system.md]], [[wiki/synthesis/meta-ad-ranking.md]] |
| Quality / relevance | How well does this ad fit the current context? | Embedding similarity, LLM-as-judge | [[wiki/concepts/contextual-relevance-advertising.md]] |
| Auction & pricing | Who wins, and what do they pay? | Ad Rank / LTV, GSP, rGSP | [[wiki/concepts/google-ad-rank-ltv-scoring.md]], [[wiki/synthesis/why-ads-have-auctions.md]] |
| Bid strategy | What should this advertiser bid? | Smart Bidding (Target CPA/ROAS) | [[wiki/synthesis/bidding-types.md]] |
| Pacing | When during the flight should the budget be spent? | Throttling, bid modulation (PID/MPC) | [[wiki/synthesis/ad-pacing.md]] |
| Conversion tracking & attribution | Did this ad lead to value? | Pixels/Conversion APIs, attribution sets | [[wiki/synthesis/what-is-a-conversion.md]] |
| Exploration | How do we keep learning without exploiting blind spots? | Contextual bandits, budgeted UCB1 | [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] |
| Experimentation | How do we ship changes safely? | Layered A/B testing | [[wiki/synthesis/how-ab-tests-work.md]] |
| Latency budget | How fast must all of this run? | ~100ms (Google/RTB), 200-300ms (Meta) | [[wiki/synthesis/what-is-the-latency-budget-for-ad-ranking.md]] |

## Open Questions

- Open question: How tightly coupled are the bid-strategy and pacing layers
  in production at Google/Meta scale — are they unified into a single
  optimization, or do they operate as separable systems that interact only
  through the submitted bid? [[wiki/synthesis/ad-pacing.md]] flags this as
  unresolved.
- Open question: Do major platforms expose the exploration (bandit) layer as
  a first-class, separately-tunable component, or is it implicit inside the
  ranking/bid-strategy models' own training-data collection?
  [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] flags a related
  question about whether Smart Bidding uses bandit-style exploration
  internally.

## Related Pages

- [[wiki/synthesis/two-tower-factorized-models.md]] — retrieval architecture
- [[wiki/entities/google-ctr-prediction-system.md]] — production CTR prediction
- [[wiki/synthesis/meta-ad-ranking.md]] — Meta's 5-system ranking stack
- [[wiki/concepts/contextual-relevance-advertising.md]] — quality/relevance scoring
- [[wiki/synthesis/why-ads-have-auctions.md]] — auction rationale
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]] — Google's Ad Rank/LTV formula
- [[wiki/synthesis/what-is-vcg.md]] — why GSP, not VCG
- [[wiki/synthesis/bidding-types.md]] — pricing models and bid strategies
- [[wiki/synthesis/ad-pacing.md]] — budget pacing
- [[wiki/synthesis/what-is-a-conversion.md]] — conversion tracking and attribution
- [[wiki/synthesis/how-does-google-analytics-work.md]] — analytics-to-ranking data flow
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — exploration layer
- [[wiki/synthesis/how-ab-tests-work.md]] — experimentation infrastructure
- [[wiki/synthesis/what-is-the-latency-budget-for-ad-ranking.md]] — the cross-cutting latency constraint
