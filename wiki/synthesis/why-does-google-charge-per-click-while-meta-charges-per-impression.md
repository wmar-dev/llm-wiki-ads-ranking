---
title: "Why Does Google Charge Per Click While Meta Charges Per Impression?"
type: "synthesis"
sources:
  - "web/pay-per-pricing-models-digital-advertising-martech.md"
  - "web/google-ad-rank-briefing-paper.md"
  - "web/meta-ads-algorithm-2026-guide.md"
  - "web/tiktok-bidding-strategies.md"
status: "current"
created: "2026-06-10"
last_updated: "2026-06-10"
---

# Why Does Google Charge Per Click While Meta Charges Per Impression?

The premise needs one correction before the "why": neither platform is
locked to a single billing unit. Google's Display Network and YouTube bill on
CPM, and Meta supports CPC bidding alongside its CPM/oCPM defaults
[[wiki/synthesis/bidding-types.md]]. The real pattern is narrower —
**Google's flagship Search product defaults to CPC, while Meta's flagship Feed
product defaults to CPM (often via oCPM)** — and that pattern traces back to
each format's history, the predictability of the user action being billed,
and how risk is split between the platform and the advertiser.

![why-does-google-charge-per-click-while-meta-charges-per-impression-diagram-1](/assets/why-does-google-charge-per-click-while-meta-charges-per-impression-diagram-1.svg)

## 1. Different Origins: Search vs. Display Heritage

The two billing conventions were established in different eras for different
formats and never fully converged:

- **CPM** became the standard for **display advertising** starting around
  1995-96, when Netscape, Infoseek, and especially DoubleClick's 1996 launch
  popularized billing by impression — a direct carryover from offline media
  (TV, print, radio), where "reach" was already the currency
  [[wiki/sources/pay-per-pricing-models-digital-advertising-martech.md]]
  *(blog post)*.
- **CPC** was pioneered by Goto.com in 1998 specifically for **paid search**,
  formally adopted by Google in 2002, and has been the standard for search
  ever since
  [[wiki/sources/pay-per-pricing-models-digital-advertising-martech.md]]
  *(blog post)*.

Meta's ad product is a feed — a descendant of display advertising's
attention-based, "reach a scrolling audience" model. Google's flagship product
is search — a query-driven, intent-based format that CPC was invented for.
Each platform's default billing unit is largely an inheritance from the format
it grew out of, not an arbitrary choice made independently by each company.

## 2. Predictability and Risk Allocation

The deeper economic reason is **who bears the risk that an impression doesn't
"work"** [[wiki/sources/pay-per-pricing-models-digital-advertising-martech.md]]
*(blog post)*:

| Billing unit | What the platform guarantees | Who bears the risk of a "wasted" impression |
|---|---|---|
| **CPM** | The ad is shown | The advertiser — they pay regardless of whether the user engages |
| **CPC** | The ad is shown *and* clicked | The platform — an impression with no click earns nothing |
| **CPA** | The ad is shown, clicked, *and* converts | The platform almost entirely — the riskiest unit for the platform |

Clicks on a search results page are **frequent, immediate, and highly
predictable** from query and ad text alone — Google's pCTR model is the
single most important input to its Ad Rank score precisely because it is so
predictive [[wiki/concepts/google-ad-rank-ltv-scoring.md]]. Because
click-through is so predictable per query, Google can absorb the risk of
billing only on click (CPC) without much uncertainty in its revenue.

Feed impressions are different: a user scrolling Instagram or Facebook is in
a **discovery, not a transaction, mindset**. Whether a given impression leads
to *any* downstream action — a click, a video view, an app install, a
purchase — is far less predictable per impression, and the "right" action to
optimize for varies by campaign objective. Billing per impression (CPM) lets
Meta monetize that inventory regardless of which (if any) downstream action
occurs, while still using its own prediction models internally to decide
*which* impressions to allocate to *which* advertisers
[[wiki/synthesis/meta-ad-ranking.md]].

## 3. Both Auctions Actually Clear in the Same Currency: eCPM

