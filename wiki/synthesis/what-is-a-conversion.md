---
title: "What Is a Conversion?"
type: "synthesis"
sources:
  - "web/google-ads-about-conversions.md"
  - "web/statistical-learning-attribution-sets.md"
  - "web/google-ad-rank-briefing-paper.md"
status: "current"
created: "2026-06-10"
last_updated: "2026-06-10"
---

# What Is a Conversion?

A **conversion** is an advertiser-defined customer action that the advertiser
considers valuable — a purchase, sign-up, lead form submission, app install,
in-app purchase, phone call, store visit, or any other action the business wants
more of [[wiki/sources/google-ads-about-conversions.md]] *(official documentation)*.
There is no fixed taxonomy: each advertiser configures which events count as
conversions (and how much each is worth) for their account.

![what-is-a-conversion-diagram-1](/assets/what-is-a-conversion-diagram-1.svg)

## How Conversions Are Tracked

| Mechanism | How it works |
|---|---|
| **Tags / pixels** | A snippet on the confirmation/"thank you" page fires when the action completes, matched back to a click identifier (cookie, GCLID) set when the user clicked the ad |
| **App SDKs / Play Store reporting** | Installs and in-app purchases are reported automatically — no manual tagging |
| **Call tracking** | Forwarding numbers shown in ads automatically record and attribute calls |
| **Offline / imported conversions** | CRM data, in-store sales, or events from third-party analytics (e.g., Google Analytics, Firebase) are uploaded/imported |
| **Enhanced Conversions / Conversion API** | Hashed first-party data (e.g., email) sent server-side, improving match rates as cookie-based tracking degrades |

[[wiki/sources/google-ads-about-conversions.md]] *(official documentation)*

## Attribution: Connecting a Conversion Back to an Ad

A conversion is only useful for ranking/bidding if it can be **attributed** to
the ad exposure that caused it. Google's "All conversions" reporting matches a
conversion to the ad click (or, for **view-through conversions**, an ad
impression) that preceded it within an **attribution/lookback window** — commonly
1, 7, or 30 days, with longer windows needed for purchases with longer
consideration cycles (e.g., mobile app installs that convert days after the click)
[[wiki/sources/google-ads-about-conversions.md]].

As third-party cookies are deprecated, browsers increasingly expose only
**privacy-preserving attribution APIs** (e.g., Privacy Sandbox's Attribution
Reporting API), which return an **attribution set** — a group of candidate clicks
any one of which could be the true cause — rather than a single deterministic
click→conversion link. Recent work shows that conversion-prediction models can
remain statistically unbiased under this coarsening if trained with the correct
estimator, but naive credit-splitting heuristics lose accuracy as attribution sets
grow larger and more overlapping
[[wiki/sources/statistical-learning-attribution-sets.md]].

## Conversion Rate (CVR) and pCVR

**Conversion rate** = conversions ÷ clicks (or ÷ impressions, for view-through).
In production ranking/bidding systems, a machine-learned **pCVR** (predicted
conversion rate) — and often **predicted conversion value** — is computed per
auction, analogous to pCTR for clicks
[[wiki/concepts/google-ad-rank-ltv-scoring.md]].

## How Conversions Feed Bidding and Ranking

Conversions are the foundation of **performance-based pricing and bidding**:

- **CPA / CPL** (cost-per-action / cost-per-lead) bills the advertiser directly
  per conversion [[wiki/synthesis/bidding-types.md]].
- **oCPM** is nominally billed per 1,000 impressions, but the platform's pCVR
  model decides *which* impressions to deliver to maximize conversions
  [[wiki/synthesis/bidding-types.md]].
- **Smart Bidding** strategies — **Target CPA**, **Target ROAS**, **Maximize
  Conversions** — use pCVR/predicted conversion value to set a per-auction bid
  automatically, which then enters the Ad Rank/LTV auction as the advertiser's
  effective bid [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
  [[wiki/sources/google-ads-about-conversions.md]].

**Inference:** conversions don't typically enter the ranking formula directly
(Google's LTV = eCPM − costs is computed from pCTR, pCQ, pLQ, and the bid
[[wiki/concepts/google-ad-rank-ltv-scoring.md]]) — instead, conversion signals
shape the **bid itself** via Smart Bidding before that bid is plugged into the
auction. This is why "what is a conversion" and "what is Ad Rank"
[[wiki/synthesis/what-is-ad-rank.md]] are related but distinct questions:
conversions are a *demand-side* signal that determines how much an advertiser is
willing to pay, while Ad Rank is the *supply-side* mechanism that allocates and
prices slots given those bids.

Improvements in conversion prediction translate directly into measurable lift —
e.g., scaling up recommendation/ranking models has been shown to produce a 4.3%
conversion uplift in production [[wiki/sources/llatte-scaling-laws-recommendation.md]],
and Reddit's automated MAX campaigns reported a 27% increase in conversions
relative to manual campaigns [[wiki/sources/reddit-max-campaigns-trajectory.md]]
*(other)*.

## Why It Matters for Ads Ranking

- Conversions are the **ground-truth label** for performance advertising — every
  CPA/ROAS-based bid strategy is ultimately a bet on predicted conversion
  behavior.
- **Privacy regulation** is reshaping conversion measurement from deterministic
  (cookie-based) to probabilistic (attribution-set-based), which changes what
  training signal is available to pCVR models
  [[wiki/sources/statistical-learning-attribution-sets.md]].
- Conversions sit at the intersection of **measurement** (how does the platform
  know it happened?), **attribution** (which ad gets credit?), and **ranking**
  (how does that credit change future bids and allocations?).

## Related Pages

- [[wiki/sources/google-ads-about-conversions.md]]
- [[wiki/synthesis/bidding-types.md]]
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
- [[wiki/sources/statistical-learning-attribution-sets.md]]
- [[wiki/synthesis/what-is-ad-rank.md]]
