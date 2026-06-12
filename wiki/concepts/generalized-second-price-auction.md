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

![concepts-generalized-second-price-auction-diagram-1](/assets/concepts-generalized-second-price-auction-diagram-1.svg)

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
- Google's production Ad Rank system uses an **LTV (Long-term Value) Score** that includes cost-side terms (creative quality, landing page quality) absent from the theoretical GSP model.
- Google launched **rGSP (Randomized General Second-Price Auction)** globally in January 2019, adding randomization to the mechanism.
- Reserve pricing applies when no competitor clears the ad quality threshold — a significant fraction of real-world auctions.
- Modern programmatic display advertising increasingly uses **first-price auction** formats (header bidding), where GSP assumptions do not hold.

## Related Pages

- [[wiki/synthesis/simple-ads-auction-python.md]] — Python implementation of GSP's bid x quality ranking and minimum-to-hold-position pricing
- [[wiki/synthesis/second-price-auction.md]]
- [[wiki/sources/edelman-ostrovsky-schwarz-gsp-auction.md]]
- [[wiki/sources/google-ad-rank-briefing.md]]
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
