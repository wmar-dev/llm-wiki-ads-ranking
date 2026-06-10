---
title: "What Are the Different Bidding Types?"
type: "synthesis"
sources:
  - "web/digital-ad-formats-epom.md"
  - "web/google-ad-rank-briefing-paper.md"
  - "web/reddit-ads-how-it-works.md"
  - "web/reddit-max-campaigns.md"
  - "web/edelman-ostrovsky-schwarz-gsp-auction.md"
  - "web/tiktok-bidding-strategies.md"
  - "web/first-price-second-price-auction-setupad.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
---

# What Are the Different Bidding Types?

"Bidding" in digital advertising actually bundles together three independent
decisions: **what you pay for**, **how aggressively the system spends your
budget**, and **how the platform clears competing bids into a price**.
Confusing these three axes is a common source of confusion — e.g. CPC and
"second-price" are not the same thing; CPC is a pricing model, second-price
is an auction-clearing rule, and either can combine with manual or automated
bid strategies.

![synthesis-bidding-types-diagram-1](/assets/synthesis-bidding-types-diagram-1.svg)

---

## Axis 1: Pricing Model — What You Pay For

The pricing model determines the unit of delivery the advertiser is billed
for [[wiki/synthesis/types-of-ads.md]]:

| Model | Billed per | Typical use | Typical range |
|---|---|---|---|
| **CPM** (cost per mille) | 1,000 impressions | Awareness, reach, branding | $0.50 – $50 [[wiki/synthesis/types-of-ads.md]] |
| **CPC** (cost per click) | Click | Traffic, search, consideration | $0.10 – $10+ [[wiki/synthesis/types-of-ads.md]] |
| **CPA / CPL** (cost per action / lead) | Conversion or lead | Performance/affiliate marketing, popularized in the early 2000s | Varies by vertical [[wiki/synthesis/types-of-ads.md]] |
| **CPV** (cost per view) | Video view (e.g., 15-30s or completion) | Video awareness campaigns | $0.03 – $0.20 [[wiki/synthesis/types-of-ads.md]] |
| **oCPM** (optimized CPM) | 1,000 impressions, but the platform's ML chooses *which* impressions to serve to maximize conversions | App installs, conversion campaigns on social platforms | — [[wiki/sources/tiktok-bidding-strategies.md]] *(official documentation)* |

**Inference:** oCPM is best understood as a hybrid — the advertiser is
nominally billed on a CPM basis, but the platform's prediction models (pCTR,
pCVR) decide which specific impressions to fill, effectively converting a CPM
buy into conversion-optimized delivery. This is conceptually the bridge
between Axis 1 (pricing model) and Axis 2 (bid strategy) below.

---

## Axis 2: Bid Strategy — How the System Spends Your Budget

Independent of the pricing model, advertisers choose **how much control** to
hand to the platform's optimization algorithms:

### Manual Bidding

The advertiser sets an explicit bid (e.g., max CPC or max CPM) for each
ad/ad group, and that bid is used directly in the auction. Reddit calls this
"Manual bidding — set specific max bids per action"
[[wiki/synthesis/reddit-ads.md]].

### Automated / Smart Bidding

The platform's ML sets bids per-auction using real-time signals (device,
location, time, audience, remarketing lists) to hit an advertiser-specified
goal. Google's **Smart Bidding** strategies illustrate the range of goals
[[wiki/concepts/google-ad-rank-ltv-scoring.md]]:

| Strategy | Goal |
|---|---|
| Target CPA | Maximize conversions at a target cost-per-acquisition |
| Target ROAS | Maximize conversion value at a target return-on-ad-spend |
| Maximize Clicks | Spend the full budget to get as many clicks as possible |
| Maximize Conversions | Spend the full budget to get as many conversions as possible |
| Enhanced CPC | Adjust a manual bid up or down to capture more conversions |
| Target Impression Share | Reach a specified fraction of targeted queries |

TikTok's automated strategies map onto the same two patterns
[[wiki/sources/tiktok-bidding-strategies.md]] *(official documentation)*:

- **Cost Cap** ≈ Target CPA — advertiser sets a target cost per action; the
  system holds the *average* CPA near that target even during competitive
  periods. Best for upper-funnel efficiency goals (reach, video views).
- **Maximum Delivery** ≈ Maximize Conversions — no target CPA; the system
  spends the full budget to maximize total conversion volume, letting CPA
  fluctuate daily.

Reddit's **MAX Campaigns** (beta, January 2026) go a step further, using
"Reddit Community Intelligence" (signals from 23B+ posts/comments) to predict
the value of every impression and auto-select creative, placement, and budget
allocation — not just the bid
[[wiki/sources/reddit-max-campaigns.md]] *(official announcement)*.

**Inference:** Across Google, TikTok, and Reddit, automated bid strategies
converge on the same two archetypes — "hit this efficiency target" (Target
CPA / Cost Cap) vs. "spend everything as efficiently as possible without a
hard target" (Maximize Conversions / Maximum Delivery) — even though each
platform gives them different names.

