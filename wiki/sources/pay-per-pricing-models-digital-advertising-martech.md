---
title: "Pay Per What? Choosing Pricing Models in Digital Advertising"
type: "source_summary"
sources:
  - "web/pay-per-pricing-models-digital-advertising-martech.md"
status: "current"
source_type: "blog_post"
processing_status: "processed"
ingest_count: 1
created: "2026-06-10"
last_updated: "2026-06-10"
---

# Pay Per What? Choosing Pricing Models in Digital Advertising

**Source type:** `blog_post`

## Summary

A MarTech industry explainer on the history and economics of digital ad
pricing models. Traces **CPM** to 1995-96 (Netscape/Infoseek/DoubleClick),
becoming the standard for display, and **CPC** to Goto.com (1998), formally
adopted by Google in 2002 and standard for paid search ever since. Frames the
CPM-vs-CPC-vs-CPA choice as a **risk allocation** problem: clicks are frequent,
immediate, and predictable, while conversions are rare, delayed, and harder to
predict — so CPM is lowest-risk for the platform/publisher, CPC is
intermediate, and CPA is highest-risk for the platform. Introduces the
**eCPM (effective cost-per-mille)** normalization that lets an auction compare
CPC and CPA bids against CPM bids on a common basis: `eCPM = CPC x pCTR x 1000`
and `eCPM = CPA x pCVR x pCTR x 1000`
[[raw/web/pay-per-pricing-models-digital-advertising-martech.md]].

## Key Claims

| Claim | Status |
|---|---|
| CPM became standard for display advertising via DoubleClick (1996) | Stated |
| CPC was pioneered by Goto.com (1998), adopted by Google (2002), standard for paid search since | Stated |
| CPM is lowest-risk for the platform; CPC is intermediate; CPA is highest-risk for the platform | Stated |
| Auctions normalize CPC/CPA bids to eCPM via predicted CTR/CVR to compare against CPM bids | Stated |
| Facebook's oCPM is a hybrid: CPM-like scale with CPC/CPE-like effort | Stated |

## Relevance to Ads Ranking

This is the historical/economic complement to the wiki's existing
mechanics-focused pages on pricing models
[[wiki/synthesis/bidding-types.md]] and Google's production Ad Rank formula
[[wiki/concepts/google-ad-rank-ltv-scoring.md]]. The eCPM normalization
described here is the same transformation Google's `eCPM = bid x pCTR`
performs inside its LTV score, and the risk-allocation framing directly
explains why search platforms (high, predictable click-through) default to
CPC while feed/display platforms (lower per-impression predictability of the
ultimate objective) default to CPM/oCPM.

## Related Pages

- [[wiki/synthesis/why-does-google-charge-per-click-while-meta-charges-per-impression.md]]
- [[wiki/synthesis/bidding-types.md]]
- [[wiki/concepts/google-ad-rank-ltv-scoring.md]]
- [[wiki/synthesis/meta-ad-ranking.md]]
