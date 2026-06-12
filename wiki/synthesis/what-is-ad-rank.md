---
title: "What Is Ad Rank?"
type: "synthesis"
sources:
  - "web/google-ad-rank-briefing-paper.md"
  - "web/edelman-ostrovsky-schwarz-gsp-auction.md"
  - "web/rgsp-randomized-second-price-explained.md"
  - "web/vickrey-clarke-groves-mechanism.md"
  - "web/meta-ads-algorithm-2026-guide.md"
  - "web/google-ads-about-conversions.md"
status: "current"
created: "2026-06-10"
last_updated: "2026-06-10"
---

# What Is Ad Rank?

**Ad Rank** is the score Google computes for every ad in a Search auction that
determines three things at once: **whether the ad is eligible to show at
all**, **what position it gets relative to other ads**, and **what price
(Actual CPC) the advertiser pays**. It is Google's production refinement of
the textbook "rank by `bid x quality score`" rule from the
[[wiki/concepts/generalized-second-price-auction.md|Generalized Second-Price (GSP) auction]],
expressed instead as a cost-aware expected-value score called **LTV**, and
since January 2019 it includes a randomized tie-breaking layer called
[[wiki/concepts/randomized-gsp-rgsp.md|rGSP]]
[[wiki/sources/google-ad-rank-briefing.md]] *(primary source — DOJ litigation
exhibit UPX0010, "How Search Ads are Ranked and Priced on Google")*.

![what-is-ad-rank-diagram-1](/assets/what-is-ad-rank-diagram-1.svg)

## 1. The Core Formula: LTV

Google's internal name for Ad Rank's score is **LTV**:

```
LTV = eCPM - (impression cost + click cost)

where:
  eCPM           = bid x pCTR
  impression cost = f(1 - pCQ)
  click cost      = f(1 - pLQ)
```

[[wiki/concepts/google-ad-rank-ltv-scoring.md]]
[[wiki/sources/google-ad-rank-briefing.md]] *(primary source)*.

| Input | Meaning | Where it comes from |
|---|---|---|
| **bid** (Max CPC) | The advertiser's willingness to pay per click | Set manually, or computed per-auction by **Smart Bidding** [[wiki/synthesis/bidding-types.md]] |
| **pCTR** | Predicted probability the ad is clicked if shown | Heavy-ranking ML models [[wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md]] |
| **pCQ** | Predicted creative quality (ad relevance/expected CTR-style quality of the creative itself) | Quality/relevance scoring models [[wiki/concepts/google-ad-rank-ltv-scoring.md]] |
| **pLQ** | Predicted landing page quality/experience | Landing page evaluation models [[wiki/concepts/google-ad-rank-ltv-scoring.md]] |

`eCPM = bid x pCTR` converts a per-click bid into an **expected revenue per
thousand impressions** — the same normalization that lets CPC, CPM, and CPA
bids be compared on one scale
[[wiki/synthesis/why-does-google-charge-per-click-while-meta-charges-per-impression.md]].
The two cost terms then subtract off the *expected harm* of showing a
low-quality ad (`f(1-pCQ)`) or sending users to a poor landing page
(`f(1-pLQ)`) — Ad Rank nets these directly against expected revenue rather
than folding "quality" into a single multiplicative factor.

## 2. From "Bid x Quality Score" to LTV

Textbook GSP ranks ads by `bid x quality_score`
[[wiki/concepts/generalized-second-price-auction.md]]. LTV is recognizable as
the same family of score — it is still increasing in bid and in predicted
ad quality — but reformulated so that quality enters as **subtracted expected
costs** rather than a **multiplied scaling factor**:

| | Textbook GSP | Google Ad Rank (LTV) |
|---|---|---|
| Ranking score | `bid x quality_score` | `eCPM - (impression cost + click cost)` = `(bid x pCTR) - f(1-pCQ) - f(1-pLQ)` |
| Quality enters as | A multiplicative scaling factor | Subtracted expected-cost terms (in the same eCPM units as revenue) |
| Units of the score | Abstract ("quality-weighted bid") | Expected value per mille impressions (eCPM-equivalent) |
| Eligibility rule | Implicit (score > 0 trivially if bid > 0) | Explicit: **LTV > 0** required, regardless of bid |

