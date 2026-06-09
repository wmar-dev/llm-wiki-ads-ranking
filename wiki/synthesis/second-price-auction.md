---
title: "What Is a Second Price Auction?"
type: "synthesis"
sources:
  - "web/edelman-ostrovsky-schwarz-gsp-auction.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# What Is a Second Price Auction?

A **second price auction** (also called a **Vickrey auction**) is a sealed-bid auction mechanism where the highest bidder wins but pays the *second-highest bid* — not their own. It was formalized by economist William Vickrey in 1961, for which he later received the Nobel Prize in Economics.

## Mechanics

![synthesis-second-price-auction-diagram-1](/assets/synthesis-second-price-auction-diagram-1.svg)

1. Each bidder submits a sealed bid without seeing others' bids.
2. The highest bidder wins the item.
3. The winner pays the amount of the **second-highest bid** (the highest losing bid).

## The Key Property: Incentive Compatibility

The second price rule makes **truthful bidding a dominant strategy** — bidding your true value for the item is always at least as good as any other bid, regardless of what others bid.

**Intuition:**

- If you overbid above your true value, you risk winning and paying more than the item is worth to you.
- If you underbid below your true value, you risk losing an auction you would have profited from.
- At your true value, you win when the item is worth winning and lose when it isn't — your payment is always determined by someone else's bid, not yours.

This property is called **incentive compatibility** or **strategy-proofness**, and is the central reason second price auctions are studied and deployed.

## Generalized Second Price (GSP) in Online Advertising

Search and display advertising platforms adapted this mechanism into the **Generalized Second Price (GSP) auction**, which handles multiple ad slots simultaneously:

![synthesis-second-price-auction-diagram-2](/assets/synthesis-second-price-auction-diagram-2.svg)

- Advertisers bid a **cost-per-click (CPC)**.
- Slots are ranked by `bid × Quality Score` (Google) or similar relevance signal.
- Each winner pays the **minimum bid needed to hold their slot** — effectively the next competitor's adjusted bid divided by their own quality score.

GSP is *not* exactly a Vickrey auction (it covers multiple units), but it inherits the spirit of second-price payment and approximates incentive-compatible bidding in practice.

## Revenue Equivalence

Under standard assumptions (independent private values, risk-neutral bidders), the **Revenue Equivalence Theorem** states that first-price and second-price auctions yield the same expected revenue to the seller. The difference is in *when* bidders shade their bids:

- **First price**: bidders shade bids below true value (strategic underbidding).
- **Second price**: bidders bid their true value (no shading needed).

## Why It Matters for Ads Ranking

| Property | Relevance to Ads Systems |
| --- | --- |
| Truthful bidding | Advertisers reveal true willingness-to-pay, giving the platform accurate demand signals |
| Quality weighting | GSP multiplies bid × quality score, aligning payout with user relevance |
| Threshold pricing | Winner pays the "clearing price" — the minimum to beat the next competitor |
| Auction theory foundation | Underpins most CPC/CPM pricing logic in Google Ads, Meta Ads, RTB exchanges |

## Limitations and Criticisms

- **GSP is not fully incentive-compatible** — in multi-slot settings, bidders can benefit from strategic underbidding, making it an approximation rather than a true Vickrey mechanism.
- **Reserve prices** complicate truthfulness: if a reserve price exceeds the second-highest bid, the winner pays the reserve, not the second-highest bid.
- **Click fraud and low-quality traffic** distort the signal the auction is meant to surface.
- Modern platforms increasingly move toward **first-price auction hybrids** (e.g., header bidding in programmatic display), where second-price assumptions no longer hold.

## Open Questions

- How do platforms calibrate quality scores to preserve auction efficiency?
- What happens to incentive compatibility when machine learning models predict click-through rates as part of the ranking signal?

## Related Pages

- [[wiki/sources/overlapping-experiment-infrastructure.md]] — experimentation infrastructure for testing auction parameter changes at scale
- [[wiki/sources/google-ad-rank-briefing.md]] — Google's internal description of Ad Rank with LTV scoring, thresholds, and rGSP *(regulatory filing)*
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]] — production Ad Rank system with cost-side terms and reserve pricing
