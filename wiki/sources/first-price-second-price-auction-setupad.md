---
title: "First-Price vs Second-Price Auction in Programmatic Advertising"
type: "source_summary"
sources:
  - "web/first-price-second-price-auction-setupad.md"
status: "current"
created: "2026-06-09"
last_updated: "2026-06-09"
source_type: "blog_post"
---

# First-Price vs Second-Price Auction in Programmatic Advertising

**Source:** Setupad Blog, "First-Price vs Second-Price Auction | Differences Explained"

**Source type:** `blog_post` (ad tech vendor)

**Processing:** single-pass

---

## Summary

Explains the two auction-clearing rules used in programmatic real-time
bidding (RTB) — first-price (pay your exact bid) and second-price (pay
$0.01 above the runner-up) — and the 2019 industry-wide shift to first-price
driven by header bidding.

## Key Claims

- First-price: winner pays their exact bid (the clearing price). Second-price:
  winner pays $0.01 above the second-highest bid
  [[raw/web/first-price-second-price-auction-setupad.md]] *(blog post)*.
- Google Ad Manager switched display/video inventory from second-price to
  first-price auctions in 2019, driven by header bidding making second-price
  auctions hard to optimize across multiple simultaneous exchanges
  [[raw/web/first-price-second-price-auction-setupad.md]] *(blog post)*.
- 78% of publishers reported higher revenue after switching to first-price;
  trade-off is "bid shading" by buyers, which can divert up to ~20% of
  publisher revenue if floor prices aren't set
  [[raw/web/first-price-second-price-auction-setupad.md]] *(blog post)*.
- This is the programmatic/display counterpart to the GSP (generalized
  second-price) auctions used in search and feed ads
  [[wiki/synthesis/vickrey-and-gsp.md]] [[wiki/concepts/generalized-second-price-auction.md]].

## Related Pages

- [[wiki/synthesis/bidding-types.md]] — unifying taxonomy of bidding types
- [[wiki/synthesis/vickrey-and-gsp.md]] — Vickrey/GSP second-price theory
- [[wiki/concepts/generalized-second-price-auction.md]] — GSP mechanics
- [[wiki/synthesis/why-ads-have-auctions.md]] — economic rationale for ad auctions