Despite the different advertiser-facing billing units, **both platforms'
internal auctions rank candidates by an expected value per impression** — the
billing unit and the auction currency are two different things
[[wiki/sources/pay-per-pricing-models-digital-advertising-martech.md]]
*(blog post)*:

- **Google**: `LTV = eCPM - costs`, where `eCPM = bid(CPC) x pCTR`. A CPC bid
  is converted into an expected-revenue-per-impression figure before it's
  compared to other ads [[wiki/concepts/google-ad-rank-ltv-scoring.md]].
- **Meta**: `Total Value = (Bid x Estimated Action Rate) + Ad Quality`. Even
  when the advertiser's bid is denominated in CPM, Meta's "Estimated Action
  Rate" plays the same normalizing role as Google's pCTR — converting a bid
  toward whatever objective (click, install, purchase) the campaign targets
  into a comparable per-impression score
  [[wiki/synthesis/meta-ad-ranking.md]].

The general form of this normalization, `eCPM = CPC x pCTR x 1000` (or
`eCPM = CPA x pCVR x pCTR x 1000` for conversion-based bids), is how *any*
auction can rank CPM, CPC, and CPA bids against each other on one scale
[[wiki/sources/pay-per-pricing-models-digital-advertising-martech.md]]
*(blog post)*. **The billing unit is a product/UX decision about what story
to tell the advertiser ("you only pay for clicks" vs. "you're buying reach");
the auction currency underneath is impression-equivalent value either way.**

## 4. oCPM Is the Bridge

Meta's (and TikTok's) **oCPM** ("optimized CPM") is the clearest evidence that
the billing-unit/auction-currency distinction is real: the advertiser is
nominally billed per 1,000 impressions, but the platform's pCTR/pCVR models
choose *which* impressions to fill toward a conversion-style goal — giving
"scaling capabilities close to CPM" with "effort on the order of CPC/CPE
campaigns"
[[wiki/sources/pay-per-pricing-models-digital-advertising-martech.md]]
*(blog post)*. Google's Smart Bidding strategies (Target CPA, Maximize
Conversions) achieve the mirror-image result starting from CPC: the advertiser
sets a conversion-oriented goal, and Google's models decide the per-auction
CPC bid [[wiki/concepts/google-ad-rank-ltv-scoring.md]]. Both platforms,
in other words, are converging toward "tell us your goal; we'll handle the
unit-economics" — they just kept their original billing labels (CPC for
Google Search, CPM/oCPM for Meta Feed) as the user-facing framing.

## Summary

| | Google Search | Meta Feed |
|---|---|---|
| Default billing unit | CPC | CPM / oCPM |
| Format heritage | Paid search (Goto.com 1998 -> Google 2002) | Display (DoubleClick 1996) |
| User context | High intent (typed a query) | Discovery / scrolling |
| Risk of an unproductive impression borne by | Platform (no click = no revenue) | Advertiser (impression billed regardless of action) |
| Internal auction currency | eCPM = bid x pCTR (LTV) [[wiki/concepts/google-ad-rank-ltv-scoring.md]] | Total Value = Bid x EAR + Quality [[wiki/synthesis/meta-ad-ranking.md]] |
| Hybrid bridge | Smart Bidding (Target CPA/ROAS over a CPC base) | oCPM (conversion-optimized delivery over a CPM base) |

## Open Questions

- Open question: As both platforms push advertisers toward fully automated
  "tell us your goal" bidding (Performance Max, Advantage+), does the
  advertiser-facing billing unit (CPC vs. CPM) retain any practical meaning
  beyond legacy reporting conventions, or is it on a path to becoming purely
  cosmetic?

## Related Pages

- [[wiki/synthesis/bidding-types.md]] — pricing models, bid strategies, and auction mechanisms
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]] — Google's eCPM/LTV formula
- [[wiki/synthesis/meta-ad-ranking.md]] — Meta's Total Value formula
- [[wiki/sources/pay-per-pricing-models-digital-advertising-martech.md]] — history and risk-allocation framing for CPM/CPC/CPA
- [[wiki/synthesis/what-is-a-conversion.md]] — pCVR and conversion-based bidding