---

## Axis 3: Auction Mechanism — How Bids Clear Into a Price

This axis determines what the *winner* actually pays, independent of the
pricing model or bid strategy:

### Second-Price / GSP (Search & Social Feeds)

The Vickrey second-price auction (1961) — winner pays the second-highest bid
plus a small increment — generalizes to multi-slot **GSP (Generalized
Second-Price)** auctions, the mechanism behind search and social feed ads
[[wiki/synthesis/vickrey-and-gsp.md]] [[wiki/sources/edelman-ostrovsky-schwarz-gsp-auction.md]]
*(peer-reviewed, AER 2007)*. Ads are ranked by `bid × quality score`
(Google's Ad Rank uses `LTV = eCPM - costs`
[[wiki/concepts/google-ad-rank-ltv-scoring.md]]; Meta uses
`Total Value = (Bid × Estimated Action Rate) + Ad Quality`
[[wiki/synthesis/meta-ad-ranking.md]]). Google additionally randomizes the
winner among close-LTV bidders since 2019 (**rGSP**)
[[wiki/concepts/randomized-gsp-rgsp.md]].

### First-Price (Programmatic Display / RTB)

Open-exchange programmatic display and video largely moved to **first-price
auctions** — the winner pays exactly what they bid — starting with Google Ad
Manager's 2019 transition for display/video inventory
[[wiki/sources/first-price-second-price-auction-setupad.md]] *(blog post)*.
This shift was driven by **header bidding**: once multiple ad exchanges bid
on the same impression simultaneously, a per-exchange second-price auction
would discard "less competitive" bids before they ever reached the
publisher's final auction, depressing win rates. With first-price, the
buyer's submitted bid competes directly in the final auction.

| | Second-price / GSP | First-price |
|---|---|---|
| Winner pays | ~second-highest bid (+ε), adjusted by quality | Their exact bid |
| Used by | Search (Google), social feeds (Meta, Reddit) | Open-exchange programmatic display/video |
| Why | Quality-weighted ranking aligns relevance with revenue; higher revenue than VCG [[wiki/sources/edelman-ostrovsky-schwarz-gsp-auction.md]] | Header bidding made second-price hard to optimize across simultaneous exchanges; ~78% of publishers saw revenue gains after switching [[wiki/sources/first-price-second-price-auction-setupad.md]] |
| Strategic risk | Bid shading is rational but bounded (locally envy-free equilibrium) [[wiki/synthesis/vickrey-and-gsp.md]] | Aggressive bid shading by buyers can divert up to ~20% of publisher revenue if floors aren't set [[wiki/sources/first-price-second-price-auction-setupad.md]] |

---

## Putting the Axes Together

A single real-world "bid" is a combination of all three axes. For example:

- A Google Search campaign on **Target CPA** (Axis 2: automated) is billed in
  **CPC** terms (Axis 1) but cleared via **rGSP** (Axis 3)
  [[wiki/concepts/google-ad-rank-ltv-scoring.md]].
- A TikTok app-install campaign on **oCPM** (Axis 1, which already embeds
  conversion optimization — Axis 2) is delivered against TikTok's internal
  ranking, not an open first-price exchange
  [[wiki/sources/tiktok-bidding-strategies.md]].
- A programmatic display buy via header bidding is typically **CPM** (Axis 1),
  set either manually or via a DSP's automated bidder (Axis 2), and cleared
  via **first-price** (Axis 3)
  [[wiki/sources/first-price-second-price-auction-setupad.md]].

---

## Open Questions

- Open question: How do DSPs' automated bid-shading algorithms for
  first-price auctions compare in sophistication to Google's/Meta's Smart
  Bidding for second-price/GSP auctions — do they use similar ML techniques
  (e.g., contextual bandits, as in [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]])?

## Related Pages

- [[wiki/synthesis/types-of-ads.md]] — ad format taxonomy and per-format pricing
- [[wiki/synthesis/vickrey-and-gsp.md]] — Vickrey/GSP second-price theory
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]] — Google's Ad Rank, LTV scoring, and Smart Bidding
- [[wiki/concepts/randomized-gsp-rgsp.md]] — rGSP randomization mechanism
- [[wiki/synthesis/reddit-ads.md]] — Reddit's manual/automatic bidding and MAX Campaigns
- [[wiki/synthesis/meta-ad-ranking.md]] — Meta's auction equation
- [[wiki/synthesis/bandit-algorithms-in-ad-systems.md]] — exploration/exploitation in ad delivery
- [[wiki/sources/tiktok-bidding-strategies.md]] — TikTok bidding options and strategies
- [[wiki/sources/first-price-second-price-auction-setupad.md]] — first-price vs second-price in programmatic
- [[wiki/synthesis/why-does-google-charge-per-click-while-meta-charges-per-impression.md]] — why CPC/CPM eCPM normalization lets oCPM and Smart Bidding bridge billing units