**Inference:** expressing quality as a cost subtracted in the same units as
expected revenue (rather than a unitless multiplier) makes the **LTV > 0
eligibility threshold** meaningful — a sufficiently low-quality ad can have
*negative* LTV (the expected cost of showing it exceeds its expected revenue)
and be excluded entirely, something a pure multiplicative `bid x quality`
score cannot represent cleanly when quality is a fraction in (0, 1].

## 3. Eligibility and Pricing

- **Eligibility**: an ad must have **LTV > 0** to be considered for any slot.
  Ads that fail this — typically very low pCQ or pLQ relative to their bid —
  are not shown, regardless of bid size
  [[wiki/concepts/google-ad-rank-ltv-scoring.md]].
- **Pricing (Actual CPC)**: among eligible ads, the winner pays the minimum
  bid that would have been needed to (a) clear the LTV > 0 threshold **and**
  (b) still beat the next-highest-LTV competitor — a second-price-style rule
  applied in LTV-space rather than raw-bid-space
  [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
  [[wiki/sources/google-ad-rank-briefing.md]].
- **Reserve pricing**: if no competing ad clears the LTV > 0 threshold, the
  winner pays a reserve price rather than a competitor-derived price
  [[wiki/concepts/google-ad-rank-ltv-scoring.md]].

## 4. rGSP: Randomized Tie-Breaking Since January 2019

Since January 2019, Google does not always award the slot to the single
highest-LTV ad. When the top LTV scores are **"close enough"** to each other,
the winner is selected **at random** from that group — but the price is
unaffected: the winner (whoever it is) pays the next-highest qualifying bid
plus $0.01
[[wiki/concepts/randomized-gsp-rgsp.md]] [[wiki/synthesis/rgsp.md]]
[[wiki/sources/google-ad-rank-briefing.md]].

This came to light during *United States v. Google* antitrust litigation:
internal evidence cited a case where an ad with **3.7x** the LTV of a
competitor still lost the randomized draw, and a Google executive (Adam Juda)
described the change in terms of trading a small amount of allocative
precision for additional revenue — plaintiffs' estimates put the effect at
roughly a 5-10% advertiser cost increase and roughly a 10% revenue increase
[[wiki/concepts/randomized-gsp-rgsp.md]] *(litigation claims, not Google's own
disclosed figures)*. The exact width of the "close enough" band and the
probability distribution used for the random draw remain undisclosed
[[wiki/concepts/randomized-gsp-rgsp.md]] [[wiki/synthesis/rgsp.md]].

**In short: Ad Rank = LTV ranking + LTV>0 eligibility + LTV-space second
pricing, with rGSP layered on top as a randomized tie-break among
near-equal-LTV ads.**

## 5. Ad Rank vs. GSP vs. VCG

| Mechanism | Ranking rule | Payment rule | Strategic property |
|---|---|---|---|
| **VCG** | Allocate to maximize total reported value | Pay the externality imposed on others | Truthful bidding is a dominant strategy [[wiki/synthesis/what-is-vcg.md]] |
| **Textbook GSP** | `bid x quality_score`, highest first | Minimum bid to hold position (next-highest, quality-adjusted) | Locally envy-free equilibrium; same advertiser payoffs as VCG, higher platform revenue [[wiki/concepts/generalized-second-price-auction.md]] [[wiki/synthesis/vickrey-and-gsp.md]] |
| **Google Ad Rank (LTV)** | `LTV = eCPM - costs`, highest first, subject to LTV > 0 | Minimum bid to clear threshold *and* beat next competitor's LTV; reserve price otherwise | Same GSP family — locally envy-free equilibrium reasoning applies to the deterministic ranking step [[wiki/concepts/google-ad-rank-ltv-scoring.md]] |
| **Google Ad Rank + rGSP** | As above, but randomized among "close enough" top-LTV ads | Next-highest qualifying bid + $0.01, regardless of which near-tied ad wins | **Inference:** randomization breaks the clean correspondence to a single deterministic locally envy-free equilibrium — no formal extension of the GSP equilibrium results to rGSP has been published [[wiki/concepts/randomized-gsp-rgsp.md]] |

Ad Rank is best understood as **GSP's `bid x quality_score` idea, re-derived
in cost-accounting terms (LTV) so that quality has explicit, subtractable
units, plus a randomization layer (rGSP) that the original GSP theory does
not cover** [[wiki/concepts/generalized-second-price-auction.md]]
[[wiki/synthesis/what-is-vcg.md]].

## 6. Where Ad Rank's Inputs Come From

Ad Rank does not operate in isolation — it is the point where several other
subsystems' outputs converge
[[wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md]]:

- **pCTR, pCQ, pLQ** are produced by the ranking and quality-scoring models
  that sit upstream of the auction
  [[wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md]].
- **The bid** is either set manually by the advertiser or computed
  per-auction by **Smart Bidding** (Target CPA, Target ROAS, Maximize
  Conversions), which uses **pCVR** — predicted conversion rate — derived
  from conversion data flowing back through Google Ads/GA4
  [[wiki/synthesis/what-is-a-conversion.md]]
  [[wiki/synthesis/how-does-google-analytics-work.md]]
  [[wiki/sources/google-ads-about-conversions.md]].

As [[wiki/synthesis/what-is-a-conversion.md]] frames it: conversions and
Smart Bidding are the **demand-side** signal that determines *how much* an
advertiser is willing to pay, while **Ad Rank is the supply-side mechanism**
that allocates slots and sets prices *given* those bids. The two are
distinct stages of the same pipeline, connected by the bid that Smart Bidding
hands to Ad Rank each auction.

## 7. Ad Rank vs. Meta's Total Value

Meta's analogous score for its feed auction is:

```
Total Value = (Bid x Estimated Action Rate) + Ad Quality
```

[[wiki/synthesis/meta-ad-ranking.md]]. Both Ad Rank/LTV and Meta's Total Value
are members of the same conceptual family — a **GSP-style ranking score that
normalizes a bid into an expected-value-per-impression figure and adjusts it
for predicted quality**
[[wiki/synthesis/why-does-google-charge-per-click-while-meta-charges-per-impression.md]].
The visible difference (Google nets quality as *subtracted costs*; Meta adds
quality as a *bonus term*) is a difference in formula shape, not in the
underlying auction-theoretic role each plays.

## Open Questions

- Open question: the canonical formula leaves `f()` — the function mapping
  `(1 - pCQ)` and `(1 - pLQ)` into cost units — unspecified. Is `f()` linear,
  and are its outputs denominated directly in eCPM-equivalent dollars (so that
  `LTV > 0` is a literal break-even test), or in some intermediate
  quality-score units that are rescaled before being compared to `eCPM`?
  [[wiki/sources/google-ad-rank-briefing.md]] does not specify.
- Open question: "Ad Rank" as documented (and as named in the DOJ exhibit, "How
  Search Ads are Ranked and Priced on **Google**") describes Search auctions
  specifically. Does Google apply the same `LTV = eCPM - costs` formula,
  including the `pCQ`/`pLQ` cost terms, to its CPM-billed Display Network and
  YouTube inventory, or do those surfaces use a structurally different ranking
  score? [[wiki/concepts/google-ad-rank-ltv-scoring.md]]

## Related Pages

- [[wiki/synthesis/simple-ads-auction-python.md]] — Python implementation of the LTV formula, eligibility filter, and second-price-in-LTV-space payment rule
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]] — detailed LTV formula and component definitions
- [[wiki/concepts/randomized-gsp-rgsp.md]] — rGSP randomization mechanism and DOJ findings
- [[wiki/synthesis/rgsp.md]] — rGSP synthesis with "From GSP to rGSP" walkthrough
- [[wiki/concepts/generalized-second-price-auction.md]] — textbook GSP theory
- [[wiki/synthesis/vickrey-and-gsp.md]] — Vickrey/GSP second-price theory
- [[wiki/synthesis/what-is-vcg.md]] — VCG mechanism and why ad platforms use GSP instead
- [[wiki/synthesis/bidding-types.md]] — pricing models, bid strategies, and auction mechanisms
- [[wiki/synthesis/what-is-a-conversion.md]] — pCVR, Smart Bidding, and the demand-side/supply-side distinction
- [[wiki/synthesis/how-does-google-analytics-work.md]] — how conversion data reaches Smart Bidding
- [[wiki/synthesis/meta-ad-ranking.md]] — Meta's Total Value formula
- [[wiki/synthesis/why-does-google-charge-per-click-while-meta-charges-per-impression.md]] — eCPM normalization across platforms
- [[wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md]] — where Ad Rank fits in the overall ranking pipeline
