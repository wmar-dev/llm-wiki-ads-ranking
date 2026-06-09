---
title: "Generalized Second-Price Auction (GSP)"
type: "concept"
sources:
  - "web/edelman-ostrovsky-schwarz-gsp-auction.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# Generalized Second-Price Auction (GSP)

The **Generalized Second-Price (GSP) auction** is the mechanism used by search engines to allocate sponsored ad slots to advertisers bidding on keywords. It is the multi-slot analog of the Vickrey second-price auction, but with importantly different theoretical properties.

## How It Works

1. Advertisers submit a cost-per-click (CPC) bid.
2. Slots are ranked by `bid × quality score` (Google) or equivalent relevance signal.
3. The winner of slot *k* pays the **minimum price needed to hold that slot** — derived from the next-ranked competitor's adjusted bid divided by the winner's quality score.

```mermaid
sequenceDiagram
    participant Adv as Advertiser
    participant Eng as Search Engine
    participant Ranker as Auction Engine

    Adv->>Eng: Submit CPC bid
    Eng->>Ranker: Rank by bid × quality score
    Ranker->>Adv: Assign slot; charge next bidder's clearing price
```

## Relationship to Vickrey (Second-Price) Auction

| Property | Vickrey (single item) | GSP (multiple slots) |
|---|---|---|
| Dominant strategy | Truth-telling | **Not** dominant strategy |
| Nash equilibrium | Truth-telling | Locally envy-free equilibrium |
| Payoff vs. VCG | Identical | Identical at LEF equilibrium |
| Platform revenue vs. VCG | Equal | **Higher** |

Key result from [[wiki/sources/edelman-ostrovsky-schwarz-gsp-auction.md]]: GSP does not have a dominant-strategy equilibrium, and truthful bidding is not a Nash equilibrium. However, its **locally envy-free equilibrium** (the stable outcome of the corresponding generalized English auction) yields the same advertiser payoffs as VCG — while generating more revenue for the platform.

## Locally Envy-Free Equilibrium

A bidding profile is **locally envy-free** if no advertiser prefers to swap positions with the immediately adjacent competitor at that competitor's current price. This is the theoretically predicted stable outcome in the dynamic, repeated-bidding environment of keyword auctions.

## Why GSP Over VCG?

- GSP generates strictly **higher expected revenue** for the platform than a Vickrey-Clarke-Groves mechanism.
- VCG requires computing externalities across all advertisers; GSP is operationally simpler.
- Despite lacking dominant-strategy truthfulness, GSP equilibria recover VCG-level efficiency in welfare.

## Limitations

- Strategic underbidding is rational — advertisers shade bids below true value.
- Quality score models (ML-based CTR prediction) introduce additional complexity not captured by the original GSP theory.
- Modern programmatic display advertising increasingly uses **first-price auction** formats (header bidding), where GSP assumptions do not hold.

## Related Pages

- [[wiki/synthesis/second-price-auction.md]]
- [[wiki/sources/edelman-ostrovsky-schwarz-gsp-auction.md]]
