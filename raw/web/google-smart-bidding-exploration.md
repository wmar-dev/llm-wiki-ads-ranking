# Smart Bidding Exploration (Google Ads, 2025)

**Source URLs:**
- https://blog.google/products/ads-commerce/smart-bidding-exploration-ai/ (announcement)
- https://support.google.com/google-ads/answer/15489627 (official help page)

**Source type:** official_documentation

---

## What it is

Announced May 2025 as Google's "biggest update to bidding in over a decade."
Smart Bidding Exploration gives Target-ROAS Smart Bidding a **dual mandate**:

1. Continue hitting the advertiser's original ROAS target on
   historically-good-performing queries/keywords.
2. Use a **ROAS-target tolerance band (10-30%, advertiser-configurable via a
   slider)** to bid into auctions for queries the campaign has never (or
   rarely) targeted before — "potentially high-performing search queries"
   outside the campaign's established query set.

## Framing: opportunity expansion, not explicit "exploration" terminology

Google's public materials frame this as **expanding the addressable
opportunity set** ("capturing new searches," "a wider range of unique
categories") rather than using bandit/explore-exploit terminology explicitly.
There is no mention of confidence intervals, regret bounds, or arm/reward
formalism. Functionally, however, the mechanism — a tolerance band that
permits temporarily worse-than-target performance in exchange for trying
untested queries/auctions — matches the **explore/exploit tradeoff**
structure of a bandit algorithm, even though Google does not describe it as
one.

## Quantitative results (March-April 2025 global testing)

- **+18%** increase in unique search-query categories with conversions
- **+19%** increase in conversions
- Campaigns require >=15 conversions in the trailing 30 days (ideally several
  in the trailing 7 days) to be eligible
- Advertisers should expect **temporarily reduced ROAS** during exploration,
  controllable via the tolerance slider

## What remains undisclosed

Neither source describes:

- The specific algorithm (no mention of UCB, Thompson Sampling, or any named
  bandit method)
- How/whether the ROAS-tolerance parameter maps to a per-auction bid
  adjustment formula
- Whether "Bidding exploration" (the related onboarding-period bid
  experimentation Google Ads runs for any new Smart Bidding campaign, lasting
  days to weeks) shares any mechanism with Smart Bidding Exploration

---

## Relevance

This is the most direct evidence that Google's Smart Bidding **does**
incorporate an explore/exploit-style mechanism — a tunable tolerance band
that trades short-term ROAS for coverage of untested queries — directly into
its auction-time bidding. But Google does not publicly frame, name, or detail
this as a bandit algorithm, leaving the underlying algorithmic mechanism
(UCB/Thompson/other) undisclosed.
