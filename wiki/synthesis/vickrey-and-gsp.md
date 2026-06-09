---
title: "What Are Vickrey and GSP Auctions?"
type: "synthesis"
sources:
  - "web/edelman-ostrovsky-schwarz-gsp-auction.md"
  - "web/google-ad-rank-briefing-paper.md"
status: "current"
created: "2026-06-08"
last_updated: "2026-06-08"
---

# What Are Vickrey and GSP Auctions?

## Vickrey (Second-Price) Auction

A **Vickrey auction** (also called a **second-price auction**) is a sealed-bid mechanism where the highest bidder wins but pays the second-highest bid. Formalized by economist William Vickrey in 1961 (Nobel Prize in Economics).

![synthesis-vickrey-and-gsp-diagram-1](/assets/synthesis-vickrey-and-gsp-diagram-1.svg)

**Key property — incentive compatibility**: truth-telling is a dominant strategy. Overbidding risks paying more than value; underbidding risks losing a profitable win. Your bid only determines *whether* you win, not *how much* you pay — the price is set by others.

## Generalized Second-Price (GSP) Auction

GSP extends the Vickrey idea to **multiple ad slots**. It is the mechanism used by Google, Meta, and other ad platforms to allocate sponsored positions. [[wiki/sources/edelman-ostrovsky-schwarz-gsp-auction.md]]

![synthesis-vickrey-and-gsp-diagram-2](/assets/synthesis-vickrey-and-gsp-diagram-2.svg)

Advertisers bid a **cost-per-click (CPC)**. Ads are ranked by `bid × quality score` (a relevance signal). Each winner pays the **minimum needed to hold their slot** — derived from the next competitor's adjusted bid.

## Critical Differences

| Property | Vickrey (single item) | GSP (multiple slots) |
|---|---|---|
| Dominant strategy | Truth-telling | **Not** dominant strategy |
| Nash equilibrium | Truth-telling | Locally envy-free equilibrium |
| Incentive compatibility | Fully strategy-proof | Strategic underbidding is rational |
| Platform revenue vs VCG | Equal | **Higher** |

GSP lacks the Vickrey auction's dominant-strategy truthfulness. Bidders can benefit from shading bids below true value. However, GSP has a unique **locally envy-free equilibrium** (where no advertiser wants to swap positions with an adjacent competitor at that competitor's price) that yields the same advertiser payoffs as VCG — while generating higher platform revenue.

## Why GSP Exists

- **Higher revenue**: GSP generates strictly more revenue for the platform than a VCG mechanism [[wiki/sources/edelman-ostrovsky-schwarz-gsp-auction.md]] *(peer_reviewed)*
- **Operational simplicity**: No need to compute externalities across all bidders
- **Quality weighting**: The bid × quality score ranking aligns advertiser incentives with user relevance

## Production Reality vs Theory

Google's actual Ad Rank system ([[wiki/concepts/google-ad-rank-ltv-scoring.md]]) differs from the textbook GSP model in three ways:

1. **LTV scoring**: ranking uses `LTV = eCPM - costs` (including creative quality and landing page penalties), not just `bid × quality score`
2. **Reserve pricing**: when no competitor clears the quality threshold, the winner pays the reserve price — not the next competitor's bid
3. **rGSP**: Google launched a randomized variant of GSP globally in January 2019 [[wiki/sources/google-ad-rank-briefing.md]]

Meta's auction ([[wiki/synthesis/meta-ad-ranking.md]]) follows the same GSP principles with a different ranking formula: Total Value = (Bid × Estimated Action Rate) + Ad Quality.

## Why They Matter for Ads Ranking

Second-price logic is the foundation of nearly all CPC/CPM pricing in search, social, and programmatic advertising. The key intuitions:

- Your payment depends on **competition**, not your own bid
- **Quality weighting** means a lower bid with higher relevance can beat a higher bid
- **Reserve prices** mean the platform can set a floor even in uncompetitive auctions
- Platforms prefer GSP over Vickrey/VCG because it generates **more revenue** while maintaining reasonable efficiency

## Related Pages

- [[wiki/synthesis/second-price-auction.md]] — deeper dive on second-price mechanics and revenue equivalence
- [[wiki/concepts/generalized-second-price-auction.md]] — GSP concept page with equilibrium analysis
- [[wiki/sources/edelman-ostrovsky-schwarz-gsp-auction.md]] — the seminal AER 2007 paper *(peer_reviewed)*
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]] — Google's production Ad Rank with LTV scoring
