---
title: "About Bid and Budget Pacing (Meta Business Help Center)"
type: "source_summary"
sources:
  - "web/meta-bid-and-budget-pacing.md"
source_url: "https://www.facebook.com/business/help/571961726580148"
status: "draft"
source_type: "official_documentation"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# About Bid and Budget Pacing (Meta Business Help Center)

**Source:** Meta Business Help Center, "About Bid and Budget Pacing"

**Source type:** `official_documentation` *(content recovered via search-result
snippets — direct page fetch returned only the title; see
[[raw/web/meta-bid-and-budget-pacing.md]] for provenance note)*

## Summary

Meta's documentation describes **bid pacing and budget pacing as one process**:
the system adjusts either the bid value submitted to an auction or which
auctions to enter, based on remaining budget and remaining flight time. The
mechanism is a **pacing multiplier** applied directly to the ad's "total
value" in the auction — the same total-value term composed of the
advertiser's bid, the predicted action rate, and ad quality
[[raw/web/meta-bid-and-budget-pacing.md]].

## Key Claims

| Claim | Status |
|---|---|
| "Budget pacing and bid pacing are one process" — Meta adjusts the bid or which auctions to enter based on remaining budget/time | Stated (official documentation) |
| Pacing operates per-auction: raising/lowering the bid, or skipping an auction entirely | Stated |
| A "pacing multiplier" adjusts the ad's "total value" (advertiser bid x estimated action rate x ad quality) used in the auction | Stated |
| Advertiser-set bid multipliers (value rules) and Meta's pacing multiplier both modify the same total-value term and can interact | Stated (third-party doc, Sprinklr) |

## Relevance to Ads Ranking

This directly addresses the
[[wiki/synthesis/ad-pacing.md]] /
[[wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md]] open
question on how tightly pacing and bid-strategy are coupled at Meta: per
Meta's own documentation, they are **not separable systems** that interact
only through a submitted bid — pacing is implemented as a multiplicative term
*inside* the same auction-value calculation that the bid strategy (Cost Cap,
Bid Cap, Lowest Cost) also feeds into
[[wiki/concepts/google-ad-rank-ltv-scoring.md]].

## Open Questions

- Open question: no source found gives the control-loop details for the
  pacing multiplier itself — how frequently it is recalculated, what signals
  (delivery curve vs. target, time-of-day demand) drive it, or whether it
  uses a PID/MPC-style controller comparable to the one described in
  [[wiki/synthesis/ad-pacing.md]] for Google's KDD 2015 system.

## Related Pages

- [[wiki/synthesis/ad-pacing.md]]
- [[wiki/synthesis/what-are-the-components-of-an-ad-ranking-system.md]]
- [[wiki/sources/google-marketing-live-2026-bidding-budgeting.md]]
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
