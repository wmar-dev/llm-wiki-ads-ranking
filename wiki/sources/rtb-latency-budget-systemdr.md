---
title: "Real-Time Ad Bidding Systems (RTB): Designing for <100ms Responses"
type: "source_summary"
sources:
  - "web/rtb-latency-budget-systemdr.md"
status: "draft"
source_type: "blog_post"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# Real-Time Ad Bidding Systems (RTB): Designing for <100ms Responses

**Source type:** `blog_post`

## Summary

A practitioner explainer of the latency budget governing real-time bidding (RTB)
auctions: an overall **80-120ms** cycle (industry standard 100-300ms including
RTT), broken down as ~10ms publisher→exchange transmission, ~15ms exchange
processing/fanout, **~50ms DSP bid calculation** (the critical constraint), ~15ms
response aggregation/auction logic, and ~10ms network return. OpenRTB enforces
this with hard cutoffs (408 Timeout) — late bids are dropped, not scored late.
Systems stay within budget primarily via aggressive pre-computation/caching
(hot user-profile and targeting-rule caches) and "skip-on-timeout" policies for
auxiliary signals [[raw/web/rtb-latency-budget-systemdr.md]].

## Key Claims

| Claim | Status |
|---|---|
| RTB auction cycle is ~80-120ms total, industry standard 100-300ms with RTT | Stated |
| DSP bid-calculation window (~50ms) is the dominant share of the budget | Stated |
| OpenRTB drops late bids via hard timeout (408), no late scoring | Stated |
| Systems rely on pre-computed caches, not on-the-fly computation, to fit the budget | Stated |

## Relevance to Ads Ranking

This gives the **programmatic/RTB-side** latency budget, complementary to the
**owned-platform** figures already in the wiki: Google's Ad Rank auction
(~100ms, [[wiki/synthesis/meta-ad-ranking.md]]) and Meta's 200-300ms end-to-end
ranking [[wiki/synthesis/meta-ad-ranking.md]]. The ~50ms DSP compute window is
directly comparable to the per-stage budgets in the two-tower retrieval/ranking
pipeline [[wiki/synthesis/two-tower-factorized-models.md]] — both converge on the
same order-of-magnitude constraint (tens of milliseconds per stage) despite very
different architectures.

## Related Pages

- [[wiki/synthesis/what-is-the-latency-budget-for-ad-ranking.md]]
- [[wiki/synthesis/two-tower-factorized-models.md]]
- [[wiki/synthesis/meta-ad-ranking.md]]
