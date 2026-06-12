---
title: "Google Ad Rank and LTV Scoring"
type: "concept"
sources:
  - "web/google-ad-rank-briefing-paper.md"
  - "web/edelman-ostrovsky-schwarz-gsp-auction.md"
  - "web/rgsp-randomized-second-price-explained.md"
status: "draft"
created: "2026-06-08"
last_updated: "2026-06-09"
---

# Google Ad Rank and LTV Scoring

**Ad Rank** is Google's system for selecting and ranking search ads on the SERP. It determines which ads appear, in what order, and at what price.

## LTV Score

Ads are scored by their estimated **Long-Term Value (LTV)** — the net benefit to Google (and ecosystem health) of showing the ad:

![concepts-google-ad-rank-ltv-scoring-diagram-1](/assets/concepts-google-ad-rank-ltv-scoring-diagram-1.svg)

### Components

| Signal | Role |
|---|---|
| **pCTR** (predicted click-through rate) | Most important quality metric. Normalized to remove positional bias. |
| **pCQ** (predicted creative quality) | Measures ad copy quality; avoids rewarding low-quality creative that might get short-term clicks. |
| **pLQ** (predicted landing page quality) | Measures post-click user experience on the advertiser's site. |
| **Max CPC** (advertiser bid) | Maximum per-click cost the advertiser is willing to pay. |

**Inverse relationship:** Higher quality enables lower bids to win; lower quality requires higher bids. This incentivizes ad quality improvement.

## Eligibility

Only ads with **LTV > 0** are eligible. Thresholds differ by slot (top vs. bottom) and can be dynamically adjusted based on related auctions.

## Pricing

- **Actual CPC** = minimum amount needed to: (1) clear the LTV > 0 threshold, and (2) beat the next-highest competitor's LTV score
- **Reserve price**: when no competitor passes the threshold, the winner pays the minimum bid that achieves LTV > 0
- **Second-price**: when competitors exist, the winner pays enough to beat the next competitor
- Pricing follows the [[wiki/concepts/randomized-gsp-rgsp.md|**rGSP**]] (Randomized General Second-Price Auction) mechanism since January 2019: when top contenders' LTV scores are close enough, the slot winner is chosen **at random** from that group rather than always being the single highest-LTV ad, and the winner pays the next-highest qualifying bid plus $0.01

*Inference: Reserve pricing applies to a significant share of clicks, especially for singleton ads (only one ad shown on the SERP). Precise percentages were redacted in the public filing.* — [[wiki/sources/google-ad-rank-briefing.md]] *(other)*

## Relationship to GSP Theory

[[wiki/concepts/generalized-second-price-auction.md]] describes GSP as ranking by `bid × quality score` with winners paying the next competitor's adjusted bid. Google's production system differs in two ways:

1. **Cost side of LTV**: eCPM minus costs (pCQ, pLQ penalties) — not just `bid × pCTR`
2. **Threshold/reserve pricing**: the "next competitor" rule applies only when competitors clear the threshold; otherwise, reserve pricing governs

## Automated Bidding

Advertisers can use **Smart Bidding** where ML sets bids at query time based on auction-time signals (device, location, time, remarketing lists, etc.) to meet advertiser goals:

| Strategy | Goal |
|---|---|
| Target CPA | Maximize conversions at target cost-per-acquisition |
| Target ROAS | Maximize conversion value at target return-on-ad-spend |
| Maximize Clicks | Get as many clicks as budget allows |
| Maximize Conversions | Get as many conversions as budget allows |
| Enhanced CPC | Adjust manual bids to increase conversion volume |
| Target Impression Share | Reach a specified fraction of targeted queries |

## Open Questions

- How does rGSP randomization interact with the equilibrium properties proven for standard GSP?
- What optimization objective does the LTV formula optimize — short-term revenue, long-term platform health, or a weighted combination?
- Can the LTV framework extend beyond search to display/social advertising?

## Related Pages

- [[wiki/sources/google-ad-rank-briefing.md]]
- [[wiki/concepts/generalized-second-price-auction.md]]
- [[wiki/synthesis/second-price-auction.md]]
- [[wiki/concepts/randomized-gsp-rgsp.md]] — dedicated page on the rGSP randomization mechanism, revenue impact, and DOJ trial findings
- [[wiki/concepts/ordinal-regression-loss.md]] — if pCQ/pLQ quality components are represented as discrete ordered tiers, ordinal regression losses (CORAL/CORN) are a candidate training objective for them
